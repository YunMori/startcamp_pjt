<template>
  <div class="row">
    <div class="avatar">🍒</div>
    <div class="bubble">
      <span class="dot"></span>
      <span class="dot d2"></span>
      <span class="dot d3"></span>
    </div>
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
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 4px 18px 18px 18px;
  padding: 14px 16px;
  display: flex;
  gap: 5px;
}

.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #f5a9b8;
  animation: blink 1.2s infinite;
}

.d2 {
  animation-delay: 0.2s;
}

.d3 {
  animation-delay: 0.4s;
}
</style>
