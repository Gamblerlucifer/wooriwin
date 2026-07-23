"""
gist-post.py
──────────────────
wooriwin.com 포스트를 소재로 제미나이가 완전히 새로 쓴 글을, 앵커 텍스트 백링크와 함께
GitHub Gist에 마크다운으로 발행.

사전 준비:
  1. https://github.com/settings/tokens 에서 Personal Access Token 발급 (gist 권한만 체크)
  2. .env.local에 GITHUB_GIST_TOKEN=발급받은토큰 추가

사용법:
  python scripts/gist-post.py            # 1개 발행
  python scripts/gist-post.py --count 3  # 3개 발행
"""

import os
import sys
import re
import time
import argparse
import requests
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.path.insert(0, os.path.dirname(__file__))
from backlink_content import generate_backlink_article

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))

GITHUB_GIST_TOKEN = os.environ.get("GITHUB_GIST_TOKEN", "")

BASE_DIR             = os.path.join(os.path.dirname(__file__), "..")
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "keys", "wooriwin-indexing.json")
INDEXING_SCOPE       = "https://www.googleapis.com/auth/indexing"

GITHUB_API = "https://api.github.com/gists"


def post_to_gist(title: str, body_markdown: str) -> str:
    filename = re.sub(r"[^a-zA-Z0-9\-]+", "-", title).strip("-")[:60] or "wooriwin-post"

    res = requests.post(GITHUB_API, headers={
        "Authorization": f"Bearer {GITHUB_GIST_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    }, json={
        "description": title[:255],
        "public": True,
        "files": {f"{filename}.md": {"content": f"# {title}\n\n{body_markdown}\n"}},
    }, timeout=15)
    res.raise_for_status()
    return res.json()["html_url"]


def submit_to_indexing(url: str):
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"  ⚠️ 서비스 계정 키 없음, 색인 제출 스킵: {SERVICE_ACCOUNT_FILE}")
        return
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=[INDEXING_SCOPE]
    )
    service = build("indexing", "v3", credentials=credentials)
    try:
        service.urlNotifications().publish(body={"url": url, "type": "URL_UPDATED"}).execute()
        print(f"  ✅ Indexing API 제출 완료: {url}")
    except HttpError as e:
        print(f"  ❌ Indexing API 제출 실패: HTTP {e.resp.status}: {e.reason}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--count", type=int, default=1, help="발행할 글 개수")
    args = parser.parse_args()

    if not GITHUB_GIST_TOKEN:
        print("❌ GITHUB_GIST_TOKEN이 .env.local에 없습니다.")
        print("   https://github.com/settings/tokens 에서 gist 권한 토큰 발급 후 추가하세요.")
        return

    print("=" * 50)
    print("  GitHub Gist 자동 포스팅 (wooriwin.com 백링크)")
    print("=" * 50)

    for i in range(args.count):
        print(f"\n[{i+1}/{args.count}] 글 생성 중...")
        article = generate_backlink_article("GitHub Gist")
        print(f"  📝 {article['title']} (앵커: \"{article['anchor_text']}\")")

        gist_url = post_to_gist(article["title"], article["body_markdown"])
        print(f"  ✅ 발행 완료: {gist_url}")

        submit_to_indexing(gist_url)
        time.sleep(1)


if __name__ == "__main__":
    main()
