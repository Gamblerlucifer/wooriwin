import os
import re
import json
import time
import requests
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))
from datetime import datetime, timedelta, timezone
from google import genai
import random

SITE_BASE_URL = 'https://wooriwin.com'

# ── API 키 ────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")

# ── 경로 ──────────────────────────────────────────
BASE_DIR      = os.path.join(os.path.dirname(__file__), "..")
POSTS_DIR     = os.path.join(BASE_DIR, "data", "posts")
POSTS_PER_RUN = random.randint(1, 3)  # 하루 1~3개 랜덤 (과도한 발행으로 인한 색인 적체 방지)

# ── E-E-A-T 고정 문구 (모든 글 하단 hard-code) ────
RESPONSIBLE_GAMBLING_TEXT = """

---

> ⚠️ **책임감 있는 게임 안내**
> 에볼루션카지노는 만 19세 이상 성인만 이용 가능합니다.
> 과도한 도박은 개인과 가정에 심각한 피해를 줄 수 있습니다.
> 도박 문제로 어려움을 겪고 계신다면 **한국도박문제예방치유원 ☎ 1336** (24시간 무료상담)에 연락하세요.
> 온라인 상담: [kcgp.or.kr](https://kcgp.or.kr)
"""

# ── 도입부 유형 랜덤화 ────────────────────────────
INTRO_TYPES = [
    "사용자들이 자주 혼동하는 인터페이스 설정 문제로 시작",
    "플레이 환경 최적화 관점의 설명으로 시작",
    "UX 분석 기반의 기능 설명으로 시작",
    "초보자들이 놓치기 쉬운 설정 요소 소개로 시작",
    "리스크 관리 관점의 플레이 환경 설명으로 시작",
    "실제 사용자 FAQ 기반 설명으로 시작",
]

# ─────────────────────────────────────────────────
# 카테고리 + 핵심 키워드 (50개 하드코딩 주제 대신 동적 생성)
# ─────────────────────────────────────────────────
CATEGORIES = {
    "에볼루션 가이드": {
        "keywords": ["가입 방법", "인터페이스", "독점 기술", "역사와 성장", "플랫폼 구조"],
        "pexels_queries": ["live casino studio", "casino platform interface", "online casino environment"],
        "slug_prefix": "live-casino",
        "slug_suffixes": ["guide", "tips", "review", "explained", "overview", "complete", "beginners", "advanced"],
    },
    "바카라 가이드": {
        "keywords": ["기본 규칙", "라이트닝 바카라", "스피드 바카라", "스퀴즈 바카라", "로드맵 시스템"],
        "pexels_queries": ["baccarat casino table", "baccarat cards dealer", "live baccarat"],
        "slug_prefix": "baccarat",
        "slug_suffixes": ["strategy", "rules", "tips", "guide", "winning", "odds", "how-to", "explained"],
    },
    "블랙잭 가이드": {
        "keywords": ["기본 전략", "인피니트 블랙잭", "라이트닝 블랙잭", "사이드 베팅", "파워 블랙잭"],
        "pexels_queries": ["blackjack casino table", "blackjack dealer", "live blackjack"],
        "slug_prefix": "blackjack",
        "slug_suffixes": ["strategy", "rules", "tips", "guide", "basic-strategy", "odds", "how-to", "variants"],
    },
    "게임쇼 분석": {
        "keywords": ["크레이지타임", "모노폴리 라이브", "드림캐처", "메가볼", "게임쇼 비교"],
        "pexels_queries": ["casino game show wheel", "live game show casino", "casino entertainment"],
        "slug_prefix": "game-show",
        "slug_suffixes": ["review", "guide", "analysis", "tips", "explained", "how-to-play", "odds", "strategy"],
    },
    "룰렛 & 포커": {
        "keywords": ["유럽식 룰렛", "라이트닝 룰렛", "임머시브 룰렛", "카지노 홀덤", "3 카드 포커"],
        "pexels_queries": ["roulette wheel casino", "live roulette dealer", "casino poker table"],
        "slug_prefix": "roulette",
        "slug_suffixes": ["strategy", "guide", "tips", "odds", "how-to", "variants", "explained", "winning"],
    },
    "최신 트렌드": {
        "keywords": ["2026 신규 게임", "암호화폐 결제", "AI 기술", "글로벌 스튜디오", "VR 카지노"],
        "pexels_queries": ["casino innovation 2026", "casino technology", "live casino studio"],
        "slug_prefix": "casino-trends",
        "slug_suffixes": ["2026", "update", "new", "latest", "future", "review", "guide", "overview"],
    },
    "자금 관리": {
        "keywords": ["세션 예산", "입출금 시스템", "손실 한도", "베팅 단위", "세션 관리"],
        "pexels_queries": ["casino budget management", "money management casino", "casino bankroll"],
        "slug_prefix": "bankroll",
        "slug_suffixes": ["management", "strategy", "guide", "tips", "budgeting", "limits", "control", "plan"],
    },
    "보안 및 라이선스": {
        "keywords": ["MGA UKGC 라이선스", "암호화 보안", "RNG 검증", "플랫폼 선택", "고객센터 활용"],
        "pexels_queries": ["casino license security", "online security casino", "casino safety"],
        "slug_prefix": "casino-safety",
        "slug_suffixes": ["license", "security", "guide", "tips", "verified", "trusted", "how-to", "checklist"],
    },
    "모바일 최적화": {
        "keywords": ["앱 vs 브라우저", "스트리밍 최적화", "iOS vs 안드로이드", "네트워크 설정", "태블릿 활용"],
        "pexels_queries": ["mobile casino smartphone", "smartphone gaming casino", "tablet casino"],
        "slug_prefix": "mobile-casino",
        "slug_suffixes": ["guide", "tips", "setup", "optimization", "ios", "android", "streaming", "settings"],
    },
    "책임감 있는 게임": {
        "keywords": ["기본 원칙", "자기 제한", "도박 문제 예방", "딜러 에티켓", "초보자 FAQ"],
        "pexels_queries": ["responsible gambling", "casino healthy gaming", "gambling prevention"],
        "slug_prefix": "responsible-gambling",
        "slug_suffixes": ["guide", "tips", "limits", "prevention", "self-control", "faq", "principles", "rules"],
    },
}

