// RRS Dashboard - Client Side Application

const API_BASE = window.location.origin;

// State Management
let currentUser = null;
let subscriptions = [];
let posts = [];
let currentFilter = 'all';
let currentSearchQuery = '';

// DOM Elements
const navDashboard = document.getElementById('nav-dashboard');
const navFeeds = document.getElementById('nav-feeds');
const navPosts = document.getElementById('nav-posts');
const navCreatePost = document.getElementById('nav-create-post');
const navProfile = document.getElementById('nav-profile');

const screenAuth = document.getElementById('screen-auth');
const screenDashboard = document.getElementById('screen-dashboard');
const screenFeeds = document.getElementById('screen-feeds');
const screenPosts = document.getElementById('screen-posts');
const screenCreatePost = document.getElementById('screen-create-post');
const screenProfile = document.getElementById('screen-profile');

const pageTitle = document.getElementById('page-title');
const btnLogout = document.getElementById('btn-logout');
const btnParseGlobal = document.getElementById('btn-parse-global');
const btnParseQuick = document.getElementById('btn-parse-quick');
const btnGoFeeds = document.getElementById('btn-go-feeds');
const btnProfileLogout = document.getElementById('btn-profile-logout');

const userWidget = document.getElementById('user-widget');
const widgetUsername = document.getElementById('widget-username');
const widgetRole = document.getElementById('widget-role');

const statFeedsCount = document.getElementById('stat-feeds-count');
const statPostsCount = document.getElementById('stat-posts-count');
const statUserStatus = document.getElementById('stat-user-status');

// Forms
const formLogin = document.getElementById('form-login');
const formRegister = document.getElementById('form-register');
const formAddFeed = document.getElementById('form-add-feed');
const formCreatePost = document.getElementById('form-create-post');
const selectPostFeed = document.getElementById('post-feed-id');

// List containers
const feedsListBody = document.getElementById('feeds-list-body');
const feedsTable = document.getElementById('feeds-table');
const feedsLoading = document.getElementById('feeds-loading');
const feedsEmpty = document.getElementById('feeds-empty');

const postsGrid = document.getElementById('posts-grid');
const postsLoading = document.getElementById('posts-loading');
const postsEmpty = document.getElementById('posts-empty');
const postSearch = document.getElementById('post-search');

// Toast Notification Container
const toastContainer = document.getElementById('toast-container');

// Tabs for login/register
const tabLogin = document.getElementById('tab-login');
const tabRegister = document.getElementById('tab-register');

