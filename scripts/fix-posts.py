#!/usr/bin/env python3
"""
scripts/fix-posts.py
기존 블로그 포스트 일괄 품질 수정 스크립트

수정 대상:
  Type A — 제목에 날짜(MM월 DD일) 포함 (~61개)
            → 제목 + 본문 + description + FAQ + keywords 전면 재생성
  Type B — 제목은 정상이나 제목-본문 불일치 의심 (~12개)
            → 본문 + description + FAQ + keywords 재생성 (제목·슬러그 유지)

유지 항목: slug(URL), date, category, image, author
실행법:
  python scripts/fix-posts.py            # 전체 수정
  python scripts/fix-posts.py --dry-run  # 대상 목록만 출력
  python scripts/fix-posts.py --resume   # 중단 이후 이어서 (체크포인트 활용)
"""

import os, sys, re, json, time, random, argparse
from datetime import datetime, timedelta, timezone
from pathlib import Path
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))
from google import genai

# ── API 키 ────────────────────────────────────────────────
GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

# ── 경로 ─────────────────────────────────────────────────
BASE_DIR       = Path(__file__).parent.parent
POSTS_DIR      = BASE_DIR / "data" / "posts"
CHECKPOINT_FILE = Path(__file__).parent / ".fix-posts-progress.json"

# ── 진행 속도 (API 레이트리밋 방지) ──────────────────────
SLEEP_BETWEEN_POSTS = 4   # 포스트 사이 대기 (초)
SLEEP_AFTER_TITLE   = 2   # 제목 생성 후 대기 (초)

# ─────────────────────────────────────────────────────────
# 공유 상수 (generate-post.py와 동일)
# ─────────────────────────────────────────────────────────
RESPONSIBLE_GAMBLING_TEXT = """

---

> ⚠️ **책임감 있는 게임 안내**
> 에볼루션카지노는 만 19세 이상 성인만 이용 가능합니다.
> 과도한 도박은 개인과 가정에 심각한 피해를 줄 수 있습니다.
> 도박 문제로 어려움을 겪고 계신다면 **한국도박문제예방치유원 ☎ 1336** (24시간 무료상담)에 연락하세요.
> 온라인 상담: [kcgp.or.kr](https://kcgp.or.kr)
"""

CATEGORY_TO_PAGE = {
    "에볼루션 가이드":   {"slug": "live-casino",        "anchor": "에볼루션 라이브카지노 완벽 가이드"},
    "바카라 가이드":     {"slug": "baccarat",           "anchor": "에볼루션카지노 바카라 완벽 가이드"},
    "블랙잭 가이드":     {"slug": "blackjack",          "anchor": "에볼루션카지노 블랙잭 완벽 가이드"},
    "게임쇼 분석":       {"slug": "slots",              "anchor": "에볼루션카지노 슬롯 완벽 가이드"},
    "룰렛 & 포커":       {"slug": "roulette",           "anchor": "에볼루션카지노 룰렛 완벽 가이드"},
    "최신 트렌드":       {"slug": "live-casino",        "anchor": "에볼루션 라이브카지노 완벽 가이드"},
    "자금 관리":         {"slug": "responsible-gaming", "anchor": "책임감 있는 게임 가이드"},
    "보안 및 라이선스":  {"slug": "about",              "anchor": "WOORIWIN 소개"},
    "모바일 최적화":     {"slug": "live-casino",        "anchor": "에볼루션 라이브카지노 완벽 가이드"},
    "책임감 있는 게임":  {"slug": "responsible-gaming", "anchor": "책임감 있는 게임 가이드"},
}

