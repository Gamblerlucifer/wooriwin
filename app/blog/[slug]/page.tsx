import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'
import { notFound } from 'next/navigation'
import { readFileSync, readdirSync, existsSync } from 'fs'
import { join } from 'path'
import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'

const POSTS_DIR = join(process.cwd(), 'data', 'posts')

function getPost(slug: string) {
  const filepath = join(POSTS_DIR, `${slug}.json`)
  if (!existsSync(filepath)) return null
  return JSON.parse(readFileSync(filepath, 'utf-8'))
}

function getAllSlugs(): string[] {
  if (!existsSync(POSTS_DIR)) return []
  return readdirSync(POSTS_DIR)
    .filter((f) => f.endsWith('.json'))
    .map((f) => f.replace('.json', ''))
}

function getRelatedPosts(currentSlug: string, currentCategory: string, count = 3) {
  const slugs = getAllSlugs().filter((s) => s !== currentSlug)
  const posts = slugs.map((s) => {
    const p = getPost(s)
    return { slug: s, title: p?.title || '', date: p?.date || '', category: p?.category || '' }
  })
  // 동일 카테고리 우선, 그 다음 날짜순
  const sameCategory = posts.filter((p) => p.category === currentCategory)
    .sort((a, b) => b.date.localeCompare(a.date))
  const others = posts.filter((p) => p.category !== currentCategory)
    .sort((a, b) => b.date.localeCompare(a.date))
  return [...sameCategory, ...others].slice(0, count)
}

function getImageUrl(image: string) {
  if (!image) return 'https://wooriwin.com/images/og-main.jpg'
  return image.startsWith('http') ? image : `https://wooriwin.com${image}`
}

// ✅ ISR: 1시간마다 자동 재생성 (새 포스트 추가/수정 시 재배포 없이 반영)
export const revalidate = 3600

export async function generateMetadata({
  params,
}: {
  params: Promise<{ slug: string }>
}): Promise<Metadata> {
  const { slug } = await params
  const post = getPost(slug)
  if (!post) return {}
  const finalImageUrl = getImageUrl(post.image)
  return {
    title: `${post.title} | WOORIWIN`,
    description: post.description,
    keywords: post.keywords,
    alternates: { canonical: `https://wooriwin.com/blog/${slug}` },
    // ✅ robots 제거 → layout에서 전체 공통 처리
    openGraph: {
      title: post.title,
      description: post.description,
      url: `https://wooriwin.com/blog/${slug}`,
      // ✅ siteName, locale 제거 → layout 상속
      type: 'article',
      images: [{ url: finalImageUrl, width: 1200, height: 630 }],
    },
    twitter: {
      card: 'summary_large_image',
      title: post.title,
      description: post.description,
      images: [finalImageUrl],
    },
  }
}

export async function generateStaticParams() {
  return getAllSlugs().map((slug) => ({ slug }))
}

