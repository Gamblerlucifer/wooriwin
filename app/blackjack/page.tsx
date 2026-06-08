import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'
import { readFileSync, readdirSync, existsSync } from 'fs'
import { join } from 'path'

// ─── 타입 정의 (③ 코드 품질 개선: as any 제거) ───────────────────────────
interface FAQItem {
  '@type': 'Question'
  name: string
  acceptedAnswer: {
    '@type': 'Answer'
    text: string
  }
}

interface Variant {
  name: string
  desc: string
  rtp: string
}

interface RelatedLink {
  href: string
  label: string
}


// ─── 메타데이터 ────────────────────────────────────────────────────────────
export const metadata: Metadata = {
  title: '에볼루션카지노 블랙잭 완벽 가이드 2026 | WOORIWIN',
  description: '에볼루션카지노 블랙잭 규칙·전략·베이직 스트래티지 완벽 정리. 인피니트 블랙잭, 라이트닝 블랙잭, 스피드 블랙잭까지 변형 게임 총망라. 초보자도 이해하는 블랙잭 완전 공략.',
  keywords: ['에볼루션카지노 블랙잭', '에볼루션 블랙잭', '블랙잭 전략', '블랙잭 규칙'],
  alternates: { canonical: 'https://wooriwin.com/blackjack' },
  openGraph: {
    title: '에볼루션카지노 블랙잭 완벽 가이드 2026 | WOORIWIN',
    description: '에볼루션 블랙잭 규칙·전략·변형 게임 완벽 정리.',
    url: 'https://wooriwin.com/blackjack',
    images: [{ url: 'https://wooriwin.com/images/blackjack.jpg', width: 1200, height: 630 }],
  },
  twitter: {
    card: 'summary_large_image',
    title: '에볼루션카지노 블랙잭 완벽 가이드 2026 | WOORIWIN',
    description: '에볼루션 블랙잭 규칙·전략·변형 게임 완벽 정리.',
    images: ['https://wooriwin.com/images/blackjack.jpg'],
  },
}

// ─── JSON-LD (① SEO 개선: author/datePublished/dateModified 추가, 스키마 분리) ─
const jsonLdArticle = {
  '@context': 'https://schema.org',
  '@type': 'TechArticle',
  headline: '에볼루션카지노 블랙잭 완벽 가이드 2026',
  description: '에볼루션카지노 블랙잭 규칙, 전략, 변형 게임 완벽 정리',
  url: 'https://wooriwin.com/blackjack',
  image: 'https://wooriwin.com/images/blackjack.jpg',
  inLanguage: 'ko-KR',
  datePublished: '2026-05-01T09:00:00+09:00',
  dateModified: '2026-05-10T09:00:00+09:00',
  author: {
    '@type': 'Organization',
    name: 'WOORIWIN 팀',
    url: 'https://wooriwin.com/about',
  },
  publisher: {
    '@type': 'Organization',
    name: 'WOORIWIN',
    url: 'https://wooriwin.com',
    logo: {
      '@type': 'ImageObject',
      url: 'https://wooriwin.com/images/logo.png',
    },
  },
}

const jsonLdBreadcrumb = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [
    { '@type': 'ListItem', position: 1, name: '홈', item: 'https://wooriwin.com' },
    { '@type': 'ListItem', position: 2, name: '블랙잭', item: 'https://wooriwin.com/blackjack' },
  ],
}

