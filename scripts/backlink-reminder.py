"""
backlink-reminder.py — 1-2단계 반자동 플랫폼 주간 알림
ISO 주차 기준으로 이번 주 플랫폼을 정하고, 제미나이로 글을 미리 생성해서
제목/본문을 텔레그램 메시지에 그대로 넣어 보낸다. 사용자는 그 사이트를 열고
제목/본문을 복붙 + 발행만 하면 됨 (Claude를 다시 부를 필요 없음).
GitHub Actions cron: '0 4 * * 3'  # 수요일 13:00 KST
"""

import os
import sys
import html
from dotenv import load_dotenv

sys.path.insert(0, os.path.dirname(__file__))
from telegram_notify import send_message
from semiauto_platforms import get_this_week_platform, get_next_platform, TOTAL, week_index
from backlink_content import generate_backlink_article, markdown_to_html

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))


def build_message(p: dict, next_p: dict, idx: int, article: dict | None) -> str:
    da_str = f" (DA {p['da']})" if p["da"] else ""
    next_da = f" DA {next_p['da']}" if next_p["da"] else ""

    header = (
        f"🔔 <b>이번 주 반자동 백링크</b>  [{idx + 1}/{TOTAL}]\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"📌 플랫폼: <b>{p['name']}</b>{da_str}\n"
        f"🔗 새 글 화면: <a href='{p['new_post_url']}'>{p['new_post_url']}</a>\n"
    )

    if article is None:
        body_block = (
            f"━━━━━━━━━━━━━━━━\n"
            f"⚠️ 글 자동 생성 실패 — 아래 메시지로 직접 요청하세요:\n"
            f"<code>{p['name']} 백링크 해줘</code>\n"
        )
    else:
        body = article["body_markdown"]
        if p["body_format"] == "html":
            body = markdown_to_html(body)

        body_block = (
            f"━━━━━━━━━━━━━━━━\n"
            f"✏️ <b>제목</b> (탭해서 복사)\n"
            f"<code>{html.escape(article['title'])}</code>\n\n"
            f"📝 <b>본문</b> (탭해서 복사)\n"
            f"<pre>{html.escape(body)}</pre>\n\n"
            f"🔗 앵커: {html.escape(article['anchor_text'])}\n"
        )

    footer = (
        f"━━━━━━━━━━━━━━━━\n"
        f"위 사이트 열고(Chrome, 로그인 상태 확인) 제목·본문 붙여넣기 → 발행.\n"
        f"발행 URL은 Claude에게 알려주면 색인 제출까지 처리합니다.\n\n"
        f"▶ 다음 주: {next_p['name']}{next_da}"
    )

    return header + body_block + footer


def main():
    p = get_this_week_platform()
    next_p = get_next_platform()
    idx = week_index()

    try:
        article = generate_backlink_article(p["name"])
    except Exception as e:
        print(f"⚠️ 글 생성 실패: {e}")
        article = None

    msg = build_message(p, next_p, idx, article)

    ok = send_message(msg)
    print("✅ 알림 전송 성공" if ok else "❌ 알림 전송 실패")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
