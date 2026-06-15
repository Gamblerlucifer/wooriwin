"""
notify-indexing.py
───────────────────
generate-post.py가 새로 생성한 포스트 URL을 Google Indexing API
(urlNotifications.publish, type=URL_UPDATED)로 색인 요청.

서비스 계정 키는 GitHub Actions의 "Restore Google Service Account Key" 단계에서
저장소 루트에 wooriwin-indexing.json 으로 미리 복원되어 있어야 함.
"""

import os
import json
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SITE_BASE_URL = "https://wooriwin.com"
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "wooriwin-indexing.json")
NEW_POSTS_FILE = os.path.join(BASE_DIR, "data", ".new-posts-pending.json")

SCOPES = ["https://www.googleapis.com/auth/indexing"]


def main():
    if not os.path.exists(NEW_POSTS_FILE):
        print("⏭️  신규 포스트 없음 — 색인 알림 스킵")
        return

    with open(NEW_POSTS_FILE, encoding="utf-8") as f:
        slugs = json.load(f)

    if not slugs:
        print("⏭️  신규 포스트 없음 — 색인 알림 스킵")
        os.remove(NEW_POSTS_FILE)
        return

    if not os.path.exists(SERVICE_ACCOUNT_FILE) or os.path.getsize(SERVICE_ACCOUNT_FILE) == 0:
        print("⏭️  서비스 계정 키 없음/비어있음 — 색인 알림 스킵")
        return

    try:
        with open(SERVICE_ACCOUNT_FILE, encoding="utf-8") as f:
            json.load(f)
    except json.JSONDecodeError:
        print("⏭️  서비스 계정 키 형식 오류 — 색인 알림 스킵")
        return

    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("indexing", "v3", credentials=credentials)

    print(f"📡 Indexing API 알림 전송: {len(slugs)}개 URL")
    for slug in slugs:
        url = f"{SITE_BASE_URL}/blog/{slug}"
        try:
            service.urlNotifications().publish(
                body={"url": url, "type": "URL_UPDATED"}
            ).execute()
            print(f"  ✅ {url}")
        except HttpError as e:
            print(f"  ❌ {url}  -> HTTP {e.resp.status}: {e.reason}")
        time.sleep(1)

    os.remove(NEW_POSTS_FILE)


if __name__ == "__main__":
    main()