CATEGORIES = {
    "에볼루션 가이드":   {"pexels_queries": ["live casino studio", "casino platform interface"],     "slug_prefix": "live-casino"},
    "바카라 가이드":     {"pexels_queries": ["baccarat casino table", "live baccarat dealer"],       "slug_prefix": "baccarat"},
    "블랙잭 가이드":     {"pexels_queries": ["blackjack casino table", "live blackjack dealer"],     "slug_prefix": "blackjack"},
    "게임쇼 분석":       {"pexels_queries": ["casino game show wheel", "live game show"],            "slug_prefix": "game-show"},
    "룰렛 & 포커":       {"pexels_queries": ["roulette wheel casino", "live roulette dealer"],       "slug_prefix": "roulette"},
    "최신 트렌드":       {"pexels_queries": ["casino innovation 2026", "casino technology"],         "slug_prefix": "casino-trends"},
    "자금 관리":         {"pexels_queries": ["casino budget management", "bankroll management"],     "slug_prefix": "bankroll"},
    "보안 및 라이선스":  {"pexels_queries": ["casino license security", "online security casino"],  "slug_prefix": "casino-safety"},
    "모바일 최적화":     {"pexels_queries": ["mobile casino smartphone", "smartphone gaming"],       "slug_prefix": "mobile-casino"},
    "책임감 있는 게임":  {"pexels_queries": ["responsible gambling", "casino healthy gaming"],       "slug_prefix": "responsible-gambling"},
}

CATEGORY_TITLE_KEYWORDS = {
    "에볼루션 가이드":   ["에볼루션게이밍", "에볼루션 게이밍", "Evolution Gaming", "에볼루션카지노", "라이브카지노"],
    "바카라 가이드":     ["에볼루션바카라", "에볼루션 바카라", "바카라", "라이브바카라"],
    "블랙잭 가이드":     ["에볼루션블랙잭", "에볼루션 블랙잭", "블랙잭", "라이브블랙잭"],
    "게임쇼 분석":       ["크레이지타임", "모노폴리라이브", "라이브게임쇼", "드림캐처"],
    "룰렛 & 포커":       ["라이트닝룰렛", "라이트닝 룰렛", "룰렛", "라이브룰렛"],
    "최신 트렌드":       ["에볼루션게이밍", "라이브카지노", "온라인카지노", "카지노 트렌드"],
    "자금 관리":         ["카지노 자금관리", "뱅크롤", "베팅 전략", "손실 관리"],
    "보안 및 라이선스":  ["카지노 보안", "라이선스 카지노", "안전한 카지노", "MGA 라이선스"],
    "모바일 최적화":     ["모바일카지노", "모바일 카지노", "스마트폰 카지노"],
    "책임감 있는 게임":  ["도박 중독 예방", "안전한 게임", "카지노 자기제한"],
}

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
- 검증 불가능한 전문가 경력·현장 경험 설정 금지
- 본문에 'YMYL', 'E-E-A-T', 'EEAT', 'SEO' 같은 용어 직접 노출 금지

━━━ 올바른 표현 기준 ━━━
- RTP·하우스 엣지 수치는 사실로 제시하되 베팅 유도 없이 서술
- 전략 설명 시 '고려할 수 있습니다', '참고할 수 있습니다' 등 중립 표현 사용
- 게임 선택은 플레이어 본인의 판단임을 항상 명시
- RTP 수치 언급 시 '이론적 기댓값이며 실제 결과와 다를 수 있습니다' 병기
- 출처 명시: 'Evolution Gaming 공식 게임 수학 문서 기준'

━━━ 필수 포함 요소 ━━━
- 손실 위험 안내 문구 본문 내 1회 이상 포함
- eCOGRA 등 공인 감사기관 언급으로 신뢰도 강화
- 마크다운 표 1개 이상
- 본문 최소 1600자 이상

