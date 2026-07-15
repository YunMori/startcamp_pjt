<script setup>
defineProps({ text: { type: String, default: '' } })
</script>

<template>
  <div class="row">
    <div class="avatar">🍒</div>
    <div class="bubble"><slot>{{ text }}</slot></div>
  </div>
</template>

<style scoped>
.row {
  display: flex;
  gap: 8px;
  align-items: flex-end;
  animation: msgIn 0.28s ease;
}

.avatar {
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: var(--gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  flex-shrink: 0;
}

.bubble {
  max-width: 78%;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 4px 18px 18px 18px;
  padding: 11px 14px;
  font-size: 14px;
  line-height: 1.55;
  color: var(--text);
  box-shadow: 0 2px 8px rgba(60, 20, 30, 0.05);
}
</style>
