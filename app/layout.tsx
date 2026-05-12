import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import Link from "next/link";
import "./globals.css";

const geistSans = Geist({ variable: "--font-geist-sans", subsets: ["latin"] });
const geistMono = Geist_Mono({ variable: "--font-geist-mono", subsets: ["latin"] });

export const metadata: Metadata = {
  metadataBase: new URL("https://wooriwin.com"),
  robots: {
    index: true,
    follow: true,
    googleBot: {
      index: true,
      follow: true,
      "max-image-preview": "large",
      "max-snippet": -1,
    },
  },

  openGraph: {
    title: "WOORIWIN — 에볼루션카지노 완벽 가이드",
    description: "에볼루션카지노 라이브 게임 전략, 테이블 분석, 플레이 가이드 및 건전한 게임 문화 정보를 제공합니다.",
    images: [{ url: "https://wooriwin.com/og-default.jpg", width: 1200, height: 630, alt: "WOORIWIN 에볼루션카지노 가이드" }],
    siteName: "WOORIWIN",
    locale: "ko_KR",
    type: "website",
  },

  alternates: {
    canonical: "https://wooriwin.com",
    languages: { "ko-KR": "https://wooriwin.com" },
  },

  verification: {
    google: "nIE-kYgpwmgTKiQssndHTqWzLBBLBCECkbSVmSOR_Uk",
  },

  title: {
    default: "WOORIWIN",
    template: "%s",
  },

  description:
    "에볼루션카지노 라이브 게임 전략, 테이블 분석, 플레이 가이드 및 건전한 게임 문화 정보를 제공합니다.",
};
const relatedLinks = [
  { href: '/', label: '에볼루션카지노 메인' },
  { href: '/baccarat', label: '에볼루션카지노 바카라' },
  { href: '/blackjack', label: '에볼루션카지노 블랙잭' },
  { href: '/roulette', label: '에볼루션카지노 룰렛' },
  { href: '/slots', label: '에볼루션카지노 슬롯' },
  { href: '/live-casino', label: '에볼루션 라이브카지노' },
  { href: '/blog', label: '전략 블로그' },
]
const policyLinks = [
  { href: 'privacy-policy', label: '개인정보처리방침' },
  { href: 'terms', label: '이용약관' },
  { href: 'disclaimer', label: '면책조항' },
  { href: 'about', label: '소개' },
  { href: 'responsible-gaming', label: '책임감 있는 게임' },
]
const jsonLd = {
  "@context": "https://schema.org",
  "@type": "WebSite",

  "name": "WOORIWIN",
  "url": "https://wooriwin.com",

  "description":
    "에볼루션카지노 라이브 게임 전략 및 플레이 가이드를 제공하는 건전한 게임 문화 정보형 콘텐츠 플랫폼",

  "inLanguage": "ko-KR",

  "publisher": {
    "@type": "Organization",
    "name": "WOORIWIN 콘텐츠 분석팀",
    "url": "https://wooriwin.com",

    "logo": {
      "@type": "ImageObject",
      "url": "https://wooriwin.com/logo.png"
    }
  }
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="ko" className={`${geistSans.variable} ${geistMono.variable} h-full antialiased text-white`}>
      <head>
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      </head>
      <body className="min-h-full flex flex-col bg-[#0A0A0F]">
        
        {/* 1. 최상단 정책 배너: 구글 정책 준수 (고정형) */}
        <div className="bg-black/95 text-[10px] md:text-xs text-gray-500 py-2 border-b border-gray-800 text-center sticky top-0 z-[100] backdrop-blur-md">
          <div className="max-w-7xl mx-auto px-4 flex flex-col md:flex-row justify-center items-center gap-x-4 gap-y-1">
            <span className="text-red-500 font-bold"><span aria-hidden="true">🔞</span> 만 18세 미만 이용 불가</span>
            <span className="hidden md:inline text-gray-800">|</span>
            <span>본 사이트는 제휴 마케팅 링크를 포함하며 정보 제공만을 목적으로 합니다.</span>
            <span className="hidden md:inline text-gray-800">|</span>
            <span className="font-semibold text-gray-400 font-mono text-[9px] md:text-xs">도박중독 상담: 1336</span>
          </div>
        </div>

        <main className="flex-grow">
          {children}
        </main>

        {/* 2. RESPONSIBLE GAMING 섹션: 모든 페이지 공통 신뢰 신호 */}
        <section style={{ borderTop: '1px solid rgba(201,168,76,0.12)', background: '#0D0D13' }}>
          <div className="max-w-6xl mx-auto px-6 py-16">
            <div className="flex flex-col md:flex-row md:items-stretch gap-8 mb-8">
              <div className="flex-1">
                <h3 className="text-2xl font-black text-white mb-6 uppercase tracking-tighter">Responsible Gaming & Strategy</h3>
                <p className="text-gray-400 leading-relaxed mb-4 text-sm md:text-base">
                  <span className="text-white font-semibold">WOORIWIN</span>은 단순한 정보 제공을 넘어, 건전하고 지속 가능한 게임 문화를 지향합니다. 에볼루션카지노의 심층 분석 데이터는 오직 플레이어의 현명한 선택을 돕기 위해 존재합니다.
                </p>
                <p className="text-gray-400 leading-relaxed text-sm">항상 본인만의 자산 관리 원칙을 준수하시길 권장합니다.</p>
              </div>

              <div className="md:w-[340px] flex flex-col justify-between p-6 rounded-2xl"
                style={{ background: 'rgba(201,168,76,0.05)', border: '1px solid rgba(201,168,76,0.2)' }}>
                <div>
                  <div className="flex items-center gap-2 mb-4">
                    <div className="w-2 h-2 rounded-full" style={{ background: '#C9A84C' }} />
                    <p className="font-bold uppercase tracking-widest text-xs" style={{ color: '#C9A84C' }}>WOORIWIN CHECK</p>
                  </div>
                  <p className="text-sm leading-snug mb-5 text-gray-300 italic">
                    &quot;통계는 보조 지표일 뿐, 감정에 치우치지 않는 냉정한 베팅이 가장 강력한 전략입니다.&quot;
                  </p>
                  <ul className="space-y-2">
                    {['잃어도 되는 금액만 베팅하세요', '감정적 베팅은 손실을 키웁니다'].map((tip) => (
                      <li key={tip} className="flex items-start gap-2 text-xs text-gray-400">
                        <span aria-hidden="true" style={{ color: '#C9A84C' }}>✓</span> {tip}
                      </li>
                    ))}
                  </ul>
                </div>
              </div>
            </div>

            <div className="rounded-xl p-5" style={{ background: 'rgba(120,20,20,0.2)', border: '1px solid rgba(180,30,30,0.3)' }}>
              <div className="flex flex-col md:flex-row md:items-center md:justify-between gap-4">
                <div className="text-sm space-y-1 text-gray-400">
                  <p className="font-bold text-red-400 mb-2 flex items-center gap-2 text-xs md:text-sm"><span aria-hidden="true">⚠️</span> 문제 도박 예방 안내</p>
                  <p className="text-xs">· 도박은 오락 목적으로만 이용하시고, <span className="text-white underline">만 18세 미만은 이용하실 수 없습니다.</span></p>
                </div>
                <div className="shrink-0 inline-flex items-center gap-2 text-sm font-semibold px-5 py-3 rounded-lg bg-red-900/30 text-red-300 border border-red-800/50">
                  <span aria-hidden="true">📞</span>
                  <a href="https://www.kcgp.or.kr" target="_blank" rel="noopener noreferrer"
                    className="hover:text-red-200 transition">
                    도박문제관리센터
                  </a>
                  ·
                  <a href="tel:1336" className="underline hover:text-red-200 transition">1336</a>
                  <span className="text-[10px] opacity-70">(24시간 무료)</span>
                </div>
              </div>
            </div>
          </div>
        </section>

        {/* 3. 공통 정책 푸터 */}
        <footer className="bg-[#050507] py-12 border-t border-gray-900 mt-auto">
          <div className="max-w-6xl mx-auto px-6 text-center">
            <p className="text-[#C9A84C] font-bold text-2xl mb-4 font-serif tracking-widest">WOORIWIN</p>
            <p className="text-[#C9A84C] font-bold text-sm mb-4">관련 에볼루션카지노 가이드</p>
            <div className="flex flex-wrap justify-center gap-4 mb-4 text-sm">
              {relatedLinks.map((l) => (
                <Link key={l.href} href={l.href} className="text-gray-400 hover:text-yellow-400 transition">{l.label}</Link>
              ))}
            </div>
            <p className="text-[10px] md:text-[11px] text-gray-600 max-w-3xl mx-auto leading-relaxed mb-1">
              WOORIWIN은 정보 제공 가이드 사이트이며, 직접 게임 서비스를 제공하지 않습니다.
            </p>
            <p className="text-[10px] md:text-[11px] text-gray-600 max-w-3xl mx-auto leading-relaxed mb-4">
              모든 배팅의 책임은 이용자 본인에게 있으며, 당사는 이용 결과에 대한 법적 책임을 지지 않습니다.
            </p>
            <div className="flex justify-center flex-wrap gap-x-6 gap-y-3 text-[10px] md:text-[11px] text-gray-500 mb-8">
              {policyLinks.map(({ href, label }) => (
                <Link key={href} href={`/${href}`} className="hover:text-yellow-500 transition-colors">
                  {label}
                </Link>
              ))}
            </div>
            <p className="text-[9px] text-gray-800 uppercase tracking-[0.3em]">© 2026 WOORIWIN. ALL RIGHTS RESERVED.</p>
          </div>
        </footer>
      </body>
    </html>
  );
}