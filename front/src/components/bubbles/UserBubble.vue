<script setup>
defineProps({ text: { type: String, required: true } })
</script>

<template>
  <div class="row">
    <div class="bubble">{{ text }}</div>
  </div>
</template>

<style scoped>
.row {
  display: flex;
  justify-content: flex-end;
  animation: msgIn 0.28s ease;
}

.bubble {
  max-width: 78%;
  background: var(--gradient-bubble);
  color: #fff;
  border-radius: 18px 4px 18px 18px;
  padding: 11px 14px;
  font-size: 14px;
  line-height: 1.55;
  box-shadow: 0 4px 12px rgba(240, 78, 107, 0.25);
}
</style>
