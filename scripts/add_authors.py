import os
import json
import random

# ── 작성자 데이터 ─────────────────────────────────
AUTHORS = {
    "박성준": {
        "role": "창업자 · 대표",
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

# ── 카테고리별 담당 작성자 ─────────────────────────
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


def get_author(category: str) -> dict:
    candidates = CATEGORY_TO_AUTHORS.get(category, list(AUTHORS.keys()))
    name = random.choice(candidates)
    return {"name": name, **AUTHORS[name]}


def process_posts(posts_dir: str):
    if not os.path.exists(posts_dir):
        print(f"❌ 경로를 찾을 수 없습니다: {posts_dir}")
        return

    files = [f for f in os.listdir(posts_dir) if f.endswith(".json")]
    if not files:
        print("❌ JSON 파일이 없습니다.")
        return

    updated = 0
    errors  = 0

    print(f"📂 대상 폴더: {posts_dir}")
    print(f"📄 총 파일 수: {len(files)}\n")

    for fname in sorted(files):
        fpath = os.path.join(posts_dir, fname)
        try:
            with open(fpath, "r", encoding="utf-8") as f:
                post = json.load(f)

            category = post.get("category", "")
            author   = get_author(category)
            post["author"] = author

            with open(fpath, "w", encoding="utf-8") as f:
                json.dump(post, f, ensure_ascii=False, indent=2)

            print(f"  ✅ 완료: {fname}")
            print(f"      카테고리: {category} → 작성자: {author['name']} ({author['role']})")
            updated += 1

        except Exception as e:
            print(f"  ❌ 오류 ({fname}): {e}")
            errors += 1

    print(f"\n{'='*45}")
    print(f"  완료: {updated}개  |  오류: {errors}개")
    print(f"{'='*45}")


if __name__ == "__main__":
    # ── 경로 설정: 실제 posts 폴더 경로로 수정하세요 ──
    POSTS_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "posts")
    process_posts(POSTS_DIR)
