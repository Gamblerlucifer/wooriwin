import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'

// ─── 타입 정의 ──────────────────────────────────────────────────────────────
interface FAQItem {
  '@type': 'Question'
  name: string
  acceptedAnswer: { '@type': 'Answer'; text: string }
}

interface Game {
  name: string
  href: string
  img: string
  alt: string
  keyword: string
  rtp: string
  desc: string
}

interface SeoBlock {
  icon: string
  title: string
  paras: string[]
}

// ─── 메타데이터 ────────────────────────────────────────────────────────────
export const metadata: Metadata = {
  title: '에볼루션카지노 완벽 가이드 2026 | WOORIWIN',
  description:
    '에볼루션카지노 라이브 게임 전략, 테이블 분석, 플레이 가이드 및 건전한 게임 문화 정보를 제공합니다.',
  keywords: [
    '에볼루션카지노',
    '에볼루션카지노 바카라',
    '에볼루션카지노 블랙잭',
    '에볼루션카지노 라이브',
    '에볼루션카지노 룰렛',
    '에볼루션카지노 슬롯',
    '에볼루션카지노 규칙',
    '에볼루션 사이트',
    '에볼루션카지노 위치',
    '에볼루션카지노 무료체험',
    'Evolution Gaming',
    '에볼루션 공식 홈페이지',
    '에볼루션 카지노 주식',
    '에볼루션 라이브',
  ],
  alternates: { canonical: 'https://wooriwin.com' },
  openGraph: {
    title: '에볼루션카지노 완벽 가이드 2026 | WOORIWIN',
    description: '에볼루션카지노 라이브 게임 전략 및 플레이 가이드를 제공하는 건전한 게임 문화 정보형 콘텐츠 플랫폼.',
    url: 'https://wooriwin.com',
    images: [{ url: 'https://wooriwin.com/images/og-main.jpg', width: 1200, height: 630, alt: '에볼루션카지노 완벽 가이드 WOORIWIN' }],
  },
  twitter: {
    card: 'summary_large_image',
    title: '에볼루션카지노 완벽 가이드 2026 | WOORIWIN',
    description: '에볼루션카지노 라이브 게임 전략 및 플레이 가이드를 제공하는 건전한 게임 문화 정보형 콘텐츠 플랫폼',
    images: ['https://wooriwin.com/images/og-main.jpg'],
  },
}

