"""
기존 data/posts/*.json 일괄 검수/수정 스크립트
- 중복 title 자동 수정 (Gemini로 새 제목 생성)
- 카테고리 → 게임 페이지 내부 링크 자동 추가
- relatedPosts 필드 제거 (page.tsx에서 동적 처리)

사용법:
    python scripts/fix-existing-posts.py
"""
import os
import re
import json
import time
import random
from dotenv import load_dotenv
load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
BASE_DIR  = os.path.join(os.path.dirname(__file__), "..")
POSTS_DIR = os.path.join(BASE_DIR, "data", "posts")

# ── 카테고리 → 게임 페이지 매핑 ─────────────────
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

# ── 카테고리별 슬러그 prefix 매핑 ────────────────
CATEGORY_SLUG_PREFIX = {
    "에볼루션 가이드":  "live-casino",
    "바카라 가이드":    "baccarat",
    "블랙잭 가이드":    "blackjack",
    "게임쇼 분석":      "game-show",
    "룰렛 & 포커":      "roulette",
    "최신 트렌드":      "casino-trends",
    "자금 관리":        "bankroll",
    "보안 및 라이선스": "casino-safety",
    "모바일 최적화":    "mobile-casino",
    "책임감 있는 게임": "responsible-gambling",
}

SLUG_SUFFIXES = ["guide", "tips", "review", "strategy", "explained", "overview", "how-to", "complete"]

BAD_SLUG_PATTERNS = ["evolution-casino", "interface", "-ux-", "-4-", "-2-", "-5-"]

STOP_WORDS = {
    "에볼루션카지노", "에볼루션", "카지노", "위한", "가이드", "이해", "활용",
    "방법", "설정", "분석", "관리", "최적화", "환경", "플레이", "라이브",
    "vs", "&", "·", "-", "—",
}

def extract_keywords(title: str) -> set:
    words = re.split(r'[\s:,()·\-—|]+', title)
    return {w for w in words if len(w) >= 2 and w not in STOP_WORDS}

def has_duplicate(new_title, existing_titles, threshold=3):
    new_words = extract_keywords(new_title)
    for old in existing_titles:
        old_words = extract_keywords(old)
        if len(new_words & old_words) >= threshold:
            return True
    return False

def clean_json_response(text):
    text = text.strip()
    if "```json" in text:
        text = text.split("```json")[1].split("```")[0]
    elif "```" in text:
        text = text.split("```")[1].split("```")[0]
    return text.strip()

def needs_slug_fix(slug: str) -> bool:
    """기존 패턴 슬러그인지 검사."""
    return any(pat in slug for pat in BAD_SLUG_PATTERNS)

def generate_new_slug(category: str, title: str, existing_slugs: set) -> str:
    """카테고리 prefix + 제목 키워드 기반 새 슬러그 생성."""
    prefix = CATEGORY_SLUG_PREFIX.get(category, "casino")
    suffix = random.choice(SLUG_SUFFIXES)
    # 제목에서 핵심 단어 추출 (영문 변환은 간단히 처리)
    keywords = extract_keywords(title)
    # 불용어 제거 후 2~3개 단어 선택
    kw_list = list(keywords)[:2]
    # 한글 → 간단 영문 매핑
    KO_EN = {
        "바카라": "baccarat", "블랙잭": "blackjack", "룰렛": "roulette",
        "슬롯": "slots", "포커": "poker", "게임쇼": "gameshow",
        "스피드": "speed", "라이트닝": "lightning", "인피니트": "infinite",
        "모바일": "mobile", "보안": "security", "자금": "bankroll",
        "전략": "strategy", "규칙": "rules", "가입": "signup",
        "인터페이스": "interface", "스트리밍": "streaming",
        "크레이지타임": "crazytime", "모노폴리": "monopoly",
    }
    en_parts = [KO_EN.get(k, "") for k in kw_list if KO_EN.get(k)]
    if en_parts:
        candidate = f"{prefix}-{'-'.join(en_parts)}-{suffix}"
    else:
        candidate = f"{prefix}-{suffix}-{random.randint(100, 999)}"
    # 중복 방지
    if candidate in existing_slugs:
        candidate = f"{candidate}-{random.randint(10, 99)}"
    return candidate


def generate_new_title(client, category, existing_titles):
    """기존 제목과 중복 안 되는 새 제목 생성."""
    existing_list = "\n".join(f"- {t}" for t in existing_titles[-20:])
    
    for attempt in range(3):
        prompt = f"""
다음 조건으로 한국인 독자에게 매력적인 블로그 제목 3개를 생성하세요.

카테고리: {category}

조건:
- "에볼루션카지노" 키워드 반드시 포함
- 정보형·가이드형 톤 유지
- 25~45자 사이
- 제목에 콜론(:) 사용 금지

⚠️ 아래 기존 제목들과 핵심 단어 3개 이상 겹치는 제목 금지:
{existing_list}

JSON 배열만 출력 (마크다운 없이):
["제목1", "제목2", "제목3"]
"""
        try:
            response = client.models.generate_content(
                model="gemini-3.1-flash-lite",
                contents=prompt,
            )
            titles = json.loads(clean_json_response(response.text))
            if isinstance(titles, list):
                for t in titles:
                    if not has_duplicate(t, existing_titles):
                        return t
        except Exception as e:
            print(f"  ⚠️ 시도 {attempt+1} 실패: {e}")
            time.sleep(2)
    return None

