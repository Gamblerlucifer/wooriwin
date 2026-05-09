import os
import json
import time
import requests
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))
from datetime import datetime, timedelta
from google import genai
import random

# ── API 키 ────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

# ── 경로 ──────────────────────────────────────────
BASE_DIR   = os.path.join(os.path.dirname(__file__), "..")
POSTS_DIR  = os.path.join(BASE_DIR, "data", "posts")
USED_CACHE = os.path.join(BASE_DIR, "data", "used_topics.json")
POSTS_PER_RUN = 3

# ── E-E-A-T 고정 문구 (모든 글 하단 hard-code) ────
RESPONSIBLE_GAMBLING_TEXT = """

---

> ⚠️ **책임감 있는 게임 안내**
> 에볼루션카지노는 만 19세 이상 성인만 이용 가능합니다.
> 과도한 도박은 개인과 가정에 심각한 피해를 줄 수 있습니다.
> 도박 문제로 어려움을 겪고 계신다면 **한국도박문제예방치유원 ☎ 1336** (24시간 무료상담)에 연락하세요.
> 온라인 상담: [kcgp.or.kr](https://kcgp.or.kr)
"""

# ── 21개 확정 주제 (주제 + 카테고리 + Pexels 쿼리 세트) ──
TOPICS = [
    # ── 카테고리 1: 초보자 교육 및 기술적 신뢰 ──
    {
        "id": 1,
        "topic": "에볼루션 카지노 라이선스의 모든 것: MGA, UKGC 등 보안 안정성 분석",
        "category": "가이드",
        "pexels_queries": ["casino license security certificate", "official gambling regulation", "casino security trust"],
    },
    {
        "id": 2,
        "topic": "모바일 최적화 가이드: 빠른 접속을 위한 에볼루션 설정법",
        "category": "가이드",
        "pexels_queries": ["mobile casino smartphone", "online casino mobile app", "smartphone gaming casino"],
    },
    {
        "id": 3,
        "topic": "에볼루션 입출금 시스템 이해: 안전한 자금 관리를 위한 초보자 매뉴얼",
        "category": "가이드",
        "pexels_queries": ["casino payment deposit withdraw", "online banking casino", "secure payment casino"],
    },
    {
        "id": 4,
        "topic": "인터페이스(UI) 완벽 조작법: 멀티 게임 모드 및 채팅 기능 활용하기",
        "category": "가이드",
        "pexels_queries": ["casino user interface screen", "live casino interface multiple games", "casino chat interface"],
    },
    {
        "id": 5,
        "topic": "에볼루션만의 독점 기술: 듀얼 플레이와 다이렉트 게임 Launch 기술 분석",
        "category": "가이드",
        "pexels_queries": ["casino technology innovation", "live streaming casino studio", "casino dual screen technology"],
    },
    {
        "id": 6,
        "topic": "라이브 스트리밍 품질 최적화: 끊김 없는 게임을 위한 네트워크 환경 설정",
        "category": "가이드",
        "pexels_queries": ["live streaming network setup", "internet connection speed router", "casino streaming HD quality"],
    },
    {
        "id": 7,
        "topic": "에볼루션 카지노 역사: 업계 1위가 된 기술력과 성장 스토리",
        "category": "가이드",
        "pexels_queries": ["casino history evolution timeline", "gambling company headquarters", "casino industry growth"],
    },
    # ── 카테고리 2: 게임별 심층 전략 및 확률 ──
    {
        "id": 8,
        "topic": "라이트닝 바카라 vs 일반 바카라: 승률과 배당의 수학적 차이 분석",
        "category": "바카라",
        "pexels_queries": ["baccarat cards lightning casino", "baccarat table comparison", "casino card game odds"],
    },
    {
        "id": 9,
        "topic": "골든 바카라: 골든 카드를 활용한 수익 극대화 전략",
        "category": "바카라",
        "pexels_queries": ["golden baccarat casino cards", "gold playing cards casino", "baccarat golden strategy"],
    },
    {
        "id": 10,
        "topic": "에볼루션 블랙잭: 전문가들이 말하는 기본 전략(Basic Strategy) 적용법",
        "category": "블랙잭",
        "pexels_queries": ["blackjack basic strategy cards", "blackjack casino table dealer", "card counting blackjack"],
    },
    {
        "id": 11,
        "topic": "라이트닝 룰렛 확률 분석: 번개 번호가 터지는 메커니즘 이해하기",
        "category": "룰렛",
        "pexels_queries": ["roulette wheel lightning bolt", "casino roulette numbers", "lightning roulette casino"],
    },
    {
        "id": 12,
        "topic": "코리안 스피드 바카라: 한국인 딜러와 함께하는 게임의 장단점 리뷰",
        "category": "바카라",
        "pexels_queries": ["korean casino dealer baccarat", "asian live casino dealer", "baccarat speed cards"],
    },
    {
        "id": 13,
        "topic": "에볼루션 게임쇼 TOP 3: 크레이지타임, 모노폴리 라이브 완벽 분석",
        "category": "슬롯/게임쇼",
        "pexels_queries": ["casino game show wheel spin", "crazy time casino colorful", "monopoly live casino board"],
    },
    {
        "id": 14,
        "topic": "바카라 로드맵 분석의 허와 실: 에볼루션 그림 시스템 활용법",
        "category": "바카라",
        "pexels_queries": ["baccarat road map scoreboard", "baccarat pattern analysis", "casino baccarat statistics"],
    },
    # ── 카테고리 3: 트렌드 및 책임감 있는 게임 ──
    {
        "id": 15,
        "topic": "2026년 에볼루션 신규 출시 게임: 최신 라인업 미리보기 및 리뷰",
        "category": "가이드",
        "pexels_queries": ["new casino game launch 2026", "casino innovation new release", "live casino new game"],
    },
    {
        "id": 16,
        "topic": "에볼루션 카지노와 암호화폐: 비트코인 결제 및 보안 트렌드",
        "category": "가이드",
        "pexels_queries": ["bitcoin casino cryptocurrency payment", "crypto gambling blockchain", "digital currency casino"],
    },
    {
        "id": 17,
        "topic": "도박 중독 방지 가이드: 에볼루션 내 자기 제한 기능 설정하는 법",
        "category": "가이드",
        "pexels_queries": ["responsible gambling awareness", "casino self exclusion limit", "gambling addiction prevention"],
    },
    {
        "id": 18,
        "topic": "라이브 딜러와의 에티켓: 건전한 게임 환경을 위한 커뮤니티 가이드",
        "category": "가이드",
        "pexels_queries": ["live casino dealer etiquette", "casino community friendly dealer", "live dealer smile casino"],
    },
    {
        "id": 19,
        "topic": "에볼루션 카지노 FAQ: 유저들이 가장 많이 묻는 질문 10가지",
        "category": "가이드",
        "pexels_queries": ["casino FAQ questions answers", "customer support casino help", "online casino guide beginner"],
    },
    {
        "id": 20,
        "topic": "글로벌 에볼루션 스튜디오 탐방: 라트비아에서 몰타까지의 인프라 분석",
        "category": "가이드",
        "pexels_queries": ["casino studio latvia filming", "live casino studio interior", "casino broadcasting studio"],
    },
    {
        "id": 21,
        "topic": "나에게 맞는 에볼루션 게임 찾기: 성향별 게임 추천 테스트",
        "category": "가이드",
        "pexels_queries": ["casino game selection choice", "casino variety games table", "player choosing casino game"],
    },
]