# ── 내부 링크 맵 (Topic Cluster) ─────────────────
INTERNAL_LINKS = [
    {"slug": "baccarat",    "title": "에볼루션카지노 바카라 완벽 가이드",  "anchor": "에볼루션카지노 바카라"},
    {"slug": "blackjack",   "title": "에볼루션카지노 블랙잭 완벽 가이드",  "anchor": "에볼루션카지노 블랙잭"},
    {"slug": "roulette",    "title": "에볼루션카지노 룰렛 완벽 가이드",    "anchor": "에볼루션카지노 룰렛"},
    {"slug": "slots",       "title": "에볼루션카지노 슬롯 완벽 가이드",    "anchor": "에볼루션카지노 슬롯"},
    {"slug": "live-casino", "title": "에볼루션 라이브카지노 완벽 가이드",  "anchor": "에볼루션 라이브카지노"},
]

# ── 카테고리 → 게임 페이지 매핑 (Topic Cluster 강화) ─
CATEGORY_TO_PAGE = {
    "에볼루션 가이드":   {"slug": "live-casino",         "anchor": "에볼루션 라이브카지노 완벽 가이드"},
    "바카라 가이드":     {"slug": "baccarat",            "anchor": "에볼루션카지노 바카라 완벽 가이드"},
    "블랙잭 가이드":     {"slug": "blackjack",           "anchor": "에볼루션카지노 블랙잭 완벽 가이드"},
    "게임쇼 분석":       {"slug": "slots",               "anchor": "에볼루션카지노 슬롯 완벽 가이드"},
    "룰렛 & 포커":       {"slug": "roulette",            "anchor": "에볼루션카지노 룰렛 완벽 가이드"},
    "최신 트렌드":       {"slug": "live-casino",         "anchor": "에볼루션 라이브카지노 완벽 가이드"},
    "자금 관리":         {"slug": "responsible-gaming",  "anchor": "책임감 있는 게임 가이드"},
    "보안 및 라이선스":  {"slug": "about",               "anchor": "WOORIWIN 소개"},
    "모바일 최적화":     {"slug": "live-casino",         "anchor": "에볼루션 라이브카지노 완벽 가이드"},
    "책임감 있는 게임":  {"slug": "responsible-gaming",  "anchor": "책임감 있는 게임 가이드"},
}

