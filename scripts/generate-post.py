import os
import re
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
BASE_DIR      = os.path.join(os.path.dirname(__file__), "..")
POSTS_DIR     = os.path.join(BASE_DIR, "data", "posts")
USED_CACHE    = os.path.join(BASE_DIR, "data", "used_topics.json")
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

# ── [2번] CTR 스코어링 단어 리스트 ───────────────
# 클릭베이트 위험 단어 제거, SEO 안전 단어 중심
HIGH_CTR_WORDS = [
    "전략", "실전", "2026", "승률", "핵심",
    "노하우", "TOP", "분석", "완벽", "가이드",
    "비교", "차이", "방법", "공개", "검증",
]

# ── [4번] 도입부 유형 랜덤화 리스트 ─────────────
INTRO_TYPES = [
    "이용자들이 가장 많이 하는 실수 TOP 3로 시작",
    "업계 전문가만 아는 충격적인 통계 수치 제시로 시작",
    "10년 딜러 경력의 현장 사례 한 가지로 시작",
    "대부분의 플레이어가 놓치는 핵심 포인트 한 줄로 시작",
    "실제 유저 질문에서 발견한 공통 오해로 시작",
    "오늘 당장 써먹을 수 있는 실전 팁 하나로 시작",
]

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

# ── 페르소나 시스템 지침 (공통) ───────────────────
SYSTEM_INSTRUCTION = (
    "당신은 10년 경력의 에볼루션카지노 전문 딜러 출신 SEO 컨설턴트입니다. "
    "라이브 카지노 현장 경험을 바탕으로 독창적인 실전 노하우를 제공하며 "
    "구글 E-E-A-T를 철저히 준수합니다. "
    "뻔한 정보는 절대 쓰지 않고, 구체적인 수치와 현장 경험을 바탕으로 글을 작성합니다."
)

# ─────────────────────────────────────────────────
# 유틸리티 함수
# ─────────────────────────────────────────────────

def setup_gemini() -> genai.Client:
    return genai.Client(api_key=GEMINI_API_KEY)


def clean_json_response(text: str) -> str:
    """Gemini 응답에서 순수 JSON만 추출"""
    text = text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    return text.strip()


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
    """사용되지 않은 주제 반환. 전부 소진되면 자동 리셋."""
    available = [t for t in TOPICS if t["id"] not in used_ids]
    if not available:
        print("  🔄 21개 주제 전부 소진 → 자동 리셋 후 재시작")
        save_used_topics([])
        available = TOPICS.copy()
    return available


def get_weighted_related_posts(category: str) -> list:
    """핵심 페이지에 우선순위를 둔 내부 링크 3개 반환."""
    high_value_slugs = ["baccarat", "blackjack", "live-casino"]
    cat_map = {
        "바카라": "baccarat", "블랙잭": "blackjack",
        "룰렛": "roulette", "슬롯/게임쇼": "slots", "가이드": "live-casino",
    }
    current_cat_slug = cat_map.get(category, "")
    candidates = [l for l in INTERNAL_LINKS if l["slug"] != current_cat_slug]
    candidates.sort(key=lambda x: x["slug"] in high_value_slugs, reverse=True)
    return random.sample(candidates[:4], min(3, len(candidates)))


# ─────────────────────────────────────────────────
# [1번] JSON 에러 방지 및 재시도 (안정성)
# ─────────────────────────────────────────────────

def safe_generate_content(client: genai.Client, prompt: str, use_search: bool = False, retries: int = 1) -> dict | list | None:
    """
    실패 시 재시도 로직이 포함된 안전한 생성 함수.
    재시도 시 프롬프트 끝에 변형 지시를 추가해 같은 오류 반복을 방지.
    """
    for attempt in range(retries + 1):
        try:
            cfg = {"system_instruction": SYSTEM_INSTRUCTION}
            if use_search:
                cfg["tools"] = [{"google_search": {}}]

            # 재시도 시 프롬프트 살짝 변형 (같은 오류 반복 방지)
            current_prompt = prompt
            if attempt > 0:
                current_prompt += f"\n\n[재시도 {attempt}회차: 반드시 유효한 JSON만 출력할 것. 마크다운 코드블록 없이 순수 JSON만.]"

            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=current_prompt,
                config=cfg,
            )
            cleaned = clean_json_response(response.text)
            return json.loads(cleaned)

        except json.JSONDecodeError as e:
            if attempt < retries:
                print(f"  ⚠️ JSON 파싱 실패({e}), {attempt + 1}회 재시도 중...")
                time.sleep(2)
            else:
                print(f"  ❌ 최종 JSON 파싱 실패 — 포스트 스킵")
                return None
        except Exception as e:
            if attempt < retries:
                print(f"  ⚠️ 생성 실패({e}), {attempt + 1}회 재시도 중...")
                time.sleep(2)
            else:
                print(f"  ❌ 최종 생성 실패 — 포스트 스킵")
                return None


