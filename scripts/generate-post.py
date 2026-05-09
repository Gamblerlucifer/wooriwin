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
                    "전략", "가이드", "분석", "비교", "방법", "설정", "인터페이스", "UX", "환경", "리스크",
]

# ── [4번] 도입부 유형 랜덤화 리스트 ─────────────
INTRO_TYPES = [
                "사용자들이 자주 혼동하는 인터페이스 설정 문제로 시작",
                "플레이 환경 최적화 관점의 설명으로 시작",
                "UX 분석 기반의 기능 설명으로 시작",
                "초보자들이 놓치기 쉬운 설정 요소 소개로 시작",
                "리스크 관리 관점의 플레이 환경 설명으로 시작",
                "실제 사용자 FAQ 기반 설명으로 시작",
]
TITLE_FORMATS = [
    "N가지 방법",
    "N가지 팁",
    "N가지 체크리스트",
    "N가지 비교 포인트",
    "N가지 설정 요소",
    "N가지 핵심 기능",
    "완벽 가이드",
    "A vs B 비교 분석",
    "초보자를 위한 입문",
    "란 무엇인가",
]
# ── 21개 확정 주제 (주제 + 카테고리 + Pexels 쿼리 세트) ──
TOPICS = [
    # ── 카테고리 1: 에볼루션 가이드 ──
    {
        "id": 1,
        "topic": "에볼루션카지노란 무엇인가: 플랫폼 구조와 게임 환경 완벽 이해",
        "category": "에볼루션 가이드",
        "pexels_queries": ["live casino studio overview", "casino platform interface", "online casino environment"],
    },
    {
        "id": 2,
        "topic": "에볼루션카지노 처음 시작하는 법: 가입부터 첫 게임까지 단계별 가이드",
        "category": "에볼루션 가이드",
        "pexels_queries": ["online casino beginner guide", "casino registration setup", "casino first game"],
    },
    {
        "id": 3,
        "topic": "에볼루션카지노 인터페이스(UI) 활용법: 멀티 게임 모드와 채팅 기능",
        "category": "에볼루션 가이드",
        "pexels_queries": ["casino user interface screen", "live casino interface multiple games", "casino chat interface"],
    },
    {
        "id": 4,
        "topic": "에볼루션카지노 독점 기술 분석: 듀얼 플레이와 다이렉트 런치 기능",
        "category": "에볼루션 가이드",
        "pexels_queries": ["casino technology innovation", "live streaming casino studio", "casino dual screen technology"],
    },
    {
        "id": 5,
        "topic": "에볼루션카지노 역사와 성장: 업계 1위가 된 배경과 기술력",
        "category": "에볼루션 가이드",
        "pexels_queries": ["casino history evolution timeline", "gambling company headquarters", "casino industry growth"],
    },

    # ── 카테고리 2: 바카라 가이드 ──
    {
        "id": 6,
        "topic": "에볼루션카지노 바카라 기본 규칙: 카드 계산법과 배팅 종류 완벽 정리",
        "category": "바카라 가이드",
        "pexels_queries": ["baccarat casino table cards", "baccarat rules card game", "live baccarat dealer"],
    },
    {
        "id": 7,
        "topic": "라이트닝 바카라 vs 일반 바카라: 게임 구조와 배당 방식 비교",
        "category": "바카라 가이드",
        "pexels_queries": ["baccarat cards lightning casino", "baccarat table comparison", "casino card game odds"],
    },
    {
        "id": 8,
        "topic": "골든 바카라 완벽 가이드: 골든 카드 시스템과 게임 특징 이해",
        "category": "바카라 가이드",
        "pexels_queries": ["golden baccarat casino cards", "gold playing cards casino", "baccarat golden strategy"],
    },
    {
        "id": 9,
        "topic": "코리안 스피드 바카라: 한국어 서비스 환경과 게임 특징 리뷰",
        "category": "바카라 가이드",
        "pexels_queries": ["korean casino dealer baccarat", "asian live casino dealer", "baccarat speed cards"],
    },
    {
        "id": 10,
        "topic": "바카라 로드맵 시스템 이해: 에볼루션 그림 표시 방식과 활용법",
        "category": "바카라 가이드",
        "pexels_queries": ["baccarat road map scoreboard", "baccarat pattern analysis", "casino baccarat statistics"],
    },

    # ── 카테고리 3: 블랙잭 가이드 ──
    {
        "id": 11,
        "topic": "에볼루션카지노 블랙잭 기본 규칙: 카드 합산과 딜러 규칙 완벽 정리",
        "category": "블랙잭 가이드",
        "pexels_queries": ["blackjack casino table cards", "blackjack dealer rules", "live blackjack casino"],
    },
    {
        "id": 12,
        "topic": "블랙잭 베이직 스트래티지 가이드: 상황별 최적 판단 기준 이해",
        "category": "블랙잭 가이드",
        "pexels_queries": ["blackjack basic strategy cards", "blackjack casino table dealer", "card strategy blackjack"],
    },
    {
        "id": 13,
        "topic": "에볼루션 인피니트 블랙잭: 다중 참여 방식과 게임 구조 분석",
        "category": "블랙잭 가이드",
        "pexels_queries": ["infinite blackjack casino multiple players", "live blackjack studio", "blackjack online interface"],
    },
    {
        "id": 14,
        "topic": "블랙잭 사이드 베팅 종류: Perfect Pairs와 21+3 옵션 이해",
        "category": "블랙잭 가이드",
        "pexels_queries": ["blackjack side bet casino", "blackjack pairs betting", "casino card side bet"],
    },
    {
        "id": 15,
        "topic": "에볼루션 파워 블랙잭: 더블 다운과 스플릿 기능 활용 가이드",
        "category": "블랙잭 가이드",
        "pexels_queries": ["blackjack double down split", "power blackjack casino", "blackjack advanced options"],
    },

    # ── 카테고리 4: 게임쇼 분석 ──
    {
        "id": 16,
        "topic": "에볼루션 크레이지타임 완벽 가이드: 게임 구조와 보너스 라운드 이해",
        "category": "게임쇼 분석",
        "pexels_queries": ["crazy time casino wheel colorful", "casino game show spin", "live game show casino"],
    },
    {
        "id": 17,
        "topic": "모노폴리 라이브 분석: 보드게임 연동 방식과 보너스 게임 구조",
        "category": "게임쇼 분석",
        "pexels_queries": ["monopoly live casino board", "casino board game show", "monopoly game show studio"],
    },
    {
        "id": 18,
        "topic": "에볼루션 드림캐처: 휠 게임 구조와 배당 방식 완벽 이해",
        "category": "게임쇼 분석",
        "pexels_queries": ["dream catcher casino wheel", "casino wheel spin colorful", "live casino wheel game"],
    },
    {
        "id": 19,
        "topic": "메가볼 완벽 가이드: 빙고 방식 게임 구조와 멀티플라이어 시스템",
        "category": "게임쇼 분석",
        "pexels_queries": ["mega ball casino bingo", "casino ball game show", "live casino lottery game"],
    },
    {
        "id": 20,
        "topic": "에볼루션 게임쇼 TOP 5 비교: 구조와 특징으로 보는 선택 가이드",
        "category": "게임쇼 분석",
        "pexels_queries": ["casino game show comparison", "live casino variety games", "casino entertainment show"],
    },

    # ── 카테고리 5: 룰렛 & 포커 ──
    {
        "id": 21,
        "topic": "에볼루션카지노 룰렛 기본 규칙: 유럽식과 미국식 차이 완벽 정리",
        "category": "룰렛 & 포커",
        "pexels_queries": ["roulette wheel casino table", "european roulette casino", "live roulette dealer"],
    },
    {
        "id": 22,
        "topic": "라이트닝 룰렛 완벽 가이드: 멀티플라이어 시스템과 게임 구조 이해",
        "category": "룰렛 & 포커",
        "pexels_queries": ["lightning roulette casino wheel", "roulette multiplier game", "casino roulette numbers"],
    },
    {
        "id": 23,
        "topic": "에볼루션 임머시브 룰렛: 멀티 카메라 환경과 슬로우 모션 기능 분석",
        "category": "룰렛 & 포커",
        "pexels_queries": ["immersive roulette slow motion", "casino roulette close up", "live roulette camera"],
    },
    {
        "id": 24,
        "topic": "에볼루션 카지노 홀덤 포커: 게임 규칙과 진행 방식 완벽 가이드",
        "category": "룰렛 & 포커",
        "pexels_queries": ["casino holdem poker table", "live poker casino dealer", "poker casino cards"],
    },
    {
        "id": 25,
        "topic": "에볼루션 3 카드 포커: 게임 구조와 배팅 옵션 이해",
        "category": "룰렛 & 포커",
        "pexels_queries": ["three card poker casino", "poker three cards dealer", "live poker casino table"],
    },

    # ── 카테고리 6: 최신 트렌드 ──
    {
        "id": 26,
        "topic": "2026년 에볼루션카지노 신규 게임 라인업: 최신 출시작 완벽 리뷰",
        "category": "최신 트렌드",
        "pexels_queries": ["new casino game launch 2026", "casino innovation new release", "live casino new game"],
    },
    {
        "id": 27,
        "topic": "에볼루션카지노 암호화폐 결제: 비트코인 입출금 환경과 보안 트렌드",
        "category": "최신 트렌드",
        "pexels_queries": ["bitcoin casino cryptocurrency payment", "crypto gambling blockchain", "digital currency casino"],
    },
    {
        "id": 28,
        "topic": "라이브 카지노 AI 기술 트렌드: 에볼루션의 기술 혁신 방향 분석",
        "category": "최신 트렌드",
        "pexels_queries": ["casino AI technology innovation", "live casino future technology", "casino digital innovation"],
    },
    {
        "id": 29,
        "topic": "글로벌 에볼루션 스튜디오 탐방: 라트비아부터 몰타까지 인프라 분석",
        "category": "최신 트렌드",
        "pexels_queries": ["casino studio latvia filming", "live casino studio interior", "casino broadcasting studio"],
    },
    {
        "id": 30,
        "topic": "에볼루션카지노 VR 라이브 카지노: 미래 게임 환경 전망과 현황",
        "category": "최신 트렌드",
        "pexels_queries": ["VR casino virtual reality", "future casino technology VR", "virtual casino environment"],
    },

    # ── 카테고리 7: 자금 관리 ──
    {
        "id": 31,
        "topic": "카지노 자금 관리 기초: 세션 예산 설정과 플레이 환경 최적화",
        "category": "자금 관리",
        "pexels_queries": ["casino budget management finance", "money management casino", "casino bankroll planning"],
    },
    {
        "id": 32,
        "topic": "에볼루션카지노 입출금 시스템: 안전한 자금 흐름 이해와 관리법",
        "category": "자금 관리",
        "pexels_queries": ["casino payment deposit withdraw", "online banking casino", "secure payment casino"],
    },
    {
        "id": 33,
        "topic": "손실 한도 설정 가이드: 에볼루션 플랫폼 내 자기 제한 기능 활용",
        "category": "자금 관리",
        "pexels_queries": ["casino loss limit setting", "responsible gambling limit", "casino self control budget"],
    },
    {
        "id": 34,
        "topic": "베팅 단위 설정법: 리스크 관리 관점에서 본 플레이 환경 구성",
        "category": "자금 관리",
        "pexels_queries": ["casino betting unit management", "casino chip betting strategy", "casino risk management"],
    },
    {
        "id": 35,
        "topic": "카지노 세션 관리: 플레이 시간과 예산을 효율적으로 구성하는 법",
        "category": "자금 관리",
        "pexels_queries": ["casino session time management", "casino playing time budget", "casino time limit setting"],
    },

    # ── 카테고리 8: 보안 및 라이선스 ──
    {
        "id": 36,
        "topic": "에볼루션카지노 라이선스 완벽 분석: MGA, UKGC 인증 의미와 중요성",
        "category": "보안 및 라이선스",
        "pexels_queries": ["casino license security certificate", "official gambling regulation", "casino security trust"],
    },
    {
        "id": 37,
        "topic": "라이브 카지노 보안 시스템: 암호화 기술과 개인정보 보호 환경",
        "category": "보안 및 라이선스",
        "pexels_queries": ["casino cybersecurity encryption", "online security protection", "casino data privacy"],
    },
    {
        "id": 38,
        "topic": "에볼루션카지노 공정성 검증: RNG 시스템과 외부 감사 기관 역할",
        "category": "보안 및 라이선스",
        "pexels_queries": ["casino fairness audit certificate", "random number generator casino", "casino third party audit"],
    },
    {
        "id": 39,
        "topic": "안전한 카지노 플랫폼 선택 기준: 라이선스와 보안 환경 확인법",
        "category": "보안 및 라이선스",
        "pexels_queries": ["casino safety checklist security", "online casino verification", "casino trust badge"],
    },
    {
        "id": 40,
        "topic": "에볼루션카지노 고객센터 활용법: 문의 채널과 분쟁 해결 프로세스",
        "category": "보안 및 라이선스",
        "pexels_queries": ["casino customer support service", "online casino help center", "casino dispute resolution"],
    },

    # ── 카테고리 9: 모바일 최적화 ──
    {
        "id": 41,
        "topic": "에볼루션카지노 모바일 환경 가이드: 앱과 브라우저 방식 비교",
        "category": "모바일 최적화",
        "pexels_queries": ["mobile casino smartphone app", "online casino mobile browser", "casino mobile interface"],
    },
    {
        "id": 42,
        "topic": "모바일 라이브 카지노 최적화: 끊김 없는 스트리밍 환경 구성법",
        "category": "모바일 최적화",
        "pexels_queries": ["mobile casino smartphone", "online casino mobile app", "smartphone gaming casino"],
    },
    {
        "id": 43,
        "topic": "iOS vs 안드로이드 카지노 환경: 플랫폼별 최적화 설정 가이드",
        "category": "모바일 최적화",
        "pexels_queries": ["ios android casino comparison", "mobile gaming platform casino", "smartphone casino setup"],
    },
    {
        "id": 44,
        "topic": "모바일 카지노 네트워크 설정: 와이파이와 5G 환경별 최적화 방법",
        "category": "모바일 최적화",
        "pexels_queries": ["mobile network wifi casino", "5G internet speed casino", "casino network connection"],
    },
    {
        "id": 45,
        "topic": "태블릿으로 즐기는 에볼루션카지노: 화면 크기 활용과 UI 최적화",
        "category": "모바일 최적화",
        "pexels_queries": ["tablet casino gaming interface", "ipad casino live game", "casino tablet screen"],
    },

    # ── 카테고리 10: 책임감 있는 게임 ──
    {
        "id": 46,
        "topic": "책임감 있는 게임이란: 건전한 카지노 이용 환경의 기본 원칙",
        "category": "책임감 있는 게임",
        "pexels_queries": ["responsible gambling awareness", "casino healthy gaming", "gambling prevention education"],
    },
    {
        "id": 47,
        "topic": "에볼루션카지노 자기 제한 기능: 입금 한도와 플레이 시간 설정법",
        "category": "책임감 있는 게임",
        "pexels_queries": ["casino self exclusion limit", "casino time limit setting", "responsible gaming tools"],
    },
    {
        "id": 48,
        "topic": "도박 문제 인식과 예방: 건강한 게임 습관 형성을 위한 가이드",
        "category": "책임감 있는 게임",
        "pexels_queries": ["gambling addiction prevention", "casino problem awareness", "healthy gaming habits"],
    },
    {
        "id": 49,
        "topic": "라이브 딜러 에티켓: 건전한 게임 커뮤니티를 위한 행동 가이드",
        "category": "책임감 있는 게임",
        "pexels_queries": ["live casino dealer etiquette", "casino community friendly", "casino respectful gaming"],
    },
    {
        "id": 50,
        "topic": "에볼루션카지노 FAQ: 처음 이용자가 가장 많이 묻는 질문 10가지",
        "category": "책임감 있는 게임",
        "pexels_queries": ["casino FAQ questions answers", "customer support casino help", "online casino guide beginner"],
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
SYSTEM_INSTRUCTION = """
당신은 라이브 카지노 UX 분석 및 플레이 환경 최적화 전문 콘텐츠 팀입니다.

사용자 경험 중심의 인터페이스 활용 가이드와
리스크 관리 관점의 정보를 제공합니다.

Google E-E-A-T 및 Helpful Content 기준을 준수합니다.

수치 보장, 승률 예측, 결과 보장, 과장형 표현,
검증 불가능한 전문가 경력 설정은 절대 사용하지 않습니다.

콘텐츠는 다음 관점을 중심으로 작성합니다:

UX 분석
플레이 환경
인터페이스 활용
환경 설정
사용자 경험
리스크 관리

사실 기반 정보와 사용자 편의 중심으로
중립적이고 설명형 문체를 유지합니다.
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

"에볼루션카지노" 키워드 반드시 포함
클릭하고 싶은 제목 작성
단, 정보형·가이드형 톤 유지
과장형·선정적 표현 금지
최신 UI/업데이트 맥락일 경우에만 연도 포함 가능
수치 보장·승률 예측·결과 보장 표현 절대 금지
각 제목은 서로 다른 앵글로 작성
(초보자용 / 플레이 환경 최적화형 /
인터페이스 가이드형 / 리스크 관리형 등)

제목 포맷 규칙:
3개 중 1~2개는 아래 포맷 풀에서 골라 적용하고 나머지는 자연스러운 가이드형으로 작성
포맷 풀: N가지 방법 / N가지 팁 / N가지 체크리스트 / N가지 비교 포인트 / N가지 설정 요소 / N가지 핵심 기능
N은 3·4·5·6·7·10 중 주제에 맞게 자유 선택
3개 제목 모두 같은 포맷 금지

금지 표현:

'10년 차 딜러'
'전직 딜러'
'현장 경험'
'승률 XX%'
'반드시'
'충격'
'99%'
'돈 버는'
'필승'
'고수만 아는'
'핵심 비밀'
'아무도 모르는'

출력 형식:
JSON 배열만 출력
예시: ["제목1", "제목2","제목3"]

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
1. 본문은 최소 1500자 이상 작성
2. H2 헤더(##)를 4~6개 포함
3. 사용자 경험 중심의 설명형 콘텐츠로 작성
4. UX 분석·플레이 환경·인터페이스 활용 관점 유지
5. 첫 문단 도입부 스타일: {intro_type}
6. 본문 중간에 마크다운 표(|컬럼|컬럼|) 최소 1개 포함
7. FAQ 5개 포함 (초보자 관점 질문 포함)
8. SEO 키워드는 자연스럽게 배치
9. pexels_query 필드에 적절한 영문 이미지 검색어 1개 생성
10. RTP·배당률·확률 관련 내용은 설명형 정보로만 제한
11. 수치 보장·승률 예측·결과 보장 표현 절대 금지
12. 공식 제공 정보 기반의 일반 설명 형태 유지

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

        print(f"\n📌 주제 [{topic_data['id']}/50]: {topic[:45]}...")
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
    print(f"  사용된 주제: {len(used_ids)}/50 | 남은 주제: {len(remaining)}")
    print("=" * 55)
    print("\n✨ git add . && git commit -m 'auto: add posts' && git push")


if __name__ == "__main__":
    main()