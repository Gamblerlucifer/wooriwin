import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'

// ─── 타입 정의 ───────────────────────────────────────────────
type FAQItem = {
  '@type': 'Question'
  name: string
  acceptedAnswer: { '@type': 'Answer'; text: string }
}

type Feature = {
  icon: string
  title: string
  desc: string
}


// ─── 메타데이터 ──────────────────────────────────────────────
export const metadata: Metadata = {
  title: '에볼루션 라이브카지노 완벽 가이드 2026 | WOORIWIN',
  description:
    '에볼루션 라이브카지노 게임 종류·규칙·전략 완벽 정리. 바카라, 블랙잭, 룰렛, 게임쇼까지 모든 라이브 게임 총망라. 초보자도 쉽게 이해하는 가이드.',
  keywords: ['에볼루션 라이브카지노', '에볼루션카지노 라이브', '라이브카지노', '라이브 딜러 카지노'],
  alternates: { canonical: 'https://wooriwin.com/live-casino' },
  openGraph: {
    title: '에볼루션 라이브카지노 완벽 가이드 2026 | WOORIWIN',
    description:
      '에볼루션 라이브카지노 게임 종류·규칙·전략 완벽 정리. 바카라, 블랙잭, 룰렛, 게임쇼까지 모든 라이브 게임 총망라.',
    url: 'https://wooriwin.com/live-casino',
    images: [{ url: 'https://wooriwin.com/images/live-casino.jpg', width: 1200, height: 630 }],
  },
  twitter: {
    card: 'summary_large_image',
    title: '에볼루션 라이브카지노 완벽 가이드 2026 | WOORIWIN',
    description:
      '에볼루션 라이브카지노 게임 종류·규칙·전략 완벽 정리. 바카라, 블랙잭, 룰렛, 게임쇼까지 모든 라이브 게임 총망라.',
    images: ['https://wooriwin.com/images/live-casino.jpg'],
  },
}

// ─── JSON-LD ─────────────────────────────────────────────────
const jsonLdArticle = {
  '@context': 'https://schema.org',
  '@type': 'Article',
  headline: '에볼루션 라이브카지노 완벽 가이드 2026',
  url: 'https://wooriwin.com/live-casino',
  inLanguage: 'ko-KR',
  datePublished: '2026-01-01',
  dateModified: '2026-05-10',
  author: { '@type': 'Person', name: 'Gambler Lucifer', url: 'https://wooriwin.com/about' },
  publisher: { '@type': 'Organization', name: 'WOORIWIN', url: 'https://wooriwin.com' },
}

const jsonLdFaq = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: '에볼루션 라이브카지노란 무엇인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '에볼루션 라이브카지노는 실제 딜러가 진행하는 카지노 게임을 HD 영상으로 실시간 스트리밍하는 서비스입니다. 라트비아·조지아·루마니아·캐나다 등의 전문 스튜디오에서 24시간 운영되며, 실제 카드·룰렛으로 진행해 조작 불가능한 공정한 게임을 제공합니다.',
      },
    },
    {
      '@type': 'Question',
      name: '에볼루션 라이브카지노 가입방법은?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '에볼루션은 B2B 소프트웨어 제공사로 직접 가입이 불가합니다. 에볼루션 라이선스를 보유한 합법적인 온라인 카지노(WOORIWIN 추천 카지노)에 회원가입 후 입금하면 에볼루션 라이브 로비에 입장할 수 있습니다. 가입은 보통 5분 이내에 완료됩니다.',
      },
    },
    {
      '@type': 'Question',
      name: '에볼루션 라이브카지노는 공정한가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '에볼루션카지노는 UKGC(영국 도박위원회)·MGA(몰타 도박청)·DGA(덴마크)·AGCO(캐나다 온타리오) 등 세계 최고 권위 규제 기관의 라이선스를 보유합니다. 모든 게임은 eCOGRA·GLI 등 독립 심사기관의 정기 감사를 받으며, 실물 카드와 룰렛을 사용하므로 조작이 물리적으로 불가능합니다.',
      },
    },
    {
      '@type': 'Question',
      name: '에볼루션 라이브카지노는 24시간 이용 가능한가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '네, 에볼루션 라이브카지노는 24시간 365일 운영됩니다. 전 세계 여러 스튜디오가 교대로 운영되며, 바카라·블랙잭·룰렛 등 주요 게임은 항상 라이브 테이블이 열려 있습니다. 새벽 시간대에도 딜러 부족 없이 이용 가능합니다.',
      },
    },
    {
      '@type': 'Question',
      name: '에볼루션 살롱 프리베(Salon Privé)란 무엇인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '살롱 프리베는 에볼루션의 VIP 전용 프라이빗 라이브 테이블입니다. 바카라·블랙잭·룰렛의 고액 한도 테이블로 구성되며, 일반 테이블에 노출되지 않는 프라이빗 환경을 제공합니다. 입장 기준은 카지노마다 다릅니다.',
      },
    },
    {
      '@type': 'Question',
      name: '에볼루션 라이브카지노 한국어 딜러가 있나요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '에볼루션 표준 테이블은 영어·다국어로 진행됩니다. 일부 카지노 파트너는 한국어 딜러 전용 테이블을 별도로 운영하기도 합니다. 한국어 서비스를 원한다면 WOORIWIN 추천 카지노 중 한국어 딜러 제공 카지노를 선택하세요.',
      },
    },
    {
      '@type': 'Question',
      name: '에볼루션 라이브카지노 모바일 품질은 어떤가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '에볼루션 라이브카지노는 HTML5 기반으로 iOS·Android에서 앱 설치 없이 브라우저에서 이용 가능합니다. 모바일 전용 UI가 최적화되어 있으며, LTE·5G 환경에서 끊김 없는 HD 스트리밍을 지원합니다. WiFi 환경을 권장합니다.',
      },
    },
    {
      '@type': 'Question',
      name: '에볼루션 라이브카지노 입출금 방식은?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '입출금 방식은 각 카지노마다 다릅니다. 주요 방식으로는 암호화폐(비트코인·USDT 등), 신용/직불카드, 전자지갑(스크릴·네텔러) 등이 있습니다. WOORIWIN에서는 빠른 입출금과 보안이 검증된 카지노를 추천합니다.',
      },
    },
  ] satisfies FAQItem[],
}

