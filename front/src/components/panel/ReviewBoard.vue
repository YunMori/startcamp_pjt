<script setup>
import { computed } from 'vue'
import { usePanelStore } from '../../stores/usePanelStore'
import { useReviewStore } from '../../stores/useReviewStore'

const { state: panel, showDetail } = usePanelStore()
const { state: reviews } = useReviewStore()

const list = computed(() => reviews.byCourse[panel.courseId] || [])

const stars = (n) => '★'.repeat(n)
const starsOff = (n) => '★'.repeat(5 - n)
</script>

<template>
  <div>
    <div v-if="reviews.loading" class="empty">리뷰를 불러오는 중…</div>
    <div v-else-if="list.length === 0" class="empty">
      아직 리뷰가 없어요.<br />첫 리뷰를 남겨보세요! 💕
    </div>
    <div v-else class="items">
      <button v-for="r in list" :key="r.id" class="item" @click="showDetail(r.id)">
        <div class="meta">
          <div class="face">🙂</div>
          <span class="nick">{{ r.nickname }}</span>
          <span class="stars">{{ stars(r.rating) }}<span class="off">{{ starsOff(r.rating) }}</span></span>
          <span class="date">{{ r.date }}</span>
        </div>
        <div class="text">{{ r.text }}</div>
      </button>
    </div>
  </div>
</template>

<style scoped>
.empty {
  text-align: center;
  color: var(--text-faint);
  font-size: 13px;
  padding: 26px 0;
  line-height: 1.6;
}

.items {
  display: flex;
  flex-direction: column;
  gap: 9px;
}

.item {
  text-align: left;
  background: #fff;
  border: 1px solid var(--border-soft);
  border-radius: 14px;
  padding: 12px 13px;
  cursor: pointer;
  width: 100%;
  transition: border-color 0.15s;
}

.item:hover {
  border-color: var(--primary-soft);
}

.meta {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 6px;
}

.face {
  width: 26px;
  height: 26px;
  border-radius: 50%;
  background: var(--primary-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 13px;
}

.nick {
  font-weight: 700;
  font-size: 13px;
  color: var(--text);
}

.stars {
  font-size: 12px;
  color: var(--star);
  letter-spacing: 1px;
}

.off {
  color: var(--star-off);
}

.date {
  margin-left: auto;
  font-size: 11px;
  color: var(--text-faint);
}

.text {
  font-size: 13px;
  line-height: 1.5;
  color: var(--text-sub);
  overflow: hidden;
  display: -webkit-box;
  -webkit-line-clamp: 2;
  -webkit-box-orient: vertical;
}
</style>