// Show notification toast
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast ${type}`;
    toast.innerHTML = `
        <span>${message}</span>
        <button class="toast-close">&times;</button>
    `;
    toastContainer.appendChild(toast);
    
    // Close button event
    toast.querySelector('.toast-close').addEventListener('click', () => {
        toast.remove();
    });
    
    // Auto-remove after 4 seconds
    setTimeout(() => {
        if (toast.parentNode) {
            toast.remove();
        }
    }, 4000);
}

// Request wrapper with automatic token handling and token refresh
async function apiRequest(path, method = 'GET', body = null) {
    const url = `${API_BASE}${path}`;
    const headers = {
        'Accept': 'application/json'
    };
    
    // Attach authorization header if token exists
    const accessToken = localStorage.getItem('accessToken');
    if (accessToken) {
        headers['Authorization'] = `Bearer ${accessToken}`;
    }
    
    const config = {
        method,
        headers
    };
    
    if (body) {
        headers['Content-Type'] = 'application/json';
        config.body = JSON.stringify(body);
    }
    
    try {
        let response = await fetch(url, config);
        
        // Handle Token Expiration (401 Unauthorized)
        if (response.status === 401 && path !== '/auth/login' && path !== '/auth/refresh') {
            const refreshToken = localStorage.getItem('refreshToken');
            if (refreshToken) {
                console.log('Access token expired, attempting refresh...');
                try {
                    const refreshResponse = await fetch(`${API_BASE}/auth/refresh`, {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ refresh_token: refreshToken })
                    });
                    
                    if (refreshResponse.ok) {
                        const refreshData = await refreshResponse.json();
                        localStorage.setItem('accessToken', refreshData.access_token);
                        localStorage.setItem('refreshToken', refreshData.refresh_token);
                        
                        // Retry the original request with the new access token
                        config.headers['Authorization'] = `Bearer ${refreshData.access_token}`;
                        response = await fetch(url, config);
                    } else {
                        // Refresh failed
                        handleAuthFailure();
                        throw new Error('Сессия истекла. Войдите заново.');
                    }
                } catch (refreshErr) {
                    handleAuthFailure();
                    throw refreshErr;
                }
            } else {
                handleAuthFailure();
                throw new Error('Вы не авторизованы. Войдите в аккаунт.');
            }
        }
        
        if (!response.ok) {
            let errorDetail = 'Произошла ошибка при запросе';
            try {
                const errorData = await response.json();
                errorDetail = errorData.detail || errorDetail;
            } catch (e) {}
            throw new Error(errorDetail);
        }
        
        // Some endpoints return standard JSON string rather than dictionary
        const contentType = response.headers.get('content-type');
        if (contentType && contentType.includes('application/json')) {
            return await response.json();
        }
        return await response.text();
        
    } catch (error) {
        console.error(`API Error on ${path}:`, error);
        throw error;
    }
}

// Clear local authentication state
function handleAuthFailure() {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    currentUser = null;
    updateUserWidgetUI();
    
    // Switch to profile screen showing auth panel if not already there
    if (window.location.hash !== '#profile') {
        window.location.hash = '#profile';
    }
}

// Load current user profile details
async function loadCurrentUser() {
    const token = localStorage.getItem('accessToken');
    if (!token) return false;
    
    try {
        currentUser = await apiRequest('/auth/me');
        updateUserWidgetUI();
        updateProfileUI();
        return true;
    } catch (e) {
        console.log('Failed to restore session:', e);
        return false;
    }
}

// Update UI elements showing active user details
function updateUserWidgetUI() {
    if (currentUser) {
        widgetUsername.textContent = currentUser.username;
        widgetRole.textContent = currentUser.isAdmin ? 'Администратор' : (currentUser.isCreator ? 'Создатель' : 'Пользователь');
        btnLogout.style.display = 'block';
        statUserStatus.textContent = currentUser.username;
    } else {
        widgetUsername.textContent = 'Гость';
        widgetRole.textContent = 'Не авторизован';
        btnLogout.style.display = 'none';
        statUserStatus.textContent = 'Не авторизован';
    }
}

// Update profile screen card content
function updateProfileUI() {
    const profileUsername = document.getElementById('profile-username');
    const profileRoleBadge = document.getElementById('profile-role-badge');
    const profileId = document.getElementById('profile-id');
    const profileIsCreator = document.getElementById('profile-is-creator');
    const profileIsAdmin = document.getElementById('profile-is-admin');
    const profileStatus = document.getElementById('profile-status');
    
    if (currentUser) {
        profileUsername.textContent = currentUser.username;
        profileRoleBadge.textContent = currentUser.isAdmin ? 'Admin' : (currentUser.isCreator ? 'Creator' : 'User');
        profileId.textContent = currentUser.id;
        profileIsCreator.textContent = currentUser.isCreator ? 'Да' : 'Нет';
        profileIsAdmin.textContent = currentUser.isAdmin ? 'Да' : 'Нет';
        profileStatus.textContent = currentUser.status === 1 ? 'Активен' : `Заблокирован (${currentUser.status})`;
    }
}

// Load all feed subscriptions
async function loadSubscriptions() {
    if (!currentUser) return;
    
    feedsLoading.style.display = 'block';
    feedsTable.style.display = 'none';
    feedsEmpty.style.display = 'none';
    
    try {
        subscriptions = await apiRequest('/subscriptions/get-all-subs');
        
        feedsLoading.style.display = 'none';
        
        // Update stats
        statFeedsCount.textContent = subscriptions.length;
        
        // Update dropdown choices in create post screen
        selectPostFeed.innerHTML = '<option value="" disabled selected>Выберите ленту</option>';
        
        if (subscriptions.length === 0) {
            feedsEmpty.style.display = 'block';
            return;
        }
        
        feedsTable.style.display = 'table';
        feedsListBody.innerHTML = '';
        
        subscriptions.forEach(sub => {
            // Append rows
            const tr = document.createElement('tr');
            tr.innerHTML = `
                <td><strong>${sub.id}</strong></td>
                <td><span style="font-weight: 600; color: #a5b4fc;">${sub.custom_name || 'Без названия'}</span></td>
                <td><code style="color: var(--text-secondary); font-size: 0.85rem;">${sub.feed_url}</code></td>
                <td><span class="badge-status">${sub.is_active ? 'Активна' : 'Отключена'}</span></td>
                <td>${sub.created_at ? new Date(sub.created_at).toLocaleString('ru-RU') : 'Неизвестно'}</td>
            `;
            feedsListBody.appendChild(tr);
            
            // Append options
            const opt = document.createElement('option');
            opt.value = sub.id;
            opt.textContent = `${sub.custom_name} (ID: ${sub.id})`;
            selectPostFeed.appendChild(opt);
        });
        
    } catch (err) {
        feedsLoading.style.display = 'none';
        feedsEmpty.style.display = 'block';
        feedsEmpty.innerHTML = `<p style="color: var(--error-color)">Ошибка: ${err.message}</p>`;
    }
}

// Load all parsed posts
async function loadPosts() {
    if (!currentUser) return;
    
    postsLoading.style.display = 'block';
    postsEmpty.style.display = 'none';
    postsGrid.innerHTML = '';
    
    try {
        posts = await apiRequest('/api/posts/get-all-post');
        postsLoading.style.display = 'none';
        
        // Update stats
        statPostsCount.textContent = posts.length;
        
        renderPosts();
        
    } catch (err) {
        postsLoading.style.display = 'none';
        postsEmpty.style.display = 'block';
        postsEmpty.innerHTML = `<p style="color: var(--error-color)">Ошибка: ${err.message}</p>`;
    }
}

// Render posts grid with filtering and search applied
function renderPosts() {
    postsGrid.innerHTML = '';
    
    // Apply filters
    let filtered = [...posts];
    
    if (currentFilter === 'manual') {
        // Manually created have published_at set to null
        filtered = filtered.filter(p => !p.published_at);
    } else if (currentFilter === 'parsed') {
        filtered = filtered.filter(p => p.published_at);
    }
    
    // Apply search query
    if (currentSearchQuery) {
        const query = currentSearchQuery.toLowerCase();
        filtered = filtered.filter(p => 
            p.title.toLowerCase().includes(query) || 
            (p.summary && p.summary.toLowerCase().includes(query))
        );
    }
    
    if (filtered.length === 0) {
        postsEmpty.style.display = 'block';
        return;
    }
    
    postsEmpty.style.display = 'none';
    
    // Get feed names dictionary to map feed_id to custom_name
    const feedNames = {};
    subscriptions.forEach(sub => {
        feedNames[sub.id] = sub.custom_name;
    });
    
    filtered.forEach(post => {
        const card = document.createElement('article');
        card.className = 'post-card glass-panel';
        
        const sourceName = feedNames[post.feed_id] || `Лента #${post.feed_id}`;
        const isManual = !post.published_at;
        const iconLabel = isManual ? '✍️ Вручную' : '📡 Парсер';
        const formattedDate = post.published_at 
            ? new Date(post.published_at).toLocaleString('ru-RU')
            : (post.created_at ? new Date(post.created_at).toLocaleString('ru-RU') : 'Недавно');
            
        card.innerHTML = `
            <div class="post-meta">
                <span class="post-source">${sourceName}</span>
                <span style="color: ${isManual ? '#f59e0b' : '#38bdf8'}">${iconLabel}</span>
            </div>
            <h3><a href="${post.link}" target="_blank" rel="noopener noreferrer">${post.title || 'Без заголовка'}</a></h3>
            <p class="post-summary">${post.summary || 'Краткое содержание отсутствует'}</p>
            <div class="post-footer">
                <span>Дата: ${formattedDate}</span>
                <a href="${post.link}" target="_blank" rel="noopener noreferrer" class="btn-read-more">Перейти ↗</a>
            </div>
        `;
        postsGrid.appendChild(card);
    });
}

