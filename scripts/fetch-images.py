import requests
import os
import time

# ── 설정 ──────────────────────────────────────────
PEXELS_API_KEY = "LpH7rG8vxTvK9ypMDBndRtyAOn56g32hUX5KM35vnulm0XotSFTR7tQW"
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "public", "images")

# 다운로드할 이미지 목록
# { 파일명: 검색 키워드 }
IMAGES = {
    "hero.jpg":       "luxury casino live dealer",
    "baccarat.jpg":   "baccarat card game casino table",
    "blackjack.jpg":  "blackjack casino table cards",
    "roulette.jpg":   "roulette wheel casino",
    "slots.jpg":      "casino slot machine colorful",
    "live-casino.jpg":"live casino dealer studio",
    "blog.jpg":       "casino strategy guide book",
    "og-main.jpg":    "luxury casino interior elegant",
}

# 이미지 크기 설정 (large2x = 원본급 고해상도)
IMAGE_SIZE = "large2x"
# ────────────────────────────────────────────────


def fetch_image_url(query: str) -> str | None:
    """Pexels API로 검색 후 첫 번째 이미지 URL 반환"""
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 1, "orientation": "landscape"}

    try:
        res = requests.get(url, headers=headers, params=params, timeout=10)
        res.raise_for_status()
        data = res.json()
        photos = data.get("photos", [])
        if not photos:
            print(f"  ⚠️  검색 결과 없음: '{query}'")
            return None
        return photos[0]["src"][IMAGE_SIZE]
    except Exception as e:
        print(f"  ❌ API 오류 ({query}): {e}")
        return None


def download_image(url: str, filepath: str) -> bool:
    """이미지 URL을 다운로드하여 파일로 저장"""
    try:
        res = requests.get(url, timeout=30, stream=True)
        res.raise_for_status()
        with open(filepath, "wb") as f:
            for chunk in res.iter_content(chunk_size=8192):
                f.write(chunk)
        size_kb = os.path.getsize(filepath) // 1024
        print(f"  ✅ 저장 완료: {os.path.basename(filepath)} ({size_kb}KB)")
        return True
    except Exception as e:
        print(f"  ❌ 다운로드 실패: {e}")
        return False


def main():
    print("=" * 50)
    print("  WOORIWIN 이미지 자동 다운로드 시작")
    print("=" * 50)

    # public/images 폴더 생성
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    print(f"\n📁 저장 경로: {os.path.abspath(OUTPUT_DIR)}\n")

    success = 0
    fail = 0

    for filename, query in IMAGES.items():
        filepath = os.path.join(OUTPUT_DIR, filename)

        # 이미 존재하면 스킵
        if os.path.exists(filepath):
            print(f"  ⏭️  스킵 (이미 존재): {filename}")
            success += 1
            continue

        print(f"\n🔍 검색 중: '{query}'")
        img_url = fetch_image_url(query)

        if img_url:
            print(f"  📥 다운로드 중...")
            if download_image(img_url, filepath):
                success += 1
            else:
                fail += 1
        else:
            fail += 1

        # API 요청 간격 (rate limit 방지)
        time.sleep(0.5)

    print("\n" + "=" * 50)
    print(f"  완료: 성공 {success}개 / 실패 {fail}개")
    print("=" * 50)
    print("\n✨ 이제 'npm run dev'로 이미지를 확인하세요!")


if __name__ == "__main__":
    main()