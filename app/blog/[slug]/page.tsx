import type { Metadata } from 'next'
import Link from 'next/link'

// 포스트 데이터 (나중에 자동화 스크립트로 교체)
const posts: Record<string, {
  title: string
  description: string
  category: string
  date: string
  readTime: string
  keywords: string[]
  content: string
  faq: { q: string; a: string }[]
  relatedPosts: { slug: string; title: string }[]
}> = {
  'evolution-baccarat-strategy-2026': {
    title: '에볼루션카지노 바카라 전략 총정리 2026 — 뱅커 vs 플레이어 최적 베팅법',
    description: '에볼루션 바카라에서 장기적으로 수익을 극대화하는 뱅커·플레이어 베팅 전략을 통계와 함께 분석합니다.',
    category: '바카라',
    date: '2026-05-09',
    readTime: '8분',
    keywords: ['에볼루션카지노 바카라 전략', '바카라 뱅커 베팅', '바카라 플레이어 베팅', '에볼루션 바카라 RTP'],
    content: `
에볼루션카지노 바카라는 카지노 게임 중 가장 낮은 하우스 엣지를 자랑하는 게임입니다. 뱅커 베팅의 하우스 엣지는 1.06%, 플레이어 베팅은 1.24%로 블랙잭 다음으로 플레이어에게 유리한 게임입니다.

## 뱅커 vs 플레이어 — 어느 쪽이 유리한가?

통계적으로 뱅커 베팅 승률은 45.86%, 플레이어 베팅은 44.62%입니다. 나머지 9.52%는 타이(무승부)입니다. 뱅커 베팅이 승률이 높지만 당첨 시 5% 커미션이 부과됩니다.

장기적으로 보면 뱅커 베팅이 유리합니다. 10,000라운드 기준으로 뱅커 베팅은 플레이어 베팅보다 약 180라운드 더 이깁니다.

## 마틴게일 전략 — 현실적인 분석

마틴게일 전략은 질 때마다 베팅을 두 배로 올리는 방식입니다. 이론적으로는 한 번 이기면 손실을 회복할 수 있지만, 연속 패배 시 베팅 한도 초과 위험이 있습니다.

예를 들어 시작 베팅 $10으로 연속 8패하면 $2,560을 베팅해야 합니다. 대부분의 테이블 최대 베팅 한도($10,000)를 고려하면 10연패 전후에 한계에 도달합니다.

## 파롤리 전략 — 안전한 대안

파롤리 전략은 이길 때마다 베팅을 두 배로 올리고 3연승 시 초기 베팅으로 돌아오는 방식입니다. 손실 리스크가 낮고 연승 시 큰 수익을 기대할 수 있습니다.

## 타이 베팅은 절대 피하세요

타이 베팅은 8:1 배당이지만 하우스 엣지가 14.36%로 매우 높습니다. 100번 베팅하면 평균 14.36번의 손실이 발생하는 구조입니다. 전문가들은 타이 베팅을 절대 권장하지 않습니다.

## 자금 관리가 핵심

바카라에서 가장 중요한 것은 자금 관리입니다. 세션 예산의 최대 5% 이상을 한 번에 베팅하지 않는 것이 원칙입니다. 손절 기준(예: 세션 예산의 50% 손실 시 중단)을 미리 정해두세요.
    `,
    faq: [
      { q: '에볼루션 바카라 뱅커와 플레이어 중 어느 쪽이 유리한가요?', a: '통계적으로 뱅커 베팅이 승률 45.86%로 플레이어(44.62%)보다 높습니다. 장기적으로는 뱅커 베팅의 하우스 엣지(1.06%)가 플레이어(1.24%)보다 낮아 유리합니다.' },
      { q: '바카라 마틴게일 전략은 효과가 있나요?', a: '단기적으로 작동할 수 있지만 장기적으로는 하우스 엣지를 극복할 수 없습니다. 연속 패배 시 베팅 한도 초과 위험이 있으므로 자금 관리를 철저히 해야 합니다.' },
      { q: '바카라 타이 베팅을 해야 하나요?', a: '타이 베팅은 하우스 엣지가 14.36%로 매우 높습니다. 전문가들은 타이 베팅을 피하고 뱅커 또는 플레이어 베팅에 집중하도록 권장합니다.' },
    ],
    relatedPosts: [
      { slug: 'baccarat-road-reading-guide', title: '바카라 빅로드·비드로드 읽는 법' },
      { slug: 'lightning-roulette-multiplier-guide', title: '라이트닝 룰렛 멀티플라이어 완벽 이해' },
      { slug: 'evolution-casino-signup-guide', title: '에볼루션카지노 가입방법 단계별 완벽 가이드' },
    ],
  },
  'lightning-roulette-multiplier-guide': {
    title: '라이트닝 룰렛 멀티플라이어 완벽 이해 — 500배 당첨 확률과 전략',
    description: '라이트닝 룰렛 멀티플라이어의 확률 구조를 분석하고 최적의 베팅 조합 전략을 제시합니다.',
    category: '룰렛',
    date: '2026-05-08',
    readTime: '6분',
    keywords: ['라이트닝 룰렛 전략', '라이트닝 룰렛 멀티플라이어', '에볼루션 룰렛', '라이트닝 룰렛 확률'],
    content: `
라이트닝 룰렛(Lightning Roulette)은 에볼루션의 가장 인기 있는 게임 중 하나입니다. 매 스핀마다 1~5개의 번호에 50x·100x·200x·300x·500x 멀티플라이어가 무작위로 적용되어 일반 룰렛보다 훨씬 큰 당첨금을 기대할 수 있습니다.

## 멀티플라이어 확률 구조

각 스핀마다 평균 3개의 번호에 멀티플라이어가 적용됩니다. 500x 멀티플라이어가 적용될 확률은 약 2~3%이며, 50x는 가장 자주 등장합니다.

멀티플라이어가 없는 번호의 스트레이트업 당첨은 29:1로 일반 룰렛(35:1)보다 낮습니다. 이 점을 반드시 감안해야 합니다.

## 최적 베팅 전략

라이트닝 룰렛에서는 스트레이트업(단일 번호) 베팅과 이너 베팅을 조합하는 전략이 효과적입니다. 이너 베팅으로 안정적인 수익을 유지하면서 스트레이트업으로 멀티플라이어 당첨을 노리는 방식입니다.

아우터 베팅(레드/블랙 등)만 하면 멀티플라이어 혜택을 전혀 받지 못하므로, 라이트닝 룰렛의 특성을 활용하려면 반드시 이너 베팅을 포함해야 합니다.

## RTP 분석

라이트닝 룰렛의 RTP는 97.30%로 일반 유럽식 룰렛과 동일합니다. 멀티플라이어는 당첨금 분포를 바꾸지만 전체 RTP는 유지됩니다. 고변동성을 원한다면 스트레이트업 비중을 높이고, 안정성을 원한다면 아우터 베팅 비중을 높이세요.
    `,
    faq: [
      { q: '라이트닝 룰렛 RTP는 얼마인가요?', a: '라이트닝 룰렛의 RTP는 97.30%로 일반 유럽식 룰렛과 동일합니다. 멀티플라이어는 당첨금 분포를 변경하지만 전체 환수율은 유지됩니다.' },
      { q: '라이트닝 룰렛에서 아우터 베팅만 해도 되나요?', a: '아우터 베팅(레드/블랙 등)만 하면 멀티플라이어 혜택을 받지 못합니다. 라이트닝 룰렛의 특성을 활용하려면 스트레이트업 등 이너 베팅을 포함하는 것이 좋습니다.' },
      { q: '500배 멀티플라이어 당첨 확률은?', a: '500x 멀티플라이어가 특정 번호에 적용될 확률은 스핀당 약 2~3%이며, 해당 번호에 스트레이트업 베팅이 맞을 확률까지 포함하면 매우 낮습니다.' },
    ],
    relatedPosts: [
      { slug: 'evolution-baccarat-strategy-2026', title: '에볼루션카지노 바카라 전략 총정리 2026' },
      { slug: 'blackjack-basic-strategy-chart', title: '에볼루션 블랙잭 기본 전략표 완벽 가이드' },
      { slug: 'evolution-casino-signup-guide', title: '에볼루션카지노 가입방법 단계별 완벽 가이드' },
    ],
  },
  'blackjack-basic-strategy-chart': {
    title: '에볼루션 블랙잭 기본 전략표 완벽 가이드 — RTP 99.28% 달성하는 법',
    description: '블랙잭 기본 전략표를 완벽히 이해하고 적용하면 하우스 엣지를 0.5% 이하로 낮출 수 있습니다.',
    category: '블랙잭',
    date: '2026-05-07',
    readTime: '10분',
    keywords: ['블랙잭 기본 전략표', '에볼루션 블랙잭 전략', '블랙잭 RTP', '인피니트 블랙잭 전략'],
    content: `
에볼루션카지노 블랙잭은 기본 전략(Basic Strategy)을 완벽히 따르면 RTP 99.28%, 하우스 엣지 0.5% 수준으로 낮출 수 있습니다. 이는 카지노 게임 중 가장 높은 환수율 중 하나입니다.

## 기본 전략이란?

기본 전략은 플레이어의 핸드 합계와 딜러의 업카드 조합에 따라 Hit·Stand·Double·Split의 통계적으로 최적 행동을 도표화한 것입니다.

온라인 블랙잭에서는 기본 전략표를 옆에 두고 참조하며 플레이하는 것이 허용됩니다. 적극 활용하세요.

## 핵심 규칙 요약

**항상 스플릿:** AA(에이스 페어), 88(8 페어)

**절대 스플릿 금지:** TT(10 페어), 55(5 페어)

**더블다운 권장:** 핸드 11점(항상), 핸드 10점(딜러 9 이하), 핸드 9점(딜러 3~6)

**항상 스탠드:** 핸드 17점 이상(딜러 업카드 무관)

**항상 히트:** 핸드 8점 이하

## 소프트 핸드 전략

소프트 핸드(A 포함 핸드)는 별도 규칙이 적용됩니다. A+7(소프트 18)은 딜러가 2~8일 때 스탠드, 9·10·A일 때 히트합니다.

## 보험 베팅은 하지 마세요

딜러 업카드가 A일 때 제공되는 보험(Insurance)은 하우스 엣지가 7.69%로 매우 불리합니다. 카드 카운팅을 하지 않는 일반 플레이어는 보험 베팅을 피하세요.
    `,
    faq: [
      { q: '블랙잭 기본 전략표는 어디서 구하나요?', a: '인터넷에서 "블랙잭 기본 전략표"를 검색하면 무료로 구할 수 있습니다. 온라인 블랙잭에서는 전략표를 참조하며 플레이하는 것이 허용됩니다.' },
      { q: '에볼루션 인피니트 블랙잭에서도 기본 전략이 유효한가요?', a: '네, 인피니트 블랙잭도 기본 규칙은 동일하므로 기본 전략표를 그대로 적용할 수 있습니다.' },
      { q: '블랙잭에서 AA는 항상 스플릿해야 하나요?', a: '네, AA는 딜러 업카드에 상관없이 항상 스플릿하는 것이 기본 전략입니다. 에이스는 1 또는 11로 계산되므로 두 개의 강력한 핸드를 만들 수 있습니다.' },
    ],
    relatedPosts: [
      { slug: 'evolution-baccarat-strategy-2026', title: '에볼루션카지노 바카라 전략 총정리 2026' },
      { slug: 'crazy-time-bonus-strategy', title: '크레이지타임 보너스 게임 전략' },
      { slug: 'evolution-casino-signup-guide', title: '에볼루션카지노 가입방법 단계별 완벽 가이드' },
    ],
  },
  'crazy-time-bonus-strategy': {
    title: '크레이지타임 보너스 게임 전략 — 캐시헌트·코인플립·퍼시피코 완벽 공략',
    description: '크레이지타임 4가지 보너스 게임의 확률과 최적 선택 전략을 분석합니다.',
    category: '슬롯/게임쇼',
    date: '2026-05-06',
    readTime: '7분',
    keywords: ['크레이지타임 전략', '크레이지타임 보너스', '캐시헌트 전략', '에볼루션 게임쇼 전략'],
    content: `
크레이지타임(Crazy Time)은 에볼루션의 가장 인기 있는 라이브 게임쇼입니다. 머니 휠을 스핀하여 4가지 보너스 게임 중 하나에 진입할 수 있으며, 이론상 최대 2만배 이상의 당첨금이 가능합니다.

## 머니 휠 구성

크레이지타임 휠은 총 64칸으로 구성됩니다. 1(23칸)·2(15칸)·5(7칸)·10(4칸)의 숫자 칸과 캐시헌트(8칸)·코인플립(6칸)·퍼시피코(2칸)·크레이지타임(1칸)의 보너스 칸으로 이루어져 있습니다.

## 캐시헌트(Cash Hunt) 전략

캐시헌트는 108개의 심볼 중 하나를 선택하는 게임입니다. 최소 배당은 10x이며 최대는 수백 배입니다. 선택은 순전히 랜덤이므로 전략보다는 직관으로 빠르게 선택하세요.

## 코인플립(Coin Flip) 전략

코인플립은 빨강/파랑 동전의 앞면을 맞추는 게임입니다. 멀티플라이어가 무작위로 적용되며 평균 배당은 약 40x입니다. 간단하지만 멀티플라이어에 따라 큰 당첨이 가능합니다.

## 퍼시피코(Pachinko) 전략

퍼시피코는 핀볼이 떨어지는 위치에 따라 배당을 받습니다. 더블 칸에 떨어지면 모든 배당이 두 배가 됩니다. 연속 더블 시 수천 배 당첨도 가능합니다.

## 크레이지타임(Crazy Time) 보너스

크레이지타임 보너스는 3개의 플래퍼 중 하나를 선택하는 게임입니다. 이론상 최대 2만배 이상의 당첨이 가능한 에볼루션 최고의 보너스 게임입니다.

## 베팅 전략

보너스 게임 진입 확률을 높이려면 캐시헌트(8칸)와 코인플립(6칸) 베팅을 병행하는 것이 효과적입니다. 크레이지타임(1칸)만 노리면 진입 확률이 낮습니다.
    `,
    faq: [
      { q: '크레이지타임 RTP는 얼마인가요?', a: '크레이지타임의 전체 RTP는 96.08%입니다. 베팅하는 칸에 따라 RTP가 다소 다를 수 있습니다.' },
      { q: '크레이지타임 최대 당첨금은 얼마인가요?', a: '이론상 크레이지타임 보너스에서 최대 2만배 이상의 당첨이 가능합니다. 실제로 수천 배 당첨 사례가 다수 기록되어 있습니다.' },
      { q: '크레이지타임에서 어떤 칸에 베팅해야 하나요?', a: '보너스 진입 확률을 높이려면 캐시헌트(8칸)와 코인플립(6칸)을 병행하는 것이 좋습니다. 숫자 칸(1·2·5·10)은 안정적인 소액 당첨을 원할 때 선택하세요.' },
    ],
    relatedPosts: [
      { slug: 'evolution-baccarat-strategy-2026', title: '에볼루션카지노 바카라 전략 총정리 2026' },
      { slug: 'blackjack-basic-strategy-chart', title: '에볼루션 블랙잭 기본 전략표 완벽 가이드' },
      { slug: 'evolution-casino-signup-guide', title: '에볼루션카지노 가입방법 단계별 완벽 가이드' },
    ],
  },
  'evolution-casino-signup-guide': {
    title: '에볼루션카지노 가입방법 단계별 완벽 가이드 2026',
    description: '에볼루션 라이선스 카지노 가입부터 첫 입금, 에볼루션 로비 접속까지 단계별로 안내합니다.',
    category: '가이드',
    date: '2026-05-05',
    readTime: '5분',
    keywords: ['에볼루션카지노 가입방법', '에볼루션카지노 가입', '에볼루션 라이브카지노 가입', '온라인카지노 가입방법'],
    content: `
에볼루션카지노는 B2B 소프트웨어 제공사로 직접 가입이 불가능합니다. 에볼루션 라이선스를 보유한 온라인 카지노를 통해 이용해야 합니다.

## 1단계 — 카지노 선택

에볼루션 라이선스를 보유한 합법적인 온라인 카지노를 선택합니다. UKGC·MGA 등 공신력 있는 규제 기관의 라이선스를 보유한 카지노를 선택하는 것이 중요합니다.

## 2단계 — 회원가입

카지노 사이트에서 회원가입을 진행합니다. 이메일·비밀번호·기본 정보 입력 후 이메일 인증을 완료합니다. 보통 5분 이내에 가입이 완료됩니다.

## 3단계 — 본인인증

대부분의 합법적인 카지노는 첫 출금 전 본인인증(KYC)을 요구합니다. 신분증·주소 증명 서류를 준비해두세요.

## 4단계 — 입금

카지노의 입금 방식(암호화폐·카드·전자지갑 등)을 통해 입금합니다. 첫 입금 시 보너스를 제공하는 카지노가 많으니 확인하세요.

## 5단계 — 에볼루션 로비 접속

로비에서 Live Casino 섹션을 선택하면 에볼루션의 모든 게임에 접속할 수 있습니다. 바카라·블랙잭·룰렛·게임쇼 등 200종 이상의 게임을 즐길 수 있습니다.
    `,
    faq: [
      { q: '에볼루션카지노에 직접 가입할 수 있나요?', a: '에볼루션은 B2B 소프트웨어 제공사로 직접 가입이 불가능합니다. 에볼루션 라이선스를 보유한 온라인 카지노에 가입 후 이용할 수 있습니다.' },
      { q: '에볼루션카지노 가입 시 본인인증이 필요한가요?', a: '대부분의 합법적인 카지노는 첫 출금 전 본인인증(KYC)을 요구합니다. 신분증과 주소 증명 서류를 준비해두세요.' },
      { q: '에볼루션카지노 모바일에서 가입 가능한가요?', a: '네, 에볼루션 라이선스 카지노는 모두 모바일 브라우저에서 가입 및 플레이가 가능합니다. 별도 앱 설치가 필요 없습니다.' },
    ],
    relatedPosts: [
      { slug: 'evolution-baccarat-strategy-2026', title: '에볼루션카지노 바카라 전략 총정리 2026' },
      { slug: 'baccarat-road-reading-guide', title: '바카라 빅로드·비드로드 읽는 법' },
      { slug: 'lightning-roulette-multiplier-guide', title: '라이트닝 룰렛 멀티플라이어 완벽 이해' },
    ],
  },
  'baccarat-road-reading-guide': {
    title: '바카라 빅로드·비드로드 읽는 법 — 에볼루션 바카라 통계 완벽 이해',
    description: '에볼루션 바카라의 빅로드·비드로드·스몰로드·비그아이보이 통계를 읽고 활용하는 방법을 정리합니다.',
    category: '바카라',
    date: '2026-05-04',
    readTime: '9분',
    keywords: ['바카라 빅로드', '바카라 비드로드', '바카라 통계', '에볼루션 바카라 도로'],
    content: `
에볼루션 바카라에는 4가지 통계 트래킹 도구가 기본으로 내장되어 있습니다. 빅로드(Big Road)·비드로드(Bead Road)·스몰로드(Small Road)·비그아이보이(Big Eye Boy)가 그것입니다.

## 비드로드(Bead Road)

비드로드는 가장 기본적인 통계로, 매 라운드 결과를 순서대로 기록합니다. 뱅커 승리는 빨간 원, 플레이어 승리는 파란 원, 타이는 초록 원으로 표시됩니다.

## 빅로드(Big Road)

빅로드는 연속 승리(스트릭)를 기록하는 도구입니다. 같은 결과가 연속되면 같은 열에 기록되고, 결과가 바뀌면 새 열로 이동합니다. 패턴을 시각적으로 파악하기 쉬운 가장 인기 있는 도구입니다.

## 스몰로드(Small Road)

스몰로드는 빅로드를 기반으로 2칸 간격의 패턴을 분석합니다. 패턴이 반복되면 빨간 원, 바뀌면 파란 원이 찍힙니다.

## 비그아이보이(Big Eye Boy)

비그아이보이는 빅로드를 기반으로 1칸 간격의 패턴을 분석합니다. 스몰로드보다 더 세밀한 패턴 분석이 가능합니다.

## 중요한 주의사항

바카라는 독립 시행 게임입니다. 과거 결과가 미래 결과에 영향을 미치지 않습니다. 통계 도구는 패턴을 시각화할 뿐이며, 이를 바탕으로 한 베팅이 통계적으로 유리하지 않다는 점을 반드시 기억하세요.
    `,
    faq: [
      { q: '바카라 빅로드를 읽는 방법은?', a: '빅로드는 연속 승리(스트릭)를 기록합니다. 같은 결과가 연속되면 같은 열에 기록되고, 결과가 바뀌면 새 열로 이동합니다. 뱅커는 빨간 원, 플레이어는 파란 원입니다.' },
      { q: '바카라 통계 도구가 베팅에 도움이 되나요?', a: '바카라는 독립 시행 게임이므로 과거 결과가 미래를 예측하지 못합니다. 통계 도구는 패턴을 시각화할 뿐이며 베팅 우위를 제공하지 않습니다.' },
      { q: '에볼루션 바카라에서 통계 도구는 어디서 볼 수 있나요?', a: '에볼루션 바카라 게임 화면 하단에 빅로드·비드로드·스몰로드·비그아이보이가 기본으로 표시됩니다. 클릭하여 크게 볼 수도 있습니다.' },
    ],
    relatedPosts: [
      { slug: 'evolution-baccarat-strategy-2026', title: '에볼루션카지노 바카라 전략 총정리 2026' },
      { slug: 'evolution-casino-signup-guide', title: '에볼루션카지노 가입방법 단계별 완벽 가이드' },
      { slug: 'lightning-roulette-multiplier-guide', title: '라이트닝 룰렛 멀티플라이어 완벽 이해' },
    ],
  },
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }): Promise<Metadata> {
  const { slug } = await params
  const post = posts[slug]
  if (!post) return { title: '포스트를 찾을 수 없습니다 | WOORIWIN' }
  return {
    title: `${post.title} | WOORIWIN`,
    description: post.description,
    keywords: post.keywords,
    alternates: { canonical: `https://wooriwin.com/blog/${slug}` },
    openGraph: {
      title: post.title,
      description: post.description,
      url: `https://wooriwin.com/blog/${slug}`,
      siteName: 'WOORIWIN',
      locale: 'ko_KR',
      type: 'article',
      images: [{ url: 'https://wooriwin.com/images/blog.jpg', width: 1200, height: 630 }],
    },
  }
}

