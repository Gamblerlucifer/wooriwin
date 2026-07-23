"""
backlink-rotation.py
──────────────────
백링크 플랫폼에 순서대로 1개씩 포스팅, 플랫폼 사이 2분 대기.
플랫폼당 실행 1회에 1개 글만 발행되므로 개별 플랫폼 입장에서는 스팸 패턴이 아님.
GitHub Actions에서 주 1회 트리거되는 것을 전제로 함(빈도는 .github/workflows에서 조절).

사용법:
  python scripts/backlink-rotation.py
"""

import os
import sys
import time
import subprocess

SCRIPTS_DIR = os.path.dirname(__file__)
GAP_SECONDS = 120

PLATFORMS = [
    "telegraph-post.py",
    "gist-post.py",
    "blogger-post.py",
    "tumblr-post.py",
    # Write.as / WordPress.com — 2026-07 기준 무료 플랜 폐지, 스킵
]


def main():
    print("=" * 50)
    print(f"  백링크 로테이션 — {len(PLATFORMS)}개 플랫폼")
    print("=" * 50)

    results = []
    for i, script in enumerate(PLATFORMS):
        print(f"\n[{i+1}/{len(PLATFORMS)}] {script}")
        result = subprocess.run([sys.executable, os.path.join(SCRIPTS_DIR, script)])
        ok = result.returncode == 0
        results.append((script, ok))
        if not ok:
            print(f"  ⚠️ {script} 실패 — 나머지는 계속 진행")

        if i < len(PLATFORMS) - 1:
            print(f"  ⏳ {GAP_SECONDS}초 대기...")
            time.sleep(GAP_SECONDS)

    print("\n" + "=" * 50)
    print("  결과 요약")
    print("=" * 50)
    for script, ok in results:
        print(f"  {'✅' if ok else '❌'} {script}")


if __name__ == "__main__":
    main()
