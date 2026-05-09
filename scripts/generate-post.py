import os
import json
import time
import requests
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))
from datetime import datetime, timedelta
from google import genai
import random  # ← 이 줄 추가

# ── API 키 설정 ──────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

# ── 경로 설정 ─────────────────────────────────────
BASE_DIR = os.path.join(os.path.dirname(__file__), "..")
POSTS_DIR = os.path.join(BASE_DIR, "data", "posts")
KEYWORDS_CACHE = os.path.join(BASE_DIR, "data", "keywords.json")
POSTS_PER_RUN = 3
MAX_DEPTH = 3  # 파생 깊이

# ── 시드 키워드 ───────────────────────────────────
SEED_KEYWORDS = [
    "에볼루션카지노",
    "에볼루션카지노 바카라",
    "에볼루션카지노 블랙잭",
    "에볼루션카지노 룰렛",
    "에볼루션카지노 슬롯",
    "에볼루션카지노 가입방법",  # ← 추가
    "에볼루션카지노 추천",      # ← 추가
    "라이트닝 바카라",          # ← 추가
    "인피니트 블랙잭",          # ← 추가
    "크레이지타임",             # ← 추가
]

# ────────────────────────────────────────────────

def collect_keywords_with_search(client, seed: str, used: list) -> list:
    used_str = ", ".join(used[-20:]) if used else "없음"
    prompt = f"""
'{seed}' 관련 한국인이 구글에 많이 검색하는 롱테일 키워드 15개.
조건: 한국어, 에볼루션카지노 포함, 제외: {used_str}
JSON 배열만: ["키워드1", "키워드2", ...]
"""
    try:
        response = client.models.generate_content(
            model="gemini-3.1-flash-lite",
            contents=prompt,
            config={"tools": [{"google_search": {}}]}
        )
        text = response.text.strip()
        if "```" in text:
            text = text.split("```")[1]
            if text.startswith("json"): text = text[4:]
        return [k for k in json.loads(text.strip()) if isinstance(k, str) and len(k) > 3]
    except Exception as e:
        print(f"  ⚠️ 키워드 수집 오류: {e}")
        return []


def load_keywords_cache() -> dict:
    """키워드 캐시 로드"""
    if os.path.exists(KEYWORDS_CACHE):
        with open(KEYWORDS_CACHE, "r", encoding="utf-8") as f:
            return json.load(f)
    return {"keywords": [], "used": []}

def save_keywords_cache(cache: dict):
    """키워드 캐시 저장"""
    os.makedirs(os.path.dirname(KEYWORDS_CACHE), exist_ok=True)
    with open(KEYWORDS_CACHE, "w", encoding="utf-8") as f:
        json.dump(cache, f, ensure_ascii=False, indent=2)

def get_existing_slugs() -> set:
    """이미 생성된 슬러그 목록"""
    if not os.path.exists(POSTS_DIR):
        return set()
    return {f.replace(".json", "") for f in os.listdir(POSTS_DIR) if f.endswith(".json")}

def keyword_to_slug(keyword: str) -> str:
    """키워드를 슬러그로 변환"""
    import re
    slug = keyword.lower()
    slug = re.sub(r'[^\w\s-]', '', slug)
    slug = re.sub(r'[\s_]+', '-', slug)
    slug = re.sub(r'-+', '-', slug)
    return slug.strip('-')

def get_category(keyword: str) -> str:
    """키워드에서 카테고리 추출"""
    if any(w in keyword for w in ['바카라', 'baccarat']):
        return '바카라'
    elif any(w in keyword for w in ['블랙잭', 'blackjack']):
        return '블랙잭'
    elif any(w in keyword for w in ['룰렛', 'roulette']):
        return '룰렛'
    elif any(w in keyword for w in ['슬롯', '크레이지타임', '게임쇼', 'slot']):
        return '슬롯/게임쇼'
    else:
        return '가이드'

def get_image_query(keyword: str) -> tuple[str, str]:
    """키워드에서 이미지 검색어와 alt 텍스트 생성"""
    category = get_category(keyword)
    queries = {
        '바카라': ('baccarat casino cards dealer', f'{keyword} 라이브 딜러 카지노'),
        '블랙잭': ('blackjack casino table cards', f'{keyword} 라이브 테이블'),
        '룰렛': ('roulette wheel casino', f'{keyword} 라이브 게임'),
        '슬롯/게임쇼': ('casino game show wheel', f'{keyword} 게임쇼'),
        '가이드': ('casino guide strategy', f'{keyword} 완벽 가이드'),
    }
    return queries.get(category, ('casino live dealer', f'{keyword}'))

