"""
wp-news-generate.py
───────────────────
wooriwin.net WordPress 뉴스 기사 자동 생성 + REST API 포스팅

사용법:
  python scripts/wp-news-generate.py
  python scripts/wp-news-generate.py --category macau-casino
  python scripts/wp-news-generate.py --count 5
"""

import os
import re
import sys
import json
import time
import base64
import random
import argparse
import requests
import cloudscraper
from datetime import datetime, timedelta, timezone
from dotenv import load_dotenv
from google import genai

sys.stdout.reconfigure(encoding='utf-8')

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))

# ── API / 설정 ─────────────────────────────────────
GEMINI_API_KEY  = os.environ.get("GEMINI_NET_API_KEY", "") or os.environ.get("GEMINI_API_KEY", "")
PEXELS_API_KEY  = os.environ.get("PEXELS_API_KEY", "")
WP_URL          = os.environ.get("WP_NET_URL", "https://wooriwin.net")
WP_USER         = os.environ.get("WP_NET_USER", "")
WP_APP_PASSWORD = os.environ.get("WP_NET_APP_PASSWORD", "")

BASE_DIR         = os.path.join(os.path.dirname(__file__), "..")
USED_TOPICS_FILE  = os.path.join(BASE_DIR, "data", "wp-net-used-topics.json")
USED_IMAGES_FILE  = os.path.join(BASE_DIR, "data", "wp-net-used-images.json")
MAX_USED_IMAGES   = 100
POSTS_PER_RUN    = random.randint(2, 4)

# ── 카테고리 ──────────────────────────────────────
CATEGORIES = {
    "casino-news": {
        "name": "카지노 뉴스",
        "keywords": [
            "MGM Resorts", "Las Vegas Sands", "Wynn Resorts", "Melco Resorts",
            "Genting Group", "Caesars Entertainment", "신규 카지노 라이선스",
            "카지노 IPO", "카지노 주가 동향", "카지노 리조트 개발",
            "카지노 기업 실적", "신규 카지노 오픈", "정부 규제 정책",
            "카지노 투자 소식", "글로벌 카지노 순위",
            "태국 카지노 합법화", "방콕 엔터테인먼트 컴플렉스",
            "푸켓 카지노 투자", "태국 정부 카지노 정책", "태국 IR 개발",
        ],
        "pexels_queries": ["casino resort luxury", "casino industry business", "casino gaming floor"],
        "slug_prefix": "casino-news",
        "slug_suffixes": ["analysis", "report", "update", "news", "overview", "review"],
        "priority": 1,
    },
    "toto-news": {
        "name": "토토 뉴스",
        "keywords": [
            "DraftKings", "FanDuel", "BetMGM", "Flutter Entertainment", "Entain",
            "미국 스포츠 베팅 시장", "영국 도박위원회 규제", "브라질 스포츠 베팅",
            "인도 스포츠 베팅", "스포츠북 산업",
            "스포츠 베팅 시장 규모", "국가별 베팅 규제", "합법 베팅 라이선스",
            "베팅 산업 성장률", "이스포츠 베팅 동향", "베팅 사기 단속",
            "올림픽 베팅 시장", "베팅 플랫폼 변화",
        ],
        "pexels_queries": ["sports betting odds", "sports stadium crowd", "online sports betting"],
        "slug_prefix": "toto-news",
        "slug_suffixes": ["analysis", "report", "update", "trends", "overview", "news"],
        "priority": 9,
    },
    "slot-news": {
        "name": "슬롯 뉴스",
        "keywords": [
            "Pragmatic Play", "Evolution Gaming", "Playtech", "Light & Wonder",
            "IGT", "NetEnt", "Microgaming", "Nolimit City", "Hacksaw Gaming",
            "슬롯 프로바이더 시장", "신규 슬롯 출시", "슬롯 개발사 동향",
            "슬롯 RTP 비교", "메가웨이즈 트렌드", "슬롯 전시회 소식",
            "잭팟 슬롯 동향", "슬롯 규제 변화", "인기 슬롯 순위",
        ],
        "pexels_queries": ["slot machine casino", "casino gambling machines", "casino gaming"],
        "slug_prefix": "slot-news",
        "slug_suffixes": ["news", "update", "trends", "report", "analysis", "review"],
        "priority": 8,
    },
    "industry-trends": {
        "name": "카지노 & 토토 업계 동향",
        "keywords": [
            "Global Gaming Report", "GGR 통계", "카지노 ESG",
            "카지노 디지털 전환", "무현금 카지노", "AI 딜러",
            "크립토 카지노", "온라인 게이밍 시장", "iGaming 시장",
            "글로벌 카지노 투자", "카지노 AI 도입", "온라인 카지노 규제",
            "불법 도박 단속", "카지노 블록체인", "라이선스 정책 변화",
            "카지노 사이버보안", "도박 중독 정책", "카지노 산업 전망",
        ],
        "pexels_queries": ["casino technology innovation", "gaming industry digital", "casino trends future"],
        "slug_prefix": "industry",
        "slug_suffixes": ["trends", "report", "analysis", "outlook", "update", "overview"],
        "priority": 5,
    },
    "macau-casino": {
        "name": "마카오 카지노",
        "keywords": [
            "MGM Macau", "Wynn Macau", "Sands China", "Galaxy Entertainment",
            "Melco Resorts", "Studio City", "City of Dreams", "Cotai Strip",
            "Macau SAR 정부", "마카오 프리미엄 매스 시장",
            "마카오 월별 GGR", "중국 관광객 회복", "코타이 스트립 개발",
            "마카오 정부 규제", "마카오 카지노 세수", "마카오 관광 통계",
        ],
        "pexels_queries": ["Macau casino resort", "Cotai Strip Macau", "Macau skyline gaming"],
        "slug_prefix": "macau",
        "slug_suffixes": ["news", "report", "analysis", "update", "trends", "review"],
        "priority": 2,
    },
    "philippines-casino": {
        "name": "필리핀 카지노",
        "keywords": [
            "PAGCOR", "Newport World Resorts", "Okada Manila", "Solaire Resort",
            "City of Dreams Manila", "Bloomberry", "Entertainment City",
            "Clark Freeport", "POGO 규제", "필리핀 IR 프로젝트",
            "마닐라 카지노 리조트", "클락 카지노", "앙헬레스 카지노",
            "세부 카지노", "필리핀 카지노 매출",
        ],
        "pexels_queries": ["Manila casino resort", "Philippines gaming", "Entertainment City Manila"],
        "slug_prefix": "philippines",
        "slug_suffixes": ["news", "report", "analysis", "update", "trends", "review"],
        "priority": 3,
    },
    "vietnam-casino": {
        "name": "베트남 카지노",
        "keywords": [
            "Corona Resort & Casino", "Ho Tram Strip", "Van Don Casino",
            "Da Nang IR", "베트남 시범사업", "외국인 카지노 정책",
            "카지노 투자법", "베트남 복합리조트", "카지노 관광객 유치",
            "푸꾸옥 카지노 개발", "다낭 복합리조트", "호치민 카지노",
            "하노이 카지노", "베트남 카지노 규제 완화",
        ],
        "pexels_queries": ["Vietnam resort beach", "Da Nang resort Vietnam", "Phu Quoc island resort"],
        "slug_prefix": "vietnam",
        "slug_suffixes": ["news", "report", "analysis", "update", "trends", "review"],
        "priority": 7,
    },
    "cambodia-casino": {
        "name": "캄보디아 카지노",
        "keywords": [
            "NagaWorld", "NagaCorp", "Poipet", "Sihanoukville",
            "Koh Kong", "Phnom Penh Casino", "캄보디아 게임위원회",
            "중국 관광객 회복", "카지노 경제특구", "국경 카지노 시장",
            "포이펫 카지노", "시아누크빌 카지노", "프놈펜 카지노",
            "캄보디아 도박법", "캄보디아 IR 개발",
        ],
        "pexels_queries": ["Phnom Penh Cambodia", "NagaWorld casino Phnom Penh", "Cambodia resort gaming"],
        "slug_prefix": "cambodia",
        "slug_suffixes": ["news", "report", "analysis", "update", "trends", "review"],
        "priority": 6,
    },
    "overseas-casino": {
        "name": "해외 카지노",
        "keywords": [
            "라스베가스 카지노", "MGM Grand", "Bellagio", "Caesars Palace", "Wynn Las Vegas",
            "애틀랜틱시티 카지노", "Hard Rock Atlantic City", "Borgata",
            "모나코 카지노", "Monte Carlo Casino", "유럽 카지노 시장",
            "런던 카지노", "Hippodrome Casino", "영국 카지노 규제",
            "싱가포르 카지노", "Marina Bay Sands", "Resorts World Sentosa",
            "일본 IR 카지노", "오사카 IR", "나가사키 IR",
            "태국 카지노 합법화", "방콕 엔터테인먼트 컴플렉스",
            "한국 카지노 규제", "강원랜드", "파라다이스시티",
            "호주 카지노 시장", "Crown Resorts", "Star Entertainment",
            "인도 카지노 합법화", "Goa 카지노",
            "UAE 카지노 합법화", "두바이 카지노",
            "브라질 카지노 합법화", "남미 도박 시장",
            "남아공 카지노", "Sun City Resort",
        ],
        "pexels_queries": ["Asia casino resort luxury", "Singapore Marina Bay casino", "international casino resort"],
        "slug_prefix": "overseas",
        "slug_suffixes": ["news", "report", "analysis", "update", "trends", "review"],
        "priority": 4,
    },
}