// ─── 데이터 ──────────────────────────────────────────────────
const features: Feature[] = [
  { icon: '🎬', title: 'HD 실시간 스트리밍', desc: '전문 스튜디오에서 실제 딜러가 24/7 HD 품질로 진행. 지연 없는 라이브 경험.' },
  { icon: '🔒', title: '세계 최고 수준 라이선스', desc: 'UKGC·MGA·DGA 등 최고 권위 규제 기관 라이선스 보유. 완벽한 공정성 보장.' },
  { icon: '📱', title: '완벽한 모바일 지원', desc: 'iOS·Android 브라우저에서 앱 없이 이용. 모바일 전용 UI 최적화.' },
  { icon: '🎮', title: '200종 이상 게임', desc: '바카라·블랙잭·룰렛·게임쇼 등 200개 이상의 라이브 테이블 상시 운영.' },
  { icon: '💎', title: 'VIP 살롱 프리베', desc: '고액 전용 프라이빗 테이블. 한도 협의 가능한 VIP 전용 환경.' },
  { icon: '🌍', title: '100개국 서비스', desc: '전 세계 1,000개 이상 카지노에 소프트웨어 공급. 업계 절대 표준.' },
]

// ─── 페이지 컴포넌트 ─────────────────────────────────────────
export default function LiveCasinoPage() {
  const faqList: FAQItem[] = jsonLdFaq.mainEntity

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdArticle) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdFaq) }} />
      <main className="min-h-screen bg-gray-900 text-white">

        {/* Hero */}
        <section className="relative flex flex-col items-center justify-center min-h-[55vh] text-center px-4 py-20 overflow-hidden">
          <div className="absolute inset-0 z-0">
            <Image src="/images/live-casino.jpg" alt="에볼루션 라이브카지노 스튜디오 딜러" fill className="object-cover opacity-25" priority />
          </div>
          <div className="relative z-10 max-w-4xl mx-auto">
            <nav aria-label="breadcrumb" className="text-sm text-gray-400 mb-6">
              <Link href="/" className="hover:text-yellow-400">홈</Link>
              {' '}&rsaquo;{' '}
              <span className="text-white" aria-current="page">라이브카지노</span>
            </nav>
            <p className="text-sm text-yellow-400 font-semibold tracking-widest uppercase mb-4">24/7 HD 스트리밍 · UKGC·MGA 라이선스</p>
            <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
              에볼루션 라이브카지노<br />
              <span className="text-yellow-400">완벽 가이드 2026</span>
            </h1>
            <p className="text-lg text-gray-300 max-w-2xl mx-auto leading-relaxed">
              세계 1위 라이브카지노 에볼루션의 모든 것. 가입방법부터 VIP 살롱 프리베까지 완벽 정리했습니다.
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
              <Link href="/about" className="text-yellow-400 hover:underline font-semibold">Gambler Lucifer</Link>
              <span>·</span>
              <span>라이브카지노 전문 애널리스트 · 에볼루션 게임 10년 경력</span>
            </div>
            <h2 className="text-2xl md:text-3xl font-extrabold mb-6 text-white border-b border-gray-800 pb-4">
              에볼루션 라이브카지노: <span className="text-yellow-400 text-xl md:text-2xl">20년 기술력이 만든 세계 표준</span>
            </h2>
            <p className="text-xl text-gray-400 leading-relaxed mb-6">
              단순한 온라인 게임이 아닙니다. 실제 딜러, 실제 카드, 실제 룰렛 휠. 에볼루션이 만든 라이브카지노는 오프라인 카지노의 긴장감과 온라인의 편의성을 완벽하게 융합한 새로운 차원의 경험입니다.
            </p>
          </header>

          <div className="space-y-16 text-base md:text-lg leading-relaxed">

            {/* 섹션 1 */}
            <article>
              <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
                <span className="text-yellow-400 mr-3">#01</span> 왜 1,000개 카지노가 에볼루션을 선택하는가
              </h3>
              <p className="mb-4">
                <strong>에볼루션카지노(Evolution Gaming)</strong>는 2006년 설립 이후 단 한 번도 업계 1위 자리를 내준 적이 없습니다. 그 비결은 단순합니다. 경쟁사가 흉내 낼 수 없는 <strong>하드웨어 기술력</strong>과 <strong>운영 노하우</strong>입니다. 라트비아 리가, 조지아 트빌리시, 캐나다 밴쿠버 등 전 세계 스튜디오에서 24시간 365일 HD 스트리밍이 끊김 없이 제공됩니다.
              </p>
              <p>
                에볼루션의 모든 게임은 <strong>UKGC(영국 도박위원회)</strong>와 <strong>MGA(몰타 게임청)</strong> 라이선스를 보유하고 있으며,{' '}
                <a href="https://ecogra.org" target="_blank" rel="noopener noreferrer" className="text-yellow-400 hover:underline">eCOGRA</a> 등 국제 공인기관의 정기 감사를 통해 공정성이 검증됩니다. 실물 카드·룰렛 휠을 사용하기 때문에 RNG 게임과 달리 결과 조작이 물리적으로 불가능합니다.
              </p>
            </article>

            {/* 섹션 2: PRO ANALYSIS */}
            <article className="bg-gray-800/30 p-8 rounded-2xl border border-gray-700">
              <h3 className="text-xl font-bold text-yellow-400 mb-6 text-center underline underline-offset-8">
                PRO ANALYSIS: 에볼루션 라이브카지노 게임별 RTP 비교
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div className="bg-black/40 p-5 rounded-xl text-center border border-gray-600">
                  <p className="text-gray-400 text-sm mb-2">바카라 (뱅커)</p>
                  <p className="text-3xl font-black text-green-400">98.94%</p>
                  <p className="text-xs mt-2 text-gray-500">업계 최저 하우스 엣지</p>
                </div>
                <div className="bg-black/40 p-5 rounded-xl text-center border border-gray-600">
                  <p className="text-gray-400 text-sm mb-2">블랙잭 (기본전략)</p>
                  <p className="text-3xl font-black text-blue-400">99.28%</p>
                  <p className="text-xs mt-2 text-gray-500">전략 적용 시 최고 환수율</p>
                </div>
                <div className="bg-black/40 p-5 rounded-xl text-center border border-gray-600">
                  <p className="text-gray-400 text-sm mb-2">라이트닝 룰렛</p>
                  <p className="text-3xl font-black text-yellow-400">97.30%</p>
                  <p className="text-xs mt-2 text-gray-500">최대 500x 멀티플라이어</p>
                </div>
              </div>
              <blockquote className="border-l-4 border-gray-500 pl-4 italic text-sm text-gray-400 mb-4">
                "게임 선택이 곧 전략입니다. 장기적인 수익을 추구한다면 RTP가 높은 바카라·블랙잭이 유리하고, 단기 고배당을 노린다면 라이트닝 룰렛·크레이지타임이 적합합니다."
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
                ⚠️ <strong>손실 위험 안내:</strong> 모든 카지노 게임은 장기적으로 하우스 엣지가 존재하며, 손실이 발생할 수 있습니다. RTP가 높은 게임도 단기 손실을 보장하지 않습니다. 자신의 재정 범위 내에서만 게임을 즐기시기 바랍니다.
              </div>
            </article>

            {/* 섹션 3: 게임 라인업 */}
            <article className="bg-gray-800/20 p-8 rounded-3xl border border-gray-800 shadow-2xl">
              <h3 className="text-2xl font-bold text-white mb-8 italic">Evolution Innovation: 200종 게임 라인업</h3>
              <div className="space-y-10">
                <div className="flex flex-col md:flex-row gap-6 items-start">
                  <div className="w-full md:w-1/3">
                    <h4 className="text-yellow-400 font-extrabold text-xl mb-2">라이브 테이블 게임</h4>
                    <span className="text-xs border border-yellow-400/50 px-2 py-0.5 rounded text-yellow-400 uppercase">Core Games</span>
                  </div>
                  <div className="w-full md:w-2/3">
                    <p className="text-sm text-gray-300">
                      바카라(스피드·라이트닝·스퀴즈·노커미션 등 10종), 블랙잭(인피니트·스피드·라이트닝), 룰렛(라이트닝·이머시브·프렌치·아메리칸), 홀덤 포커, 드래곤 타이거까지. 에볼루션의 <strong>핵심 테이블 게임</strong>은 모두 실물 도구로 진행되며 24시간 운영됩니다.
                    </p>
                  </div>
                </div>
                <div className="flex flex-col md:flex-row gap-6 items-start">
                  <div className="w-full md:w-1/3">
                    <h4 className="text-yellow-400 font-extrabold text-xl mb-2">라이브 게임쇼</h4>
                    <span className="text-xs border border-yellow-400/50 px-2 py-0.5 rounded text-yellow-400 uppercase">Game Show</span>
                  </div>
                  <div className="w-full md:w-2/3">
                    <p className="text-sm text-gray-300">
                      크레이지타임, 모노폴리 라이브, 메가볼, 드림캐처, 딜 오어 노딜 등 <strong>TV 게임쇼 포맷</strong>을 카지노에 접목한 혁신적인 타이틀입니다. 단순 베팅을 넘어 엔터테인먼트 경험을 제공하며, MZ 세대에게 폭발적인 인기를 끌고 있습니다.
                    </p>
                  </div>
                </div>
                <div className="flex flex-col md:flex-row gap-6 items-start">
                  <div className="w-full md:w-1/3">
                    <h4 className="text-yellow-400 font-extrabold text-xl mb-2">살롱 프리베 VIP</h4>
                    <span className="text-xs border border-yellow-400/50 px-2 py-0.5 rounded text-yellow-400 uppercase">VIP Only</span>
                  </div>
                  <div className="w-full md:w-2/3">
                    <p className="text-sm text-gray-300">
                      고액 플레이어를 위한 프라이빗 테이블입니다. 일반 테이블보다 높은 베팅 한도, 전담 딜러, 독립된 게임 환경을 제공합니다. 바카라·블랙잭·룰렛 모두 살롱 프리베 버전이 있으며, <strong>VIP 자격 조건</strong>은 각 카지노마다 상이합니다.
                    </p>
                  </div>
                </div>
              </div>
            </article>

            {/* 섹션 4: 모바일 */}
            <article>
              <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
                <span className="text-yellow-400 mr-3">#04</span> 모바일 최적화: 언제 어디서나 HD 품질
              </h3>
              <p className="mb-6">
                에볼루션 라이브카지노 전체 트래픽의 <strong>60% 이상이 모바일</strong>에서 발생합니다. HTML5 기반으로 iOS·Android 모든 기기에서 별도 앱 설치 없이 모바일 브라우저로 이용 가능합니다. 세로 모드에서도 완벽하게 최적화된 UI를 제공하며, 터치 인터페이스로 베팅·채팅·게임 기록 확인이 모두 가능합니다.
              </p>
              <div className="bg-black/50 p-6 rounded-xl border border-gray-800">
                <h4 className="text-white font-bold mb-4">모바일 최적 환경 체크리스트</h4>
                <ul className="grid md:grid-cols-2 gap-3 text-xs md:text-sm">
                  <li className="flex items-center text-gray-400">✔ Wi-Fi 또는 5G 환경 권장 (HD 스트리밍 기준 10Mbps 이상)</li>
                  <li className="flex items-center text-gray-400">✔ Chrome·Safari 최신 버전 사용</li>
                  <li className="flex items-center text-gray-400">✔ 배터리 절약 모드 해제 시 화질 안정</li>
                  <li className="flex items-center text-gray-400">✔ 화면 밝기 70% 이상 권장</li>
                </ul>
              </div>
            </article>
          </div>
        </section>

        {/* 특징 카드 */}
        <section className="bg-gray-800 py-16 px-4">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-3">에볼루션 라이브카지노 특징</h2>
            <p className="text-gray-400 text-center mb-10">왜 에볼루션이 세계 1위인가</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              {features.map((f) => (
                <div key={f.title} className="bg-gray-900 rounded-xl p-5 border border-gray-700 hover:border-yellow-400 transition">
                  <div className="text-3xl mb-3">{f.icon}</div>
                  <h3 className="text-yellow-400 font-bold text-base mb-2">{f.title}</h3>
                  <p className="text-gray-400 text-sm">{f.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* FAQ */}
        <section className="max-w-4xl mx-auto px-4 py-16">
          <h2 className="text-3xl font-bold mb-10 text-center">에볼루션 라이브카지노 FAQ</h2>
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
