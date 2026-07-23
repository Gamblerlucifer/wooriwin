"""
telegraph-post.py
──────────────────
wooriwin.com 포스트를 소재로 제미나이가 완전히 새로 쓴 글을, 앵커 텍스트 백링크와 함께
텔레그래프(telegra.ph)에 발행. 가입 절차 없이 API 호출만으로 계정 생성(최초 1회, 로컬 저장).

사용법:
  python scripts/telegraph-post.py            # 1개 발행
  python scripts/telegraph-post.py --count 3  # 3개 발행
"""

import os
import sys
import json
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

BASE_DIR              = os.path.join(os.path.dirname(__file__), "..")
TOKEN_FILE            = os.path.join(BASE_DIR, "keys", "telegraph-token.json")
SERVICE_ACCOUNT_FILE  = os.path.join(BASE_DIR, "keys", "wooriwin-indexing.json")
INDEXING_SCOPE        = "https://www.googleapis.com/auth/indexing"

TELEGRAPH_API = "https://api.telegra.ph"
AUTHOR_NAME   = "wooriwin"
AUTHOR_URL    = "https://wooriwin.com"


def get_telegraph_token() -> str:
    env_token = os.environ.get("TELEGRAPH_ACCESS_TOKEN")
    if env_token:
        return env_token

    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, encoding="utf-8") as f:
            return json.load(f)["access_token"]

    res = requests.post(f"{TELEGRAPH_API}/createAccount", data={
        "short_name": AUTHOR_NAME,
        "author_name": AUTHOR_NAME,
        "author_url": AUTHOR_URL,
    }, timeout=15)
    res.raise_for_status()
    result = res.json()["result"]

    os.makedirs(os.path.dirname(TOKEN_FILE), exist_ok=True)
    with open(TOKEN_FILE, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"  🆕 텔레그래프 계정 생성 완료 (access_token 저장: {TOKEN_FILE})")
    return result["access_token"]


def markdown_to_nodes(body_markdown: str, anchor_text: str, target_url: str) -> list:
    """아주 단순한 마크다운→Telegraph Node 변환. [앵커](url) 링크 1개와 일반 문단만 처리."""
    nodes = []
    link_md = f"[{anchor_text}]({target_url})"
    for para in [p.strip() for p in body_markdown.split("\n\n") if p.strip()]:
        if link_md in para:
            before, after = para.split(link_md, 1)
            children = []
            if before.strip():
                children.append(before.strip())
            children.append({"tag": "a", "attrs": {"href": target_url}, "children": [anchor_text]})
            if after.strip():
                children.append(after.strip())
            nodes.append({"tag": "p", "children": children})
        else:
            nodes.append({"tag": "p", "children": [para]})
    return nodes


def post_to_telegraph(token: str, title: str, body_markdown: str, anchor_text: str, target_url: str) -> str:
    content = markdown_to_nodes(body_markdown, anchor_text, target_url)

    res = requests.post(f"{TELEGRAPH_API}/createPage", json={
        "access_token": token,
        "title": title[:256],
        "author_name": AUTHOR_NAME,
        "author_url": AUTHOR_URL,
        "content": content,
        "return_content": False,
    }, timeout=15)
    res.raise_for_status()
    data = res.json()
    if not data.get("ok"):
        raise RuntimeError(f"Telegraph API 오류: {data}")
    return data["result"]["url"]


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

    print("=" * 50)
    print("  Telegraph 자동 포스팅 (wooriwin.com 백링크)")
    print("=" * 50)

    token = get_telegraph_token()

    for i in range(args.count):
        print(f"\n[{i+1}/{args.count}] 글 생성 중...")
        article = generate_backlink_article("Telegraph")
        target_url = f"https://wooriwin.com/blog/{article['source_slug']}"
        print(f"  📝 {article['title']} (앵커: \"{article['anchor_text']}\")")

        telegraph_url = post_to_telegraph(
            token, article["title"], article["body_markdown"], article["anchor_text"], target_url
        )
        print(f"  ✅ 발행 완료: {telegraph_url}")

        submit_to_indexing(telegraph_url)
        time.sleep(1)


if __name__ == "__main__":
    main()
