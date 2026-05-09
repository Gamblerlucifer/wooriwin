import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'

export const metadata: Metadata = {
  title: '에볼루션카지노 — 바카라·블랙잭·룰렛 완벽 가이드 | WOORIWIN',
  description:
    '에볼루션카지노 공식 가이드. 바카라, 블랙잭, 룰렛, 슬롯 규칙과 전략부터 가입방법까지. 국내 최다 에볼루션카지노 정보를 WOORIWIN에서 확인하세요.',
  keywords: [
    '에볼루션카지노',
    '에볼루션카지노 바카라',
    '에볼루션카지노 블랙잭',
    '에볼루션카지노 가입',
    '에볼루션 라이브카지노',
    '온라인카지노',
    '에볼루션카지노 추천',
    '에볼루션카지노 규칙',
  ],
  openGraph: {
    title: '에볼루션카지노 완벽 가이드 | WOORIWIN',
    description: '바카라, 블랙잭, 룰렛 전략부터 가입방법까지. WOORIWIN에서 확인하세요.',
    url: 'https://wooriwin.com',
    siteName: 'WOORIWIN',
    locale: 'ko_KR',
    type: 'website',
    images: [{ url: 'https://wooriwin.com/images/og-main.jpg', width: 1200, height: 630 }],
  },
  alternates: { canonical: 'https://wooriwin.com' },
}

const jsonLd = {
  '@context': 'https://schema.org',
  '@graph': [
    {
      '@type': 'WebSite',
      '@id': 'https://wooriwin.com/#website',
      url: 'https://wooriwin.com',
      name: 'WOORIWIN',
      description: '에볼루션카지노 완벽 가이드',
      inLanguage: 'ko-KR',
    },
    {
      '@type': 'FAQPage',
      mainEntity: [
        {
          '@type': 'Question',
          name: '에볼루션카지노란 무엇인가요?',
          acceptedAnswer: {
            '@type': 'Answer',
            text: '에볼루션카지노(Evolution Gaming)는 세계 최대 라이브 카지노 소프트웨어 제공업체입니다. 실제 딜러가 진행하는 바카라, 블랙잭, 룰렛, 슬롯 등 다양한 게임을 HD 스트리밍으로 제공하며, 전 세계 수천 개의 온라인 카지노에서 채택하고 있습니다.',
          },
        },
        {
          '@type': 'Question',
          name: '에볼루션카지노는 어떤 게임을 제공하나요?',
          acceptedAnswer: {
            '@type': 'Answer',
            text: '에볼루션카지노는 라이브 바카라, 라이브 블랙잭, 라이브 룰렛, 라이브 슬롯, 게임쇼(크레이지타임, 라이트닝 룰렛 등) 등 수백 가지 게임을 제공합니다. 특히 라이트닝 바카라, 스피드 바카라 등 독자적인 변형 게임이 인기입니다.',
          },
        },
        {
          '@type': 'Question',
          name: '에볼루션카지노 가입은 어떻게 하나요?',
          acceptedAnswer: {
            '@type': 'Answer',
            text: '에볼루션카지노는 B2B 소프트웨어 제공업체로 직접 가입은 불가능합니다. 에볼루션 게임을 제공하는 온라인 카지노 사이트에 회원가입 후 라이브 카지노 섹션에서 이용할 수 있습니다.',
          },
        },
        {
          '@type': 'Question',
          name: '에볼루션카지노 바카라 승률은 얼마인가요?',
          acceptedAnswer: {
            '@type': 'Answer',
            text: '에볼루션 바카라의 RTP(환수율)는 약 98.94%입니다. 뱅커 베팅 승률은 약 45.86%, 플레이어 베팅은 약 44.62%이며 뱅커 베팅이 통계적으로 유리하지만 5% 커미션이 부과됩니다.',
          },
        },
        {
          '@type': 'Question',
          name: '에볼루션카지노를 모바일에서 이용할 수 있나요?',
          acceptedAnswer: {
            '@type': 'Answer',
            text: '네, 에볼루션카지노의 모든 게임은 iOS와 Android 기기에서 완벽하게 최적화되어 있습니다. 별도 앱 설치 없이 모바일 브라우저에서 바로 HD 품질의 라이브 게임을 즐길 수 있습니다.',
          },
        },
        {
          '@type': 'Question',
          name: '에볼루션카지노 최소 베팅 금액은 얼마인가요?',
          acceptedAnswer: {
            '@type': 'Answer',
            text: '에볼루션카지노의 최소 베팅 금액은 테이블마다 다르며, 일반적으로 바카라는 $1~$5부터 시작합니다. 스피드 바카라나 일반 테이블은 소액으로 시작 가능하며, VIP 살롱 프리베 테이블은 고액 베팅 전용입니다.',
          },
        },
        {
          '@type': 'Question',
          name: '에볼루션카지노와 일반 온라인 카지노의 차이점은 무엇인가요?',
          acceptedAnswer: {
            '@type': 'Answer',
            text: '에볼루션카지노는 실제 딜러와 실제 카드·룰렛으로 진행되는 라이브 게임입니다. 일반 RNG(난수생성기) 카지노와 달리 실시간 HD 영상으로 진행되어 실제 카지노와 동일한 경험을 제공하며 조작 가능성이 없습니다.',
          },
        },
        {
          '@type': 'Question',
          name: '에볼루션카지노 라이트닝 바카라란 무엇인가요?',
          acceptedAnswer: {
            '@type': 'Answer',
            text: '라이트닝 바카라는 에볼루션의 대표 변형 게임으로, 매 라운드마다 1~5장의 라이트닝 카드가 무작위로 선정되어 2x~8x 배율을 제공합니다. 기본 바카라에 슬롯 요소를 결합한 혁신적인 게임입니다.',
          },
        },
      ],
    },
  ],
}

