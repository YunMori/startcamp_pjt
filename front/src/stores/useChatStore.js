import { reactive, readonly } from 'vue'
import { SURVEY } from '../data/courses'
import { sendChatMessage } from '../services/chatApi'

let seq = 0
const newId = () => ++seq

const state = reactive({
  messages: [
    { id: newId(), role: 'bot', kind: 'text', text: '안녕하세요! 저는 두 분의 데이트를 함께 그려갈 큐레이터, 러비예요 🍒' },
    { id: newId(), role: 'bot', kind: 'text', text: '대전·충청 어디든 오늘 딱 맞는 코스를 찾아드릴게요. 몇 가지만 여쭤볼게요!' },
    { id: newId(), role: 'bot', kind: 'chips', text: SURVEY[0].q, chips: SURVEY[0].chips, answered: false, selected: null },
  ],
  step: 0,
  sending: false,
})

function pushTyping() {
  state.messages.push({ id: newId(), role: 'bot', kind: 'typing' })
}

function removeTyping() {
  state.messages = state.messages.filter((m) => m.kind !== 'typing')
}

// 설문 칩 선택
function answer(msgId, label) {
  const msg = state.messages.find((m) => m.id === msgId)
  if (!msg || msg.answered) return
  msg.answered = true
  msg.selected = label
  state.messages.push({ id: newId(), role: 'user', kind: 'text', text: label })
  pushTyping()
  setTimeout(advance, 850)
}

// 다음 설문 질문 또는 추천 카드 노출
function advance() {
  removeTyping()
  const next = state.step + 1
  state.step = next
  if (next < SURVEY.length) {
    state.messages.push({ id: newId(), role: 'bot', kind: 'chips', text: SURVEY[next].q, chips: SURVEY[next].chips, answered: false, selected: null })
    return
  }
  state.messages.push({ id: newId(), role: 'bot', kind: 'text', text: '완벽해요! 두 분의 취향을 담아 딱 맞는 코스 세 가지를 골라봤어요 💕 마음에 드는 코스를 눌러보세요.' })
  state.messages.push({ id: newId(), role: 'bot', kind: 'cards' })
}

// 자유 채팅 전송 (응답은 백엔드 /chat 프록시 — 준비 전에는 목 응답)
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
  return { state: readonly(state), answer, sendChat }
}
