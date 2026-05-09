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

export const metadata: Metadata = {
  title: {
    default: "에볼루션카지노 완벽 가이드 2026 | WOORIWIN",
    template: "%s | WOORIWIN",
  },
  description:
    "에볼루션카지노 바카라·블랙잭·룰렛·슬롯 완벽 가이드. 규칙·전략·RTP 완전 정리. 세계 1위 라이브카지노 에볼루션의 모든 것.",
  keywords: [
    "에볼루션카지노",
    "에볼루션카지노 바카라",
    "에볼루션카지노 블랙잭",
    "에볼루션카지노 룰렛",
    "에볼루션 라이브카지노",
    "에볼루션카지노 전략",
  ],
  metadataBase: new URL("https://wooriwin.com"),
  alternates: {
    canonical: "https://wooriwin.com",
  },
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
    type: "website",
    locale: "ko_KR",
    url: "https://wooriwin.com",
    siteName: "WOORIWIN",
    title: "에볼루션카지노 완벽 가이드 2026 | WOORIWIN",
    description:
      "에볼루션카지노 바카라·블랙잭·룰렛·슬롯 완벽 가이드. 규칙·전략·RTP 완전 정리.",
    images: [
      {
        url: "https://wooriwin.com/images/og-main.jpg",
        width: 1200,
        height: 630,
        alt: "에볼루션카지노 완벽 가이드 WOORIWIN",
      },
    ],
  },
  twitter: {
    card: "summary_large_image",
    title: "에볼루션카지노 완벽 가이드 2026 | WOORIWIN",
    description:
      "에볼루션카지노 바카라·블랙잭·룰렛·슬롯 완벽 가이드.",
    images: ["https://wooriwin.com/images/og-main.jpg"],
  },
  verification: {
    google: "google-site-verification=nIE-kYgpwmgTKiQssndHTqWzLBBLBCECkbSVmSOR_Uk",
  },
};

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
