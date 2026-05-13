'use client'

import { useState, useEffect } from 'react'
import { useSearchParams, useRouter } from 'next/navigation'
import Image from 'next/image'
import Link from 'next/link'

interface Post {
  slug: string
  title: string
  description: string
  category: string
  date: string
  readTime: string
  image: string
  imageAlt?: string
}

interface CategoryFilterProps {
  posts: Post[]
  categories: string[]
  categorySlugMap: Record<string, string>
  slugCategoryMap: Record<string, string>
}

const POSTS_PER_PAGE = 21

export default function CategoryFilter({ posts, categories, categorySlugMap, slugCategoryMap }: CategoryFilterProps) {
  const searchParams = useSearchParams()
  const router = useRouter()
  const [active, setActive] = useState('전체')
  const [page, setPage] = useState(1)

  useEffect(() => {
    const slug = searchParams.get('category')
    if (slug) {
      const cat = slugCategoryMap[slug]
      if (cat && categories.includes(cat)) {
        setActive(cat)
      }
    } else {
      setActive('전체')
    }
    setPage(1)
  }, [searchParams, categories, slugCategoryMap])

  const handleSelect = (cat: string) => {
    setActive(cat)
    setPage(1)
    if (cat === '전체') {
      router.replace('/blog', { scroll: false })
    } else {
      const slug = categorySlugMap[cat] || encodeURIComponent(cat)
      router.replace(`/blog?category=${slug}`, { scroll: false })
    }
  }

  const filtered = active === '전체' ? posts : posts.filter((p) => p.category === active)
  const totalPages = Math.ceil(filtered.length / POSTS_PER_PAGE)
  const paginated = filtered.slice((page - 1) * POSTS_PER_PAGE, page * POSTS_PER_PAGE)

  return (
    <>
      {/* 카테고리 탭 */}
      <section className="max-w-5xl mx-auto px-4 py-8">
        <div className="flex flex-wrap gap-2 justify-center">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => handleSelect(cat)}
              className={`px-4 py-2 rounded-full text-sm font-semibold transition ${
                active === cat
                  ? 'bg-yellow-400 text-gray-900'
                  : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white'
              }`}
            >
              {cat}
            </button>
          ))}
        </div>
      </section>

      {/* 포스트 그리드 */}
      <section className="max-w-5xl mx-auto px-4 pb-16">
        {paginated.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-gray-400">
              {active === '전체'
                ? '포스트가 없습니다. 자동화 스크립트를 실행하세요.'
                : `'${active}' 카테고리에 아직 포스트가 없습니다.`}
            </p>
          </div>
        ) : (
          <>
            <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
              {paginated.map((post) => (
                <Link
                  key={post.slug}
                  href={`/blog/${post.slug}`}
                  className="group bg-gray-800 rounded-xl overflow-hidden hover:bg-gray-700 transition-all hover:shadow-xl hover:shadow-yellow-400/10"
                >
                  <div className="relative h-48 bg-gray-700">
                    <Image
                      src={post.image}
                      alt={post.imageAlt || post.title}
                      fill
                      className="object-cover group-hover:opacity-90 transition"
                    />
                  </div>
                  <div className="p-5">
                    <div className="flex items-center justify-between mb-3">
                      <span className="text-xs font-semibold text-yellow-400 bg-yellow-400/10 px-2 py-1 rounded">
                        {post.category}
                      </span>
                      <span className="text-xs text-gray-500">{post.readTime} 읽기</span>
                    </div>
                    <p className="text-base font-bold text-white mb-3 leading-snug group-hover:text-yellow-400 transition line-clamp-2">
                      {post.title}
                    </p>
                    <p className="text-gray-400 text-sm leading-relaxed line-clamp-3 mb-4">
                      {post.description}
                    </p>
                    <div className="flex items-center justify-between">
                      <span className="text-xs text-gray-500">{post.date}</span>
                      <span className="text-xs text-yellow-400 font-semibold group-hover:underline">
                        자세히 보기 →
                      </span>
                    </div>
                  </div>
                </Link>
              ))}
            </div>

            {/* 페이지네이션 */}
            {totalPages > 1 && (
              <div className="flex justify-center items-center gap-2 mt-12">
                <button
                  onClick={() => { setPage(p => Math.max(1, p - 1)); window.scrollTo({ top: 0, behavior: 'smooth' }) }}
                  disabled={page === 1}
                  className="px-4 py-2 rounded-full text-sm font-semibold transition bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed"
                >
                  ← 이전
                </button>
                {Array.from({ length: totalPages }, (_, i) => i + 1).map((p) => (
                  <button
                    key={p}
                    onClick={() => { setPage(p); window.scrollTo({ top: 0, behavior: 'smooth' }) }}
                    className={`w-9 h-9 rounded-full text-sm font-semibold transition ${
                      page === p
                        ? 'bg-yellow-400 text-gray-900'
                        : 'bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white'
                    }`}
                  >
                    {p}
                  </button>
                ))}
                <button
                  onClick={() => { setPage(p => Math.min(totalPages, p + 1)); window.scrollTo({ top: 0, behavior: 'smooth' }) }}
                  disabled={page === totalPages}
                  className="px-4 py-2 rounded-full text-sm font-semibold transition bg-gray-800 text-gray-400 hover:bg-gray-700 hover:text-white disabled:opacity-30 disabled:cursor-not-allowed"
                >
                  다음 →
                </button>
              </div>
            )}
          </>
        )}
      </section>
    </>
  )
}
