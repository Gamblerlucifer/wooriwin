"""
semiauto_platforms.py
──────────────────
1-2단계(Chrome 반자동) 플랫폼 목록 — backlink-reminder.py, semi-auto-post.py 공용.
new_post_url: 가능하면 "새 글 작성" 딥링크, 불확실하면 홈페이지.
body_format: "html"(리치 에디터, 마크다운→HTML 변환 후 복사) | "plain"(일반 텍스트박스)

준비 상태(ready)는 여기 하드코딩하지 않고 .semiauto_ready.json(로컬, gitignore)에서 관리한다.
계정 가입 + Chrome 로그인이 실제로 확인된 플랫폼만 ready=true로 표시되고,
semi-auto-post.py는 ready가 아닌 플랫폼은 절대 열지 않는다 (묻지도 따지지도 않고 여는 것 방지).
"""

import os
import json
import datetime

READY_FILE = os.path.join(os.path.dirname(__file__), ".semiauto_ready.json")

PLATFORMS = [
    {"name": "Diigo",             "da": 91, "desc": "북마크 추가",         "new_post_url": "https://www.diigo.com/",                                    "body_format": "plain"},
    {"name": "Medium",            "da": 95, "desc": "블로그 포스팅",        "new_post_url": "https://medium.com/new-story",                              "body_format": "html"},
    {"name": "WordPress.com",     "da": 93, "desc": "블로그 포스팅",        "new_post_url": "https://wordpress.com/post/wooriwin.wordpress.com",         "body_format": "html"},
    # 네이버 블로그 — 본문 외부 링크에 rel="nofollow" 자동 적용, dofollow 백링크 목적에 안 맞아 제외
    {"name": "구글 사이트",         "da": 90, "desc": "새 페이지 추가",       "new_post_url": "https://sites.google.com/",                                  "body_format": "plain"},
    {"name": "Penzu",             "da": 55, "desc": "저널 작성",            "new_post_url": "https://penzu.com/journals",                                 "body_format": "plain"},
    {"name": "Pearltrees",        "da": 62, "desc": "아이템 추가",          "new_post_url": "https://www.pearltrees.com/",                                "body_format": "plain"},
    {"name": "Mystrikingly",      "da": 63, "desc": "블로그 포스트",         "new_post_url": "https://www.mystrikingly.com/",                              "body_format": "html"},
    {"name": "federatedjournals", "da": 43, "desc": "포스팅",              "new_post_url": "https://federatedjournals.com/",                             "body_format": "html"},
    {"name": "Bloggersdelight",   "da": 42, "desc": "포스팅",              "new_post_url": "https://bloggersdelight.dk/",                                "body_format": "html"},
    {"name": "xtgem",             "da": 48, "desc": "포스팅",              "new_post_url": "https://xtgem.com/",                                         "body_format": "plain"},
    {"name": "Anotepad",          "da": 38, "desc": "노트 발행",            "new_post_url": "https://anotepad.com/notes/new",                             "body_format": "plain"},
    {"name": "Pastelink",         "da": 37, "desc": "발행 + dofollow 확인", "new_post_url": "https://pastelink.net/",                                     "body_format": "plain"},
    {"name": "Txt.fyi",           "da": 35, "desc": "발행",                "new_post_url": "https://txt.fyi/",                                           "body_format": "plain"},
]

TOTAL = len(PLATFORMS)


def week_index() -> int:
    week_num = datetime.date.today().isocalendar()[1]
    return (week_num - 1) % TOTAL


def get_this_week_platform() -> dict:
    return PLATFORMS[week_index()]


def get_next_platform() -> dict:
    return PLATFORMS[(week_index() + 1) % TOTAL]


def find_platform(name: str) -> dict | None:
    """이름으로 검색 (대소문자 무시, 부분 일치)."""
    name_lower = name.strip().lower()
    for p in PLATFORMS:
        if p["name"].lower() == name_lower:
            return p
    for p in PLATFORMS:
        if name_lower in p["name"].lower() or p["name"].lower() in name_lower:
            return p
    return None


def load_ready() -> dict:
    if os.path.exists(READY_FILE):
        with open(READY_FILE, encoding="utf-8") as f:
            return json.load(f)
    return {}


def is_ready(name: str) -> bool:
    return load_ready().get(name, False) is True


def mark_ready(name: str, ready: bool = True):
    state = load_ready()
    state[name] = ready
    with open(READY_FILE, "w", encoding="utf-8") as f:
        json.dump(state, f, ensure_ascii=False, indent=2)