// Trigger RSS Parsing backend endpoint
async function runParser() {
    showToast('Запуск парсинга лент в фоновом режиме...', 'info');
    try {
        const result = await apiRequest('/parser/parse', 'POST');
        showToast(`Парсинг успешно завершен: ${result}`, 'success');
        // Reload feeds and posts
        await loadSubscriptions();
        await loadPosts();
    } catch (e) {
        showToast(`Не удалось распарсить: ${e.message}`, 'error');
    }
}

// Screen Routing
function handleRouting() {
    const hash = window.location.hash || '#dashboard';
    
    // Reset active nav items
    const navItems = [navDashboard, navFeeds, navPosts, navCreatePost, navProfile];
    navItems.forEach(item => item.classList.remove('active'));
    
    // Hide all screens
    const screens = [screenAuth, screenDashboard, screenFeeds, screenPosts, screenCreatePost, screenProfile];
    screens.forEach(s => s.style.display = 'none');
    
    // Show header buttons conditionally
    btnParseGlobal.style.display = currentUser ? 'block' : 'none';
    
    if (!currentUser) {
        // If not logged in, force authentication screen
        screenAuth.style.display = 'block';
        navProfile.classList.add('active');
        pageTitle.textContent = 'Авторизация';
        return;
    }
    
    switch(hash) {
        case '#dashboard':
            screenDashboard.style.display = 'block';
            navDashboard.classList.add('active');
            pageTitle.textContent = 'Обзор панели';
            // Refresh counts
            statFeedsCount.textContent = subscriptions.length;
            statPostsCount.textContent = posts.length;
            break;
            
        case '#feeds':
            screenFeeds.style.display = 'block';
            navFeeds.classList.add('active');
            pageTitle.textContent = 'Мои подписки';
            loadSubscriptions();
            break;
            
        case '#posts':
            screenPosts.style.display = 'block';
            navPosts.classList.add('active');
            pageTitle.textContent = 'Лента публикаций';
            loadPosts();
            break;
            
        case '#create-post':
            screenCreatePost.style.display = 'block';
            navCreatePost.classList.add('active');
            pageTitle.textContent = 'Создать публикацию';
            loadSubscriptions(); // reload feeds list for select options
            break;
            
        case '#profile':
            screenProfile.style.display = 'block';
            navProfile.classList.add('active');
            pageTitle.textContent = 'Профиль пользователя';
            updateProfileUI();
            break;
            
        default:
            window.location.hash = '#dashboard';
            break;
    }
}

