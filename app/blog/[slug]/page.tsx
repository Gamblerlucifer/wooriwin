import type { Metadata } from 'next'
import Image from 'next/image'
import Link from 'next/link'
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

function getImageUrl(image: string) {
  if (!image) return 'https://wooriwin.com/og-default.jpg'
  return image.startsWith('http') ? image : `https://wooriwin.com${image}`
}

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

  if (!post) {
    return (
      <main className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-3xl font-bold mb-4">Post not found</h1>
          <Link href="/blog" className="text-yellow-400 hover:text-yellow-300">
            블로그로 이동
          </Link>
        </div>
      </main>
    )
  }

  const finalImageUrl = getImageUrl(post.image)

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Article',
        headline: post.title,
        description: post.description,
        url: `https://wooriwin.com/blog/${slug}`,
        inLanguage: 'ko-KR',
        datePublished: `${post.date}T09:00:00+09:00`,
        dateModified: `${post.date}T09:00:00+09:00`,
        image: finalImageUrl,
        author: { '@type': 'Organization', name: 'WOORIWIN', url: 'https://wooriwin.com' },
        publisher: {
          '@type': 'Organization',
          name: 'WOORIWIN',
          url: 'https://wooriwin.com',
          logo: { '@type': 'ImageObject', url: 'https://wooriwin.com/logo.png' },
        },
      },
      {
        '@type': 'FAQPage',
        mainEntity: (post.faq || []).map((f: { q: string; a: string }) => ({
          '@type': 'Question',
          name: f.q,
          acceptedAnswer: { '@type': 'Answer', text: f.a },
        })),
      },
    ],
  }

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <main className="min-h-screen bg-gray-900 text-white">

        {/* Hero */}
        <section className="relative h-64 md:h-80 overflow-hidden">
          <Image src={finalImageUrl} alt={post.imageAlt || post.title} fill className="object-cover opacity-40" priority />
          <div className="absolute inset-0 bg-gradient-to-t from-gray-900 to-transparent" />
          <div className="absolute bottom-0 left-0 right-0 max-w-4xl mx-auto px-4 pb-8">
            <nav className="text-sm text-gray-400 mb-3">
              <Link href="/" className="hover:text-yellow-400">홈</Link> &rsaquo;{' '}
              <Link href="/blog" className="hover:text-yellow-400">블로그</Link> &rsaquo;{' '}
              <span className="text-white">{post.category}</span>
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
                  {post.faq.map((f: { q: string; a: string }, i: number) => (
                    <details key={i} className="bg-gray-800 rounded-xl p-5 group cursor-pointer">
                      <summary className="font-semibold text-white flex justify-between items-center list-none">
                        {f.q}
                        <span className="text-yellow-400 text-xl transition-transform group-open:rotate-45">+</span>
                      </summary>
                      <p className="mt-4 text-gray-400 text-sm leading-relaxed">{f.a}</p>
                    </details>
                  ))}
                </div>
              </section>
            )}
          </article>

          {/* Sidebar */}
          <aside className="w-full lg:w-64 shrink-0 mt-12 lg:mt-0">
            <div className="sticky top-8 space-y-6">
              {(post.relatedPosts || []).length > 0 && (
                <div className="bg-gray-800 rounded-xl p-5 border border-gray-700">
                  <h3 className="text-yellow-400 font-bold mb-4">관련 포스트</h3>
                  <ul className="space-y-3">
                    {post.relatedPosts.map((r: { slug: string; title: string }) => (
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

        {/* Footer */}
        <footer className="bg-gray-950 py-10 px-4 text-center">
          <div className="flex flex-wrap justify-center gap-4 text-sm mb-4">
            <Link href="/" className="text-gray-400 hover:text-yellow-400 transition">에볼루션카지노 메인</Link>
            <Link href="/blog" className="text-gray-400 hover:text-yellow-400 transition">블로그 전체보기</Link>
            <Link href="/baccarat" className="text-gray-400 hover:text-yellow-400 transition">바카라 가이드</Link>
            <Link href="/blackjack" className="text-gray-400 hover:text-yellow-400 transition">블랙잭 가이드</Link>
            <Link href="/roulette" className="text-gray-400 hover:text-yellow-400 transition">룰렛 가이드</Link>
          </div>
          <p className="text-gray-600 text-xs">© 2026 WOORIWIN. All rights reserved.</p>
        </footer>
      </main>
    </>
  )
}