def already_has_internal_link(content):
    """내부 링크가 이미 있는지 검사."""
    return "wooriwin.com/" in content and "## 함께 보면 좋은 글" in content

def main():
    print("=" * 60)
    print("  기존 포스트 일괄 검수/수정")
    print("=" * 60)
    
    if not os.path.exists(POSTS_DIR):
        print("⚠️ data/posts/ 폴더가 없습니다. 종료.")
        return
    
    files = sorted([f for f in os.listdir(POSTS_DIR) if f.endswith(".json")])
    print(f"\n총 {len(files)}개 포스트 발견\n")
    
    # 모든 포스트 로드
    posts = []
    for f in files:
        with open(os.path.join(POSTS_DIR, f), encoding="utf-8") as fp:
            p = json.load(fp)
            p["_file"] = f
            posts.append(p)
    
    # 0단계 — 슬러그 패턴 교체
    print("=== 0단계: 슬러그 패턴 교체 ===")
    existing_slugs = {p["slug"] for p in posts}
    slug_map = {}  # 구 슬러그 → 새 슬러그 매핑

    for p in posts:
        old_slug = p["slug"]
        if needs_slug_fix(old_slug):
            new_slug = generate_new_slug(p["category"], p["title"], existing_slugs)
            slug_map[old_slug] = new_slug
            existing_slugs.discard(old_slug)
            existing_slugs.add(new_slug)
            p["slug"] = new_slug
            print(f"  🔄 {old_slug}")
            print(f"     → {new_slug}")
        else:
            print(f"  ✅ 유지: {old_slug}")

    print(f"\n슬러그 교체: {len(slug_map)}개\n")

    # 1단계 — 중복 title 검사
    print("=== 1단계: 중복 title 검사 ===")
    duplicates = []
    titles_seen = []
    for p in posts:
        if has_duplicate(p["title"], titles_seen):
            duplicates.append(p)
            print(f"  ⚠️ 중복: {p['_file']}")
            print(f"     '{p['title']}'")
        titles_seen.append(p["title"])
    
    print(f"\n중복 발견: {len(duplicates)}개\n")
    
    # 2단계 — 중복 title 수정
    if duplicates:
        print("=== 2단계: 중복 title 새로 생성 ===")
        client = genai.Client(api_key=GEMINI_API_KEY)
        
        # 중복 제외한 깨끗한 title 목록
        clean_titles = [p["title"] for p in posts if p not in duplicates]
        
        for p in duplicates:
            print(f"\n📝 수정 중: {p['_file']}")
            print(f"   기존: '{p['title']}'")
            new_title = generate_new_title(client, p["category"], clean_titles)
            if new_title:
                print(f"   신규: '{new_title}'")
                p["title"] = new_title
                clean_titles.append(new_title)
            else:
                # Fallback — 카테고리 + 타임스탬프
                from datetime import datetime
                p["title"] = f"에볼루션카지노 {p['category']} 심층 가이드 ({datetime.now().strftime('%m월')})"
                print(f"   Fallback: '{p['title']}'")
            time.sleep(1)
    
    # 3단계 — 내부 링크 추가 + relatedPosts 제거
    print("\n=== 3단계: 내부 링크 추가 + relatedPosts 제거 ===")
    for p in posts:
        modified = False
        
        # relatedPosts 제거
        if "relatedPosts" in p:
            del p["relatedPosts"]
            modified = True
            print(f"  🗑️  relatedPosts 제거: {p['_file']}")
        
        # 내부 링크 추가
        if not already_has_internal_link(p.get("content", "")):
            cat = p.get("category", "")
            link_info = CATEGORY_TO_PAGE.get(cat)
            if link_info:
                link_md = f"\n\n## 함께 보면 좋은 글\n\n해당 주제에 대한 더 자세한 정보는 **[{link_info['anchor']}](https://wooriwin.com/{link_info['slug']})** 페이지에서 확인하실 수 있습니다.\n"
                
                # "책임감 있는 게임 안내" 위에 삽입 (있으면)
                content = p["content"]
                marker = "\n---\n\n> ⚠️ **책임감 있는 게임 안내**"
                if marker in content:
                    content = content.replace(marker, link_md + marker)
                else:
                    content = content + link_md
                
                p["content"] = content
                modified = True
                print(f"  🔗 내부 링크 추가 ({cat} → /{link_info['slug']}): {p['_file']}")
    
    # 4단계 — 저장 (파일명도 새 슬러그로 변경)
    print("\n=== 4단계: 파일 저장 ===")
    for p in posts:
        old_file = p.pop("_file")
        new_file = f"{p['slug']}.json"
        # 구 파일 삭제
        old_path = os.path.join(POSTS_DIR, old_file)
        new_path = os.path.join(POSTS_DIR, new_file)
        if old_file != new_file and os.path.exists(old_path):
            os.remove(old_path)
            print(f"  🗑️  삭제: {old_file}")
        with open(new_path, "w", encoding="utf-8") as fp:
            json.dump(p, fp, ensure_ascii=False, indent=2)
        print(f"  ✅ 저장: {new_file}")
    
    print("\n" + "=" * 60)
    print(f"  완료! 총 {len(posts)}개 포스트 처리")
    print("=" * 60)

if __name__ == "__main__":
    main()
