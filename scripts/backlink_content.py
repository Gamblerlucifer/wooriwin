"""
backlink_content.py
──────────────────
백링크 포스팅 스크립트(telegraph-post.py, gist-post.py, blogger-post.py, writeas-post.py 등)가
공통으로 쓰는 콘텐츠 생성 모듈.

wooriwin.com의 실제 포스트(data/posts/*.json) 중 하나를 골라, 그 글을 발췌/복사하는 게 아니라
제미나이로 완전히 새로운 짧은 글을 쓰고, 그 안에 다양한 앵커 텍스트로 wooriwin.com 백링크를
1개 자연스럽게 삽입한다. 같은 원문이라도 호출할 때마다 다른 글 + 다른 앵커가 나온다.
"""

import os
import re
import json
import glob
import random
from google import genai

GEMINI_API_KEY = os.environ.get("GEMINI_API_KEY", "")

BASE_DIR   = os.path.join(os.path.dirname(__file__), "..")
POSTS_DIR  = os.path.join(BASE_DIR, "data", "posts")
SITE_BASE_URL = "https://wooriwin.com"

MODEL = "gemini-3.1-flash-lite"

ANCHOR_STYLES = [
    "exact",     # 키워드 그대로 (예: "에볼루션카지노")
    "phrase",    # 키워드 + 후기/가이드/정보 (예: "에볼루션카지노 후기")
    "branded",   # 사이트명 노출형 (예: "wooriwin 카지노 가이드")
    "generic",   # 일반 CTA형 (예: "자세히 알아보기")
]

GENERIC_ANCHORS = ["자세히 알아보기", "원문에서 확인하기", "더 많은 정보 보기", "관련 글 읽어보기"]
PHRASE_SUFFIXES = ["후기", "가이드", "정보", "분석"]


def load_wooriwin_posts() -> list:
    posts = []
    for path in glob.glob(os.path.join(POSTS_DIR, "*.json")):
        with open(path, encoding="utf-8") as f:
            posts.append(json.load(f))
    return posts


def pick_source_post() -> dict:
    posts = load_wooriwin_posts()
    if not posts:
        raise RuntimeError(f"data/posts/ 에 글이 없습니다: {POSTS_DIR}")
    return random.choice(posts)


def build_anchor_text(post: dict) -> str:
    style = random.choice(ANCHOR_STYLES)
    keyword = random.choice(post.get("keywords") or [post["category"]])

    if style == "exact":
        return keyword
    if style == "phrase":
        return f"{keyword} {random.choice(PHRASE_SUFFIXES)}"
    if style == "branded":
        return random.choice(["wooriwin 카지노 가이드", "wooriwin.com 바로가기", "wooriwin 카지노 정보"])
    return random.choice(GENERIC_ANCHORS)


def clean_json_response(text: str) -> str:
    text = text.strip()
    text = re.sub(r"^```(?:json)?\s*", "", text)
    text = re.sub(r"\s*```$", "", text)
    return text.strip()


def generate_backlink_article(platform_name: str) -> dict:
    """반환값: {"title", "body_markdown", "anchor_text", "source_slug"}"""
    post = pick_source_post()
    anchor_text = build_anchor_text(post)
    target_url = f"{SITE_BASE_URL}/blog/{post['slug']}"

    prompt = f"""당신은 카지노/온라인 게이밍 분야 칼럼니스트입니다. {platform_name}에 올릴 짧은 글을 씁니다.

아래는 참고할 원본 글 정보입니다. 이 글을 요약하거나 발췌하지 말고, 같은 주제를 완전히 다른 각도로
새로 쓰세요(예: 최근 이슈 코멘트, 짧은 팁 모음, 개인적 관전평 등 원본과 다른 형식).

원본 제목: {post['title']}
원본 주제: {post['description']}
카테고리: {post['category']}
키워드: {', '.join(post.get('keywords', []))}

요구사항:
- 400~600자 분량의 완전히 새로운 한국어 글
- 마크다운 형식
- 본문 중 자연스러운 위치에 다음 앵커 텍스트로 링크를 정확히 1번 삽입: "{anchor_text}"
  링크 형식: [{anchor_text}]({target_url})
- 광고 문구나 "지금 가입하세요" 같은 표현 없이, 정보/분석 톤 유지
- 응답은 아래 JSON 형식으로만 출력 (다른 텍스트 금지):
{{"title": "글 제목", "body_markdown": "마크다운 본문"}}
"""

    client = genai.Client(api_key=GEMINI_API_KEY)
    response = client.models.generate_content(model=MODEL, contents=prompt)
    data = json.loads(clean_json_response(response.text))

    return {
        "title": data["title"],
        "body_markdown": data["body_markdown"],
        "anchor_text": anchor_text,
        "source_slug": post["slug"],
    }