const games = [
  {
    name: '바카라',
    href: '/baccarat',
    desc: '에볼루션 대표 게임. 뱅커vs플레이어 승부로 RTP 98.94%의 높은 환수율.',
    img: '/images/baccarat.jpg',
    alt: '에볼루션카지노 바카라 뱅커 플레이어 베팅 RTP 98.94% 라이브 딜러',
    keyword: '에볼루션카지노 바카라',
  },
  {
    name: '블랙잭',
    href: '/blackjack',
    desc: '21을 향한 두뇌싸움. 인피니트 블랙잭, 스피드 블랙잭 등 다양한 변형 제공.',
    img: '/images/blackjack.jpg',
    alt: '에볼루션카지노 블랙잭 인피니트 블랙잭 기본전략 RTP 99.28% 라이브 테이블',
    keyword: '에볼루션카지노 블랙잭',
  },
  {
    name: '룰렛',
    href: '/roulette',
    desc: '라이트닝 룰렛, 이머시브 룰렛. 최대 500배 멀티플라이어 제공.',
    img: '/images/roulette.jpg',
    alt: '에볼루션카지노 라이트닝 룰렛 500배 멀티플라이어 유럽식 룰렛 라이브',
    keyword: '에볼루션카지노 룰렛',
  },
  {
    name: '슬롯',
    href: '/slots',
    desc: '에볼루션 게임쇼. 크레이지타임, 모노폴리 라이브 등 인기 타이틀.',
    img: '/images/slots.jpg',
    alt: '에볼루션카지노 크레이지타임 2만배 모노폴리 라이브 게임쇼',
    keyword: '에볼루션카지노 슬롯',
  },
  {
    name: '라이브카지노',
    href: '/live-casino',
    desc: '실제 딜러와 실시간 HD 스트리밍. 전 세계 최고 수준의 라이브 카지노.',
    img: '/images/live-casino.jpg',
    alt: '에볼루션 라이브카지노 24시간 HD 스트리밍 UKGC MGA 라이선스',
    keyword: '에볼루션 라이브카지노',
  },
  {
    name: '블로그',
    href: '/blog',
    desc: '에볼루션카지노 전략, 규칙, 팁을 전문가가 분석한 최신 가이드.',
    img: '/images/blog.jpg',
    alt: '에볼루션카지노 바카라 블랙잭 룰렛 전략 규칙 팁 전문가 분석',
    keyword: '에볼루션카지노 전략',
  },
]

const features = [
  {
    title: '세계 1위 라이브 카지노',
    desc: '에볼루션은 전 세계 1,000개 이상의 온라인 카지노에 소프트웨어를 공급하는 업계 표준입니다.',
  },
  {
    title: 'HD 실시간 스트리밍',
    desc: '최첨단 스튜디오에서 전문 딜러가 진행하는 HD 품질의 라이브 게임을 24시간 즐길 수 있습니다.',
  },
  {
    title: '수백 가지 게임 제공',
    desc: '바카라, 블랙잭, 룰렛부터 크레이지타임, 모노폴리 라이브까지 다양한 게임을 한 플랫폼에서.',
  },
  {
    title: '완벽한 모바일 지원',
    desc: 'iOS·Android 모든 기기에서 앱 설치 없이 브라우저만으로 풀HD 라이브 게임 이용 가능.',
  },
]

