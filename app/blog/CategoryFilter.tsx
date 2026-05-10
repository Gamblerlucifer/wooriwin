'use client'

import { useState } from 'react'
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
}

export default function CategoryFilter({ posts, categories }: CategoryFilterProps) {
  const [active, setActive] = useState('전체')

  const filtered = active === '전체' ? posts : posts.filter((p) => p.category === active)

  return (
    <>
      {/* 카테고리 탭 */}
      <section className="max-w-5xl mx-auto px-4 py-8">
        <div className="flex flex-wrap gap-2 justify-center">
          {categories.map((cat) => (
            <button
              key={cat}
              onClick={() => setActive(cat)}
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
        {filtered.length === 0 ? (
          <div className="text-center py-20">
            <p className="text-gray-400">
              {active === '전체'
                ? '포스트가 없습니다. 자동화 스크립트를 실행하세요.'
                : `'${active}' 카테고리에 아직 포스트가 없습니다.`}
            </p>
          </div>
        ) : (
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {filtered.map((post) => (
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
        )}
      </section>
    </>
  )
}
