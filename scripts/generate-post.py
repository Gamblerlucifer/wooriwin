import os
import json
import time
import requests
from datetime import datetime, timedelta
from google import genai

# ── API 키 설정 ──────────────────────────────────
GEMINI_API_KEY = "AIzaSyAUCWk-YmLtIm_YezhCgXEQUWOy2D74Xq0"
PEXELS_API_KEY = "LpH7rG8vxTvK9ypMDBndRtyAOn56g32hUX5KM35vnulm0XotSFTR7tQW"

# ── 경로 설정 ─────────────────────────────────────
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
POSTS_DIR = os.path.join(BASE_DIR, "data", "posts")
POSTS_PER_RUN = 3

# ── 키워드 목록 ───────────────────────────────────
KEYWORDS = [
    {"slug": "evolution-baccarat-banker-commission", "title": "에볼루션 바카라 뱅커 커미션 완벽 이해 — 5% 커미션의 진실", "category": "바카라", "image_query": "baccarat casino cards dealer", "image_alt": "에볼루션 바카라 뱅커 커미션 5% 완벽 이해 라이브 딜러"},
    {"slug": "evolution-speed-baccarat-guide", "title": "에볼루션 스피드 바카라 완벽 가이드 — 27초 완료 빠른 게임", "category": "바카라", "image_query": "fast card game casino table", "image_alt": "에볼루션 스피드 바카라 27초 빠른 게임 라이브 카지노"},
    {"slug": "evolution-lightning-baccarat-multiplier", "title": "에볼루션 라이트닝 바카라 멀티플라이어 전략 — 최대 8배 공략", "category": "바카라", "image_query": "lightning baccarat live casino", "image_alt": "에볼루션 라이트닝 바카라 멀티플라이어 최대 8배 전략"},
    {"slug": "evolution-squeeze-baccarat-guide", "title": "에볼루션 스퀴즈 바카라란? — VIP 느낌의 카드 공개 방식", "category": "바카라", "image_query": "baccarat squeeze card casino", "image_alt": "에볼루션 스퀴즈 바카라 VIP 카드 공개 방식"},
    {"slug": "evolution-no-commission-baccarat", "title": "에볼루션 노커미션 바카라 — 커미션 없는 바카라의 장단점", "category": "바카라", "image_query": "baccarat no commission casino", "image_alt": "에볼루션 노커미션 바카라 커미션 없는 바카라"},
    {"slug": "evolution-blackjack-infinite-guide", "title": "에볼루션 인피니트 블랙잭 완벽 가이드 — 무제한 착석의 비밀", "category": "블랙잭", "image_query": "blackjack infinite players casino", "image_alt": "에볼루션 인피니트 블랙잭 무제한 착석 라이브 테이블"},
    {"slug": "evolution-blackjack-double-down", "title": "블랙잭 더블다운 완벽 가이드 — 언제 두 배를 걸어야 하나", "category": "블랙잭", "image_query": "blackjack double down cards", "image_alt": "블랙잭 더블다운 전략 최적 타이밍 에볼루션카지노"},
    {"slug": "evolution-blackjack-split-guide", "title": "블랙잭 스플릿 완벽 가이드 — AA와 88은 항상 스플릿하라", "category": "블랙잭", "image_query": "blackjack split pair cards", "image_alt": "블랙잭 스플릿 AA 88 페어 에볼루션카지노 전략"},
    {"slug": "evolution-roulette-french-guide", "title": "에볼루션 프렌치 룰렛 완벽 가이드 — 앙 프리종 룰의 모든 것", "category": "룰렛", "image_query": "french roulette wheel casino", "image_alt": "에볼루션 프렌치 룰렛 앙 프리종 룰 RTP 98.65%"},
    {"slug": "evolution-roulette-american-vs-european", "title": "유럽식 vs 아메리칸 룰렛 — 어느 쪽이 더 유리한가", "category": "룰렛", "image_query": "roulette wheel green zero", "image_alt": "유럽식 아메리칸 룰렛 비교 하우스엣지 에볼루션카지노"},
    {"slug": "evolution-immersive-roulette-guide", "title": "에볼루션 이머시브 룰렛 완벽 가이드 — 슬로우모션의 몰입감", "category": "룰렛", "image_query": "roulette ball slow motion", "image_alt": "에볼루션 이머시브 룰렛 슬로우모션 HD 멀티캠"},
    {"slug": "evolution-crazy-time-wheel-guide", "title": "크레이지타임 휠 구성 완벽 분석 — 64칸의 확률 계산", "category": "슬롯/게임쇼", "image_query": "game show wheel spin colorful", "image_alt": "크레이지타임 휠 64칸 확률 분석 에볼루션 게임쇼"},
    {"slug": "evolution-monopoly-live-guide", "title": "에볼루션 모노폴리 라이브 완벽 가이드 — 3D 보드게임의 흥분", "category": "슬롯/게임쇼", "image_query": "monopoly board game colorful", "image_alt": "에볼루션 모노폴리 라이브 3D 보드게임 라이브쇼"},
    {"slug": "evolution-mega-ball-guide", "title": "에볼루션 메가볼 완벽 가이드 — 100만배 멀티플라이어의 비밀", "category": "슬롯/게임쇼", "image_query": "lottery balls bingo numbers", "image_alt": "에볼루션 메가볼 100만배 멀티플라이어 복권 게임"},
    {"slug": "evolution-casino-mobile-guide", "title": "에볼루션카지노 모바일 완벽 가이드 — 앱 없이 즐기는 방법", "category": "가이드", "image_query": "mobile phone casino app", "image_alt": "에볼루션카지노 모바일 앱 없이 브라우저 플레이"},
    {"slug": "evolution-casino-vip-salon-prive", "title": "에볼루션 살롱 프리베 완벽 가이드 — VIP 전용 테이블의 모든 것", "category": "가이드", "image_query": "luxury vip casino private room", "image_alt": "에볼루션 살롱 프리베 VIP 전용 프라이빗 테이블"},
    {"slug": "evolution-casino-rtp-guide", "title": "에볼루션카지노 RTP 완벽 정리 — 게임별 환수율 비교", "category": "가이드", "image_query": "casino statistics chart analysis", "image_alt": "에볼루션카지노 RTP 환수율 게임별 비교 바카라 블랙잭"},
    {"slug": "evolution-casino-deposit-guide", "title": "에볼루션카지노 입금방법 완벽 가이드 — 암호화폐·카드·전자지갑", "category": "가이드", "image_query": "cryptocurrency bitcoin casino deposit", "image_alt": "에볼루션카지노 입금방법 암호화폐 비트코인 카드"},
    {"slug": "evolution-baccarat-tie-bet-analysis", "title": "바카라 타이 베팅 분석 — 14% 하우스엣지의 함정", "category": "바카라", "image_query": "baccarat tie bet casino", "image_alt": "바카라 타이 베팅 하우스엣지 14% 분석 에볼루션"},
    {"slug": "evolution-blackjack-surrender-guide", "title": "블랙잭 서렌더 완벽 가이드 — 언제 포기하는 게 유리한가", "category": "블랙잭", "image_query": "blackjack surrender strategy cards", "image_alt": "블랙잭 서렌더 전략 포기 타이밍 에볼루션카지노"},
]