# ── 내부 링크 맵 (Topic Cluster) ─────────────────
INTERNAL_LINKS = [
    {"slug": "baccarat",    "title": "에볼루션카지노 바카라 완벽 가이드",  "anchor": "에볼루션카지노 바카라"},
    {"slug": "blackjack",   "title": "에볼루션카지노 블랙잭 완벽 가이드",  "anchor": "에볼루션카지노 블랙잭"},
    {"slug": "roulette",    "title": "에볼루션카지노 룰렛 완벽 가이드",    "anchor": "에볼루션카지노 룰렛"},
    {"slug": "slots",       "title": "에볼루션카지노 슬롯 완벽 가이드",    "anchor": "에볼루션카지노 슬롯"},
    {"slug": "live-casino", "title": "에볼루션 라이브카지노 완벽 가이드",  "anchor": "에볼루션 라이브카지노"},
]

# ── [추가된 유틸리티 함수] ────────────────────────

def clean_json_response(text: str) -> str:
    """제미나이 응답에서 순수 JSON만 추출 (안정성 강화)"""
    text = text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    return text.strip()

def get_weighted_related_posts(category: str) -> list:
    """핵심 페이지(바카라/블랙잭 등)에 우선순위를 둔 내부 링크 생성"""
    high_value_slugs = ["baccarat", "blackjack", "live-casino"]
    cat_map = {"바카라": "baccarat", "블랙잭": "blackjack", "룰렛": "roulette", "슬롯/게임쇼": "slots", "가이드": "live-casino"}
    current_cat_slug = cat_map.get(category, "")
    
    candidates = [l for l in INTERNAL_LINKS if l["slug"] != current_cat_slug]
    # 핵심 페이지를 리스트 앞으로 보내 가중치 부여
    candidates.sort(key=lambda x: x["slug"] in high_value_slugs, reverse=True)
    return random.sample(candidates[:4], min(3, len(candidates)))

# ── [수정된 핵심 로직 함수] ────────────────────────

def setup_gemini():
    return genai.Client(api_key=GEMINI_API_KEY)

