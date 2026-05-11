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
  description: '에볼루션카지노 전략·분석 전문 콘텐츠 플랫폼',
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
  description: 'WOORIWIN은 에볼루션카지노 전략·분석 전문 콘텐츠 플랫폼입니다.',
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

// ─── 팀원 데이터 ───────────────────────────────────────────────────────────
const teamMembers = [
  {
    id: '01',
    name: '박성준',
    role: 'WOORIWIN 대표',
    experience: '15년+',
    articles: null,
    image: '/about/01.jpg',
    bio: '글로벌 금융 보안 전문가 출신으로, 불투명한 온라인 게이밍 시장에 \'데이터 기반 신뢰\'라는 표준을 세우기 위해 WOORIWIN을 설립했습니다. 단순한 홍보가 아닌, 철저한 라이선스 검증과 자본력 분석을 통해 사용자가 안심하고 즐길 수 있는 생태계를 구축하는 데 앞장서고 있습니다.',
    category: '운영',
    specialty: ['보안 및 라이선스', '최신 트렌드'],
  },
  {
    id: '02',
    name: '김도현',
    role: '라이브카지노 전문가',
    experience: '10년+',
    articles: 87,
    image: '/about/02.jpg',
    bio: '해외 메이저 카지노의 플로어 매니저 경력을 바탕으로 라이브 스트리밍의 공정성을 현미경처럼 분석합니다. 딜러의 숙련도, 카드 슈의 투명성, 0.1초의 레이턴시까지 놓치지 않는 날카로운 시각으로 실제 베팅 환경의 모든 변수를 수치화하여 전달합니다.',
    category: '전문가',
    specialty: ['바카라 가이드', '블랙잭 가이드', '룰렛 & 포커', '게임쇼 분석'],
  },
  {
    id: '03',
    name: '이수연',
    role: '콘텐츠 전문가',
    experience: '8년+',
    articles: 143,
    image: '/about/03.jpg',
    bio: '복잡하게 얽힌 카지노 룰과 보너스 약관을 누구나 이해할 수 있는 직관적인 콘텐츠로 재구성합니다. UX 중심의 가이드 제작을 총괄하며, 초보자와 숙련자 모두가 길을 잃지 않도록 가장 친절하고 명확한 콘텐츠 로드맵을 설계합니다.',
    category: '콘텐츠',
    specialty: ['에볼루션 가이드', '모바일 최적화'],
  },
  {
    id: '04',
    name: '최민석',
    role: '에디터',
    experience: '12년+',
    articles: 210,
    image: '/about/04.jpg',
    bio: '화려한 광고 문구 뒤에 숨겨진 \'진짜 데이터\'를 추적하는 저널리스트입니다. 수천 개의 게임 데이터를 대조하여 실제 RTP와 입출금 속도의 상관관계를 파헤치며, 타협 없는 팩트 체크로 플랫폼의 단점까지 가감 없이 기록합니다.',
    category: '에디터',
    specialty: ['에볼루션 가이드', '최신 트렌드', '자금 관리'],
  },
  {
    id: '05',
    name: '정혜진',
    role: '책임도박 담당',
    experience: '11년+',
    articles: 56,
    image: '/about/05.jpg',
    bio: '상담 심리학 석사로서 게임의 즐거움이 삶의 침해로 이어지지 않도록 방어선을 구축합니다. 도박 중독 예방 가이드를 설계하고, 모든 플랫폼 리뷰에 \'안전 베팅 지수\'를 도입하여 과몰입 방지를 위한 실질적인 솔루션을 제공합니다.',
    category: '전문가',
    specialty: ['책임감 있는 게임', '자금 관리'],
  },
  {
    id: '06',
    name: '한재원',
    role: '커뮤니티 매니저',
    experience: '6년+',
    articles: null,
    image: '/about/06.jpg',
    bio: '유저들의 생생한 목소리를 수집하여 리뷰의 완성도를 높이는 소통의 가교입니다. 대형 게임 커뮤니티 운영 노하우를 살려 허위 리뷰를 걸러내고 유저와 업체 간 분쟁 발생 시 중재자 역할을 수행하며, 플레이어의 집단지성이 핵심 기준이 되도록 관리합니다.',
    category: '커뮤니티',
    specialty: ['에볼루션 가이드', '모바일 최적화'],
  },
]

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
  { label: '검수 게임 수', value: '120+' },
  { label: '콘텐츠 업데이트', value: '주간' },
  { label: '검수 기준', value: 'RTP · 규칙' },
  { label: '책임도박 정책', value: '상시 적용' },
]

