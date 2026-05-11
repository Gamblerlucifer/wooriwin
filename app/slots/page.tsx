import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'

// ─── 타입 정의 ───────────────────────────────────────────────
type FAQItem = {
  '@type': 'Question'
  name: string
  acceptedAnswer: { '@type': 'Answer'; text: string }
}

type GameShow = {
  name: string
  desc: string
  rtp: string
}

// ─── 메타데이터 ──────────────────────────────────────────────
export const metadata: Metadata = {
  title: '에볼루션카지노 슬롯 완벽 가이드 2026 | WOORIWIN',
  description:
    '에볼루션카지노 슬롯·게임쇼 완벽 가이드. NetEnt·Red Tiger 슬롯 RTP 비교부터 크레이지타임·모노폴리 라이브 게임쇼 공략까지 총망라. 초보자도 쉽게 이해하는 가이드.',
  keywords: ['에볼루션카지노 슬롯', '에볼루션 슬롯', '크레이지타임', '모노폴리 라이브', '에볼루션 게임쇼', '라이브 슬롯'],
  alternates: { canonical: 'https://wooriwin.com/slots' },
  openGraph: {
    title: '에볼루션카지노 슬롯 완벽 가이드 2026 | WOORIWIN',
    description:
      '크레이지타임·모노폴리 라이브 등 에볼루션 슬롯·게임쇼 완벽 정리. NetEnt·Red Tiger 슬롯까지 총망라.',
    url: 'https://wooriwin.com/slots',
    type: 'article',
    images: [{ url: 'https://wooriwin.com/images/slots.jpg', width: 1200, height: 630 }],
  },
  twitter: {
    card: 'summary_large_image',
    title: '에볼루션카지노 슬롯 완벽 가이드 2026 | WOORIWIN',
    description:
      '크레이지타임·모노폴리 라이브 등 에볼루션 슬롯·게임쇼 완벽 정리. NetEnt·Red Tiger 슬롯까지 총망라.',
    images: ['https://wooriwin.com/images/slots.jpg'],
  },
}

