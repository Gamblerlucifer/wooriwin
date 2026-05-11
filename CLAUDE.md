@AGENTS.md

# WOORIWIN — Claude 작업 컨텍스트

> 목표: "에볼루션카지노" 구글 검색 1위  
> 도메인: wooriwin.com (2016년생, 백링크 24,333개)  
> GitHub: https://github.com/Gamblerlucifer/wooriwin  
> 로컬 경로: `C:\Users\jjun1\Desktop\project\wooriwin`

---

## 기술 스택

| 항목 | 내용 |
|------|------|
| 프레임워크 | Next.js (SSG) + Vercel |
| 콘텐츠 자동화 | Gemini **3.1 Flash-Lite** API |
| 이미지 | Pexels API |
| CI/CD | GitHub Actions (매일 새벽 1시 KST) |
| 터미널 | PowerShell (&&  안됨 → `;` 사용) |

---

## 프로젝트 구조

```
app/
├── page.tsx              # 메인 (에볼루션카지노)
├── baccarat/page.tsx     # 바카라 가이드 (기준 템플릿)
├── blackjack/page.tsx
├── roulette/page.tsx
├── slots/page.tsx
├── live-casino/page.tsx
├── blog/page.tsx
├── blog/[slug]/page.tsx
├── about/page.tsx
├── disclaimer/page.tsx
├── privacy-policy/page.tsx
├── terms/page.tsx
└── responsible-gaming/page.tsx

scripts/
└── generate-post.py      # Gemini 3.1 Flash-Lite 자동 포스팅

data/
└── posts/*.json          # GitHub Actions만 커밋 (로컬 무시)

.github/workflows/
└── main.yml              # 자동 포스팅 워크플로우
```

---

## metadata 구조 규칙

| 항목 | layout.tsx | 각 page.tsx |
|------|-----------|-------------|
| title | 미사용 (주석 처리) | 완전한 title 직접 설정 |
| metadataBase | ✅ | - |
| robots | ✅ 전역 허용 | 각 페이지에 따로 안 넣어도 됨 |
| openGraph 공통 | siteName, locale, type | url, title, description, image |
| WebSite JSON-LD | ✅ | - |

### title 규칙
```
메인:     '에볼루션카지노 완벽 가이드 2026 | WOORIWIN'
서브:     '에볼루션카지노 바카라 완벽 가이드 2026 | WOORIWIN'
블로그:   `${post.title} | WOORIWIN`
```

---

## 저자 표준 코드 (모든 게임 페이지 공통)

```tsx
<div className="flex items-center gap-3 text-sm text-gray-500 mb-6">
  <span>작성자</span>
  <Link href="/about" className="text-yellow-400 hover:underline font-semibold">WOORIWIN 팀</Link>
  <span>·</span>
  <span>라이브카지노 전문 애널리스트 · Evolution 공식 자료 기반 검수</span>
</div>
```

> ⚠️ "10년 경력" 같은 검증 불가 표현 금지 (YMYL 위반)

---

## SEO / E-E-A-T 규칙

- RTP 수치 언급 시 반드시 `이론적 기댓값이며 실제 결과와 다를 수 있습니다` 병기
- 출처 명시: `Evolution Gaming 공식 게임 수학 문서 기준`
- 손실 위험 안내 본문 내 1회 이상 포함
- eCOGRA 언급으로 신뢰도 강화
- 모든 이모지 `<span aria-hidden="true">🎯</span>` 처리
- BreadcrumbList Schema 모든 페이지 필수

---

## .gitignore 주요 항목

```
wooriwin-indexing.json   # Google 서비스 계정 키 (절대 커밋 금지)
/data/posts/             # GitHub Actions만 관리
```

---

## GitHub Actions (main.yml)

- 서비스 계정 키: `GOOGLE_INDEXING_KEY` Secret에 **Base64 인코딩**으로 저장
- Base64 인코딩 방법:
  ```powershell
  [Convert]::ToBase64String([IO.File]::ReadAllBytes("wooriwin-indexing.json"))
  ```
- 워크플로우에서 복원:
  ```yaml
  echo '${{ secrets.GOOGLE_INDEXING_KEY }}' | base64 -d > wooriwin-indexing.json
  ```
- `git add data/posts/` — 포스트만 커밋

---

## Google Indexing API

- 서비스 계정: `service-account@wooriwin-indexing-api.iam.gserviceaccount.com`
- 키 파일: `wooriwin-indexing.json` (로컬만 보관, .gitignore)
- Web Search Indexing API: ✅ 활성화
- generate-post.py에 연동 완료 (포스트 저장 후 자동 색인 요청)

---

## 푸시 명령어 (PowerShell)

```powershell
# 충돌 시
git pull origin main
git push origin main

# 일반 푸시
git add .
git commit -m "커밋 메시지"
git pull origin main
git push origin main
```

> `git config pull.rebase true` 설정 완료

---

## 완료된 작업 (2026-05-11 기준)

- ✅ 전체 개발/배포/SEO 설정
- ✅ 콘텐츠 자동화 파이프라인 (Gemini 3.1 Flash-Lite)
- ✅ Google Indexing API 연동 (generate-post.py)
- ✅ next-sitemap — 블로그 포스트 + 정책 페이지 추가
- ✅ next.config.ts — 레거시 폴리필 제거, browserslist
- ✅ app/page.tsx — BreadcrumbList Schema, hero preload, lazy images
- ✅ 모든 게임 페이지 저자 표현 수정
- ✅ 정책 페이지 robots/canonical/description 추가
- ✅ .gitignore — data/posts, wooriwin-indexing.json 제외
- ✅ main.yml — Base64 키 복원, google-auth 패키지 추가

## 남은 작업

- [ ] GitHub Secret `GOOGLE_INDEXING_KEY` Base64 등록
- [ ] 기존 포스트 일괄 색인 요청 스크립트 실행
- [ ] GSC 사이트맵 재제출 (sitemap 수정 후)
