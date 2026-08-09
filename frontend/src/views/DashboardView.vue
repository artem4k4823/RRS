<template>
  <div class="container dashboard">
    <div class="dashboard-header flex items-center justify-between mb-6 flex-wrap gap-4">
      <div>
        <h1 class="title">My Feed</h1>
        <p class="text-muted" style="font-size: 0.9rem;">Latest articles and updates from your subscribed RSS sources</p>
      </div>
      <button @click="showAddSub = !showAddSub" class="btn btn-accent">
        {{ showAddSub ? 'Close Form' : '+ Add Subscription' }}
      </button>
    </div>

    <!-- Add Subscription Form Card -->
    <div v-if="showAddSub" class="card mb-6" style="border-left: 4px solid var(--accent-color);">
      <h3 style="margin-bottom: 1rem; color: var(--text-main); font-size: 1.1rem;">Subscribe to a Custom RSS Link</h3>
      <form @submit.prevent="handleAddSub" class="flex gap-4 items-center flex-wrap">
        <input type="url" v-model="newSubUrl" placeholder="https://example.com/rss.xml" required style="flex: 2; min-width: 240px;" />
        <input type="text" v-model="newSubName" placeholder="Source Title" required style="flex: 1; min-width: 160px;" />
        <button type="submit" class="btn" :disabled="subLoading">
          {{ subLoading ? 'Adding...' : 'Subscribe' }}
        </button>
      </form>
      <div v-if="subError" class="error-msg mt-4">{{ subError }}</div>
    </div>

    <div class="feed-layout">
      <!-- Main Posts Feed Section -->
      <div class="posts-section">
        <div v-if="loadingPosts" class="card text-center text-muted">
          Loading your personalized feed...
        </div>
        <div v-else-if="posts.length === 0" class="card text-center empty-feed-card">
          <h3 style="color: var(--text-main); margin-bottom: 0.5rem;">No posts found</h3>
          <p class="text-muted" style="max-width: 400px; margin: 0 auto 1.5rem auto;">
            Your feed is currently empty. Subscribe to custom RSS URLs or select recommended sources on the right.
          </p>
        </div>
        <div v-else class="posts-list">
          <article v-for="post in posts" :key="post.id || post.link" class="card post-card">
            <h2 class="post-title">
              <a :href="post.link" target="_blank" rel="noopener noreferrer">{{ post.title }}</a>
            </h2>
            <div class="post-meta">
              <span class="post-date">{{ formatDate(post) }}</span>
            </div>
            <div class="post-summary" v-html="post.summary"></div>
          </article>
        </div>
      </div>

      <!-- Subscriptions & Favorites Sidebar Section -->
      <aside class="subs-sidebar">
        <!-- My Subscriptions Card -->
        <div class="card sidebar-card">
          <div class="flex items-center justify-between mb-4">
            <h3 class="sidebar-title">My Subscriptions</h3>
            <span class="badge badge-user">{{ subscriptions.length }}</span>
          </div>
          <div v-if="loadingSubs" class="text-muted" style="font-size: 0.875rem;">Loading...</div>
          <div v-else-if="subscriptions.length === 0" class="text-muted" style="font-size: 0.875rem;">
            No subscriptions added yet.
          </div>
          <ul v-else class="subs-list">
            <li v-for="sub in subscriptions" :key="sub.id" class="sub-item">
              <div class="sub-info">
                <strong class="sub-name">{{ sub.custom_name }}</strong>
                <div class="sub-url" :title="sub.url">{{ sub.url }}</div>
              </div>
              <button @click="handleDeleteSub(sub.id)" class="btn-delete" title="Remove subscription">
                &times;
              </button>
            </li>
          </ul>
        </div>

        <!-- Favorite Feeds Card -->
        <div class="card sidebar-card">
          <div class="flex items-center justify-between mb-4">
            <h3 class="sidebar-title flex items-center gap-2">
              <span>❤️</span> Favorite Feeds
            </h3>
            <span class="badge badge-favorite">{{ favorites.length }}</span>
          </div>
          <div v-if="loadingFavorites" class="text-muted" style="font-size: 0.875rem;">Loading favorites...</div>
          <div v-else-if="favorites.length === 0" class="text-muted" style="font-size: 0.875rem;">
            No favorites added yet. Click ❤️ on recommended feeds below!
          </div>
          <ul v-else class="subs-list">
            <li v-for="fav in favorites" :key="fav.id" class="sub-item">
              <div class="sub-info" v-if="fav.optional_url">
                <strong class="sub-name">{{ fav.optional_url.name }}</strong>
                <div class="sub-desc" v-if="fav.optional_url.description">{{ fav.optional_url.description }}</div>
              </div>
              <div class="flex items-center gap-2 flex-shrink-0">
                <button v-if="fav.optional_url" @click="subscribeToOptional(fav.optional_url)" class="btn btn-secondary btn-sm" :disabled="subLoading" title="Subscribe to this feed">
                  + Add
                </button>
                <button @click="toggleFavorite({ id: fav.url_id })" class="btn-heart active" title="Remove from favorites">
                  ❤️
                </button>
              </div>
            </li>
          </ul>
        </div>

        <!-- Recommended Feeds Card -->
        <div class="card sidebar-card">
          <h3 class="sidebar-title mb-4">Recommended Feeds</h3>
          <div v-if="loadingOptionals" class="text-muted" style="font-size: 0.875rem;">Loading suggestions...</div>
          <div v-else-if="optionalFeeds.length === 0" class="text-muted" style="font-size: 0.875rem;">
            No preset feeds configured.
          </div>
          <ul v-else class="subs-list">
            <li v-for="feed in optionalFeeds" :key="feed.id || feed.url" class="sub-item">
              <div class="sub-info">
                <div class="flex items-center gap-2 flex-wrap mb-1">
                  <strong class="sub-name">{{ feed.name }}</strong>
                  <span class="likes-badge" title="Likes">
                    ❤️ {{ feed.likes || 0 }}
                  </span>
                </div>
                <div class="sub-desc" v-if="feed.description">{{ feed.description }}</div>
              </div>
              <div class="flex items-center gap-2 flex-shrink-0">
                <button 
                  @click="toggleFavorite(feed)" 
                  class="btn-heart" 
                  :class="{ active: isFavorite(feed.id) }" 
                  :title="isFavorite(feed.id) ? 'Remove from favorites' : 'Add to favorites'"
                >
                  {{ isFavorite(feed.id) ? '❤️' : '🤍' }}
                </button>
                <button @click="subscribeToOptional(feed)" class="btn btn-secondary btn-sm" :disabled="subLoading">
                  + Add
                </button>
              </div>
            </li>
          </ul>
        </div>
      </aside>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import api from '../services/api'