def load_used_topics() -> list:
    if os.path.exists(USED_CACHE):
        with open(USED_CACHE, "r", encoding="utf-8") as f:
            return json.load(f).get("used_ids", [])
    return []

def save_used_topics(used_ids: list):
    os.makedirs(os.path.dirname(USED_CACHE), exist_ok=True)
    with open(USED_CACHE, "w", encoding="utf-8") as f:
        json.dump({"used_ids": used_ids}, f, ensure_ascii=False, indent=2)

def get_existing_slugs() -> set:
    if not os.path.exists(POSTS_DIR):
        return set()
    return {f.replace(".json", "") for f in os.listdir(POSTS_DIR) if f.endswith(".json")}

def get_available_topics(used_ids: list) -> list:
    """사용되지 않은 주제 반환. 전부 소진되면 리셋."""
    available = [t for t in TOPICS if t["id"] not in used_ids]
    if not available:
        print("  🔄 21개 주제 전부 소진 → 리셋 후 재시작")
        available = TOPICS.copy()
    return available

def generate_titles_with_trending(client, topic: str) -> list:
    """
    제미나이가 오늘의 구글 인기 키워드를 섞어서
    해당 주제로 매력적인 제목 3개를 생성
    """
    prompt = f"""
당신은 10년 경력의 에볼루션카지노 전문 딜러 출신 SEO 컨설턴트입니다.
라이브 카지노 현장 경험을 바탕으로 글을 씁니다.

오늘 날짜: {datetime.now().strftime("%Y년 %m월 %d일")}

다음 주제를 바탕으로, 오늘의 구글 인기 검색 트렌드를 섞어서
한국인 독자에게 매력적인 블로그 제목 3개를 생성하세요.

주제: {topic}

조건:
- "에볼루션카지노" 키워드 반드시 포함
- 클릭하고 싶은 호기심 유발 제목
- 구체적인 수치나 연도 포함 시 더 좋음
- 각 제목은 서로 다른 앵글(초보자용/전략형/최신트렌드형)

JSON 배열만 응답 (다른 텍스트 없이):
["제목1", "제목2", "제목3"]
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
            if text.startswith("json"):
                text = text[4:]
        titles = json.loads(text.strip())
        return titles if isinstance(titles, list) else []
    except Exception as e:
        print(f"  ⚠️ 제목 생성 오류: {e}")
        return [topic]

def generate_post_content(client, title: str, topic: str, category: str) -> dict:
    """
    확정된 제목으로 본문 생성
    페르소나 + 표 + 도입부 전략 + Pexels alt 모두 포함
    """
    prompt = f"""
당신은 10년 경력의 에볼루션카지노 전문 딜러 출신 SEO 컨설턴트입니다.
라이브 카지노 현장 경험을 바탕으로 글을 씁니다.
초보자가 절대 모르는 실전 노하우를 반드시 포함하고, 뻔한 정보는 절대 쓰지 않습니다.
구글 로봇이 즉시 파악할 수 있게 의미론적으로 완벽한 글을 설계합니다.
모든 글은 사이트 전체의 주제적 권위(Topical Authority)를 높이는 방향으로 작성합니다.

글 제목: {title}
주제: {topic}
카테고리: {category}

