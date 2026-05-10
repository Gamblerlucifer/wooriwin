module.exports = {
  siteUrl: 'https://wooriwin.com',
  generateRobotsTxt: true,
  changefreq: 'daily',
  priority: 0.7,
  additionalPaths: async (config) => {
    const fs = require('fs');
    const path = require('path');
    const postsDir = path.join(process.cwd(), 'data/posts');
    const files = fs.readdirSync(postsDir);
    return files.map((file) => ({
      loc: `/blog/${file.replace('.json', '')}`,
      changefreq: 'daily',
      priority: 0.8,
    }));
  },
}