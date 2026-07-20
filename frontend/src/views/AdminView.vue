<template>
  <div class="container admin-panel">
    <h1 class="title">Admin Dashboard</h1>
    
    <div class="card mb-4">
      <h3 style="margin-bottom: 1rem; color: var(--text-main);">User Management</h3>
      <p style="color: var(--text-muted); margin-bottom: 1.5rem;">
        Search for a user by their ID to manage their account.
      </p>

      <form @submit.prevent="searchUser" class="flex gap-4 items-center mb-4">
        <input type="number" v-model="searchId" placeholder="Enter User ID" required style="max-width: 200px;" />
        <button type="submit" class="btn" :disabled="loading">
          {{ loading ? 'Searching...' : 'Search' }}
        </button>
      </form>

      <div v-if="errorMsg" class="error-msg">{{ errorMsg }}</div>

      <div v-if="user" class="table-responsive mt-4">
        <table class="admin-table">
          <thead>
            <tr>
              <th>Username</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>{{ user.username }}</td>
              <td>
                <span :class="user.status ? 'status-active' : 'status-banned'">
                  {{ user.status ? 'Active' : 'Banned' }}
                </span>
              </td>
              <td class="actions">
                <button 
                  v-if="user.status" 
                  @click="banUser(searchId)" 
                  class="btn btn-danger btn-sm">
                  Ban
                </button>
                <button 
                  v-else 
                  @click="unbanUser(searchId)" 
                  class="btn btn-secondary btn-sm">
                  Unban
                </button>
              </td>
            </tr>
          </tbody>
        </table>

        <!-- User Subscriptions -->
        <div class="mt-4" style="margin-top: 2rem;">
          <h4 style="margin-bottom: 1rem; color: var(--text-main);">User Subscriptions</h4>
          <div v-if="!user.subscriptions || user.subscriptions.length === 0" class="text-muted">
            This user has no subscriptions.
          </div>
          <ul v-else class="subs-list">
            <li v-for="sub in user.subscriptions" :key="sub.id" class="sub-item">
              <div>
                <strong>{{ sub.custom_name }}</strong>
                <div class="sub-url">{{ sub.url }}</div>
              </div>
              <button @click="deleteSub(searchId, sub.id)" class="btn-delete" title="Delete subscription">
                &times;
              </button>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../services/api'

const searchId = ref('')
const user = ref(null)
const loading = ref(false)
const errorMsg = ref('')

const searchUser = async () => {
  if (!searchId.value) return
  loading.value = true
  errorMsg.value = ''
  user.value = null
  try {
    const res = await api.get(`/admin-operations/get-users-with-subs?user_id=${searchId.value}`)
    user.value = res.data
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'User not found or you lack permissions.'
  } finally {
    loading.value = false
  }
}

const banUser = async (id) => {
  if (!confirm('Are you sure you want to ban this user?')) return
  try {
    await api.patch(`/admin-operations/ban-user?user_id=${id}`)
    await searchUser()
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Failed to ban user'
  }
}

const unbanUser = async (id) => {
  if (!confirm('Are you sure you want to unban this user?')) return
  try {
    await api.patch(`/admin-operations/unban-user?user_id=${id}`)
    await searchUser()
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Failed to unban user'
  }
}

const deleteSub = async (userId, subId) => {
  if (!confirm('Are you sure you want to delete this subscription?')) return
  try {
    await api.delete(`/admin-operations/delete-user-sub?user_id=${userId}&sub_id=${subId}`)
    await searchUser() // Refresh data
  } catch (err) {
    errorMsg.value = err.response?.data?.detail || 'Failed to delete subscription'
  }
}
</script>

<style scoped>
.admin-table {
  width: 100%;
  border-collapse: collapse;
}

.admin-table th, .admin-table td {
  padding: 1rem;
  text-align: left;
  border-bottom: 1px solid var(--border-color);
}

.admin-table th {
  font-weight: 600;
  color: var(--text-muted);
}

.status-active {
  color: var(--success-color);
  font-weight: 500;
}

.status-banned {
  color: var(--danger-color);
  font-weight: 500;
}

.btn-sm {
  padding: 0.25rem 0.75rem;
  font-size: 0.875rem;
}

.table-responsive {
  overflow-x: auto;
}

.actions {
  display: flex;
  gap: 0.5rem;
}

.error-msg {
  color: var(--danger-color);
  margin-top: 1rem;
}

.subs-list {
  list-style: none;
  padding: 0;
}

.sub-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border-color);
}

.sub-item:last-child {
  border-bottom: none;
}

.sub-url {
  font-size: 0.875rem;
  color: var(--text-muted);
  word-break: break-all;
  padding-right: 1rem;
}

.btn-delete {
  background: none;
  color: var(--danger-color);
  font-size: 1.25rem;
  padding: 0.25rem;
}
.btn-delete:hover {
  color: #b91c1c;
}
</style>
