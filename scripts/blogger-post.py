"""
blogger-post.py
──────────────────
wooriwin.com 포스트를 소재로 제미나이가 완전히 새로 쓴 글을, 앵커 텍스트 백링크와 함께
Blogger에 발행.

Blogger API는 서비스 계정을 지원하지 않고 실제 사용자 OAuth 인증이 필요합니다.
최초 1회만 브라우저로 로그인하면, 이후에는 저장된 토큰으로 자동 실행됩니다.

사전 준비:
  1. blogger.com에서 블로그 생성 (블로그를 소유한 구글 계정으로)
  2. Google Cloud Console → 사용자 인증 정보 → 기존 OAuth 2.0 클라이언트 ID(데스크톱)의
     JSON을 다운로드해 keys/blogger-oauth-client.json으로 저장
  3. .env.local에 BLOGGER_BLOG_URL=생성한 블로그 URL 추가
  4. 최초 1회 로컬에서 실행 → 브라우저가 열리면 블로그 소유 계정으로 로그인/동의

사용법:
  python scripts/blogger-post.py            # 1개 발행
  python scripts/blogger-post.py --count 3  # 3개 발행
"""

import os
import sys
import re
import time
import argparse
import markdown as md_lib
from dotenv import load_dotenv
from google.oauth2 import service_account
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.path.insert(0, os.path.dirname(__file__))
from backlink_content import generate_backlink_article

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))

BLOGGER_BLOG_URL = os.environ.get("BLOGGER_BLOG_URL", "")

BASE_DIR              = os.path.join(os.path.dirname(__file__), "..")
SERVICE_ACCOUNT_FILE   = os.path.join(BASE_DIR, "keys", "wooriwin-indexing.json")
OAUTH_CLIENT_FILE      = os.path.join(BASE_DIR, "keys", "blogger-oauth-client.json")
OAUTH_TOKEN_FILE       = os.path.join(BASE_DIR, "keys", "blogger-token.json")
INDEXING_SCOPE         = "https://www.googleapis.com/auth/indexing"
BLOGGER_SCOPE          = "https://www.googleapis.com/auth/blogger"


def markdown_to_html(text: str) -> str:
    try:
        return md_lib.markdown(text)
    except Exception:
        # markdown 패키지 미설치 시 최소한의 폴백 (문단만 <p>로 감싸기)
        return "".join(f"<p>{line}</p>" for line in text.split("\n\n") if line.strip())


def get_blogger_credentials() -> Credentials:
    env_token = os.environ.get("BLOGGER_OAUTH_TOKEN")
    if env_token:
        with open(OAUTH_TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(env_token)

    creds = None
    if os.path.exists(OAUTH_TOKEN_FILE):
        creds = Credentials.from_authorized_user_file(OAUTH_TOKEN_FILE, [BLOGGER_SCOPE])

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(OAUTH_CLIENT_FILE):
                raise SystemExit(
                    f"❌ OAuth 클라이언트 파일 없음: {OAUTH_CLIENT_FILE}\n"
                    "   GCP 콘솔 → 사용자 인증 정보 → 데스크톱 OAuth 클라이언트 JSON 다운로드 후 저장하세요."
                )
            flow = InstalledAppFlow.from_client_secrets_file(OAUTH_CLIENT_FILE, [BLOGGER_SCOPE])
            print("  🔐 브라우저가 열립니다 — 블로그 소유 계정으로 로그인/동의해주세요.")
            creds = flow.run_local_server(port=0)

        os.makedirs(os.path.dirname(OAUTH_TOKEN_FILE), exist_ok=True)
        with open(OAUTH_TOKEN_FILE, "w", encoding="utf-8") as f:
            f.write(creds.to_json())
        print(f"  ✅ 토큰 저장 완료: {OAUTH_TOKEN_FILE} (다음부턴 재로그인 불필요)")

    return creds


def get_blog_id(service) -> str:
    result = service.blogs().getByUrl(url=BLOGGER_BLOG_URL).execute()
    return result["id"]


def post_to_blogger(service, blog_id: str, title: str, body_markdown: str) -> str:
    result = service.posts().insert(blogId=blog_id, body={
        "title": title,
        "content": markdown_to_html(body_markdown),
    }).execute()
    return result["url"]


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

    if not BLOGGER_BLOG_URL:
        print("❌ BLOGGER_BLOG_URL이 .env.local에 없습니다.")
        return

    print("=" * 50)
    print("  Blogger 자동 포스팅 (wooriwin.com 백링크)")
    print("=" * 50)

    credentials = get_blogger_credentials()
    blogger = build("blogger", "v3", credentials=credentials)

    try:
        blog_id = get_blog_id(blogger)
    except HttpError as e:
        print(f"❌ 블로그 조회 실패: HTTP {e.resp.status}: {e.reason}")
        return

    for i in range(args.count):
        print(f"\n[{i+1}/{args.count}] 글 생성 중...")
        article = generate_backlink_article("Blogger")
        print(f"  📝 {article['title']} (앵커: \"{article['anchor_text']}\")")

        post_url = post_to_blogger(blogger, blog_id, article["title"], article["body_markdown"])
        print(f"  ✅ 발행 완료: {post_url}")

        submit_to_indexing(post_url)
        time.sleep(1)


if __name__ == "__main__":
    main()