# ── 카테고리별 작성자 ID ──────────────────────────
CATEGORY_AUTHORS = {
    "casino-news":        8,   # newseditor
    "toto-news":          9,   # totoeditor
    "slot-news":          6,   # slotseditor
    "industry-trends":    7,   # industryeditor
    "macau-casino":       11,  # macaueditor
    "philippines-casino": 14,  # philippineseditor
    "vietnam-casino":     12,  # vietnameditor
    "cambodia-casino":    13,  # cambodiaeditor
    "overseas-casino":    10,  # asiaeditor
}

# ── 카테고리별 제목 키워드 풀 ─────────────────────
CATEGORY_TITLE_KEYWORDS = {
    "casino-news":       ["글로벌 카지노", "카지노 산업", "MGM Resorts", "Las Vegas Sands", "카지노 업계"],
    "toto-news":         ["스포츠 베팅", "토토 시장", "DraftKings", "FanDuel", "스포츠북"],
    "slot-news":         ["슬롯 시장", "슬롯 개발사", "Pragmatic Play", "Evolution Gaming", "슬롯 산업"],
    "industry-trends":   ["카지노 업계 동향", "iGaming", "온라인 카지노 시장", "글로벌 도박 산업", "카지노 기술"],
    "macau-casino":      ["마카오 카지노", "마카오 GGR", "코타이 스트립", "Sands China", "마카오 정부"],
    "philippines-casino":["필리핀 카지노", "PAGCOR", "마닐라 카지노", "Entertainment City", "필리핀 IR"],
    "vietnam-casino":    ["베트남 카지노", "푸꾸옥 카지노", "다낭 리조트", "베트남 IR", "베트남 복합리조트"],
    "cambodia-casino":   ["캄보디아 카지노", "NagaWorld", "프놈펜 카지노", "시아누크빌", "NagaCorp"],
    "overseas-casino":   ["해외 카지노", "싱가포르 카지노", "일본 IR", "Marina Bay Sands", "아시아 카지노"],
}

