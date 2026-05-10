import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: '개인정보처리방침 | WOORIWIN',
  robots: { index: false, follow: false },
}

type Section = {
  title: string
  content?: string
  list?: string[]
  footer?: string
}

const sections: Section[] = [
  {
    title: '1. 수집하는 개인정보',
    content: `본 사이트(WOORIWIN)는 별도의 회원가입 없이 이용 가능한 정보 제공형 웹사이트입니다. 사용자가 직접 제공하는 개인정보는 수집하지 않습니다. 다만, 웹사이트 운영 과정에서 다음과 같은 정보가 자동으로 수집될 수 있습니다.`,
    list: [
      '접속 IP 주소',
      '방문 일시 및 이용 기록',
      '브라우저 종류 및 운영체제',
      '유입 경로(리퍼러)',
    ],
  },
  {
    title: '2. 개인정보의 수집 및 이용 목적',
    content: '자동 수집되는 정보는 다음의 목적으로만 활용됩니다.',
    list: [
      '웹사이트 운영 및 서비스 품질 개선',
      '접속 통계 분석 (Google Analytics 등 제3자 도구 활용)',
      '보안 및 서비스 안정성 유지',
    ],
  },
  {
    title: '3. 쿠키(Cookie) 사용',
    content: '본 사이트는 서비스 개선을 위해 쿠키를 사용할 수 있습니다. 쿠키는 사용자의 브라우저에 저장되는 소량의 데이터 파일로, 브라우저 설정을 통해 거부하거나 삭제할 수 있습니다.',
    list: [
      'Google Analytics: 방문자 통계 분석 목적',
      '광고 파트너 쿠키: 제휴 마케팅 성과 측정 목적',
    ],
    footer: '브라우저에서 쿠키를 비활성화해도 사이트 이용에는 지장이 없습니다.',
  },
  {
    title: '4. 제3자 링크 및 광고',
    content: `본 사이트는 제3자 온라인 카지노 사이트로 연결되는 제휴 링크를 포함합니다. 해당 외부 사이트의 개인정보처리방침은 WOORIWIN과 무관하며, 각 외부 사이트의 정책을 별도로 확인하시기 바랍니다. 외부 사이트 이용으로 인한 결과에 대해 WOORIWIN은 책임을 지지 않습니다.`,
  },
  {
    title: '5. 개인정보 보관 기간',
    content: `자동 수집되는 로그 데이터는 서비스 운영 목적에 필요한 최소한의 기간 동안만 보관하며, 목적 달성 후 즉시 파기합니다.`,
  },
  {
    title: '6. 이용자의 권리',
    content: `이용자는 언제든지 본 사이트의 정보 수집에 대해 문의하거나 관련 요청을 할 수 있습니다. 문의사항은 아래 연락처를 통해 접수해 주시기 바랍니다.`,
  },
  {
    title: '7. 개인정보처리방침 변경',
    content: `본 방침은 법령 또는 서비스 변경에 따라 수정될 수 있습니다. 변경 시 웹사이트를 통해 공지하며, 변경된 방침은 게시 즉시 효력이 발생합니다.`,
    footer: '최종 업데이트: 2026년 5월 1일',
  },
]

export default function PrivacyPolicy() {
  return <PolicyPage title="개인정보처리방침" subtitle="Privacy Policy" sections={sections} />
}

// ─── 공통 레이아웃 컴포넌트 ───────────────────────────────────────────────
function PolicyPage({ title, subtitle, sections }: {
  title: string
  subtitle: string
  sections: Section[]
}) {
  return (
    <main className="min-h-screen text-white" style={{ background: '#0A0A0F' }}>
      {/* Header */}
      <section style={{ borderBottom: '1px solid rgba(201,168,76,0.15)', background: '#111118' }}>
        <div className="max-w-3xl mx-auto px-6 py-16">
          <nav aria-label="breadcrumb" className="text-sm text-gray-500 mb-6">
            <Link href="/" className="hover:text-yellow-400 transition">홈</Link>
            <span className="mx-2">›</span>
            <span className="text-gray-400">{title}</span>
          </nav>
          <p className="text-xs tracking-widest uppercase mb-3" style={{ color: '#C9A84C' }}>{subtitle}</p>
          <h1 className="text-3xl md:text-4xl font-bold" style={{ fontFamily: 'Georgia, serif' }}>{title}</h1>
        </div>
      </section>

      {/* Content */}
      <div className="max-w-3xl mx-auto px-6 py-16 space-y-10">
        {sections.map((s) => (
          <div key={s.title} style={{ borderLeft: '2px solid rgba(201,168,76,0.3)', paddingLeft: 24 }}>
            <h2 className="font-bold text-white mb-3 text-base">{s.title}</h2>
            {s.content && (
              <p className="text-sm leading-relaxed mb-3" style={{ color: '#8A8A9A' }}>{s.content}</p>
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
            개인정보 관련 문의사항은 아래 이메일로 연락해 주시기 바랍니다.
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
