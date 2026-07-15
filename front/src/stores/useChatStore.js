import { reactive, readonly } from 'vue'
import { SURVEY, COURSES } from '../data/courses'
import { sendChatMessage, recommendCourses, getCourseStory } from '../services/chatApi'

let seq = 0
const newId = () => ++seq

const state = reactive({
  messages: [
    { id: newId(), role: 'bot', kind: 'text', text: '안녕하세요! 저는 두 분의 데이트를 함께 그려갈 큐레이터, 러비예요 🍒' },
    { id: newId(), role: 'bot', kind: 'text', text: '대전·충청 어디든 오늘 딱 맞는 코스를 찾아드릴게요. 몇 가지만 여쭤볼게요!' },
    { id: newId(), role: 'bot', kind: 'chips', text: SURVEY[0].q, chips: SURVEY[0].chips, answered: false, selected: null },
  ],
  step: 0,
  answers: {}, // SURVEY key(mobility/festival/q1~q5) -> value
  sending: false,
  storyLoaded: {}, // courseId -> true (스토리 중복 요청 방지)
})

function pushTyping() {
  state.messages.push({ id: newId(), role: 'bot', kind: 'typing' })
}

function removeTyping() {
  state.messages = state.messages.filter((m) => m.kind !== 'typing')
}

// 설문 칩 선택 — chip: { label, value }
function answer(msgId, chip) {
  const msg = state.messages.find((m) => m.id === msgId)
  if (!msg || msg.answered) return
  msg.answered = true
  msg.selected = chip.label
  state.answers[SURVEY[state.step].key] = chip.value
  state.messages.push({ id: newId(), role: 'user', kind: 'text', text: chip.label })
  pushTyping()
  setTimeout(advance, 850)
}

// 다음 설문 질문 또는 추천 카드 노출
async function advance() {
  const next = state.step + 1
  state.step = next
  if (next < SURVEY.length) {
    removeTyping()
    state.messages.push({ id: newId(), role: 'bot', kind: 'chips', text: SURVEY[next].q, chips: SURVEY[next].chips, answered: false, selected: null })
    return
  }

  // 설문 완료 → 백엔드 추천 알고리즘 호출
  let courseIds
  try {
    const recommended = await recommendCourses(state.answers)
    courseIds = recommended.map((c) => c.id).filter((id) => COURSES.some((c) => c.id === id))
  } catch {
    courseIds = null
  }
  removeTyping()

  if (courseIds && courseIds.length) {
    state.messages.push({ id: newId(), role: 'bot', kind: 'text', text: '완벽해요! 두 분의 취향을 담아 딱 맞는 코스를 골라봤어요 💕 마음에 드는 코스를 눌러보세요.' })
  } else {
    courseIds = ['course_C', 'course_B', 'course_A']
    state.messages.push({ id: newId(), role: 'bot', kind: 'text', text: '앗, 추천 서버 연결이 잠시 어려워서 러비의 기본 추천 코스를 보여드릴게요 🥲' })
  }
  state.messages.push({ id: newId(), role: 'bot', kind: 'cards', courseIds })
}

// 코스 카드 선택 → Gemini 스토리텔링 메시지 요청 (코스당 1회)
async function selectCourse(courseId) {
  if (state.storyLoaded[courseId]) return
  state.storyLoaded[courseId] = true

  const course = COURSES.find((c) => c.id === courseId)
  pushTyping()
  try {
    const { message } = await getCourseStory(courseId)
    removeTyping()
    state.messages.push({ id: newId(), role: 'bot', kind: 'text', text: message })
  } catch {
    removeTyping()
    if (course) {
      state.messages.push({ id: newId(), role: 'bot', kind: 'text', text: `'${course.name}' 좋은 선택이에요! 옆 패널에서 코스 소개와 리뷰를 확인해 보세요 💕` })
    }
    state.storyLoaded[courseId] = false
  }
}

// 자유 채팅 전송 (백엔드 POST /chat)
async function sendChat(text) {
  const trimmed = (text || '').trim()
  if (!trimmed || state.sending) return
  state.sending = true
  state.messages.push({ id: newId(), role: 'user', kind: 'text', text: trimmed })
  pushTyping()

  const history = state.messages
    .filter((m) => m.kind === 'text')
    .slice(-10)
    .map((m) => ({ role: m.role === 'user' ? 'user' : 'assistant', content: m.text }))

  try {
    const reply = await sendChatMessage(history)
    removeTyping()
    state.messages.push({ id: newId(), role: 'bot', kind: 'text', text: reply || '음, 다시 한 번 말씀해 주실래요? 😊' })
  } catch {
    removeTyping()
    state.messages.push({ id: newId(), role: 'bot', kind: 'text', text: '앗, 지금은 응답을 불러오기 어려워요 🥲 잠시 후 다시 시도해 주세요!' })
  } finally {
    state.sending = false
  }
}

export function useChatStore() {
  return { state: readonly(state), answer, sendChat, selectCourse }
}
