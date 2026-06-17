"""
gsc-deindex-site.py
───────────────────
사이트의 sitemap에서 URL을 읽어 Google Indexing API로 URL_DELETED 전송.
색인 제거 요청 (콘텐츠 삭제 후 실행).

사용법:
  python scripts/gsc-deindex-site.py --site howtobet7
  python scripts/gsc-deindex-site.py --site moneyrush
  python scripts/gsc-deindex-site.py --site mytoto365
"""

import os
import sys
import time
import json
import argparse
import urllib.request
import xml.etree.ElementTree as ET

from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
SCOPES = ["https://www.googleapis.com/auth/indexing"]

SITE_CONFIG = {
    "howtobet7": {
        "base_url": "https://howtobet7.com",
        "sitemap": "https://howtobet7.com/sitemap_index.xml",
        "key_pattern": "howtobet7-instant-indexing",
    },
    "moneyrush": {
        "base_url": "https://moneyrush.net",
        "sitemap": "https://moneyrush.net/sitemap_index.xml",
        "key_pattern": "moneyrush-instant-indexing",
    },
    "mytoto365": {
        "base_url": "https://mytoto365.com",
        "sitemap": "https://mytoto365.com/sitemap_index.xml",
        "key_pattern": "mytoto365-instant-indexing",
    },
    "wooriwin-net": {
        "base_url": "https://wooriwin.net",
        "sitemap": "https://wooriwin.net/sitemap_index.xml",
        "key_pattern": "wooriwin-indexing",
    },
}


def find_key_file(pattern):
    keys_dir = os.path.join(BASE_DIR, "keys")
    for f in os.listdir(keys_dir):
        if pattern in f and f.endswith(".json"):
            return os.path.join(keys_dir, f)
    return None


HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)"}


def fetch_urls_from_sitemap(sitemap_url):
    urls = []
    try:
        req = urllib.request.Request(sitemap_url, headers=HEADERS)
        with urllib.request.urlopen(req, timeout=10) as resp:
            tree = ET.parse(resp)
        root = tree.getroot()
        ns = root.tag.split("}")[0].lstrip("{") if "}" in root.tag else ""
        prefix = f"{{{ns}}}" if ns else ""

        # sitemap index
        for sitemap in root.findall(f"{prefix}sitemap"):
            loc = sitemap.find(f"{prefix}loc")
            if loc is not None:
                urls.extend(fetch_urls_from_sitemap(loc.text.strip()))

        # urlset
        for url in root.findall(f"{prefix}url"):
            loc = url.find(f"{prefix}loc")
            if loc is not None:
                urls.append(loc.text.strip())

    except Exception as e:
        print(f"  sitemap 접근 실패: {sitemap_url} → {e}")

    return urls


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site", required=True, choices=list(SITE_CONFIG.keys()))
    args = parser.parse_args()

    cfg = SITE_CONFIG[args.site]
    key_file = find_key_file(cfg["key_pattern"])
    if not key_file:
        print(f"키 파일 없음: {cfg['key_pattern']}*.json")
        sys.exit(1)

    print(f"키 파일: {os.path.basename(key_file)}")
    print(f"사이트: {cfg['base_url']}")

    credentials = service_account.Credentials.from_service_account_file(
        key_file, scopes=SCOPES
    )
    service = build("indexing", "v3", credentials=credentials)

    urls_file = os.path.join(BASE_DIR, "data", f"{args.site}-urls.txt")
    if os.path.exists(urls_file):
        print(f"URL 파일 사용: {urls_file}")
        with open(urls_file, encoding="utf-8") as f:
            urls = [l.strip() for l in f if l.strip()]
    else:
        print(f"sitemap 수집 중: {cfg['sitemap']}")
        urls = fetch_urls_from_sitemap(cfg["sitemap"])
        urls = list(set(urls))

    if not urls:
        print("URL 없음 — sitemap 접근 불가이거나 이미 비어있음")
        sys.exit(0)

    print(f"총 {len(urls)}개 URL → URL_DELETED 전송\n")

    log = {}
    success, fail = 0, 0
    for i, url in enumerate(urls, 1):
        try:
            service.urlNotifications().publish(
                body={"url": url, "type": "URL_DELETED"}
            ).execute()
            print(f"[{i}/{len(urls)}] OK   {url}")
            log[url] = "deleted"
            success += 1
        except HttpError as e:
            print(f"[{i}/{len(urls)}] FAIL {url} → HTTP {e.resp.status}: {e.reason}")
            log[url] = f"error_{e.resp.status}"
            fail += 1
            if e.resp.status == 429:
                print("할당량 초과 — 중단")
                break
        time.sleep(0.5)

    log_file = os.path.join(BASE_DIR, "data", f"deindex-{args.site}.json")
    with open(log_file, "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

    print(f"\n=== 완료: 성공 {success} / 실패 {fail} ===")
    print(f"로그: {log_file}")


if __name__ == "__main__":
    main()