# ── Gemini 설정 ───────────────────────────────────
def setup_gemini():
    client = genai.Client(api_key=GEMINI_API_KEY)
    return client

# ── 본문 생성 ─────────────────────────────────────
def generate_post_content(client, keyword: dict) -> dict:
    prompt = f"""
당신은 에볼루션카지노 전문 SEO 콘텐츠 라이터입니다.
아래 주제로 한국어 블로그 포스트를 작성해주세요.

제목: {keyword['title']}
카테고리: {keyword['category']}
이미지 설명: {keyword['image_alt']}

요구사항:
1. 본문은 최소 1500자 이상
2. H2 헤더(## )를 4~6개 포함
3. 구체적인 수치와 통계 포함
4. 초보자도 이해할 수 있는 쉬운 설명
5. FAQ 3개 포함
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
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt
        )
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```")[1]
            if text.startswith("json"):
                text = text[4:]
        return json.loads(text.strip())
    except Exception as e:
        print(f"  ❌ Gemini 생성 오류: {e}")
        return None

# ── Pexels 이미지 URL ─────────────────────────────
def fetch_pexels_image_url(query: str) -> str:
    url = "https://api.pexels.com/v1/search"
    headers = {"Authorization": PEXELS_API_KEY}
    params = {"query": query, "per_page": 3, "orientation": "landscape"}
    try:
        res = requests.get(url, headers=headers, params=params, timeout=10)
        res.raise_for_status()
        photos = res.json().get("photos", [])
        if not photos:
            return "https://images.pexels.com/photos/1871508/pexels-photo-1871508.jpeg"
        print(f"  ✅ 이미지 URL 확보")
        return photos[0]["src"]["large2x"]
    except Exception as e:
        print(f"  ❌ 이미지 오류: {e}")
        return "https://images.pexels.com/photos/1871508/pexels-photo-1871508.jpeg"

# ── 관련 포스트 ───────────────────────────────────
def get_related_posts(current_slug: str, category: str) -> list:
    related = []
    for kw in KEYWORDS:
        if kw["slug"] != current_slug and kw["category"] == category:
            related.append({"slug": kw["slug"], "title": kw["title"]})
        if len(related) >= 3:
            break
    return related

# ── 포스트 저장 ───────────────────────────────────
def save_post(slug: str, keyword: dict, content_data: dict, image_url: str, date: str):
    post = {
        "slug": slug,
        "title": keyword["title"],
        "description": content_data["description"],
        "category": keyword["category"],
        "date": date,
        "readTime": f"{max(5, len(content_data['content']) // 300)}분",
        "keywords": content_data["keywords"],
        "image": image_url,
        "imageAlt": keyword["image_alt"],
        "content": content_data["content"],
        "faq": content_data["faq"],
        "relatedPosts": get_related_posts(slug, keyword["category"]),
    }
    filepath = os.path.join(POSTS_DIR, f"{slug}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(post, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 포스트 저장: {slug}.json")

# ── 기존 슬러그 확인 ──────────────────────────────
def get_existing_slugs() -> set:
    if not os.path.exists(POSTS_DIR):
        return set()
    return {f.replace(".json", "") for f in os.listdir(POSTS_DIR) if f.endswith(".json")}

# ── 메인 ─────────────────────────────────────────
def main():
    print("=" * 55)
    print("  WOORIWIN 블로그 포스트 자동 생성 시작")
    print("=" * 55)

    os.makedirs(POSTS_DIR, exist_ok=True)
    client = setup_gemini()
    existing = get_existing_slugs()
    pending = [kw for kw in KEYWORDS if kw["slug"] not in existing]

    if not pending:
        print("✅ 모든 포스트가 이미 생성되어 있습니다.")
        return

    today = datetime.now()
    success = 0

    for i, keyword in enumerate(pending[:POSTS_PER_RUN]):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        print(f"\n📝 [{i+1}/{POSTS_PER_RUN}] {keyword['title'][:40]}...")

        print("  🤖 Gemini 본문 생성 중...")
        content_data = generate_post_content(client, keyword)
        if not content_data:
            continue

        print("  📸 Pexels 이미지 URL 가져오는 중...")
        image_url = fetch_pexels_image_url(keyword["image_query"])

        save_post(keyword["slug"], keyword, content_data, image_url, date)
        success += 1
        time.sleep(2)

    print("\n" + "=" * 55)
    print(f"  완료: {success}개 포스트 생성")
    print("=" * 55)
    print("\n✨ 이제 'git add . && git commit -m \"feat: add posts\" && git push' 로 배포하세요!")

if __name__ == "__main__":
    main()
