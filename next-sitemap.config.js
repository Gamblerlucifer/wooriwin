const fs = require('fs')
const path = require('path')

module.exports = {
  siteUrl: 'https://wooriwin.com',
  generateRobotsTxt: false,
  generateIndexSitemap: false,
  changefreq: 'daily',
  priority: 0.7,
  sitemapSize: 5000,
  exclude: ['/server-sitemap.xml'],

  transform: async (config, url) => {
    if (/\/(disclaimer|privacy-policy|terms|about|responsible-gaming)$/.test(url)) {
      return {
        loc: url,
        changefreq: 'monthly',
        priority: 0.5,
        lastmod: new Date().toISOString(),
      }
    }
    if (url.includes('/blog/')) {
      return {
        loc: url,
        changefreq: 'weekly',
        priority: 0.8,
        lastmod: new Date().toISOString(),
      }
    }
    return {
      loc: url,
      changefreq: config.changefreq,
      priority: config.priority,
      lastmod: new Date().toISOString(),
    }
  },

  additionalPaths: async (config) => {
    const results = []
    const postsDir = path.join(process.cwd(), 'data', 'posts')

    if (fs.existsSync(postsDir)) {
      const files = fs.readdirSync(postsDir).filter(f => f.endsWith('.json'))
      console.log(`[sitemap] Found ${files.length} blog posts`)
      for (const file of files) {
        const slug = file.replace('.json', '')
        try {
          const raw = fs.readFileSync(path.join(postsDir, file), 'utf-8')
          const post = JSON.parse(raw)
          results.push({
            loc: `/blog/${slug}`,
            changefreq: 'weekly',
            priority: 0.8,
            lastmod: post.date
              ? new Date(post.date).toISOString()
              : new Date().toISOString(),
          })
        } catch (e) {
          console.error(`[sitemap] Failed to parse ${file}:`, e.message)
        }
      }
    } else {
      console.log(`[sitemap] WARNING: posts dir not found at ${postsDir}`)
    }

    return results
  },
}
