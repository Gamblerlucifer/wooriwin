import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'

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
    siteName: 'WOORIWIN',
    locale: 'ko_KR',
    type: 'website',
    images: [{ url: 'https://wooriwin.com/images/blog.jpg', width: 1200, height: 630 }],
  },
}

const jsonLd = {
  '@context': 'https://schema.org',
  '@type': 'Blog',
  name: 'WOORIWIN 에볼루션카지노 전략 블로그',
  description: '에볼루션카지노 바카라·블랙잭·룰렛 전략, 규칙, 팁 전문 블로그',
  url: 'https://wooriwin.com/blog',
  inLanguage: 'ko-KR',
  publisher: { '@type': 'Organization', name: 'WOORIWIN', url: 'https://wooriwin.com' },
}

// 샘플 포스트 데이터 (나중에 자동 생성 스크립트로 교체)
const samplePosts = [
  {
    slug: 'evolution-baccarat-strategy-2026',
    title: '에볼루션카지노 바카라 전략 총정리 2026 — 뱅커 vs 플레이어 최적 베팅법',
    category: '바카라',
    date: '2026-05-09',
    desc: '에볼루션 바카라에서 장기적으로 수익을 극대화하는 뱅커·플레이어 베팅 전략을 통계와 함께 분석합니다.',
    readTime: '8분',
  },
  {
    slug: 'lightning-roulette-multiplier-guide',
    title: '라이트닝 룰렛 멀티플라이어 완벽 이해 — 500배 당첨 확률과 전략',
    category: '룰렛',
    date: '2026-05-08',
    desc: '라이트닝 룰렛 멀티플라이어의 확률 구조를 분석하고 최적의 베팅 조합 전략을 제시합니다.',
    readTime: '6분',
  },
  {
    slug: 'blackjack-basic-strategy-chart',
    title: '에볼루션 블랙잭 기본 전략표 완벽 가이드 — RTP 99.28% 달성하는 법',
    category: '블랙잭',
    date: '2026-05-07',
    desc: '블랙잭 기본 전략표를 완벽히 이해하고 적용하면 하우스 엣지를 0.5% 이하로 낮출 수 있습니다.',
    readTime: '10분',
  },
  {
    slug: 'crazy-time-bonus-strategy',
    title: '크레이지타임 보너스 게임 전략 — 캐시헌트·코인플립·퍼시피코 완벽 공략',
    category: '슬롯/게임쇼',
    date: '2026-05-06',
    desc: '크레이지타임 4가지 보너스 게임의 확률과 최적 선택 전략을 분석합니다.',
    readTime: '7분',
  },
  {
    slug: 'evolution-casino-signup-guide',
    title: '에볼루션카지노 가입방법 단계별 완벽 가이드 2026',
    category: '가이드',
    date: '2026-05-05',
    desc: '에볼루션 라이선스 카지노 가입부터 첫 입금, 에볼루션 로비 접속까지 단계별로 안내합니다.',
    readTime: '5분',
  },
  {
    slug: 'baccarat-road-reading-guide',
    title: '바카라 빅로드·비드로드 읽는 법 — 에볼루션 바카라 통계 완벽 이해',
    category: '바카라',
    date: '2026-05-04',
    desc: '에볼루션 바카라의 빅로드·비드로드·스몰로드·비그아이보이 통계를 읽고 활용하는 방법을 정리합니다.',
    readTime: '9분',
  },
]

const categories = ['전체', '바카라', '블랙잭', '룰렛', '슬롯/게임쇼', '가이드']

const relatedLinks = [
  { href: '/', label: '에볼루션카지노 메인' },
  { href: '/baccarat', label: '에볼루션카지노 바카라' },
  { href: '/blackjack', label: '에볼루션카지노 블랙잭' },
  { href: '/roulette', label: '에볼루션카지노 룰렛' },
  { href: '/live-casino', label: '에볼루션 라이브카지노' },
]

