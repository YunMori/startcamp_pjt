<script setup>
import { nextTick, ref, watch } from 'vue'
import { useChatStore } from '../stores/useChatStore'
import BotBubble from './bubbles/BotBubble.vue'
import UserBubble from './bubbles/UserBubble.vue'
import TypingIndicator from './bubbles/TypingIndicator.vue'
import ChipsMessage from './ChipsMessage.vue'
import CourseCards from './CourseCards.vue'

const { state } = useChatStore()
const listEl = ref(null)

watch(
  () => state.messages.length,
  async () => {
    await nextTick()
    if (listEl.value) listEl.value.scrollTop = listEl.value.scrollHeight
  },
  { immediate: true },
)
</script>

<template>
  <div ref="listEl" class="list">
    <template v-for="m in state.messages" :key="m.id">
      <BotBubble v-if="m.role === 'bot' && m.kind === 'text'" :text="m.text" />
      <UserBubble v-else-if="m.role === 'user'" :text="m.text" />
      <TypingIndicator v-else-if="m.kind === 'typing'" />
      <ChipsMessage v-else-if="m.kind === 'chips'" :message="m" />
      <CourseCards v-else-if="m.kind === 'cards'" :course-ids="m.courseIds" />
    </template>
  </div>
</template>

<style scoped>
.list {
  flex: 1;
  min-height: 0;
  overflow-y: auto;
  padding: 18px 14px 16px;
  display: flex;
  flex-direction: column;
  gap: 14px;
}
</style>