━━━ 콘텐츠 관점 ━━━
제목이 암시하는 주제를 본문이 실제로 다루도록 작성하고,
사실 기반 정보와 사용자 편의 중심의 중립적·설명형 문체를 유지합니다.
"""

# ─────────────────────────────────────────────────────────
# 유틸리티
# ─────────────────────────────────────────────────────────

def setup_gemini() -> genai.Client:
    return genai.Client(api_key=GEMINI_API_KEY)


def clean_json_response(text: str) -> str:
    text = text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    return text.strip()


def safe_generate(client: genai.Client, prompt: str, retries: int = 3):
    for attempt in range(retries + 1):
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt if attempt == 0 else prompt + f"\n\n[재시도 {attempt}회차: 반드시 유효한 JSON만 출력]",
                config={"system_instruction": SYSTEM_INSTRUCTION},
            )
            return json.loads(clean_json_response(response.text))
        except json.JSONDecodeError as e:
            if attempt < retries:
                print(f"    ⚠️  JSON 파싱 실패({e}), 재시도 {attempt+1}/{retries}...")
                time.sleep(3)
            else:
                print(f"    ❌ JSON 파싱 최종 실패 — 스킵")
                return None
        except Exception as e:
            if attempt < retries:
                print(f"    ⚠️  생성 실패({e}), 재시도 {attempt+1}/{retries}...")
                time.sleep(5)
            else:
                print(f"    ❌ 생성 최종 실패 — 스킵")
                return None


def get_content_angle(title: str) -> str:
    if any(k in title for k in ["전략", "공략법", "필승", "노하우", "팁"]):
        return (
            "제목이 '전략/공략/팁'을 약속했으므로, 베팅 라운드를 진행하며 고려할 수 있는 "
            "판단 기준·체크포인트·흐름 읽는 법 등 '의사결정에 실질적으로 도움이 되는 내용'을 "
            "중심으로 작성 (단순 화면·환경 설정 안내로 대체하지 말 것)"
        )
    if any(k in title for k in ["가이드", "방법", "안내", "이용", "설치"]):
        return "제목이 '가이드/방법'을 약속했으므로, 절차를 단계별로 안내하고 실용적인 정보 전달을 중심으로 작성"
    if any(k in title for k in ["분석", "비교", "특징", "구성", "탐색"]):
        return "제목이 '분석/비교'를 약속했으므로, 구체적인 기준으로 비교하고 차이점을 짚어주는 내용을 중심으로 작성"
    if any(k in title for k in ["트렌드", "인사이트", "소식", "이슈", "전망"]):
        return "제목이 '트렌드/인사이트'를 약속했으므로, 최근 변화나 흐름과 그것이 플레이어에게 갖는 의미를 중심으로 작성"
    if any(k in title for k in ["규칙", "룰", "방식", "메커니즘"]):
        return "제목이 '규칙/방식'을 약속했으므로, 게임 진행 방식과 핵심 규칙을 정확하고 이해하기 쉽게 설명하는 내용을 중심으로 작성"
    return "제목이 독자에게 암시하는 핵심 주제를 정확히 파악하여, 그 주제에서 벗어나지 않는 내용을 중심으로 작성"


def insert_inline_image(content: str, image_url: str, alt_text: str) -> str:
    if not image_url:
        return content
    headers = [m.start() for m in re.finditer(r"^## ", content, re.MULTILINE)]
    if len(headers) >= 3:
        pos = headers[2]
        return content[:pos] + f"![{alt_text}]({image_url})\n\n" + content[pos:]
    return content


def load_checkpoint() -> set:
    if CHECKPOINT_FILE.exists():
        with open(CHECKPOINT_FILE, "r", encoding="utf-8") as f:
            return set(json.load(f).get("done", []))
    return set()


def save_checkpoint(done: set):
    with open(CHECKPOINT_FILE, "w", encoding="utf-8") as f:
        json.dump({"done": sorted(done), "updated_at": datetime.now().isoformat()}, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────────────
# 포스트 분류
# ─────────────────────────────────────────────────────────

def has_date_in_title(title: str) -> bool:
    return bool(re.search(r'\d{1,2}월\s*\d{1,2}일', title))


def extract_keyword_from_date_title(title: str) -> str:
    """'에볼루션카지노 세션 관리 05월 19일 인사이트' → '세션 관리'"""
    m = re.search(r'(?:에볼루션카지노|에볼루션|카지노)\s+(.+?)\s+\d{1,2}월', title)
    if m:
        return m.group(1).strip()
    # fallback: 날짜·공통어 제거
    cleaned = re.sub(r'\d{1,2}월\s*\d{1,2}일', '', title)
    cleaned = re.sub(r'에볼루션카지노|에볼루션|카지노|인사이트|가이드', '', cleaned)
    return cleaned.strip() or "라이브카지노"


UX_KEYWORDS   = {'인터페이스', 'UI', 'UX', '화면', '설정', '탐색', '레이아웃'}
INTENT_KEYWORDS = {'전략', '공략', '필승', '노하우', '팁', '규칙', '룰', '확률', '배당'}

def is_content_mismatch(title: str, content: str) -> bool:
    has_intent = any(k in title for k in INTENT_KEYWORDS)
    ux_count   = sum(content[:1200].count(k) for k in UX_KEYWORDS)
    return has_intent and ux_count >= 3


def classify_posts() -> tuple[list, list, list]:
    """(type_a_date, type_b_mismatch, type_ok) 분류"""
    type_a, type_b, type_ok = [], [], []
    for fp in sorted(POSTS_DIR.glob("*.json")):
        with open(fp, "r", encoding="utf-8") as f:
            post = json.load(f)
        title   = post.get("title", "")
        content = post.get("content", "")
        if has_date_in_title(title):
            type_a.append(post)
        elif is_content_mismatch(title, content):
            type_b.append(post)
        else:
            type_ok.append(post)
    return type_a, type_b, type_ok


# ─────────────────────────────────────────────────────────
# 제목 생성 (Type A 전용)
# ─────────────────────────────────────────────────────────

def generate_new_title(client: genai.Client, category: str, keyword: str,
                       existing_titles: list) -> str:
    title_kw = random.choice(CATEGORY_TITLE_KEYWORDS.get(category, ["에볼루션카지노"]))
    existing_sample = "\n".join(f"- {t}" for t in existing_titles[-30:]) or "없음"

    prompt = f"""