// ─── JSON-LD ─────────────────────────────────────────────────
const jsonLdArticle = {
  '@context': 'https://schema.org',
  '@type': 'Article',
  headline: '에볼루션카지노 슬롯 완벽 가이드 2026',
  description: '에볼루션카지노 슬롯·게임쇼 완벽 가이드. NetEnt·Red Tiger 슬롯 RTP 비교, 크레이지타임·모노폴리 라이브 공략.',
  url: 'https://wooriwin.com/slots',
  image: 'https://wooriwin.com/images/slots.jpg',
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

const jsonLdFaq = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: '에볼루션카지노 슬롯과 라이브 게임의 차이는?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '에볼루션카지노의 슬롯은 RNG(난수생성기) 기반의 디지털 게임으로 NetEnt·Red Tiger·Nolimit City 등 계열사 브랜드가 제공합니다. 라이브 게임은 실제 딜러가 실시간 진행하는 게임입니다. 게임쇼(크레이지타임 등)는 라이브 게임이지만 슬롯 요소가 결합된 하이브리드 형식입니다.',
      },
    },
    {
      '@type': 'Question',
      name: '크레이지타임이란 무엇인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '크레이지타임(Crazy Time)은 에볼루션의 대표 라이브 게임쇼입니다. 거대한 머니 휠을 스핀하여 착지 칸에 따라 배당을 받거나 4가지 보너스 게임(캐시 헌트·코인 플립·퍼시피코·크레이지타임)에 진입합니다. 크레이지타임 보너스의 최대 당첨은 이론상 2만배 이상입니다.',
      },
    },
    {
      '@type': 'Question',
      name: '에볼루션 슬롯 RTP는 평균 얼마인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: "에볼루션 계열(NetEnt·Red Tiger) 슬롯의 평균 RTP는 96% 전후입니다. 인기 타이틀인 Starburst는 96.09%, Gonzo's Quest는 95.97%, Divine Fortune은 96.59%입니다. 일부 고변동성 슬롯은 RTP가 97~98%에 달하지만 잭팟에 집중된 구조입니다.",
      },
    },
    {
      '@type': 'Question',
      name: '모노폴리 라이브는 어떤 게임인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '모노폴리 라이브(Monopoly Live)는 에볼루션과 Hasbro가 협력하여 만든 라이브 게임쇼입니다. 머니 휠 스핀 후 보너스에 진입하면 3D 모노폴리 보드게임이 시뮬레이션되며 다수의 당첨 기회를 제공합니다. 보너스 최대 당첨은 수백 배에 달합니다.',
      },
    },
    {
      '@type': 'Question',
      name: '에볼루션 메가볼이란 무엇인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '메가볼(Mega Ball)은 에볼루션의 라이브 복권 스타일 게임입니다. 여러 장의 카드를 구입 후 번호가 추첨되며, 카드에 당첨 번호가 많을수록 더 높은 배당을 받습니다. 메가볼 번호가 추첨되면 최대 1,000,000배까지 멀티플라이어가 적용됩니다.',
      },
    },
    {
      '@type': 'Question',
      name: 'NetEnt와 Red Tiger는 에볼루션과 어떤 관계인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: "NetEnt는 2020년, Red Tiger는 2019년 에볼루션에 인수된 슬롯 제공업체입니다. NetEnt는 Starburst·Gonzo's Quest 등 클래식 슬롯으로 유명하고, Red Tiger는 고변동성 메가웨이즈 슬롯으로 유명합니다. 에볼루션 라이선스 카지노에서 이 브랜드 슬롯도 함께 이용 가능합니다.",
      },
    },
    {
      '@type': 'Question',
      name: '에볼루션 드림 캐처란 무엇인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '드림 캐처(Dream Catcher)는 에볼루션 최초의 라이브 머니 휠 게임쇼입니다. 1·2·5·10·20·40 배당이 표시된 대형 수직 휠을 스핀하여 착지 칸의 배당을 받습니다. 2x·7x 멀티플라이어 칸이 있어 연속 적용 시 높은 배당을 기대할 수 있습니다.',
      },
    },
    {
      '@type': 'Question',
      name: '에볼루션 슬롯은 모바일에서 이용 가능한가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '에볼루션 계열 슬롯은 HTML5 기반으로 iOS·Android 모바일 브라우저에서 별도 앱 설치 없이 이용 가능합니다. 라이브 게임쇼(크레이지타임·모노폴리 라이브 등)도 모바일에 완전 최적화되어 있습니다.',
      },
    },
  ] satisfies FAQItem[],
}

// ─── BreadcrumbList JSON-LD ──────────────────────────────────
const jsonLdBreadcrumb = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [
    { '@type': 'ListItem', position: 1, name: '홈', item: 'https://wooriwin.com' },
    { '@type': 'ListItem', position: 2, name: '슬롯', item: 'https://wooriwin.com/slots' },
  ],
}

// ─── 데이터 ──────────────────────────────────────────────────
const gameShows: GameShow[] = [
  { name: '크레이지타임', desc: '에볼루션 최고 인기 게임쇼. 최대 2만배+ 보너스 당첨.', rtp: 'RTP 96.08%' },
  { name: '모노폴리 라이브', desc: 'Hasbro 협력 3D 보드게임 결합 라이브 쇼.', rtp: 'RTP 96.23%' },
  { name: '드림 캐처', desc: '에볼루션 최초 머니 휠. 최대 7x 멀티플라이어.', rtp: 'RTP 96.58%' },
  { name: '메가볼', desc: '복권 스타일 게임. 최대 100만배 멀티플라이어.', rtp: 'RTP 95.05%' },
  { name: '딜 오어 노딜', desc: 'TV쇼 원작 라이브 게임. 최대 500배 당첨.', rtp: 'RTP 95.42%' },
  { name: '퍼시피코', desc: '크레이지타임 보너스 게임 독립 버전. 산 정상 등반 컨셉.', rtp: 'RTP 96.00%' },
]