const jsonLdFaq = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: '에볼루션카지노 블랙잭 RTP는 얼마인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        // ① SEO/YMYL: 출처 표기
        text: '에볼루션 블랙잭의 RTP는 기본 전략 사용 시 약 99.28%입니다. 카지노 게임 중 가장 높은 환수율에 속하며, 기본 전략(Basic Strategy)을 따를 경우 하우스 엣지는 약 0.5% 수준입니다. (출처: Evolution Gaming 공식 게임 수학 문서)',
      },
    },
    {
      '@type': 'Question',
      name: '인피니트 블랙잭이란 무엇인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '인피니트 블랙잭(Infinite Blackjack)은 에볼루션의 대표 블랙잭 변형 게임으로, 한 테이블에 무제한 플레이어가 동시에 착석할 수 있습니다. 모든 플레이어가 동일한 두 장의 카드를 받아 시작하지만, 이후 Hit·Stand·Double·Split 결정은 개인이 독립적으로 내립니다.',
      },
    },
    {
      '@type': 'Question',
      name: '블랙잭 기본 전략이란 무엇인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '기본 전략(Basic Strategy)은 플레이어의 핸드와 딜러의 업카드 조합에 따라 통계적으로 최적의 행동(Hit/Stand/Double/Split)을 도표로 정리한 것입니다. 이를 완벽히 따르면 하우스 엣지를 0.5% 이하로 낮출 수 있습니다. 온라인 블랙잭에서는 기본 전략표를 옆에 두고 참조하며 플레이할 수 있습니다.',
      },
    },
    {
      '@type': 'Question',
      name: '블랙잭에서 언제 더블다운을 해야 하나요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '기본 전략에 따르면, 플레이어 핸드가 11점일 때는 딜러 업카드에 상관없이 더블다운 확률이 높습니다. 10점 핸드는 딜러가 9 이하일 때, 9점 핸드는 딜러가 3~6일 때 더블다운을 고려할 수 있습니다. 소프트 핸드(A 포함)는 별도 규칙이 적용됩니다.',
      },
    },
    {
      '@type': 'Question',
      name: '에볼루션 스피드 블랙잭은 어떤 게임인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '스피드 블랙잭은 모든 플레이어가 동시에 Hit/Stand 결정을 내리는 빠른 진행 변형 게임입니다. 순서 대기 없이 동시에 결정하기 때문에 라운드 시간이 대폭 단축됩니다. 규칙과 RTP는 일반 블랙잭과 동일합니다.',
      },
    },
    {
      '@type': 'Question',
      name: '블랙잭에서 페어(Pair)는 언제 스플릿해야 하나요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'AA(에이스 페어)와 88(8 페어)는 항상 스플릿합니다. 반면 TT(10 페어)와 55(5 페어)는 절대 스플릿하지 않습니다. 99는 딜러가 7, T, A를 제외한 경우 스플릿이 유리합니다. 기본 전략표를 참조하면 모든 페어 상황의 최적 결정을 확인할 수 있습니다.',
      },
    },
    {
      '@type': 'Question',
      name: '에볼루션 라이트닝 블랙잭이란 무엇인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '라이트닝 블랙잭은 매 라운드마다 특정 핸드에 멀티플라이어가 적용되는 변형 게임입니다. 자연 블랙잭(Ace+10)에 대해 추가 배당이 붙을 수 있으며, 기본 베팅에 대한 추가 비용이 발생하는 대신 더 큰 당첨금의 기회를 제공합니다.',
      },
    },
    {
      '@type': 'Question',
      name: '블랙잭에서 보험(Insurance)은 들어야 하나요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '블랙잭 보험(Insurance)은 딜러 업카드가 A일 때 제공되며 블랙잭에 대한 2:1 배당을 제공합니다. 하지만 카드 카운팅을 하지 않는 일반 플레이어에게 보험은 하우스 엣지가 7.69%로 매우 높은 불리한 베팅입니다. 기본 전략에서는 보험 베팅을 하지 않도록 권장합니다.',
      },
    },
  ] as FAQItem[],
}

const variants: Variant[] = [
  { name: '인피니트 블랙잭', desc: '무제한 동시 착석. 좌석 부족 걱정 없는 에볼루션 대표작.', rtp: 'RTP 99.51%' },
  { name: '스피드 블랙잭', desc: '동시 결정 방식으로 라운드 시간 50% 단축. 빠른 진행.', rtp: 'RTP 99.28%' },
  { name: '라이트닝 블랙잭', desc: '자연 블랙잭에 멀티플라이어 적용. 최대 25x 당첨 가능.', rtp: 'RTP 99.56%' },
  { name: '파워 블랙잭', desc: '더블다운·스플릿 규칙 변형. 고급 전략 플레이어용.', rtp: 'RTP 98.80%' },
  { name: 'VIP 블랙잭', desc: '고액 베팅 전용 테이블. 프라이빗 환경에서 집중 플레이.', rtp: 'RTP 99.28%' },
  { name: '프리베 블랙잭', desc: '살롱 프리베 VIP 전용 테이블. 한도 협의 가능.', rtp: '고액 전용' },
]


