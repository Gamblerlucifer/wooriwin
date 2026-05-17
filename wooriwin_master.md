# WOORIWIN — 마스터 문서
> 도메인: wooriwin.com (2016년생, 백링크 24,333개)
> 목표: "에볼루션카지노" 관련 키워드 구글 1위
> 스택: Next.js 16 (SSG) + Vercel + Gemini API 자동화
> 최종 업데이트: 2026-05-16

---

## 완료

- 배포: wooriwin.vercel.app → wooriwin.com (Vercel DNS)
- 에볼루션카지노.site → wooriwin.com 301 리다이렉트
- WordPress 한글 URL 301 리다이렉트
- Lighthouse 모바일 95/100/100/100, 데스크톱 99/100/100/100
- GSC 등록 + 사이트맵 제출 (27 URL)
- GitHub Actions 자동 포스팅 (매일 07:00 KST, Gemini API, 하루 3포스트)
- generate-post.py: KST 날짜, 이미지 중복 방지, 슬러그 다각화, 제목 키워드 다양화
- fix-existing-posts.py: 기존 15개 포스트 제목+슬러그 전체 교체
- 모든 게임 페이지 MZ스타일 리빌드 (baccarat, blackjack, roulette, slots, live-casino)
- 정책 페이지 제작 (disclaimer, privacy-policy, terms, responsible-gaming)
- app/not-found.tsx: 404 페이지 생성
- about 페이지 전면 개선 (Lucifer 프로필, 메타, OG, 외부 링크)
- metadata 구조 확정 (모든 페이지 | WOORIWIN 직접 포함)
- app/page.tsx: 홈에 최신 블로그 6개 + Evolution 본사 구글맵 + 파트너사 마키
- app/blog/page.tsx: 페이지네이션 (21개씩)
- app/blog/CategoryFilter.tsx: 카테고리 URL 영문 slug 변환 + aria-pressed
- app/layout.tsx: 신뢰기관 로고 6개 + Evolution SNS + 배너 색상 개선
- blog SEO 본문 10개 카테고리 완성
- 블로그 포스트 저자 프로필 추가, ISR 설정
- blog/[slug] — notFound() 적용
- 전체 파일 — BreadcrumbList JSON-LD 추가 (14개 파일)
- blog/[slug] — 저자 Schema Person으로 동적 처리
- live-casino·roulette — blockquote 이중 따옴표 오타 수정
- 정책 3개 파일 — 실제 이메일 연락처 추가
- 전체 파일 — 이모지 aria-hidden="true" 처리
- CategoryFilter aria-pressed 추가
- PolicyPage 컴포넌트 분리 후 재사용
- 정책 파일 bullet → ul/li 태그 변경
- disclaimer — 최종 수정일 추가
- responsible-gaming — 전화번호 tel: 링크 변환
- blackjack — 애니페어 하우스엣지 4.10%
- blog — 포스트 이미지 sizes prop 추가
- Google Indexing API → 포기

---

## 현황 (2026-05-16)

| 항목 | 수치 |
|------|------|
| 블로그 포스트 | 18개+ (매일 3개 자동 생성) |
| 사이트맵 URL | 27개 |
| DoFollow 비율 | 16% |
| GSC 색인 | PASS 5개 / NEUTRAL 22개 |

---

## TODO

### 🔴 높음

- [ ] generate-wp-posts.py 제작 — howtobet7.com, moneyrush.net, wooriwin.net 자동 포스팅 + wooriwin.com DoFollow 백링크 삽입 (각 사이트 WordPress 앱 비밀번호 발급 필요)
- [ ] DoFollow 비율 개선 (현재 16%) — howtobet7.com footer에 wooriwin.com 링크 추가
- [ ] 보유 SNS 계정에 wooriwin.com 백링크 삽입 (프로필 링크, 게시물 링크)
- [ ] Google 색인 403 해결 — 서비스 계정 권한 문제

### 🟡 중간

- [ ] Gemini 503 에러 재시도 횟수 1→3회로 수정 (generate-post.py)
- [ ] layout.tsx — OG 기본값 (og:image 등) 추가
- [ ] wooriwin.net → wooriwin.com 301 리다이렉트 검토 (백링크 97.6%가 DA20 미만 저품질 → 보류 권장)
- [ ] NEUTRAL 22개 → PASS 전환 모니터링 (1~2주 대기)

### 📈 장기

- [ ] howtobet7.com, moneyrush.net, wooriwin.net 자체 콘텐츠 전략 수립
- [ ] /game-shows 페이지 분리 (slots에서 게임쇼 콘텐츠 분리)
- [ ] 블로그 주제 50개 → 100개 확장

---

## 콘텐츠 자동화

- 스크립트: scripts/generate-post.py (Gemini Flash-Lite)
- 실행: GitHub Actions, 매일 07:00 KST, 하루 3포스트
- 주제: 50개 × 10개 카테고리 (약 17일 1순환)
- 이미지: scripts/fetch-images.py (Pexels API, 중복 방지 적용)
- 저장: data/posts/*.json

| 기간 | 목표 포스팅 | 목표 |
|------|------------|------|
| 1개월 | 90건 | 롱테일 유입 시작 |
| 2개월 | 180건 | 롱테일 10위권 진입 |
| 3개월 | 270건 | 메인 키워드 상위 진입 |

---

## SEO 구조

메인(/) → "에볼루션카지노"
├── /baccarat      → "에볼루션카지노 바카라"
├── /blackjack     → "에볼루션카지노 블랙잭"
├── /roulette      → "에볼루션카지노 룰렛"
├── /slots         → "에볼루션카지노 슬롯"
├── /live-casino   → "에볼루션 라이브카지노"
└── /blog          → 롱테일 키워드 (자동 포스팅)

---

## 백링크 전략

| 방법 | 실행 방법 | 적합도 |
|------|----------|--------|
| 글쓰기 플랫폼 | Medium 등에 에볼루션카지노 관련 글 작성 → wooriwin.com 링크 삽입 | ✅ |
| Broken Link Swapping | Ahrefs로 카지노·바카라 키워드 깨진 링크 찾기 → wooriwin.com 대체 제안 | ✅ |
| Guest Posting | 카지노·갬블링 관련 커뮤니티/블로그에 전략 글 기고 → 링크 삽입 | ✅ |
| HARO | 도박·카지노 관련 기자 질문에 전문가로 답변 (영어권) | ✅ |
| 보유 SNS 프로필 | 프로필 링크 + 게시물 링크 wooriwin.com 삽입 | ✅ |
| Product Hunt | 소프트웨어 제품 전용 | ❌ |