# ── Gemini 설정 ───────────────────────────────────
def setup_gemini():
    client = genai.Client(api_key=GEMINI_API_KEY)
    return client

def generate_post_content(client, keyword: str, category: str) -> dict:
    """Gemini API로 포스트 콘텐츠 생성"""
    prompt = f"""
당신은 에볼루션카지노 전문 SEO 콘텐츠 라이터입니다.
아래 키워드로 한국어 블로그 포스트를 작성해주세요.

키워드: {keyword}
카테고리: {category}

요구사항:
1. 제목은 키워드를 포함한 매력적인 제목
2. 본문은 최소 1500자 이상
3. H2 헤더(## )를 4~6개 포함
4. 구체적인 수치와 통계 포함
5. 초보자도 이해할 수 있는 쉬운 설명
6. FAQ 3개 포함
7. SEO 최적화된 자연스러운 키워드 배치

다음 JSON 형식으로만 응답하세요 (다른 텍스트 없이):
{{
  "slug": "키워드를 영문으로 번역한 슬러그 (예: evolution-baccarat-strategy-guide)",
  "title": "포스트 제목 (키워드 포함)",
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

def fetch_pexels_image_url(query: str) -> str:
    """Pexels 이미지 URL 반환"""
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

def save_post(slug: str, content_data: dict, image_url: str, image_alt: str, category: str, date: str):
    """포스트 JSON 저장"""
    post = {
        "slug": slug,
        "title": content_data["title"],
        "description": content_data["description"],
        "category": category,
        "date": date,
        "readTime": f"{max(5, len(content_data['content']) // 300)}분",
        "keywords": content_data["keywords"],
        "image": image_url,
        "imageAlt": image_alt,
        "content": content_data["content"],
        "faq": content_data["faq"],
        "relatedPosts": [],
    }
    filepath = os.path.join(POSTS_DIR, f"{slug}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(post, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 포스트 저장: {slug}.json")

# ── 메인 ─────────────────────────────────────────
def main():
    print("=" * 55)
    print("  WOORIWIN 블로그 포스트 자동 생성 시작")
    print("=" * 55)

    os.makedirs(POSTS_DIR, exist_ok=True)

    # 1. 키워드 캐시 로드
    cache = load_keywords_cache()
    existing_slugs = get_existing_slugs()

    # 2. 키워드 부족하면 구글에서 새로 수집
    available = [k for k in cache["keywords"] if k not in cache["used"]]
    if len(available) < POSTS_PER_RUN:
        print("\n🔍 Gemini 구글 검색으로 새 키워드 수집 중...")
        client_temp = setup_gemini()
        seed = random.choice(SEED_KEYWORDS)
        print(f"  시드: '{seed}'")
        new_keywords = collect_keywords_with_search(client_temp, seed, cache["used"])
        existing_set = set(cache["keywords"])
        added = 0
        for kw in new_keywords:
            if kw not in existing_set:
                cache["keywords"].append(kw)
                existing_set.add(kw)
                added += 1
        save_keywords_cache(cache)
        available = [k for k in cache["keywords"] if k not in cache["used"]]
        print(f"  ✅ {added}개 추가 (총 {len(available)}개 가능)")
        time.sleep(1)

    # 3. 포스트 생성
    client = setup_gemini()
    today = datetime.now()
    success = 0

    for i, keyword in enumerate(available[:POSTS_PER_RUN]):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        category = get_category(keyword)
        image_query, image_alt = get_image_query(keyword)

        print(f"\n📝 [{i+1}/{POSTS_PER_RUN}] {keyword[:40]}...")
        print(f"  카테고리: {category}")

        print("  🤖 Gemini 본문 생성 중...")
        content_data = generate_post_content(client, keyword, category)
        if not content_data:
            continue

        slug = content_data.get("slug", keyword_to_slug(keyword))

        # 이미 생성된 슬러그면 스킵
        if slug in existing_slugs:
            cache["used"].append(keyword)
            save_keywords_cache(cache)
            continue

        print("  📸 Pexels 이미지 URL 가져오는 중...")
        image_url = fetch_pexels_image_url(image_query)

        save_post(slug, content_data, image_url, image_alt, category, date)

        # 사용된 키워드 표시
        cache["used"].append(keyword)
        save_keywords_cache(cache)

        success += 1
        time.sleep(2)

    print("\n" + "=" * 55)
    print(f"  완료: {success}개 포스트 생성")
    print(f"  남은 키워드: {len([k for k in cache['keywords'] if k not in cache['used']])}개")
    print("=" * 55)
    print("\n✨ 이제 'git add . && git commit -m \"feat: add posts\" && git push' 로 배포하세요!")

if __name__ == "__main__":
    main()
