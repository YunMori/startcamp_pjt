<script setup>
defineProps({
  region: { type: Object, required: true },
})
</script>

<template>
  <div>
    <div class="photo">
      <span class="photo-emoji">{{ region.emoji }}</span>
      <span class="photo-label">지역·축제 대표 사진</span>
    </div>
    <div v-if="region.isFestival" class="period">📅 축제 기간 {{ region.period }}</div>
    <p class="desc">{{ region.desc }}</p>
    <div class="divider"></div>
  </div>
</template>

<style scoped>
.photo {
  height: 150px;
  border-radius: 16px;
  overflow: hidden;
  position: relative;
  background: linear-gradient(135deg, #ffe1e9, #f3e7e1);
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  gap: 6px;
}

.photo-emoji {
  font-size: 44px;
}

.photo-label {
  font-size: 11px;
  color: var(--text-faint);
  font-weight: 600;
}

.period {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  margin-top: 12px;
  background: #fff3d6;
  color: #b07a00;
  font-size: 12px;
  font-weight: 700;
  padding: 5px 11px;
  border-radius: 12px;
}

.desc {
  font-size: 13px;
  line-height: 1.75;
  color: var(--text-sub);
  margin: 12px 0 0;
}

.divider {
  height: 1px;
  background: var(--border-soft);
  margin: 16px 0;
}
</style>