// ─── JSON-LD ───────────────────────────────────────────────────────────────
const jsonLdArticle = {
  '@context': 'https://schema.org',
  '@type': 'Article',
  headline: '에볼루션카지노 완벽 가이드 2026',
  description: '에볼루션카지노 라이브 게임 전략 및 플레이 가이드를 제공하는 건전한 게임 문화 정보형 콘텐츠 플랫폼',
  url: 'https://wooriwin.com',
  inLanguage: 'ko-KR',
  datePublished: '2026-05-01',
  dateModified: '2026-05-10',
  author: {
    '@type': 'Organization',
    name: 'Gambler Lucifer',
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

const faqJsonLd = {
  '@context': 'https://schema.org',
  '@type': 'FAQPage',
  mainEntity: [
    {
      '@type': 'Question',
      name: '에볼루션카지노란 무엇인가요?',
      acceptedAnswer: { '@type': 'Answer', text: '에볼루션카지노(Evolution Gaming)는 세계 최대 라이브 카지노 소프트웨어 제공업체입니다. 실제 딜러가 진행하는 바카라, 블랙잭, 룰렛, 슬롯 등 다양한 게임을 HD 스트리밍으로 제공하며, 전 세계 수천 개의 온라인 카지노에서 채택하고 있습니다.' },
    },
    {
      '@type': 'Question',
      name: '에볼루션카지노는 어떤 게임을 제공하나요?',
      acceptedAnswer: { '@type': 'Answer', text: '에볼루션카지노는 라이브 바카라, 라이브 블랙잭, 라이브 룰렛, 라이브 슬롯, 게임쇼(크레이지타임, 라이트닝 룰렛 등) 등 수백 가지 게임을 제공합니다. 특히 라이트닝 바카라, 스피드 바카라 등 독자적인 변형 게임이 인기입니다.' },
    },
    {
      '@type': 'Question',
      name: '에볼루션카지노 가입은 어떻게 하나요?',
      acceptedAnswer: { '@type': 'Answer', text: '에볼루션카지노는 B2B 소프트웨어 제공업체로 직접 가입은 불가능합니다. 에볼루션 게임을 제공하는 온라인 카지노 사이트에 회원가입 후 라이브 카지노 섹션에서 이용할 수 있습니다.' },
    },
    {
      '@type': 'Question',
      name: '에볼루션카지노 바카라 승률은 얼마인가요?',
      acceptedAnswer: { '@type': 'Answer', text: '에볼루션 바카라의 RTP(환수율)는 약 98.94%입니다. 뱅커 베팅 승률은 약 45.86%, 플레이어 베팅은 약 44.62%이며, 뱅커 베팅에는 5% 커미션이 부과됩니다. 모든 베팅에는 손실 위험이 존재합니다.' },
    },
    {
      '@type': 'Question',
      name: '에볼루션카지노를 모바일에서 이용할 수 있나요?',
      acceptedAnswer: { '@type': 'Answer', text: '네, 에볼루션카지노의 모든 게임은 iOS와 Android 기기에서 완벽하게 최적화되어 있습니다. 별도 앱 설치 없이 모바일 브라우저에서 바로 HD 품질의 라이브 게임을 즐길 수 있습니다.' },
    },
    {
      '@type': 'Question',
      name: '에볼루션카지노 최소 베팅 금액은 얼마인가요?',
      acceptedAnswer: { '@type': 'Answer', text: '에볼루션카지노의 최소 베팅 금액은 테이블마다 다르며, 일반적으로 바카라는 $1~$5부터 시작합니다. 스피드 바카라나 일반 테이블은 소액으로 시작 가능하며, VIP 살롱 프리베 테이블은 고액 베팅 전용입니다.' },
    },
    {
      '@type': 'Question',
      name: '에볼루션카지노와 일반 온라인 카지노의 차이점은 무엇인가요?',
      acceptedAnswer: { '@type': 'Answer', text: '에볼루션카지노는 실제 딜러와 실제 카드·룰렛으로 진행되는 라이브 게임입니다. 일반 RNG(난수생성기) 카지노와 달리 실시간 HD 영상으로 진행되어 실제 카지노와 동일한 경험을 제공하며 조작 가능성이 없습니다.' },
    },
    {
      '@type': 'Question',
      name: '에볼루션카지노 라이트닝 바카라란 무엇인가요?',
      acceptedAnswer: { '@type': 'Answer', text: '라이트닝 바카라는 에볼루션의 대표 변형 게임으로, 매 라운드마다 1~5장의 라이트닝 카드가 무작위로 선정되어 카드당 2x~8x 배율을 제공합니다. 배율 중첩 시 최대 512배까지 가능합니다.' },
    },
  ] as FAQItem[],
}

// ─── 데이터 ────────────────────────────────────────────────────────────────
const games: Game[] = [
  {
    name: '바카라', href: '/baccarat', img: '/images/baccarat.jpg',
    alt: '에볼루션카지노 바카라 라이브 테이블', keyword: '에볼루션카지노 바카라', rtp: 'RTP 98.94%',
    desc: '에볼루션 대표 게임. 뱅커 vs 플레이어 승부로 RTP 98.94%의 높은 환수율을 자랑합니다. 스피드 바카라(27초 완료), 라이트닝 바카라(최대 512배), 스퀴즈 바카라, No Commission 바카라 등 다양한 변형 게임을 제공합니다.',
  },
  {
    name: '블랙잭', href: '/blackjack', img: '/images/blackjack.jpg',
    alt: '에볼루션카지노 블랙잭 라이브 테이블', keyword: '에볼루션카지노 블랙잭', rtp: 'RTP 99%+',
    desc: '21을 향한 두뇌싸움. 인피니트 블랙잭(무제한 착석), 스피드 블랙잭, 라이트닝 블랙잭 등 다양한 변형 게임을 제공합니다. 기본 전략을 사용할 경우 RTP가 99% 이상에 달해 카지노 게임 중 가장 높은 환수율을 자랑하는 게임입니다.',
  },
  {
    name: '룰렛', href: '/roulette', img: '/images/roulette.jpg',
    alt: '에볼루션카지노 라이트닝 룰렛 라이브', keyword: '에볼루션카지노 룰렛', rtp: '최대 500×',
    desc: '라이트닝 룰렛, 이머시브 룰렛 등 혁신적인 변형 게임을 제공합니다. 라이트닝 룰렛은 매 스핀마다 2~5개의 숫자에 50x~500x의 멀티플라이어가 적용됩니다. 이머시브 룰렛은 다중 카메라 앵글로 시각적 몰입감을 극대화합니다.',
  },
  {
    name: '슬롯', href: '/slots', img: '/images/slots.jpg',
    alt: '에볼루션카지노 크레이지타임 게임쇼', keyword: '에볼루션카지노 슬롯', rtp: '',
    desc: '에볼루션의 독창적인 라이브 게임쇼 타이틀을 소개합니다. 크레이지타임(Crazy Time), 모노폴리 라이브(Monopoly Live), 드림캐처(Dream Catcher), 딜오어노딜(Deal or No Deal) 등 실시간 엔터테인먼트 경험을 제공합니다.',
  },
]

const featuredGame: Game = {
  name: '라이브카지노', href: '/live-casino', img: '/images/live-casino.jpg',
  alt: '에볼루션 라이브카지노 HD 스트리밍', keyword: '에볼루션 라이브카지노', rtp: '',
  desc: '실제 딜러와 실시간 HD 스트리밍으로 진행되는 전 세계 최고 수준의 라이브 카지노입니다. 실제 카드·룰렛으로 게임이 진행되어 조작 가능성이 없으며 진짜 카지노와 동일한 경험을 제공합니다.',
}

const blogCard: Game = {
  name: '블로그', href: '/blog', img: '/images/blog.jpg',
  alt: '에볼루션카지노 전략 가이드 블로그', keyword: '에볼루션카지노 전략', rtp: '',
  desc: '에볼루션카지노 전략, 규칙, 팁을 전문가가 분석한 최신 가이드입니다. 초보자부터 전략적 베팅을 원하는 고수까지 모두에게 유용한 바카라·블랙잭·룰렛 공략법을 상세히 안내합니다.',
}

const seoBlocks: SeoBlock[] = [
  {
    icon: '🃏',
    title: '에볼루션카지노 바카라 — 규칙과 전략',
    paras: [
      '에볼루션카지노 바카라는 아시아 시장에서 가장 인기 있는 라이브 카지노 게임입니다. 기본 규칙은 뱅커(Banker)와 플레이어(Player) 중 합이 9에 가까운 쪽에 베팅하는 방식으로, 진행 속도가 빠르고 규칙이 간단해 초보자도 쉽게 즐길 수 있습니다.',
      '에볼루션이 제공하는 바카라 종류는 다양합니다. 스피드 바카라는 한 라운드가 27초 내에 완료되며, 라이트닝 바카라는 카드당 2×~8× 멀티플라이어가 중첩 적용되어 최대 512배 배당이 가능합니다. 스퀴즈 바카라는 딜러가 직접 카드를 천천히 뒤집는 긴장감을 제공하며, No Commission 바카라는 뱅커 베팅 시 커미션 5%가 없어 실질 환수율이 높습니다.',
      '통계적으로 뱅커 베팅 승률은 약 45.86%, 플레이어 베팅은 44.62%, 타이는 9.52%입니다. RTP(환수율) 기준으로 뱅커 베팅은 98.94%, 플레이어 베팅은 98.76%이며, 어떤 베팅을 선택하든 하우스 엣지가 존재하므로 손실 가능성을 항상 인식하십시오.',
    ],
  },
  {
    icon: '🂡',
    title: '에볼루션카지노 블랙잭 — 기본 전략과 변형 게임',
    paras: [
      '에볼루션카지노 블랙잭은 딜러보다 21에 가까운 패를 만들면 이기는 게임으로, 기본 전략(Basic Strategy)을 완벽히 적용할 경우 RTP가 99% 이상에 달해 카지노 게임 중 가장 높은 환수율을 제공합니다.',
      '인피니트 블랙잭(Infinite Blackjack)은 착석 인원 제한 없이 무제한으로 참여 가능한 혁신적인 형식입니다. 스피드 블랙잭은 히트·스탠드 결정을 더 빠르게 내려야 하는 방식으로 긴장감이 높습니다. 라이트닝 블랙잭은 각 라운드마다 무작위 카드에 2×~25× 멀티플라이어가 부여됩니다.',
      '기본 전략의 핵심은 딜러 업카드에 따라 최적의 행동(히트·스탠드·더블·스플릿)을 선택하는 것입니다. 딜러 업카드가 6 이하이면 스탠드, 11이면 더블다운이 확률적으로 높은 선택입니다. 에볼루션 블랙잭은 멀티덱(6~8덱)으로 운영됩니다.',
    ],
  },
  {
    icon: '🎡',
    title: '에볼루션카지노 룰렛 — 라이트닝 룰렛 완벽 분석',
    paras: [
      '에볼루션 라이트닝 룰렛(Lightning Roulette)은 일반 유럽식 룰렛에 무작위 멀티플라이어 요소를 결합한 게임입니다. 매 스핀마다 2~5개의 숫자에 50×, 100×, 200×, 300×, 400×, 500× 중 하나의 배율이 무작위로 부여되어 일반 룰렛(최대 35×)보다 훨씬 큰 당첨금을 기대할 수 있습니다.',
      '이머시브 룰렛(Immersive Roulette)은 다중 HD 카메라 앵글로 공이 굴러가는 모습을 슬로우 모션으로 재생해 시각적 몰입감을 극대화합니다. 더블볼 룰렛(Double Ball Roulette)은 한 번의 스핀에 두 개의 공을 사용하는 독특한 변형 게임입니다.',
      "유럽식 룰렛(싱글 제로)은 아메리칸 룰렛(더블 제로)보다 하우스 엣지가 낮습니다. 마틴게일, 피보나치, D'Alembert 등의 베팅 시스템은 단기 흐름을 관리하는 방식이지만, 장기적으로 하우스 엣지를 없애지는 못합니다.",
    ],
  },
  {
    icon: '📋',
    title: '에볼루션카지노 가입 방법과 이용 안내',
    paras: [
      "에볼루션카지노 가입은 에볼루션 게임을 제공하는 온라인 카지노 사이트를 통해 이루어집니다. 에볼루션 Gaming은 B2B 소프트웨어 제공업체로 직접 가입은 불가능하며, 에볼루션 라이센스를 보유한 파트너 카지노에 회원가입 후 해당 사이트의 '라이브 카지노' 섹션에서 에볼루션 게임을 이용할 수 있습니다.",
      '에볼루션카지노 최소 베팅 금액은 테이블마다 다릅니다. 일반 바카라·블랙잭 테이블은 $1~$5부터 시작하며, 스피드 바카라도 소액으로 참여 가능합니다. VIP 전용 살롱 프리베(Salon Privé) 테이블은 고액 베팅자를 위한 공간으로 별도 초대가 필요합니다.',
      '모바일 환경에서의 이용도 매우 편리합니다. iOS(Safari)와 Android(Chrome) 브라우저에서 별도 앱 설치 없이 풀HD 라이브 스트리밍을 즐길 수 있으며, 세로 모드와 가로 모드 모두 최적화되어 있습니다. 안정적인 인터넷 연결(최소 5Mbps 권장) 환경에서 끊김 없는 라이브 게임을 경험할 수 있습니다.',
    ],
  },
]

// ─── 메인 컴포넌트 ──────────────────────────────────────────────────────────
export default function Home() {
  const faqList: FAQItem[] = faqJsonLd.mainEntity

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdArticle) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(faqJsonLd) }} />

      <main className="min-h-screen text-white" style={{ background: '#0A0A0F' }}>

        {/* 1. HERO 섹션 (제휴 안내 복구) */}
        <section className="relative flex flex-col items-center justify-center min-h-screen text-center px-6 py-24 overflow-hidden">
          <div className="absolute inset-0 z-0">
            <Image src="/images/hero.jpg" alt="에볼루션카지노 라이브 딜러" fill className="object-cover" style={{ opacity: 0.18 }} priority sizes="100vw" />
          </div>
          
          <div className="relative z-10 max-w-4xl mx-auto">
            <div className="inline-flex items-center gap-2 mb-8 px-5 py-2 rounded-full text-xs tracking-widest uppercase"
              style={{ border: '1px solid rgba(201,168,76,0.25)', background: 'rgba(201,168,76,0.06)', color: '#C9A84C' }}>
              세계 1위 라이브 카지노 소프트웨어
            </div>

            <h1 className="font-bold leading-none mb-3" style={{ fontSize: 'clamp(52px, 9vw, 110px)', fontFamily: 'Georgia, serif' }}>
              EVOLUTION
            </h1>
            <p className="font-bold mb-8" style={{ fontSize: 'clamp(26px, 4vw, 50px)', color: '#C9A84C', fontFamily: 'Georgia, serif' }}>
              에볼루션카지노 완벽 가이드
            </p>
            <p className="mb-12 leading-relaxed" style={{ color: '#AAAABC', maxWidth: 560, margin: '0 auto 48px' }}>
              바카라, 블랙잭, 룰렛 전략부터 가입방법까지.<br />
              에볼루션카지노의 모든 정보를 WOORIWIN에서 확인하세요.
            </p>


            <div className="flex flex-col gap-4 items-center">
              {/* ✅ YMYL: 제휴 광고 투명성 명시 (이미지에 있던 부분 복구) */}
              <p className="text-xs" style={{ color: 'rgba(201,168,76,0.6)', letterSpacing: '0.05em' }}>
                ※ 아래 버튼은 광고제휴 파트너 링크입니다
              </p>
              
              <Link
                href="https://ac24mj.com/"
                target="_blank"
                rel="noopener noreferrer nofollow sponsored"
                className="cta-glow inline-flex flex-col items-center justify-center gap-1 font-bold transition-all hover:-translate-y-1 w-80"
                style={{ background: '#C9A84C', color: '#0A0A0F', padding: '20px', borderRadius: 3 }}
              >
                <span className="text-base">에볼루션카지노 지금 체험하기 →</span>
              </Link>
              
              <p className="text-xs" style={{ color: 'rgba(201,168,76,0.45)' }}>
                ✓ eCOGRA 인증 파트너 · 안전한 광고제휴
              </p>

              <Link
                href="/blog"
                className="inline-flex items-center justify-center gap-2 font-medium transition-all hover:bg-yellow-400/10 w-80"
                style={{ border: '1px solid rgba(201,168,76,0.4)', color: '#C9A84C', padding: '18px', borderRadius: 3 }}
              >
                에볼루션카지노 블로그
              </Link>
            </div>
          </div>
        </section>

        {/* 2. ABOUT 섹션 */}
        <section style={{ borderTop: '1px solid rgba(201,168,76,0.12)' }}>
          <div className="max-w-6xl mx-auto px-6 py-28">
            
            {/* 상단 타이틀 */}
            <div className="text-center mb-16">
              <p className="flex items-center justify-center gap-3 text-xs tracking-widest uppercase mb-4" style={{ color: '#C9A84C', letterSpacing: '0.25em' }}>
                <span style={{ width: 40, height: 1, background: '#C9A84C', opacity: 0.5 }} />
                About Evolution
                <span style={{ width: 40, height: 1, background: '#C9A84C', opacity: 0.5 }} />
              </p>
              <h2 className="font-bold leading-tight" style={{ fontSize: 'clamp(32px, 5vw, 48px)', fontFamily: 'Georgia, serif' }}>
                에볼루션<span style={{ color: '#C9A84C' }}>카지노란?</span>
              </h2>
            </div>

            {/* ✅ 수치 1*4 가로 배치 그리드 */}
            <div className="grid grid-cols-2 md:grid-cols-4 gap-px mb-20" style={{ border: '1px solid rgba(201,168,76,0.2)', background: 'rgba(201,168,76,0.2)' }}>
              {[
                { value: '1,000+', label: '제휴 카지노 수' },
                { value: '98.94%', label: '바카라 RTP' },
                { value: '24/7', label: '운영 시간' },
                { value: 'HD', label: '라이브 스트리밍' },
              ].map(({ value, label }) => (
                <div key={label} className="py-10 px-4 bg-[#0A0A0F] text-center transition-colors hover:bg-[#111118]">
                  <p className="leading-none mb-3 font-bold" style={{ fontSize: 'clamp(28px, 3vw, 36px)', color: '#C9A84C', fontFamily: 'Georgia, serif' }}>
                    {value}
                  </p>
                  <p className="text-xs tracking-wide font-medium" style={{ color: '#AAAABC' }}>{label}</p>
                </div>
              ))}
            </div>

            {/* ✅ 그리드 하단 상세 설명 문구 */}
            <div className="grid md:grid-cols-2 gap-x-16 gap-y-10">
              {[
                { 
                  bold: '에볼루션카지노(Evolution Gaming)', 
                  rest: '는 2006년 설립된 세계 최대 라이브 카지노 소프트웨어 제공업체입니다. 스웨덴 스톡홀름에 본사를 두고 있으며, 나스닥 스톡홀름에 상장된 합법적인 글로벌 기업입니다.' 
                },
                { 
                  bold: '실제 딜러(Live Dealer)', 
                  rest: '가 진행하는 게임을 HD 화질로 실시간 제공하는 것이 특징입니다. 전문 교육을 이수한 딜러들이 24시간 365일 실시간으로 게임을 진행하여 현장감을 극대화합니다.' 
                },
                { 
                  bold: '에볼루션 바카라', 
                  rest: '는 아시아 시장에서 압도적인 인기를 자랑하며, 스피드 바카라, 라이트닝 바카라, 스퀴즈 바카라 등 독자적이고 다양한 변형 게임 라인업을 보유하고 있습니다.' 
                },
                { 
                  bold: '공정성과 신뢰성', 
                  rest: '은 에볼루션의 핵심 가치입니다. 모든 게임은 eCOGRA 등 국제 공인 기관의 인증을 거치며, 실시간 HD 스트리밍을 통해 조작 불가능한 투명한 게임 환경을 보장합니다.' 
                }
              ].map((item, i) => (
                <div key={i} className="relative pl-7 text-[15px] leading-relaxed" style={{ color: '#AAAABC' }}>
                  {/* 포인트 아이콘(점) */}
                  <span className="absolute left-0 top-2 w-1.5 h-1.5 rounded-full" style={{ background: '#C9A84C' }} />
                  <strong style={{ color: '#fff', fontWeight: 600, display: 'block', marginBottom: '4px' }}>{item.bold}</strong>
                  {item.rest}
                </div>
              ))}
            </div>

          </div>
        </section>
        {/* 3. GAMES 그리드 섹션 */}
        <section style={{ borderTop: '1px solid rgba(201,168,76,0.12)' }}>
          <div className="max-w-7xl mx-auto px-6 py-28">
            <h2 className="font-bold mb-16 text-center" style={{ fontSize: 'clamp(28px, 4vw, 48px)', fontFamily: 'Georgia, serif' }}>
              게임별 <span style={{ color: '#C9A84C' }}>완벽 가이드</span>
            </h2>
            <div className="grid sm:grid-cols-2 lg:grid-cols-3 gap-5">
              {[...games, featuredGame, blogCard].map((game) => (
                <Link key={game.href} href={game.href} className="group block bg-[#111118] border border-gray-800 rounded-xl overflow-hidden hover:border-[#C9A84C] transition-all">
                  <div className="relative h-48 overflow-hidden">
                    <Image src={game.img} alt={game.alt} fill className="object-cover opacity-70 group-hover:scale-105 transition-transform" />
                  </div>
                  <div className="p-6">
                    <h3 className="font-bold mb-3" style={{ color: '#F5F0E8' }}>{game.keyword}</h3>
                    <p className="text-sm leading-relaxed mb-5" style={{ color: '#AAAABC' }}>{game.desc}</p>
                    <span className="text-xs text-[#C9A84C] uppercase tracking-widest">자세히 보기 →</span>
                  </div>
                </Link>
              ))}
            </div>
          </div>
        </section>

        {/* 4. SEO 상세 내용 섹션 */}
        <section style={{ borderTop: '1px solid rgba(201,168,76,0.12)' }}>
          <div className="max-w-5xl mx-auto px-6 py-28">
            <h2 className="font-bold mb-16" style={{ fontSize: 'clamp(28px, 4vw, 48px)', fontFamily: 'Georgia, serif' }}>
              에볼루션카지노 <span style={{ color: '#C9A84C' }}>게임별 심층 분석</span>
            </h2>
            <div className="flex flex-col gap-px bg-gray-800">
              {seoBlocks.map((block) => (
                <div key={block.title} className="bg-[#111118] p-10">
                  <h3 className="font-bold text-lg mb-6 flex items-center gap-3" style={{ color: '#F5F0E8' }}>
                    <span>{block.icon}</span> {block.title}
                  </h3>
                  <div className="space-y-4">
                    {block.paras.map((para, i) => (
                      <p key={i} className="text-sm leading-relaxed" style={{ color: '#AAAABC' }}>{para}</p>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* 5. FAQ 섹션 */}
        <section style={{ borderTop: '1px solid rgba(201,168,76,0.12)' }}>
          <div className="max-w-3xl mx-auto px-6 py-28">
            <h2 className="font-bold mb-16 text-center" style={{ fontSize: 'clamp(28px, 4vw, 48px)', fontFamily: 'Georgia, serif' }}>
              자주 묻는 <span style={{ color: '#C9A84C' }}>질문</span>
            </h2>
            <div className="space-y-2">
              {faqList.map((faq) => (
                <details key={faq.name} className="group border-b border-gray-800">
                  <summary className="flex justify-between items-center py-6 cursor-pointer list-none font-medium text-sm hover:text-yellow-400" style={{ color: '#F5F0E8' }}>
                    {faq.name}
                    <span className="text-[#C9A84C] group-open:rotate-45 transition-transform">+</span>
                  </summary>
                  <div className="pb-6 pl-5 border-l-2 border-[#C9A84C]">
                    <p className="text-sm leading-relaxed" style={{ color: '#AAAABC' }}>{faq.acceptedAnswer.text}</p>
                  </div>
                </details>
              ))}
            </div>
          </div>
        </section>

      </main>
    </>
  )
}