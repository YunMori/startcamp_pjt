<script setup>
import { computed, reactive, watch } from 'vue'
import { usePanelStore } from '../../stores/usePanelStore'
import { useReviewStore } from '../../stores/useReviewStore'
import RegionInfo from './RegionInfo.vue'
import CourseSpots from './CourseSpots.vue'
import ReviewBoard from './ReviewBoard.vue'
import ReviewDetail from './ReviewDetail.vue'
import ReviewForm from './ReviewForm.vue'
import PasswordGate from './PasswordGate.vue'

const { state: panel, course, closePanel, showBoard, showDetail, showWrite, showEdit } = usePanelStore()
const reviewStore = useReviewStore()

const gate = reactive({
  open: false,
  action: null, // 'edit' | 'delete'
  error: false,
  verifiedPassword: '',
})

const region = computed(() => course.value?.region || null)
const reviewList = computed(() => reviewStore.state.byCourse[panel.courseId] || [])
const activeReview = computed(() => reviewStore.getReview(panel.courseId, panel.activeReviewId))

watch(
  () => [panel.open, panel.courseId],
  ([open, courseId]) => {
    if (open && courseId) reviewStore.loadReviews(courseId)
  },
)

function openGate(action) {
  gate.action = action
  gate.error = false
  gate.open = true
}

function closeGate() {
  gate.open = false
  gate.error = false
}

async function confirmGate(password) {
  const reviewId = panel.activeReviewId
  try {
    if (gate.action === 'delete') {
      await reviewStore.removeReview(panel.courseId, reviewId, password)
      closeGate()
      showBoard()
    } else {
      await reviewStore.verifyPassword(reviewId, password)
      gate.verifiedPassword = password
      closeGate()
      showEdit()
    }
  } catch {
    gate.error = true
  }
}

async function handleWrite(form) {
  await reviewStore.addReview(panel.courseId, form)
  showBoard()
}

async function handleEdit(form) {
  const reviewId = panel.activeReviewId
  await reviewStore.editReview(panel.courseId, reviewId, {
    ...form,
    // 권한 확인은 게이트에서 검증한 비밀번호로, 폼의 비밀번호는 새 비밀번호(선택)
    password: gate.verifiedPassword,
    newPassword: form.password,
  })
  showDetail(reviewId)
}
</script>

<template>
  <!-- 스크림: 패널이 열릴 때 챗 화면 위를 살짝 덮되 대화 맥락은 유지 -->
  <div
    class="scrim"
    :class="{ visible: panel.open }"
    @click="closePanel"
  ></div>

  <div class="panel" :class="{ open: panel.open }">
    <div class="grabber-wrap"><div class="grabber"></div></div>

    <div v-if="course" class="head">
      <span class="kind">{{ region.kind }}</span>
      <div class="name">{{ region.name }}</div>
      <button class="close" @click="closePanel">✕</button>
    </div>

    <div v-if="course" class="scroll">
      <RegionInfo :region="region" />

      <CourseSpots :spots="course.spots" :duration="course.duration" />

      <div class="review-head">
        <div class="review-title">
          익명 리뷰 <span class="count">{{ reviewList.length }}</span>
        </div>
        <button v-if="panel.view === 'board'" class="write-btn" @click="showWrite">✏️ 리뷰 쓰기</button>
      </div>

      <ReviewBoard v-if="panel.view === 'board'" />
      <ReviewDetail
        v-else-if="panel.view === 'detail'"
        @request-edit="openGate('edit')"
        @request-delete="openGate('delete')"
      />
      <ReviewForm
        v-else-if="panel.view === 'write'"
        mode="write"
        @submit="handleWrite"
        @cancel="showBoard"
      />
      <ReviewForm
        v-else-if="panel.view === 'edit'"
        mode="edit"
        :initial="activeReview"
        @submit="handleEdit"
        @cancel="showDetail(panel.activeReviewId)"
      />
    </div>

    <div class="footer">
      <button class="back-to-chat" @click="closePanel">💬 챗봇에게 다른 곳 물어보기</button>
    </div>

    <PasswordGate
      v-if="gate.open"
      :title="gate.action === 'delete' ? '리뷰 삭제' : '리뷰 수정'"
      :error="gate.error"
      @confirm="confirmGate"
      @close="closeGate"
    />
  </div>
</template>

<style scoped>
.scrim {
  position: absolute;
  inset: 0;
  background: rgba(50, 25, 30, 0.35);
  transition: opacity 0.35s;
  opacity: 0;
  pointer-events: none;
  z-index: 5;
}

.scrim.visible {
  opacity: 1;
  pointer-events: auto;
}

.panel {
  position: absolute;
  left: 0;
  right: 0;
  bottom: 0;
  top: 64px;
  background: var(--panel-bg);
  border-radius: 24px 24px 0 0;
  box-shadow: 0 -10px 40px rgba(60, 20, 30, 0.25);
  transform: translateY(110%);
  transition: transform 0.42s cubic-bezier(0.22, 1, 0.36, 1);
  z-index: 6;
  display: flex;
  flex-direction: column;
  overflow: hidden;
}

.panel.open {
  transform: translateY(0);
}

.grabber-wrap {
  padding: 9px 0 3px;
  display: flex;
  justify-content: center;
  flex-shrink: 0;
}

.grabber {
  width: 40px;
  height: 5px;
  border-radius: 3px;
  background: #e6d6d0;
}

.head {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 5px 16px 12px;
  flex-shrink: 0;
  border-bottom: 1px solid var(--border);
}

.kind {
  font-size: 11px;
  font-weight: 700;
  padding: 3px 9px;
  border-radius: 10px;
  background: var(--primary-bg);
  color: var(--primary);
  flex-shrink: 0;
}

.name {
  font-weight: 700;
  font-size: 15px;
  color: var(--text);
  flex: 1;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.close {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  border: none;
  background: var(--input-bg);
  cursor: pointer;
  font-size: 15px;
  color: var(--text-muted);
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.scroll {
  flex: 1;
  overflow-y: auto;
  padding: 14px 16px 16px;
}

.review-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 11px;
}

.review-title {
  font-weight: 700;
  font-size: 15px;
  color: var(--text);
}

.count {
  color: var(--primary);
}

.write-btn {
  border: none;
  background: var(--gradient);
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  padding: 7px 13px;
  border-radius: 16px;
  cursor: pointer;
}

.footer {
  padding: 12px 16px max(16px, env(safe-area-inset-bottom));
  border-top: 1px solid var(--border-soft);
  flex-shrink: 0;
  background: var(--panel-bg);
}

.back-to-chat {
  width: 100%;
  padding: 13px;
  border-radius: 16px;
  border: 1.5px solid var(--primary-soft);
  background: #fff;
  color: var(--primary);
  font-weight: 700;
  font-size: 14px;
  cursor: pointer;
}

.back-to-chat:hover {
  background: #fff4f6;
}
</style>
