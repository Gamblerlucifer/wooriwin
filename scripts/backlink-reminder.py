"""
backlink-reminder.py — 1-2단계 반자동 플랫폼 주간 알림
ISO 주차 기준으로 플랫폼을 순환하며 매주 수요일 텔레그램으로 알림.
GitHub Actions cron: '0 4 * * 3'  # 수요일 13:00 KST
"""

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))
from telegram_notify import send_message
from semiauto_platforms import get_this_week_platform, get_next_platform, TOTAL, week_index


def main():
    p = get_this_week_platform()
    next_p = get_next_platform()
    idx = week_index()

    da_str = f" (DA {p['da']})" if p["da"] else ""
    next_da = f" DA {next_p['da']}" if next_p["da"] else ""

    msg = (
        f"🔔 <b>이번 주 반자동 백링크</b>  [{idx + 1}/{TOTAL}]\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"📌 플랫폼: <b>{p['name']}</b>{da_str}\n"
        f"🔧 작업: {p['desc']}\n"
        f"🔗 <a href='{p['new_post_url']}'>{p['new_post_url']}</a>\n"
        f"━━━━━━━━━━━━━━━━\n"
        f"PC에서 Claude에게 아래 메시지 그대로 전송:\n"
        f"<code>{p['name']} 백링크 해줘</code>\n\n"
        f"▶ 다음 주: {next_p['name']}{next_da}"
    )

    ok = send_message(msg)
    print("✅ 알림 전송 성공" if ok else "❌ 알림 전송 실패")
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