export default async function BlogPost({
  params,
}: {
  params: Promise<{ slug: string }>
}) {
  const { slug } = await params
  const post = getPost(slug)

  if (!post) notFound()

  const finalImageUrl = getImageUrl(post.image)
  const relatedPosts = getRelatedPosts(slug, post.category)

  const jsonLdArticle = {
    '@context': 'https://schema.org',
    '@type': 'Article',
    headline: post.title,
    description: post.description,
    url: `https://wooriwin.com/blog/${slug}`,
    inLanguage: 'ko-KR',
    datePublished: `${post.date}T09:00:00+09:00`,
    dateModified: `${post.updatedAt || post.date}T09:00:00+09:00`,
    image: finalImageUrl,
    author: {
      '@type': post.author?.name ? 'Person' : 'Organization',
      name: post.author?.name || 'WOORIWIN 편집팀',
      url: post.author?.url ? `https://wooriwin.com${post.author.url}` : 'https://wooriwin.com/about',
    },
    publisher: {
      '@type': 'Organization',
      name: 'WOORIWIN',
      url: 'https://wooriwin.com',
      logo: { '@type': 'ImageObject', url: 'https://wooriwin.com/images/logo.png' },
    },
  }

  const jsonLdFaq = {
    '@context': 'https://schema.org',
    '@type': 'FAQPage',
    mainEntity: (post.faq || []).map((f: { q: string; a: string }) => ({
      '@type': 'Question',
      name: f.q,
      acceptedAnswer: { '@type': 'Answer', text: f.a },
    })),
  }

  const jsonLdBreadcrumb = {
    '@context': 'https://schema.org',
    '@type': 'BreadcrumbList',
    itemListElement: [
      { '@type': 'ListItem', position: 1, name: '홈', item: 'https://wooriwin.com' },
      { '@type': 'ListItem', position: 2, name: '블로그', item: 'https://wooriwin.com/blog' },
      { '@type': 'ListItem', position: 3, name: post.title, item: `https://wooriwin.com/blog/${slug}` },
    ],
  }

  return (
    <>
      {/* ① SEO: Article·FAQPage·BreadcrumbList 스키마 분리 */}
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdArticle) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdFaq) }} />
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLdBreadcrumb) }} />
      <main className="min-h-screen bg-gray-900 text-white">

        {/* Hero */}
        <section className="relative h-64 md:h-80 overflow-hidden">
          <Image src={finalImageUrl} alt={post.imageAlt || post.title} fill className="object-cover opacity-40" priority />
          <div className="absolute inset-0 bg-gradient-to-t from-gray-900 to-transparent" />
          <div className="absolute bottom-0 left-0 right-0 max-w-4xl mx-auto px-4 pb-8">
            <nav aria-label="breadcrumb" className="text-sm text-gray-400 mb-3">
              <Link href="/" className="hover:text-yellow-400">홈</Link> &rsaquo;{' '}
              <Link href="/blog" className="hover:text-yellow-400">블로그</Link> &rsaquo;{' '}
              <span className="text-white" aria-current="page">{post.category}</span>
            </nav>
            <div className="flex items-center gap-3 mb-3">
              <span className="text-xs font-semibold text-yellow-400 bg-yellow-400/10 px-2 py-1 rounded">{post.category}</span>
              <span className="text-xs text-gray-400">{post.readTime} 읽기</span>
              <span className="text-xs text-gray-400">{post.date}</span>
            </div>
            <h1 className="text-2xl md:text-4xl font-bold leading-tight">{post.title}</h1>
          </div>
        </section>

        {/* Description */}
        <section className="bg-gray-800 border-b border-gray-700 px-4 py-5">
          <p className="max-w-4xl mx-auto text-gray-400 text-lg leading-relaxed">{post.description}</p>
        </section>

        {/* Content */}
        <div className="max-w-6xl mx-auto px-4 py-12 flex gap-10">
          <article className="flex-1 min-w-0">
            {/* ① SEO: 정보 최신성 고지 */}
            <p className="text-xs text-gray-500 mb-8 text-right">
              본 정보는 2026년 5월 기준이며, 실제 게임 수치는 운영사 정책에 따라 변동될 수 있습니다.
            </p>

            <div className="text-gray-300 space-y-5 leading-relaxed text-base md:text-lg">
              <ReactMarkdown
                remarkPlugins={[remarkGfm]}
                components={{
                  // ✅ node prop 제거: 구조분해로 node를 분리하고 나머지만 DOM에 전달
                  table: ({ node, ...props }) => (
                    <div className="overflow-x-auto my-6">
                      <table className="w-full border-collapse text-sm" {...props} />
                    </div>
                  ),
                  thead: ({ node, ...props }) => <thead className="bg-gray-700" {...props} />,
                  th: ({ node, ...props }) => (
                    <th className="border border-gray-600 px-4 py-2 text-yellow-400 text-left" {...props} />
                  ),
                  td: ({ node, ...props }) => (
                    <td className="border border-gray-600 px-4 py-2 text-gray-300" {...props} />
                  ),
                  tr: ({ node, ...props }) => <tr className="even:bg-gray-800" {...props} />,
                  img: ({ node, alt, ...props }) => (
                    // eslint-disable-next-line @next/next/no-img-element
                    <img
                      alt={alt || ''}
                      loading="lazy"
                      className="w-full h-auto rounded-2xl my-8 border border-gray-800"
                      {...props}
                    />
                  ),
                }}
              >
                {post.content}
              </ReactMarkdown>
            </div>

            {/* FAQ */}
            {(post.faq || []).length > 0 && (
              <section className="mt-16">
                <h2 className="text-2xl font-bold mb-6 text-yellow-400">자주 묻는 질문</h2>
                <div className="space-y-4">
                  {post.faq.map((f: { q: string; a: string }) => (
                    <details key={f.q} className="bg-gray-800 rounded-xl p-5 group cursor-pointer">
                      <summary className="font-semibold text-white flex justify-between items-center list-none">
                        {f.q}
                        <span className="text-yellow-400 text-xl transition-transform group-open:rotate-45" aria-hidden="true">+</span>
                      </summary>
                      <p className="mt-4 text-gray-400 text-sm leading-relaxed">{f.a}</p>
                    </details>
                  ))}
                </div>
              </section>
            )}

            {/* ✅ 저자 프로필 (E-E-A-T: 작성 주체 신뢰 신호) */}
            <div className="mt-16 pt-8 border-t border-gray-700">
              <div className="flex items-center gap-4 bg-gray-800/50 rounded-xl p-5 border border-gray-700">
                <div className="w-12 h-12 rounded-full shrink-0 overflow-hidden"
                  style={{ border: '1px solid rgba(201,168,76,0.3)' }}>
                  {post.author?.image ? (
                    <img
                      src={post.author.image}
                      alt={post.author.name}
                      className="w-full h-full object-cover"
                    />
                  ) : (
                    <div className="w-full h-full flex items-center justify-center text-xl font-bold"
                      style={{ background: 'rgba(201,168,76,0.15)', color: '#C9A84C' }}>
                      {post.author?.name ? post.author.name[0].toUpperCase() : 'W'}
                    </div>
                  )}
                </div>
                <div className="flex-1 min-w-0">
                  <p className="text-xs text-gray-500 mb-0.5">작성자</p>
                  <div className="flex items-center gap-2 flex-wrap">
                    <p className="font-bold text-white text-sm">{post.author?.name}</p>
                    {post.author?.role && <span className="text-xs text-gray-400">· {post.author.role}</span>}
                    {post.author?.experience && <span className="text-xs text-gray-500">· 경력 {post.author.experience}</span>}
                  </div>
                  {post.author?.specialty?.length > 0 && (
                    <div className="flex flex-wrap items-center gap-1 mt-1.5">
                      <span className="text-xs text-gray-500 shrink-0">전문분야 :</span>
                      {post.author.specialty.map((s: string) => (
                        <span key={s} className="text-xs px-2 py-0.5 rounded-full"
                          style={{ background: 'rgba(201,168,76,0.1)', color: '#C9A84C', border: '1px solid rgba(201,168,76,0.2)' }}>
                          {s}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
                <Link
                  href="/about"
                  className="shrink-0 text-xs px-3 py-1.5 rounded-lg transition hover:text-yellow-300"
                  style={{ border: '1px solid rgba(201,168,76,0.3)', color: '#C9A84C' }}
                >
                  소개 보기
                </Link>
              </div>
            </div>

          </article>

          {/* Sidebar */}
          <aside className="w-full lg:w-64 shrink-0 mt-12 lg:mt-0">
            <div className="sticky top-8 space-y-6">
              {relatedPosts.length > 0 && (
                <div className="bg-gray-800 rounded-xl p-5 border border-gray-700">
                  <h3 className="text-yellow-400 font-bold mb-4">관련 포스트</h3>
                  <ul className="space-y-3">
                    {relatedPosts.map((r: { slug: string; title: string }) => (
                      <li key={r.slug}>
                        <Link href={`/blog/${r.slug}`} className="text-gray-400 text-sm hover:text-yellow-400 transition leading-snug block">
                          → {r.title}
                        </Link>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
              <div className="bg-gray-800 rounded-xl p-5 border border-gray-700">
                <h3 className="text-yellow-400 font-bold mb-4">게임 가이드</h3>
                <ul className="space-y-2 text-sm">
                  {[
                    { href: '/baccarat', label: '에볼루션카지노 바카라' },
                    { href: '/blackjack', label: '에볼루션카지노 블랙잭' },
                    { href: '/roulette', label: '에볼루션카지노 룰렛' },
                    { href: '/slots', label: '에볼루션카지노 슬롯' },
                    { href: '/live-casino', label: '에볼루션 라이브카지노' },
                  ].map((l) => (
                    <li key={l.href}>
                      <Link href={l.href} className="text-gray-400 hover:text-yellow-400 transition block">→ {l.label}</Link>
                    </li>
                  ))}
                </ul>
              </div>
            </div>
          </aside>
        </div>
      </main>
    </>
  )
}
