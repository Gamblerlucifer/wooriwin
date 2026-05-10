import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'
import { readFileSync, readdirSync, existsSync } from 'fs'
import { join } from 'path'
import CategoryFilter from './CategoryFilter'

const POSTS_DIR = join(process.cwd(), 'data', 'posts')

function getAllPosts() {
  if (!existsSync(POSTS_DIR)) return []
  return readdirSync(POSTS_DIR)
    .filter((f) => f.endsWith('.json'))
    .map((f) => JSON.parse(readFileSync(join(POSTS_DIR, f), 'utf-8')))
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
}

// ─── 메타데이터 ────────────────────────────────────────────────────────────
export const metadata: Metadata = {
  title: '에볼루션카지노 전략 블로그 | WOORIWIN',
  description:
    '에볼루션카지노 바카라·블랙잭·룰렛 전략, 규칙, 팁을 전문가가 매일 분석. 롱테일 키워드 기반 심층 가이드. 초보자부터 고수까지 필독 에볼루션카지노 블로그.',
  keywords: ['에볼루션카지노 전략', '에볼루션카지노 규칙', '에볼루션카지노 팁', '바카라 전략', '블랙잭 전략', '룰렛 전략'],
  alternates: { canonical: 'https://wooriwin.com/blog' },
  openGraph: {
    title: '에볼루션카지노 전략 블로그 | WOORIWIN',
    description: '에볼루션카지노 바카라·블랙잭·룰렛 전략 전문가 분석 블로그.',
    url: 'https://wooriwin.com/blog',
    images: [{ url: 'https://wooriwin.com/images/blog.jpg', width: 1200, height: 630 }],
  },
  // ✅ twitter 추가
  twitter: {
    card: 'summary_large_image',
    title: '에볼루션카지노 전략 블로그 | WOORIWIN',
    description: '에볼루션카지노 바카라·블랙잭·룰렛 전략 전문가 분석 블로그.',
    images: ['https://wooriwin.com/images/blog.jpg'],
  },
}

// ─── JSON-LD (① SEO 개선: author/datePublished/dateModified 추가) ─────────
const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Blog',
  name: 'WOORIWIN 에볼루션카지노 전략 블로그',
  description: '에볼루션카지노 바카라·블랙잭·룰렛 전략, 규칙, 팁 전문 블로그',
  url: 'https://wooriwin.com/blog',
  inLanguage: 'ko-KR',
  datePublished: '2026-05-01',
  dateModified: '2026-05-10',
  author: {
    '@type': 'Organization',
    name: 'Gambler Lucifer',
    url: 'https://wooriwin.com/about',
  },
  publisher: { '@type': 'Organization', name: 'WOORIWIN', url: 'https://wooriwin.com' },
}


const categories = ['전체', '에볼루션 가이드', '바카라 가이드', '블랙잭 가이드', '게임쇼 분석', '룰렛 & 포커', '최신 트렌드', '자금 관리', '보안 및 라이선스', '모바일 최적화', '책임감 있는 게임']