// Set up Auth View Tabs
tabLogin.addEventListener('click', () => {
    tabLogin.classList.add('active');
    tabRegister.classList.remove('active');
    formLogin.style.display = 'block';
    formRegister.style.display = 'none';
});

tabRegister.addEventListener('click', () => {
    tabRegister.classList.add('active');
    tabLogin.classList.remove('active');
    formRegister.style.display = 'block';
    formLogin.style.display = 'none';
});

// LOGIN ACTION
formLogin.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('login-username').value;
    const password = document.getElementById('login-password').value;
    
    try {
        const tokens = await apiRequest('/auth/login', 'POST', { username, password });
        localStorage.setItem('accessToken', tokens.access_token);
        localStorage.setItem('refreshToken', tokens.refresh_token);
        
        showToast('Вход успешно выполнен!', 'success');
        
        // Load profile and route
        const success = await loadCurrentUser();
        if (success) {
            // Load base data
            await Promise.all([loadSubscriptions(), loadPosts()]);
            window.location.hash = '#dashboard';
            handleRouting();
        }
    } catch (err) {
        showToast(`Ошибка входа: ${err.message}`, 'error');
    }
});

// REGISTER ACTION
formRegister.addEventListener('submit', async (e) => {
    e.preventDefault();
    const username = document.getElementById('register-username').value;
    const password = document.getElementById('register-password').value;
    const confirm = document.getElementById('register-confirm').value;
    
    if (password !== confirm) {
        showToast('Пароли не совпадают!', 'warning');
        return;
    }
    
    try {
        await apiRequest('/api/user/register_user', 'POST', { username, password });
        showToast('Регистрация прошла успешно! Теперь вы можете войти.', 'success');
        
        // Autofill login and switch to login tab
        document.getElementById('login-username').value = username;
        document.getElementById('login-password').value = '';
        tabLogin.click();
    } catch (err) {
        showToast(`Ошибка регистрации: ${err.message}`, 'error');
    }
});