# ── 작성자 데이터 ─────────────────────────────────
AUTHORS = {
    "박성준": {
        "role": "WOORIWIN 대표",
        "bio": "에볼루션카지노 전문 콘텐츠 분석팀 · 바카라·블랙잭·룰렛 가이드 제공",
        "image": "/about/01.jpg",
        "url": "/about",
        "experience": "15년+",
        "specialty": ["보안 및 라이선스", "최신 트렌드"],
    },
    "김도현": {
        "role": "라이브카지노 전문가",
        "bio": "에볼루션카지노 전문 콘텐츠 분석팀 · 바카라·블랙잭·룰렛 가이드 제공",
        "image": "/about/02.jpg",
        "url": "/about",
        "experience": "10년+",
        "specialty": ["바카라 가이드", "블랙잭 가이드", "룰렛 & 포커", "게임쇼 분석"],
    },
    "이수연": {
        "role": "콘텐츠 전문가",
        "bio": "에볼루션카지노 전문 콘텐츠 분석팀 · 바카라·블랙잭·룰렛 가이드 제공",
        "image": "/about/03.jpg",
        "url": "/about",
        "experience": "8년+",
        "specialty": ["에볼루션 가이드", "모바일 최적화"],
    },
    "최민석": {
        "role": "에디터",
        "bio": "에볼루션카지노 전문 콘텐츠 분석팀 · 바카라·블랙잭·룰렛 가이드 제공",
        "image": "/about/04.jpg",
        "url": "/about",
        "experience": "12년+",
        "specialty": ["에볼루션 가이드", "최신 트렌드", "자금 관리"],
    },
    "정혜진": {
        "role": "책임도박 담당",
        "bio": "에볼루션카지노 전문 콘텐츠 분석팀 · 바카라·블랙잭·룰렛 가이드 제공",
        "image": "/about/05.jpg",
        "url": "/about",
        "experience": "11년+",
        "specialty": ["책임감 있는 게임", "자금 관리"],
    },
    "한재원": {
        "role": "커뮤니티 매니저",
        "bio": "에볼루션카지노 전문 콘텐츠 분석팀 · 바카라·블랙잭·룰렛 가이드 제공",
        "image": "/about/06.jpg",
        "url": "/about",
        "experience": "6년+",
        "specialty": ["에볼루션 가이드", "모바일 최적화"],
    },
}

# 카테고리별 담당 작성자 목록 (동일 카테고리는 랜덤 배정)
CATEGORY_TO_AUTHORS = {
    "에볼루션 가이드":   ["이수연", "최민석", "한재원"],
    "바카라 가이드":     ["김도현"],
    "블랙잭 가이드":     ["김도현"],
    "게임쇼 분석":       ["김도현"],
    "룰렛 & 포커":       ["김도현"],
    "최신 트렌드":       ["박성준", "최민석"],
    "자금 관리":         ["최민석", "정혜진"],
    "보안 및 라이선스":  ["박성준"],
    "모바일 최적화":     ["이수연", "한재원"],
    "책임감 있는 게임":  ["정혜진"],
}


def get_author_for_category(category: str) -> dict:
    """카테고리에 맞는 작성자를 랜덤 배정."""
    candidates = CATEGORY_TO_AUTHORS.get(category, list(AUTHORS.keys()))
    name = random.choice(candidates)
    return {"name": name, **AUTHORS[name]}


# ── 카테고리별 제목 키워드 풀 ────────────────────
CATEGORY_TITLE_KEYWORDS = {
    "에볼루션 가이드":   ["에볼루션게이밍", "에볼루션 게이밍", "Evolution Gaming", "에볼루션카지노", "라이브카지노"],
    "바카라 가이드":     ["에볼루션바카라", "에볼루션 바카라", "바카라", "라이브바카라", "라이브 바카라"],
    "블랙잭 가이드":     ["에볼루션블랙잭", "에볼루션 블랙잭", "블랙잭", "라이브블랙잭", "라이브 블랙잭"],
    "게임쇼 분석":       ["크레이지타임", "모노폴리라이브", "라이브게임쇼", "에볼루션게임쇼", "드림캐처"],
    "룰렛 & 포커":       ["라이트닝룰렛", "라이트닝 룰렛", "룰렛", "라이브룰렛", "카지노홀덤"],
    "최신 트렌드":       ["에볼루션게이밍", "에볼루션 게이밍", "라이브카지노", "온라인카지노", "카지노 트렌드"],
    "자금 관리":         ["카지노 자금관리", "뱅크롤", "베팅 전략", "카지노 예산", "손실 관리"],
    "보안 및 라이선스":  ["카지노 보안", "라이선스 카지노", "안전한 카지노", "MGA 라이선스", "카지노 인증"],
    "모바일 최적화":     ["모바일카지노", "모바일 카지노", "스마트폰 카지노", "모바일 바카라", "앱 카지노"],
    "책임감 있는 게임":  ["책임감있는 게임", "도박 중독 예방", "안전한 게임", "카지노 자기제한", "건전한 게임문화"],
}


