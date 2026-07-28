"""
telegram-notify.py — Telegram Bot API 공용 헬퍼
다른 스크립트에서 import 하거나 단독 실행 가능.
"""

import os
import requests


def send_message(text: str, parse_mode: str = "HTML") -> bool:
    token = os.environ.get("TELEGRAM_BOT_TOKEN", "")
    chat_id = os.environ.get("TELEGRAM_CHAT_ID", "")
    if not token or not chat_id:
        print("⚠️  TELEGRAM_BOT_TOKEN / TELEGRAM_CHAT_ID 미설정, 알림 스킵")
        return False
    try:
        resp = requests.post(
            f"https://api.telegram.org/bot{token}/sendMessage",
            json={"chat_id": chat_id, "text": text, "parse_mode": parse_mode},
            timeout=10,
        )
        resp.raise_for_status()
        return True
    except Exception as e:
        print(f"텔레그램 전송 실패: {e}")
        return False


if __name__ == "__main__":
    import sys
    msg = " ".join(sys.argv[1:]) or "wooriwin 텔레그램 봇 연결 테스트 ✅"
    ok = send_message(msg)
    sys.exit(0 if ok else 1)
