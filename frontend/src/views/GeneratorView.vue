<template>
  <div class="container generator">
    <h1 class="title text-center mb-2">Custom RSS Generator</h1>
    <p class="description text-center mb-6">
      Generate a custom RSS feed from any supported website URL by specifying target pages.
    </p>

    <div class="card generator-card mx-auto">
      <form @submit.prevent="handleGenerate" class="flex flex-col gap-4">
        <div class="form-group">
          <label for="url-input" style="display: block; font-weight: 600; margin-bottom: 0.5rem; color: var(--text-main);">
            Target Website URL
          </label>
          <input 
            id="url-input"
            type="url" 
            v-model="url" 
            required 
            placeholder="https://habr.com/ru/flows/develop/" 
          />
        </div>

        <div class="form-group">
          <label for="pages-input" style="display: block; font-weight: 600; margin-bottom: 0.5rem; color: var(--text-main);">
            Number of Pages to Parse
          </label>
          <input 
            id="pages-input"
            type="number" 
            v-model.number="pages" 
            required 
            min="1" 
            max="20"
            placeholder="1" 
          />
          <p style="font-size: 0.8rem; color: var(--text-muted); margin-top: 0.25rem;">
            Select how many pages (1 - 20) the parser should scrape.
          </p>
        </div>

        <button type="submit" class="btn btn-accent" style="width: 100%; margin-top: 0.5rem;" :disabled="loading">
          {{ loading ? 'Generating Feed...' : 'Generate RSS Link' }}
        </button>
      </form>

      <div v-if="error" class="error-msg mt-4 text-center card">{{ error }}</div>

      <div v-if="generatedLink" class="result-card mt-6">
        <div class="flex items-center justify-between mb-2">
          <h3 style="color: var(--success-color); font-size: 1.1rem; font-weight: 700;">
            Feed Link Ready!
          </h3>
          <span class="badge badge-success">Generated</span>
        </div>
        <p style="color: var(--text-muted); font-size: 0.875rem; margin-bottom: 0.75rem;">
          Use this generated RSS URL to subscribe in your feed reader:
        </p>

        <div class="link-box flex items-center justify-between gap-3">
          <a :href="generatedLink" target="_blank" class="link-text">{{ generatedLink }}</a>
          <button @click="copyLink" class="btn btn-secondary btn-sm flex-shrink-0">
            {{ copied ? 'Copied!' : 'Copy Link' }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../services/api'

const url = ref('')
const pages = ref(1)
const loading = ref(false)
const error = ref('')
const generatedLink = ref('')
const copied = ref(false)

const handleGenerate = async () => {
  error.value = ''
  generatedLink.value = ''
  copied.value = false
  loading.value = true
  try {
    const res = await api.post('/generate-rrs-from-url/send-url-for-generate-rss', { 
      url: url.value,
      pages: pages.value || 1
    })
    const backendLink = res.data.rss_link
    const urlObj = new URL(backendLink)
    urlObj.hostname = window.location.hostname
    urlObj.port = '8082'
    generatedLink.value = urlObj.toString()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to generate RSS feed. Please check the URL format.'
  } finally {
    loading.value = false
  }
}

const copyLink = () => {
  if (!generatedLink.value) return
  navigator.clipboard.writeText(generatedLink.value)
  copied.value = true
  setTimeout(() => {
    copied.value = false
  }, 2500)
}
</script>

<style scoped>
.generator-card {
  max-width: 580px;
  margin: 0 auto;
}

.description {
  color: var(--text-muted);
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
}

.error-msg {
  color: var(--danger-color);
  border-left: 4px solid var(--danger-color);
}

.result-card {
  background: rgba(16, 185, 129, 0.05);
  border: 1px solid rgba(16, 185, 129, 0.2);
  border-radius: var(--radius-sm);
  padding: 1.25rem;
}

.link-box {
  background-color: rgba(11, 15, 25, 0.8);
  border: 1px solid var(--border-color);
  padding: 0.75rem 1rem;
  border-radius: 6px;
  overflow: hidden;
}

.link-text {
  font-size: 0.875rem;
  word-break: break-all;
  color: #818cf8;
}

.mx-auto {
  margin-left: auto;
  margin-right: auto;
}
</style>
