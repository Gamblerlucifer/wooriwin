import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'

export const metadata: Metadata = {
  title: '에볼루션카지노 룰렛 완벽 가이드 2026 | WOORIWIN',
  description: '에볼루션카지노 룰렛 규칙·전략·배팅 방법 완벽 정리. 라이트닝 룰렛, 임머시브 룰렛, 유럽식·미국식 룰렛까지 변형 게임 총망라.',
  keywords: ['에볼루션카지노 룰렛', '에볼루션 룰렛', '라이트닝 룰렛', '룰렛 전략', '룰렛 규칙'],
  alternates: { canonical: 'https://wooriwin.com/roulette' },
  openGraph: {
    title: '에볼루션카지노 룰렛 완벽 가이드 2026 | WOORIWIN',
    description: '에볼루션 룰렛 규칙·전략·변형 게임 완벽 정리.',
    url: 'https://wooriwin.com/roulette',
    images: [{ url: 'https://wooriwin.com/images/roulette.jpg', width: 1200, height: 630 }],
  },
  twitter: {
    card: 'summary_large_image',
    title: '에볼루션카지노 룰렛 완벽 가이드 2026 | WOORIWIN',
    description: '에볼루션 룰렛 규칙·전략·변형 게임 완벽 정리.',
    images: ['https://wooriwin.com/images/roulette.jpg'],
  },
}

const jsonLd = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'Article',
      headline: '에볼루션카지노 룰렛 완벽 가이드 2026',
      url: 'https://wooriwin.com/roulette',
      inLanguage: 'ko-KR',
      publisher: { '@type': 'Organization', name: 'WOORIWIN', url: 'https://wooriwin.com' },
    },
    {
      '@type': 'FAQPage',
      mainEntity: [
        {
          '@type': 'Question',
          name: '에볼루션카지노 룰렛 RTP는 얼마인가요?',
          acceptedAnswer: { '@type': 'Answer', text: '유럽식 룰렛(싱글 제로)의 RTP는 97.30%, 아메리칸 룰렛(더블 제로)은 94.74%입니다. 라이트닝 룰렛은 기본 RTP 97.30%에 멀티플라이어가 적용되는 구조로, 일반 룰렛보다 변동성이 큽니다.' },
        },
        {
          '@type': 'Question',
          name: '라이트닝 룰렛 멀티플라이어는 어떻게 작동하나요?',
          acceptedAnswer: { '@type': 'Answer', text: '라이트닝 룰렛은 매 스핀마다 1~5개의 번호에 50x·100x·200x·300x·500x 멀티플라이어가 무작위로 적용됩니다. 해당 번호에 스트레이트업 베팅이 맞으면 멀티플라이어 배당을 받습니다. 단, 멀티플라이어가 없는 번호의 스트레이트업 당첨은 29:1로 일반 룰렛(35:1)보다 낮습니다.' },
        },
        {
          '@type': 'Question',
          name: '유럽식 룰렛과 아메리칸 룰렛의 차이는?',
          acceptedAnswer: { '@type': 'Answer', text: '유럽식 룰렛은 0~36번 총 37개 칸(싱글 제로), 아메리칸 룰렛은 0·00·1~36 총 38개 칸(더블 제로)입니다. 더블 제로 때문에 아메리칸 룰렛의 하우스 엣지는 5.26%로 유럽식(2.70%)의 두 배입니다.' },
        },
        {
          '@type': 'Question',
          name: '이머시브 룰렛이란 무엇인가요?',
          acceptedAnswer: { '@type': 'Answer', text: '이머시브 룰렛(Immersive Roulette)은 HD 멀티캠 카메라로 볼이 떨어지는 순간을 슬로우 모션으로 보여주는 시각적 몰입감에 특화된 룰렛입니다. 규칙과 RTP는 유럽식 룰렛과 동일합니다.' },
        },
        {
          '@type': 'Question',
          name: '프렌치 룰렛 앙 프리종 룰이란?',
          acceptedAnswer: { '@type': 'Answer', text: '앙 프리종 룰은 이븐머니 베팅 시 볼이 0에 떨어지면 베팅이 몰수되지 않고 다음 스핀에 유지되는 규칙입니다. 덕분에 프렌치 룰렛의 이븐머니 베팅 RTP는 98.65%로 매우 높습니다.' },
        },
        {
          '@type': 'Question',
          name: '더블볼 룰렛이란 무엇인가요?',
          acceptedAnswer: { '@type': 'Answer', text: '더블볼 룰렛은 한 스핀에 두 개의 볼을 동시에 사용하는 에볼루션 독점 변형 게임입니다. 두 볼 모두 같은 번호에 떨어지면 스트레이트업 베팅이 1,300:1 배당을 받습니다.' },
        },
        {
          '@type': 'Question',
          name: '에볼루션 룰렛 최소 베팅은 얼마인가요?',
          acceptedAnswer: { '@type': 'Answer', text: '에볼루션 룰렛의 최소 베팅은 테이블에 따라 $0.10~$1 수준입니다. 라이트닝 룰렛은 최소 $0.20부터 시작합니다.' },
        },
      ],
    },
  ],
}