// ─── 페이지 컴포넌트 ─────────────────────────────────────────
export default function SlotsPage() {
  const faqList: FAQItem[] = jsonLdFaq.mainEntity

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdArticle) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdFaq) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdBreadcrumb) }} />
      <main className="min-h-screen bg-gray-900 text-white">

        {/* Hero */}
        <section className="relative flex flex-col items-center justify-center min-h-[55vh] text-center px-4 py-20 overflow-hidden">
          <div className="absolute inset-0 z-0">
            <Image src="/images/slots.jpg" alt="에볼루션카지노 크레이지타임 게임쇼 휠" fill className="object-cover opacity-25" priority />
          </div>
          <div className="relative z-10 max-w-4xl mx-auto">
            <nav aria-label="breadcrumb" className="text-sm text-gray-400 mb-6">
              <Link href="/" className="hover:text-yellow-400">홈</Link>
              {' '}&rsaquo;{' '}
              <span className="text-white" aria-current="page">슬롯</span>
            </nav>
            <p className="text-sm text-yellow-400 font-semibold tracking-widest uppercase mb-4">크레이지타임 최대 2만배 · NetEnt·Red Tiger 슬롯</p>
            <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
              에볼루션카지노 슬롯<br />
              <span className="text-yellow-400">완벽 가이드 2026</span>
            </h1>
            <p className="text-lg text-gray-300 max-w-2xl mx-auto leading-relaxed">
              크레이지타임·모노폴리 라이브 게임쇼부터 NetEnt·Red Tiger 슬롯까지. 에볼루션 슬롯의 모든 것을 정리했습니다.
            </p>
          </div>
        </section>

        {/* 본문 */}
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
              <span>작성자</span>
              <Link href="/about" className="text-yellow-400 hover:underline font-semibold">WOORIWIN 팀</Link>
              <span>·</span>
              <span>라이브카지노 전문 애널리스트 · Evolution 공식 자료 기반 검수</span>
            </div>
            <h2 className="text-2xl md:text-3xl font-extrabold mb-6 text-white border-b border-gray-800 pb-4">
              에볼루션 슬롯: <span className="text-yellow-400 text-xl md:text-2xl">게임쇼와 슬롯의 경계를 허물다</span>
            </h2>
            <p className="text-xl text-gray-400 leading-relaxed mb-6">
              단순히 릴을 돌리는 슬롯의 시대는 끝났습니다. 에볼루션은 라이브 딜러·대형 세트장·멀티플라이어를 결합한 완전히 새로운 카테고리를 창조했습니다. 크레이지타임은 이론상 최대 20,000배 이상의 보너스 당첨이 가능한 게임입니다.
            </p>
          </header>

          <div className="space-y-16 text-base md:text-lg leading-relaxed">

            {/* 섹션 1 */}
            <article>
              <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
                <span className="text-yellow-400 mr-3">#01</span> 에볼루션 슬롯의 두 가지 세계
              </h3>
              <p className="mb-4">
                에볼루션 슬롯을 처음 접하는 플레이어가 가장 많이 혼동하는 것은 <strong>라이브 게임쇼와 RNG 슬롯의 차이</strong>입니다. 라이브 게임쇼는 실제 딜러와 대형 세트장에서 실시간으로 진행되는 반면, RNG 슬롯은 난수생성기 기반의 전통적인 슬롯 머신입니다. 에볼루션은 NetEnt·Red Tiger·Nolimit City 인수로 두 세계를 모두 장악했습니다. Nolimit City는 xNudge·xWays 등 독자 메카닉을 앞세운 고변동성 슬롯 전문 브랜드로, 대형 당첨을 노리는 플레이어에게 특히 인기입니다.
              </p>
              <p>
                라이브 게임쇼는 엔터테인먼트 요소와 높은 배당 변동성을 제공하며, NetEnt·Red Tiger 슬롯은 안정적인 RTP와 다양한 테마를 특징으로 합니다. 모든 게임의 공정성은{' '}
                <a href="https://ecogra.org" target="_blank" rel="noopener noreferrer" className="text-yellow-400 hover:underline">eCOGRA</a> 등 국제 공인기관의 정기 감사를 통해 검증됩니다.
              </p>
            </article>

            {/* 섹션 2: PRO ANALYSIS */}
            <article className="bg-gray-800/30 p-8 rounded-2xl border border-gray-700">
              <h3 className="text-xl font-bold text-yellow-400 mb-6 text-center underline underline-offset-8">
                PRO ANALYSIS: 에볼루션 슬롯&게임쇼 RTP 비교
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div className="bg-black/40 p-5 rounded-xl text-center border border-gray-600">
                  <p className="text-gray-400 text-sm mb-2">크레이지타임</p>
                  <p className="text-3xl font-black text-green-400">96.08%</p>
                  <p className="text-xs mt-2 text-gray-500">최대 20,000배 보너스</p>
                </div>
                <div className="bg-black/40 p-5 rounded-xl text-center border border-gray-600">
                  <p className="text-gray-400 text-sm mb-2">NetEnt 스타버스트</p>
                  <p className="text-3xl font-black text-blue-400">96.09%</p>
                  <p className="text-xs mt-2 text-gray-500">저변동성 클래식 슬롯</p>
                </div>
                <div className="bg-black/40 p-5 rounded-xl text-center border border-gray-600">
                  <p className="text-gray-400 text-sm mb-2">메가볼</p>
                  <p className="text-3xl font-black text-yellow-400">95.05%</p>
                  <p className="text-xs mt-2 text-red-400">최대 1,000,000배 멀티플라이어</p>
                </div>
              </div>
              <blockquote className="border-l-4 border-gray-500 pl-4 italic text-sm text-gray-400 mb-4">
                "RTP만 보고 슬롯을 선택하는 것은 절반만 맞습니다. 변동성(Volatility)을 함께 확인하세요. 고변동성 슬롯은 당첨 빈도는 낮지만 대형 당첨이 가능합니다. 저변동성은 작은 당첨이 자주 발생해 뱅크롤을 오래 유지할 수 있습니다."
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
                <span aria-hidden="true">⚠️</span> <strong>손실 위험 안내:</strong> 모든 슬롯 및 게임쇼는 장기적으로 하우스 엣지가 존재하며 손실이 발생할 수 있습니다. 크레이지타임 등 고변동성 게임은 당첨 빈도가 낮고 단기 손실이 클 수 있습니다. 자신의 재정 범위 내에서만 게임을 즐기시기 바랍니다.
              </div>
            </article>

            {/* 섹션 3: 게임쇼의 혁명 */}
            <article className="bg-gray-800/20 p-8 rounded-3xl border border-gray-800 shadow-2xl">
              <h3 className="text-2xl font-bold text-white mb-8 italic">Evolution Innovation: 게임쇼의 혁명</h3>
              <div className="space-y-10">
                <div className="flex flex-col md:flex-row gap-6 items-start">
                  <div className="w-full md:w-1/3">
                    <h4 className="text-yellow-400 font-extrabold text-xl mb-2">크레이지타임</h4>
                    <span className="text-xs border border-yellow-400/50 px-2 py-0.5 rounded text-yellow-400 uppercase">Max 20,000x</span>
                  </div>
                  <div className="w-full md:w-2/3">
                    <p className="text-sm text-gray-300">
                      에볼루션 게임쇼의 정점입니다. 거대한 머니 휠 스핀 후 4가지 보너스 게임(캐시 헌트·코인 플립·퍼시피코·크레이지타임) 중 하나에 진입합니다. 특히 <strong>크레이지타임 보너스</strong>는 플래퍼가 달린 대형 휠로 진행되며 이론상 최대 20,000배 이상의 당첨금이 가능합니다.
                    </p>
                  </div>
                </div>
                <div className="flex flex-col md:flex-row gap-6 items-start">
                  <div className="w-full md:w-1/3">
                    <h4 className="text-yellow-400 font-extrabold text-xl mb-2">모노폴리 라이브</h4>
                    <span className="text-xs border border-yellow-400/50 px-2 py-0.5 rounded text-yellow-400 uppercase">Hasbro X Evolution</span>
                  </div>
                  <div className="w-full md:w-2/3">
                    <p className="text-sm text-gray-300">
                      세계적인 보드게임 브랜드 Hasbro와 에볼루션의 협업작입니다. 기본 머니 휠 스핀 후 <strong>2롤스·4롤스 보너스</strong>에 진입하면 3D 모노폴리 보드가 시뮬레이션됩니다. 보드 이동 중 만나는 찬스·공동기금 카드와 고급 부동산이 배당을 폭발적으로 높입니다.
                    </p>
                  </div>
                </div>
                <div className="flex flex-col md:flex-row gap-6 items-start">
                  <div className="w-full md:w-1/3">
                    <h4 className="text-yellow-400 font-extrabold text-xl mb-2">메가볼</h4>
                    <span className="text-xs border border-yellow-400/50 px-2 py-0.5 rounded text-yellow-400 uppercase">Max 1,000,000x</span>
                  </div>
                  <div className="w-full md:w-2/3">
                    <p className="text-sm text-gray-300">
                      라이브 복권 스타일의 독창적인 게임입니다. 여러 장의 카드를 구입하고 번호가 추첨되면 카드에 채워진 번호 줄에 따라 점점 높은 배당을 받습니다. <strong>메가볼 번호</strong>가 추첨될 경우 최대 1,000,000배 멀티플라이어가 적용되는 초대형 당첨의 기회가 있습니다.
                    </p>
                  </div>
                </div>
              </div>
            </article>

            {/* 섹션 4: RNG 슬롯 */}
            <article>
              <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
                <span className="text-yellow-400 mr-3">#04</span> RNG 슬롯: NetEnt·Red Tiger의 세계
              </h3>
              <p className="mb-6">
                에볼루션이 인수한 <strong>NetEnt</strong>는 Starburst·Gonzo's Quest·Divine Fortune 등 수십 년간 사랑받은 클래식 슬롯의 제조사입니다. <strong>Red Tiger</strong>는 메가웨이즈 메카닉을 활용한 고변동성 슬롯으로 대형 당첨을 노리는 플레이어에게 인기입니다.
              </p>
              <div className="bg-black/50 p-6 rounded-xl border border-gray-800">
                <h4 className="text-white font-bold mb-4">슬롯 선택 체크리스트</h4>
                <ul className="grid md:grid-cols-2 gap-3 text-xs md:text-sm">
                  <li className="flex items-center text-gray-400"><span aria-hidden="true">✔</span>&nbsp;RTP 96% 이상 슬롯 우선 선택</li>
                  <li className="flex items-center text-gray-400"><span aria-hidden="true">✔</span>&nbsp;뱅크롤 적을 때는 저변동성 선택</li>
                  <li className="flex items-center text-gray-400"><span aria-hidden="true">✔</span>&nbsp;보너스 구매 기능은 추가 하우스 엣지 유의</li>
                  <li className="flex items-center text-gray-400"><span aria-hidden="true">✔</span>&nbsp;메가웨이즈 슬롯은 고변동성 대형 당첨 노릴 때</li>
                </ul>
              </div>
            </article>
          </div>
        </section>

        {/* 게임쇼 카드 */}
        <section className="bg-gray-800 py-16 px-4">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-3">에볼루션 라이브 게임쇼</h2>
            <p className="text-gray-400 text-center mb-10">에볼루션의 대표 라이브 게임쇼 6종</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              {gameShows.map((g) => (
                <div key={g.name} className="bg-gray-900 rounded-xl p-5 border border-gray-700 hover:border-yellow-400 transition">
                  <h3 className="text-yellow-400 font-bold text-base mb-2">{g.name}</h3>
                  <p className="text-gray-400 text-sm mb-3">{g.desc}</p>
                  <span className="text-xs text-gray-500 font-mono">{g.rtp}</span>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section className="max-w-4xl mx-auto px-4 py-16">
          <h2 className="text-3xl font-bold mb-10 text-center">에볼루션카지노 슬롯 FAQ</h2>
          <div className="space-y-4">
            {faqList.map((faq) => (
              <details key={faq.name} className="bg-gray-800 rounded-xl p-5 group cursor-pointer">
                <summary className="font-semibold text-base text-white flex justify-between items-center list-none">
                  {faq.name}
                  <span aria-hidden="true" className="text-yellow-400 text-xl transition-transform group-open:rotate-45">+</span>
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
