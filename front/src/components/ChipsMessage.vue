<script setup>
import { useChatStore } from '../stores/useChatStore'

const props = defineProps({
  message: { type: Object, required: true },
})

const { answer } = useChatStore()

function chipClass(label) {
  if (!props.message.answered) return 'chip'
  return props.message.selected === label ? 'chip selected' : 'chip disabled'
}
</script>

<template>
  <div class="row">
    <div class="avatar">🍒</div>
    <div class="bubble">
      <div class="question">{{ message.text }}</div>
      <div class="chips">
        <button
          v-for="label in message.chips"
          :key="label"
          :class="chipClass(label)"
          :disabled="message.answered"
          @click="answer(message.id, label)"
        >
          {{ label }}
        </button>
      </div>
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
  max-width: 84%;
  background: #fff;
  border: 1px solid var(--border);
  border-radius: 4px 18px 18px 18px;
  padding: 12px 14px;
  box-shadow: 0 2px 8px rgba(60, 20, 30, 0.05);
}

.question {
  font-size: 14px;
  line-height: 1.55;
  color: var(--text);
  margin-bottom: 11px;
}

.chips {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.chip {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  padding: 9px 14px;
  border-radius: 20px;
  font-size: 13.5px;
  font-weight: 600;
  transition: all 0.15s;
  border: 1.5px solid var(--primary-soft);
  background: #fff;
  color: var(--primary);
  cursor: pointer;
}

.chip:not(.selected):not(.disabled):hover {
  filter: brightness(0.97);
}

.chip.selected {
  border-color: transparent;
  background: var(--gradient-bubble);
  color: #fff;
  cursor: default;
  box-shadow: 0 4px 12px rgba(240, 78, 107, 0.3);
}

.chip.disabled {
  border-color: #efe2de;
  background: #f7eeeb;
  color: var(--text-faint);
  cursor: default;
}
</style>
