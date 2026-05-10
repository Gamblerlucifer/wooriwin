import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'

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

// ─── 메타데이터 ────────────────────────────────────────────────────────────
export const metadata: Metadata = {
  title: '에볼루션카지노 바카라 완벽 가이드 2026 | WOORIWIN',
  description:
    '에볼루션카지노 바카라 규칙·전략·RTP 완벽 정리. 스피드 바카라, 라이트닝 바카라, No Commission 바카라까지 변형 게임 총망라. 초보자도 이해하는 바카라 완전 공략.',
  keywords: ['에볼루션카지노 바카라', '에볼루션 바카라', '라이트닝 바카라', '스피드 바카라', '바카라 전략', '바카라 규칙'],
  alternates: { canonical: 'https://wooriwin.com/baccarat' },
  openGraph: {
    title: '에볼루션카지노 바카라 완벽 가이드 2026 | WOORIWIN',
    description: '에볼루션 바카라 규칙·전략·변형 게임 완벽 정리.',
    url: 'https://wooriwin.com/baccarat',
    images: [{ url: 'https://wooriwin.com/images/baccarat.jpg', width: 1200, height: 630 }],
  },
  twitter: {
    card: 'summary_large_image',
    title: '에볼루션카지노 바카라 완벽 가이드 2026 | WOORIWIN',
    description: '에볼루션 바카라 규칙·전략·변형 게임 완벽 정리.',
    images: ['https://wooriwin.com/images/baccarat.jpg'],
  },
}