# ── 카테고리별 참고 출처 ───────────────────────────
CATEGORY_SOURCES = {
    "casino-news": [
        "[GGRAsia](https://www.ggasia.com)",
        "[Gambling Insider](https://gamblinginsider.com)",
        "[iGaming Business](https://igamingbusiness.com)",
        "[GamblingNews](https://www.gamblingnews.com)",
    ],
    "macau-casino": [
        "[Macau Business](https://macaubusiness.com)",
        "[DICJ](https://www.dicj.gov.mo)",
        "[GGRAsia](https://www.ggasia.com)",
        "[Asia Gaming Brief](https://agbrief.com)",
    ],
    "philippines-casino": [
        "[PAGCOR](https://www.pagcor.ph)",
        "[GGRAsia](https://www.ggasia.com)",
        "[Asia Gaming Brief](https://agbrief.com)",
        "[Gambling Insider](https://gamblinginsider.com)",
    ],
    "vietnam-casino": [
        "[GGRAsia](https://www.ggasia.com)",
        "[Asia Gaming Brief](https://agbrief.com)",
        "[iGaming Business](https://igamingbusiness.com)",
        "[GamblingNews](https://www.gamblingnews.com)",
    ],
    "cambodia-casino": [
        "[GGRAsia](https://www.ggasia.com)",
        "[Asia Gaming Brief](https://agbrief.com)",
        "[GamblingNews](https://www.gamblingnews.com)",
        "[Gambling Insider](https://gamblinginsider.com)",
    ],
    "slot-news": [
        "[iGaming Business](https://igamingbusiness.com)",
        "[Gambling Insider](https://gamblinginsider.com)",
        "[GamblingNews](https://www.gamblingnews.com)",
        "[Asia Gaming Brief](https://agbrief.com)",
    ],
    "toto-news": [
        "[iGaming Business](https://igamingbusiness.com)",
        "[Gambling Insider](https://gamblinginsider.com)",
        "[GamblingNews](https://www.gamblingnews.com)",
        "[GGRAsia](https://www.ggasia.com)",
    ],
    "industry-trends": [
        "[iGaming Business](https://igamingbusiness.com)",
        "[GGRAsia](https://www.ggasia.com)",
        "[Asia Gaming Brief](https://agbrief.com)",
        "[Gambling Insider](https://gamblinginsider.com)",
    ],
    "overseas-casino": [
        "[GGRAsia](https://www.ggasia.com)",
        "[Asia Gaming Brief](https://agbrief.com)",
        "[iGaming Business](https://igamingbusiness.com)",
        "[GamblingNews](https://www.gamblingnews.com)",
    ],
}

# ── 중복 검사용 불용어 ─────────────────────────────
STOP_WORDS = {
    "카지노", "뉴스", "시장", "업계", "현황", "분석", "전망", "동향",
    "가이드", "최신", "주요", "핵심", "완벽", "정리", "소개", "설명",
    "vs", "&", "·", "-", "—", "및", "와", "과", "의",
}

# ── 앵글 ──────────────────────────────────────────
ANGLES = {
    "속보": "최신 사실을 육하원칙(누가·언제·어디서·무엇을·어떻게·왜) 중심으로 신속하게 전달하는 관점",
    "분석": "수치·데이터·통계를 기반으로 사건의 의미와 배경을 심층 해석하는 관점",
    "동향": "시장·산업의 흐름과 반복 패턴을 추적하여 방향성을 파악하는 관점",
    "현장": "특정 지역·기업·인물에 집중하여 구체적 상황을 생생하게 보도하는 관점",
    "전망": "현재 상황을 토대로 업계의 미래 방향과 시사점을 도출하는 관점",
}

# ── 콘텐츠 모델 ────────────────────────────────────
CONTENT_MODELS = {
    "분석형": {
        "desc": "수치·통계·데이터를 중심으로 제시하고 결론 도출",
        "structure": "배경 → 데이터 제시 → 수치 비교 → 시사점",
    },
    "동향형": {
        "desc": "최근 변화와 흐름을 짚고 업계에 갖는 의미 분석",
        "structure": "현황 → 변화 요인 → 주요 트렌드 → 업계 영향",
    },
    "Q&A형": {
        "desc": "독자가 자주 묻는 질문과 답변 형식으로 전개",
        "structure": "배경 → Q1+A1 → Q2+A2 → Q3+A3 → 총정리",
    },
    "비교형": {
        "desc": "두 가지 이상을 비교하여 장단점과 시사점 제시",
        "structure": "비교 대상 소개 → 기준별 비교표 → 차이점 → 결론",
        "note": "마크다운 비교표 1개 이상 필수",
    },
    "보도형": {
        "desc": "사실 중심으로 사건·발표·정책을 간결하게 전달",
        "structure": "핵심 사실 → 배경 설명 → 관련 수치 → 향후 전망",
    },
    "심층보도형": {
        "desc": "하나의 주제를 다각도로 깊이 파고드는 장문 기사",
        "structure": "이슈 제기 → 역사적 배경 → 현황 분석 → 이해관계자 → 전망",
    },
}

# ── 문체 ──────────────────────────────────────────
TONES = [
    "저널리즘형 — 사실 중심, 중립적, 출처를 본문에 자연스럽게 녹임",
    "분석적 — 데이터와 수치 중심, 건조하고 객관적인 서술체",
    "친근한 — 쉬운 언어로 독자가 이해하기 쉽게, 공감형 표현 활용",
    "교과서형 — 체계적 설명, 소제목 명확, 정의 먼저 제시 후 사례 보강",
]

# ── 도입부 패턴 ───────────────────────────────────
INTRO_TYPES = [
    "핵심 팩트나 통계 수치를 첫 문장에 바로 제시하며 시작",
    "독자가 궁금해할 핵심 질문을 던지며 시작",
    "최근 발생한 구체적 사건이나 발표로 시작",
    "업계 현황의 변화나 충격적 수치로 시작",
]

# ── 마무리 패턴 ───────────────────────────────────
ENDING_TYPES = [
    "핵심 내용 3줄 요약으로 마무리",
    "업계 전망과 독자가 주목해야 할 포인트로 마무리",
    "관련 이슈의 미래 변화 가능성으로 마무리",
    "핵심 체크포인트 목록으로 마무리",
]

# ── 글 길이 ───────────────────────────────────────
LENGTH_OPTIONS = [
    {"label": "단문", "min": 1500},
    {"label": "중문", "min": 2000},
    {"label": "장문", "min": 2500},
]

