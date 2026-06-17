"""
wp-net-indexing.py
──────────────────
wooriwin.net 전체 URL (메인 + 카테고리 + 포스트) Google Indexing API 제출.

사용법:
  python scripts/wp-net-indexing.py           # 전체 제출
  python scripts/wp-net-indexing.py --new     # WP에서 최근 N개 포스트만 제출
"""

import os
import sys
import time
import json
import argparse
import requests
import cloudscraper
import base64
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))

WP_URL          = os.environ.get("WP_NET_URL", "https://wooriwin.net")
WP_USER         = os.environ.get("WP_NET_USER", "")
WP_APP_PASSWORD = os.environ.get("WP_NET_APP_PASSWORD", "")

BASE_DIR             = os.path.join(os.path.dirname(__file__), "..")
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "keys", "wooriwin-indexing.json")
SCOPES               = ["https://www.googleapis.com/auth/indexing"]

CATEGORY_SLUGS = [
    "casino-news",
    "toto-news",
    "slot-news",
    "industry-trends",
    "macau-casino",
    "philippines-casino",
    "vietnam-casino",
    "cambodia-casino",
    "overseas-casino",
]


def get_scraper():
    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "mobile": False}
    )
    creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
    scraper.headers.update({"Authorization": f"Basic {creds}"})
    return scraper


def get_all_post_urls(recent: int = 0) -> list:
    scraper = get_scraper()
    urls = []
    page = 1
    params = {"per_page": 100, "_fields": "link", "orderby": "date", "order": "desc"}
    while True:
        try:
            res = scraper.get(f"{WP_URL}/wp-json/wp/v2/posts",
                              params={**params, "page": page}, timeout=15)
            if res.status_code in (400, 404):
                break
            data = res.json()
            if not data:
                break
            for p in data:
                urls.append(p["link"])
            if recent and len(urls) >= recent:
                return urls[:recent]
            page += 1
            time.sleep(0.3)
        except Exception as e:
            print(f"  ⚠️ 포스트 조회 실패 (page {page}): {e}")
            break
    return urls


def build_url_list(recent: int = 0) -> list:
    urls = []

    if not recent:
        # 메인
        urls.append(f"{WP_URL}/")
        # 카테고리 페이지
        for slug in CATEGORY_SLUGS:
            urls.append(f"{WP_URL}/category/{slug}/")

    # 포스트
    print("  📄 WP 포스트 URL 조회 중...")
    post_urls = get_all_post_urls(recent)
    urls.extend(post_urls)
    print(f"  → 총 {len(urls)}개 URL 수집")
    return urls


def submit_urls(urls: list):
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"❌ 서비스 계정 키 없음: {SERVICE_ACCOUNT_FILE}")
        return
    try:
        with open(SERVICE_ACCOUNT_FILE, encoding="utf-8") as f:
            json.load(f)
    except json.JSONDecodeError:
        print("❌ 서비스 계정 키 형식 오류")
        return

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("indexing", "v3", credentials=credentials)

    success, fail = 0, 0
    for i, url in enumerate(urls):
        try:
            service.urlNotifications().publish(
                body={"url": url, "type": "URL_UPDATED"}
            ).execute()
            print(f"  ✅ [{i+1}/{len(urls)}] {url}")
            success += 1
        except HttpError as e:
            print(f"  ❌ [{i+1}/{len(urls)}] {url} → HTTP {e.resp.status}: {e.reason}")
            fail += 1
        time.sleep(1)

    print(f"\n완료: 성공 {success}개 / 실패 {fail}개")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--new", type=int, default=0,
                        help="최근 N개 포스트만 제출 (메인·카테고리 제외)")
    args = parser.parse_args()

    print("=" * 50)
    print("  WooriWin.net Google Indexing API 제출")
    print("=" * 50)

    urls = build_url_list(recent=args.new)
    if not urls:
        print("제출할 URL 없음"); return

    print(f"\n📡 총 {len(urls)}개 URL 제출 시작...")
    submit_urls(urls)


if __name__ == "__main__":
    main()
