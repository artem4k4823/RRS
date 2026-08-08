<template>
  <div class="container admin-panel">
    <h1 class="title mb-4">Admin Dashboard</h1>

    <!-- Tabs Navigation -->
    <div class="admin-tabs flex gap-4 mb-4">
      <button 
        :class="['btn', activeTab === 'users' ? 'btn-primary' : 'btn-secondary']"
        @click="activeTab = 'users'">
        User Management
      </button>
      <button 
        :class="['btn', activeTab === 'optionals' ? 'btn-primary' : 'btn-secondary']"
        @click="activeTab = 'optionals'">
        Optional RSS Feeds
      </button>
    </div>

    <!-- Error message alert -->
    <div v-if="errorMsg" class="error-msg card mb-4">{{ errorMsg }}</div>
    <div v-if="successMsg" class="success-msg card mb-4">{{ successMsg }}</div>

    <!-- TAB 1: USER MANAGEMENT -->
    <div v-if="activeTab === 'users'" class="card mb-4">
      <div class="flex items-center justify-between mb-4 flex-wrap gap-4">
        <div>
          <h3 style="color: var(--text-main);">Registered Users</h3>
          <p style="color: var(--text-muted); font-size: 0.875rem;">
            Total users: {{ users.length }}
          </p>
        </div>
        <input 
          type="text" 
          v-model="searchQuery" 
          placeholder="Search by ID or Username..." 
          style="max-width: 250px;" 
        />
      </div>

      <div v-if="loadingUsers" class="text-muted">Loading user list...</div>
      <div v-else-if="filteredUsers.length === 0" class="text-muted">No users found.</div>
      <div v-else class="table-responsive">
        <table class="admin-table">
          <thead>
            <tr>
              <th>ID</th>
              <th>Username</th>
              <th>Role</th>
              <th>Status</th>
              <th>Actions</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in filteredUsers" :key="u.id || u.username">
              <td>#{{ u.id ?? 'N/A' }}</td>
              <td>
                <strong>{{ u.username }}</strong>
              </td>
              <td>
                <span :class="u.isAdmin ? 'badge-admin' : 'badge-user'">
                  {{ u.isAdmin ? 'Admin' : 'User' }}
                </span>
              </td>
              <td>
                <span :class="u.status ? 'status-active' : 'status-banned'">
                  {{ u.status ? 'Active' : 'Banned' }}
                </span>
              </td>
              <td class="actions">
                <button 
                  v-if="u.id"
                  @click="viewUserSubs(u.id)" 
                  class="btn btn-secondary btn-sm"
                  title="View Subscriptions">
                  Subscriptions
                </button>

                <button 
                  v-if="u.status && !u.isAdmin && u.id" 
                  @click="banUser(u.id)" 
                  class="btn btn-danger btn-sm">
                  Ban
                </button>
                <button 
                  v-else-if="!u.status && !u.isAdmin && u.id" 
                  @click="unbanUser(u.id)" 
                  class="btn btn-secondary btn-sm">
                  Unban
                </button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Selected User Subscriptions Panel -->
      <div v-if="selectedUser" class="mt-4 user-subs-panel card">
        <div class="flex items-center justify-between mb-4">
          <h4 style="color: var(--text-main);">
            Subscriptions for User: <strong>{{ selectedUser.username }}</strong> (ID: {{ selectedUser.id }})
          </h4>
          <button @click="selectedUser = null" class="btn btn-secondary btn-sm">&times; Close</button>
        </div>

        <div v-if="loadingUserSubs" class="text-muted">Loading subscriptions...</div>
        <div v-else-if="!selectedUser.subscriptions || selectedUser.subscriptions.length === 0" class="text-muted">
          This user has no active subscriptions.
        </div>
        <ul v-else class="subs-list">
          <li v-for="sub in selectedUser.subscriptions" :key="sub.id" class="sub-item">
            <div>
              <strong>{{ sub.custom_name }}</strong>
              <div class="sub-url">{{ sub.url }}</div>
            </div>
            <button @click="deleteUserSub(selectedUser.id, sub.id)" class="btn-delete" title="Delete subscription">
              &times; Remove
            </button>
          </li>
        </ul>
      </div>
    </div>

    <!-- TAB 2: OPTIONAL RSS FEEDS MANAGEMENT -->
    <div v-if="activeTab === 'optionals'" class="card">
      <div class="flex items-center justify-between mb-4 flex-wrap gap-4">
        <div>
          <h3 style="color: var(--text-main);">Optional RSS Feeds List</h3>
          <p style="color: var(--text-muted); font-size: 0.875rem;">
            Recommended feed list accessible to all users for quick one-click subscription.
          </p>
        </div>
        <button @click="showAddOptional = !showAddOptional" class="btn">
          {{ showAddOptional ? 'Cancel' : '+ Add Optional Feed' }}
        </button>
      </div>

      <!-- Add Optional Feed Form -->
      <div v-if="showAddOptional" class="card mb-4" style="background-color: var(--bg-color);">
        <h4 style="margin-bottom: 1rem; color: var(--text-main);">Add New Optional Feed</h4>
        <form @submit.prevent="handleAddOptional" class="flex flex-col gap-4">
          <input type="text" v-model="newOptionalName" placeholder="Feed Name (e.g. Habr News)" required />
          <input type="text" v-model="newOptionalDesc" placeholder="Short Description" required />
          <input type="url" v-model="newOptionalUrl" placeholder="Feed RSS URL" required />
          <button type="submit" class="btn" :disabled="submittingOptional" style="align-self: flex-start;">
            {{ submittingOptional ? 'Saving...' : 'Add Feed' }}
          </button>
        </form>
      </div>

      <!-- Optional Feeds List -->
      <div v-if="loadingOptionals" class="text-muted">Loading optional feeds...</div>
      <div v-else-if="optionalFeeds.length === 0" class="text-muted">No optional feeds configured yet.</div>
      <ul v-else class="subs-list">
        <li v-for="feed in optionalFeeds" :key="feed.id || feed.url" class="sub-item">
          <div>
            <strong>{{ feed.name }}</strong>
            <p style="font-size: 0.875rem; color: var(--text-muted); margin: 0.25rem 0;">{{ feed.description }}</p>
            <div class="sub-url">{{ feed.url }}</div>
          </div>
          <button 
            v-if="feed.id" 
            @click="deleteOptionalFeed(feed.id)" 
            class="btn btn-danger btn-sm"
            title="Delete Optional Feed">
            Delete
          </button>
        </li>
      </ul>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

