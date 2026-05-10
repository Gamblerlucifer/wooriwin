import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: '책임감 있는 게임 | WOORIWIN',
  description: '문제 도박 징후 체크리스트, 건전한 게임 팁, 한국도박문제관리센터 1336 상담 안내.',
  alternates: { canonical: 'https://wooriwin.com/responsible-gaming' },
  robots: { index: false, follow: false },
}

const signs = [
  '손실을 만회하려는 목적으로 게임을 계속하고 있다',
  '게임 시간이나 금액을 스스로 통제하기 어렵다',
  '게임 때문에 일상생활, 직장, 인간관계에 지장이 생겼다',
  '게임 비용을 마련하기 위해 돈을 빌리거나 중요한 것을 포기한 적이 있다',
  '가족이나 친구에게 게임 습관을 숨기고 있다',
  '게임을 하지 않으면 불안하거나 초조하다',
]

const tips = [
  { title: '손실 한도 설정', desc: '하루·주·월 단위로 잃어도 되는 최대 금액을 미리 정하고, 그 금액에 도달하면 즉시 중단하세요.' },
  { title: '시간 한도 설정', desc: '게임 전 최대 플레이 시간을 정하고 알람을 설정하세요. 시간이 지나면 결과와 관계없이 중단합니다.' },
  { title: '냉정한 상태 유지', desc: '음주 상태이거나 감정적으로 불안정할 때는 게임을 삼가세요. 판단력이 흐려지면 손실이 커집니다.' },
  { title: '오락으로만 접근', desc: '카지노 게임을 수익 수단이 아닌 오락으로만 접근하세요. 장기적으로 하우스는 항상 엣지를 가집니다.' },
]

const jsonLdBreadcrumb = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [
    { '@type': 'ListItem', position: 1, name: '홈', item: 'https://wooriwin.com' },
    { '@type': 'ListItem', position: 2, name: '책임감 있는 게임', item: 'https://wooriwin.com/responsible-gaming' },
  ],
}

