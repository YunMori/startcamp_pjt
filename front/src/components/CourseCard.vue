<script setup>
import KakaoMiniMap from './KakaoMiniMap.vue'
import { usePanelStore } from '../stores/usePanelStore'

const props = defineProps({
  course: { type: Object, required: true },
})

const { openPanel } = usePanelStore()
</script>

<template>
  <button class="card" @click="openPanel(course.id)">
    <KakaoMiniMap :spots="course.spots" />
    <div class="body">
      <div class="thumb">{{ course.emoji }}</div>
      <div class="name-row">
        <div class="name">{{ course.name }}</div>
      </div>
      <div class="tags">
        <span v-for="tag in course.tags" :key="tag" class="tag">{{ tag }}</span>
      </div>
      <div class="footer">
        <div class="duration">
          <svg width="13" height="13" viewBox="0 0 24 24" fill="none">
            <circle cx="12" cy="12" r="9" stroke="#C9B6B9" stroke-width="2" />
            <path d="M12 7v5l3 2" stroke="#C9B6B9" stroke-width="2" stroke-linecap="round" />
          </svg>
          {{ course.duration }}
        </div>
        <span class="cta">코스 보기 →</span>
      </div>
    </div>
  </button>
</template>

<style scoped>
.card {
  text-align: left;
  padding: 0;
  border: 1px solid var(--border);
  background: #fff;
  border-radius: 18px;
  overflow: hidden;
  box-shadow: 0 6px 18px rgba(60, 20, 30, 0.08);
  cursor: pointer;
  transition: transform 0.18s, box-shadow 0.18s;
  width: 100%;
}

.card:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 28px rgba(240, 78, 107, 0.18);
}

.body {
  padding: 12px 14px 14px;
  position: relative;
}

.thumb {
  position: absolute;
  top: -30px;
  left: 14px;
  width: 52px;
  height: 52px;
  border-radius: 14px;
  border: 3px solid #fff;
  background: var(--primary-bg);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 26px;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.14);
  z-index: 2;
}

.name-row {
  padding-left: 62px;
  min-height: 26px;
  display: flex;
  align-items: center;
}

.name {
  font-weight: 700;
  font-size: 15px;
  color: var(--text);
}

.tags {
  display: flex;
  flex-wrap: wrap;
  gap: 6px;
  margin-top: 10px;
}

.tag {
  font-size: 11px;
  font-weight: 600;
  color: var(--primary);
  background: var(--primary-bg);
  padding: 3px 9px;
  border-radius: 12px;
}

.footer {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-top: 11px;
}

.duration {
  display: flex;
  align-items: center;
  gap: 5px;
  font-size: 12px;
  color: var(--text-muted);
}

.cta {
  font-size: 12px;
  font-weight: 700;
  color: var(--primary);
}
</style>