다음 조건으로 한국인 독자에게 매력적인 블로그 제목 3개를 생성하세요.

카테고리: {category}
핵심 키워드: {keyword}
반드시 포함할 브랜드/게임 키워드: {title_kw}

조건:
- 정보형·가이드형 톤 유지
- 수치 보장·승률 예측·날짜 포함 절대 금지
- "에볼루션카지노"를 항상 제목 맨 앞에 쓰는 패턴 금지
- 25~45자 사이
- 각 제목은 서로 다른 앵글로 작성

⚠️ 아래 기존 제목들과 핵심 단어 3개 이상 겹치는 제목 금지:
{existing_sample}

출력: JSON 배열만 (코드블록 없이)
예시: ["제목1", "제목2", "제목3"]
"""
    result = safe_generate(client, prompt, retries=2)
    if isinstance(result, list) and result:
        # 가능하면 중복 없는 것 선택
        for t in result:
            kw_new = set(re.findall(r'[가-힣]{2,}', t))
            dupe = False
            for old in existing_titles[-40:]:
                kw_old = set(re.findall(r'[가-힣]{2,}', old))
                if len(kw_new & kw_old) >= 3:
                    dupe = True
                    break
            if not dupe:
                return t
        return result[0]  # 모두 중복이면 첫 번째라도 사용
    return f"{keyword} 에볼루션카지노 완벽 가이드"


# ─────────────────────────────────────────────────────────
# 본문 생성
# ─────────────────────────────────────────────────────────

def generate_content(client: genai.Client, title: str, category: str,
                     keyword: str) -> dict | None:
    cat_data    = CATEGORIES.get(category, {})
    pexels_hint = ", ".join(cat_data.get("pexels_queries", ["casino live"])[:2])
    slug_prefix = cat_data.get("slug_prefix", "casino")

    prompt = f"""
글 제목: {title}
카테고리: {category}
핵심 키워드: {keyword}
참고 이미지 키워드(영문): {pexels_hint}

