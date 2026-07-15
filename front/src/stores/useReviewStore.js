import { reactive, readonly } from 'vue'
import * as reviewApi from '../services/reviewApi'

const state = reactive({
  byCourse: {}, // courseId -> review[]
  loading: false,
})

async function loadReviews(courseId) {
  state.loading = true
  try {
    state.byCourse[courseId] = await reviewApi.getReviews(courseId)
  } finally {
    state.loading = false
  }
}

async function addReview(courseId, form) {
  await reviewApi.createReview(courseId, form)
  await loadReviews(courseId)
}

async function editReview(courseId, reviewId, form) {
  await reviewApi.updateReview(reviewId, form)
  await loadReviews(courseId)
}

async function removeReview(courseId, reviewId, password) {
  await reviewApi.deleteReview(reviewId, password)
  await loadReviews(courseId)
}

function getReview(courseId, reviewId) {
  return (state.byCourse[courseId] || []).find((r) => r.id === reviewId) || null
}

export function useReviewStore() {
  return {
    state: readonly(state),
    loadReviews,
    addReview,
    editReview,
    removeReview,
    getReview,
    verifyPassword: reviewApi.verifyPassword,
  }
}