SYSTEM_INSTRUCTION = """
당신은 글로벌 카지노·스포츠베팅 업계를 전문으로 다루는 한국어 뉴스 미디어 WooriWin News의 기자입니다.

━━━ 핵심 원칙 ━━━
- 사실 기반, 중립적, 출처 명시 저널리즘 준수
- 글 제목이 독자에게 한 약속을 본문이 정확히 충족시킬 것
- 특정 카지노 사이트 홍보·유도 표현 금지
- 불법 도박 조장 표현 금지 (단속 뉴스 보도는 가능)
- 수익 보장·당첨 기대 표현 절대 금지
- 본문에 'SEO', 'E-E-A-T' 등 메타 용어 노출 금지

━━━ 뉴스 기사 형식 ━━━
- 육하원칙 기반 사실 전달
- 마크다운 표 1개 이상 (데이터 있을 경우)
- 숫자·통계는 구체적으로 (단위 명시)
- 기업명·지명은 한국어 + 영문 병기 첫 등장 시
"""


# ── WP REST API ────────────────────────────────────

def get_scraper():
    scraper = cloudscraper.create_scraper(
        browser={"browser": "chrome", "platform": "windows", "mobile": False}
    )
    creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()
    scraper.headers.update({
        "Authorization": f"Basic {creds}",
        "Content-Type": "application/json",
    })
    return scraper


def get_wp_category_ids() -> dict:
    scraper = get_scraper()
    try:
        res = scraper.get(f"{WP_URL}/wp-json/wp/v2/categories", params={"per_page": 100}, timeout=15)
        res.raise_for_status()
        return {cat["slug"]: cat["id"] for cat in res.json()}
    except Exception as e:
        print(f"  ❌ 카테고리 ID 조회 실패: {e}")
        return {}


def get_wp_post_titles() -> list:
    """WP 기존 포스트 제목 전체 조회 (중복 방지용)."""
    scraper = get_scraper()
    titles = []
    page = 1
    while True:
        try:
            res = scraper.get(
                f"{WP_URL}/wp-json/wp/v2/posts",
                params={"per_page": 100, "page": page, "_fields": "title"},
                timeout=15,
            )
            if res.status_code in (400, 404):
                break
            res.raise_for_status()
            data = res.json()
            if not data:
                break
            for post in data:
                t = post.get("title", {})
                titles.append(t.get("rendered", "") if isinstance(t, dict) else str(t))
            page += 1
            time.sleep(0.5)
        except Exception as e:
            print(f"  ⚠️ WP 포스트 제목 조회 실패 (page {page}): {e}")
            break
    return titles


def upload_image_to_wp(image_url: str, alt_text: str) -> int | None:
    """Pexels 이미지를 WP 미디어 라이브러리에 업로드하고 media ID 반환."""
    if not image_url:
        return None
    try:
        img_res = requests.get(image_url, timeout=15)
        img_res.raise_for_status()
        img_data = img_res.content
        content_type = img_res.headers.get("Content-Type", "image/jpeg").split(";")[0].strip()

        filename = image_url.split("/")[-1].split("?")[0]
        if "." not in filename:
            filename += ".jpg"

        scraper = cloudscraper.create_scraper(
            browser={"browser": "chrome", "platform": "windows", "mobile": False}
        )
        creds = base64.b64encode(f"{WP_USER}:{WP_APP_PASSWORD}".encode()).decode()

        res = scraper.post(
            f"{WP_URL}/wp-json/wp/v2/media",
            data=img_data,
            headers={
                "Authorization": f"Basic {creds}",
                "Content-Type": content_type,
                "Content-Disposition": f'attachment; filename="{filename}"',
            },
            timeout=60,
        )
        res.raise_for_status()
        media = res.json()
        media_id = media.get("id")

        if media_id and alt_text:
            scraper.post(
                f"{WP_URL}/wp-json/wp/v2/media/{media_id}",
                json={"alt_text": alt_text},
                headers={
                    "Authorization": f"Basic {creds}",
                    "Content-Type": "application/json",
                },
                timeout=15,
            )
        print(f"  ✅ 이미지 업로드 완료: ID={media_id}")
        return media_id
    except Exception as e:
        print(f"  ❌ 이미지 업로드 실패: {e}")
        return None


def post_to_wordpress(title: str, content: str, excerpt: str, slug: str,
                       category_ids: list, keyword: str = "",
                       media_id: int = None, category_name: str = "",
                       author_id: int = None, faq_jsonld: str = "") -> dict | None:
    scraper = get_scraper()
    seo_title = f"{title} | WooriWin News"
    data = {
        "title": title,
        "content": content,
        "excerpt": excerpt,
        "slug": slug,
        "status": "publish",
        "categories": category_ids,
        "format": "standard",
        "meta": {
            "rank_math_focus_keyword": keyword,
            "rank_math_description": excerpt,
            "rank_math_title": seo_title,
            "rank_math_robots": ["index", "follow"],
            "rank_math_og_title": seo_title,
            "rank_math_og_description": excerpt,
            "rank_math_twitter_title": seo_title,
            "rank_math_twitter_description": excerpt,
            "rank_math_twitter_use_facebook": "off",
            "rank_math_twitter_card_type": "summary_large_image",
            "wn_faq_schema": faq_jsonld,
        },
    }
    if media_id:
        data["featured_media"] = media_id
    if author_id:
        data["author"] = author_id

    try:
        res = scraper.post(f"{WP_URL}/wp-json/wp/v2/posts", json=data, timeout=30)
        res.raise_for_status()
        result = res.json()
        print(f"  ✅ WP 포스팅 완료: {result.get('link', '')}")
        return result
    except Exception as e:
        print(f"  ❌ WP 포스팅 실패: {e}")
        if hasattr(e, 'response') and e.response is not None:
            print(f"     응답: {e.response.text[:300]}")
        return None


# ── Gemini ────────────────────────────────────────

def setup_gemini() -> genai.Client:
    return genai.Client(api_key=GEMINI_API_KEY)


def clean_json(text: str) -> str:
    text = text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    return text.strip()


def safe_generate(client: genai.Client, prompt: str, retries: int = 3):
    for attempt in range(retries + 1):
        try:
            current_prompt = prompt
            if attempt > 0:
                current_prompt += f"\n\n[재시도 {attempt}회차: 반드시 유효한 JSON만 출력]"
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=current_prompt,
                config={"system_instruction": SYSTEM_INSTRUCTION},
            )
            return json.loads(clean_json(response.text))
        except json.JSONDecodeError as e:
            if attempt < retries:
                print(f"  ⚠️ JSON 파싱 실패({e}), 재시도 {attempt+1}...")
                time.sleep(2)
            else:
                print(f"  ❌ JSON 파싱 최종 실패")
                return None
        except Exception as e:
            if attempt < retries:
                print(f"  ⚠️ 생성 실패({e}), 재시도 {attempt+1}...")
                time.sleep(2)
            else:
                print(f"  ❌ 생성 최종 실패")
                return None


