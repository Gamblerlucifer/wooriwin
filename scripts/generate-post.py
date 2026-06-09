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
POSTS_DIR        = os.path.join(BASE_DIR, "data", "posts")
USED_TOPICS_FILE = os.path.join(BASE_DIR, "data", "used-topics.json")
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

# ── 앵글 — 독자 관점 / 수준 (5개 고정) ─────────
ANGLES = {
    "입문":   "처음 접하는 독자가 핵심 개념을 이해하고 시작할 수 있도록 안내하는 관점",
    "실전":   "기본을 아는 독자가 실제 플레이에 바로 적용할 수 있는 실용적 관점",
    "분석":   "확률·RTP·통계 데이터를 중심으로 논리적으로 접근하는 관점",
    "비교":   "다른 게임·변형·옵션과 비교하여 선택 기준을 제시하는 관점",
    "심화":   "경험 있는 플레이어를 위한 고급 전략과 심층 분석 관점",
}

# ── 콘텐츠 모델 — 문서 목적 / 전개 방식 (10개) ──
CONTENT_MODELS = {
    "교육형":     {
        "desc": "개념과 용어를 단계별로 설명하고 마지막에 정리",
        "structure": "용어 정의 → 핵심 개념 설명 → 작동 방식 → 정리 요약",
    },
    "분석형":     {
        "desc": "수치·통계·데이터를 중심으로 제시하고 결론 도출",
        "structure": "데이터 제시 → 수치 비교 → 패턴 분석 → 시사점",
    },
    "비교형":     {
        "desc": "두 가지 이상을 비교하여 장단점과 추천 상황 제시",
        "structure": "비교 대상 소개 → 기준별 비교표 → 장단점 → 상황별 추천",
    },
    "실수방지형": {
        "desc": "흔히 저지르는 실수 목록과 그 이유, 예방법 중심",
        "structure": "흔한 실수 나열 → 각 실수의 원인 → 예방·대처법 → 요약",
    },
    "체크리스트형": {
        "desc": "독자가 직접 확인할 수 있는 단계별 항목 중심",
        "structure": "목적 설명 → 단계별 체크 항목 → 각 항목 해설 → 완료 기준",
    },
    "사례연구형": {
        "desc": "구체적인 시나리오 2~3개를 제시하고 공통점·교훈 도출",
        "structure": "사례 1 → 사례 2 → (사례 3) → 공통점 분석 → 교훈",
    },
    "가이드형":   {
        "desc": "처음부터 끝까지 순서대로 따라할 수 있는 절차 안내",
        "structure": "준비 사항 → 1단계 → 2단계 → 3단계 → 마무리 팁",
    },
    "트렌드형":   {
        "desc": "최근 변화와 흐름을 짚고 플레이어에게 갖는 의미 분석",
        "structure": "현재 상황 → 변화 요인 → 주요 트렌드 → 플레이어 영향",
    },
    "Q&A형":     {
        "desc": "독자가 자주 묻는 질문과 답변 형식으로 전개",
        "structure": "배경 설명 → Q1+A1 → Q2+A2 → Q3+A3 → Q4+A4 → 총정리",
    },
    "의사결정형": {
        "desc": "상황별 추천·비추천 판단 기준을 제시하여 선택을 돕는 구조",
        "structure": "판단 기준 제시 → 상황 A (추천) → 상황 B (비추천) → 결론",
    },
}

# ── 문체 ──────────────────────────────────────────
TONES = [
    "분석적 — 데이터와 수치 중심, 건조하고 객관적인 서술체",
    "친근한 — 쉬운 언어, 독자를 '~하세요'로 직접 호칭, 공감형 표현 활용",
    "저널리즘형 — 사실 중심, 중립적, 출처 명시를 자연스럽게 본문에 녹임",
    "교과서형 — 체계적 설명, 소제목 명확, 정의 먼저 제시 후 예시 보강",
]

# ── 도입부 패턴 ───────────────────────────────────
INTRO_TYPES = [
    "독자가 공감할 만한 상황이나 질문으로 시작",
    "핵심 통계나 수치 데이터를 제시하며 시작",
    "구체적인 시나리오나 사례로 시작",
    "결론을 먼저 제시하고 이유를 풀어가는 방식으로 시작",
    "흔한 오해나 잘못된 통념을 짚으며 시작",
    "이 글이 독자에게 어떤 도움이 되는지 직접 밝히며 시작",
]