# ── 페르소나 시스템 지침 ──────────────────────────
SYSTEM_INSTRUCTION = """
당신은 에볼루션카지노 라이브 게임을 깊이 이해하는 전문 콘텐츠 팀입니다.
글의 '제목'이 독자에게 한 약속(전략 분석, 규칙 설명, 트렌드 비교, 환경 가이드 등)을
본문이 정확히 충족시키는 것을 최우선 원칙으로 삼습니다.
제목과 실제 본문의 주제가 어긋나면(예: 제목은 '전략'인데 본문은 '화면 설정'만 다룸)
독자 신뢰와 검색 품질 평가에 직접적인 악영향을 준다는 점을 항상 인지하십시오.

Google E-E-A-T, Helpful Content, YMYL 기준을 엄격히 준수합니다.

━━━ 절대 금지 표현 ━━━
- 수익 보장·승률 예측·결과 보장 표현 금지
- 특정 베팅을 추천하거나 유도하는 표현 금지
- '무조건', '절대', '반드시' 등 단정적 행동 지시 금지
- '손실을 최소화하는 방법' 등 손익을 약속하는 표현 금지
- '인생을 바꿀 수 있습니다' 등 과장된 당첨 기대 표현 금지
- 검증 불가능한 전문가 경력·현장 경험 설정 금지
- 본문에 'YMYL', 'E-E-A-T', 'EEAT' 같은 SEO 용어 직접 노출 금지

━━━ 올바른 표현 기준 ━━━
- RTP·하우스 엣지 수치는 사실로 제시하되 베팅 유도 없이 서술
- 전략 설명 시 '고려할 수 있습니다', '참고할 수 있습니다' 등 중립 표현 사용
- 게임 선택은 플레이어 본인의 판단임을 항상 명시
- 모든 RTP 수치 언급 시 '이론적 기댓값이며 실제 결과와 다를 수 있습니다' 병기
- 출처 명시: 'Evolution Gaming 공식 게임 수학 문서 기준'

━━━ 필수 포함 요소 ━━━
- 손실 위험 안내 문구 본문 내 1회 이상 포함
- eCOGRA 등 공인 감사기관 언급으로 신뢰도 강화
- 마크다운 표 1개 이상 (RTP 비교, 게임 비교 등)
- 본문 최소 1600자 이상

━━━ 콘텐츠 관점 ━━━
제목이 암시하는 주제(아래 '본문 핵심 관점' 지시를 따름)를 본문이 실제로 다루도록 작성하고,
그 안에서 사실 기반 정보와 사용자 편의 중심의 중립적·설명형 문체를 유지합니다.
"""

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


def get_existing_posts() -> list:
    """기존 포스트의 title, slug, category 전체 반환."""
    if not os.path.exists(POSTS_DIR):
        return []
    posts = []
    for f in os.listdir(POSTS_DIR):
        if not f.endswith(".json"):
            continue
        try:
            with open(os.path.join(POSTS_DIR, f), "r", encoding="utf-8") as fp:
                p = json.load(fp)
                posts.append({
                    "slug": p.get("slug", ""),
                    "title": p.get("title", ""),
                    "category": p.get("category", ""),
                })
        except Exception:
            continue
    return posts


def get_existing_slugs() -> set:
    if not os.path.exists(POSTS_DIR):
        return set()
    return {f.replace(".json", "") for f in os.listdir(POSTS_DIR) if f.endswith(".json")}


# ─────────────────────────────────────────────────
# 중복 검사 — 핵심 단어 3개 이상 겹치면 중복
# ─────────────────────────────────────────────────

# 불용어 (의미 없는 공통 단어 제거)
STOP_WORDS = {
    "에볼루션카지노", "에볼루션", "카지노", "위한", "가이드", "이해", "활용",
    "방법", "설정", "분석", "관리", "최적화", "환경", "플레이", "라이브",
    "vs", "&", "·", "-", "—",
}

def extract_keywords(title: str) -> set:
    """제목에서 의미있는 단어만 추출."""
    # 공백, 콜론, 쉼표 등으로 분리
    words = re.split(r'[\s:,()·\-—|]+', title)
    # 2글자 이상 + 불용어 제외
    return {w for w in words if len(w) >= 2 and w not in STOP_WORDS}