# ── 중복 제목 검사 ────────────────────────────────

def extract_keywords_from_title(title: str) -> set:
    words = re.split(r'[\s:,()·\-—|]+', title)
    return {w for w in words if len(w) >= 2 and w not in STOP_WORDS}


def is_duplicate_title(new_title: str, existing_titles: list, threshold: int = 3) -> bool:
    new_words = extract_keywords_from_title(new_title)
    for old in existing_titles:
        if len(new_words & extract_keywords_from_title(old)) >= threshold:
            return True
    return False


# ── 제목 생성 (중복 회피) ─────────────────────────

def generate_unique_title(client: genai.Client, category_slug: str, keyword: str,
                           angle: str, content_model: str,
                           existing_titles: list, max_attempts: int = 3) -> str:
    cat = CATEGORIES[category_slug]
    title_kw_pool = CATEGORY_TITLE_KEYWORDS.get(category_slug, [cat["name"]])
    title_kw = random.choice(title_kw_pool)

    existing_sample = existing_titles[-60:]
    existing_list   = "\n".join(f"- {t}" for t in existing_sample) if existing_sample else "없음"

    for attempt in range(max_attempts):
        prompt = f"""
다음 조건으로 카지노/베팅 뉴스 기사 제목 3개를 생성하세요.

카테고리: {cat['name']}
핵심 키워드: {keyword}
뉴스 앵글: {angle} — {ANGLES[angle]}
콘텐츠 모델: {content_model} — {CONTENT_MODELS[content_model]['desc']}
제목에 포함할 키워드: {title_kw}

조건:
- 위 키워드를 제목 어디에나 자연스럽게 포함
- 앵글({angle})과 콘텐츠 모델({content_model})이 암시하는 내용 반영
- 과장·선정적·수익보장 표현 금지
- 각 제목은 서로 다른 각도
- 제목에 콜론(:) 사용 금지
- 25~50자 사이
- 뉴스 헤드라인 스타일

기존 제목 (핵심 단어 3개 이상 겹치면 안 됨):
{existing_list}

출력: JSON 배열만 (마크다운 없이)
예시: ["제목1", "제목2", "제목3"]
"""
        result = safe_generate(client, prompt, retries=1)
        if isinstance(result, list) and result:
            for title in result:
                if isinstance(title, str) and not is_duplicate_title(title, existing_titles):
                    print(f"  🏆 선택된 제목: '{title}'")
                    return title
        print(f"  🔄 중복 제목 → 재시도 ({attempt+1}/{max_attempts})")
        time.sleep(1)

    fallback = f"{cat['name']}: {keyword} 최신 동향"
    print(f"  ⚠️ Fallback 제목: '{fallback}'")
    return fallback


# ── 주제 추적 ──────────────────────────────────────

def load_used_images() -> set:
    if os.path.exists(USED_IMAGES_FILE):
        try:
            with open(USED_IMAGES_FILE, encoding="utf-8") as f:
                return set(json.load(f))
        except Exception:
            pass
    return set()


def save_used_images(used: set):
    os.makedirs(os.path.dirname(USED_IMAGES_FILE), exist_ok=True)
    recent = list(used)[-MAX_USED_IMAGES:]
    with open(USED_IMAGES_FILE, "w", encoding="utf-8") as f:
        json.dump(recent, f, ensure_ascii=False, indent=2)


def load_used_topics() -> dict:
    if os.path.exists(USED_TOPICS_FILE):
        try:
            with open(USED_TOPICS_FILE, encoding="utf-8") as f:
                return json.load(f)
        except Exception:
            pass
    return {cat: [] for cat in CATEGORIES}


def save_used_topics(used: dict):
    os.makedirs(os.path.dirname(USED_TOPICS_FILE), exist_ok=True)
    with open(USED_TOPICS_FILE, "w", encoding="utf-8") as f:
        json.dump(used, f, ensure_ascii=False, indent=2)


def get_next_topic(category: str, used_topics: dict) -> tuple:
    all_kws    = CATEGORIES[category]["keywords"]
    all_angles = list(ANGLES.keys())
    all_models = list(CONTENT_MODELS.keys())
    used_set   = set(used_topics.get(category, []))
    available  = [
        (kw, angle, model)
        for kw    in all_kws
        for angle in all_angles
        for model in all_models
        if f"{kw}|{angle}|{model}" not in used_set
    ]
    if not available:
        print(f"  ♻️ [{category}] 전체 소진 → 초기화")
        used_topics[category] = []
        available = [(kw, a, m) for kw in all_kws for a in all_angles for m in all_models]
    kw, angle, model = random.choice(available)
    used_topics.setdefault(category, []).append(f"{kw}|{angle}|{model}")
    return kw, angle, model


# ── 이미지 ────────────────────────────────────────

def fetch_pexels_image(queries: list, used_images: set = None) -> str:
    fallback = "https://images.pexels.com/photos/1871508/pexels-photo-1871508.jpg"
    if not PEXELS_API_KEY:
        return fallback
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
                return random.choice(photos[:5])["src"]["large2x"]
        except Exception as e:
            print(f"  ⚠️ 이미지 오류 ({query}): {e}")
        time.sleep(0.3)
    print("  ⚠️ fallback 이미지 사용")
    return fallback


# ── 콘텐츠 생성 ────────────────────────────────────

