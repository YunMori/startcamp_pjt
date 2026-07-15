<template>
  <header class="header">
    <div class="row">
      <div class="logo">🍒</div>
      <div class="titles">
        <div class="brand">LocalHub</div>
        <div class="sub">대전·충청 연인 데이트 큐레이터</div>
      </div>
      <div class="status"><span class="dot"></span>러비 온라인</div>
    </div>
  </header>
</template>

<style scoped>
.header {
  padding: max(18px, env(safe-area-inset-top)) 18px 12px;
  background: var(--gradient);
  color: #fff;
  position: relative;
  z-index: 2;
  box-shadow: 0 6px 18px rgba(240, 78, 107, 0.28);
  flex-shrink: 0;
}

.row {
  display: flex;
  align-items: center;
  gap: 10px;
}

.logo {
  width: 40px;
  height: 40px;
  border-radius: 14px;
  background: rgba(255, 255, 255, 0.22);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 22px;
}

.titles {
  line-height: 1.1;
}

.brand {
  font-family: 'Fredoka', sans-serif;
  font-weight: 700;
  font-size: 20px;
  letter-spacing: 0.2px;
}

.sub {
  font-size: 11px;
  opacity: 0.92;
  margin-top: 2px;
  font-weight: 500;
}

.status {
  margin-left: auto;
  display: flex;
  align-items: center;
  gap: 6px;
  background: rgba(255, 255, 255, 0.2);
  padding: 5px 10px;
  border-radius: 20px;
  font-size: 11px;
  font-weight: 600;
}

.dot {
  width: 7px;
  height: 7px;
  border-radius: 50%;
  background: #7cf6b0;
  box-shadow: 0 0 6px #7cf6b0;
}
</style>