const activeTab = ref('users')
const users = ref([])
const loadingUsers = ref(false)
const searchQuery = ref('')

const selectedUser = ref(null)
const loadingUserSubs = ref(false)

const optionalFeeds = ref([])
const loadingOptionals = ref(false)
const showAddOptional = ref(false)
const newOptionalName = ref('')
const newOptionalDesc = ref('')
const newOptionalUrl = ref('')
const submittingOptional = ref(false)

const errorMsg = ref('')
const successMsg = ref('')

const showMessage = (msg, isError = false) => {
  if (isError) {
    errorMsg.value = msg
    successMsg.value = ''
  } else {
    successMsg.value = msg
    errorMsg.value = ''
  }
  setTimeout(() => {
    errorMsg.value = ''
    successMsg.value = ''
  }, 4000)
}

// Fetch all users
const fetchUsers = async () => {
  loadingUsers.value = true
  try {
    const res = await api.get('/admin-operations/get-all-users')
    users.value = res.data
  } catch (err) {
    showMessage(err.response?.data?.detail || 'Failed to fetch users', true)
  } finally {
    loadingUsers.value = false
  }
}

const filteredUsers = computed(() => {
  if (!searchQuery.value) return users.value
  const q = searchQuery.value.toLowerCase().trim()
  return users.value.filter(u => 
    (u.id && String(u.id).includes(q)) || 
    (u.username && u.username.toLowerCase().includes(q))
  )
})

// Ban User
const banUser = async (userId) => {
  if (!confirm('Are you sure you want to ban this user?')) return
  try {
    await api.patch(`/admin-operations/ban-user?user_id=${userId}`)
    showMessage('User banned successfully.')
    await fetchUsers()
  } catch (err) {
    showMessage(err.response?.data?.detail || 'Failed to ban user', true)
  }
}