def is_duplicate_title(new_title: str, existing_titles: list, threshold: int = 3) -> bool:
    """기존 제목과 핵심 단어가 threshold 개 이상 겹치면 중복."""
    new_words = extract_keywords(new_title)
    for old in existing_titles:
        old_words = extract_keywords(old)
        overlap = new_words & old_words
        if len(overlap) >= threshold:
            print(f"  ⚠️ 중복 단어 {len(overlap)}개 발견: {overlap}")
            return True
    return False


# ─────────────────────────────────────────────────
# Gemini 안전 호출
# ─────────────────────────────────────────────────

def safe_generate_content(client: genai.Client, prompt: str, use_search: bool = False, retries: int = 3):
    for attempt in range(retries + 1):
        try:
            cfg = {"system_instruction": SYSTEM_INSTRUCTION}
            if use_search:
                cfg["tools"] = [{"google_search": {}}]
            current_prompt = prompt
            if attempt > 0:
                current_prompt += f"\n\n[재시도 {attempt}회차: 반드시 유효한 JSON만 출력할 것.]"
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
# 제목 생성 — 중복 회피 로직 포함
# ─────────────────────────────────────────────────

def generate_unique_title(client: genai.Client, category: str, keyword: str, existing_titles: list, max_attempts: int = 3) -> str:
    """기존 제목과 중복되지 않는 새 제목 생성."""
    
    existing_sample = existing_titles[-20:] if existing_titles else []
    existing_list = "\n".join(f"- {t}" for t in existing_sample) if existing_sample else "없음"
    
    # 카테고리별 키워드 풀에서 랜덤 선택
    title_kw_pool = CATEGORY_TITLE_KEYWORDS.get(category, ["에볼루션카지노"])
    title_kw = random.choice(title_kw_pool)
    
    for attempt in range(max_attempts):
        prompt = f"""
오늘 날짜: {datetime.now().strftime("%Y년 %m월 %d일")}

다음 조건으로 한국인 독자에게 매력적인 블로그 제목 3개를 생성하세요.

카테고리: {category}
핵심 키워드: {keyword}
제목에 반드시 포함할 브랜드/게임 키워드: {title_kw}

조건:
- 위 브랜드/게임 키워드를 제목 어디에나 자연스럽게 포함 (반드시 앞에 올 필요 없음)
- "에볼루션카지노"를 항상 제목 맨 앞에 쓰는 패턴 금지
- 정보형·가이드형 톤 유지
- 과장형·선정적 표현 금지
- 수치 보장·승률 예측·결과 보장 표현 절대 금지
- 각 제목은 서로 다른 앵글로 작성
- 제목에 콜론(:) 사용 금지
- 25~45자 사이

제목 패턴 예시 (다양하게):
- "바카라 로드맵 시스템의 허와 실 | 라이브바카라 분석"
- "라이트닝 룰렛 배당률과 RTP 완벽 해설"
- "뱅크롤 관리 황금법칙 카지노 자금관리 가이드"
- "모바일카지노 스트리밍 최적화 완벽 설정법"

⚠️ 절대 금지 — 아래 기존 제목들과 핵심 단어 3개 이상 겹치는 제목 금지:
{existing_list}

기존 제목들과 완전히 다른 각도의 새로운 제목을 만드세요.

출력 형식: JSON 배열만 출력 (마크다운 코드블록 없이)
예시: ["제목1", "제목2", "제목3"]
"""
        result = safe_generate_content(client, prompt, use_search=True, retries=1)
        if not isinstance(result, list) or not result:
            print(f"  ⚠️ 제목 생성 실패 ({attempt + 1}/{max_attempts})")
            continue
        
        # 중복 체크 통과한 제목 찾기
        for title in result:
            if not is_duplicate_title(title, existing_titles):
                print(f"  🏆 선택된 제목: '{title}'")
                return title
        
        print(f"  🔄 모든 제목이 중복 — 재시도 ({attempt + 1}/{max_attempts})")
        time.sleep(1)
    
    # 최후 fallback — 카테고리+키워드+타임스탬프
    fallback = f"에볼루션카지노 {keyword} {datetime.now().strftime('%m월 %d일')} 인사이트"
    print(f"  ⚠️ Fallback 제목 사용: '{fallback}'")
    return fallback


# ─────────────────────────────────────────────────
# 제목 유형별 본문 핵심 관점 결정 (제목-본문 불일치 방지)
# ─────────────────────────────────────────────────

