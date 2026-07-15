import { computed, reactive, readonly } from 'vue'
import { COURSES } from '../data/courses'

const state = reactive({
  open: false,
  courseId: null,
  view: 'board', // board | detail | write | edit
  activeReviewId: null,
})

const course = computed(() => COURSES.find((c) => c.id === state.courseId) || null)

function openPanel(courseId) {
  state.courseId = courseId
  state.view = 'board'
  state.activeReviewId = null
  state.open = true
}

function closePanel() {
  state.open = false
}

function showBoard() {
  state.view = 'board'
  state.activeReviewId = null
}

function showDetail(reviewId) {
  state.activeReviewId = reviewId
  state.view = 'detail'
}

function showWrite() {
  state.view = 'write'
}

function showEdit() {
  state.view = 'edit'
}

export function usePanelStore() {
  return { state: readonly(state), course, openPanel, closePanel, showBoard, showDetail, showWrite, showEdit }
}
