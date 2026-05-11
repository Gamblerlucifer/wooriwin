import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: '면책조항 | WOORIWIN',
  description: 'WOORIWIN 면책조항입니다. 본 사이트는 정보 제공 목적으로 운영되며 직접 게임 서비스를 제공하지 않습니다.',
  robots: { index: true, follow: true },
  alternates: {
    canonical: 'https://wooriwin.com/disclaimer',
  },
}

const sections = [
  {
    title: '1. 정보 제공 목적',
    content: `WOORIWIN은 에볼루션카지노를 포함한 라이브 카지노 게임에 관한 정보를 순수하게 교육·참고 목적으로 제공합니다. 본 사이트의 어떠한 콘텐츠도 도박 참여를 권유하거나 촉진하기 위한 것이 아닙니다.`,
  },
  {
    title: '2. 손실에 대한 면책',
    content: `카지노 게임에는 금전적 손실 위험이 따릅니다. WOORIWIN이 제공하는 전략, RTP 수치, 확률 정보 등은 참고용이며, 이를 근거로 한 베팅 결정으로 인한 손실에 대해 WOORIWIN은 어떠한 법적·도덕적 책임도 지지 않습니다.

모든 베팅의 결과와 그에 따른 책임은 전적으로 이용자 본인에게 있습니다.`,
  },
  {
    title: '3. 정보의 정확성',
    content: `본 사이트의 정보는 최대한 정확하게 작성되었으나, RTP 수치, 게임 규칙, 베팅 한도 등은 운영 카지노 및 소프트웨어 제공업체의 정책에 따라 언제든지 변경될 수 있습니다. WOORIWIN은 정보의 완전성·정확성·최신성을 보장하지 않습니다.

중요한 결정을 내리기 전에 항상 해당 카지노의 공식 정보를 직접 확인하시기 바랍니다.`,
  },
  {
    title: '4. 외부 링크 면책',
    content: `본 사이트에 포함된 제3자 카지노 사이트 링크는 편의를 위해 제공됩니다. WOORIWIN은 해당 외부 사이트의 콘텐츠, 정책, 서비스 품질에 대해 책임을 지지 않습니다. 외부 사이트 이용 전 해당 사이트의 이용약관 및 개인정보처리방침을 반드시 확인하시기 바랍니다.`,
  },
  {
    title: '5. 지역별 법적 책임',
    content: `온라인 카지노 관련 정보 열람 및 이용의 합법성은 이용자의 거주 지역에 따라 다를 수 있습니다. 해당 지역의 법률 준수 여부는 전적으로 이용자 본인의 책임입니다. WOORIWIN은 특정 지역에서의 이용으로 인한 법적 문제에 대해 책임을 지지 않습니다.`,
  },
  {
    title: '6. 미성년자 보호',
    content: `본 사이트는 만 18세 미만의 이용자를 대상으로 하지 않습니다. 미성년자의 카지노 관련 콘텐츠 접근은 엄격히 금지됩니다. 보호자는 미성년자의 인터넷 이용을 적절히 관리할 책임이 있습니다.`,
  },
]

export default function Disclaimer() {
  return (
    <main className="min-h-screen text-white" style={{ background: '#0A0A0F' }}>
      <section style={{ borderBottom: '1px solid rgba(201,168,76,0.15)', background: '#111118' }}>
        <div className="max-w-3xl mx-auto px-6 py-16">
          <nav aria-label="breadcrumb" className="text-sm text-gray-500 mb-6">
            <Link href="/" className="hover:text-yellow-400 transition">홈</Link>
            <span className="mx-2">›</span>
            <span className="text-gray-400">면책조항</span>
          </nav>
          <p className="text-xs tracking-widest uppercase mb-3" style={{ color: '#C9A84C' }}>Disclaimer</p>
          <h1 className="text-3xl md:text-4xl font-bold" style={{ fontFamily: 'Georgia, serif' }}>면책조항</h1>
        </div>
      </section>

      <div className="max-w-3xl mx-auto px-6 py-16 space-y-10">
        {/* 강조 박스 */}
        <div className="rounded-xl p-5 text-sm" style={{ background: 'rgba(120,20,20,0.25)', border: '1px solid rgba(180,30,30,0.4)', color: '#fca5a5' }}>
          <span aria-hidden="true">⚠️</span> 본 사이트는 정보 제공만을 목적으로 하며, 도박 참여를 권유하지 않습니다. 모든 게임에는 손실 위험이 따릅니다.
        </div>

        {sections.map((s) => (
          <div key={s.title} style={{ borderLeft: '2px solid rgba(201,168,76,0.3)', paddingLeft: 24 }}>
            <h2 className="font-bold text-white mb-3 text-base">{s.title}</h2>
            <p className="text-sm leading-relaxed whitespace-pre-line" style={{ color: '#8A8A9A' }}>{s.content}</p>
          </div>
        ))}

        {/* 최종 수정일 */}
        <p className="text-xs" style={{ color: '#8A8A9A' }}>마지막 업데이트: 2026년 5월 1일</p>
      </div>
    </main>
  )
}
