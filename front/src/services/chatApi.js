import http from './http'

// 자유 채팅 LLM 응답은 백엔드(FastAPI)의 POST /chat 프록시 담당.
// 백엔드가 준비되면 false로 전환.
const USE_MOCK = true

const MOCK_REPLIES = [
  '아직 자유 대화 기능은 준비 중이에요 🥲 위의 선택지 버튼으로 코스를 추천받아 보세요!',
  '조금만 기다려 주세요, 자유 대화는 곧 열릴 예정이에요 😊 지금은 설문으로 딱 맞는 코스를 찾아드릴게요!',
]
let mockIdx = 0

/**
 * @param {{role: 'user'|'assistant', content: string}[]} history 최근 대화 히스토리
 * @returns {Promise<string>} 챗봇 응답 텍스트
 */
export async function sendChatMessage(history) {
  if (USE_MOCK) {
    await new Promise((r) => setTimeout(r, 700))
    return MOCK_REPLIES[mockIdx++ % MOCK_REPLIES.length]
  }
  const { data } = await http.post('/chat', { messages: history })
  return data.reply
}
