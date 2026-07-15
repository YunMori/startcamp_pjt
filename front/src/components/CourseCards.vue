<script setup>
import { computed } from 'vue'
import CourseCard from './CourseCard.vue'
import { COURSES } from '../data/courses'

const props = defineProps({
  // 추천 API가 돌려준 코스 ID 목록 (kind: 'cards' 메시지)
  courseIds: { type: Array, default: () => [] },
})

const courses = computed(() =>
  props.courseIds
    .map((id) => COURSES.find((c) => c.id === id))
    .filter(Boolean),
)
</script>

<template>
  <div class="cards">
    <CourseCard v-for="course in courses" :key="course.id" :course="course" />
  </div>
</template>

<style scoped>
.cards {
  display: flex;
  flex-direction: column;
  gap: 13px;
  animation: msgIn 0.28s ease;
  padding-left: 2px;
}
</style>
