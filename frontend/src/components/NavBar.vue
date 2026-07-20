<template>
  <nav class="navbar">
    <div class="container navbar-container">
      <div class="brand">
        <router-link to="/">RSS Platform</router-link>
      </div>
      <div class="nav-links">
        <router-link to="/">Dashboard</router-link>
        <router-link to="/generator">Generator</router-link>
        <button @click="logout" class="btn btn-secondary logout-btn">Logout</button>
      </div>
    </div>
  </nav>
</template>

<script setup>
import { useRouter } from 'vue-router'

const router = useRouter()

const logout = () => {
  localStorage.removeItem('access_token')
  localStorage.removeItem('refresh_token')
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
