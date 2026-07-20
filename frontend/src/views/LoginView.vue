<template>
  <div class="auth-container">
    <div class="card auth-card">
      <h1 class="title text-center">Login</h1>
      <form @submit.prevent="handleLogin">
        <div class="form-group">
          <label>Username</label>
          <input type="text" v-model="username" required placeholder="Enter your username" />
        </div>
        <div class="form-group">
          <label>Password</label>
          <input type="password" v-model="password" required placeholder="Enter your password" />
        </div>
        <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>
        <button type="submit" class="btn" style="width: 100%; margin-top: 1rem;" :disabled="loading">
          {{ loading ? 'Logging in...' : 'Log in' }}
        </button>
      </form>
      <div class="text-center mt-4">
        <span style="color: var(--text-muted)">Don't have an account? </span>
        <router-link to="/register">Register here</router-link>
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
const loading = ref(false)

const handleLogin = async () => {
  errorMsg.value = ''
  loading.value = true
  try {
    const res = await api.post('/auth/login', {
      username: username.value,
      password: password.value
    })
    
    if (res.data && res.data.access_token) {
      localStorage.setItem('access_token', res.data.access_token)
      if (res.data.refresh_token) {
        localStorage.setItem('refresh_token', res.data.refresh_token)
      }
      
      const userRes = await api.get('/auth/me')
      if (userRes.data?.isAdmin) {
        // Admin gets redirected to dashboard, but has access to admin panel
      }
      router.push('/')
    }
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Failed to login'
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
</style>
