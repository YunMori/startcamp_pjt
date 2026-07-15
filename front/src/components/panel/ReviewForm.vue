<script setup>
import { reactive } from 'vue'

const props = defineProps({
  mode: { type: String, default: 'write' }, // write | edit
  initial: { type: Object, default: null },
})

const emit = defineEmits(['submit', 'cancel'])

const form = reactive({
  nickname: props.initial?.nickname || '',
  rating: props.initial?.rating || 5,
  text: props.initial?.text || '',
  password: '',
  error: '',
})

function submit() {
  if (!form.nickname.trim() || !form.text.trim() || (props.mode === 'write' && !form.password.trim())) {
    form.error =
      props.mode === 'write'
        ? '닉네임, 내용, 비밀번호를 모두 입력해주세요.'
        : '닉네임과 내용을 입력해주세요.'
    return
  }
  form.error = ''
  emit('submit', {
    nickname: form.nickname.trim(),
    rating: form.rating,
    text: form.text.trim(),
    password: form.password,
  })
}
</script>

<template>
  <div class="form">
    <div class="title">{{ mode === 'edit' ? '리뷰 수정' : '리뷰 작성' }}</div>

    <label>닉네임</label>
    <input v-model="form.nickname" placeholder="익명 닉네임" />

    <label>만족도</label>
    <div class="stars">
      <button
        v-for="n in 5"
        :key="n"
        class="star"
        :class="{ on: form.rating >= n }"
        @click="form.rating = n"
      >
        ★
      </button>
    </div>

    <label>내용</label>
    <textarea v-model="form.text" placeholder="데이트 후기를 남겨주세요"></textarea>

    <label>
      비밀번호
      <span class="hint">{{ mode === 'edit' ? '(변경할 때만 입력)' : '(수정·삭제 시 필요)' }}</span>
    </label>
    <input v-model="form.password" type="password" placeholder="숫자·문자 조합" />

    <div v-if="form.error" class="error">{{ form.error }}</div>

    <div class="actions">
      <button class="btn cancel" @click="emit('cancel')">취소</button>
      <button class="btn submit" @click="submit">{{ mode === 'edit' ? '수정 완료' : '리뷰 등록' }}</button>
    </div>
  </div>
</template>

<style scoped>
.form {
  background: #fff;
  border: 1px solid var(--border-soft);
  border-radius: 16px;
  padding: 16px;
}

.title {
  font-weight: 700;
  font-size: 15px;
  color: var(--text);
  margin-bottom: 14px;
}

label {
  display: block;
  font-size: 12px;
  font-weight: 700;
  color: #8a7679;
  margin: 14px 0 6px;
}

label:first-of-type {
  margin-top: 0;
}

.hint {
  font-weight: 400;
  color: var(--text-faint);
}

input,
textarea {
  width: 100%;
  padding: 11px 13px;
  border: 1.5px solid #eeddd8;
  border-radius: 12px;
  font-size: 14px;
  outline: none;
  color: var(--text);
  background: #fff;
}

input:focus,
textarea:focus {
  border-color: var(--primary-light);
}

textarea {
  min-height: 84px;
  resize: none;
  line-height: 1.5;
}

.stars {
  display: flex;
  gap: 4px;
}

.star {
  font-size: 28px;
  background: none;
  border: none;
  cursor: pointer;
  padding: 0;
  line-height: 1;
  color: var(--star-off);
}

.star.on {
  color: var(--star);
}

.error {
  color: var(--danger);
  font-size: 12px;
  margin-top: 8px;
}

.actions {
  display: flex;
  gap: 8px;
  margin-top: 16px;
}

.btn {
  padding: 12px;
  border-radius: 12px;
  font-weight: 700;
  cursor: pointer;
  font-size: 13px;
}

.cancel {
  flex: 1;
  border: 1.5px solid #eeddd8;
  background: #fff;
  color: var(--text-muted);
}

.submit {
  flex: 2;
  border: none;
  background: var(--gradient);
  color: #fff;
}
</style>
