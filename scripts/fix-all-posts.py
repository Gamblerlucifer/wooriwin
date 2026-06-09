"""
fix-all-posts.py
────────────────
기존 전체 포스트를 새 파이프라인으로 재생성합니다.

유지: date, category, author, image
교체: title, slug, content, description, keywords, faq

실행:
  python scripts/fix-all-posts.py
  python scripts/fix-all-posts.py --dry-run
  python scripts/fix-all-posts.py --resume
  python scripts/fix-all-posts.py --limit 10
"""

import os
import re
import sys
import json
import time
import random
import argparse
import requests
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), '..', '.env.local'))

from datetime import datetime, timezone, timedelta
from google import genai

# ── generate-post.py 의 상수·함수 재사용 ────────────
sys.path.insert(0, os.path.dirname(__file__))
import importlib.util, types

def _load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    mod  = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod

_gp = _load("generate_post", os.path.join(os.path.dirname(__file__), "generate-post.py"))

from types import SimpleNamespace
(
    CATEGORIES, ANGLES, CONTENT_MODELS, TONES,
    INTRO_TYPES, ENDING_TYPES, LENGTH_OPTIONS,
    CATEGORY_TITLE_KEYWORDS, RESPONSIBLE_GAMBLING_TEXT,
    CATEGORY_TO_PAGE, SYSTEM_INSTRUCTION,
    setup_gemini, clean_json_response,
    safe_generate_content, is_duplicate_title,
    generate_unique_title, generate_post_content,
    get_next_topic, load_used_topics, save_used_topics,
    ensure_unique_slug, fetch_pexels_image, insert_inline_image,
    USED_TOPICS_FILE,
) = (
    getattr(_gp, x) for x in [
        "CATEGORIES", "ANGLES", "CONTENT_MODELS", "TONES",
        "INTRO_TYPES", "ENDING_TYPES", "LENGTH_OPTIONS",
        "CATEGORY_TITLE_KEYWORDS", "RESPONSIBLE_GAMBLING_TEXT",
        "CATEGORY_TO_PAGE", "SYSTEM_INSTRUCTION",
        "setup_gemini", "clean_json_response",
        "safe_generate_content", "is_duplicate_title",
        "generate_unique_title", "generate_post_content",
        "get_next_topic", "load_used_topics", "save_used_topics",
        "ensure_unique_slug", "fetch_pexels_image", "insert_inline_image",
        "USED_TOPICS_FILE",
    ]
)


# ── 경로 ──────────────────────────────────────────
BASE_DIR    = os.path.join(os.path.dirname(__file__), "..")
POSTS_DIR   = os.path.join(BASE_DIR, "data", "posts")
PROGRESS_FILE = os.path.join(BASE_DIR, "data", ".fix-all-progress.json")

SLEEP_BETWEEN = int(os.environ.get("SLEEP_BETWEEN_POSTS", "5"))

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")
PEXELS_API_KEY = os.environ.get("PEXELS_API_KEY", "")


# ─────────────────────────────────────────────────
# 진행 체크포인트
# ─────────────────────────────────────────────────

def load_progress() -> set:
    if os.path.exists(PROGRESS_FILE):
        try:
            with open(PROGRESS_FILE, encoding="utf-8") as f:
                return set(json.load(f).get("done", []))
        except Exception:
            pass
    return set()


def save_progress(done: set) -> None:
    os.makedirs(os.path.dirname(PROGRESS_FILE), exist_ok=True)
    with open(PROGRESS_FILE, "w", encoding="utf-8") as f:
        json.dump({"done": list(done)}, f, ensure_ascii=False, indent=2)


# ─────────────────────────────────────────────────
# 기존 포스트 로드
# ─────────────────────────────────────────────────

def load_all_posts() -> list:
    """data/posts/*.json 전체 로드. category 있는 것만 반환."""
    posts = []
    if not os.path.exists(POSTS_DIR):
        return posts
    for fname in sorted(os.listdir(POSTS_DIR)):
        if not fname.endswith(".json"):
            continue
        fpath = os.path.join(POSTS_DIR, fname)
        try:
            with open(fpath, encoding="utf-8") as f:
                data = json.load(f)
            if data.get("category") in CATEGORIES:
                posts.append({"file": fname, "path": fpath, "data": data})
        except Exception as e:
            print(f"  ⚠️ 로드 실패: {fname} — {e}")
    return posts


# ─────────────────────────────────────────────────
# 이미지 유틸
# ─────────────────────────────────────────────────

