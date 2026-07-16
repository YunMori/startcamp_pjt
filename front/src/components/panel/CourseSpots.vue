<script setup>
defineProps({
  spots: { type: Array, required: true },
  duration: { type: String, default: '' },
})
</script>

<template>
  <div>
    <div class="spots-head">
      <div class="spots-title">📍 코스 동선</div>
      <span v-if="duration" class="duration-badge">⏱ {{ duration }}</span>
    </div>
    <ol class="spot-list">
      <li v-for="(spot, i) in spots" :key="spot.name" class="spot-item">
        <div class="spot-marker">
          <span class="spot-num">{{ i + 1 }}</span>
          <span v-if="i < spots.length - 1" class="spot-line"></span>
        </div>
        <div class="spot-name">{{ spot.name }}</div>
      </li>
    </ol>
    <div class="divider"></div>
  </div>
</template>

<style scoped>
.spots-head {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.spots-title {
  font-weight: 700;
  font-size: 15px;
  color: var(--text);
}

.duration-badge {
  font-size: 11px;
  font-weight: 700;
  color: var(--primary);
  background: var(--primary-bg);
  padding: 3px 9px;
  border-radius: 10px;
}

.spot-list {
  list-style: none;
  margin: 0;
  padding: 0;
}

.spot-item {
  display: flex;
  align-items: stretch;
  gap: 11px;
}

.spot-marker {
  display: flex;
  flex-direction: column;
  align-items: center;
  flex-shrink: 0;
}

.spot-num {
  width: 24px;
  height: 24px;
  border-radius: 50%;
  background: var(--gradient);
  color: #fff;
  font-size: 12px;
  font-weight: 700;
  display: flex;
  align-items: center;
  justify-content: center;
  flex-shrink: 0;
}

.spot-line {
  flex: 1;
  width: 2px;
  min-height: 14px;
  background: var(--primary-soft);
  margin: 3px 0;
}

.spot-name {
  font-size: 14px;
  font-weight: 600;
  color: var(--text);
  padding: 3px 0 17px;
}

.spot-item:last-child .spot-name {
  padding-bottom: 3px;
}

.divider {
  height: 1px;
  background: var(--border-soft);
  margin: 16px 0;
}
</style>