const posts = ref([])
const subscriptions = ref([])
const optionalFeeds = ref([])
const favorites = ref([])

const loadingPosts = ref(true)
const loadingSubs = ref(true)
const loadingOptionals = ref(true)
const loadingFavorites = ref(true)

const showAddSub = ref(false)
const newSubUrl = ref('')
const newSubName = ref('')
const subLoading = ref(false)
const subError = ref('')

const favoriteUrlIds = computed(() => {
  return new Set(favorites.value.map(f => f.url_id))
})

const isFavorite = (urlId) => {
  return favoriteUrlIds.value.has(urlId)
}

const formatDate = (post) => {
  const rawDate = post.published_at || post.created_at || post.published
  if (!rawDate) return 'Recent'
  const d = new Date(rawDate)
  if (isNaN(d.getTime())) return 'Recent'
  return d.toLocaleString('ru-RU', {
    day: 'numeric',
    month: 'short',
    year: 'numeric',
    hour: '2-digit',
    minute: '2-digit'
  })
}

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

const fetchOptionalFeeds = async () => {
  try {
    const res = await api.get('/optional_url_list/get-all-optionals-urls')
    optionalFeeds.value = res.data
  } catch (err) {
    console.error('Failed to load optional feeds', err)
  } finally {
    loadingOptionals.value = false
  }
}

const fetchFavorites = async () => {
  try {
    const res = await api.get('/favorites/get-all-favorites')
    favorites.value = res.data
  } catch (err) {
    console.error('Failed to load favorites', err)
  } finally {
    loadingFavorites.value = false
  }
}

const toggleFavorite = async (feed) => {
  const isFav = isFavorite(feed.id)
  try {
    if (isFav) {
      await api.delete(`/favorites/delete-from-favorite/${feed.id}`)
    } else {
      await api.post(`/favorites/add-to-favorite/${feed.id}`)
    }
    await fetchFavorites()
    await fetchOptionalFeeds()
  } catch (err) {
    console.error('Failed to toggle favorite', err)
    alert(err.response?.data?.detail || 'Error updating favorites')
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
    try {
      await api.post('/parser/parse')
    } catch (e) {
      console.warn('Auto parse warning', e)
    }
    newSubUrl.value = ''
    newSubName.value = ''
    showAddSub.value = false
    await fetchSubs()
    await fetchPosts()
  } catch (err) {
    subError.value = err.response?.data?.detail || 'Failed to add subscription'
  } finally {
    subLoading.value = false
  }
}