def get_all_used_images(exclude_slug: str = "") -> set:
    used = set()
    if not os.path.exists(POSTS_DIR):
        return used
    for fname in os.listdir(POSTS_DIR):
        if not fname.endswith(".json"):
            continue
        slug = fname.replace(".json", "")
        if slug == exclude_slug:
            continue
        try:
            with open(os.path.join(POSTS_DIR, fname), encoding="utf-8") as f:
                d = json.load(f)
            if d.get("image"):
                used.add(d["image"])
        except Exception:
            pass
    return used


# ─────────────────────────────────────────────────
# 포스트 저장 (새 슬러그로 저장 + 기존 파일 삭제)
# ─────────────────────────────────────────────────

def save_new_post(
    new_slug: str,
    old_slug: str,
    content_data: dict,
    image_url: str,
    category: str,
    date: str,
    author: dict,
    inline_image_url: str = None,
    inline_image_alt: str = None,
) -> None:
    content = content_data["content"]
    if inline_image_url:
        content = insert_inline_image(
            content, inline_image_url,
            inline_image_alt or content_data["title"]
        )

    # 내부 링크 삽입
    internal_link = CATEGORY_TO_PAGE.get(category)
    if internal_link:
        link_md = (
            f"\n\n## 함께 보면 좋은 글\n\n"
            f"해당 주제에 대한 더 자세한 정보는 "
            f"**[{internal_link['anchor']}](https://wooriwin.com/{internal_link['slug']})** "
            f"페이지에서 확인하실 수 있습니다.\n"
        )
        content += link_md

    content_with_eeat = content + RESPONSIBLE_GAMBLING_TEXT

    post = {
        "slug":        new_slug,
        "title":       content_data["title"],
        "description": content_data["description"],
        "category":    category,
        "date":        date,
        "readTime":    f"{max(5, len(content_data['content']) // 300)}분",
        "keywords":    content_data.get("keywords", []),
        "image":       image_url,
        "imageAlt":    content_data.get("imageAlt", content_data["title"]),
        "content":     content_with_eeat,
        "faq":         content_data.get("faq", []),
        "author":      author,
    }

    # 새 파일 저장
    new_path = os.path.join(POSTS_DIR, f"{new_slug}.json")
    with open(new_path, "w", encoding="utf-8") as f:
        json.dump(post, f, ensure_ascii=False, indent=2)
    print(f"  ✅ 새 파일 저장: {new_slug}.json")

    # 기존 파일 삭제 (슬러그가 바뀐 경우만)
    if old_slug != new_slug:
        old_path = os.path.join(POSTS_DIR, f"{old_slug}.json")
        if os.path.exists(old_path):
            os.remove(old_path)
            print(f"  🗑️  기존 파일 삭제: {old_slug}.json")