def generate_article(client: genai.Client, title: str, category_slug: str,
                      keyword: str, angle: str, content_model: str,
                      tone: str, intro_type: str, ending_type: str,
                      length_option: dict) -> dict | None:
    cat = CATEGORIES[category_slug]
    model_info  = CONTENT_MODELS[content_model]
    slug_prefix = cat["slug_prefix"]
    slug_suffixes = cat.get("slug_suffixes", ["news", "update"])
    random_suffix = random.choice(slug_suffixes)
    model_note  = model_info.get("note", "")

    prompt = f"""
━━━ 뉴스 기사 생성 명세 ━━━

글 제목    : {title}
카테고리   : {cat['name']}
핵심 키워드: {keyword}
뉴스 앵글  : {angle} — {ANGLES[angle]}
콘텐츠 모델: {content_model} — {model_info['desc']}
  └ 전개 구조: {model_info['structure']}{"" if not model_note else f"{chr(10)}  └ 추가 요구사항: {model_note}"}
문체      : {tone}
도입부    : {intro_type}
마무리    : {ending_type}
글 길이   : {length_option['label']} ({length_option['min']}자 이상)

━━━ 작성 지침 ━━━
- 제목이 암시하는 주제를 본문이 정확히 충족할 것
- H2 헤더(##) 3~6개
- H3 소제목(###) 필요 시 사용
- 글 길이 반드시 {length_option['min']}자 이상
- 수치·통계 포함 시 단위 명시
- 마크다운 표 1개 이상 (관련 데이터 있을 경우)
- 기업명·지명 첫 등장 시 한국어 + 영문 병기
- 슬러그: {slug_prefix}-로 시작, 예시: {slug_prefix}-keyword-{random_suffix}, 50자 이내
- 본문 마지막에 반드시 아래 출처 전부를 표기:
  ## 참고 출처
{chr(10).join('  - ' + s for s in CATEGORY_SOURCES.get(category_slug, list(CATEGORY_SOURCES['casino-news'])))}

━━━ 출력 형식 (순수 JSON만) ━━━
{{
  "slug": "{slug_prefix}-unique-slug",
  "excerpt": "기사 요약 (150자 이내, {keyword} 포함)",
  "imageAlt": "이미지 설명 (영문, 50자 이내)",
  "pexels_query": "영문 이미지 검색어",
  "keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"],
  "content": "본문 마크다운 ({length_option['min']}자 이상)",
  "faq": [
    {{"q": "질문", "a": "답변"}}
  ]
}}
"""
    return safe_generate(client, prompt)


# ── HTML 변환 ─────────────────────────────────────

def parse_md_table(table_lines: list) -> str:
    """마크다운 표 라인 목록 → HTML table."""
    header_rows = []
    body_rows   = []
    is_header   = True
    for line in table_lines:
        cells = [c.strip() for c in line.strip().strip('|').split('|')]
        if all(re.match(r'^[-: ]+$', c) for c in cells if c.strip()):
            is_header = False
            continue
        row = '<tr>' + ''.join(
            f'<th>{c}</th>' if is_header else f'<td>{c}</td>' for c in cells
        ) + '</tr>'
        (header_rows if is_header else body_rows).append(row)

    html = '<table>\n'
    if header_rows:
        html += '<thead>\n' + '\n'.join(header_rows) + '\n</thead>\n'
    if body_rows:
        html += '<tbody>\n' + '\n'.join(body_rows) + '\n</tbody>\n'
    html += '</table>'
    return html


def markdown_to_html(md: str) -> str:
    # 1. 표 먼저 (라인 단위로 연속된 | 블록 수집)
    lines = md.split('\n')
    processed = []
    i = 0
    while i < len(lines):
        if lines[i].strip().startswith('|'):
            table_lines = []
            while i < len(lines) and lines[i].strip().startswith('|'):
                table_lines.append(lines[i])
                i += 1
            processed.append(parse_md_table(table_lines))
        else:
            processed.append(lines[i])
            i += 1
    md = '\n'.join(processed)

    # 2. 헤더
    md = re.sub(r'^### (.+)$', r'<h3>\1</h3>', md, flags=re.MULTILINE)
    md = re.sub(r'^## (.+)$',  r'<h2>\1</h2>',  md, flags=re.MULTILINE)
    md = re.sub(r'^# (.+)$',   r'<h1>\1</h1>',   md, flags=re.MULTILINE)

    # 3. 인라인 링크
    md = re.sub(r'\[([^\]]+)\]\(([^\)]+)\)', r'<a href="\2" target="_blank" rel="noopener noreferrer">\1</a>', md)

    # 4. 볼드/이탤릭
    md = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', md)
    md = re.sub(r'\*(.+?)\*',     r'<em>\1</em>',         md)

    # 4. 인용
    md = re.sub(r'^> (.+)$', r'<blockquote><p>\1</p></blockquote>', md, flags=re.MULTILINE)

    # 5. 단락 처리
    paragraphs = md.split('\n\n')
    result = []
    for p in paragraphs:
        p = p.strip()
        if not p:
            continue
        if p.startswith('<'):
            result.append(p)
        elif p.startswith('- ') or p.startswith('* '):
            items = re.findall(r'^[-*] (.+)$', p, re.MULTILINE)
            result.append('<ul>' + ''.join(f'<li>{item}</li>' for item in items) + '</ul>')
        elif re.match(r'^\d+\.', p):
            items = re.findall(r'^\d+\. (.+)$', p, re.MULTILINE)
            result.append('<ol>' + ''.join(f'<li>{item}</li>' for item in items) + '</ol>')
        else:
            result.append(f'<p>{p}</p>')
    return '\n'.join(result)


def insert_inline_image_html(content: str, image_url: str, alt_text: str) -> str:
    """세 번째 <h2> 직전에 본문 이미지 삽입."""
    if not image_url:
        return content
    matches = [m.start() for m in re.finditer(r'<h2>', content)]
    if len(matches) >= 3:
        pos = matches[2]
        img_html = (
            f'<figure class="wp-block-image size-large">'
            f'<img src="{image_url}" alt="{alt_text}" loading="lazy"/>'
            f'</figure>\n\n'
        )
        return content[:pos] + img_html + content[pos:]
    return content


def build_faq_html(faq: list) -> str:
    if not faq:
        return ""
    html = '\n<h2>자주 묻는 질문</h2>\n'
    for item in faq:
        html += f'<h3>{item["q"]}</h3>\n<p>{item["a"]}</p>\n'
    return html


