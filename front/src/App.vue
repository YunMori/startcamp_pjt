<script setup>
import ChatHeader from './components/ChatHeader.vue'
import ChatMessageList from './components/ChatMessageList.vue'
import ChatInput from './components/ChatInput.vue'
import SidePanel from './components/panel/SidePanel.vue'
</script>

<template>
  <div class="stage">
    <div class="phone">
      <ChatHeader />
      <ChatMessageList />
      <ChatInput />
      <SidePanel />
    </div>
  </div>
</template>

<style scoped>
.stage {
  height: 100%;
  display: flex;
  align-items: center;
  justify-content: center;
}

.phone {
  position: relative;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  background: var(--bg);
  /* hidden 대신 clip: 닫힌 바텀시트가 만드는 오버플로를 포커스/JS 스크롤로도 못 움직이게 */
  overflow: hidden;
  overflow: clip;
}

/* 데스크톱에서는 폰 프레임 형태로 중앙 배치 */
@media (min-width: 520px) {
  .stage {
    padding: 28px;
  }
  .phone {
    max-width: 430px;
    max-height: 874px;
    border-radius: 40px;
    box-shadow: 0 24px 60px rgba(60, 20, 30, 0.25);
    border: 1px solid rgba(255, 255, 255, 0.6);
  }
}
</style>
