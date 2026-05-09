import os
import json
import time
import requests
from datetime import datetime, timedelta
import google.generativeai as genai

# ── 설정 ──────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "AIzaSyDV8cdh4Rk-deK_SiHgx4RdwipXxVh9Hss")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "LpH7rG8vxTvK9ypMDBndRtyAOn56g32hUX5KM35vnulm0XotSFTR7tQW")

# 프로젝트 루트 기준 경로
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
POSTS_DIR = os.path.join(BASE_DIR, "data", "posts")
IMAGES_DIR = os.path.join(BASE_DIR, "public", "images", "posts")

# 생성할 포스트 수
POSTS_PER_RUN = 3

# 타겟 키워드 목록 (롱테일)
KEYWORDS = [
    {"slug": "evolution-baccarat-banker-commission", "title": "에볼루션 바카라 뱅커 커미션 완벽 이해 — 5% 커미션의 진실", "category": "바카라", "image_query": "baccarat casino cards dealer"},
    {"slug": "evolution-speed-baccarat-guide", "title": "에볼루션 스피드 바카라 완벽 가이드 — 27초 완료 빠른 게임", "category": "바카라", "image_query": "fast card game casino table"},
    {"slug": "evolution-lightning-baccarat-multiplier", "title": "에볼루션 라이트닝 바카라 멀티플라이어 전략 — 최대 8배 공략", "category": "바카라", "image_query": "lightning baccarat live casino"},
    {"slug": "evolution-squeeze-baccarat-guide", "title": "에볼루션 스퀴즈 바카라란? — VIP 느낌의 카드 공개 방식", "category": "바카라", "image_query": "baccarat squeeze card casino"},
    {"slug": "evolution-no-commission-baccarat", "title": "에볼루션 노커미션 바카라 — 커미션 없는 바카라의 장단점", "category": "바카라", "image_query": "baccarat no commission casino"},
    {"slug": "evolution-blackjack-infinite-guide", "title": "에볼루션 인피니트 블랙잭 완벽 가이드 — 무제한 착석의 비밀", "category": "블랙잭", "image_query": "blackjack infinite players casino"},
    {"slug": "evolution-blackjack-double-down", "title": "블랙잭 더블다운 완벽 가이드 — 언제 두 배를 걸어야 하나", "category": "블랙잭", "image_query": "blackjack double down cards"},
    {"slug": "evolution-blackjack-split-guide", "title": "블랙잭 스플릿 완벽 가이드 — AA와 88은 항상 스플릿하라", "category": "블랙잭", "image_query": "blackjack split pair cards"},
    {"slug": "evolution-roulette-french-guide", "title": "에볼루션 프렌치 룰렛 완벽 가이드 — 앙 프리종 룰의 모든 것", "category": "룰렛", "image_query": "french roulette wheel casino"},
    {"slug": "evolution-roulette-american-vs-european", "title": "유럽식 vs 아메리칸 룰렛 — 어느 쪽이 더 유리한가", "category": "룰렛", "image_query": "roulette wheel green zero"},
    {"slug": "evolution-immersive-roulette-guide", "title": "에볼루션 이머시브 룰렛 완벽 가이드 — 슬로우모션의 몰입감", "category": "룰렛", "image_query": "roulette ball slow motion"},
    {"slug": "evolution-crazy-time-wheel-guide", "title": "크레이지타임 휠 구성 완벽 분석 — 64칸의 확률 계산", "category": "슬롯/게임쇼", "image_query": "game show wheel spin colorful"},
    {"slug": "evolution-monopoly-live-guide", "title": "에볼루션 모노폴리 라이브 완벽 가이드 — 3D 보드게임의 흥분", "category": "슬롯/게임쇼", "image_query": "monopoly board game colorful"},
    {"slug": "evolution-mega-ball-guide", "title": "에볼루션 메가볼 완벽 가이드 — 100만배 멀티플라이어의 비밀", "category": "슬롯/게임쇼", "image_query": "lottery balls bingo numbers"},
    {"slug": "evolution-casino-mobile-guide", "title": "에볼루션카지노 모바일 완벽 가이드 — 앱 없이 즐기는 방법", "category": "가이드", "image_query": "mobile phone casino app"},
    {"slug": "evolution-casino-vip-salon-prive", "title": "에볼루션 살롱 프리베 완벽 가이드 — VIP 전용 테이블의 모든 것", "category": "가이드", "image_query": "luxury vip casino private room"},
    {"slug": "evolution-casino-rtp-guide", "title": "에볼루션카지노 RTP 완벽 정리 — 게임별 환수율 비교", "category": "가이드", "image_query": "casino statistics chart analysis"},
    {"slug": "evolution-casino-deposit-guide", "title": "에볼루션카지노 입금방법 완벽 가이드 — 암호화폐·카드·전자지갑", "category": "가이드", "image_query": "cryptocurrency bitcoin casino deposit"},
    {"slug": "evolution-baccarat-tie-bet-analysis", "title": "바카라 타이 베팅 분석 — 14% 하우스엣지의 함정", "category": "바카라", "image_query": "baccarat tie bet casino"},
    {"slug": "evolution-blackjack-surrender-guide", "title": "블랙잭 서렌더 완벽 가이드 — 언제 포기하는 게 유리한가", "category": "블랙잭", "image_query": "blackjack surrender strategy cards"},
]

# ────────────────────────────────────────────────

def setup_gemini():
    genai.configure(api_key=GEMINI_API_KEY)
    return genai.GenerativeModel("gemini-3.1-flash-lite")


