<script setup>
import CourseCard from './CourseCard.vue'
import { COURSES } from '../data/courses'
</script>

<template>
  <div class="cards">
    <CourseCard v-for="course in COURSES" :key="course.id" :course="course" />
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