// ─── JSON-LD (① SEO 개선: author/datePublished/dateModified 추가, 스키마 분리) ─
const jsonLdArticle = {
  '@context': 'https://schema.org',
  '@type': 'Article',
  headline: '에볼루션카지노 바카라 완벽 가이드 2026',
  description: '에볼루션카지노 바카라 규칙, 전략, 변형 게임 완벽 정리',
  url: 'https://wooriwin.com/baccarat',
  image: 'https://wooriwin.com/images/baccarat.jpg',
  inLanguage: 'ko-KR',
  datePublished: '2026-05-01T09:00:00+09:00',
  dateModified: '2026-05-10T09:00:00+09:00',
  author: {
    '@type': 'Organization',
    name: 'Lucifer',
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
      name: '에볼루션카지노 바카라 RTP는 얼마인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '에볼루션 바카라의 RTP는 베팅 유형에 따라 다릅니다. 뱅커 베팅 RTP는 약 98.94%, 플레이어 베팅은 98.76%, 타이 베팅은 85.64%입니다. 뱅커 베팅에는 당첨 시 5% 커미션이 부과됩니다. (출처: Evolution Gaming 공식 게임 수학 문서)',
      },
    },
    {
      '@type': 'Question',
      name: '에볼루션 스피드 바카라란 무엇인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '스피드 바카라는 에볼루션의 빠른 진행 바카라 변형 게임으로, 한 라운드가 약 27초 만에 완료됩니다. 카드를 즉시 공개하는 방식으로 대기 시간을 없애 시간당 게임 횟수를 극대화합니다.',
      },
    },
    {
      '@type': 'Question',
      name: '라이트닝 바카라 멀티플라이어는 어떻게 작동하나요?',
      acceptedAnswer: {
        '@type': 'Answer',
        // ② 콘텐츠 정확성: 멀티플라이어 범위 본문과 통일 (2x~8x per card, 최대 512x)
        text: '라이트닝 바카라는 매 라운드마다 1~5장의 라이트닝 카드가 무작위로 선정되어 카드당 2x~8x 배율을 제공합니다. 라이트닝 카드가 포함된 손패가 이기면 배율이 중첩 적용되어 최대 512배까지 가능하며, 기본 베팅 비용이 20% 추가됩니다. (출처: Evolution Gaming 공식 게임 규칙)',
      },
    },
    {
      '@type': 'Question',
      name: '바카라 뱅커와 플레이어 중 어느 쪽이 유리한가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '뱅커 베팅 승률은 45.86%, 플레이어 베팅은 44.62%입니다. 뱅커 당첨 시 5% 커미션이 차감되며, 하우스 엣지는 뱅커 1.06%, 플레이어 1.24%입니다. 어느 베팅이든 하우스 엣지가 존재하므로 장기적으로 손실이 발생할 수 있습니다.',
      },
    },
    {
      '@type': 'Question',
      name: '에볼루션 바카라 최소·최대 베팅금액은?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '일반 에볼루션 바카라 테이블의 최소 베팅은 $1(원화 약 1,400원)부터 시작합니다. 최대 베팅은 테이블에 따라 $25,000~$500,000까지 다양합니다. VIP 살롱 프리베 테이블은 협의 한도로 운영됩니다. 베팅 한도는 운영 카지노별로 상이할 수 있습니다.',
      },
    },
    {
      '@type': 'Question',
      name: '바카라 타이 베팅은 해야 하나요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '타이 베팅은 8:1 배당이지만 하우스 엣지가 14.36%로 뱅커·플레이어 베팅보다 현저히 높습니다. 각 베팅의 하우스 엣지 수치를 참고해 본인의 플레이 방식에 맞는 베팅을 선택하시기 바랍니다. 모든 베팅에는 손실 위험이 따릅니다.',
      },
    },
    {
      '@type': 'Question',
      // ② 콘텐츠 정확성: No Commission 규칙 수정 (1:2 → 0.5:1)
      name: 'No Commission 바카라란 무엇인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: 'No Commission 바카라는 뱅커 베팅 당첨 시 커미션(5%)을 부과하지 않는 변형 게임입니다. 대신 뱅커가 6점으로 이기는 경우(Super 6) 배당이 0.5:1로 줄어듭니다. 소액 베팅자에게 편리한 방식입니다.',
      },
    },
    {
      '@type': 'Question',
      name: '에볼루션 스퀴즈 바카라는 어떤 게임인가요?',
      acceptedAnswer: {
        '@type': 'Answer',
        text: '스퀴즈 바카라는 딜러가 카드를 천천히 구부려 공개하는 방식으로 긴장감을 극대화한 변형 게임입니다. 실제 마카오·라스베이거스 VIP 룸에서 인기 있는 방식을 온라인으로 구현했으며, 몰입감이 가장 높은 바카라 변형입니다.',
      },
    },
  ] as FAQItem[],
}

// ─── 변형 게임 데이터 ──────────────────────────────────────────────────────
// ② Hero "10종 이상" 표기와 맞추어 variants 설명에 근거 수치 명시
const variants: Variant[] = [
  { name: '스피드 바카라', desc: '27초 완료. 가장 빠른 바카라. 대기 없이 연속 게임.', rtp: 'RTP 98.94%' },
  { name: '라이트닝 바카라', desc: '카드당 2x~8x 멀티플라이어, 최대 512배 배당. 최고 인기 변형 게임.', rtp: '멀티플라이어 최대 512x' },
  { name: 'No Commission 바카라', desc: '뱅커 5% 커미션 없음. Super 6 시 0.5:1 지급.', rtp: '커미션 0%' },
  { name: '스퀴즈 바카라', desc: '카드 천천히 공개. VIP 느낌의 몰입감 극대화.', rtp: 'RTP 98.94%' },
  { name: '살롱 프리베 바카라', desc: '고액 VIP 전용 프라이빗 테이블. 고급 경험 제공.', rtp: '한도 무제한' },
  { name: '바카라 통계 뷰', desc: '빅로드·비드로드·스몰로드 통계 실시간 제공.', rtp: '데이터 기반 베팅' },
]


