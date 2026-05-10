import type { Metadata } from 'next'
import Link from 'next/link'

export const metadata: Metadata = {
  title: 'WOORIWIN 소개 | About',
  robots: { index: false, follow: false },
}

const values = [
  { num: '01', title: '정확한 정보', desc: '모든 RTP 수치, 게임 규칙, 전략은 Evolution Gaming 공식 자료를 기반으로 작성됩니다. 출처 없는 주장은 게재하지 않습니다.' },
  { num: '02', title: '투명한 제휴 고지', desc: '외부 카지노 링크가 제휴 마케팅 링크임을 명확히 고지합니다. 수익 구조가 콘텐츠 방향에 영향을 주지 않습니다.' },
  { num: '03', title: '책임감 있는 게임 문화', desc: '도박의 위험성을 항상 명시하며, 문제 도박 예방 정보를 적극적으로 제공합니다.' },
  { num: '04', title: '지속적인 업데이트', desc: '에볼루션카지노의 신규 게임, 규칙 변경, RTP 업데이트를 지속적으로 반영합니다.' },
]

export default function About() {
  return (
    <main className="min-h-screen text-white" style={{ background: '#0A0A0F' }}>

      {/* Header */}
      <section style={{ borderBottom: '1px solid rgba(201,168,76,0.15)', background: '#111118' }}>
        <div className="max-w-3xl mx-auto px-6 py-16">
          <nav aria-label="breadcrumb" className="text-sm text-gray-500 mb-6">
            <Link href="/" className="hover:text-yellow-400 transition">홈</Link>
            <span className="mx-2">›</span>
            <span className="text-gray-400">소개</span>
          </nav>
          <p className="text-xs tracking-widest uppercase mb-3" style={{ color: '#C9A84C' }}>About WOORIWIN</p>
          <h1 className="text-3xl md:text-4xl font-bold mb-4" style={{ fontFamily: 'Georgia, serif' }}>WOORIWIN 소개</h1>
          <p className="text-sm leading-relaxed" style={{ color: '#8A8A9A' }}>
            에볼루션카지노 라이브 게임 전략, 테이블 분석, 플레이 가이드 및 건전한 게임 문화 정보를 제공하는 콘텐츠 플랫폼입니다.
          </p>
        </div>
      </section>

      <div className="max-w-3xl mx-auto px-6 py-16 space-y-14">

        {/* 미션 */}
        <div style={{ borderLeft: '2px solid #C9A84C', paddingLeft: 24 }}>
          <h2 className="font-bold text-white mb-3 text-base">우리의 미션</h2>
          <p className="text-sm leading-relaxed" style={{ color: '#8A8A9A' }}>
            WOORIWIN은 에볼루션카지노를 처음 접하는 초보자부터 전략적 플레이를 원하는 숙련자까지, 모든 플레이어가 정확한 정보를 바탕으로 현명한 결정을 내릴 수 있도록 돕습니다.
            우리는 카지노 게임의 수학적 원리와 확률을 투명하게 공개하고, 책임감 있는 게임 문화를 함께 만들어 나가고자 합니다.
          </p>
        </div>

        {/* 핵심 가치 */}
        <div>
          <h2 className="font-bold text-white mb-6 text-base">핵심 가치</h2>
          <div className="grid sm:grid-cols-2 gap-px" style={{ background: 'rgba(201,168,76,0.08)' }}>
            {values.map((v) => (
              <div key={v.num} className="p-6" style={{ background: '#111118' }}>
                <p className="font-bold mb-2 leading-none" style={{ fontSize: 40, color: 'rgba(201,168,76,0.1)', fontFamily: 'Georgia, serif' }}>{v.num}</p>
                <h3 className="font-bold text-white text-sm mb-2">{v.title}</h3>
                <p className="text-xs leading-relaxed" style={{ color: '#8A8A9A' }}>{v.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {/* 편집팀 */}
        <div style={{ borderLeft: '2px solid rgba(201,168,76,0.3)', paddingLeft: 24 }}>
          <h2 className="font-bold text-white mb-3 text-base">편집팀</h2>
          <div className="flex items-center gap-4 mt-4">
            <div className="w-12 h-12 rounded-full flex items-center justify-center shrink-0 font-bold text-xl"
              style={{ background: 'rgba(201,168,76,0.15)', border: '1px solid rgba(201,168,76,0.3)', color: '#C9A84C' }}>
              W
            </div>
            <div>
              <p className="font-bold text-white text-sm">WOORIWIN 편집팀</p>
              <p className="text-xs mt-0.5" style={{ color: '#8A8A9A' }}>
                에볼루션카지노 전문 콘텐츠 분석팀 · 바카라·블랙잭·룰렛·슬롯 가이드 제공
              </p>
            </div>
          </div>
        </div>

        {/* 면책 */}
        <div className="rounded-xl p-5 text-xs leading-relaxed" style={{ background: 'rgba(201,168,76,0.04)', border: '1px solid rgba(201,168,76,0.15)', color: '#8A8A9A' }}>
          본 사이트는 정보 제공만을 목적으로 하며, 직접 게임 서비스를 제공하거나 도박을 중개하지 않습니다.
          모든 베팅의 책임은 이용자 본인에게 있습니다.
        </div>
      </div>
    </main>
  )
}