작성 규칙:
1. 본문은 최소 1600자 이상
2. H2 헤더(##)를 4~6개 포함
3. [본문 핵심 관점 — 반드시 준수] {get_content_angle(title)}
   ⚠️ 제목이 약속한 주제를 본문이 충족하는 것이 최우선 (인터페이스 안내로 대체 금지)
4. 본문 중간에 마크다운 표(|컬럼|컬럼|) 최소 1개 포함
5. FAQ 5개 포함 (초보자 관점 질문 위주)
6. RTP 수치 언급 시 반드시 '이론적 기댓값, 실제 결과와 다를 수 있음' 병기
7. 손실 위험 안내 문구 1회 이상 포함
8. eCOGRA 등 공인 감사기관 언급
9. 출처 명시: 'Evolution Gaming 공식 게임 수학 문서 기준' 1회 이상

[절대 금지]
- 특정 베팅 권장·유도 표현
- '무조건', '절대', '반드시' 등 단정적 지시
- 손익 보장 표현, 과장된 당첨 기대 표현
- 본문에 YMYL, E-E-A-T, SEO 등 메타 용어 직접 노출

다음 JSON 형식으로만 응답 (마크다운 코드블록 없이 순수 JSON만):
{{
  "description": "포스트 설명 (150자 이내, 키워드 자연스럽게 포함)",
  "keywords": ["키워드1", "키워드2", "키워드3", "키워드4", "키워드5"],
  "imageAlt": "이미지 설명 (50자 이내)",
  "content": "본문 내용 (마크다운, 1600자 이상, 표 포함)",
  "faq": [
    {{"q": "질문1", "a": "답변1"}},
    {{"q": "질문2", "a": "답변2"}},
    {{"q": "질문3", "a": "답변3"}},
    {{"q": "질문4", "a": "답변4"}},
    {{"q": "질문5", "a": "답변5"}}
  ]
}}
"""
    return safe_generate(client, prompt, retries=2)


# ─────────────────────────────────────────────────────────
# 포스트 업데이트 저장
# ─────────────────────────────────────────────────────────

def update_post_file(original: dict, new_title: str, content_data: dict):
    slug     = original["slug"]
    category = original["category"]
    image    = original.get("image", "")
    date     = original.get("date", "")
    author   = original.get("author", {})

    # 본문 후처리: 내부 링크 + 책임도박 문구
    content = content_data["content"]
    internal_link = CATEGORY_TO_PAGE.get(category)
    if internal_link:
        link_md = (
            f"\n\n## 함께 보면 좋은 글\n\n"
            f"해당 주제에 대한 더 자세한 정보는 "
            f"**[{internal_link['anchor']}](https://wooriwin.com/{internal_link['slug']})** "
            f"페이지에서 확인하실 수 있습니다.\n"
        )
        content += link_md
    content += RESPONSIBLE_GAMBLING_TEXT

    post = {
        "slug":        slug,
        "title":       new_title,
        "description": content_data["description"],
        "category":    category,
        "date":        date,
        "updatedAt":   datetime.now(timezone(timedelta(hours=9))).strftime("%Y-%m-%d"),
        "readTime":    f"{max(5, len(content_data['content']) // 300)}분",
        "keywords":    content_data.get("keywords", []),
        "image":       image,
        "imageAlt":    content_data.get("imageAlt", new_title),
        "content":     content,
        "faq":         content_data.get("faq", []),
        "author":      author,
    }

    filepath = POSTS_DIR / f"{slug}.json"
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(post, f, ensure_ascii=False, indent=2)
    print(f"    ✅ 저장 완료: {slug}.json")


# ─────────────────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="기존 포스트 품질 수정")
    parser.add_argument("--dry-run", action="store_true", help="수정 대상 목록만 출력")
    parser.add_argument("--resume",  action="store_true", help="체크포인트 이어서 실행")
    parser.add_argument("--type",    choices=["A", "B", "all"], default="all",
                        help="A=날짜제목만, B=불일치만, all=전체")
    args = parser.parse_args()

    print("=" * 60)
    print("  WOORIWIN 기존 포스트 품질 수정 스크립트")
    print(f"  실행: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print("=" * 60)

    # ── 분류 ──────────────────────────────────────────
    type_a, type_b, type_ok = classify_posts()
    print(f"\n📊 분류 결과:")
    print(f"   Type A (날짜 제목):       {len(type_a):3d}개  → 제목+본문+description 재생성")
    print(f"   Type B (제목-본문 불일치): {len(type_b):3d}개  → 본문+description 재생성")
    print(f"   정상 포스트:              {len(type_ok):3d}개  → 수정 없음")

    targets = []
    if args.type in ("A", "all"):
        targets += [("A", p) for p in type_a]
    if args.type in ("B", "all"):
        targets += [("B", p) for p in type_b]

    print(f"\n🎯 이번 실행 수정 대상: {len(targets)}개\n")

    if args.dry_run:
        print("─── DRY RUN 목록 ──────────────────────────────────")
        for fix_type, post in targets:
            print(f"  [{fix_type}] {post['slug']}")
            print(f"       현재 제목: {post['title']}")
        print("─── DRY RUN 종료 ──────────────────────────────────")
        return

    if not GEMINI_API_KEY:
        print("❌ GEMINI_API_KEY 없음 — .env.local 확인")
        sys.exit(1)

    # ── 체크포인트 로드 ────────────────────────────────
    done_slugs = load_checkpoint() if args.resume else set()
    if done_slugs:
        print(f"▶️  체크포인트: {len(done_slugs)}개 이미 완료 → 스킵")

    client = setup_gemini()

    # 기존 제목 목록 (중복 방지용)
    all_titles = [p.get("title", "") for _, p in targets] + \
                 [p.get("title", "") for p in type_ok]

    success = 0
    fail    = 0
    skipped = 0

    for idx, (fix_type, post) in enumerate(targets, 1):
        slug = post["slug"]
        old_title = post["title"]

        print(f"\n[{idx}/{len(targets)}] {fix_type} — {slug}")
        print(f"  기존 제목: {old_title}")

        # 체크포인트 스킵
        if slug in done_slugs:
            print(f"  ⏭️  이미 완료 → 스킵")
            skipped += 1
            continue

        try:
            category = post.get("category", "에볼루션 가이드")

            # ── Type A: 날짜 제목 → 새 제목 생성 ─────────
            if fix_type == "A":
                keyword = extract_keyword_from_date_title(old_title)
                print(f"  📌 추출 키워드: '{keyword}'")
                time.sleep(SLEEP_AFTER_TITLE)
                new_title = generate_new_title(client, category, keyword, all_titles)
                print(f"  ✨ 새 제목: '{new_title}'")
                all_titles.append(new_title)
            else:
                # Type B: 기존 제목 유지
                new_title = old_title
                keyword   = re.sub(r'에볼루션카지노|에볼루션|카지노', '', old_title).strip()

            print(f"  📝 본문 생성 중...")
            time.sleep(SLEEP_AFTER_TITLE)
            content_data = generate_content(client, new_title, category, keyword)

            if not content_data:
                print(f"  ❌ 본문 생성 실패 — 스킵")
                fail += 1
                continue

            # ── 저장 ──────────────────────────────────────
            update_post_file(post, new_title, content_data)
            done_slugs.add(slug)
            save_checkpoint(done_slugs)
            success += 1

            print(f"  🕐 {SLEEP_BETWEEN_POSTS}초 대기...")
            time.sleep(SLEEP_BETWEEN_POSTS)

        except KeyboardInterrupt:
            print("\n\n⚠️  중단됨 — 체크포인트 저장 완료. --resume 으로 이어서 실행 가능")
            save_checkpoint(done_slugs)
            break
        except Exception as e:
            print(f"  ❌ 예외 발생: {e}")
            fail += 1
            time.sleep(3)

    # ── 결과 요약 ──────────────────────────────────────
    print("\n" + "=" * 60)
    print(f"  완료: {success}개  실패: {fail}개  스킵: {skipped}개")
    print(f"  체크포인트: {CHECKPOINT_FILE}")
    print("=" * 60)

    if success > 0:
        print("\n📌 다음 단계:")
        print("  git add data/posts/")
        print("  git commit -m 'fix: 기존 포스트 품질 수정 (날짜제목+내용불일치 재생성)'")
        print("  git push origin <branch>:main")


if __name__ == "__main__":
    main()
