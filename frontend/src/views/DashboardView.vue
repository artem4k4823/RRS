<template>
  <div class="container dashboard">
    <div class="dashboard-header flex items-center justify-between">
      <h1 class="title">My Feed</h1>
      <button @click="showAddSub = true" class="btn" v-if="!showAddSub">Add Subscription</button>
    </div>

    <div v-if="showAddSub" class="card mb-4">
      <form @submit.prevent="handleAddSub" class="flex gap-4 items-center flex-wrap">
        <input type="url" v-model="newSubUrl" placeholder="Enter RSS URL" required style="flex: 1; min-width: 200px;" />
        <input type="text" v-model="newSubName" placeholder="Custom Name" required style="flex: 1; min-width: 150px;" />
        <button type="submit" class="btn" :disabled="subLoading">
          {{ subLoading ? 'Adding...' : 'Subscribe' }}
        </button>
        <button type="button" @click="showAddSub = false" class="btn btn-secondary">Cancel</button>
      </form>
      <div v-if="subError" class="error-msg mt-4">{{ subError }}</div>
    </div>

    <div class="feed-layout">
      <!-- Posts Feed -->
      <div class="posts-section">
        <div v-if="loadingPosts" class="text-muted">Loading your feed...</div>
        <div v-else-if="posts.length === 0" class="text-muted card">
          No posts found. Add a subscription to get started.
        </div>
        <div v-else class="posts-list">
          <div v-for="post in posts" :key="post.id" class="card post-card">
            <h3 class="post-title">
              <a :href="post.link" target="_blank" rel="noopener noreferrer">{{ post.title }}</a>
            </h3>
            <p class="post-meta">{{ new Date(post.published).toLocaleString() }}</p>
            <div class="post-summary" v-html="post.summary"></div>
          </div>
        </div>
      </div>

      <!-- Subscriptions Sidebar -->
      <div class="subs-sidebar">
        <div class="card">
          <h3 class="sidebar-title">My Subscriptions</h3>
          <div v-if="loadingSubs" class="text-muted">Loading...</div>
          <div v-else-if="subscriptions.length === 0" class="text-muted">No subscriptions yet.</div>
          <ul v-else class="subs-list">
            <li v-for="sub in subscriptions" :key="sub.id" class="sub-item">
              <div>
                <strong>{{ sub.custom_name }}</strong>
                <div class="sub-url">{{ sub.url }}</div>
              </div>
              <button @click="handleDeleteSub(sub.id)" class="btn-delete" title="Remove subscription">
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
import { ref, onMounted } from 'vue'
import api from '../services/api'

const posts = ref([])
const subscriptions = ref([])
const loadingPosts = ref(true)
const loadingSubs = ref(true)

const showAddSub = ref(false)
const newSubUrl = ref('')
const newSubName = ref('')
const subLoading = ref(false)
const subError = ref('')

const fetchPosts = async () => {
  try {
    const res = await api.get('/posts/get-all-post')
    posts.value = res.data
  } catch (err) {
    console.error('Failed to load posts', err)
  } finally {
    loadingPosts.value = false
  }
}

const fetchSubs = async () => {
  try {
    const res = await api.get('/subscriptions/get-all-subs')
    subscriptions.value = res.data
  } catch (err) {
    console.error('Failed to load subscriptions', err)
  } finally {
    loadingSubs.value = false
  }
}

const handleAddSub = async () => {
  subError.value = ''
  subLoading.value = true
  try {
    await api.post('/subscriptions/add-subs', { 
      url: newSubUrl.value,
      custom_name: newSubName.value 
    })
    newSubUrl.value = ''
    newSubName.value = ''
    showAddSub.value = false
    await fetchSubs()
    // Optionally fetch posts again or wait for backend worker to parse them
  } catch (err) {
    subError.value = err.response?.data?.detail || 'Failed to add subscription'
  } finally {
    subLoading.value = false
  }
}

const handleDeleteSub = async (id) => {
  if (!confirm('Are you sure you want to remove this subscription?')) return
  try {
    await api.delete(`/subscriptions/delete-sub/${id}`)
    await fetchSubs()
  } catch (err) {
    console.error('Failed to delete sub', err)
  }
}

onMounted(() => {
  fetchPosts()
  fetchSubs()
})
</script>

<style scoped>
.dashboard-header {
  margin-bottom: 2rem;
}

.feed-layout {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 2rem;
  align-items: start;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.post-card {
  padding: 1.5rem;
}

.post-title {
  font-size: 1.25rem;
  font-weight: 600;
  margin-bottom: 0.5rem;
}

.post-title a {
  color: var(--text-main);
}
.post-title a:hover {
  color: var(--primary-color);
}

.post-meta {
  font-size: 0.875rem;
  color: var(--text-muted);
  margin-bottom: 1rem;
}

.post-summary {
  color: var(--text-muted);
  line-height: 1.6;
}

.sidebar-title {
  font-size: 1.125rem;
  font-weight: 600;
  margin-bottom: 1rem;
  color: var(--text-main);
}

.subs-list {
  list-style: none;
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

.error-msg {
  color: var(--danger-color);
  font-size: 0.875rem;
}

@media (max-width: 768px) {
  .feed-layout {
    grid-template-columns: 1fr;
  }
  .subs-sidebar {
    order: -1;
  }
}
</style>