def build_jsonld_news(title: str, excerpt: str, slug: str, keyword: str,
                       category_name: str, image_url: str) -> str:
    now_iso = datetime.now(timezone(timedelta(hours=9))).isoformat()
    schema = {
        "@context": "https://schema.org",
        "@type": "NewsArticle",
        "headline": title,
        "description": excerpt,
        "url": f"{WP_URL}/{slug}/",
        "datePublished": now_iso,
        "dateModified": now_iso,
        "author": {"@type": "Organization", "name": "WooriWin News", "url": WP_URL},
        "publisher": {
            "@type": "Organization",
            "name": "WooriWin News",
            "url": WP_URL,
            "logo": {"@type": "ImageObject", "url": f"{WP_URL}/wp-content/uploads/logo.png"},
        },
        "image": image_url or f"{WP_URL}/wp-content/uploads/og-default.jpg",
        "keywords": keyword,
        "articleSection": category_name,
        "inLanguage": "ko-KR",
    }
    return f'\n<script type="application/ld+json">\n{json.dumps(schema, ensure_ascii=False, indent=2)}\n</script>'


TRUSTED_SITES = [
    {"name": "BeGambleAware",          "url": "https://www.begambleaware.org",           "desc": "책임감 있는 도박 지원 기관"},
    {"name": "eCOGRA",                 "url": "https://ecogra.org",                      "desc": "공인 게임 공정성 감사기관"},
    {"name": "UK Gambling Commission", "url": "https://www.gamblingcommission.gov.uk",   "desc": "영국 도박 규제기관"},
    {"name": "GameCheck",              "url": "https://www.gamecheck.org",               "desc": "게임 안전성 인증"},
    {"name": "GamStop",                "url": "https://www.gamstop.co.uk",               "desc": "자가 제외 서비스"},
    {"name": "Malta Gaming Authority", "url": "https://www.mga.org.mt",                  "desc": "몰타 게임 규제기관"},
]

def build_trusted_html() -> str:
    items = "".join(
        f'<li><a href="{s["url"]}" target="_blank" rel="noopener noreferrer">'
        f'<strong>{s["name"]}</strong>'
        f'<span>{s["desc"]}</span></a></li>'
        for s in TRUSTED_SITES
    )
    return (
        '\n<div class="wn-trusted">'
        '<p class="wn-trusted-title">Trusted &amp; Certified By</p>'
        f'<ul>{items}</ul>'
        '</div>'
        '\n<style>'
        '.wn-trusted{margin:32px 0 8px;padding:18px 20px;background:#f9f9f9;border:1px solid #e8e8e8;border-radius:4px;}'
        '.wn-trusted-title{font-size:11px;font-weight:700;color:#999;letter-spacing:.8px;text-transform:uppercase;margin:0 0 12px;}'
        '.wn-trusted ul{list-style:none;margin:0;padding:0;display:flex;flex-wrap:wrap;gap:10px;}'
        '.wn-trusted li a{display:flex;flex-direction:column;padding:6px 14px;background:#fff;border:1px solid #ddd;border-radius:3px;text-decoration:none;transition:border-color .2s;}'
        '.wn-trusted li a:hover{border-color:#999;}'
        '.wn-trusted li a strong{font-size:12px;color:#333;}'
        '.wn-trusted li a span{font-size:10px;color:#999;margin-top:2px;}'
        '</style>'
    )


def build_jsonld_faq(faq: list) -> str:
    """FAQPage 스키마를 JSON 문자열로 반환 (script 태그 없이 — wp_head에서 감쌈)."""
    if not faq:
        return ""
    schema = {
        "@context": "https://schema.org",
        "@type": "FAQPage",
        "mainEntity": [
            {
                "@type": "Question",
                "name": item["q"],
                "acceptedAnswer": {"@type": "Answer", "text": item["a"]},
            }
            for item in faq
        ],
    }
    return json.dumps(schema, ensure_ascii=False)


# ── 전체 삭제 ─────────────────────────────────────

def delete_all_posts():
    scraper = get_scraper()
    print("\n🗑️  전체 포스트 조회 중...")
    post_ids, media_ids = [], []
    page = 1
    while True:
        try:
            res = scraper.get(
                f"{WP_URL}/wp-json/wp/v2/posts",
                params={"per_page": 100, "page": page, "_fields": "id,featured_media"},
                timeout=15,
            )
            if res.status_code in (400, 404): break
            data = res.json()
            if not data: break
            for p in data:
                post_ids.append(p["id"])
                if p.get("featured_media"):
                    media_ids.append(p["featured_media"])
            page += 1
        except Exception as e:
            print(f"  ⚠️ 조회 실패: {e}"); break

    print(f"  포스트 {len(post_ids)}개, 미디어 {len(media_ids)}개 발견")
    confirm = input("  ⚠️ 정말 전체 삭제하시겠습니까? (yes 입력): ").strip()
    if confirm != "yes":
        print("  취소됨"); return False

    print("  포스트 삭제 중...")
    for pid in post_ids:
        try:
            scraper.delete(f"{WP_URL}/wp-json/wp/v2/posts/{pid}", params={"force": True}, timeout=15)
            print(f"    ✅ post {pid} 삭제")
        except Exception as e:
            print(f"    ❌ post {pid} 실패: {e}")
        time.sleep(0.3)

    print("  미디어 삭제 중...")
    for mid in media_ids:
        try:
            scraper.delete(f"{WP_URL}/wp-json/wp/v2/media/{mid}", params={"force": True}, timeout=15)
            print(f"    ✅ media {mid} 삭제")
        except Exception as e:
            print(f"    ❌ media {mid} 실패: {e}")
        time.sleep(0.3)

    print(f"  ✅ 삭제 완료: 포스트 {len(post_ids)}개, 미디어 {len(media_ids)}개")
    return True


