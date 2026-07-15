<script setup>
import { computed } from 'vue'
import { usePanelStore } from '../../stores/usePanelStore'
import { useReviewStore } from '../../stores/useReviewStore'

const emit = defineEmits(['request-edit', 'request-delete'])

const { state: panel, showBoard } = usePanelStore()
const { getReview } = useReviewStore()

const review = computed(() => getReview(panel.courseId, panel.activeReviewId))

const stars = (n) => '★'.repeat(n)
const starsOff = (n) => '★'.repeat(5 - n)
</script>

<template>
  <div v-if="review">
    <div class="card">
      <div class="meta">
        <div class="face">🙂</div>
        <div>
          <div class="nick">{{ review.nickname }}</div>
          <div class="date">{{ review.date }}</div>
        </div>
        <span class="stars">{{ stars(review.rating) }}<span class="off">{{ starsOff(review.rating) }}</span></span>
      </div>
      <p class="text">{{ review.text }}</p>
    </div>
    <div class="actions">
      <button class="btn ghost" @click="showBoard">← 목록</button>
      <button class="btn outline" @click="emit('request-edit')">수정</button>
      <button class="btn danger" @click="emit('request-delete')">삭제</button>
    </div>
  </div>
</template>

<style scoped>
.card {
  background: #fff;
  border: 1px solid var(--border-soft);
  border-radius: 14px;
  padding: 15px;
}

.meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 8px;
}

.face {
  width: 32px;
  height: 32px;
  border-radius: 50%;
  background: var(--primary-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
}

.nick {
  font-weight: 700;
  font-size: 14px;
  color: var(--text);
}

.date {
  font-size: 11px;
  color: var(--text-faint);
}

.stars {
  margin-left: auto;
  font-size: 15px;
  color: var(--star);
  letter-spacing: 1px;
}

.off {
  color: var(--star-off);
}

.text {
  font-size: 14px;
  line-height: 1.75;
  color: var(--text);
  margin: 6px 0 0;
}

.actions {
  display: flex;
  gap: 8px;
  margin-top: 12px;
}

.btn {
  flex: 1;
  padding: 11px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  font-size: 13px;
}

.ghost {
  border: 1.5px solid #eeddd8;
  background: #fff;
  color: var(--text-muted);
}

.outline {
  border: 1.5px solid var(--primary-soft);
  background: #fff;
  color: var(--primary);
}

.danger {
  border: none;
  background: #ffecec;
  color: var(--danger);
}
</style>
