import Link from 'next/link'
import type { Metadata } from 'next'

export const metadata: Metadata = {
  title: '페이지를 찾을 수 없습니다 | WOORIWIN',
  description: '요청하신 페이지를 찾을 수 없습니다.',
}

export default function NotFound() {
  return (
    <main className="min-h-screen flex flex-col items-center justify-center text-white px-6 text-center" style={{ background: '#0A0A0F' }}>
      <p className="text-7xl font-bold mb-4" style={{ color: '#C9A84C', fontFamily: 'Georgia, serif' }}>404</p>
      <h1 className="text-2xl font-bold mb-4">페이지를 찾을 수 없습니다</h1>
      <p className="text-gray-400 mb-10 max-w-md">
        요청하신 페이지가 삭제되었거나 주소가 변경되었습니다.
      </p>
      <div className="flex flex-col sm:flex-row gap-4">
        <Link
          href="/"
          className="px-8 py-3 rounded font-semibold transition"
          style={{ background: '#C9A84C', color: '#0A0A0F' }}
        >
          홈으로 돌아가기
        </Link>
        <Link
          href="/blog"
          className="px-8 py-3 rounded font-semibold transition"
          style={{ border: '1px solid rgba(201,168,76,0.4)', color: '#C9A84C' }}
        >
          블로그 보기
        </Link>
      </div>
    </main>
  )
}
