"""
gsc-index-pending.py
───────────────────────
data/gsc-pending-urls.txt 의 URL들에 Google Indexing API
(urlNotifications.publish, type=URL_UPDATED)로 색인 요청을 보내고,
성공한 URL을 data/.gsc-checklist-done.json 의 "done" 목록에 추가한다.

사용법:
  python scripts/gsc-index-pending.py
"""

import os
import json
import time
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "keys", "wooriwin-indexing.json")
URLS_FILE = os.path.join(BASE_DIR, "data", "gsc-pending-urls.txt")
CHECKLIST_FILE = os.path.join(BASE_DIR, "data", ".gsc-checklist-done.json")
RESULT_LOG = os.path.join(BASE_DIR, "data", "gsc-pending-index-log.json")

SCOPES = ["https://www.googleapis.com/auth/indexing"]


def load_urls():
    with open(URLS_FILE, encoding="utf-8") as f:
        return [line.strip() for line in f if line.strip()]


def load_checklist():
    with open(CHECKLIST_FILE, encoding="utf-8") as f:
        return json.load(f)


def save_checklist(data):
    with open(CHECKLIST_FILE, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def main():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    )
    service = build("indexing", "v3", credentials=credentials)

    urls = load_urls()
    checklist = load_checklist()
    done = set(checklist["done"])

    print(f"총 {len(urls)}개 URL 색인 요청 시작\n")

    log = {}
    success, fail = 0, 0
    for i, url in enumerate(urls, 1):
        try:
            response = service.urlNotifications().publish(
                body={"url": url, "type": "URL_UPDATED"}
            ).execute()
            notify_time = response.get("urlNotificationMetadata", {}).get(
                "latestUpdate", {}
            ).get("notifyTime", "")
            print(f"[{i}/{len(urls)}] OK   {url}")
            log[url] = {"status": "ok", "type": "URL_UPDATED", "notifyTime": notify_time}
            done.add(url)
            success += 1
        except HttpError as e:
            status = e.resp.status
            print(f"[{i}/{len(urls)}] FAIL {url}  -> HTTP {status}: {e.reason}")
            log[url] = {"status": f"error_{status}", "reason": str(e.reason)}
            fail += 1
            if status == 429:
                print("   할당량(429) 초과 - 중단합니다.")
                break
        time.sleep(1)

    checklist["done"] = sorted(done)
    save_checklist(checklist)

    with open(RESULT_LOG, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    print(f"\n=== 완료: 성공 {success} / 실패 {fail} ===")
    print(f"체크리스트 갱신: {CHECKLIST_FILE}")
    print(f"결과 로그: {RESULT_LOG}")


if __name__ == "__main__":
    main()
