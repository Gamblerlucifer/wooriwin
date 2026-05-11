import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: '이용약관 | WOORIWIN',
  description: 'WOORIWIN 이용약관입니다. 서비스 이용 전 반드시 확인하시기 바랍니다.',
  robots: { index: true, follow: true },
  alternates: { canonical: 'https://wooriwin.com/terms' },
}

type Section = {
  title: string
  content?: string
  list?: string[]
  footer?: string
}

const sections: Section[] = [
  {
    title: '1. 서비스 소개',
    content: `WOORIWIN(이하 "본 사이트")은 에볼루션카지노를 비롯한 라이브 카지노 게임에 관한 정보, 규칙, 전략을 제공하는 정보형 콘텐츠 플랫폼입니다. 본 사이트는 직접적인 게임 서비스를 제공하거나 도박을 중개하지 않습니다.`,
  },
  {
    title: '2. 이용 조건',
    content: '본 사이트를 이용하기 위해서는 다음 조건을 충족해야 합니다.',
    list: [
      '만 18세 이상이어야 합니다.',
      '거주 지역에서 온라인 카지노 관련 정보 열람이 합법적이어야 합니다.',
      '본 이용약관에 동의해야 합니다.',
    ],
    footer: '위 조건에 해당하지 않는 경우 즉시 본 사이트 이용을 중단해 주시기 바랍니다.',
  },
  {
    title: '3. 제휴 마케팅 고지',
    content: `본 사이트는 제3자 온라인 카지노 사이트와의 제휴 마케팅 계약을 통해 수익을 얻을 수 있습니다. 외부 카지노 사이트로 연결되는 링크는 제휴 링크일 수 있으며, 해당 링크를 통해 가입 또는 이용 시 WOORIWIN에 수수료가 지급될 수 있습니다.

이는 콘텐츠의 객관성에 영향을 주지 않으며, 본 사이트는 항상 정확하고 중립적인 정보 제공을 원칙으로 합니다.`,
  },
  {
    title: '4. 콘텐츠 이용',
    content: `본 사이트의 모든 콘텐츠(텍스트, 이미지, 구조 등)는 WOORIWIN의 저작물입니다. 사전 서면 동의 없이 복제, 배포, 상업적 이용을 금합니다. 개인적·비상업적 목적의 인용은 출처 명시 시 허용됩니다.`,
  },
  {
    title: '5. 면책',
    content: `본 사이트가 제공하는 정보는 참고 목적으로만 제공됩니다. WOORIWIN은 정보의 정확성·완전성·최신성을 보장하지 않으며, 정보를 근거로 한 베팅·투자 결정으로 인한 손실에 대해 어떠한 법적 책임도 지지 않습니다. 자세한 내용은 면책조항 페이지를 참고해 주세요.`,
  },
  {
    title: '6. 약관 변경',
    content: `본 약관은 예고 없이 변경될 수 있습니다. 변경된 약관은 웹사이트 게시 즉시 효력이 발생합니다. 지속적인 이용은 변경된 약관에 대한 동의로 간주됩니다.`,
    footer: '최종 업데이트: 2026년 5월 1일',
  },
]

export default function Terms() {
  return (
    <main className="min-h-screen text-white" style={{ background: '#0A0A0F' }}>
      <section style={{ borderBottom: '1px solid rgba(201,168,76,0.15)', background: '#111118' }}>
        <div className="max-w-3xl mx-auto px-6 py-16">
          <nav aria-label="breadcrumb" className="text-sm text-gray-500 mb-6">
            <Link href="/" className="hover:text-yellow-400 transition">홈</Link>
            <span className="mx-2">›</span>
            <span className="text-gray-400">이용약관</span>
          </nav>
          <p className="text-xs tracking-widest uppercase mb-3" style={{ color: '#C9A84C' }}>Terms of Service</p>
          <h1 className="text-3xl md:text-4xl font-bold" style={{ fontFamily: 'Georgia, serif' }}>이용약관</h1>
        </div>
      </section>

      <div className="max-w-3xl mx-auto px-6 py-16 space-y-10">
        {sections.map((s) => (
          <div key={s.title} style={{ borderLeft: '2px solid rgba(201,168,76,0.3)', paddingLeft: 24 }}>
            <h2 className="font-bold text-white mb-3 text-base">{s.title}</h2>
            {s.content && (
              <p className="text-sm leading-relaxed whitespace-pre-line mb-3" style={{ color: '#8A8A9A' }}>{s.content}</p>
            )}
            {s.list && (
              <ul className="text-sm space-y-1 mb-3 list-none" style={{ color: '#8A8A9A' }}>
                {s.list.map((item) => (
                  <li key={item} className="flex gap-2">
                    <span aria-hidden="true" style={{ color: 'rgba(201,168,76,0.6)' }}>—</span>
                    <span>{item}</span>
                  </li>
                ))}
              </ul>
            )}
            {s.footer && (
              <p className="text-sm leading-relaxed" style={{ color: '#8A8A9A' }}>{s.footer}</p>
            )}
          </div>
        ))}

        {/* 연락처 */}
        <div style={{ borderLeft: '2px solid rgba(201,168,76,0.3)', paddingLeft: 24 }}>
          <h2 className="font-bold text-white mb-3 text-base">문의처</h2>
          <p className="text-sm mb-2" style={{ color: '#8A8A9A' }}>
            이용약관 관련 문의사항은 아래 이메일로 연락해 주시기 바랍니다.
          </p>
          <a
            href="mailto:admin@wooriwin.com"
            className="text-sm inline-block hover:opacity-80 transition"
            style={{ color: '#C9A84C' }}
          >
            admin@wooriwin.com
          </a>
        </div>
      </div>
    </main>
  )
}
