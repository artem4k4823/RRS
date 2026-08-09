<template>
  <header class="navbar">
    <div class="container navbar-container">
      <div class="brand">
        <router-link to="/" class="brand-link">
          <span class="brand-text">RSS Platform</span>
        </router-link>
      </div>
      <div class="nav-links">
        <router-link to="/">Dashboard</router-link>
        <router-link to="/generator">Generator</router-link>
        <router-link v-if="isAdmin" to="/admin" class="admin-link">Admin Panel</router-link>
        <button @click="logout" class="btn btn-secondary logout-btn">Logout</button>
      </div>
    </div>
  </header>
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
  background: rgba(26, 35, 54, 0.85);
  backdrop-filter: blur(12px);
  border-bottom: 1px solid var(--border-color);
  position: sticky;
  top: 0;
  z-index: 100;
}

.navbar-container {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 0.85rem;
  padding-bottom: 0.85rem;
}

.brand-link {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  font-size: 1.25rem;
  font-weight: 800;
  color: var(--text-main);
  letter-spacing: -0.01em;
}

.brand-icon {
  font-size: 1.35rem;
}

.nav-links {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.nav-links a {
  font-weight: 600;
  font-size: 0.925rem;
  color: var(--text-muted);
  padding: 0.35rem 0.65rem;
  border-radius: 6px;
  transition: all 0.2s ease;
}

.nav-links a.router-link-active,
.nav-links a:hover {
  color: #fff;
  background: rgba(255, 255, 255, 0.06);
}

.nav-links a.router-link-active {
  color: var(--primary-color);
}

.admin-link {
  color: #818cf8 !important;
}

.logout-btn {
  padding: 0.45rem 1rem;
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .nav-links {
    gap: 0.75rem;
  }
  .brand-text {
    display: none;
  }
}
</style>