const variants = [
  { name: '라이트닝 룰렛', desc: '최대 500배 멀티플라이어. 에볼루션 룰렛 최고 인기 타이틀.', rtp: '최대 500x 배당' },
  { name: '이머시브 룰렛', desc: 'HD 멀티캠 슬로우모션. 시각적 몰입감 극대화.', rtp: 'RTP 97.30%' },
  { name: '유럽식 룰렛', desc: '싱글 제로 37칸. 하우스 엣지 2.70%로 가장 유리.', rtp: 'RTP 97.30%' },
  { name: '프렌치 룰렛', desc: '앙 프리종 룰 적용. 이븐머니 베팅 RTP 98.65%.', rtp: 'RTP 98.65%' },
  { name: '아메리칸 룰렛', desc: '더블 제로 38칸. 미국식 전통 룰렛 경험.', rtp: 'RTP 94.74%' },
  { name: '더블볼 룰렛', desc: '두 볼 동시 사용. 더블 스트레이트업 1,300:1 배당.', rtp: '최대 1,300:1' },
]

const relatedLinks = [
  { href: '/', label: '에볼루션카지노 메인' },
  { href: '/baccarat', label: '에볼루션카지노 바카라' },
  { href: '/blackjack', label: '에볼루션카지노 블랙잭' },
  { href: '/live-casino', label: '에볼루션 라이브카지노' },
  { href: '/blog', label: '룰렛 전략 블로그' },
]

