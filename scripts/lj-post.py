"""
lj-post.py
──────────────────
wooriwin.com 포스트를 소재로 제미나이가 완전히 새로 쓴 글을, 앵커 텍스트 백링크와 함께
LiveJournal에 발행 (XML-RPC challenge-response 인증).

사전 준비 (.env.local):
  LJ_USERNAME / LJ_PASSWORD  — livejournal.com 계정 (OpenID 계정은 불가, 표준 계정 필요)

사용법:
  python scripts/lj-post.py            # 1개 발행
  python scripts/lj-post.py --count 3  # 3개 발행
"""

import os
import sys
import time
import hashlib
import argparse
import xmlrpc.client
import markdown as md_lib
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.path.insert(0, os.path.dirname(__file__))
from backlink_content import generate_backlink_article

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))

LJ_USERNAME = os.environ.get("LJ_USERNAME", "")
LJ_PASSWORD = os.environ.get("LJ_PASSWORD", "")
LJ_ENDPOINT = "https://www.livejournal.com/interface/xmlrpc"

BASE_DIR             = os.path.join(os.path.dirname(__file__), "..")
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "keys", "wooriwin-indexing.json")
INDEXING_SCOPE       = "https://www.googleapis.com/auth/indexing"


def markdown_to_html(text: str) -> str:
    try:
        return md_lib.markdown(text)
    except Exception:
        return "".join(f"<p>{line}</p>" for line in text.split("\n\n") if line.strip())


def get_challenge(server: xmlrpc.client.ServerProxy) -> str:
    res = server.LJ.XMLRPC.getchallenge()
    return res["challenge"]


def auth_response(challenge: str, password: str) -> str:
    pw_hash = hashlib.md5(password.encode("utf-8")).hexdigest()
    return hashlib.md5((challenge + pw_hash).encode("utf-8")).hexdigest()


def post_to_lj(title: str, body_markdown: str) -> str:
    server = xmlrpc.client.ServerProxy(LJ_ENDPOINT)
    challenge = get_challenge(server)
    response = auth_response(challenge, LJ_PASSWORD)

    # 로컬 시스템 시계가 아니라 LJ 챌린지에 실려오는 서버 유닉스타임을 신뢰한다
    # (샌드박스/로컬 환경의 시계가 실제 시각과 어긋나면 글 날짜가 틀어지는 문제 방지)
    server_unixtime = int(challenge.split(":")[1])
    now = time.gmtime(server_unixtime)
    params = {
        "username": LJ_USERNAME,
        "auth_method": "challenge",
        "auth_challenge": challenge,
        "auth_response": response,
        "ver": 1,
        "subject": title[:255],
        "event": markdown_to_html(body_markdown),
        "lineendings": "unix",
        "security": "public",
        "year": now.tm_year,
        "mon": now.tm_mon,
        "day": now.tm_mday,
        "hour": now.tm_hour,
        "min": now.tm_min,
        "props": {"opt_preformatted": 1},
    }

    data = server.LJ.XMLRPC.postevent(params)

    if data.get("url"):
        return data["url"]
    itemid = int(data["itemid"])
    anum = int(data["anum"])
    ditemid = itemid * 256 + anum
    return f"https://{LJ_USERNAME}.livejournal.com/{ditemid}.html"


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

    if not LJ_USERNAME or not LJ_PASSWORD:
        print("❌ .env.local에 LJ_USERNAME / LJ_PASSWORD 가 없습니다")
        return

    print("=" * 50)
    print("  LiveJournal 자동 포스팅 (wooriwin.com 백링크)")
    print("=" * 50)

    for i in range(args.count):
        print(f"\n[{i+1}/{args.count}] 글 생성 중...")
        article = generate_backlink_article("LiveJournal")
        print(f"  📝 {article['title']} (앵커: \"{article['anchor_text']}\")")

        try:
            post_url = post_to_lj(article["title"], article["body_markdown"])
            print(f"  ✅ 발행 완료: {post_url}")
            submit_to_indexing(post_url)
        except xmlrpc.client.Fault as e:
            print(f"  ❌ LiveJournal API 오류: {e.faultCode} {e.faultString}")
            sys.exit(1)

        time.sleep(1)


if __name__ == "__main__":
    main()