def get_content_angle(title: str) -> str:
    """제목에 포함된 단어를 보고, 그 제목이 독자에게 약속한 내용을
    본문이 실제로 담도록 핵심 작성 관점을 동적으로 지정한다.
    (예: 제목이 '전략'인데 본문이 '화면 설정' 얘기만 하는 괴리 방지)"""
    if any(k in title for k in ["전략", "공략법", "필승", "노하우", "팁"]):
        return (
            "제목이 '전략/공략/팁'을 약속했으므로, 베팅 라운드를 진행하며 고려할 수 있는 "
            "판단 기준·체크포인트·흐름 읽는 법 등 '의사결정에 실질적으로 도움이 되는 내용'을 "
            "중심으로 작성 (수익·승률을 보장하는 표현은 절대 금지하되, '전략'이라는 제목에 걸맞은 "
            "구체적 사고 과정과 고려 요소를 다룰 것 — 단순 화면·환경 설정 안내로 대체하지 말 것)"
        )
    if any(k in title for k in ["가이드", "방법", "안내", "이용", "설치"]):
        return (
            "제목이 '가이드/방법/안내'를 약속했으므로, 절차를 단계별로 안내하고 "
            "처음 접하는 사람이 바로 따라할 수 있는 실용적인 정보 전달을 중심으로 작성"
        )
    if any(k in title for k in ["분석", "비교", "특징", "구성", "탐색"]):
        return (
            "제목이 '분석/비교'를 약속했으므로, 인터페이스·UX·게임 구조 등을 "
            "구체적인 기준으로 비교하고 차이점을 짚어주는 내용을 중심으로 작성"
        )
    if any(k in title for k in ["트렌드", "인사이트", "소식", "이슈", "전망"]):
        return (
            "제목이 '트렌드/인사이트'를 약속했으므로, 최근 변화나 흐름과 그것이 "
            "플레이어에게 갖는 의미를 중심으로 작성"
        )
    if any(k in title for k in ["규칙", "룰", "방식", "메커니즘"]):
        return (
            "제목이 '규칙/방식'을 약속했으므로, 게임 진행 방식과 핵심 규칙을 "
            "정확하고 이해하기 쉽게 설명하는 내용을 중심으로 작성"
        )
    return (
        "제목이 독자에게 암시하는 핵심 주제를 정확히 파악하여, "
        "그 주제에서 벗어나지 않는 내용을 중심으로 작성"
    )


# ─────────────────────────────────────────────────
# 본문 생성
# ─────────────────────────────────────────────────

