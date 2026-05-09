import type { Metadata } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

// ✅ layout 역할: 공통 뼈대만
// - title template (suffix 자동 부착)
// - metadataBase (절대경로 기준점)
// - robots (전체 동일)
// - GSC verification
// ❌ canonical, OG, twitter, keywords, description → 각 page.tsx에서 개별 설정
export const metadata: Metadata = {
  // title은 각 페이지에서 설정하여 로딩
  // title: {
  //  default: "에볼루션카지노 완벽 가이드 2026 | WOORIWIN",
  //  template: "%s | WOORIWIN",
  //},
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
    siteName: "WOORIWIN",
    locale: "ko_KR",
    type: "website",
  },
  verification: {
    google: "nIE-kYgpwmgTKiQssndHTqWzLBBLBCECkbSVmSOR_Uk",
  },
};
// ✅ WebSite 스키마만 여기 선언 (사이트 전체 공통, 한 번만)
// FAQPage → 메인 page.tsx
// Article + FAQPage → blog/[slug]/page.tsx
const jsonLd = {
  "@context": "https://schema.org",
  "@type": "WebSite",
  name: "WOORIWIN",
  url: "https://wooriwin.com",
  description: "에볼루션카지노 바카라·블랙잭·룰렛·슬롯 완벽 가이드",
  inLanguage: "ko-KR",
  publisher: {
    "@type": "Organization",
    name: "WOORIWIN",
    url: "https://wooriwin.com",
    logo: {
      "@type": "ImageObject",
      url: "https://wooriwin.com/favicon.ico",
    },
  },
  potentialAction: {
    "@type": "SearchAction",
    target: "https://wooriwin.com/blog?q={search_term_string}",
    "query-input": "required name=search_term_string",
  },
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="ko"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <head>
        <script
          type="application/ld+json"
          dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }}
        />
      </head>
      <body className="min-h-full flex flex-col">{children}</body>
    </html>
  );
}