const POSTS_DIR = join(process.cwd(), 'data', 'posts')

function getRelatedBlogPosts(categories: string[], count = 3) {
  if (!existsSync(POSTS_DIR)) return []
  return readdirSync(POSTS_DIR)
    .filter((f) => f.endsWith('.json'))
    .map((f) => JSON.parse(readFileSync(join(POSTS_DIR, f), 'utf-8')))
    .filter((p) => categories.includes(p.category))
    .sort((a, b) => new Date(b.date).getTime() - new Date(a.date).getTime())
    .slice(0, count)
}

export default function BlackjackPage() {
  const faqList: FAQItem[] = jsonLdFaq.mainEntity
  const relatedPosts = getRelatedBlogPosts(['블랙잭 가이드'], 3)

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdArticle) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdFaq) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdBreadcrumb) }} />
      <main className="min-h-screen bg-gray-900 text-white">

        <section className="relative flex flex-col items-center justify-center min-h-[55vh] text-center px-4 py-20 overflow-hidden">
          <div className="absolute inset-0 z-0">
            <Image src="/images/blackjack.jpg" alt="에볼루션카지노 블랙잭 라이브 테이블" fill className="object-cover opacity-25" priority />
          </div>
          <div className="relative z-10 max-w-4xl mx-auto">
            <nav aria-label="breadcrumb" className="text-sm text-gray-400 mb-6">
              <Link href="/" className="hover:text-yellow-400">홈</Link> &rsaquo; <span className="text-white" aria-current="page">블랙잭</span>
            </nav>
            <p className="text-sm text-yellow-400 font-semibold tracking-widest uppercase mb-4">RTP 99.28% · 카지노 최고 환수율</p>
            <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
              에볼루션카지노 블랙잭<br />
              <span className="text-yellow-400">완벽 가이드 2026</span>
            </h1>
            <p className="text-lg text-gray-300 max-w-2xl mx-auto leading-relaxed">
              블랙잭의 기본 전략, 블랙잭 메커니즘, 블랙잭 의사결졍, 에볼루션카지노 블랙잭의 모든 것을 정리했습니다.
            </p>
          </div>
        </section>

        <section className="max-w-4xl mx-auto px-4 py-20 text-gray-300">
          {/* ① SEO: 정보 최신성 고지 */}
          <p className="text-xs text-gray-500 mb-8 text-right">본 정보는 2026년 5월 기준이며, 실제 게임 수치는 운영사 정책에 따라 변동될 수 있습니다.</p>

          {/* 메인 헤드라인 */}
          <header className="mb-16 border-b border-gray-800 pb-8">
            <div className="flex items-center space-x-3 mb-4">
              <span className="bg-yellow-400 text-black px-3 py-1 rounded-full text-sm font-bold uppercase tracking-wider">Strategy Game</span>
            </div>
            {/* E-E-A-T: 저자 */}
            <div className="flex items-center gap-3 text-sm text-gray-500 mb-6">
            <div className="flex items-center gap-3 text-sm text-gray-500 mb-6">
              <span>작성자</span>
              <Link href="/about" className="text-yellow-400 hover:underline font-semibold">WOORIWIN 팀</Link>
              <span>·</span>
              <span>라이브카지노 전문 애널리스트 · Evolution 공식 자료 기반 검수</span>
            </div>
            </div>
            <h2 className="text-2xl md:text-3xl font-extrabold mb-6 text-white border-b border-gray-800 pb-4">
              에볼루션 블랙잭: <span className="text-yellow-400 text-xl md:text-2xl">0.5%의 하우스 엣지에 도전하는 기술</span>
            </h2>
            <p className="text-xl text-gray-400 leading-relaxed">
              에볼루션 블랙잭은 수학적 확률 구조를 이해하고 게임에 접근할 수 있는 라이브 카지노 타이틀입니다.
            </p>
          </header>

          <div className="space-y-16 text-base md:text-lg leading-relaxed">
            
            {/* 섹션 1: 블랙잭의 본질과 수학적 신뢰성 */}
            <article className="prose prose-invert max-w-none">
              <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
                <span className="text-yellow-400 mr-3">#01</span> 99.28%의 수익률, 그 메커니즘
              </h3>
              {/* ① SEO/YMYL: 출처 표기 */}
              <p className="text-xs text-gray-500 text-center mb-4">출처: Evolution Gaming 공식 게임 수학 문서 (2026년 기준)</p>
              <p className="mb-6">
                에볼루션카지노 블랙잭이 전 세계 전략가들의 성지가 된 이유는 명확합니다. 완벽한 <strong>기본 전략(Basic Strategy)</strong>을 구사할 경우, 하우스 엣지(카지노의 이익률)를 0.5% 미만으로 억제할 수 있기 때문입니다. 이는 온라인에서 즐길 수 있는 모든 카지노 게임 중 플레이어에게 가장 유리한 수치입니다.
              </p>
              <p className="mb-6">
                모든 에볼루션 블랙잭 게임은{' '}
                {/* YMYL: eCOGRA 인증 링크 추가 */}
                <a href="https://ecogra.org" target="_blank" rel="noopener noreferrer" className="text-yellow-400 underline hover:text-yellow-300">
                  <strong>eCOGRA</strong>
                </a>
                와 같은 국제 공인 기관의 정기적인 감사를 받으며, RTP 수치는 조작이 불가능한 물리적 기반 위에 서 있습니다.
              </p>
              <div className="bg-gray-900/60 p-6 rounded-xl border-l-4 border-yellow-400 mb-6 text-sm md:text-base">
                <p><strong>점수 계산의 핵심:</strong></p>
                <ul className="list-disc ml-6 space-y-2 mt-2">
                  <li><strong>A (Ace):</strong> 상황에 따라 1 또는 11로 유연하게 활용 (소프트 핸드의 핵심)</li>
                  <li><strong>10·J·Q·K:</strong> 모두 10점으로 계산 (덱의 약 30.7%를 차지하는 가장 중요한 카드군)</li>
                  <li><strong>블랙잭(Natural):</strong> 첫 두 장으로 21을 완성 시 베팅액의 1.5배(3:2) 지급</li>
                </ul>
              </div>
            </article>

              {/* 섹션 2: RTP 분석 */}
              <article className="bg-gray-800/30 p-8 rounded-2xl border border-gray-700">
                <h3 className="text-xl font-bold text-yellow-400 mb-6 text-center underline underline-offset-8">
                  PRO ANALYSIS: 베팅 타입별 기대 수익률(RTP)
                </h3>
             <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                  <div className="bg-black/40 p-5 rounded-xl text-center border border-gray-600">
                    <p className="text-gray-400 text-sm mb-2">21 + 3</p>
                    <p className="text-3xl font-black text-green-400">96.30%</p>
                    <p className="text-xs mt-2 text-gray-500">하우스 엣지 3.70%</p>
                  </div>
                  <div className="bg-black/40 p-5 rounded-xl text-center border border-gray-600">
                    <p className="text-gray-400 text-sm mb-2">퍼펙트 페어 (Perfect Pairs)</p>
                    <p className="text-3xl font-black text-blue-400">95.90%</p>
                    <p className="text-xs mt-2 text-gray-500">하우스 엣지 4.10%</p>
                  </div>
                  <div className="bg-black/40 p-5 rounded-xl text-center border border-gray-600">
                    <p className="text-gray-400 text-sm mb-2">애니 페어 (Any Pair)</p>
                    <p className="text-3xl font-black text-red-400">95.90%</p>
                    <p className="text-xs mt-2 text-red-500">하우스 엣지 4.10%</p>
                  </div>
              </div>
              <blockquote className="border-l-4 border-gray-500 pl-4 italic text-sm text-gray-400 mb-4">
                "21+3 엣지 3.70%, 퍼텍트 페어 4.10%, 애니페어 4.10% — 베팅 유형별 하우스 엣지 수치를 이해하고 본인의 플레이 환경에 맞는 선택을 하는 것이 중요합니다. 신중한 자금 관리가 모든 게임의 기본입니다."
              </blockquote>
              {/* YMYL: RTP 출처 */}
              <p className="text-xs text-gray-600 mb-4">
                ※ RTP 수치 출처:{' '}
                <a href="https://www.evolution.com" target="_blank" rel="noopener noreferrer" className="underline hover:text-gray-400">
                  Evolution Gaming 공식 게임 수학 문서
                </a>
                . 수치는 이론적 기댓값이며 실제 결과와 다를 수 있습니다.
              </p>
              {/* YMYL: 손실 위험 경고 */}
              <div className="bg-red-950/40 border border-red-800/50 rounded-lg px-5 py-3 text-xs text-red-300">
                <span aria-hidden="true">⚠️</span> <strong>손실 위험 안내:</strong> 모든 카지노 게임은 장기적으로 하우스 엣지가 존재하며, 손실이 발생할 수 있습니다. RTP가 높은 게임도 단기 손실을 보장하지 않습니다. 자신의 재정 범위 내에서만 게임을 즐기시기 바랍니다.
              </div>
            </article>

            {/* 섹션 3: 승률 극대화를 위한 '기본 전략'의 심층 분석 */}
            <article>
              <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
                <span className="text-yellow-400 mr-3">#02</span> 의사결정의 기술: Hit, Stand, or Double?
              </h3>
              <p className="mb-8">
                블랙잭은 단순히 21에 가깝게 만드는 게임이 아닙니다. <strong>'딜러가 버스트(21 초과)될 확률'</strong>을 계산하는 게임입니다. 에볼루션의 라이브 환경에서는 실시간으로 통계 데이터를 확인할 수 있어 최적의 판단이 가능합니다.
              </p>
              
              <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div className="bg-black/40 p-6 rounded-2xl border border-gray-700 hover:border-yellow-400 transition-colors">
                  <h4 className="text-white font-bold text-lg mb-3">더블다운(Double Down)</h4>
                  <p className="text-sm text-gray-400">
                    승률이 압도적으로 높을 때 베팅액을 2배로 증폭시키세요. 보통 합계가 10이나 11일 때, 딜러의 업카드가 2~6 사이라면 주저 없이 선택해야 합니다. 에볼루션은 모든 합계에서 더블다운을 허용하여 공격적인 플레이를 지원합니다.
                  </p>
                </div>
                <div className="bg-black/40 p-6 rounded-2xl border border-gray-700 hover:border-yellow-400 transition-colors">
                  <h4 className="text-white font-bold text-lg mb-3">스플릿(Split) 전략</h4>
                  <p className="text-sm text-gray-400">
                    기본 전략상 <strong>AA와 88은 스플릿</strong>선택지가 높습니다. 반면, 10-10(20점)은 일반적으로 스플릿하지 않는 것으로 안내됩니다. 에볼루션은 스플릿 후 리스플릿 기능을 통해 전략적 유연성을 더해줍니다.
                  </p>
                </div>
              </div>

              {/* YMYL: 독립 시행 경고 */}
              <div className="rounded-xl p-5 mt-6" style={{ background: 'rgba(120,20,20,0.2)', border: '1px solid rgba(180,30,30,0.3)' }}>
                <p className="text-sm" style={{ color: '#fca5a5' }}>
                  기본 전략은 장기적으로 하우스 엣지를 최소화하지만, 단기 손실을 완전히 방지하지는 않습니다.
                  각 핸드는 독립 시행이며, 이전 결과는 다음 결과에 영향을 주지 않습니다.
                </p>
              </div>
            </article>

            {/* 섹션 4: 진화된 라인업 - 인피니트 & 라이트닝 */}
            <article className="bg-gray-800/20 p-8 rounded-3xl border border-gray-800 shadow-2xl">
              <h3 className="text-2xl font-bold text-white mb-8 italic">Evolution Innovation: 미래형 블랙잭</h3>
              
              <div className="space-y-10">
                <div className="flex flex-col md:flex-row gap-6 items-start">
                  <div className="w-full md:w-1/3">
                    <h4 className="text-yellow-400 font-extrabold text-xl mb-2">인피니트 블랙잭</h4>
                    <span className="text-xs border border-yellow-400/50 px-2 py-0.5 rounded text-yellow-400 uppercase">Unlimited Seats</span>
                  </div>
                  <div className="w-full md:w-2/3">
                    <p className="text-sm text-gray-300">
                      만석을 기다릴 필요가 없습니다. 무제한 플레이어가 동시에 참여하며, 모든 플레이어는 공통의 카드로 시작하지만 <strong>결과는 각자의 전략</strong>에 따라 달라집니다. 특히 '6-Card Charlie' 룰(6장을 받을 때까지 버스트되지 않으면 무조건 승리)이 적용되어 색다른 재미를 선사합니다.
                    </p>
                  </div>
                </div>

                <div className="flex flex-col md:flex-row gap-6 items-start">
                  <div className="w-full md:w-1/3">
                    <h4 className="text-yellow-400 font-extrabold text-xl mb-2">라이트닝 블랙잭</h4>
                    <span className="text-xs border border-yellow-400/50 px-2 py-0.5 rounded text-yellow-400 uppercase">Multiplier Win</span>
                  </div>
                  <div className="w-full md:w-2/3">
                    <p className="text-sm text-gray-300">
                      블랙잭에 '폭발적 수익'을 더했습니다. 매 라운드 승리 시 다음 라운드에 적용되는 <strong>2배~25배의 멀티플라이어</strong>를 획득할 수 있습니다. 놀라운 점은 이러한 고배당 룰을 유지하면서도 RTP를 99.56%까지 끌어올려, 흥행과 수익률이라는 두 마리 토끼를 모두 잡았다는 점입니다.
                    </p>
                  </div>
                </div>
              </div>
            </article>
          </div>
        </section>

        <section className="bg-gray-800 py-16 px-4">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-3">에볼루션 블랙잭 변형 게임</h2>
            <p className="text-gray-400 text-center mb-10">에볼루션이 제공하는 6가지 블랙잭 변형 게임</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              {variants.map((v) => (
                <div key={v.name} className="bg-gray-900 rounded-xl p-5 border border-gray-700 hover:border-yellow-400 transition">
                  <h3 className="text-yellow-400 font-bold text-base mb-2">{v.name}</h3>
                  <p className="text-gray-400 text-sm mb-3">{v.desc}</p>
                  <span className="text-xs text-gray-500 font-mono">{v.rtp}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 관련 블로그 글 */}
        {relatedPosts.length > 0 && (
          <section className="bg-gray-800 py-16 px-4">
            <div className="max-w-5xl mx-auto">
              <h2 className="text-3xl font-bold text-center mb-3">에볼루션카지노 블랙잭 관련 글</h2>
              <p className="text-gray-400 text-center mb-10">더 깊이 있는 정보를 블로그에서 확인하세요</p>
              <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
                {relatedPosts.map((post) => (
                  <Link
                    key={post.slug}
                    href={`/blog/${post.slug}`}
                    className="group block bg-gray-900 rounded-xl overflow-hidden border border-gray-700 hover:border-yellow-400 transition"
                  >
                    <div className="relative h-40 overflow-hidden">
                      <Image
                        src={post.image}
                        alt={post.imageAlt || post.title}
                        fill
                        loading="lazy"
                        className="object-cover opacity-70 group-hover:scale-105 transition-transform"
                        sizes="(max-width: 640px) 100vw, (max-width: 1024px) 50vw, 33vw"
                      />
                    </div>
                    <div className="p-5">
                      <p className="text-sm font-bold mb-2 leading-snug line-clamp-2 text-white group-hover:text-yellow-400 transition">
                        {post.title}
                      </p>
                      <p className="text-xs text-gray-400 line-clamp-2 mb-2">{post.description}</p>
                      <p className="text-xs text-gray-500">{post.date}</p>
                    </div>
                  </Link>
                ))}
              </div>
              <div className="text-center mt-10">
                <Link href="/blog" className="text-yellow-400 hover:underline text-sm font-medium">전체 블로그 글 보기 →</Link>
              </div>
            </div>
          </section>
        )}

        <section className="max-w-4xl mx-auto px-4 py-16">
          <h2 className="text-3xl font-bold mb-10 text-center">에볼루션카지노 블랙잭 FAQ</h2>
          <div className="space-y-4">
            {faqList.map((faq: FAQItem) => (
              <details key={faq.name} className="bg-gray-800 rounded-xl p-5 group cursor-pointer">
                <summary className="font-semibold text-base text-white flex justify-between items-center list-none">
                  {faq.name}
                  <span className="text-yellow-400 text-xl transition-transform group-open:rotate-45" aria-hidden="true">+</span>
                </summary>
                <p className="mt-4 text-gray-400 text-sm leading-relaxed">{faq.acceptedAnswer.text}</p>
              </details>
            ))}
          </div>
        </section>
      </main>
    </>
  )
}
