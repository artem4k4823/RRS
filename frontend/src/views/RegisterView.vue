<template>
  <div class="auth-container">
    <div class="card auth-card">
      <h1 class="title text-center">Register</h1>
      <form @submit.prevent="handleRegister">
        <div class="form-group">
          <label>Username</label>
          <input type="text" v-model="username" required placeholder="Choose a username" />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model="password" required placeholder="Choose a password" />
        </div>
        <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
        <div v-if="successMsg" class="success-msg">{{ successMsg }}</div>
        <button type="submit" class="btn" style="width: 100%; margin-top: 1rem;" :disabled="loading">
          {{ loading ? 'Registering...' : 'Register' }}
        </button>
      </form>
      <div class="text-center mt-4">
        <span style="color: var(--text-muted)">Already have an account? </span>
        <router-link to="/login">Log in</router-link>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const username = ref('')
const password = ref('')
const errorMsg = ref('')
const successMsg = ref('')
const loading = ref(false)

const handleRegister = async () => {
  errorMsg.value = ''
  successMsg.value = ''
  loading.value = true
  try {
    await api.post('/api/user/register_user', {
      username: username.value,
      password: password.value
    })
    successMsg.value = 'Registration successful! Redirecting...'
    setTimeout(() => {
      router.push('/login')
    }, 1500)
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Registration failed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.auth-container {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
  padding: 1rem;
}
.auth-card {
  width: 100%;
  max-width: 400px;
}
.error-msg {
  color: var(--danger-color);
  font-size: 0.875rem;
  margin-top: 0.5rem;
}
.success-msg {
  color: var(--success-color);
  font-size: 0.875rem;
  margin-top: 0.5rem;
}
</style>
