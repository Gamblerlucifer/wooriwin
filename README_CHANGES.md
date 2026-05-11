# WOORIWIN 전체 수정 적용 가이드 (v2)

## 📁 압축 해제 방법

```powershell
cd C:\Users\jjun1\Desktop\project\wooriwin
Expand-Archive -Path wooriwin_final.zip -DestinationPath . -Force
```

## ⚠️ 중요: 사이트맵 적용 안 되던 원인 해결

이전 `.gitignore`에 `/data/posts/` 를 추가했더니 **GitHub에서 폴더가 사라져서 사이트맵 빌드 시 블로그 포스트가 누락**되었습니다.

**이번 zip에서는 `/data/posts/` 항목을 .gitignore에서 제거**했습니다.

---

## 📋 v2 변경 내역

### 🔴 사이트맵 문제 해결
- ✅ `.gitignore`에서 `/data/posts/` 제거
- ✅ GitHub에 포스트 폴더 정상 커밋 → 사이트맵에 포함

### 🆕 내부 링크 (Topic Cluster)
- ✅ 카테고리 → 게임 페이지 매핑 추가
- ✅ 새 포스트 생성 시 본문 끝에 "함께 보면 좋은 글" 자동 삽입

| 카테고리 | 연결 페이지 |
|---------|------------|
| 에볼루션 가이드 | /live-casino |
| 바카라 가이드 | /baccarat |
| 블랙잭 가이드 | /blackjack |
| 게임쇼 분석 | /slots |
| 룰렛 & 포커 | /roulette |
| 최신 트렌드 | /live-casino |
| 자금 관리 | /responsible-gaming |
| 보안 및 라이선스 | /about |
| 모바일 최적화 | /live-casino |
| 책임감 있는 게임 | /responsible-gaming |

### 🆕 기존 포스트 일괄 수정 스크립트
- ✅ scripts/fix-existing-posts.py 추가
- 기존 JSON 12개에 대해:
  - 중복 title 자동 감지 & Gemini로 새 제목 생성
  - 카테고리별 내부 링크 자동 추가
  - relatedPosts 필드 제거

```powershell
python scripts/fix-existing-posts.py
```

### 🔴 SEO 수정 (v1 포함)
- 정책 4페이지 title 30자 이상
- 정책 페이지 BreadcrumbList Schema
- live-casino, roulette, slots Schema TechArticle 통일

### 🟡 콘텐츠 (v1 포함)
- baccarat 'YMYL' 단어 제거
- generate-post.py 카테고리+키워드 동적 생성
- 중복 단어 3개 검사

### 🟢 접근성 (v1 포함)
- responsible-gaming □ → input checkbox

### ⚡ 성능 (v1 포함)
- CTA box-shadow → transform (GPU 합성)
- Hero preload, 게임 카드 lazy
- Referrer-Policy 헤더

---

## 🚀 푸시 순서

```powershell
# 1. zip 압축 해제
cd C:\Users\jjun1\Desktop\project\wooriwin
Expand-Archive -Path wooriwin_final.zip -DestinationPath . -Force

# 2. 기존 포스트 일괄 수정 (선택)
python scripts/fix-existing-posts.py

# 3. 커밋 & 푸시
git add .
git commit -m "fix: v2 - 사이트맵, 내부링크, 기존 포스트 수정"
git pull origin main
git push origin main
```

## ✅ 푸시 후 확인

1. `https://wooriwin.com/sitemap-0.xml` — 12개 포스트 + 정책 페이지 포함 확인
2. GitHub Actions 다음 실행 시 자동으로 새 포스트에 내부 링크 삽입
