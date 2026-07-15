<script setup>
import { ref } from 'vue'
import { useChatStore } from '../stores/useChatStore'

const { state, sendChat } = useChatStore()
const input = ref('')

function submit() {
  if (!input.value.trim() || state.sending) return
  sendChat(input.value)
  input.value = ''
}
</script>

<template>
  <div class="bar">
    <input
      v-model="input"
      placeholder="러비에게 자유롭게 물어보세요…"
      @keydown.enter.prevent="submit"
    />
    <button class="send" :disabled="state.sending" @click="submit">
      <svg width="18" height="18" viewBox="0 0 24 24" fill="none">
        <path d="M4 12l16-8-6 16-3-6-7-2z" fill="#fff" />
      </svg>
    </button>
  </div>
</template>

<style scoped>
.bar {
  padding: 10px 14px max(14px, env(safe-area-inset-bottom));
  background: #fff;
  border-top: 1px solid var(--border);
  display: flex;
  align-items: center;
  gap: 9px;
  position: relative;
  z-index: 2;
  flex-shrink: 0;
}

input {
  flex: 1;
  background: var(--input-bg);
  border: none;
  border-radius: 22px;
  padding: 12px 16px;
  color: var(--text);
  font-size: 13px;
  outline: none;
}

input:focus {
  background: #fcede7;
}

.send {
  width: 42px;
  height: 42px;
  border: none;
  border-radius: 50%;
  background: var(--gradient);
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 4px 12px rgba(240, 78, 107, 0.35);
  cursor: pointer;
  flex-shrink: 0;
}

.send:hover {
  filter: brightness(0.96);
}

.send:disabled {
  opacity: 0.6;
  cursor: default;
}
</style>