# ── 마무리 패턴 ───────────────────────────────────
ENDING_TYPES = [
    "핵심 내용 3줄 요약으로 마무리",
    "독자가 다음에 취할 수 있는 행동을 자연스럽게 안내하며 마무리",
    "글에서 다룬 내용의 미래 전망이나 변화 가능성으로 마무리",
    "독자 스스로 판단할 수 있도록 열린 질문을 던지며 마무리",
    "핵심 체크포인트 목록으로 마무리",
]

# ── 글 길이 옵션 ──────────────────────────────────
LENGTH_OPTIONS = [
    {"label": "단문",  "min": 1500},
    {"label": "중문",  "min": 2000},
    {"label": "장문",  "min": 2500},
]

# ─────────────────────────────────────────────────
# 카테고리 + 핵심 키워드 (50개 하드코딩 주제 대신 동적 생성)
# ─────────────────────────────────────────────────
CATEGORIES = {
    "에볼루션 가이드": {
        "keywords": [
            "가입 방법", "인터페이스", "독점 기술", "역사와 성장", "플랫폼 구조",
            "게임 종류 총정리", "라이브 딜러 시스템", "스튜디오 위치", "스트리밍 기술",
            "베팅 인터페이스", "멀티 게임 기능", "VIP 서비스", "모바일 지원",
            "신규 유저 가이드", "에볼루션 경쟁사 비교",
        ],
        "pexels_queries": ["live casino studio", "casino platform interface", "online casino environment"],
        "slug_prefix": "live-casino",
        "slug_suffixes": ["guide", "tips", "review", "explained", "overview", "complete", "beginners", "advanced"],
    },
    "바카라 가이드": {
        "keywords": [
            "기본 규칙", "라이트닝 바카라", "스피드 바카라", "스퀴즈 바카라", "로드맵 시스템",
            "플레이어 뱅커 차이", "커미션 구조", "페어 베팅", "사이드 베팅 종류",
            "바카라 통계", "연승 패턴", "테이블 선택법", "고액 베팅 전략",
            "초보자 실수", "실전 플레이 가이드",
        ],
        "pexels_queries": ["baccarat casino table", "baccarat cards dealer", "live baccarat"],
        "slug_prefix": "baccarat",
        "slug_suffixes": ["strategy", "rules", "tips", "guide", "winning", "odds", "how-to", "explained"],
    },
    "블랙잭 가이드": {
        "keywords": [
            "기본 전략", "인피니트 블랙잭", "라이트닝 블랙잭", "사이드 베팅", "파워 블랙잭",
            "히트와 스탠드", "더블다운", "스플릿 전략", "보험 베팅", "카드 카운팅 개념",
            "블랙잭 확률", "딜러 규칙", "게임 변형 비교", "초보자 공략", "실전 예시",
        ],
        "pexels_queries": ["blackjack casino table", "blackjack dealer", "live blackjack"],
        "slug_prefix": "blackjack",
        "slug_suffixes": ["strategy", "rules", "tips", "guide", "basic-strategy", "odds", "how-to", "variants"],
    },
    "게임쇼 분석": {
        "keywords": [
            "크레이지타임", "모노폴리 라이브", "드림캐처", "메가볼", "게임쇼 비교",
            "보너스 라운드", "배당 구조", "RTP 비교", "인기 게임 순위", "신규 게임쇼",
            "확률 분석", "진행 방식", "베팅 옵션", "초보자 추천", "실시간 인기 트렌드",
        ],
        "pexels_queries": ["casino game show wheel", "live game show casino", "casino entertainment"],
        "slug_prefix": "game-show",
        "slug_suffixes": ["review", "guide", "analysis", "tips", "explained", "how-to-play", "odds", "strategy"],
    },
    "룰렛 & 포커": {
        "keywords": [
            "유럽식 룰렛", "라이트닝 룰렛", "임머시브 룰렛", "카지노 홀덤", "3 카드 포커",
            "아메리칸 룰렛", "프렌치 룰렛", "룰렛 베팅 종류", "포커 족보",
            "텍사스 홀덤", "캐리비안 스터드", "사이드 베팅", "확률 계산", "실전 전략", "게임 비교",
        ],
        "pexels_queries": ["roulette wheel casino", "live roulette dealer", "casino poker table"],
        "slug_prefix": "roulette",
        "slug_suffixes": ["strategy", "guide", "tips", "odds", "how-to", "variants", "explained", "winning"],
    },
    "최신 트렌드": {
        "keywords": [
            "2026 신규 게임", "암호화폐 결제", "AI 기술", "글로벌 스튜디오", "VR 카지노",
            "AR 기술", "실시간 스트리밍", "신규 공급업체", "멀티플레이 기능", "메타버스 카지노",
            "모바일 우선 전략", "AI 딜러", "차세대 인터페이스", "블록체인 보안", "시장 전망",
        ],
        "pexels_queries": ["casino innovation 2026", "casino technology", "live casino studio"],
        "slug_prefix": "casino-trends",
        "slug_suffixes": ["2026", "update", "new", "latest", "future", "review", "guide", "overview"],
    },
    "자금 관리": {
        "keywords": [
            "세션 예산", "입출금 시스템", "손실 한도", "베팅 단위", "세션 관리",
            "자금 분배", "리스크 관리", "승리 목표 설정", "손절 전략", "장기 운영",
            "예산 계획", "베팅 기록", "수익 관리", "감정 통제", "실전 사례",
        ],
        "pexels_queries": ["casino budget management", "money management casino", "casino bankroll"],
        "slug_prefix": "bankroll",
        "slug_suffixes": ["management", "strategy", "guide", "tips", "budgeting", "limits", "control", "plan"],
    },
    "보안 및 라이선스": {
        "keywords": [
            "MGA UKGC 라이선스", "암호화 보안", "RNG 검증", "플랫폼 선택", "고객센터 활용",
            "SSL 인증", "개인정보 보호", "공정성 검증", "규제 기관", "사기 사이트 구별",
            "보안 체크리스트", "KYC 인증", "출금 안전성", "플랫폼 신뢰도", "라이선스 확인법",
        ],
        "pexels_queries": ["casino license security", "online security casino", "casino safety"],
        "slug_prefix": "casino-safety",
        "slug_suffixes": ["license", "security", "guide", "tips", "verified", "trusted", "how-to", "checklist"],
    },
    "모바일 최적화": {
        "keywords": [
            "앱 vs 브라우저", "스트리밍 최적화", "iOS vs 안드로이드", "네트워크 설정", "태블릿 활용",
            "배터리 최적화", "화질 설정", "LTE vs WiFi", "모바일 UX", "세로 모드 활용",
            "앱 설치 가이드", "데이터 절약", "터치 인터페이스", "기기 호환성", "성능 향상",
        ],
        "pexels_queries": ["mobile casino smartphone", "smartphone gaming casino", "tablet casino"],
        "slug_prefix": "mobile-casino",
        "slug_suffixes": ["guide", "tips", "setup", "optimization", "ios", "android", "streaming", "settings"],
    },
    "책임감 있는 게임": {
        "keywords": [
            "기본 원칙", "자기 제한", "도박 문제 예방", "딜러 에티켓", "초보자 FAQ",
            "시간 관리", "예산 설정", "감정 조절", "자가 진단", "휴식 전략",
            "가족 보호", "자기 차단 기능", "건전한 이용법", "위험 신호", "도움받는 방법",
        ],
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
        "bio": "글로벌 금융 보안 전문가 출신으로, 철저한 라이선스 검증과 자본력 분석을 통해 사용자가 안심하고 즐길 수 있는 생태계를 구축하는 데 앞장서고 있습니다.",
        "credentials": ["前 금융보안 컨설턴트", "MGA 라이선스 검증 전문", "온라인 플랫폼 자본력 분석"],
        "image": "/about/01.jpg",
        "url": "/about",
        "experience": "15년+",
        "specialty": ["보안 및 라이선스", "최신 트렌드"],
    },
    "김도현": {
        "role": "라이브카지노 전문가",
        "bio": "해외 메이저 카지노 현장 경력을 바탕으로 딜러의 숙련도, 카드 슈의 투명성, 0.1초의 레이턴시까지 놓치지 않는 날카로운 시각으로 라이브 게임 환경의 모든 변수를 수치화하여 전달합니다.",
        "credentials": ["前 해외 카지노 플로어 스태프", "Evolution Gaming 딜러 트레이닝 이수", "라이브 스트리밍 지연 분석 전문"],
        "image": "/about/02.jpg",
        "url": "/about",
        "experience": "10년+",
        "specialty": ["바카라 가이드", "블랙잭 가이드", "룰렛 & 포커", "게임쇼 분석"],
    },
    "이수연": {
        "role": "콘텐츠 전문가",
        "bio": "복잡하게 얽힌 카지노 룰과 보너스 약관을 누구나 이해할 수 있는 직관적인 콘텐츠로 재구성합니다. UX 중심의 가이드 제작을 총괄하며 초보자와 숙련자 모두를 위한 콘텐츠 로드맵을 설계합니다.",
        "credentials": ["UX 라이팅 전문가", "카지노 규칙·약관 현지화 경력", "한국어 SEO 콘텐츠 최적화"],
        "image": "/about/03.jpg",
        "url": "/about",
        "experience": "8년+",
        "specialty": ["에볼루션 가이드", "모바일 최적화"],
    },
    "최민석": {
        "role": "시니어 에디터",
        "bio": "수천 개의 게임 데이터를 대조하여 실제 RTP와 입출금 속도의 상관관계를 파헤치는 저널리스트입니다. 타협 없는 팩트 체크로 플랫폼의 장단점을 가감 없이 기록합니다.",
        "credentials": ["前 게임 전문 IT 저널리스트", "데이터 저널리즘 기반 팩트체크", "RTP 데이터베이스 구축·관리"],
        "image": "/about/04.jpg",
        "url": "/about",
        "experience": "12년+",
        "specialty": ["에볼루션 가이드", "최신 트렌드", "자금 관리"],
    },
    "정혜진": {
        "role": "책임도박 전문가",
        "bio": "상담 심리학 석사로서 게임의 즐거움이 삶의 침해로 이어지지 않도록 방어선을 구축합니다. 도박 중독 예방 가이드를 설계하고 모든 플랫폼 리뷰에 안전 베팅 지수를 도입하여 실질적인 솔루션을 제공합니다.",
        "credentials": ["상담 심리학 석사", "도박 중독 예방 가이드라인 집필", "책임도박 캠페인 자문 경력"],
        "image": "/about/05.jpg",
        "url": "/about",
        "experience": "11년+",
        "specialty": ["책임감 있는 게임", "자금 관리"],
    },
    "한재원": {
        "role": "커뮤니티 매니저",
        "bio": "유저들의 생생한 목소리를 수집하여 리뷰의 완성도를 높이는 소통의 가교입니다. 대형 게임 커뮤니티 운영 노하우를 살려 허위 리뷰를 걸러내고 플레이어의 집단지성이 핵심 기준이 되도록 관리합니다.",
        "credentials": ["대형 온라인 카지노 커뮤니티 운영", "플레이어 분쟁 조정 전문", "UGC 콘텐츠 품질 검수"],
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
# 사용된 주제 추적 — (카테고리 + 키워드) 중복 방지
# ─────────────────────────────────────────────────

def load_used_topics() -> dict:
    """data/used-topics.json에서 이미 사용한 (keyword|angle|content_model) 기록 로드.
    구조: {"카테고리": ["keyword|angle|content_model", ...]}
    """
    if os.path.exists(USED_TOPICS_FILE):
        try:
            with open(USED_TOPICS_FILE, "r", encoding="utf-8") as f:
                data = json.load(f)
                # 구 형식 자동 마이그레이션
                for cat in list(data.keys()):
                    entries = data[cat]
                    if not entries:
                        continue
                    # {"keyword":..., "angle":...} 형식이면 파이프 문자열로 변환
                    if isinstance(entries[0], dict):
                        data[cat] = [
                            f"{e.get('keyword','')}"
                            f"|{e.get('angle','입문')}"
                            f"|{e.get('content_model','교육형')}"
                            for e in entries
                        ]
                return data
        except Exception:
            pass
    return {cat: [] for cat in CATEGORIES}


def save_used_topics(used: dict) -> None:
    """사용된 주제 기록을 파일에 저장."""
    os.makedirs(os.path.dirname(USED_TOPICS_FILE), exist_ok=True)
    with open(USED_TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(used, f, ensure_ascii=False, indent=2)


def get_next_topic(category: str, used_topics: dict) -> tuple:
    """카테고리에서 아직 사용하지 않은 (keyword, angle, content_model) 트리플 반환.
    15 keywords × 5 angles × 10 content_models = 750 combinations/category (총 7,500).
    모두 소진되면 초기화 후 재순환."""
    all_kws     = CATEGORIES[category]["keywords"]
    all_angles  = list(ANGLES.keys())
    all_models  = list(CONTENT_MODELS.keys())
    used_set    = set(used_topics.get(category, []))
    available   = [
        (kw, angle, model)
        for kw    in all_kws
        for angle in all_angles
        for model in all_models
        if f"{kw}|{angle}|{model}" not in used_set
    ]
    if not available:
        print(f"  ♻️  [{category}] 모든 조합 소진 → 초기화하여 재순환")
        used_topics[category] = []
        available = [(kw, a, m) for kw in all_kws for a in all_angles for m in all_models]
    kw, angle, model = random.choice(available)
    used_topics.setdefault(category, []).append(f"{kw}|{angle}|{model}")
    return kw, angle, model


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

def generate_unique_title(
    client: genai.Client,
    category: str,
    keyword: str,
    angle: str,
    content_model: str,
    existing_titles: list,
    max_attempts: int = 3,
) -> str:
    """기존 제목과 중복되지 않는 새 제목 생성."""
    existing_sample = existing_titles[-60:] if existing_titles else []
    existing_list   = "\n".join(f"- {t}" for t in existing_sample) if existing_sample else "없음"
    title_kw_pool   = CATEGORY_TITLE_KEYWORDS.get(category, ["에볼루션카지노"])
    title_kw        = random.choice(title_kw_pool)

    angle_desc = ANGLES[angle]
    model_desc = CONTENT_MODELS[content_model]["desc"]

    for attempt in range(max_attempts):
        prompt = f"""
다음 조건으로 한국인 독자에게 매력적인 블로그 제목 3개를 생성하세요.

카테고리: {category}
핵심 키워드: {keyword}
독자 관점(앵글): {angle} — {angle_desc}
문서 목적(콘텐츠 모델): {content_model} — {model_desc}
제목에 반드시 포함할 브랜드/게임 키워드: {title_kw}

조건:
- 위 브랜드/게임 키워드를 제목 어디에나 자연스럽게 포함
- "에볼루션카지노"를 항상 제목 맨 앞에 쓰는 패턴 금지
- 앵글({angle})과 콘텐츠 모델({content_model})이 암시하는 내용을 제목이 반영할 것
- 과장형·선정적 표현 금지, 수익·승률 보장 표현 절대 금지
- 각 제목은 서로 다른 각도로 작성
- 제목에 콜론(:) 사용 금지
- 25~45자 사이

⚠️ 절대 금지 — 아래 기존 제목들과 핵심 단어 3개 이상 겹치는 제목 금지:
{existing_list}

출력 형식: JSON 배열만 출력 (마크다운 코드블록 없이)
예시: ["제목1", "제목2", "제목3"]
"""
        result = safe_generate_content(client, prompt, use_search=False, retries=1)
        if not isinstance(result, list) or not result:
            print(f"  ⚠️ 제목 생성 실패 ({attempt + 1}/{max_attempts})")
            continue
        for title in result:
            if not is_duplicate_title(title, existing_titles):
                print(f"  🏆 선택된 제목: '{title}'")
                return title
        print(f"  🔄 모든 제목이 중복 — 재시도 ({attempt + 1}/{max_attempts})")
        time.sleep(1)

    fallback = f"에볼루션카지노 {keyword} 완벽 가이드"
    print(f"  ⚠️ Fallback 제목 사용: '{fallback}'")
    return fallback


# ─────────────────────────────────────────────────
# 본문 생성
# ─────────────────────────────────────────────────

def generate_post_content(
    client: genai.Client,
    title: str,
    category: str,
    keyword: str,
    angle: str,
    content_model: str,
    tone: str,
    intro_type: str,
    ending_type: str,
    length_option: dict,
    fixed_queries: list,
    existing_slugs: set,
    slug_prefix: str = "",
    slug_suffixes: list = None,
):
    slugs_sample  = list(existing_slugs)[-50:]
    slugs_list    = "\n".join(f"- {s}" for s in slugs_sample) if slugs_sample else "없음"
    if not slug_suffixes:
        slug_suffixes = ["guide", "tips", "review", "strategy"]
    random_suffix = random.choice(slug_suffixes)

    model_info    = CONTENT_MODELS[content_model]
    length_min    = length_option["min"]
    length_label  = length_option["label"]

    prompt = f"""
━━━ 콘텐츠 생성 명세 ━━━

글 제목    : {title}
카테고리   : {category}
핵심 키워드: {keyword}
독자 앵글  : {angle} — {ANGLES[angle]}
콘텐츠 모델: {content_model} — {model_info['desc']}
  └ 권장 전개 구조: {model_info['structure']}
문체       : {tone}
도입부     : {intro_type}
마무리     : {ending_type}
글 길이    : {length_label} ({length_min}자 이상)

━━━ 작성 지침 ━━━

[구조]
- 위 콘텐츠 모델의 전개 구조를 충실히 따를 것
- H2 헤더(##) 3~7개 (콘텐츠 모델에 맞게 자유롭게)
- H3 소제목(###)은 필요 시 사용 (필수 아님)
- 글 길이는 반드시 {length_min}자 이상으로 작성

[다양성 — 아래 요소는 콘텐츠 모델에 따라 유동적으로 결정]
- 표(|컬럼|컬럼|): 분석형·비교형은 2개 이상, 나머지는 필요 시만 포함
- FAQ: Q&A형은 6~8개, 나머지는 0~4개 자유 배치 또는 생략
- 체크리스트, 인용 박스, 번호 목록 등은 모델 구조에 어울릴 때만 사용

[YMYL 필수]
- 특정 베팅 권장·유도 표현 금지
- '무조건', '절대', '반드시' 등 단정적 행동 지시 금지
- 손익 보장·당첨 기대 표현 금지
- 본문에 'YMYL', 'E-E-A-T', 'EEAT', 'SEO' 노출 금지
- RTP 수치 언급 시 '이론적 기댓값이며 실제 결과와 다를 수 있습니다' 병기
- 'Evolution Gaming 공식 게임 수학 문서 기준' 출처 1회 이상 포함
- 손실 위험 안내 문구 1회 이상 포함
- eCOGRA 등 공인 감사기관 언급

[슬러그]
- 기존 슬러그 목록과 겹치지 않게 생성
- 영문 소문자 + 숫자 + 하이픈, 50자 이내
- prefix로 시작: {slug_prefix}
- 예시: {slug_prefix}-keyword-{random_suffix}
- "evolution-casino", "interface", "ux" 사용 금지

기존 슬러그:
{slugs_list}

━━━ 출력 형식 (순수 JSON만, 코드블록 없이) ━━━
{{
  "slug": "unique-slug",
  "title": "{title}",
  "description": "150자 이내 포스트 설명",
  "keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"],
  "imageAlt": "이미지 설명 50자 이내",
  "pexels_query": "english-image-search-query",
  "content": "본문 마크다운 ({length_min}자 이상)",
  "faq": [
    {{"q": "질문", "a": "답변"}}
  ]
}}
"""
    return safe_generate_content(client, prompt, use_search=False, retries=1)


def ensure_unique_slug(slug: str, existing_slugs: set) -> str:
    if slug not in existing_slugs:
        return slug
    suffix = random.randint(1000, 9999)
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

    # 사용된 주제 기록 로드 (카테고리+키워드 중복 방지)
    used_topics = load_used_topics()
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
        cat_data      = CATEGORIES[category]
        pexels_queries = cat_data["pexels_queries"]
        slug_prefix   = cat_data.get("slug_prefix", "casino")
        slug_suffixes = cat_data.get("slug_suffixes", ["guide", "tips"])

        # ── 파이프라인 변수 결정 ──────────────────────
        keyword, angle, content_model = get_next_topic(category, used_topics)
        tone         = random.choice(TONES)
        intro_type   = random.choice(INTRO_TYPES)
        ending_type  = random.choice(ENDING_TYPES)
        length_option = random.choice(LENGTH_OPTIONS)

        print(f"\n📌 [{i+1}/{POSTS_PER_RUN}] 카테고리: {category}")
        print(f"   키워드: {keyword} | 앵글: {angle} | 모델: {content_model}")
        print(f"   문체: {tone[:10]}... | 길이: {length_option['label']} ({length_option['min']}자 이상)")

        # Step 1 — 중복 회피 제목 생성
        print("  🔍 제목 생성 중...")
        title = generate_unique_title(
            client, category, keyword, angle, content_model, existing_titles
        )
        time.sleep(1)

        # Step 2 — 도입부·마무리 확정 로그
        print(f"  📖 도입부: {intro_type[:20]}... | 마무리: {ending_type[:20]}...")

        # Step 3 — 본문 생성
        print("  🤖 Gemini 본문 생성 중...")
        content_data = generate_post_content(
            client, title, category, keyword,
            angle, content_model, tone, intro_type, ending_type, length_option,
            pexels_queries, existing_slugs, slug_prefix, slug_suffixes,
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

        # 사용된 주제 기록 즉시 저장 (다음 실행 시 재탕 방지)
        save_used_topics(used_topics)
        print(f"  💾 used-topics.json 업데이트: [{category}] {keyword}|{angle}|{content_model}")

        time.sleep(2)

    print("\n" + "=" * 55)
    print(f"  완료: {success}개 포스트 생성")
    print(f"  전체 포스트: {len(existing_posts) + success}개")
    print("=" * 55)


if __name__ == "__main__":
    main()
