<template>
  <nav class="navbar">
    <div class="container navbar-container">
      <div class="brand">
        <router-link to="/">RSS Platform</router-link>
      </div>
      <div class="nav-links">
        <router-link to="/">Dashboard</router-link>
        <router-link to="/generator">Generator</router-link>
        <router-link v-if="isAdmin" to="/admin">Admin Panel</router-link>
        <button @click="logout" class="btn btn-secondary logout-btn">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import api from '../services/api'

const router = useRouter()
const isAdmin = ref(false)

const checkUserAdmin = async () => {
  try {
    const token = localStorage.getItem('access_token')
    if (token) {
      const res = await api.get('/auth/me')
      isAdmin.value = !!res.data?.isAdmin
    }
  } catch (e) {
    isAdmin.value = false
  }
}

onMounted(() => {
  checkUserAdmin()
})

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
  isAdmin.value = false
  router.push('/login')
}
</script>

<style scoped>
.navbar {
  background-color: var(--surface-color);
  border-bottom: 1px solid var(--border-color);
  padding: 0.5rem 0;
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.5rem;
  padding-bottom: 0.5rem;
}

.brand a {
  font-size: 1.25rem;
  font-weight: 700;
  color: var(--text-main);
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-links a {
  font-weight: 500;
  color: var(--text-muted);
}

.nav-links a.router-link-active,
.nav-links a:hover {
  color: var(--primary-color);
}

.logout-btn {
  padding: 0.5rem 1rem;
}

@media (max-width: 768px) {
  .nav-links {
    gap: 1rem;
  }
}
</style>