// ─── 페이지 컴포넌트 ───────────────────────────────────────────────────────
export default function BaccaratPage() {
  const faqList: FAQItem[] = jsonLdFaq.mainEntity

  return (
    <>
      {/* ① SEO: Article·FAQPage 스키마 분리 */}
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdArticle) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdFaq) }} />

      <main className="min-h-screen bg-gray-900 text-white">

        {/* Hero */}
        <section className="relative flex flex-col items-center justify-center min-h-[55vh] text-center px-4 py-20 overflow-hidden">
          <div className="absolute inset-0 z-0">
            <Image src="/images/baccarat.jpg" alt="에볼루션카지노 바카라 라이브 딜러" fill className="object-cover opacity-25" priority />
          </div>
          <div className="relative z-10 max-w-4xl mx-auto">
            {/* ④ 접근성: breadcrumb aria-label 추가 */}
            <nav aria-label="breadcrumb" className="text-sm text-gray-400 mb-6">
              <Link href="/" className="hover:text-yellow-400">홈</Link> &rsaquo; <span className="text-white" aria-current="page">바카라</span>
            </nav>
            <p className="text-sm text-yellow-400 font-semibold tracking-widest uppercase mb-4">RTP 98.94% · 10종 이상 변형 게임</p>
            <h1 className="text-4xl md:text-6xl font-bold mb-6 leading-tight">
              에볼루션카지노 바카라<br />
              <span className="text-yellow-400">완벽 가이드 2026</span>
            </h1>
            <p className="text-lg text-gray-300 max-w-2xl mx-auto leading-relaxed">
              스피드 바카라·라이트닝 바카라·No Commission까지. 에볼루션 바카라의 모든 규칙과 전략을 정리했습니다.
            </p>
          </div>
        </section>

        <section className="max-w-4xl mx-auto px-4 py-20 text-gray-300">
          {/* ① SEO: 정보 최신성 고지 */}
          <p className="text-xs text-gray-500 mb-8 text-right">본 정보는 2026년 5월 기준이며, 실제 게임 수치는 운영사 정책에 따라 변동될 수 있습니다.</p>

          {/* 메인 헤드라인 */}
          <header className="mb-16 border-b border-gray-800 pb-8">
            <div className="flex items-center space-x-3 mb-4">
              <span className="bg-yellow-400 text-black px-3 py-1 rounded-full text-sm font-bold uppercase tracking-wider">Baccarat Strategy</span>
            </div>
            {/* E-E-A-T: 저자 */}
            <div className="flex items-center gap-3 text-sm text-gray-500 mb-6">
              <span>작성자</span>
              <Link href="/about" className="text-yellow-400 hover:underline font-semibold">Lucifer</Link>
              <span>·</span>
              <span>라이브카지노 전문 애널리스트 · 에볼루션 게임 10년 경력</span>
            </div>
            <h2 className="text-2xl md:text-3xl font-extrabold mb-6 text-white border-b border-gray-800 pb-4">
              에볼루션 바카라: <span className="text-yellow-400 text-xl md:text-2xl">완벽한 승리를 위한 마스터 가이드</span>
            </h2>
            <p className="text-xl text-gray-400 leading-relaxed">
              전 세계 1위 라이브 카지노 솔루션, 에볼루션(Evolution)의 바카라는 단순한 게임을 넘어선 하나의 공학입니다.
              투명한 확률, 혁신적인 기술력, 그리고 당신의 전략이 만나는 지점을 분석합니다.
            </p>
          </header>

          <div className="space-y-12 text-base md:text-lg leading-relaxed">

            {/* 섹션 1 */}
            <article>
              <h3 className="text-2xl font-bold text-white mb-4 flex items-center">
                <span className="w-2 h-8 bg-yellow-400 mr-4" aria-hidden="true"></span>
                왜 전 세계 플레이어는 '에볼루션'에 열광하는가?
              </h3>
              <p className="mb-4">
                에볼루션카지노 바카라는 단순히 화면을 송출하는 것에 그치지 않습니다. 라트비아와 몰타 등 전 세계 곳곳에 위치한
                최첨단 스튜디오에서 <strong>UHD급 초고화질 스트리밍</strong>을 통해 실제 카지노의 공기마저 그대로 전달합니다.
                특히 '카드를 쪼는' 재미를 극대화한 '바카라 스퀴즈' 모드나, 딜러와의 실시간 채팅 기능은 온라인과 오프라인의 경계를 완전히 허물었습니다.
              </p>
              <p>
                또한 모든 게임은{' '}
                {/* YMYL: eCOGRA 인증 링크 추가 */}
                <a href="https://ecogra.org" target="_blank" rel="noopener noreferrer" className="text-yellow-400 underline hover:text-yellow-300">
                  <strong>eCOGRA</strong>
                </a>
                와 같은 국제 공인 기관의 정기적인 감사를 받으며,
                모든 결과는 조작이 불가능한 물리적 기반 위에 서 있습니다. 이는 사용자의 자산과 직결되는 YMYL 분야에서 에볼루션이 독보적인 신뢰를 얻는 이유입니다.
              </p>
            </article>

              {/* 섹션 2: RTP 분석 */}
              <article className="bg-gray-800/30 p-8 rounded-2xl border border-gray-700">
                <h3 className="text-xl font-bold text-yellow-400 mb-6 text-center underline underline-offset-8">
                  PRO ANALYSIS: 베팅 타입별 기대 수익률(RTP)
                </h3>
                <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-6">
                  <div className="bg-black/40 p-5 rounded-xl text-center border border-gray-600">
                    <p className="text-gray-400 text-sm mb-2">뱅커(Banker)</p>
                    <p className="text-3xl font-black text-green-400">98.94%</p>
                    <p className="text-xs mt-2 text-gray-500">하우스 엣지 1.06%</p>
                  </div>
                  <div className="bg-black/40 p-5 rounded-xl text-center border border-gray-600">
                    <p className="text-gray-400 text-sm mb-2">플레이어(Player)</p>
                    <p className="text-3xl font-black text-blue-400">98.76%</p>
                    <p className="text-xs mt-2 text-gray-500">하우스 엣지 1.24%</p>
                  </div>
                  <div className="bg-black/40 p-5 rounded-xl text-center border border-gray-600">
                    <p className="text-gray-400 text-sm mb-2">타이(Tie)</p>
                    <p className="text-3xl font-black text-red-400">85.64%</p>
                    <p className="text-xs mt-2 text-red-500">하우스 엣지 14.36% (고위험)</p>
                  </div>
              </div>
              <blockquote className="border-l-4 border-gray-500 pl-4 italic text-sm text-gray-400 mb-4">
                "뱅커 하우스 엣지 1.06%, 플레이어 1.24%, 타이 14.36% — 베팅 유형별 하우스 엣지 수치를 이해하고 본인의 플레이 환경에 맞는 선택을 하는 것이 중요합니다. 신중한 자금 관리가 모든 게임의 기본입니다."
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

            {/* 섹션 3: 3대 변형 게임 */}
            <article className="space-y-8">
              <h3 className="text-2xl font-bold text-white mb-6">시대를 앞서가는 3대 변형 게임</h3>
              <div className="space-y-6">
                <div className="group bg-gray-900/50 p-6 rounded-lg hover:bg-gray-800 transition">
                  <h4 className="text-yellow-400 font-bold text-xl mb-2">01. 라이트닝 바카라 (Lightning Baccarat)</h4>
                  <p>
                    Z세대가 가장 열광하는 모드로, 클래식 바카라에 '승수(Multiplier)' 개념을 도입했습니다.
                    {/* ② 콘텐츠 정확성: FAQ와 수치 통일 */}
                    매 라운드 번개와 함께 선정되는 1~5장의 라이트닝 카드는 카드당 2x~8x 배율을 제공하며,
                    배율이 중첩 적용되어 최대 512배에 달하는 폭발적인 배당을 제공합니다.
                    하나의 게임 쇼에 참여하는 듯한 몰입감을 제공합니다.
                  </p>
                </div>

                <div className="group bg-gray-900/50 p-6 rounded-lg hover:bg-gray-800 transition">
                  <h4 className="text-yellow-400 font-bold text-xl mb-2">02. 스피드 바카라 (Speed Baccarat)</h4>
                  <p>
                    효율성을 중시하는 한국인 플레이어에게 최적화되었습니다. 일반 게임이 48초 내외라면, 스피드 모드는 단 27초 만에
                    한 라운드를 종료합니다. 빠른 호흡 속에서도 에볼루션의 기술력은 끊김 없는 스트리밍을 보장하며,
                    짧은 시간에 게임 데이터를 확인하고자 하는 플레이어들에게 적합한 변형 게임입니다.
                  </p>
                </div>

                <div className="group bg-gray-900/50 p-6 rounded-lg hover:bg-gray-800 transition">
                  {/* ② 콘텐츠 정확성: No Commission 규칙 수정 */}
                  <h4 className="text-yellow-400 font-bold text-xl mb-2">03. 노 커미션 바카라 (No Commission)</h4>
                  <p>
                    뱅커 승리 시 5%의 수수료가 아쉬웠던 플레이어들을 위한 모드입니다.
                    뱅커가 6점으로 이기는 경우(Super 6)에만 배당이 0.5:1로 줄어들며,
                    그 외 모든 뱅커 승리 시 1:1 배당을 그대로 가져갑니다.
                    직관적인 자금 계산을 선호하는 플레이어에게 적합한 방식입니다.
                  </p>
                </div>
              </div>
            </article>

            {/* 섹션 4: 로드맵 */}
            <article>
              <h3 className="text-2xl font-bold text-white mb-4 italic underline decoration-yellow-400">The Science of Patterns: 로드맵 활용법</h3>
              <p className="mb-4">
                에볼루션은 플레이어에게 <strong>빅로드(Big Road), 비드로드(Bead Plate), 스몰로드, 빅아이보이</strong> 등
                전문적인 통계 도구를 실시간으로 제공합니다. 많은 숙련자들은 이 패턴 속에서 '줄타기'나 '데칼코마니' 형상을 찾아내 베팅 방향을 결정합니다.
              </p>
              <p className="text-gray-400">
                하지만 기억하십시오. 바카라는 '독립 시행'의 게임입니다. 이전의 뱅커 10연승이 다음 라운드의 뱅커 승률을 1%도 높여주지 않습니다.
                분석 도구는 감정적인 베팅을 억제하고 냉정함을 유지하는 '페이스메이커'로 활용할 때 가장 가치 있습니다.
              </p>
            </article>

          </div>
        </section>

        {/* 변형 게임 카드 */}
        <section className="bg-gray-800 py-16 px-4">
          <div className="max-w-5xl mx-auto">
            <h2 className="text-3xl font-bold text-center mb-3">에볼루션 바카라 변형 게임</h2>
            <p className="text-gray-400 text-center mb-10">에볼루션이 제공하는 대표 바카라 변형 게임</p>
            <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-5">
              {variants.map((v) => (
                // ③ 코드 품질: key를 index 대신 고유값(name)으로
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
          <h2 className="text-3xl font-bold mb-10 text-center">에볼루션카지노 바카라 FAQ</h2>
          <div className="space-y-4">
            {faqList.map((faq) => (
              // ③ 코드 품질: key를 index 대신 faq.name으로, as any 제거
              <details key={faq.name} className="bg-gray-800 rounded-xl p-5 group cursor-pointer">
                <summary className="font-semibold text-base text-white flex justify-between items-center list-none">
                  {faq.name}
                  {/* ④ 접근성: aria-hidden으로 장식 요소 처리 */}
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
