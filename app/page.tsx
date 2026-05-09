export default function Home() {
  const menuItems = [
    { name: '바카라', href: '/baccarat' },
    { name: '블랙잭', href: '/blackjack' },
    { name: '룰렛', href: '/roulette' },
    { name: '슬롯', href: '/slots' },
    { name: '라이브카지노', href: '/live-casino' },
    { name: '블로그', href: '/blog' },
  ]

  return (
    <main className="min-h-screen bg-gray-900 text-white">
      <section className="flex flex-col items-center justify-center min-h-screen text-center px-4">
        <h1 className="text-5xl font-bold mb-6">에볼루션카지노 완벽 가이드</h1>
        <p className="text-xl text-gray-300 mb-8 max-w-2xl">
          바카라, 블랙잭, 룰렛 전략부터 가입방법까지. wooriwin에서 확인하세요.
        </p>
        <div className="grid grid-cols-2 md:grid-cols-3 gap-4 mt-8">
          {menuItems.map((item) => (
            <a key={item.href} href={item.href} className="bg-gray-800 hover:bg-gray-700 rounded-lg p-6 text-center transition">
              <span className="text-lg font-semibold">{item.name}</span>
            </a>
          ))}
        </div>
      </section>
    </main>
  )
}