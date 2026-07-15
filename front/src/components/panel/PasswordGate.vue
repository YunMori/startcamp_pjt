<script setup>
import { ref } from 'vue'

defineProps({
  title: { type: String, required: true }, // 예: '리뷰 수정' | '리뷰 삭제'
  error: { type: Boolean, default: false },
})

const emit = defineEmits(['confirm', 'close'])
const password = ref('')
</script>

<template>
  <div class="overlay" @click.self="emit('close')">
    <div class="modal">
      <div class="title">🔒 {{ title }}</div>
      <div class="sub">작성 시 입력한 비밀번호를 넣어주세요.</div>
      <input
        v-model="password"
        type="password"
        placeholder="비밀번호"
        @keydown.enter="emit('confirm', password)"
      />
      <div v-if="error" class="error">비밀번호가 일치하지 않아요.</div>
      <div class="actions">
        <button class="btn cancel" @click="emit('close')">취소</button>
        <button class="btn confirm" @click="emit('confirm', password)">확인</button>
      </div>
    </div>
  </div>
</template>

<style scoped>
.overlay {
  position: absolute;
  inset: 0;
  background: rgba(50, 25, 30, 0.4);
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 24px;
}

.modal {
  background: #fff;
  border-radius: 18px;
  padding: 20px;
  width: 100%;
  max-width: 280px;
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.25);
}

.title {
  font-weight: 700;
  font-size: 15px;
  color: var(--text);
  margin-bottom: 4px;
}

.sub {
  font-size: 12px;
  color: var(--text-muted);
  margin-bottom: 12px;
}

input {
  width: 100%;
  padding: 11px 13px;
  border: 1.5px solid #eeddd8;
  border-radius: 12px;
  font-size: 14px;
  outline: none;
  color: var(--text);
}

input:focus {
  border-color: var(--primary-light);
}

.error {
  color: var(--danger);
  font-size: 12px;
  margin-top: 6px;
}

.actions {
  display: flex;
  gap: 8px;
  margin-top: 14px;
}

.btn {
  flex: 1;
  padding: 11px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  font-size: 13px;
}

.cancel {
  border: 1.5px solid #eeddd8;
  background: #fff;
  color: var(--text-muted);
}

.confirm {
  border: none;
  background: var(--gradient);
  color: #fff;
}
</style>
