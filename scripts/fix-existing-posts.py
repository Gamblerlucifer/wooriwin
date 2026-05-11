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
    
    # 4단계 — 저장
    print("\n=== 4단계: 파일 저장 ===")
    for p in posts:
        file = p.pop("_file")
        with open(os.path.join(POSTS_DIR, file), "w", encoding="utf-8") as fp:
            json.dump(p, fp, ensure_ascii=False, indent=2)
        print(f"  ✅ 저장: {file}")
    
    print("\n" + "=" * 60)
    print(f"  완료! 총 {len(posts)}개 포스트 처리")
    print("=" * 60)

if __name__ == "__main__":
    main()
