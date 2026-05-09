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
            <Image src="/images/roulette.jpg" alt="에볼루션카지노 룰렛 라이브 게임" fill className="object-cover opacity-25" priority />
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

        {/* 본문 */}
        <section className="max-w-4xl mx-auto px-4 py-16">
          <h2 className="text-3xl font-bold mb-6 text-yellow-400">에볼루션카지노 룰렛이란?</h2>
          <div className="text-gray-300 space-y-5 leading-relaxed text-base md:text-lg">
            <p>
              <strong className="text-white">에볼루션카지노 룰렛</strong>은 세계 최고 수준의 라이브 스튜디오 환경에서
              실제 딜러가 진행하는 라이브 룰렛 게임입니다. 유럽식·아메리칸·프렌치 룰렛의 전통 게임부터
              라이트닝 룰렛·이머시브 룰렛·더블볼 룰렛 등 에볼루션만의 독점 변형 게임까지 10종 이상을 제공합니다.
            </p>
            <p>
              룰렛의 기본 규칙은 딜러가 휠을 돌리고 볼을 던져 볼이 멈추는 번호와 색상을 맞추는 게임입니다.
              베팅은 크게 <strong className="text-white">이너 베팅(Inner Bet)</strong>과
              <strong className="text-white"> 아우터 베팅(Outer Bet)</strong>으로 나뉩니다.
            </p>
            <p>
              에볼루션의 가장 인기 있는 룰렛 게임은 단연 <strong className="text-white">라이트닝 룰렛(Lightning Roulette)</strong>입니다.
              매 스핀마다 1~5개의 번호에 50x·100x·200x·300x·500x의 멀티플라이어가 무작위로 적용됩니다.
              해당 번호에 스트레이트업 베팅이 맞으면 최대 500배까지 당첨금을 받을 수 있습니다.
            </p>
            <p>
              가장 높은 RTP를 원한다면 <strong className="text-white">프렌치 룰렛</strong>을 선택하세요.
              이븐머니 베팅 시 볼이 0에 떨어지면 베팅을 몰수하지 않고 다음 스핀에 유지하는
              앙 프리종(En Prison) 룰이 적용되어 이븐머니 베팅의 RTP가 98.65%에 달합니다.
            </p>
            <p>
              <strong className="text-white">이머시브 룰렛</strong>은 HD 멀티캠 카메라 시스템으로
              볼이 떨어지는 순간을 슬로우 모션으로 포착하여 극적인 시각적 경험을 제공합니다.
              처음 라이브 룰렛을 경험하는 플레이어에게 추천하는 입문 게임입니다.
            </p>
            <p>
              에볼루션의 독점 변형 게임 <strong className="text-white">더블볼 룰렛</strong>은
              한 스핀에 두 개의 볼을 동시에 사용합니다. 두 볼이 모두 같은 번호에 멈추면
              스트레이트업 베팅이 1,300:1의 배당을 제공합니다.
            </p>
            <p>
              WOORIWIN에서는 에볼루션 룰렛의 모든 변형 게임 비교, 베팅 전략 분석, 확률 계산을
              블로그를 통해 상세히 제공합니다.
            </p>
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