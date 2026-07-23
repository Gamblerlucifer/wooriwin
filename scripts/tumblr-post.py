"""
tumblr-post.py
──────────────────
wooriwin.com 포스트를 소재로 제미나이가 완전히 새로 쓴 글을, 앵커 텍스트 백링크와 함께
Tumblr에 발행 (OAuth 1.0a).

사전 준비 (.env.local):
  TUMBLR_CONSUMER_KEY / TUMBLR_CONSUMER_SECRET  — tumblr.com/oauth/apps 앱 등록으로 발급
  TUMBLR_TOKEN / TUMBLR_TOKEN_SECRET            — 앱 목록의 "Explore API"에서 로그인 후 발급
  TUMBLR_BLOG_NAME                              — 블로그 식별자 (예: wooriwin.tumblr.com이면 "wooriwin")

사용법:
  python scripts/tumblr-post.py            # 1개 발행
  python scripts/tumblr-post.py --count 3  # 3개 발행
"""

import os
import sys
import time
import argparse
import requests
import markdown as md_lib
from requests_oauthlib import OAuth1
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.path.insert(0, os.path.dirname(__file__))
from backlink_content import generate_backlink_article

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))

TUMBLR_CONSUMER_KEY    = os.environ.get("TUMBLR_CONSUMER_KEY", "")
TUMBLR_CONSUMER_SECRET = os.environ.get("TUMBLR_CONSUMER_SECRET", "")
TUMBLR_TOKEN           = os.environ.get("TUMBLR_TOKEN", "")
TUMBLR_TOKEN_SECRET    = os.environ.get("TUMBLR_TOKEN_SECRET", "")
TUMBLR_BLOG_NAME       = os.environ.get("TUMBLR_BLOG_NAME", "")

BASE_DIR             = os.path.join(os.path.dirname(__file__), "..")
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "keys", "wooriwin-indexing.json")
INDEXING_SCOPE       = "https://www.googleapis.com/auth/indexing"


def markdown_to_html(text: str) -> str:
    try:
        return md_lib.markdown(text)
    except Exception:
        return "".join(f"<p>{line}</p>" for line in text.split("\n\n") if line.strip())


def post_to_tumblr(title: str, body_markdown: str) -> str:
    auth = OAuth1(TUMBLR_CONSUMER_KEY, TUMBLR_CONSUMER_SECRET, TUMBLR_TOKEN, TUMBLR_TOKEN_SECRET)
    url = f"https://api.tumblr.com/v2/blog/{TUMBLR_BLOG_NAME}.tumblr.com/post"

    res = requests.post(url, auth=auth, data={
        "type": "text",
        "title": title,
        "body": markdown_to_html(body_markdown),
    }, timeout=15)
    res.raise_for_status()
    data = res.json()["response"]
    return f"https://{TUMBLR_BLOG_NAME}.tumblr.com/post/{data['id']}"


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

    missing = [k for k, v in {
        "TUMBLR_CONSUMER_KEY": TUMBLR_CONSUMER_KEY,
        "TUMBLR_CONSUMER_SECRET": TUMBLR_CONSUMER_SECRET,
        "TUMBLR_TOKEN": TUMBLR_TOKEN,
        "TUMBLR_TOKEN_SECRET": TUMBLR_TOKEN_SECRET,
        "TUMBLR_BLOG_NAME": TUMBLR_BLOG_NAME,
    }.items() if not v]
    if missing:
        print(f"❌ .env.local에 다음 값이 없습니다: {', '.join(missing)}")
        return

    print("=" * 50)
    print("  Tumblr 자동 포스팅 (wooriwin.com 백링크)")
    print("=" * 50)

    for i in range(args.count):
        print(f"\n[{i+1}/{args.count}] 글 생성 중...")
        article = generate_backlink_article("Tumblr")
        print(f"  📝 {article['title']} (앵커: \"{article['anchor_text']}\")")

        post_url = post_to_tumblr(article["title"], article["body_markdown"])
        print(f"  ✅ 발행 완료: {post_url}")

        submit_to_indexing(post_url)
        time.sleep(1)


if __name__ == "__main__":
    main()