# ─────────────────────────────────────────────────
# [2번] CTR 스코어링 — 돈 되는 제목 선택
# ─────────────────────────────────────────────────

def get_best_title(titles: list) -> str:
    """
    제목들 중 CTR 점수가 가장 높은 것을 선택.
    클릭베이트 위험 단어 제외, SEO 안전 단어 중심.
    """
    def score_title(t: str) -> int:
        return sum(1 for word in HIGH_CTR_WORDS if word in t)

    scored = sorted(titles, key=score_title, reverse=True)
    best = scored[0]
    print(f"  🏆 CTR 스코어링 결과: '{best}' (점수: {score_title(best)})")
    return best


# ─────────────────────────────────────────────────
# [3번] 고유 슬러그 생성 — Gemini가 기존 슬러그와 비교해 생성
# ─────────────────────────────────────────────────

def ensure_unique_slug(slug: str, existing_slugs: set) -> str:
    """
    Gemini가 생성한 슬러그가 중복일 때 최후 방어선.
    날짜 접미사 추가로 유니크 보장.
    """
    if slug not in existing_slugs:
        return slug
    suffix = datetime.now().strftime("%m%d%H%M")
    unique = f"{slug}-{suffix}"
    print(f"  🔄 슬러그 중복 → 변경: {slug} → {unique}")
    return unique


# ─────────────────────────────────────────────────
# Gemini API 호출 함수
# ─────────────────────────────────────────────────

def generate_titles_with_trending(client: genai.Client, topic: str) -> list:
    """Google Search 툴로 트렌드 반영 제목 3개 생성. safe_generate_content 사용."""
    prompt = f"""
오늘 날짜: {datetime.now().strftime("%Y년 %m월 %d일")}

다음 주제를 바탕으로, 오늘의 구글 인기 검색 트렌드를 섞어서
한국인 독자에게 매력적인 블로그 제목 3개를 생성하세요.

주제: {topic}

조건:
- "에볼루션카지노" 키워드 반드시 포함
- 클릭하고 싶은 호기심 유발 제목
- 구체적인 수치나 연도 포함 시 더 좋음
- 각 제목은 서로 다른 앵글(초보자용 / 전략형 / 최신트렌드형)

JSON 배열만 응답 (다른 텍스트 없이):
["제목1", "제목2", "제목3"]
"""
    result = safe_generate_content(client, prompt, use_search=True, retries=1)
    if isinstance(result, list) and result:
        return result
    print(f"  ⚠️ 제목 생성 실패 → 원본 주제로 대체")
    return [topic]