export default function RoulettePage() {
  const faqList = (jsonLd['@graph'][1] as any).mainEntity

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <main className="min-h-screen bg-gray-900 text-white">

        {/* Hero */}
        <section className="relative flex flex-col items-center justify-center min-h-[55vh] text-center px-4 py-20 overflow-hidden">
          <div className="absolute inset-0 z-0">
            <Image src="/images/roulette.jpg" alt="에볼루션카지노 룰렛 라이브 휠 딜러" fill className="object-cover opacity-25" priority />
          </div>
          <div className="relative z-10 max-w-4xl mx-auto">
            <nav className="text-sm text-gray-400 mb-6">
              <Link href="/" className="hover:text-yellow-400">홈</Link> &rsaquo; <span className="text-white">룰렛</span>
            </nav>
            <p className="text-sm text-yellow-400 font-semibold tracking-widest uppercase mb-4">라이트닝 룰렛 최대 500배 · 10종 이상 변형</p>
            <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
              에볼루션카지노 룰렛<br />
              <span className="text-yellow-400">완벽 가이드 2026</span>
            </h1>
            <p className="text-lg text-gray-300 max-w-2xl mx-auto leading-relaxed">
              라이트닝 룰렛 500배부터 프렌치 룰렛 앙 프리종까지. 에볼루션 룰렛의 모든 변형과 전략을 정리했습니다.
            </p>
          </div>
        </section>

        <section className="max-w-4xl mx-auto px-4 py-20 text-gray-300">
          <header className="mb-16 border-b border-gray-800 pb-10">
            <div className="flex items-center space-x-3 mb-4">
              <span className="bg-yellow-400 text-black px-3 py-1 rounded-full text-sm font-bold uppercase tracking-wider">Roulette</span>
            </div>
            <h2 className="text-2xl md:text-3xl font-extrabold mb-6 text-white border-b border-gray-800 pb-4">
              에볼루션 룰렛: <span className="text-yellow-400 text-xl md:text-2xl">번개가 내리치는 순간, 500배의 기적</span>
            </h2>
            <p className="text-xl text-gray-400 leading-relaxed max-w-3xl">
              단순히 번호를 맞추는 게임이 아닙니다. 에볼루션 룰렛은 물리 법칙과 확률론이 교차하는 과학입니다. 어떤 변형 게임을 선택하느냐에 따라 하우스 엣지가 2배 이상 차이납니다.
            </p>
          </header>

          <div className="space-y-16 text-base md:text-lg leading-relaxed">

            {/* 섹션 1 */}
            <article>
              <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
                <span className="text-yellow-400 mr-3">#01</span> 룰렛의 본질: 수학이 지배하는 휠
              </h3>
              <p className="mb-4">
                룰렛을 처음 접하는 플레이어가 가장 많이 하는 실수는 <strong>'특정 번호가 연속으로 나오지 않으면 곧 나온다'</strong>고 믿는 것입니다. 이는 도박사의 오류(Gambler's Fallacy)입니다. 룰렛의 각 스핀은 완전히 독립적입니다. 이전 결과가 다음 결과에 영향을 주지 않습니다.
              </p>
              <p>
                유럽 룰렛(싱글 제로)의 하우스 엣지는 <strong>2.70%</strong>, 아메리칸 룰렛(더블 제로)은 <strong>5.26%</strong>입니다. 처음부터 유럽 또는 프렌치 룰렛을 선택하는 것만으로도 장기적으로 수익률이 크게 달라집니다.
              </p>
            </article>

            {/* 섹션 2: PRO ANALYSIS */}
            <article className="bg-gray-800/30 p-8 rounded-2xl border border-gray-700">
              <h3 className="text-xl font-bold text-yellow-400 mb-6 text-center underline underline-offset-8">
                PRO ANALYSIS: 에볼루션 룰렛 변형별 RTP 비교
              </h3>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                <div className="bg-black/40 p-5 rounded-xl text-center border border-gray-600">
                  <p className="text-gray-400 text-sm mb-2">프렌치 룰렛</p>
                  <p className="text-3xl font-black text-green-400">98.65%</p>
                  <p className="text-xs mt-2 text-gray-500">앙 프리종 룰 적용 최고 RTP</p>
                </div>
                <div className="bg-black/40 p-5 rounded-xl text-center border border-gray-600">
                  <p className="text-gray-400 text-sm mb-2">유럽 룰렛</p>
                  <p className="text-3xl font-black text-blue-400">97.30%</p>
                  <p className="text-xs mt-2 text-gray-500">싱글 제로 스탠다드</p>
                </div>
                <div className="bg-black/40 p-5 rounded-xl text-center border border-gray-600">
                  <p className="text-gray-400 text-sm mb-2">라이트닝 룰렛</p>
                  <p className="text-3xl font-black text-yellow-400">97.30%</p>
                  <p className="text-xs mt-2 text-red-400">최대 500x 멀티플라이어</p>
                </div>
              </div>
              <blockquote className="border-l-4 border-gray-500 pl-4 italic text-sm text-gray-400">
                "아메리칸 룰렛(RTP 94.74%)은 절대 피하세요. 더블 제로 하나가 하우스 엣지를 2배로 만듭니다. 같은 베팅을 해도 유럽 룰렛 대비 장기적으로 수익률 차이가 극명하게 벌어집니다."
              </blockquote>
            </article>

            {/* 섹션 3 */}
            <article className="bg-gray-800/20 p-8 rounded-3xl border border-gray-800 shadow-2xl">
              <h3 className="text-2xl font-bold text-white mb-8 italic">Evolution Innovation: 룰렛의 진화</h3>
              <div className="space-y-10">
                <div className="flex flex-col md:flex-row gap-6 items-start">
                  <div className="w-full md:w-1/3">
                    <h4 className="text-yellow-400 font-extrabold text-xl mb-2">라이트닝 룰렛</h4>
                    <span className="text-xs border border-yellow-400/50 px-2 py-0.5 rounded text-yellow-400 uppercase">Max 500x</span>
                  </div>
                  <div className="w-full md:w-2/3">
                    <p className="text-sm text-gray-300">
                      매 스핀마다 1~5개 번호에 <strong>50x·100x·200x·300x·500x</strong> 멀티플라이어가 무작위 적용됩니다. 해당 번호 스트레이트업 베팅 적중 시 최대 500배 당첨금을 받습니다. 단, 멀티플라이어 적용을 위해 스트레이트업 베팅의 기본 배당이 30:1로 조정됩니다.
                    </p>
                  </div>
                </div>
                <div className="flex flex-col md:flex-row gap-6 items-start">
                  <div className="w-full md:w-1/3">
                    <h4 className="text-yellow-400 font-extrabold text-xl mb-2">이머시브 룰렛</h4>
                    <span className="text-xs border border-yellow-400/50 px-2 py-0.5 rounded text-yellow-400 uppercase">HD Multi-Cam</span>
                  </div>
                  <div className="w-full md:w-2/3">
                    <p className="text-sm text-gray-300">
                      다중 카메라 앵글과 <strong>슬로우 모션</strong> 재생으로 볼이 휠에 떨어지는 순간을 극적으로 포착합니다. 시각적 몰입감이 극대화되어 라이브 룰렛 입문자에게 가장 추천하는 게임입니다. RTP는 유럽 룰렛과 동일한 97.30%입니다.
                    </p>
                  </div>
                </div>
                <div className="flex flex-col md:flex-row gap-6 items-start">
                  <div className="w-full md:w-1/3">
                    <h4 className="text-yellow-400 font-extrabold text-xl mb-2">더블볼 룰렛</h4>
                    <span className="text-xs border border-yellow-400/50 px-2 py-0.5 rounded text-yellow-400 uppercase">Dual Ball</span>
                  </div>
                  <div className="w-full md:w-2/3">
                    <p className="text-sm text-gray-300">
                      한 스핀에 <strong>두 개의 볼</strong>을 동시에 사용하는 에볼루션의 독점 변형 게임입니다. 두 볼이 같은 번호에 멈추면 스트레이트업 베팅이 <strong>1,300:1</strong> 배당을 제공합니다. 이너 베팅은 두 볼 중 하나만 맞아도 당첨됩니다.
                    </p>
                  </div>
                </div>
              </div>
            </article>

            {/* 섹션 4 */}
            <article>
              <h3 className="text-2xl font-bold text-white mb-6 flex items-center">
                <span className="text-yellow-400 mr-3">#04</span> 베팅 전략: 수학적으로 검증된 접근법
              </h3>
              <p className="mb-6">
                룰렛에서 장기적으로 수익을 보장하는 베팅 시스템은 존재하지 않습니다. 그러나 <strong>자금 관리와 베팅 패턴</strong>으로 손실을 최소화하고 게임을 오래 즐길 수 있습니다.
              </p>
              <div className="bg-black/50 p-6 rounded-xl border border-gray-800">
                <h4 className="text-white font-bold mb-4">룰렛 플레이어 체크리스트</h4>
                <ul className="grid md:grid-cols-2 gap-3 text-xs md:text-sm">
                  <li className="flex items-center text-gray-400">✔ 아메리칸 룰렛(더블 제로) 대신 유럽·프렌치 룰렛 선택</li>
                  <li className="flex items-center text-gray-400">✔ 이븐머니 베팅(레드/블랙)의 RTP가 가장 높음</li>
                  <li className="flex items-center text-gray-400">✔ 마틴게일 시스템: 베팅 한도와 뱅크롤 반드시 확인</li>
                  <li className="flex items-center text-gray-400">✔ 라이트닝 룰렛 스트레이트업은 기본 배당 30:1 유의</li>
                </ul>
              </div>
            </article>

            {/* 섹션 5: Responsible Gaming */}
            <footer className="pt-12 border-t border-gray-800 text-left">
              <div className="flex flex-col md:flex-row md:items-start md:justify-between gap-10">
                <div className="max-w-2xl">
                  <h3 className="text-2xl font-black text-white mb-6 uppercase tracking-tighter">
                    Responsible Gaming & Strategy
                  </h3>
                  <p className="text-gray-400 leading-relaxed mb-6">
                    <span className="text-white font-semibold">WOORIWIN</span>은 단순한 정보 제공을 넘어, 건전하고 지속 가능한 게임 문화를 지향합니다.
                    에볼루션카지노 룰렛의 모든 변형 게임 분석과 확률 데이터는 오직 플레이어 여러분의 현명한 선택을 돕기 위해 존재합니다.
                  </p>
                  <p className="text-gray-400 leading-relaxed">
                    에볼루션이 제공하는 기술의 정점을 만끽하시되, 항상 본인만의 자산 관리 원칙을 준수하시길 권장합니다.
                  </p>
                </div>
                <div className="bg-yellow-400/5 p-6 rounded-2xl border border-yellow-400/20 md:min-w-[320px]">
                  <div className="flex items-center gap-2 mb-3">
                    <div className="w-2 h-2 bg-yellow-400 rounded-full animate-pulse" />
                    <p className="text-yellow-400 font-bold uppercase tracking-widest text-sm">WOORIWIN CHECK</p>
                  </div>
                  <p className="text-sm text-gray-300 leading-snug">
                    "룰렛은 독립 시행의 게임입니다. 빨강이 10번 연속으로 나왔어도 다음 스핀의 빨강 확률은 여전히 48.6%입니다. 패턴이 아닌 확률을 신뢰하세요."
                  </p>
                </div>
              </div>
            </footer>
          </div>
        </section>

        {/* 변형 게임 카드 */}
        <section className="bg-gray-800 py-16 px-4">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-3">에볼루션 룰렛 변형 게임</h2>
            <p className="text-gray-400 text-center mb-10">에볼루션이 제공하는 룰렛 변형 게임 비교</p>
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

        {/* FAQ */}
        <section className="max-w-4xl mx-auto px-4 py-16">
          <h2 className="text-3xl font-bold mb-10 text-center">에볼루션카지노 룰렛 FAQ</h2>
          <div className="space-y-4">
            {faqList.map((faq: any, i: number) => (
              <details key={i} className="bg-gray-800 rounded-xl p-5 group cursor-pointer">
                <summary className="font-semibold text-base text-white flex justify-between items-center list-none">
                  {faq.name}
                  <span className="text-yellow-400 text-xl transition-transform group-open:rotate-45">+</span>
                </summary>
                <p className="mt-4 text-gray-400 text-sm leading-relaxed">{faq.acceptedAnswer.text}</p>
              </details>
            ))}
          </div>
        </section>

        {/* Footer */}
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