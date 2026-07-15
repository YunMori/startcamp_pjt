import http from './http'

// 백엔드(FastAPI :8000) 연동. 문제가 있을 때만 true로 되돌려 목으로 개발.
const USE_MOCK = false

const MOCK_REPLIES = [
  '아직 자유 대화 기능은 준비 중이에요 🥲 위의 선택지 버튼으로 코스를 추천받아 보세요!',
  '조금만 기다려 주세요, 자유 대화는 곧 열릴 예정이에요 😊 지금은 설문으로 딱 맞는 코스를 찾아드릴게요!',
]
let mockIdx = 0

/**
 * 자유 채팅 — POST /chat
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

/**
 * 설문 답변으로 추천 코스 상위 3개 조회 — POST /api/recommend
 * @param {{mobility: string, festival: boolean, q1: string, q2: string, q3: string, q4: string, q5: string}} answers
 * @returns {Promise<{id: string, name: string, spots: {name, lat, lng}[]}[]>}
 */
export async function recommendCourses(answers) {
  const { data } = await http.post('/api/recommend', answers)
  return data.courses
}

/**
 * 선택한 코스의 Gemini 스토리텔링 + 지도 핀 좌표 — POST /api/chat
 * @param {string} courseId 예: 'course_A'
 * @returns {Promise<{message: string, places: {name, lat, lng, image_url, address}[]}>}
 */
export async function getCourseStory(courseId) {
  const { data } = await http.post('/api/chat', { course_id: courseId })
  return data
}