def generate_post_content(
    client: genai.Client,
    title: str,
    topic: str,
    category: str,
    fixed_queries: list,
    existing_slugs: set,
    intro_type: str,          # [4번] 도입부 유형 주입
) -> dict | None:
    """
    확정된 제목으로 본문 생성.
    - [1번] safe_generate_content로 재시도 포함
    - [3번] 기존 슬러그 목록 주입 → Gemini가 겹치지 않게 생성
    - [4번] 도입부 유형 랜덤 주입
    """
    # 기존 슬러그 최근 50개만 프롬프트에 주입 (토큰 절약)
    slugs_sample = list(existing_slugs)[-50:]
    slugs_list   = "\n".join(f"- {s}" for s in slugs_sample) if slugs_sample else "없음"

    prompt = f"""
글 제목: {title}
주제: {topic}
카테고리: {category}
참고 이미지 키워드(영문): {", ".join(fixed_queries)}

작성 규칙:
1. 본문은 최소 1500자 이상
2. H2 헤더(## )를 4~6개 포함
3. 수치를 제시할 때는 반드시 "이론적 RTP 기준" 또는 "에볼루션 공식 가이드에 따르면" 등 출처/전제 조건을 붙여서 작성할 것.
4. 10년 딜러 개인 경험임을 명시하여 주관적 노하우임을 강조할 것
5. [도입부 필수] 반드시 "{intro_type}" 방식으로 첫 문단을 작성할 것
6. 본문 중간에 마크다운 표(|컬럼|컬럼|) 반드시 1개 이상 포함
7. FAQ 5개 포함 (실전 경험에서 나온 질문)
8. SEO 최적화된 자연스러운 키워드 배치
9. pexels_query 필드에 이 글에 딱 맞는 영문 이미지 검색어 1개를 제안
10. [YMYL 방어 규칙]: RTP, 승률, 배당률 등 수치를 언급할 때는 반드시 '이론적 통계' 또는 '공식 가이드라인에 따른 수치'임을 명시할 것.
11. 절대 '무조건', '필승', '수익 보장' 같은 단어를 사용하지 말고 '전략적 접근', '리스크 관리'라는 표현을 사용할 것.
12. 모든 통계 데이터의 출처는 '에볼루션 공식 제공 정보'를 기반으로 한다고 언급할 것.

⚠️ 슬러그 생성 규칙:
- 아래 기존 슬러그 목록과 절대 겹치지 않게 생성
- 영문 소문자 + 숫자 + 하이픈만 사용, 50자 이내
- 에볼루션카지노 관련 키워드 포함 권장

기존 슬러그 목록:
{slugs_list}

다음 JSON 형식으로만 응답 (마크다운 코드블록 없이 순수 JSON만):
{{
  "slug": "unique-english-url-friendly-slug",
  "title": "{title}",
  "description": "포스트 설명 (150자 이내, 키워드 자연스럽게 포함)",
  "keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"],
  "imageAlt": "에볼루션카지노 관련 구체적 이미지 설명 (키워드 포함, 50자 이내)",
  "pexels_query": "suggested-english-image-search-query",
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
    return safe_generate_content(client, prompt, use_search=False, retries=1)


def fetch_pexels_image(queries: list) -> str:
    """Gemini 추천 쿼리 → 고정 쿼리 순차 시도, 모두 실패 시 fallback."""
    fallback = "https://images.pexels.com/photos/1871508/pexels-photo-1871508.jpeg"
    for query in queries:
        if not query:
            continue
        try:
            res = requests.get(
                "https://api.pexels.com/v1/search",
                headers={"Authorization": PEXELS_API_KEY},
                params={"query": query, "per_page": 5, "orientation": "landscape"},
                timeout=10,
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


def save_post(slug, content_data, image_url, category, date, related_posts):
    """E-E-A-T 책임감 있는 게임 문구 하드코딩 후 JSON 저장."""
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


# ─────────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────────

def main():
    print("=" * 55)
    print("  WOORIWIN 블로그 포스트 자동 생성 시작")
    print(f"  날짜: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 55)

    os.makedirs(POSTS_DIR, exist_ok=True)
    client = setup_gemini()

    used_ids       = load_used_topics()
    existing_slugs = get_existing_slugs()
    available      = get_available_topics(used_ids)
    selected       = random.sample(available, min(POSTS_PER_RUN, len(available)))

    today   = datetime.now()
    success = 0

    for i, topic_data in enumerate(selected):
        date           = (today - timedelta(days=i)).strftime("%Y-%m-%d")
        topic          = topic_data["topic"]
        category       = topic_data["category"]
        pexels_queries = topic_data["pexels_queries"]

        print(f"\n📌 주제 [{topic_data['id']}/21]: {topic[:45]}...")
        print(f"   카테고리: {category}")

        # Step 1 — 트렌드 키워드 반영 제목 3개 생성
        print("  🔍 트렌드 키워드로 제목 생성 중...")
        titles = generate_titles_with_trending(client, topic)

        # [2번] CTR 스코어링으로 최고 제목 선택
        title = get_best_title(titles)
        time.sleep(1)

        # [4번] 도입부 유형 랜덤 선택
        intro_type = random.choice(INTRO_TYPES)
        print(f"  📖 도입부 유형: {intro_type}")

        # Step 2 — 본문 생성
        # [1번] safe_generate_content 재시도 포함
        # [3번] 기존 슬러그 목록 전달 → Gemini가 겹치지 않게 생성
        # [4번] intro_type 주입
        print("  🤖 Gemini 본문 생성 중...")
        content_data = generate_post_content(
            client, title, topic, category,
            pexels_queries, existing_slugs, intro_type
        )
        if not content_data:
            continue

        # [3번] 슬러그 유니크 보장 (Gemini 생성 후 2중 검증)
        raw_slug = content_data.get("slug", "")
        if not raw_slug:
            print("  ⏭️ 슬러그 없음 → 스킵")
            used_ids.append(topic_data["id"])
            save_used_topics(used_ids)
            continue

        slug = ensure_unique_slug(raw_slug, existing_slugs)

        # Step 3 — 이미지 검색 (Gemini 추천 → 고정 쿼리 순차)
        gemini_query  = content_data.get("pexels_query", "")
        image_queries = ([gemini_query] if gemini_query else []) + pexels_queries
        print("  📸 Pexels 이미지 검색 중...")
        image_url = fetch_pexels_image(image_queries)

        # Step 4 — 가중치 적용된 내부 링크
        related_posts = get_weighted_related_posts(category)

        # Step 5 — 저장
        content_data["slug"] = slug  # ensure_unique_slug 결과 반영
        save_post(slug, content_data, image_url, category, date, related_posts)

        used_ids.append(topic_data["id"])
        save_used_topics(used_ids)
        existing_slugs.add(slug)
        success += 1
        time.sleep(2)

    print("\n" + "=" * 55)
    print(f"  완료: {success}개 포스트 생성")
    remaining = [t for t in TOPICS if t["id"] not in used_ids]
    print(f"  사용된 주제: {len(used_ids)}/21 | 남은 주제: {len(remaining)}")
    print("=" * 55)
    print("\n✨ git add . && git commit -m 'auto: add posts' && git push")


if __name__ == "__main__":
    main()