# ─────────────────────────────────────────────────
# 메인
# ─────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="전체 포스트 새 파이프라인으로 재생성")
    parser.add_argument("--dry-run", action="store_true", help="대상 목록만 출력, 실제 수정 없음")
    parser.add_argument("--resume",  action="store_true", help="이전 진행 이어서 실행")
    parser.add_argument("--limit",   type=int, default=0, help="처리할 최대 포스트 수 (0=전체)")
    args = parser.parse_args()

    print("=" * 60)
    print("  WOORIWIN 전체 포스트 재생성 (새 파이프라인 적용)")
    print(f"  날짜: {datetime.now().strftime('%Y-%m-%d %H:%M')}")
    if args.dry_run: print("  [DRY-RUN 모드]")
    if args.resume:  print("  [RESUME 모드]")
    print("=" * 60)

    all_posts = load_all_posts()
    done_slugs = load_progress() if args.resume else set()

    # 미처리 포스트만 필터
    pending = [p for p in all_posts if p["data"]["slug"] not in done_slugs]
    if args.limit > 0:
        pending = pending[:args.limit]

    print(f"\n📊 전체: {len(all_posts)}개 | 완료: {len(done_slugs)}개 | 처리 예정: {len(pending)}개\n")

    if args.dry_run:
        for p in pending:
            d = p["data"]
            print(f"  [{d.get('category','?')}] {d.get('slug','')} — {d.get('title','')[:40]}")
        return

    client     = setup_gemini()
    used_topics = load_used_topics()

    # 현재 전체 제목·슬러그 목록 (중복 방지용)
    existing_titles = [p["data"].get("title", "") for p in all_posts]
    existing_slugs  = {p["data"].get("slug", "") for p in all_posts}

    success = 0
    fail    = 0

    for idx, post_entry in enumerate(pending):
        old_data = post_entry["data"]
        old_slug = old_data.get("slug", "")
        category = old_data.get("category", "")
        date     = old_data.get("date", datetime.now().strftime("%Y-%m-%d"))
        author   = old_data.get("author", {})
        image    = old_data.get("image", "")

        cat_data      = CATEGORIES[category]
        pexels_queries = cat_data["pexels_queries"]
        slug_prefix   = cat_data.get("slug_prefix", "casino")
        slug_suffixes = cat_data.get("slug_suffixes", ["guide", "tips"])

        print(f"\n[{idx+1}/{len(pending)}] {old_slug}")
        print(f"  카테고리: {category} | 원본 날짜: {date}")

        # ── 파이프라인 변수 결정 ──────────────────
        keyword, angle, content_model = get_next_topic(category, used_topics)
        tone          = random.choice(TONES)
        intro_type    = random.choice(INTRO_TYPES)
        ending_type   = random.choice(ENDING_TYPES)
        length_option = random.choice(LENGTH_OPTIONS)

        print(f"  키워드: {keyword} | 앵글: {angle} | 모델: {content_model}")
        print(f"  길이: {length_option['label']} | 문체: {tone[:15]}...")

        try:
            # Step 1 — 제목 생성
            print("  🔍 제목 생성 중...")
            title = generate_unique_title(
                client, category, keyword, angle, content_model,
                existing_titles,
            )
            time.sleep(2)

            # Step 2 — 본문 생성
            print("  🤖 본문 생성 중...")
            # 현재 처리 중인 슬러그는 기존 목록에서 제외 (새 슬러그 할당 위해)
            slugs_for_generation = existing_slugs - {old_slug}
            content_data = generate_post_content(
                client, title, category, keyword,
                angle, content_model, tone, intro_type, ending_type, length_option,
                pexels_queries, slugs_for_generation, slug_prefix, slug_suffixes,
            )
            if not content_data:
                print("  ❌ 본문 생성 실패 — 스킵")
                fail += 1
                continue

            # Step 3 — 슬러그 확정
            raw_slug = content_data.get("slug", "")
            if not raw_slug:
                print("  ❌ 슬러그 없음 — 스킵")
                fail += 1
                continue
            new_slug = ensure_unique_slug(raw_slug, existing_slugs)

            # Step 4 — 이미지 (기존 이미지 재사용, 검색 실패 시에만)
            used_images = get_all_used_images(exclude_slug=old_slug)
            if image and image not in used_images:
                print(f"  🖼️  기존 이미지 재사용")
                final_image = image
            else:
                print("  📸 새 이미지 검색 중...")
                gemini_query = content_data.get("pexels_query", "")
                image_queries = ([gemini_query] if gemini_query else []) + pexels_queries
                final_image = fetch_pexels_image(image_queries, used_images)

            # 본문 삽입 이미지
            inline_queries = pexels_queries[::-1]
            used_images.add(final_image)
            inline_image_url = fetch_pexels_image(inline_queries, used_images)
            inline_image_alt = f"{content_data.get('imageAlt', title)} - 본문 참고 이미지"

            # Step 5 — 저장
            content_data["slug"] = new_slug
            save_new_post(
                new_slug, old_slug, content_data,
                final_image, category, date, author,
                inline_image_url, inline_image_alt,
            )

            # 상태 업데이트
            existing_titles.append(title)
            existing_slugs.discard(old_slug)
            existing_slugs.add(new_slug)
            done_slugs.add(old_slug)
            save_progress(done_slugs)
            save_used_topics(used_topics)
            print(f"  💾 진행 저장: {len(done_slugs)}/{len(all_posts)}")

            success += 1

        except KeyboardInterrupt:
            print("\n\n⛔ 중단됨 — 진행 상황 저장됨. --resume 으로 재시작 가능.")
            save_progress(done_slugs)
            save_used_topics(used_topics)
            sys.exit(0)
        except Exception as e:
            print(f"  ❌ 오류: {e}")
            fail += 1

        time.sleep(SLEEP_BETWEEN)

    print("\n" + "=" * 60)
    print(f"  완료: {success}개 성공 | {fail}개 실패")
    print(f"  전체 포스트: {len(existing_slugs)}개")
    print("=" * 60)

    # 완료 시 진행 파일 삭제
    if os.path.exists(PROGRESS_FILE):
        os.remove(PROGRESS_FILE)


if __name__ == "__main__":
    main()