export async function generateStaticParams() {
  return Object.keys(posts).map((slug) => ({ slug }))
}

export default async function BlogPostPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params
  const post = posts[slug]

  if (!post) {
    return (
      <main className="min-h-screen bg-gray-900 text-white flex items-center justify-center">
        <div className="text-center">
          <h1 className="text-4xl font-bold mb-4">404</h1>
          <p className="text-gray-400 mb-6">포스트를 찾을 수 없습니다.</p>
          <Link href="/blog" className="text-yellow-400 hover:underline">블로그로 돌아가기</Link>
        </div>
      </main>
    )
  }

  const jsonLd = {
    '@context': 'https://schema.org',
    '@graph': [
      {
        '@type': 'Article',
        headline: post.title,
        description: post.description,
        url: `https://wooriwin.com/blog/${slug}`,
        inLanguage: 'ko-KR',
        datePublished: post.date,
        dateModified: post.date,
        author: { '@type': 'Organization', name: 'WOORIWIN' },
        publisher: { '@type': 'Organization', name: 'WOORIWIN', url: 'https://wooriwin.com' },
      },
      {
        '@type': 'FAQPage',
        mainEntity: post.faq.map((f) => ({
          '@type': 'Question',
          name: f.q,
          acceptedAnswer: { '@type': 'Answer', text: f.a },
        })),
      },
    ],
  }

  const paragraphs = post.content.trim().split('\n\n').filter(Boolean)

  return (
    <>
      <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(jsonLd) }} />
      <main className="min-h-screen bg-gray-900 text-white">

        {/* Hero */}
        <section className="bg-gray-800 py-12 px-4 border-b border-gray-700">
          <div className="max-w-4xl mx-auto">
            <nav className="text-sm text-gray-400 mb-4">
              <Link href="/" className="hover:text-yellow-400">홈</Link> &rsaquo;{' '}
              <Link href="/blog" className="hover:text-yellow-400">블로그</Link> &rsaquo;{' '}
              <span className="text-white">{post.category}</span>
            </nav>
            <div className="flex items-center gap-3 mb-4">
              <span className="text-xs font-semibold text-yellow-400 bg-yellow-400/10 px-2 py-1 rounded">{post.category}</span>
              <span className="text-xs text-gray-500">{post.readTime} 읽기</span>
              <span className="text-xs text-gray-500">{post.date}</span>
            </div>
            <h1 className="text-3xl md:text-4xl font-bold leading-tight mb-4">{post.title}</h1>
            <p className="text-gray-400 text-lg leading-relaxed">{post.description}</p>
          </div>
        </section>

        {/* 본문 + 사이드바 */}
        <div className="max-w-6xl mx-auto px-4 py-12 flex gap-10">

          {/* 본문 */}
          <article className="flex-1 min-w-0">
            <div className="text-gray-300 space-y-6 leading-relaxed text-base md:text-lg">
              {paragraphs.map((para, i) => {
                if (para.startsWith('## ')) {
                  return <h2 key={i} className="text-2xl font-bold text-yellow-400 mt-8 mb-4">{para.replace('## ', '')}</h2>
                }
                if (para.startsWith('**') && para.endsWith('**')) {
                  return <p key={i} className="font-bold text-white">{para.replace(/\*\*/g, '')}</p>
                }
                return <p key={i}>{para}</p>
              })}
            </div>

            {/* FAQ */}
            <section className="mt-16">
              <h2 className="text-2xl font-bold mb-6 text-yellow-400">자주 묻는 질문</h2>
              <div className="space-y-4">
                {post.faq.map((f, i) => (
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
          </article>

          {/* 사이드바 */}
          <aside className="hidden lg:block w-64 shrink-0">
            <div className="sticky top-8 space-y-6">
              <div className="bg-gray-800 rounded-xl p-5 border border-gray-700">
                <h3 className="text-yellow-400 font-bold mb-4">관련 포스트</h3>
                <ul className="space-y-3">
                  {post.relatedPosts.map((r) => (
                    <li key={r.slug}>
                      <Link href={`/blog/${r.slug}`} className="text-gray-400 text-sm hover:text-yellow-400 transition leading-snug block">
                        → {r.title}
                      </Link>
                    </li>
                  ))}
                </ul>
              </div>
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