작성 규칙:
1. 본문은 최소 1500자 이상
2. H2 헤더(## )를 4~6개 포함
3. 구체적인 수치와 통계 포함 (RTP, 승률, 배율 등 실제 데이터)
4. [도입부 필수] 첫 문단에 "이용자들이 가장 많이 하는 실수 TOP 3" 또는 충격적인 통계로 시작
5. 본문 중간에 마크다운 표(|컬럼|컬럼|) 반드시 1개 이상 포함
6. FAQ 5개 포함 (실전 경험에서 나온 질문)
7. SEO 최적화된 자연스러운 키워드 배치
8. slug는 제목을 영문으로 번역한 URL 친화적 형태

다음 JSON 형식으로만 응답 (다른 텍스트 없이):
{{
  "slug": "title-in-english-url-friendly",
  "title": "{title}",
  "description": "포스트 설명 (150자 이내, 키워드 자연스럽게 포함)",
  "keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"],
  "imageAlt": "에볼루션카지노 관련 구체적 이미지 설명 (키워드 포함, 50자 이내)",
  "content": "본문 내용 (마크다운 형식, 1500자 이상, 표 포함)",
  "faq": [
    {{"q": "질문1", "a": "답변1"}},
    {{"q": "질문2", "a": "답변2"}},
    {{"q": "질문3", "a": "답변3"}},
    {{"q": "질문4", "a": "답변4"}},
    {{"q": "질문5", "a": "답변5"}}
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

def fetch_pexels_image(queries: list) -> str:
    """주제별 고정 Pexels 쿼리로 이미지 검색 (fallback 포함)"""
    fallback = "https://images.pexels.com/photos/1871508/pexels-photo-1871508.jpeg"
    for query in queries:
        try:
            res = requests.get(
                "https://api.pexels.com/v1/search",
                headers={"Authorization": PEXELS_API_KEY},
                params={"query": query, "per_page": 5, "orientation": "landscape"},
                timeout=10
            )
            res.raise_for_status()
            photos = res.json().get("photos", [])
            if photos:
                print(f"  ✅ 이미지 확보: '{query}'")
                return random.choice(photos[:5])["src"]["large2x"]
        except Exception as e:
            print(f"  ⚠️ 이미지 오류 ({query}): {e}")
        time.sleep(0.3)
    print("  ⚠️ fallback 이미지 사용")
    return fallback

def get_related_posts(category: str) -> list:
    """카테고리 기반 내부 링크 3개"""
    cat_map = {
        "바카라": "baccarat", "블랙잭": "blackjack",
        "룰렛": "roulette", "슬롯/게임쇼": "slots", "가이드": "live-casino",
    }
    current = cat_map.get(category, "")
    candidates = [l for l in INTERNAL_LINKS if l["slug"] != current]
    return random.sample(candidates, min(3, len(candidates)))

def save_post(slug, content_data, image_url, category, date, related_posts):
    # E-E-A-T 책임감 있는 게임 문구 하드코딩
    content_with_eeat = content_data["content"] + RESPONSIBLE_GAMBLING_TEXT

    post = {
        "slug": slug,
        "title": content_data["title"],
        "description": content_data["description"],
        "category": category,
        "date": date,
        "readTime": f"{max(5, len(content_data['content']) // 300)}분",
        "keywords": content_data.get("keywords", []),
        "image": image_url,
        "imageAlt": content_data.get("imageAlt", content_data["title"]),
        "content": content_with_eeat,
        "faq": content_data.get("faq", []),
        "relatedPosts": related_posts,
    }
    os.makedirs(POSTS_DIR, exist_ok=True)
    filepath = os.path.join(POSTS_DIR, f"{slug}.json")
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(post, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 포스트 저장: {slug}.json")

# ── 메인 ─────────────────────────────────────────
def main():
    print("=" * 55)
    print("  WOORIWIN 블로그 포스트 자동 생성 시작")
    print(f"  날짜: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 55)

    os.makedirs(POSTS_DIR, exist_ok=True)
    client = setup_gemini()

    used_ids = load_used_topics()
    existing_slugs = get_existing_slugs()
    available_topics = get_available_topics(used_ids)

    # 오늘 쓸 주제 3개 랜덤 선택
    selected = random.sample(available_topics, min(POSTS_PER_RUN, len(available_topics)))

    today = datetime.now()
    success = 0

    for i, topic_data in enumerate(selected):
        date = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        topic   = topic_data["topic"]
        category = topic_data["category"]
        pexels_queries = topic_data["pexels_queries"]

        print(f"\n📌 주제 [{topic_data['id']}/21]: {topic[:40]}...")
        print(f"  카테고리: {category}")

        # Step 1: 오늘의 트렌드 키워드 섞어서 제목 3개 생성
        print("  🔍 오늘의 트렌드 키워드로 제목 생성 중...")
        titles = generate_titles_with_trending(client, topic)
        title = titles[0] if titles else topic
        print(f"  📝 선택된 제목: {title}")
        time.sleep(1)

        # Step 2: 본문 생성
        print("  🤖 Gemini 본문 생성 중...")
        content_data = generate_post_content(client, title, topic, category)
        if not content_data:
            continue

        slug = content_data.get("slug", "")
        if not slug or slug in existing_slugs:
            print(f"  ⏭️ 스킵 (슬러그 없음 또는 중복): {slug}")
            used_ids.append(topic_data["id"])
            save_used_topics(used_ids)
            continue

        # Step 3: 주제별 고정 Pexels 쿼리로 이미지
        print(f"  📸 Pexels 이미지 검색 중...")
        image_url = fetch_pexels_image(pexels_queries)

        # Step 4: 관련 포스트
        related_posts = get_related_posts(category)

        # Step 5: 저장 (E-E-A-T 문구 자동 삽입)
        save_post(slug, content_data, image_url, category, date, related_posts)

        used_ids.append(topic_data["id"])
        save_used_topics(used_ids)
        existing_slugs.add(slug)
        success += 1
        time.sleep(2)

    print("\n" + "=" * 55)
    print(f"  완료: {success}개 포스트 생성")
    print(f"  사용된 주제: {len(used_ids)}/21개")
    remaining = [t for t in TOPICS if t["id"] not in used_ids]
    print(f"  남은 주제: {len(remaining)}개")
    print("=" * 55)
    print("\n✨ git add . && git commit -m 'feat: add posts' && git push")

if __name__ == "__main__":
    main()