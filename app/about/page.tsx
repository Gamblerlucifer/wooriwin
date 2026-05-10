import type { Metadata } from 'next'
import Link from 'next/link'

// ─── JSON-LD ───────────────────────────────────────────────────────────────
const jsonLdOrg = {
  '@context': 'https://schema.org',
  '@type': 'Organization',
  name: 'WOORIWIN',
  url: 'https://wooriwin.com',
  logo: {
    '@type': 'ImageObject',
    url: 'https://wooriwin.com/favicon.png',
  },
  description:
    '에볼루션카지노 전략·분석 전문 콘텐츠 플랫폼',
  email: 'admin@wooriwin.com',
  foundingDate: '2026',
  sameAs: [
    'https://www.evolution.com',
    'https://ecogra.org',
    'https://www.kcgp.or.kr',
  ],
}

const jsonLdBreadcrumb = {
  '@context': 'https://schema.org',
  '@type': 'BreadcrumbList',
  itemListElement: [
    {
      '@type': 'ListItem',
      position: 1,
      name: '홈',
      item: 'https://wooriwin.com',
    },
    {
      '@type': 'ListItem',
      position: 2,
      name: 'WOORIWIN 소개',
      item: 'https://wooriwin.com/about',
    },
  ],
}

const jsonLdWebPage = {
  '@context': 'https://schema.org',
  '@type': 'AboutPage',
  name: 'WOORIWIN 소개',
  url: 'https://wooriwin.com/about',
  description:
    'WOORIWIN은 에볼루션카지노 전략·분석 전문 콘텐츠 플랫폼입니다.',
  inLanguage: 'ko-KR',
  datePublished: '2026-05-10',
  dateModified: '2026-05-11',
  reviewedBy: {
    '@type': 'Organization',
    name: 'WOORIWIN 콘텐츠 검수팀',
  },
  publisher: {
    '@type': 'Organization',
    name: 'WOORIWIN',
    url: 'https://wooriwin.com',
  },
}

// ─── 검수 데이터 ───────────────────────────────────────────────────────────
const reviewProcess = [
  {
    title: '공식 자료 검증',
    desc: 'Evolution 공식 자료, RTP 문서, 게임 규칙 자료를 기반으로 콘텐츠를 검수합니다.',
  },
  {
    title: '콘텐츠 업데이트',
    desc: '신규 게임 출시, RTP 변경, 규칙 개정 시 콘텐츠를 지속 업데이트합니다.',
  },
  {
    title: '책임도박 정책',
    desc: '모든 콘텐츠는 책임감 있는 게임 원칙을 기준으로 작성됩니다.',
  },
  {
    title: '광고 투명성',
    desc: '제휴 링크 여부를 명확하게 고지하며 콘텐츠와 광고를 구분합니다.',
  },
]

// ─── 실측 데이터 ───────────────────────────────────────────────────────────
const experienceData = [
  {
    label: '검수 게임 수',
    value: '120+',
  },
  {
    label: '콘텐츠 업데이트',
    value: '주간',
  },
  {
    label: '검수 기준',
    value: 'RTP · 규칙',
  },
  {
    label: '책임도박 정책',
    value: '상시 적용',
  },
]

// ─── 외부 출처 ─────────────────────────────────────────────────────────────
const sources = [
  {
    label: 'Evolution 공식 사이트',
    href: 'https://www.evolution.com',
  },
  {
    label: 'eCOGRA 인증 기관',
    href: 'https://ecogra.org',
  },
  {
    label: '한국도박문제관리센터',
    href: 'https://www.kcgp.or.kr',
  },
]

export const metadata: Metadata = {
  title: 'WOORIWIN 소개',
  description:
    'WOORIWIN은 에볼루션카지노 전략·분석 전문 콘텐츠 플랫폼입니다. RTP·게임 규칙·책임도박 정책 기반 콘텐츠를 제공합니다.',
  alternates: {
    canonical: 'https://wooriwin.com/about',
  },
  robots: {
    index: true,
    follow: true,
  },
  openGraph: {
    title: 'WOORIWIN 소개',
    description:
      '에볼루션카지노 전략·분석 전문 콘텐츠 플랫폼',
    url: 'https://wooriwin.com/about',
    images: [
      {
        url: 'https://wooriwin.com/og-default.jpg',
        width: 1200,
        height: 630,
        alt: 'WOORIWIN 소개',
      },
    ],
  },
}