export default function ResponsibleGaming() {
  return (
    <main className="min-h-screen text-white" style={{ background: '#0A0A0F' }}>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdBreadcrumb) }} />

      {/* Header */}
      <section style={{ borderBottom: '1px solid rgba(201,168,76,0.15)', background: '#111118' }}>
        <div className="max-w-3xl mx-auto px-6 py-16">
          <nav aria-label="breadcrumb" className="text-sm text-gray-500 mb-6">
            <Link href="/" className="hover:text-yellow-400 transition">홈</Link>
            <span className="mx-2">›</span>
            <span className="text-gray-400">책임감 있는 게임</span>
          </nav>
          <p className="text-xs tracking-widest uppercase mb-3" style={{ color: '#C9A84C' }}>Responsible Gaming</p>
          <h1 className="text-3xl md:text-4xl font-bold mb-4" style={{ fontFamily: 'Georgia, serif' }}>책임감 있는 게임</h1>
          <p className="text-sm leading-relaxed" style={{ color: '#8A8A9A' }}>
            WOORIWIN은 건전한 게임 문화를 지향합니다. 게임은 오락이어야 하며, 삶을 해쳐서는 안 됩니다.
          </p>
          <p className="text-xs mt-4" style={{ color: '#8A8A9A' }}>마지막 업데이트: 2026년 5월</p>
        </div>
      </section>

      <div className="max-w-3xl mx-auto px-6 py-16 space-y-14">

        {/* 경고 */}
        <div className="rounded-xl p-6" style={{ background: 'rgba(120,20,20,0.25)', border: '1px solid rgba(180,30,30,0.4)' }}>
          <p className="font-bold text-red-400 mb-3 flex items-center gap-2">
            <span aria-hidden="true">⚠️</span> 중요 안내
          </p>
          <ul className="text-sm space-y-2" style={{ color: '#fca5a5' }}>
            <li><span aria-hidden="true">•</span> 카지노 게임에는 항상 금전적 손실 위험이 따릅니다.</li>
            <li><span aria-hidden="true">•</span> <strong>만 18세 미만은 이용하실 수 없습니다.</strong></li>
            <li><span aria-hidden="true">•</span> 도박은 수익 수단이 아닌 오락으로만 즐기시기 바랍니다.</li>
          </ul>
        </div>

        {/* 문제 도박 징후 */}
        <div>
          <h2 className="font-bold text-white mb-6 text-base" style={{ borderLeft: '2px solid #C9A84C', paddingLeft: 16 }}>
            문제 도박 징후 체크리스트
          </h2>
          <p className="text-sm mb-6" style={{ color: '#8A8A9A' }}>
            다음 중 하나라도 해당된다면 전문 기관의 도움을 받으시기 바랍니다.
          </p>
          <ul className="space-y-3">
            {signs.map((sign) => (
              <li key={sign} className="flex items-start gap-3 text-sm p-4 rounded-lg" style={{ background: '#111118', border: '1px solid rgba(201,168,76,0.1)', color: '#B0B0C0' }}>
                {/* □ 기호 → aria-hidden 처리 */}
                <span aria-hidden="true" style={{ color: '#C9A84C', marginTop: 1 }}>□</span>
                {sign}
              </li>
            ))}
          </ul>
        </div>

        {/* 건전한 게임 팁 */}
        <div>
          <h2 className="font-bold text-white mb-6 text-base" style={{ borderLeft: '2px solid #C9A84C', paddingLeft: 16 }}>
            건전한 게임을 위한 팁
          </h2>
          <div className="grid sm:grid-cols-2 gap-px" style={{ background: 'rgba(201,168,76,0.08)' }}>
            {tips.map((t) => (
              <div key={t.title} className="p-6" style={{ background: '#111118' }}>
                <h3 className="font-bold text-sm mb-2" style={{ color: '#C9A84C' }}>{t.title}</h3>
                <p className="text-xs leading-relaxed" style={{ color: '#8A8A9A' }}>{t.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* 상담 기관 */}
        <div>
          <h2 className="font-bold text-white mb-6 text-base" style={{ borderLeft: '2px solid #C9A84C', paddingLeft: 16 }}>
            도움받을 수 있는 기관
          </h2>
          <div className="space-y-4">

            {/* kcgp 카드 — <a> 중첩 방지: 카드는 div, 전화번호만 <a> */}
            <div
              className="flex items-center justify-between p-5 rounded-xl"
              style={{ background: '#111118', border: '1px solid rgba(201,168,76,0.2)' }}
            >
              <div>
                <a
                  href="https://www.kcgp.or.kr"
                  target="_blank"
                  rel="noopener noreferrer"
                  className="font-bold text-white text-sm hover:text-yellow-400 transition"
                >
                  한국도박문제관리센터
                </a>
                <p className="text-xs mt-1" style={{ color: '#8A8A9A' }}>전화상담 · 대면상담 · 온라인 상담 제공</p>
              </div>
              <div className="text-right shrink-0">
                <a href="tel:1336" className="font-bold text-lg" style={{ color: '#C9A84C' }}>1336</a>
                <p className="text-xs" style={{ color: '#8A8A9A' }}>24시간 무료</p>
              </div>
            </div>

            <div className="p-5 rounded-xl" style={{ background: '#111118', border: '1px solid rgba(201,168,76,0.1)' }}>
              <p className="font-bold text-white text-sm mb-1">정신건강 위기상담 전화</p>
              <p className="text-xs mb-2" style={{ color: '#8A8A9A' }}>정신건강 위기 상황 전반에 걸친 24시간 상담</p>
              <a href="tel:15770199" className="font-bold" style={{ color: '#C9A84C' }}>1577-0199</a>
            </div>

          </div>
        </div>

      </div>
    </main>
  )
}