const subscribeToOptional = async (feed) => {
  subLoading.value = true
  try {
    await api.post('/subscriptions/add-subs', {
      url: feed.url,
      custom_name: feed.name
    })
    try {
      await api.post('/parser/parse')
    } catch (e) {
      console.warn('Auto parse warning', e)
    }
    await fetchSubs()
    await fetchPosts()
  } catch (err) {
    alert(err.response?.data?.detail || 'Failed to add subscription')
  } finally {
    subLoading.value = false
  }
}

const handleDeleteSub = async (id) => {
  if (!confirm('Are you sure you want to remove this subscription?')) return
  try {
    await api.delete(`/subscriptions/delete-sub/${id}`)
    await fetchSubs()
    fetchPosts()
  } catch (err) {
    console.error('Failed to delete sub', err)
  }
}

onMounted(() => {
  fetchPosts()
  fetchSubs()
  fetchOptionalFeeds()
  fetchFavorites()
})
</script>

<style scoped>
.feed-layout {
  display: grid;
  grid-template-columns: 1fr 340px;
  gap: 2rem;
  align-items: start;
}

.posts-list {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
}

.post-card {
  padding: 1.75rem;
  transition: transform 0.2s ease, border-color 0.2s ease;
}

.post-card:hover {
  transform: translateY(-2px);
  border-color: rgba(99, 102, 241, 0.3);
}

.post-title {
  font-size: 1.25rem;
  font-weight: 700;
  line-height: 1.4;
  margin-bottom: 0.5rem;
}

.post-title a {
  color: var(--text-main);
}
.post-title a:hover {
  color: var(--primary-color);
}

.post-meta {
  font-size: 0.825rem;
  color: var(--text-muted);
  margin-bottom: 1rem;
}

.post-summary {
  color: #cbd5e1;
  font-size: 0.95rem;
  line-height: 1.65;
}

.subs-sidebar {
  display: flex;
  flex-direction: column;
  gap: 1.5rem;
  width: 100%;
}

.sidebar-card {
  padding: 1.5rem;
}

.sidebar-title {
  font-size: 1.1rem;
  font-weight: 700;
  color: var(--text-main);
}

.subs-list {
  list-style: none;
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.sub-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 0;
  border-bottom: 1px solid var(--border-color);
}

.sub-item:last-child {
  border-bottom: none;
  padding-bottom: 0;
}

.sub-info {
  flex: 1;
  min-width: 0;
}

.sub-name {
  display: block;
  font-size: 0.925rem;
  color: var(--text-main);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
}

.sub-url, .sub-desc {
  font-size: 0.775rem;
  color: var(--text-muted);
  white-space: nowrap;
  overflow: hidden;
  text-overflow: ellipsis;
  margin-top: 0.15rem;
}

.btn-delete {
  background: rgba(239, 68, 68, 0.1);
  color: var(--danger-color);
  width: 28px;
  height: 28px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.btn-delete:hover {
  background: var(--danger-color);
  color: #fff;
}

.btn-heart {
  background: rgba(255, 255, 255, 0.05);
  border: 1px solid var(--border-color);
  font-size: 1.05rem;
  cursor: pointer;
  padding: 4px 8px;
  border-radius: 6px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s ease;
  flex-shrink: 0;
}

.btn-heart:hover {
  transform: scale(1.1);
  background: rgba(244, 63, 94, 0.15);
  border-color: rgba(244, 63, 94, 0.4);
}

.btn-heart.active {
  background: rgba(244, 63, 94, 0.2);
  border-color: rgba(244, 63, 94, 0.5);
}

.likes-badge {
  font-size: 0.75rem;
  color: #f43f5e;
  background: rgba(244, 63, 94, 0.12);
  padding: 0.1rem 0.4rem;
  border-radius: 12px;
  font-weight: 600;
  display: inline-flex;
  align-items: center;
  gap: 0.2rem;
}

.badge-favorite {
  background: rgba(244, 63, 94, 0.2);
  color: #f43f5e;
  padding: 0.2rem 0.5rem;
  border-radius: 9999px;
  font-size: 0.75rem;
  font-weight: 700;
}

.empty-feed-card {
  padding: 3rem 2rem;
}

.empty-icon {
  font-size: 3rem;
  margin-bottom: 1rem;
}

.error-msg {
  color: var(--danger-color);
  font-size: 0.875rem;
}

@media (max-width: 960px) {
  .feed-layout {
    grid-template-columns: 1fr;
  }
}
</style>