export default function Home() {
  const faqList = (jsonLd['@graph'][1] as any).mainEntity

  return (
    <>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
      />
      <main className="min-h-screen bg-gray-900 text-white">

        {/* ── Hero ── */}
        <section className="relative flex flex-col items-center justify-center min-h-[70vh] text-center px-4 py-20 overflow-hidden">
          <div className="absolute inset-0 z-0">
            <Image
              src="/images/hero.jpg"
              alt="에볼루션카지노 세계 1위 라이브카지노 바카라 블랙잭 룰렛 HD 스트리밍"
              fill
              className="object-cover opacity-30"
              priority
            />
          </div>
          <div className="relative z-10 max-w-4xl mx-auto">
            <p className="text-sm text-yellow-400 font-semibold tracking-widest uppercase mb-4">
              세계 1위 라이브 카지노 소프트웨어
            </p>
            <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
              에볼루션카지노<br />
              <span className="text-yellow-400">완벽 가이드</span>
            </h1>
            <p className="text-lg md:text-xl text-gray-300 mb-10 max-w-2xl mx-auto leading-relaxed">
              바카라, 블랙잭, 룰렛 전략부터 가입방법까지.<br />
              에볼루션카지노의 모든 정보를 WOORIWIN에서 확인하세요.
            </p>
            <div className="flex flex-wrap gap-4 justify-center">
              <Link href="/baccarat" className="bg-yellow-400 text-gray-900 font-bold px-8 py-3 rounded-lg hover:bg-yellow-300 transition">
                바카라 가이드 보기
              </Link>
              <Link href="/blog" className="border border-white text-white font-semibold px-8 py-3 rounded-lg hover:bg-white hover:text-gray-900 transition">
                전략 블로그
              </Link>
            </div>
          </div>
        </section>

        {/* ── 에볼루션카지노 소개 본문 ── */}
        <section className="max-w-4xl mx-auto px-4 py-16">
          <h2 className="text-3xl font-bold mb-6 text-yellow-400">에볼루션카지노란?</h2>
          <div className="text-gray-300 space-y-5 leading-relaxed text-base md:text-lg">
            <p>
              <strong className="text-white">에볼루션카지노(Evolution Gaming)</strong>는 2006년 설립된 세계 최대 라이브 카지노
              소프트웨어 제공업체입니다. 스웨덴 스톡홀름에 본사를 두고 있으며, 나스닥 스톡홀름에 상장된 합법적인 글로벌
              기업입니다. 현재 전 세계 1,000개 이상의 온라인 카지노에 라이브 게임 소프트웨어를 공급하며 업계 표준으로
              자리 잡고 있습니다.
            </p>
            <p>
              에볼루션카지노의 가장 큰 특징은 <strong className="text-white">실제 딜러(Live Dealer)</strong>가 진행하는 게임을
              HD 화질의 실시간 스트리밍으로 제공한다는 점입니다. 라트비아, 조지아, 캐나다, 루마니아 등 세계 각지에 위치한
              최첨단 스튜디오에서 전문 교육을 받은 딜러들이 24시간 365일 게임을 진행합니다.
            </p>
            <p>
              에볼루션이 제공하는 게임 라인업은 크게 <strong className="text-white">라이브 테이블 게임</strong>과{' '}
              <strong className="text-white">라이브 게임쇼</strong> 두 가지로 나뉩니다. 라이브 바카라, 라이브 블랙잭,
              라이브 룰렛이 핵심 테이블 게임이며, 크레이지타임(Crazy Time), 모노폴리 라이브(Monopoly Live),
              라이트닝 룰렛(Lightning Roulette) 등 독창적인 게임쇼 타이틀이 큰 인기를 끌고 있습니다.
            </p>
            <p>
              특히 <strong className="text-white">에볼루션 바카라</strong>는 아시아 시장에서 압도적인 인기를 자랑합니다.
              기본 바카라 외에도 스피드 바카라(27초 완료), 라이트닝 바카라(최대 8배 멀티플라이어),
              스퀴즈 바카라(카드 뒤집는 긴장감), No Commission 바카라 등 다양한 변형 게임을 제공합니다.
              RTP(환수율)는 약 98.94%로 업계 최고 수준이며, 뱅커 베팅 승률은 약 45.86%입니다.
            </p>
            <p>
              <strong className="text-white">에볼루션카지노 블랙잭</strong>은 인피니트 블랙잭(무제한 착석),
              스피드 블랙잭, 라이트닝 블랙잭 등의 변형 게임을 통해 다양한 플레이 스타일을 지원합니다.
              기본 전략을 사용할 경우 RTP가 99% 이상에 달해 카지노 게임 중 가장 높은 환수율을 자랑합니다.
            </p>
            <p>
              <strong className="text-white">에볼루션 룰렛</strong>의 경우 라이트닝 룰렛이 단연 인기입니다.
              매 스핀마다 2~5개의 숫자에 50x~500x의 멀티플라이어가 적용되어 일반 룰렛보다 훨씬 큰 당첨금을 기대할 수 있습니다.
              이머시브 룰렛은 다중 카메라 앵글로 느린 화면 재생을 제공하여 시각적 몰입감을 극대화합니다.
            </p>
            <p>
              모바일 지원 측면에서도 에볼루션은 업계 최고 수준입니다. iOS와 Android 모든 기기에서 별도 앱 설치 없이
              모바일 브라우저만으로 풀HD 라이브 게임을 즐길 수 있습니다. 세로 화면 모드도 완벽하게 지원하여
              스마트폰으로도 불편함 없이 이용 가능합니다.
            </p>
            <p>
              WOORIWIN은 에볼루션카지노의 모든 게임에 대한 상세한 규칙, 전략, 팁을 제공합니다.
              처음 에볼루션카지노를 접하는 초보자부터 전략적 베팅을 원하는 고수까지 모두에게 유용한 정보를 담고 있습니다.
              아래 게임별 가이드를 통해 원하는 게임의 완벽한 전략을 확인해보세요.
            </p>
          </div>
        </section>

        {/* ── 게임 카드 그리드 ── */}
        <section className="max-w-6xl mx-auto px-4 py-12">
          <h2 className="text-3xl font-bold text-center mb-3">게임별 완벽 가이드</h2>
          <p className="text-gray-400 text-center mb-10">에볼루션카지노의 모든 게임을 한눈에 확인하세요.</p>
          <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
            {games.map((game) => (
              <Link
                key={game.href}
                href={game.href}
                className="group bg-gray-800 rounded-xl overflow-hidden hover:bg-gray-700 transition-all hover:scale-105 hover:shadow-xl hover:shadow-yellow-400/10"
              >
                <div className="relative h-48 bg-gray-700">
                  <Image
                    src={game.img}
                    alt={game.alt}
                    fill
                    className="object-cover group-hover:opacity-90 transition"
                  />
                </div>
                <div className="p-5">
                  <h3 className="text-lg font-bold text-yellow-400 mb-2">{game.keyword}</h3>
                  <p className="text-gray-400 text-sm leading-relaxed">{game.desc}</p>
                  <span className="inline-block mt-4 text-sm text-yellow-400 font-semibold group-hover:underline">
                    자세히 보기 →
                  </span>
                </div>
              </Link>
            ))}
          </div>
        </section>

        {/* ── 왜 에볼루션인가 ── */}
        <section className="bg-gray-800 py-16 px-4 mt-8">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-3">왜 에볼루션카지노인가?</h2>
            <p className="text-gray-400 text-center mb-10">전 세계 플레이어가 에볼루션을 선택하는 이유</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 gap-6">
              {features.map((f) => (
                <div key={f.title} className="bg-gray-900 rounded-xl p-6 border border-gray-700 hover:border-yellow-400 transition">
                  <h3 className="text-lg font-bold text-yellow-400 mb-3">✦ {f.title}</h3>
                  <p className="text-gray-400 text-sm leading-relaxed">{f.desc}</p>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* ── FAQ ── */}
        <section className="max-w-4xl mx-auto px-4 py-16">
          <h2 className="text-3xl font-bold mb-10 text-center">에볼루션카지노 자주 묻는 질문</h2>
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

        {/* ── Footer 내부 링크 ── */}
        <footer className="bg-gray-950 py-10 px-4 text-center">
          <p className="text-gray-500 text-sm mb-4">에볼루션카지노 관련 가이드</p>
          <div className="flex flex-wrap justify-center gap-4 text-sm">
            {games.map((g) => (
              <Link key={g.href} href={g.href} className="text-gray-400 hover:text-yellow-400 transition">
                {g.keyword}
              </Link>
            ))}
          </div>
          <p className="text-gray-600 text-xs mt-8">© 2026 WOORIWIN. All rights reserved.</p>
        </footer>

      </main>
    </>
  )
}
