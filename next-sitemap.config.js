module.exports = {
  siteUrl: 'https://wooriwin.com',
  generateRobotsTxt: false, // robots.txt는 public/robots.txt로 직접 관리
  changefreq: 'daily',
  priority: 0.7,

  // 자동 감지에서 제외할 경로 없음
  exclude: [],

  additionalPaths: async (config) => {
    const fs   = require('fs');
    const path = require('path');
    const results = [];

    // ── 1. 정적 페이지 ──────────────────────────────
    const staticPages = [
      { loc: '/about',              priority: 0.6, changefreq: 'monthly' },
      { loc: '/privacy-policy',     priority: 0.5, changefreq: 'monthly' },
      { loc: '/terms',              priority: 0.5, changefreq: 'monthly' },
      { loc: '/disclaimer',         priority: 0.5, changefreq: 'monthly' },
      { loc: '/responsible-gaming', priority: 0.6, changefreq: 'monthly' },
    ];
    for (const page of staticPages) {
      results.push({
        loc:        page.loc,
        changefreq: page.changefreq,
        priority:   page.priority,
        lastmod:    new Date().toISOString(),
      });
    }

    // ── 2. 블로그 포스트 (동적) ──────────────────────
    const postsDir = path.join(process.cwd(), 'data', 'posts');
    if (fs.existsSync(postsDir)) {
      const files = fs.readdirSync(postsDir).filter(f => f.endsWith('.json'));
      for (const file of files) {
        try {
          const raw  = fs.readFileSync(path.join(postsDir, file), 'utf-8');
          const post = JSON.parse(raw);
          results.push({
            loc:        `/blog/${file.replace('.json', '')}`,
            changefreq: 'weekly',
            priority:   0.8,
            lastmod:    post.date
              ? new Date(post.date).toISOString()
              : new Date().toISOString(),
          });
        } catch {
          // 파싱 실패 시 스킵
        }
      }
    }

    return results;
  },
}