export default function BlogPage() {
  const posts = getAllPosts()

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <main className="min-h-screen bg-gray-900 text-white">

        {/* Hero */}
        <section className="relative flex flex-col items-center justify-center min-h-[45vh] text-center px-4 py-16 overflow-hidden">
          <div className="absolute inset-0 z-0">
            {/* ✅ alt 키워드 스터핑 제거 */}
            <Image src="/images/blog.jpg" alt="에볼루션카지노 전략 블로그" fill className="object-cover opacity-20" priority />
          </div>
          <div className="relative z-10 max-w-4xl mx-auto">
            <nav aria-label="breadcrumb" className="text-sm text-gray-400 mb-6">
              <Link href="/" className="hover:text-yellow-400">홈</Link> &rsaquo; <span className="text-white" aria-current="page">블로그</span>
            </nav>
            <p className="text-sm text-yellow-400 font-semibold tracking-widest uppercase mb-4">매일 업데이트 · 전문가 분석</p>
            <h1 className="text-4xl md:text-5xl font-bold mb-6 leading-tight">
              에볼루션카지노<br />
              <span className="text-yellow-400">전략 블로그</span>
            </h1>
            <p className="text-lg text-gray-300 max-w-2xl mx-auto">
              바카라·블랙잭·룰렛 전략부터 가입방법·규칙까지. 에볼루션카지노의 모든 정보를 매일 업데이트합니다.
            </p>
          </div>
        </section>

        {/* 카테고리 필터 + 포스트 그리드 */}
        <CategoryFilter posts={posts} categories={categories} />

        {/* SEO 본문 */}
        <section className="bg-gray-800 py-16 px-4">
          <div className="max-w-4xl mx-auto space-y-12">

            {/* 소개 */}
            <div>
              <h2 className="text-3xl font-bold mb-6 text-yellow-400">에볼루션카지노 전략 블로그 소개</h2>
              <div className="text-gray-300 space-y-5 leading-relaxed text-base">
                <p>
                  WOORIWIN 에볼루션카지노 전략 블로그는 <strong className="text-white">바카라·블랙잭·룰렛·슬롯·게임쇼</strong>를 포함한
                  에볼루션카지노 모든 게임의 전략, 규칙, 팁을 전문가 수준으로 분석합니다.
                  10년 경력 딜러 출신 전문가의 실전 노하우와 최신 트렌드를 매일 업데이트합니다.
                  초보자부터 고수까지, 에볼루션카지노에 관한 모든 정보를 한 곳에서 확인하세요.
                </p>
              </div>
            </div>

            {/* 1. 에볼루션 가이드 */}
            <div>
              <h3 className="text-2xl font-bold mb-4 text-yellow-300">📘 에볼루션 가이드</h3>
              <div className="text-gray-300 space-y-4 leading-relaxed text-base">
                <p>
                  <strong className="text-white">에볼루션카지노(Evolution Gaming)</strong>는 2006년 설립된 세계 최대 라이브 카지노
                  소프트웨어 제공업체로, 나스닥 스톡홀름에 상장된 합법적인 글로벌 기업입니다.
                  전 세계 1,000개 이상의 온라인 카지노에 소프트웨어를 공급하며 업계 표준을 정의합니다.
                </p>
                <p>
                  에볼루션 가이드 카테고리에서는 플랫폼 전반에 대한 심층 분석을 제공합니다.
                  게임 인터페이스 조작법, <strong className="text-white">멀티 게임 동시 플레이</strong> 설정,
                  라이브 채팅 기능 활용법 등 처음 접하는 플레이어도 즉시 이해할 수 있도록 단계별로 안내합니다.
                  또한 에볼루션만의 독점 기술인 <strong className="text-white">듀얼 플레이</strong>와
                  다이렉트 게임 런치 기능도 상세히 분석합니다.
                </p>
              </div>
            </div>

            {/* 2. 바카라 가이드 */}
            <div>
              <h3 className="text-2xl font-bold mb-4 text-yellow-300">🃏 바카라 가이드</h3>
              <div className="text-gray-300 space-y-4 leading-relaxed text-base">
                <p>
                  에볼루션카지노에서 가장 인기 있는 게임인 <strong className="text-white">바카라</strong>는
                  뱅커·플레이어 베팅 승률부터 라이트닝 바카라 멀티플라이어 전략까지 다양한 콘텐츠로 다룹니다.
                  RTP 98.94%를 자랑하는 바카라에서 뱅커 베팅 승률 45.86%의 통계적 의미와
                  실전에서 활용 가능한 마틴게일·파롤리·1-3-2-6 베팅 시스템을 비교 분석합니다.
                </p>
                <p>
                  특히 <strong className="text-white">라이트닝 바카라 vs 일반 바카라</strong>의 수학적 차이,
                  골든 카드 활용 전략, 코리안 스피드 바카라 장단점,
                  그리고 많은 플레이어가 맹신하는 <strong className="text-white">로드맵(그림) 분석의 허와 실</strong>까지
                  데이터 기반으로 정직하게 분석합니다.
                </p>
              </div>
            </div>

            {/* 3. 블랙잭 가이드 */}
            <div>
              <h3 className="text-2xl font-bold mb-4 text-yellow-300">🎴 블랙잭 가이드</h3>
              <div className="text-gray-300 space-y-4 leading-relaxed text-base">
                <p>
                  카지노 게임 중 <strong className="text-white">RTP 99% 이상</strong>을 달성할 수 있는 유일한 게임,
                  에볼루션 블랙잭 완벽 가이드를 제공합니다.
                  기본 전략표(Basic Strategy Chart) 적용법, 더블다운·스플릿·서렌더의 최적 타이밍,
                  인피니트 블랙잭과 스피드 블랙잭의 차이점을 상황별로 정리합니다.
                </p>
                <p>
                  <strong className="text-white">라이트닝 블랙잭</strong>의 무작위 멀티플라이어 메커니즘 이해부터
                  딜러 업카드별 최적 플레이 결정까지, 전문가가 실제 현장에서 검증한 전략을 공유합니다.
                  기본 전략만 제대로 적용해도 하우스 엣지를 0.5% 이하로 낮출 수 있습니다.
                </p>
              </div>
            </div>

            {/* 4. 게임쇼 분석 */}
            <div>
              <h3 className="text-2xl font-bold mb-4 text-yellow-300">🎡 게임쇼 분석</h3>
              <div className="text-gray-300 space-y-4 leading-relaxed text-base">
                <p>
                  에볼루션의 혁신적인 라이브 게임쇼는 기존 카지노의 한계를 완전히 뛰어넘었습니다.
                  <strong className="text-white">크레이지타임(Crazy Time)</strong>의 4개 보너스 게임 확률 분석,
                  <strong className="text-white">모노폴리 라이브</strong>의 보너스 배율 메커니즘,
                  딥씨(Deep Sea)·파워업 룰렛 등 최신 게임쇼까지 전부 심층 분석합니다.
                </p>
                <p>
                  게임쇼 카테고리에서는 단순한 규칙 설명을 넘어
                  <strong className="text-white">실제 RTP 데이터</strong>와 보너스 트리거 확률,
                  각 세그먼트별 기대값 계산법을 제공합니다.
                  어떤 베팅이 장기적으로 가장 유리한지 수학적으로 접근합니다.
                </p>
              </div>
            </div>

            {/* 5. 룰렛 & 포커 */}
            <div>
              <h3 className="text-2xl font-bold mb-4 text-yellow-300">🎰 룰렛 &amp; 포커</h3>
              <div className="text-gray-300 space-y-4 leading-relaxed text-base">
                <p>
                  에볼루션 룰렛의 꽃, <strong className="text-white">라이트닝 룰렛</strong>의 번개 번호 메커니즘을
                  완벽하게 해부합니다. 매 스핀 2~5개 숫자에 적용되는 50x~500x 멀티플라이어의
                  실제 확률과 기대값, 일반 유럽 룰렛 대비 유불리를 정직하게 분석합니다.
                </p>
                <p>
                  <strong className="text-white">이머시브 룰렛</strong>의 다중 카메라 앵글 활용법,
                  아메리칸 vs 유럽 룰렛의 하우스 엣지 차이(5.26% vs 2.7%),
                  섹터 베팅·이웃 베팅 전략까지 룰렛을 수학적으로 이해하는 모든 방법을 담았습니다.
                  에볼루션 카지노 홀덤 포커 전략도 함께 다룹니다.
                </p>
              </div>
            </div>

            {/* 6. 최신 트렌드 */}
            <div>
              <h3 className="text-2xl font-bold mb-4 text-yellow-300">📡 최신 트렌드</h3>
              <div className="text-gray-300 space-y-4 leading-relaxed text-base">
                <p>
                  에볼루션카지노는 매 분기 새로운 게임을 출시하며 업계 트렌드를 선도합니다.
                  <strong className="text-white">2026년 신규 출시 게임</strong> 미리보기,
                  암호화폐(비트코인·이더리움) 결제 도입 현황,
                  AI 딜러 기술 도입 가능성 등 최신 업계 동향을 가장 빠르게 전달합니다.
                </p>
                <p>
                  한국 시장을 겨냥한 <strong className="text-white">코리안 테이블</strong> 확대,
                  아시아 스튜디오 신설 계획, 글로벌 규제 변화가 한국 플레이어에게 미치는 영향까지
                  실용적인 최신 정보를 지속적으로 업데이트합니다.
                </p>
              </div>
            </div>

            {/* 7. 자금 관리 */}
            <div>
              <h3 className="text-2xl font-bold mb-4 text-yellow-300">💰 자금 관리</h3>
              <div className="text-gray-300 space-y-4 leading-relaxed text-base">
                <p>
                  장기적으로 에볼루션카지노를 즐기기 위한 핵심은 <strong className="text-white">철저한 자금 관리</strong>입니다.
                  뱅크롤 관리의 황금 법칙인 '1% 룰', 세션별 손실 한도 설정법,
                  입출금 시스템의 구조와 안전한 자금 이동 방법을 초보자도 이해하기 쉽게 설명합니다.
                </p>
                <p>
                  베팅 시스템(마틴게일·파롤리·달랑베르)의 장단점과 실제 시뮬레이션 결과,
                  <strong className="text-white">손익분기점 계산법</strong>,
                  롤링 요건 이해와 보너스 함정 피하는 방법까지 실질적인 자금 보호 전략을 다룹니다.
                </p>
              </div>
            </div>

            {/* 8. 보안 및 라이선스 */}
            <div>
              <h3 className="text-2xl font-bold mb-4 text-yellow-300">🔒 보안 및 라이선스</h3>
              <div className="text-gray-300 space-y-4 leading-relaxed text-base">
                <p>
                  에볼루션카지노는 <strong className="text-white">MGA(몰타 게임청)</strong>,
                  <strong className="text-white">UKGC(영국 도박위원회)</strong> 등 세계 최고 권위의
                  라이선스를 보유하고 있습니다. 각 라이선스의 의미와 플레이어 보호 수준,
                  RNG(난수생성기) 인증 기관인 GLI·eCOGRA의 검증 과정을 상세히 설명합니다.
                </p>
                <p>
                  256비트 SSL 암호화, 개인정보 보호 정책, 의심스러운 사이트를 구별하는
                  <strong className="text-white">정품 에볼루션 사이트 확인 방법</strong>까지
                  안전하게 게임을 즐기기 위한 모든 보안 지식을 제공합니다.
                </p>
              </div>
            </div>

            {/* 9. 모바일 최적화 */}
            <div>
              <h3 className="text-2xl font-bold mb-4 text-yellow-300">📱 모바일 최적화</h3>
              <div className="text-gray-300 space-y-4 leading-relaxed text-base">
                <p>
                  에볼루션카지노 전체 트래픽의 <strong className="text-white">60% 이상이 모바일</strong>에서 발생합니다.
                  iOS·Android 기기별 최적 설정법, 끊김 없는 스트리밍을 위한 네트워크 환경 구성,
                  Wi-Fi vs LTE 환경에서의 화질 차이와 데이터 소비량을 실측 데이터로 비교합니다.
                </p>
                <p>
                  세로 모드 최적화된 게임 목록, <strong className="text-white">저사양 기기에서도 원활한 플레이</strong>를
                  위한 브라우저 캐시 관리법, 배터리 절약 모드에서의 게임 품질 유지 방법까지
                  모바일 플레이어를 위한 실용적인 가이드를 제공합니다.
                </p>
              </div>
            </div>
          </div>
        </section>
      </main>
    </>
  )
}