def generate_post_content(
    client: genai.Client,
    title: str,
    category: str,
    keyword: str,
    fixed_queries: list,
    existing_slugs: set,
    intro_type: str,
    slug_prefix: str = "",
    slug_suffixes: list = None,
):
    slugs_sample = list(existing_slugs)[-50:]
    slugs_list = "\n".join(f"- {s}" for s in slugs_sample) if slugs_sample else "없음"
    if not slug_suffixes:
        slug_suffixes = ["guide", "tips", "review", "strategy"]
    random_suffix = random.choice(slug_suffixes)

    prompt = f"""
글 제목: {title}
카테고리: {category}
핵심 키워드: {keyword}
참고 이미지 키워드(영문): {", ".join(fixed_queries)}

작성 규칙:
1. 본문은 최소 1600자 이상 작성
2. H2 헤더(##)를 4~6개 포함
3. 사용자 경험 중심의 설명형 콘텐츠로 작성
4. [본문 핵심 관점 — 반드시 준수] {get_content_angle(title)}
   ⚠️ 위 관점이 제목과 어긋나 보이더라도, 제목이 약속한 주제를 본문이 충족하는 것이
   화면 설정/인터페이스 안내보다 항상 우선합니다. (제목="전략" → 본문도 전략 이야기를 해야 함)
5. 첫 문단 도입부 스타일: {intro_type}
6. 본문 중간에 마크다운 표(|컬럼|컬럼|) 최소 1개 포함
7. FAQ 5개 포함 (초보자 관점 질문 포함)
8. SEO 키워드는 자연스럽게 배치
9. pexels_query 필드에 본문 주제와 어울리는 구체적인 영문 이미지 검색어 1개 생성

[YMYL 필수 준수 사항]
10. [절대 금지] 특정 베팅을 권장·유도하는 표현 금지
11. [절대 금지] '무조건', '절대', '반드시' 등 단정적 행동 지시 금지
12. [절대 금지] 손익 보장 표현 금지
13. [절대 금지] 과장된 당첨 기대 표현 금지
14. [절대 금지] 본문에 'YMYL', 'E-E-A-T', 'EEAT', 'SEO' 같은 용어 직접 노출 금지
15. [필수] RTP 수치 언급 시 반드시 '이론적 기댓값이며 실제 결과와 다를 수 있습니다' 병기
16. [필수] 출처 명시: 'Evolution Gaming 공식 게임 수학 문서 기준' 본문 내 1회 이상 포함
17. [필수] 손실 위험 안내 문구 본문 내 1회 이상 포함
18. [필수] eCOGRA 등 공인 감사기관 언급으로 신뢰도 강화

⚠️ 슬러그 생성 규칙:
- 아래 기존 슬러그 목록과 절대 겹치지 않게 생성
- 영문 소문자 + 숫자 + 하이픈만 사용, 50자 이내
- 반드시 슬러그 prefix로 시작: {slug_prefix}
- prefix 다음에 핵심 키워드 영문 번역 + suffix 중 하나 조합
- 예시: {slug_prefix}-keyword-{random_suffix}
- "evolution-casino", "interface", "ux" 단어 슬러그에 사용 금지

기존 슬러그 목록:
{slugs_list}

다음 JSON 형식으로만 응답 (마크다운 코드블록 없이 순수 JSON만):
{{
  "slug": "unique-english-url-friendly-slug",
  "title": "{title}",
  "description": "포스트 설명 (150자 이내, 키워드 자연스럽게 포함)",
  "keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"],
  "imageAlt": "에볼루션카지노 관련 구체적 이미지 설명 (50자 이내)",
  "pexels_query": "suggested-english-image-search-query",
  "content": "본문 내용 (마크다운 형식, 1600자 이상, 표 포함)",
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


def ensure_unique_slug(slug: str, existing_slugs: set) -> str:
    if slug not in existing_slugs:
        return slug
    suffix = datetime.now().strftime("%m%d%H%M")
    unique = f"{slug}-{suffix}"
    print(f"  🔄 슬러그 중복 → 변경: {slug} → {unique}")
    return unique


def get_used_images() -> set:
    """기존 포스트에서 사용된 이미지 URL 수집."""
    used = set()
    if not os.path.exists(POSTS_DIR):
        return used
    for f in os.listdir(POSTS_DIR):
        if f.endswith('.json'):
            try:
                with open(os.path.join(POSTS_DIR, f), encoding='utf-8') as fp:
                    data = json.load(fp)
                    if data.get('image'):
                        used.add(data['image'])
            except Exception:
                pass
    return used


def fetch_pexels_image(queries: list, used_images: set = None) -> str:
    fallback = "https://images.pexels.com/photos/1871508/pexels-photo-1871508.jpg"
    if used_images is None:
        used_images = set()
    for query in queries:
        if not query:
            continue
        try:
            res = requests.get(
                "https://api.pexels.com/v1/search",
                headers={"Authorization": PEXELS_API_KEY},
                params={"query": query, "per_page": 15, "orientation": "landscape"},
                timeout=10,
            )
            res.raise_for_status()
            photos = res.json().get("photos", [])
            available = [p for p in photos if p["src"]["large2x"] not in used_images]
            if available:
                chosen = random.choice(available[:10])["src"]["large2x"]
                print(f"  ✅ 이미지 확보: '{query}'")
                return chosen
            elif photos:
                print(f"  ⚠️ 중복 없는 이미지 없음 → 기존 중 랜덤 사용")
                return random.choice(photos[:5])["src"]["large2x"]
        except Exception as e:
            print(f"  ⚠️ 이미지 오류 ({query}): {e}")
        time.sleep(0.3)
    print("  ⚠️ fallback 이미지 사용")
    return fallback


def insert_inline_image(content: str, image_url: str, alt_text: str) -> str:
    """본문 중간(세 번째 H2 섹션 시작 직전)에 이미지 1장을 삽입해
    글이 텍스트로만 빽빽하지 않도록 시각적 호흡을 추가한다."""
    if not image_url:
        return content
    headers = [m.start() for m in re.finditer(r"^## ", content, re.MULTILINE)]
    if len(headers) >= 3:
        pos = headers[2]
        img_md = f"![{alt_text}]({image_url})\n\n"
        return content[:pos] + img_md + content[pos:]
    return content


def save_post(slug, content_data, image_url, category, date, inline_image_url=None, inline_image_alt=None):
    # 본문 중간 이미지 삽입 (있는 경우)
    content = content_data["content"]
    if inline_image_url:
        content = insert_inline_image(content, inline_image_url, inline_image_alt or content_data["title"])

    # 내부 링크 자동 삽입 (Topic Cluster 강화)
    internal_link = CATEGORY_TO_PAGE.get(category)
    if internal_link:
        link_md = f"\n\n## 함께 보면 좋은 글\n\n해당 주제에 대한 더 자세한 정보는 **[{internal_link['anchor']}](https://wooriwin.com/{internal_link['slug']})** 페이지에서 확인하실 수 있습니다.\n"
        content = content + link_md

    content_with_eeat = content + RESPONSIBLE_GAMBLING_TEXT

    # 카테고리별 작성자 랜덤 배정
    author = get_author_for_category(category)
    print(f"  ✍️  작성자 배정: {author['name']} ({author['role']})")

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
        "author": author,
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

    # 기존 포스트 분석
    existing_posts = get_existing_posts()
    existing_titles = [p["title"] for p in existing_posts]
    existing_slugs = get_existing_slugs()
    
    print(f"\n📊 기존 포스트: {len(existing_posts)}개")

    # 카테고리별 포스트 수 카운트 → 적게 작성된 카테고리 우선
    category_counts = {cat: 0 for cat in CATEGORIES}
    for p in existing_posts:
        if p["category"] in category_counts:
            category_counts[p["category"]] += 1
    
    # 가장 적게 작성된 카테고리 순 정렬
    sorted_cats = sorted(category_counts.items(), key=lambda x: x[1])
    selected_categories = [c[0] for c in sorted_cats[:POSTS_PER_RUN]]
    
    print(f"📌 오늘 작성 카테고리: {selected_categories}\n")

    KST = timezone(timedelta(hours=9))
    today = datetime.now(KST)
    used_images = get_used_images()
    print(f"🖼️  기존 사용 이미지: {len(used_images)}개 (중복 방지)")
    success = 0

    for i, category in enumerate(selected_categories):
        date = today.strftime("%Y-%m-%d")
        cat_data = CATEGORIES[category]
        keyword = random.choice(cat_data["keywords"])
        pexels_queries = cat_data["pexels_queries"]
        slug_prefix = cat_data.get("slug_prefix", "casino")
        slug_suffixes = cat_data.get("slug_suffixes", ["guide", "tips"])

        print(f"\n📌 [{i+1}/{POSTS_PER_RUN}] 카테고리: {category}")
        print(f"   핵심 키워드: {keyword}")

        # Step 1 — 중복 회피 제목 생성
        print("  🔍 제목 생성 중 (중복 단어 3개 검사 포함)...")
        title = generate_unique_title(client, category, keyword, existing_titles)
        time.sleep(1)

        # Step 2 — 도입부 유형
        intro_type = random.choice(INTRO_TYPES)
        print(f"  📖 도입부 유형: {intro_type}")

        # Step 3 — 본문 생성
        print("  🤖 Gemini 본문 생성 중...")
        content_data = generate_post_content(
            client, title, category, keyword,
            pexels_queries, existing_slugs, intro_type,
            slug_prefix, slug_suffixes
        )
        if not content_data:
            continue

        raw_slug = content_data.get("slug", "")
        if not raw_slug:
            print("  ⏭️ 슬러그 없음 → 스킵")
            continue
        slug = ensure_unique_slug(raw_slug, existing_slugs)

        # Step 4 — 이미지 검색 (대표 이미지 + 본문 삽입용 이미지)
        gemini_query = content_data.get("pexels_query", "")
        image_queries = ([gemini_query] if gemini_query else []) + pexels_queries
        print("  📸 Pexels 대표 이미지 검색 중...")
        image_url = fetch_pexels_image(image_queries, used_images)
        used_images.add(image_url)  # 이번 루프에서 사용한 이미지도 중복 방지

        print("  📸 Pexels 본문 삽입 이미지 검색 중...")
        # 대표 이미지와 다른 분위기를 위해 검색어 순서를 섞어서 재검색
        inline_queries = pexels_queries[::-1] + ([gemini_query] if gemini_query else [])
        inline_image_url = fetch_pexels_image(inline_queries, used_images)
        used_images.add(inline_image_url)
        inline_image_alt = f"{content_data.get('imageAlt', title)} - 본문 참고 이미지"

        # Step 5 — 저장
        content_data["slug"] = slug
        save_post(
            slug, content_data, image_url, category, date,
            inline_image_url=inline_image_url, inline_image_alt=inline_image_alt,
        )

        # 다음 루프를 위해 즉시 업데이트
        existing_titles.append(title)
        existing_slugs.add(slug)
        success += 1
        time.sleep(2)

    print("\n" + "=" * 55)
    print(f"  완료: {success}개 포스트 생성")
    print(f"  전체 포스트: {len(existing_posts) + success}개")
    print("=" * 55)


if __name__ == "__main__":
    main()