def generate_post_content(model, keyword: dict) -> dict:
    """Gemini API로 포스트 콘텐츠 생성"""
    prompt = f"""
당신은 에볼루션카지노 전문 SEO 콘텐츠 라이터입니다.
아래 주제로 한국어 블로그 포스트를 작성해주세요.

제목: {keyword['title']}
카테고리: {keyword['category']}

요구사항:
1. 본문은 최소 1500자 이상
2. H2 헤더(## )를 4~6개 포함
3. 구체적인 수치와 통계 포함
4. 초보자도 이해할 수 있는 쉬운 설명
5. FAQ 3개 포함 (JSON 형식으로)
6. SEO 최적화된 자연스러운 키워드 배치

다음 JSON 형식으로만 응답하세요 (다른 텍스트 없이):
{{
  "description": "포스트 설명 (150자 이내)",
  "keywords": ["키워드1", "키워드2", "키워드3", "키워드4"],
  "content": "본문 내용 (마크다운 형식, 1500자 이상)",
  "faq": [
    {{"q": "질문1", "a": "답변1"}},
    {{"q": "질문2", "a": "답변2"}},
    {{"q": "질문3", "a": "답변3"}}
  ]
}}
"""
    try:
        response = model.generate_content(prompt)
        text = response.text.strip()
        # JSON 파싱
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except Exception as e:
        print(f"  ❌ Gemini 생성 오류: {e}")
        return None

def fetch_pexels_image(query: str, slug: str) -> str | None:
    """Pexels API로 이미지 다운로드"""
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 1, "orientation": "landscape"}

    try:
        res = requests.get(url, headers=headers, params=params, timeout=10)
        res.raise_for_status()
        photos = res.json().get("photos", [])
        if not photos:
            return None
        
        img_url = photos[0]["src"]["large2x"]
        img_path = os.path.join(IMAGES_DIR, f"{slug}.jpg")
        
        img_res = requests.get(img_url, timeout=30, stream=True)
        img_res.raise_for_status()
        with open(img_path, "wb") as f:
            for chunk in img_res.iter_content(chunk_size=8192):
                f.write(chunk)
        
        print(f"  ✅ 이미지 저장: {slug}.jpg")
        return f"/images/posts/{slug}.jpg"
    except Exception as e:
        print(f"  ❌ 이미지 오류: {e}")
        return "/images/blog.jpg"  # 기본 이미지 폴백

def get_related_posts(current_slug: str, category: str) -> list:
    """관련 포스트 추천"""
    related = []
    for kw in KEYWORDS:
        if kw["slug"] != current_slug and kw["category"] == category:
            related.append({"slug": kw["slug"], "title": kw["title"]})
        if len(related) >= 3:
            break
    return related

def save_post(slug: str, keyword: dict, content_data: dict, image_path: str, date: str):
    """포스트 JSON 파일 저장"""
    post = {
        "slug": slug,
        "title": keyword["title"],
        "description": content_data["description"],
        "category": keyword["category"],
        "date": date,
        "readTime": f"{max(5, len(content_data['content']) // 300)}분",
        "keywords": content_data["keywords"],
        "image": image_path,
        "content": content_data["content"],
        "faq": content_data["faq"],
        "relatedPosts": get_related_posts(slug, keyword["category"]),
    }
    
    filepath = os.path.join(POSTS_DIR, f"{slug}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(post, f, ensure_ascii=False, indent=2)
    
    print(f"  ✅ 포스트 저장: {slug}.json")

def get_existing_slugs() -> set:
    """이미 생성된 슬러그 목록"""
    if not os.path.exists(POSTS_DIR):
        return set()
    return {f.replace(".json", "") for f in os.listdir(POSTS_DIR) if f.endswith(".json")}

def main():
    print("=" * 55)
    print("  WOORIWIN 블로그 포스트 자동 생성 시작")
    print("=" * 55)

    # 폴더 생성
    os.makedirs(POSTS_DIR, exist_ok=True)
    os.makedirs(IMAGES_DIR, exist_ok=True)

    # Gemini 설정
    model = setup_gemini()

    # 기존 슬러그 확인
    existing = get_existing_slugs()
    pending = [kw for kw in KEYWORDS if kw["slug"] not in existing]

    if not pending:
        print("✅ 모든 포스트가 이미 생성되어 있습니다.")
        return

    # 오늘 날짜부터 역순으로 날짜 부여
    today = datetime.now()
    success = 0

    for i, keyword in enumerate(pending[:POSTS_PER_RUN]):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        print(f"\n📝 [{i+1}/{POSTS_PER_RUN}] {keyword['title'][:40]}...")

        # 1. Gemini로 본문 생성
        print("  🤖 Gemini 본문 생성 중...")
        content_data = generate_post_content(model, keyword)
        if not content_data:
            continue

        # 2. Pexels 이미지 다운로드
        print("  📸 Pexels 이미지 다운로드 중...")
        image_path = fetch_pexels_image(keyword["image_query"], keyword["slug"])

        # 3. JSON 저장
        save_post(keyword["slug"], keyword, content_data, image_path, date)
        success += 1

        # API 요청 간격
        time.sleep(2)

    print("\n" + "=" * 55)
    print(f"  완료: {success}개 포스트 생성")
    print("=" * 55)
    print("\n✨ 이제 'git add . && git commit -m \"feat: add posts\" && git push' 로 배포하세요!")

if __name__ == "__main__":
    main()