// ─── 외부 출처 ─────────────────────────────────────────────────────────────
const sources = [
  { label: 'Evolution 공식 사이트', href: 'https://www.evolution.com' },
  { label: 'eCOGRA 인증 기관', href: 'https://ecogra.org' },
  { label: '한국도박문제관리센터', href: 'https://www.kcgp.or.kr' },
]

export const metadata: Metadata = {
  title: 'WOORIWIN 소개',
  description:
    'WOORIWIN은 에볼루션카지노 전략·분석 전문 콘텐츠 플랫폼입니다. RTP·게임 규칙·책임도박 정책 기반 콘텐츠를 제공합니다.',
  alternates: { canonical: 'https://wooriwin.com/about' },
  robots: { index: true, follow: true },
  openGraph: {
    title: 'WOORIWIN 소개',
    description: '에볼루션카지노 전략·분석 전문 콘텐츠 플랫폼',
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
    <main className="min-h-screen text-white" style={{ background: '#0A0A0F' }}>
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdOrg) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdBreadcrumb) }}
      />
      <script
        type="application/ld+json"
        dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdWebPage) }}
      />

      {/* ── HEADER ── */}
      <section
        style={{
          borderBottom: '1px solid rgba(201,168,76,0.15)',
          background: '#111118',
        }}
      >
        <div className="max-w-4xl mx-auto px-6 py-20">
          <nav aria-label="breadcrumb" className="text-sm text-gray-500 mb-6">
            <Link href="/" className="hover:text-yellow-400 transition">
              홈
            </Link>
            <span className="mx-2">›</span>
            <span className="text-gray-400">소개</span>
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
            WOORIWIN은 에볼루션카지노 관련 게임 규칙, RTP, 전략, 책임도박
            정책을 기반으로 콘텐츠를 제작하는 정보형 콘텐츠 플랫폼입니다.
          </p>
        </div>
      </section>

      {/* ── STATS ── */}
      <section style={{ borderBottom: '1px solid rgba(201,168,76,0.08)' }}>
        <div className="max-w-6xl mx-auto px-6 py-20">
          <div className="grid grid-cols-2 md:grid-cols-4 gap-px bg-[#2A2A32]">
            {experienceData.map((item) => (
              <div key={item.label} className="bg-[#111118] p-8 text-center">
                <p
                  className="text-3xl font-bold mb-3"
                  style={{ color: '#C9A84C', fontFamily: 'Georgia, serif' }}
                >
                  {item.value}
                </p>
                <p className="text-xs tracking-wide" style={{ color: '#9A9AAA' }}>
                  {item.label}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── MISSION ── */}
      <section>
        <div className="max-w-4xl mx-auto px-6 py-20">
          <div className="pl-6" style={{ borderLeft: '2px solid #C9A84C' }}>
            <h2 className="text-xl font-bold mb-5">콘텐츠 운영 원칙</h2>
            <div
              className="space-y-5 text-sm leading-relaxed"
              style={{ color: '#9A9AAA' }}
            >
              <p>
                WOORIWIN은 카지노 게임을 단순 홍보하지 않으며, 게임 규칙·확률·RTP
                기반의 정보 제공 콘텐츠를 제작합니다.
              </p>
              <p>
                모든 콘텐츠는 Evolution 공식 자료, 게임 규칙 문서, RTP 데이터,
                책임도박 가이드라인을 기준으로 검수됩니다.
              </p>
              <p>
                콘텐츠 내 일부 링크는 광고 제휴 링크를 포함할 수 있으며, 해당
                링크는 명확하게 고지됩니다.
              </p>
              <p>
                WOORIWIN은 직접 게임 서비스를 제공하지 않으며, 모든 콘텐츠는
                정보 제공 목적입니다.
              </p>
            </div>
          </div>
        </div>
      </section>

      {/* ── TEAM ── */}
      <section style={{ borderTop: '1px solid rgba(201,168,76,0.08)' }}>
        <div className="max-w-6xl mx-auto px-6 py-20">
          {/* 헤더 */}
          <div className="mb-4">
            <p
              className="text-xs tracking-widest uppercase mb-3"
              style={{ color: '#C9A84C' }}
            >
              Our Team
            </p>
            <h2
              className="text-2xl font-bold mb-3"
              style={{ fontFamily: 'Georgia, serif' }}
            >
              콘텐츠 검수팀
            </h2>
            <p className="text-sm" style={{ color: '#9A9AAA' }}>
              에볼루션카지노 전문가들이 모든 콘텐츠의 정확성과 신뢰성을
              보장합니다.
            </p>
          </div>

          {/* 총 경력 배지 */}
          <div className="flex items-center gap-2 mb-12">
            <span
              className="text-xs px-3 py-1 rounded-full"
              style={{
                background: 'rgba(201,168,76,0.1)',
                border: '1px solid rgba(201,168,76,0.25)',
                color: '#C9A84C',
              }}
            >
              ✦ 총 합산 경력 62년+
            </span>
            <span
              className="text-xs px-3 py-1 rounded-full"
              style={{
                background: 'rgba(201,168,76,0.06)',
                border: '1px solid rgba(201,168,76,0.15)',
                color: '#8A8A9A',
              }}
            >
              전문가 6인
            </span>
          </div>

          {/* 팀원 그리드 */}
          <div className="grid md:grid-cols-2 gap-px bg-[#2A2A32]">
            {teamMembers.map((member) => (
              <article
                key={member.id}
                className="bg-[#111118] p-8 group"
                style={{ transition: 'background 0.2s' }}
              >
                <div className="flex gap-5 mb-5">
                  {/* 사진 */}
                  <div
                    className="flex-shrink-0 overflow-hidden"
                    style={{
                      width: 72,
                      height: 72,
                      borderRadius: '50%',
                      border: '2px solid rgba(201,168,76,0.3)',
                    }}
                  >
                    {/* eslint-disable-next-line @next/next/no-img-element */}
                    <img
                      src={member.image}
                      alt={`${member.name} 프로필 사진`}
                      style={{
                        objectFit: 'cover',
                        width: '100%',
                        height: '100%',
                      }}
                    />
                  </div>

                  {/* 이름 + 역할 */}
                  <div className="flex flex-col justify-center gap-1">
                    {/* 역할 배지 */}
                    <span
                      className="text-xs w-fit px-2 py-0.5"
                      style={{
                        background: 'rgba(201,168,76,0.08)',
                        border: '1px solid rgba(201,168,76,0.18)',
                        color: '#C9A84C',
                        borderRadius: 4,
                      }}
                    >
                      {member.role}
                    </span>

                    <div className="flex items-center gap-2">
                      <p
                        className="text-base font-bold"
                        style={{ color: '#F5F5F5' }}
                      >
                        {member.name}
                      </p>
                      {/* 검증 아이콘 */}
                      <svg
                        width="16"
                        height="16"
                        viewBox="0 0 16 16"
                        fill="none"
                        aria-label="검증된 전문가"
                      >
                        <circle cx="8" cy="8" r="8" fill="#C9A84C" opacity="0.15" />
                        <circle cx="8" cy="8" r="7" stroke="#C9A84C" strokeWidth="0.8" />
                        <path
                          d="M5 8l2 2 4-4"
                          stroke="#C9A84C"
                          strokeWidth="1.2"
                          strokeLinecap="round"
                          strokeLinejoin="round"
                        />
                      </svg>
                    </div>

                    {/* 경력 + 아티클 수 */}
                    <div className="flex items-center gap-3">
                      <span className="text-xs" style={{ color: '#6A6A7A' }}>
                        경력 {member.experience}
                      </span>
                      {member.articles && (
                        <>
                          <span style={{ color: '#3A3A4A', fontSize: 10 }}>|</span>
                          <span className="text-xs" style={{ color: '#6A6A7A' }}>
                            콘텐츠 {member.articles}건
                          </span>
                        </>
                      )}
                    </div>
                  </div>
                </div>

                {/* 소개글 */}
                <p
                  className="text-sm leading-relaxed"
                  style={{ color: '#7A7A8A' }}
                >
                  {member.bio}
                </p>

                {/* 하단 구분선 + 태그 */}
                <div
                  className="mt-5 pt-4 flex items-center gap-2 flex-wrap"
                  style={{ borderTop: '1px solid rgba(201,168,76,0.06)' }}
                >
                  {member.specialty.map((s) => (
                    <Link
                      key={s}
                      href={`/blog?category=${encodeURIComponent(s)}`}
                      className="text-xs px-2 py-0.5 transition hover:text-yellow-300"
                      style={{
                        background: 'rgba(201,168,76,0.08)',
                        border: '1px solid rgba(201,168,76,0.2)',
                        color: '#C9A84C',
                        borderRadius: 999,
                      }}
                    >
                      {s}
                    </Link>
                  ))}
                </div>
              </article>
            ))}
          </div>
        </div>
      </section>

      {/* ── REVIEW PROCESS ── */}
      <section style={{ borderTop: '1px solid rgba(201,168,76,0.08)' }}>
        <div className="max-w-5xl mx-auto px-6 py-20">
          <h2
            className="text-2xl font-bold mb-10"
            style={{ fontFamily: 'Georgia, serif' }}
          >
            콘텐츠 검수 프로세스
          </h2>

          <div className="grid md:grid-cols-2 gap-px bg-[#2A2A32]">
            {reviewProcess.map((item, idx) => (
              <div key={idx} className="bg-[#111118] p-8">
                <p className="text-sm font-bold mb-3" style={{ color: '#F5F5F5' }}>
                  {item.title}
                </p>
                <p className="text-sm leading-relaxed" style={{ color: '#9A9AAA' }}>
                  {item.desc}
                </p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── SOURCES ── */}
      <section style={{ borderTop: '1px solid rgba(201,168,76,0.08)' }}>
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

      {/* ── UPDATE ── */}
      <section style={{ borderTop: '1px solid rgba(201,168,76,0.08)' }}>
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
              <p>· 신규 게임 출시 시 콘텐츠 업데이트</p>
              <p>· RTP 및 게임 규칙 변경 시 수정 반영</p>
              <p>· 책임도박 정책 변경 사항 검토</p>
              <p>· 오래된 콘텐츠 정기 검수 진행</p>
              <p>· 마지막 검수일: 2026-05-11</p>
            </div>
          </div>
        </div>
      </section>

      {/* ── CONTACT ── */}
      <section style={{ borderTop: '1px solid rgba(201,168,76,0.08)' }}>
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

            <p className="text-xs leading-relaxed" style={{ color: '#8A8A9A' }}>
              본 사이트는 정보 제공 목적의 콘텐츠 플랫폼이며, 직접 게임
              서비스를 제공하거나 도박을 중개하지 않습니다.
            </p>
          </div>
        </div>
      </section>
    </main>
  )
}
