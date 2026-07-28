"""
semi-auto-post.py
──────────────────
1-2단계(API 없는 플랫폼) 반자동 포스팅 도우미.
제미나이로 글을 생성 → 본문을 클립보드에 복사 → 대상 사이트를 기본 브라우저(Chrome)로 오픈.
사용자는 이미 로그인된 화면에서 제목 확인 + Ctrl+V + 발행 버튼만 누르면 끝.

사용법:
  python scripts/semi-auto-post.py                    # 이번 주 순번 플랫폼
  python scripts/semi-auto-post.py Medium             # 특정 플랫폼 지정
  python scripts/semi-auto-post.py --confirm <발행된 URL>   # 방금 발행한 글 URL 확인 → 색인 제출 + 로그 기록
"""

import os
import sys
import json
import argparse
import datetime
import subprocess
import webbrowser
import pyperclip
import markdown as md_lib
from dotenv import load_dotenv
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

sys.path.insert(0, os.path.dirname(__file__))
from backlink_content import generate_backlink_article
from semiauto_platforms import get_this_week_platform, find_platform, is_ready, mark_ready, PLATFORMS

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))

BASE_DIR             = os.path.join(os.path.dirname(__file__), "..")
SERVICE_ACCOUNT_FILE = os.path.join(BASE_DIR, "keys", "wooriwin-indexing.json")
INDEXING_SCOPE       = "https://www.googleapis.com/auth/indexing"
LOG_FILE              = os.path.join(os.path.dirname(__file__), ".semiauto_log.json")

CHROME_EXE         = os.environ.get("CHROME_EXE", "")
CHROME_PROFILE_DIR = os.environ.get("CHROME_PROFILE_DIR", "")


def open_in_chrome(url: str) -> str:
    """백링크 계정이 로그인된 지정 Chrome 프로필로 새 창을 연다. 실패 시 기본 브라우저로 폴백."""
    if CHROME_EXE and CHROME_PROFILE_DIR and os.path.exists(CHROME_EXE):
        subprocess.Popen([CHROME_EXE, f"--profile-directory={CHROME_PROFILE_DIR}", "--new-window", url])
        return f"Chrome ({CHROME_PROFILE_DIR})"
    webbrowser.open(url)
    return "기본 브라우저 (⚠️ 프로필 미지정 — .env.local에 CHROME_EXE/CHROME_PROFILE_DIR 설정 권장)"


def markdown_to_html(text: str) -> str:
    try:
        return md_lib.markdown(text)
    except Exception:
        return "".join(f"<p>{line}</p>" for line in text.split("\n\n") if line.strip())


def load_log() -> list:
    if os.path.exists(LOG_FILE):
        with open(LOG_FILE, encoding="utf-8") as f:
            return json.load(f)
    return []


def save_log(entries: list):
    with open(LOG_FILE, "w", encoding="utf-8") as f:
        json.dump(entries, f, ensure_ascii=False, indent=2)


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


def do_confirm(published_url: str):
    entries = load_log()
    pending = [e for e in entries if e["status"] == "pending"]
    if not pending:
        print("⚠️ 확인 대기 중인 항목이 없습니다.")
        return
    entry = pending[-1]
    entry["status"] = "confirmed"
    entry["published_url"] = published_url
    entry["confirmed_at"] = datetime.datetime.now().isoformat(timespec="seconds")
    save_log(entries)

    print(f"✅ 확인 완료: [{entry['platform']}] {entry['title']}")
    print(f"   → {published_url}")
    submit_to_indexing(published_url)


def do_generate(platform_arg: str | None):
    platform = find_platform(platform_arg) if platform_arg else get_this_week_platform()
    if not platform:
        print(f"❌ '{platform_arg}' 플랫폼을 찾을 수 없습니다.")
        return

    print("=" * 50)
    print(f"  반자동 백링크 — {platform['name']}")
    print("=" * 50)

    if not is_ready(platform["name"]):
        print(f"""
  🛑 아직 준비 안 된 플랫폼입니다: {platform['name']}

  아래 둘 다 확인 전에는 자동으로 열지 않습니다:
    1) {platform['name']} 계정 가입 완료
    2) Chrome (Profile 5 / gamblerlucifer)에 로그인된 상태로 열어봄 확인

  확인됐으면 다음 명령으로 준비완료 표시 후 다시 실행하세요:
    python scripts/semi-auto-post.py --mark-ready "{platform['name']}"
""")
        return

    print("\n글 생성 중...")
    article = generate_backlink_article(platform["name"])

    body = article["body_markdown"]
    if platform["body_format"] == "html":
        body = markdown_to_html(body)

    pyperclip.copy(body)

    entries = load_log()
    entries.append({
        "platform": platform["name"],
        "title": article["title"],
        "anchor_text": article["anchor_text"],
        "source_slug": article["source_slug"],
        "created_at": datetime.datetime.now().isoformat(timespec="seconds"),
        "status": "pending",
    })
    save_log(entries)

    opened_via = open_in_chrome(platform["new_post_url"])

    print(f"""
  📌 플랫폼   : {platform['name']}
  📝 제목     : {article['title']}
  🔗 앵커텍스트: {article['anchor_text']}
  🌐 새 글 화면: {platform['new_post_url']}
  🧑‍💻 오픈 위치 : {opened_via}

  ✅ 본문이 클립보드에 복사되었습니다 — 제목 입력란에 위 제목 입력 후,
     본문란에 Ctrl+V로 붙여넣고 발행 버튼을 누르세요.

  발행 완료되면 다음 명령으로 알려주세요:
    python scripts/semi-auto-post.py --confirm <발행된 글 URL>
""")


def do_list_ready():
    print("=" * 50)
    print("  플랫폼 준비 상태")
    print("=" * 50)
    for p in PLATFORMS:
        mark = "✅ 준비됨" if is_ready(p["name"]) else "⬜ 미확인"
        print(f"  {mark}  {p['name']}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("platform", nargs="?", default=None, help="플랫폼 이름 (생략 시 이번 주 순번)")
    parser.add_argument("--confirm", metavar="URL", help="발행 완료한 글의 URL")
    parser.add_argument("--mark-ready", metavar="PLATFORM", help="계정 가입+로그인 확인된 플랫폼을 준비완료로 표시")
    parser.add_argument("--unmark-ready", metavar="PLATFORM", help="준비완료 표시 해제")
    parser.add_argument("--list-ready", action="store_true", help="전체 플랫폼 준비 상태 표시")
    args = parser.parse_args()

    if args.list_ready:
        do_list_ready()
    elif args.mark_ready:
        p = find_platform(args.mark_ready)
        if not p:
            print(f"❌ '{args.mark_ready}' 플랫폼을 찾을 수 없습니다.")
            return
        mark_ready(p["name"], True)
        print(f"✅ {p['name']} 준비완료로 표시했습니다.")
    elif args.unmark_ready:
        p = find_platform(args.unmark_ready)
        if not p:
            print(f"❌ '{args.unmark_ready}' 플랫폼을 찾을 수 없습니다.")
            return
        mark_ready(p["name"], False)
        print(f"⬜ {p['name']} 준비완료 표시를 해제했습니다.")
    elif args.confirm:
        do_confirm(args.confirm)
    else:
        do_generate(args.platform)


if __name__ == "__main__":
    main()