// ADD FEED ACTION
formAddFeed.addEventListener('submit', async (e) => {
    e.preventDefault();
    const url = document.getElementById('feed-url').value;
    const custom_name = document.getElementById('feed-name').value;
    
    try {
        await apiRequest('/subscriptions/add-subs', 'POST', { url, custom_name });
        showToast('Подписка успешно добавлена!', 'success');
        formAddFeed.reset();
        loadSubscriptions();
    } catch (err) {
        showToast(`Не удалось добавить подписку: ${err.message}`, 'error');
    }
});

// CREATE POST ACTION
formCreatePost.addEventListener('submit', async (e) => {
    e.preventDefault();
    const feed_id = parseInt(selectPostFeed.value);
    const title = document.getElementById('post-title').value;
    const link = document.getElementById('post-link').value;
    const summary = document.getElementById('post-summary').value;
    
    if (!feed_id) {
        showToast('Пожалуйста, выберите ленту!', 'warning');
        return;
    }
    
    try {
        const postData = { feed_id, title, link, summary };
        await apiRequest('/api/posts/create-post', 'POST', postData);
        showToast('Пост успешно создан и опубликован в RabbitMQ!', 'success');
        formCreatePost.reset();
        window.location.hash = '#posts';
    } catch (err) {
        showToast(`Ошибка создания поста: ${err.message}`, 'error');
    }
});

// Global buttons
btnParseGlobal.addEventListener('click', runParser);
btnParseQuick.addEventListener('click', runParser);
btnGoFeeds.addEventListener('click', () => { window.location.hash = '#feeds'; });

// Logouts
const performLogout = () => {
    localStorage.removeItem('accessToken');
    localStorage.removeItem('refreshToken');
    currentUser = null;
    updateUserWidgetUI();
    showToast('Вы вышли из аккаунта.', 'info');
    window.location.hash = '#profile';
    handleRouting();
};

btnLogout.addEventListener('click', performLogout);
btnProfileLogout.addEventListener('click', performLogout);

// Filter Controls for Posts
document.getElementById('filter-all').addEventListener('click', (e) => {
    setActiveFilter(e.target, 'all');
});
document.getElementById('filter-manual').addEventListener('click', (e) => {
    setActiveFilter(e.target, 'manual');
});
document.getElementById('filter-parsed').addEventListener('click', (e) => {
    setActiveFilter(e.target, 'parsed');
});

function setActiveFilter(btnElement, filterValue) {
    document.querySelectorAll('.filter-controls .btn').forEach(btn => btn.classList.remove('active'));
    btnElement.classList.add('active');
    currentFilter = filterValue;
    renderPosts();
}

// Search field logic
postSearch.addEventListener('input', (e) => {
    currentSearchQuery = e.target.value;
    renderPosts();
});

// Router Initializer
window.addEventListener('hashchange', handleRouting);

// App Bootstrapping
async function initApp() {
    const hasToken = localStorage.getItem('accessToken');
    if (hasToken) {
        const success = await loadCurrentUser();
        if (success) {
            // Pre-load data in background
            loadSubscriptions().catch(() => {});
            loadPosts().catch(() => {});
        } else {
            handleAuthFailure();
        }
    } else {
        handleAuthFailure();
    }
    handleRouting();
}

// Boot
initApp();
