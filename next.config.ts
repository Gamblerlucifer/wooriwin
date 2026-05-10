import type { NextConfig } from "next";

const nextConfig: NextConfig = {
  images: {
    // [추가] WebP/AVIF 자동 변환 → slots.jpg 등 55KiB 절감
    formats: ["image/avif", "image/webp"],
    remotePatterns: [
      {
        protocol: "https",
        hostname: "images.pexels.com",
        pathname: "/**",
      },
    ],
  },

  async headers() {
    return [
      {
        source: "/(.*)",
        headers: [
          // HSTS
          {
            key: "Strict-Transport-Security",
            value: "max-age=63072000; includeSubDomains; preload",
          },
          // Clickjacking 방지
          {
            key: "X-Frame-Options",
            value: "SAMEORIGIN",
          },
          // COOP
          {
            key: "Cross-Origin-Opener-Policy",
            value: "same-origin",
          },
          // XSS 방지
          {
            key: "X-Content-Type-Options",
            value: "nosniff",
          },
        ],
      },
    ];
  },

  async redirects() {
    return [
      // ── 에볼루션카지노.site → wooriwin.com 301 리다이렉트 ──
      {
        source: "/:path*",
        has: [{ type: "host", value: "xn--o80b14lqrduwfmtg5wg16i.site" }],
        destination: "https://wooriwin.com/:path*",
        permanent: true,
      },

      // ── 기존 WordPress 한글 URL → 새 URL ──
      { source: "/%ec%97%90%eb%b3%bc%eb%a3%a8%ec%85%98-%ec%b9%b4%ec%a7%80%eb%85%b8-%eb%b0%94%ec%b9%b4%eb%9d%bc", destination: "/baccarat", permanent: true },
      { source: "/%eb%b0%94%ec%b9%b4%eb%9d%bc-%ec%a0%84%eb%9e%b5-%ec%99%84%eb%b2%bd-%eb%b6%84%ec%84%9d", destination: "/baccarat", permanent: true },
      { source: "/%eb%b8%94%eb%9e%99%ec%9e%ad-%ec%a0%84%eb%9e%b5-%ec%99%84%eb%b2%bd-%eb%b6%84%ec%84%9d", destination: "/blackjack", permanent: true },
      { source: "/%eb%a3%b0%eb%a0%9b-%ec%a0%84%eb%9e%b5-%eb%a7%88%ec%8a%a4%ed%84%b0-%ea%b0%80%ec%9d%b4%eb%93%9c", destination: "/roulette", permanent: true },
      { source: "/%ec%8a%ac%eb%a1%af-%ec%a0%84%eb%9e%b5-%eb%a7%88%ec%8a%a4%ed%84%b0-%ea%b0%80%ec%9d%b4%eb%93%9c", destination: "/slots", permanent: true },
      { source: "/%ed%94%84%eb%9d%bc%ea%b7%b8%eb%a7%88%ed%8b%b1-%ec%8a%ac%eb%a1%af", destination: "/slots", permanent: true },
      { source: "/%eb%9d%bc%ec%b9%b4%ec%a7%80%eb%85%b8", destination: "/", permanent: true },
      { source: "/%ec%98%a8%eb%9d%bc%ec%9d%b8%ec%b9%b4%ec%a7%80%eb%85%b8-%eb%b8%94%eb%a1%9c%ea%b7%b8", destination: "/blog", permanent: true },
      { source: "/sorry", destination: "/", permanent: true },
    ];
  },
};

export default nextConfig;