// Unban User
const unbanUser = async (userId) => {
  if (!confirm('Are you sure you want to unban this user?')) return
  try {
    await api.patch(`/admin-operations/unban-user?user_id=${userId}`)
    showMessage('User unbanned successfully.')
    await fetchUsers()
  } catch (err) {
    showMessage(err.response?.data?.detail || 'Failed to unban user', true)
  }
}

// View subscriptions for a user
const viewUserSubs = async (userId) => {
  loadingUserSubs.value = true
  selectedUser.value = null
  try {
    const res = await api.get(`/admin-operations/get-users-with-subs?user_id=${userId}`)
    selectedUser.value = res.data
  } catch (err) {
    showMessage(err.response?.data?.detail || 'Failed to fetch user subscriptions', true)
  } finally {
    loadingUserSubs.value = false
  }
}

// Delete subscription of user
const deleteUserSub = async (userId, subId) => {
  if (!confirm('Are you sure you want to delete this subscription?')) return
  try {
    await api.delete(`/admin-operations/delete-user-sub?user_id=${userId}&sub_id=${subId}`)
    showMessage('Subscription deleted successfully.')
    await viewUserSubs(userId)
  } catch (err) {
    showMessage(err.response?.data?.detail || 'Failed to delete user subscription', true)
  }
}

// Fetch optional feeds list
const fetchOptionalFeeds = async () => {
  loadingOptionals.value = true
  try {
    const res = await api.get('/optional_url_list/get-all-optionals-urls')
    optionalFeeds.value = res.data
  } catch (err) {
    showMessage(err.response?.data?.detail || 'Failed to fetch optional feeds', true)
  } finally {
    loadingOptionals.value = false
  }
}

// Add Optional Feed
const handleAddOptional = async () => {
  submittingOptional.value = true
  try {
    await api.post('/optional_url_list/add-url-to-optional', {
      name: newOptionalName.value,
      description: newOptionalDesc.value,
      url: newOptionalUrl.value
    })
    showMessage('Optional RSS feed added successfully.')
    newOptionalName.value = ''
    newOptionalDesc.value = ''
    newOptionalUrl.value = ''
    showAddOptional.value = false
    await fetchOptionalFeeds()
  } catch (err) {
    showMessage(err.response?.data?.detail || 'Failed to add optional feed', true)
  } finally {
    submittingOptional.value = false
  }
}

// Delete Optional Feed
const deleteOptionalFeed = async (urlId) => {
  if (!confirm('Are you sure you want to delete this optional feed?')) return
  try {
    await api.delete(`/optional_url_list/delete-optional-url?url_id=${urlId}`)
    showMessage('Optional feed deleted successfully.')
    await fetchOptionalFeeds()
  } catch (err) {
    showMessage(err.response?.data?.detail || 'Failed to delete optional feed', true)
  }
}

onMounted(() => {
  fetchUsers()
  fetchOptionalFeeds()
})
</script>

<style scoped>
.admin-tabs {
  border-bottom: 1px solid var(--border-color);
  padding-bottom: 0.5rem;
}

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
  font-weight: 600;
}

.status-banned {
  color: var(--danger-color);
  font-weight: 600;
}

.badge-admin {
  background-color: rgba(99, 102, 241, 0.15);
  color: #6366f1;
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
  font-weight: 600;
}

.badge-user {
  background-color: rgba(156, 163, 175, 0.15);
  color: var(--text-muted);
  padding: 0.2rem 0.5rem;
  border-radius: 4px;
  font-size: 0.75rem;
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
  border-left: 4px solid var(--danger-color);
}

.success-msg {
  color: var(--success-color);
  border-left: 4px solid var(--success-color);
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
  font-size: 0.875rem;
  padding: 0.25rem 0.5rem;
  cursor: pointer;
}
.btn-delete:hover {
  text-decoration: underline;
}

.user-subs-panel {
  border: 1px solid var(--border-color);
  background-color: var(--bg-color);
}
</style>
