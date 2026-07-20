<template>
  <div class="container generator">
    <h1 class="title text-center">Custom RSS Generator</h1>
    <div class="card generator-card mx-auto">
      <p class="description text-center">
        Enter a URL to generate a custom RSS feed from its contents.
      </p>
      
      <form @submit.prevent="handleGenerate">
        <div class="form-group">
          <input type="url" v-model="url" required placeholder="https://example.com" />
        </div>
        <button type="submit" class="btn" style="width: 100%;" :disabled="loading">
          {{ loading ? 'Generating...' : 'Generate RSS Link' }}
        </button>
      </form>

      <div v-if="error" class="error-msg mt-4 text-center">{{ error }}</div>

      <div v-if="generatedLink" class="result mt-4">
        <h3 style="margin-bottom: 0.5rem; color: var(--success-color);">Success!</h3>
        <p style="color: var(--text-muted); margin-bottom: 1rem;">Here is your custom RSS feed link:</p>
        <div class="link-box">
          <a :href="generatedLink" target="_blank">{{ generatedLink }}</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref } from 'vue'
import api from '../services/api'

const url = ref('')
const loading = ref(false)
const error = ref('')
const generatedLink = ref('')

const handleGenerate = async () => {
  error.value = ''
  generatedLink.value = ''
  loading.value = true
  try {
    const res = await api.post('/generate-rrs-from-url/send-url-for-generate-rss', { url: url.value })
    const backendLink = res.data.rss_link
    const urlObj = new URL(backendLink)
    urlObj.hostname = window.location.hostname
    urlObj.port = '8082'
    generatedLink.value = urlObj.toString()
  } catch (err) {
    error.value = err.response?.data?.detail || 'Failed to generate RSS feed'
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.generator-card {
  max-width: 600px;
  margin: 0 auto;
}
.description {
  color: var(--text-muted);
  margin-bottom: 2rem;
}
.error-msg {
  color: var(--danger-color);
}
.link-box {
  background-color: var(--bg-color);
  border: 1px solid var(--border-color);
  padding: 1rem;
  border-radius: 4px;
  word-break: break-all;
}
.mx-auto {
  margin-left: auto;
  margin-right: auto;
}
</style>