# ── 메인 ──────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--category", choices=list(CATEGORIES.keys()), help="특정 카테고리만 생성")
    parser.add_argument("--count", type=int, default=POSTS_PER_RUN, help="생성할 기사 수 (카테고리 1개 지정 시)")
    parser.add_argument("--per-category", type=int, default=0, help="전체 카테고리에 N개씩 생성")
    parser.add_argument("--delete-all", action="store_true", help="전체 포스트·미디어 삭제 후 종료")
    args = parser.parse_args()

    print("=" * 55)
    print("  WooriWin News 자동 기사 생성")
    print(f"  날짜: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    print("=" * 55)

    if not WP_USER or not WP_APP_PASSWORD:
        print("❌ WP_NET_USER / WP_NET_APP_PASSWORD 없음"); return

    # 전체 삭제 모드
    if args.delete_all:
        delete_all_posts()
        return

    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY 없음"); return

    client      = setup_gemini()
    used_topics = load_used_topics()

    print("\n📋 WP 카테고리 ID 조회 중...")
    cat_id_map = get_wp_category_ids()
    if not cat_id_map:
        print("❌ WP 카테고리 조회 실패 — 종료"); return
    print(f"  확인된 카테고리: {list(cat_id_map.keys())}")

    print("\n📰 기존 WP 포스트 제목 조회 중 (중복 방지)...")
    existing_titles = get_wp_post_titles()
    print(f"  기존 포스트: {len(existing_titles)}개")

    # 카테고리 목록 결정
    if args.per_category > 0:
        # 전체 카테고리에 N개씩
        sorted_cats = sorted(CATEGORIES.items(), key=lambda x: x[1]["priority"])
        target_cats = []
        for _ in range(args.per_category):
            target_cats.extend([c[0] for c in sorted_cats])
        print(f"\n🎯 전체 {len(CATEGORIES)}개 카테고리 × {args.per_category}개 = {len(target_cats)}개 예정")
    elif args.category:
        target_cats = [args.category] * args.count
    else:
        sorted_cats = sorted(CATEGORIES.items(), key=lambda x: x[1]["priority"])
        target_cats = [c[0] for c in sorted_cats[:args.count]]

    used_images = load_used_images()
    print(f"🖼️  기존 사용 이미지: {len(used_images)}개 (중복 방지)")
    success = 0

    for i, cat_slug in enumerate(target_cats):
        print(f"\n{'='*50}")
        cat = CATEGORIES[cat_slug]
        print(f"📌 [{i+1}/{len(target_cats)}] {cat['name']}")

        cat_id = cat_id_map.get(cat_slug)
        if not cat_id:
            print(f"  ⚠️ WP에 '{cat_slug}' 카테고리 없음 — 스킵")
            continue

        # 부모 카테고리 (해외 카지노)
        overseas_id = cat_id_map.get("overseas-casino")
        category_ids = [cat_id]
        if overseas_id and cat_slug in ["macau-casino", "philippines-casino",
                                         "vietnam-casino", "cambodia-casino"]:
            category_ids.append(overseas_id)

        # 주제 조합 선택
        keyword, angle, content_model = get_next_topic(cat_slug, used_topics)
        tone          = random.choice(TONES)
        intro_type    = random.choice(INTRO_TYPES)
        ending_type   = random.choice(ENDING_TYPES)
        length_option = random.choice(LENGTH_OPTIONS)

        print(f"   키워드: {keyword} | 앵글: {angle} | 모델: {content_model}")
        print(f"   문체: {tone[:15]}... | 길이: {length_option['label']} ({length_option['min']}자+)")

        # Step 1 — 제목 생성
        print("  🔍 제목 생성 중...")
        title = generate_unique_title(
            client, cat_slug, keyword, angle, content_model, existing_titles
        )
        print(f"  ⏳ RPM 대기 (4s)...")
        time.sleep(4)

        # Step 2 — 본문 생성
        print("  🤖 Gemini 본문 생성 중...")
        article = generate_article(
            client, title, cat_slug, keyword, angle, content_model,
            tone, intro_type, ending_type, length_option,
        )
        if not article:
            print("  ❌ 생성 실패 — 스킵")
            time.sleep(4)
            continue

        slug    = article.get("slug", f"{cat['slug_prefix']}-{int(time.time())}")
        excerpt = article.get("excerpt", "")
        faq     = article.get("faq", [])

        # Step 3 — 이미지
        pexels_queries   = cat.get("pexels_queries", ["casino resort"])
        gemini_query     = article.get("pexels_query", "")
        queries          = ([gemini_query] if gemini_query else []) + pexels_queries
        inline_queries   = pexels_queries[::-1] + ([gemini_query] if gemini_query else [])

        print("  📸 대표 이미지 검색 중...")
        image_url = fetch_pexels_image(queries, used_images)
        used_images.add(image_url)

        print("  📸 본문 삽입 이미지 검색 중...")
        inline_image_url = fetch_pexels_image(inline_queries, used_images)
        used_images.add(inline_image_url)

        image_alt = article.get("imageAlt", title)

        print("  ⬆️ WP 미디어 업로드 중...")
        media_id = upload_image_to_wp(image_url, image_alt)

        # Step 4 — HTML 조립
        content_html = markdown_to_html(article.get("content", ""))
        content_html = insert_inline_image_html(content_html, inline_image_url, image_alt)
        faq_html     = build_faq_html(faq)
        faq_jsonld   = build_jsonld_faq(faq)
        full_html    = content_html + faq_html
        print(f"  📋 FAQ: {len(faq)}개 {'→ 메타 저장' if faq_jsonld else '→ 없음(스킵)'}")

        # Step 5 — WP 포스팅
        print(f"  📤 WP 포스팅: {title}")
        result = post_to_wordpress(
            title         = title,
            content       = full_html,
            excerpt       = excerpt,
            slug          = slug,
            category_ids  = category_ids,
            keyword       = keyword,
            media_id      = media_id,
            category_name = cat["name"],
            author_id     = CATEGORY_AUTHORS.get(cat_slug),
            faq_jsonld    = faq_jsonld,
        )

        if result:
            success += 1
            existing_titles.append(title)
            save_used_topics(used_topics)
            save_used_images(used_images)
            print(f"  💾 used-topics.json 업데이트: [{cat_slug}] {keyword}|{angle}|{content_model}")

        if i < len(target_cats) - 1:
            print(f"  ⏳ 다음 포스트 대기 (10s)...")
            time.sleep(10)

    print(f"\n{'='*55}")
    print(f"  완료: {success}/{len(target_cats)}개 포스팅")
    print(f"{'='*55}")


if __name__ == "__main__":
    main()