export default function BlogPage() {
  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <main className="min-h-screen bg-gray-900 text-white">

        {/* Hero */}
        <section className="relative flex flex-col items-center justify-center min-h-[45vh] text-center px-4 py-16 overflow-hidden">
          <div className="absolute inset-0 z-0">
            <Image src="/images/blog.jpg" alt="에볼루션카지노 전략 블로그" fill className="object-cover opacity-20" priority />
          </div>
          <div className="relative z-10 max-w-4xl mx-auto">
            <nav className="text-sm text-gray-400 mb-6">
              <Link href="/" className="hover:text-yellow-400">홈</Link> &rsaquo; <span className="text-white">블로그</span>
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

        {/* 카테고리 탭 */}
        <section className="max-w-5xl mx-auto px-4 py-8">
          <div className="flex flex-wrap gap-2 justify-center">
            {categories.map((cat) => (
              <span
                key={cat}
                className={`px-4 py-2 rounded-full text-sm font-semibold cursor-pointer transition ${
                  cat === '전체'
                    ? 'bg-yellow-400 text-gray-900'
                    : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white'
                }`}
              >
                {cat}
              </span>
            ))}
          </div>
        </section>

        {/* 블로그 포스트 그리드 */}
        <section className="max-w-5xl mx-auto px-4 pb-16">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {samplePosts.map((post) => (
              <Link
                key={post.slug}
                href={`/blog/${post.slug}`}
                className="group bg-gray-800 rounded-xl overflow-hidden hover:bg-gray-700 transition-all hover:shadow-xl hover:shadow-yellow-400/10"
              >
                <div className="p-5">
                  <div className="flex items-center justify-between mb-3">
                    <span className="text-xs font-semibold text-yellow-400 bg-yellow-400/10 px-2 py-1 rounded">
                      {post.category}
                    </span>
                    <span className="text-xs text-gray-500">{post.readTime} 읽기</span>
                  </div>
                  <h2 className="text-base font-bold text-white mb-3 leading-snug group-hover:text-yellow-400 transition line-clamp-2">
                    {post.title}
                  </h2>
                  <p className="text-gray-400 text-sm leading-relaxed line-clamp-3 mb-4">{post.desc}</p>
                  <div className="flex items-center justify-between">
                    <span className="text-xs text-gray-500">{post.date}</span>
                    <span className="text-xs text-yellow-400 font-semibold group-hover:underline">자세히 보기 →</span>
                  </div>
                </div>
              </Link>
            ))}
          </div>

          {/* 더보기 영역 */}
          <div className="text-center mt-12">
            <p className="text-gray-400 text-sm mb-4">매일 새로운 에볼루션카지노 전략 포스트가 업데이트됩니다.</p>
            <div className="inline-block bg-gray-800 border border-gray-700 rounded-xl px-8 py-4 text-gray-500 text-sm">
              🔄 콘텐츠 자동 업데이트 중...
            </div>
          </div>
        </section>

        {/* SEO 본문 텍스트 */}
        <section className="bg-gray-800 py-16 px-4">
          <div className="max-w-4xl mx-auto">
            <h2 className="text-3xl font-bold mb-6 text-yellow-400">에볼루션카지노 전략 블로그 소개</h2>
            <div className="text-gray-300 space-y-5 leading-relaxed text-base">
              <p>
                WOORIWIN 에볼루션카지노 전략 블로그는 <strong className="text-white">바카라·블랙잭·룰렛·슬롯</strong>을 포함한
                에볼루션카지노 모든 게임의 전략, 규칙, 팁을 전문가 수준으로 분석하는 콘텐츠를 제공합니다.
                매일 3건 이상의 새 포스트가 업데이트되어 항상 최신 정보를 확인할 수 있습니다.
              </p>
              <p>
                특히 <strong className="text-white">에볼루션카지노 바카라 전략</strong> 콘텐츠는
                뱅커·플레이어 베팅 확률 분석, 마틴게일·파롤리·1-3-2-6 등 베팅 시스템 비교,
                라이트닝 바카라 멀티플라이어 활용법 등 심층적인 내용을 다룹니다.
              </p>
              <p>
                <strong className="text-white">블랙잭 기본 전략</strong> 포스트에서는 완전한 기본 전략표와
                함께 더블다운·스플릿·서렌더의 최적 타이밍을 상황별로 정리합니다.
                RTP 99.28%를 달성하기 위한 단계별 가이드도 제공합니다.
              </p>
              <p>
                <strong className="text-white">에볼루션카지노 가입방법</strong> 및 입출금 관련 가이드도 충실하게 다룹니다.
                처음 온라인 카지노를 시작하는 초보자도 이해할 수 있도록 단계별로 안내하며,
                안전하고 검증된 카지노 선택 기준도 함께 제공합니다.
              </p>
            </div>
          </div>
        </section>

        <footer className="bg-gray-950 py-10 px-4 text-center">
          <p className="text-gray-500 text-sm mb-4">관련 에볼루션카지노 가이드</p>
          <div className="flex flex-wrap justify-center gap-4 text-sm">
            {relatedLinks.map((l) => (
              <Link key={l.href} href={l.href} className="text-gray-400 hover:text-yellow-400 transition">{l.label}</Link>
            ))}
          </div>
          <p className="text-gray-600 text-xs mt-8">© 2026 WOORIWIN. All rights reserved.</p>
        </footer>
      </main>
    </>
  )
}