export default function About() {
  return (
    <main
      className="min-h-screen text-white"
      style={{ background: '#0A0A0F' }}
    >
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLdOrg),
        }}
      />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLdBreadcrumb),
        }}
      />

      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{
          __html: JSON.stringify(jsonLdWebPage),
        }}
      />

      {/* HEADER */}
      <section
        style={{
          borderBottom: '1px solid rgba(201,168,76,0.15)',
          background: '#111118',
        }}
      >
        <div className="max-w-4xl mx-auto px-6 py-20">
          <nav
            aria-label="breadcrumb"
            className="text-sm text-gray-500 mb-6"
          >
            <Link
              href="/"
              className="hover:text-yellow-400 transition"
            >
              홈
            </Link>

            <span className="mx-2">›</span>

            <span className="text-gray-400">
              소개
            </span>
          </nav>

          <p
            className="text-xs tracking-widest uppercase mb-4"
            style={{ color: '#C9A84C' }}
          >
            About WOORIWIN
          </p>

          <h1
            className="text-4xl md:text-5xl font-bold mb-6"
            style={{ fontFamily: 'Georgia, serif' }}
          >
            WOORIWIN 소개
          </h1>

          <p
            className="text-base leading-relaxed max-w-3xl"
            style={{ color: '#A0A0B0' }}
          >
            WOORIWIN은 에볼루션카지노 관련
            게임 규칙, RTP, 전략, 책임도박 정책을
            기반으로 콘텐츠를 제작하는
            정보형 콘텐츠 플랫폼입니다.
          </p>
        </div>
      </section>

      {/* EXPERIENCE */}
      <section
        style={{
          borderBottom: '1px solid rgba(201,168,76,0.08)',
        }}
      >
        <div className="max-w-6xl mx-auto px-6 py-20">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-px bg-[#2A2A32]">
            {experienceData.map((item) => (
              <div
                key={item.label}
                className="bg-[#111118] p-8 text-center"
              >
                <p
                  className="text-3xl font-bold mb-3"
                  style={{
                    color: '#C9A84C',
                    fontFamily: 'Georgia, serif',
                  }}
                >
                  {item.value}
                </p>

                <p
                  className="text-xs tracking-wide"
                  style={{ color: '#9A9AAA' }}
                >
                  {item.label}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* MISSION */}
      <section>
        <div className="max-w-4xl mx-auto px-6 py-20">
          <div
            className="pl-6"
            style={{
              borderLeft: '2px solid #C9A84C',
            }}
          >
            <h2 className="text-xl font-bold mb-5">
              콘텐츠 운영 원칙
            </h2>

            <div
              className="space-y-5 text-sm leading-relaxed"
              style={{ color: '#9A9AAA' }}
            >
              <p>
                WOORIWIN은 카지노 게임을
                단순 홍보하지 않으며,
                게임 규칙·확률·RTP 기반의
                정보 제공 콘텐츠를 제작합니다.
              </p>

              <p>
                모든 콘텐츠는 Evolution 공식 자료,
                게임 규칙 문서, RTP 데이터,
                책임도박 가이드라인을 기준으로
                검수됩니다.
              </p>

              <p>
                콘텐츠 내 일부 링크는
                광고 제휴 링크를 포함할 수 있으며,
                해당 링크는 명확하게 고지됩니다.
              </p>

              <p>
                WOORIWIN은 직접 게임 서비스를
                제공하지 않으며,
                모든 콘텐츠는 정보 제공 목적입니다.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* REVIEW PROCESS */}
      <section
        style={{
          borderTop: '1px solid rgba(201,168,76,0.08)',
        }}
      >
        <div className="max-w-5xl mx-auto px-6 py-20">
          <h2
            className="text-2xl font-bold mb-10"
            style={{ fontFamily: 'Georgia, serif' }}
          >
            콘텐츠 검수 프로세스
          </h2>

          <div className="grid md:grid-cols-2 gap-px bg-[#2A2A32]">
            {reviewProcess.map((item, idx) => (
              <div
                key={idx}
                className="bg-[#111118] p-8"
              >
                <p
                  className="text-sm font-bold mb-3"
                  style={{ color: '#F5F5F5' }}
                >
                  {item.title}
                </p>

                <p
                  className="text-sm leading-relaxed"
                  style={{ color: '#9A9AAA' }}
                >
                  {item.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* SOURCES */}
      <section
        style={{
          borderTop: '1px solid rgba(201,168,76,0.08)',
        }}
      >
        <div className="max-w-4xl mx-auto px-6 py-20">
          <h2
            className="text-2xl font-bold mb-8"
            style={{ fontFamily: 'Georgia, serif' }}
          >
            참고 출처 및 검증 기관
          </h2>

          <div className="space-y-3">
            {sources.map((source) => (
              <a
                key={source.href}
                href={source.href}
                target="_blank"
                rel="noopener noreferrer"
                className="block text-sm hover:text-yellow-400 transition"
                style={{ color: '#C9A84C' }}
              >
                → {source.label}
              </a>
            ))}
          </div>
        </div>
      </section>

      {/* UPDATE */}
      <section
        style={{
          borderTop: '1px solid rgba(201,168,76,0.08)',
        }}
      >
        <div className="max-w-4xl mx-auto px-6 py-20">
          <h2
            className="text-2xl font-bold mb-8"
            style={{ fontFamily: 'Georgia, serif' }}
          >
            콘텐츠 업데이트 정책
          </h2>

          <div
            className="rounded-2xl p-8"
            style={{
              background: '#111118',
              border: '1px solid rgba(201,168,76,0.12)',
            }}
          >
            <div
              className="space-y-4 text-sm leading-relaxed"
              style={{ color: '#9A9AAA' }}
            >
              <p>
                · 신규 게임 출시 시 콘텐츠 업데이트
              </p>

              <p>
                · RTP 및 게임 규칙 변경 시 수정 반영
              </p>

              <p>
                · 책임도박 정책 변경 사항 검토
              </p>

              <p>
                · 오래된 콘텐츠 정기 검수 진행
              </p>

              <p>
                · 마지막 검수일:
                2026-05-11
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* CONTACT */}
      <section
        style={{
          borderTop: '1px solid rgba(201,168,76,0.08)',
        }}
      >
        <div className="max-w-4xl mx-auto px-6 py-20">
          <h2
            className="text-2xl font-bold mb-8"
            style={{ fontFamily: 'Georgia, serif' }}
          >
            문의 및 정책
          </h2>

          <div className="space-y-4">
            <a
              href="mailto:admin@wooriwin.com"
              className="block text-sm hover:text-yellow-400 transition"
              style={{ color: '#C9A84C' }}
            >
              admin@wooriwin.com
            </a>

            <p
              className="text-xs leading-relaxed"
              style={{ color: '#8A8A9A' }}
            >
              본 사이트는 정보 제공 목적의
              콘텐츠 플랫폼이며,
              직접 게임 서비스를 제공하거나
              도박을 중개하지 않습니다.
            </p>
          </div>
        </div>
      </section>
    </main>
  )
}