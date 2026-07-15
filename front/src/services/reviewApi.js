import http from './http'
import { SEED_REVIEWS } from '../data/courses'

// 백엔드(FastAPI) 준비 전까지 목 데이터로 동작. 연동 시 false로 전환.
const USE_MOCK = true

const delay = (ms = 250) => new Promise((r) => setTimeout(r, ms))

// ---- 목 저장소 (새로고침 시 초기화) ----
const mockDB = JSON.parse(JSON.stringify(SEED_REVIEWS))
let mockSeq = 100

const today = () => {
  const d = new Date()
  return `${d.getFullYear()}.${String(d.getMonth() + 1).padStart(2, '0')}.${String(d.getDate()).padStart(2, '0')}`
}

const findReview = (reviewId) => {
  for (const courseId of Object.keys(mockDB)) {
    const review = mockDB[courseId].find((r) => r.id === reviewId)
    if (review) return { courseId, review }
  }
  return null
}

// 비밀번호 불일치를 백엔드의 403 응답처럼 표현하기 위한 에러
export class PasswordMismatchError extends Error {
  constructor() {
    super('비밀번호가 일치하지 않아요.')
    this.name = 'PasswordMismatchError'
  }
}

// GET /courses/{courseId}/reviews
export async function getReviews(courseId) {
  if (USE_MOCK) {
    await delay()
    return (mockDB[courseId] || []).map(({ password, ...rest }) => rest)
  }
  const { data } = await http.get(`/courses/${courseId}/reviews`)
  return data
}

// POST /courses/{courseId}/reviews
export async function createReview(courseId, { nickname, rating, text, password }) {
  if (USE_MOCK) {
    await delay()
    const review = { id: `r${++mockSeq}`, nickname, rating, text, password, date: today() }
    mockDB[courseId] = [review, ...(mockDB[courseId] || [])]
    const { password: _, ...rest } = review
    return rest
  }
  const { data } = await http.post(`/courses/${courseId}/reviews`, { nickname, rating, text, password })
  return data
}

// POST /reviews/{reviewId}/verify — 수정/삭제 전 비밀번호 확인
export async function verifyPassword(reviewId, password) {
  if (USE_MOCK) {
    await delay()
    const found = findReview(reviewId)
    if (!found || found.review.password !== password) throw new PasswordMismatchError()
    return true
  }
  try {
    await http.post(`/reviews/${reviewId}/verify`, { password })
    return true
  } catch (err) {
    if (err.response?.status === 403) throw new PasswordMismatchError()
    throw err
  }
}

// PUT /reviews/{reviewId}
export async function updateReview(reviewId, { nickname, rating, text, password }) {
  if (USE_MOCK) {
    await delay()
    const found = findReview(reviewId)
    if (!found) throw new Error('리뷰를 찾을 수 없어요.')
    Object.assign(found.review, { nickname, rating, text })
    if (password) found.review.password = password
    const { password: _, ...rest } = found.review
    return rest
  }
  const { data } = await http.put(`/reviews/${reviewId}`, { nickname, rating, text, password })
  return data
}

// DELETE /reviews/{reviewId}
export async function deleteReview(reviewId, password) {
  if (USE_MOCK) {
    await delay()
    const found = findReview(reviewId)
    if (!found || found.review.password !== password) throw new PasswordMismatchError()
    mockDB[found.courseId] = mockDB[found.courseId].filter((r) => r.id !== reviewId)
    return true
  }
  try {
    await http.delete(`/reviews/${reviewId}`, { data: { password } })
    return true
  } catch (err) {
    if (err.response?.status === 403) throw new PasswordMismatchError()
    throw err
  }
}
