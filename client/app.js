const API_URL = 'https://blogify-service.onrender.com/api';
// const API_URL = 'http://localhost:5000/api';

class Blogify {
    constructor() {
        this.posts = [];
        this.filteredPosts = [];
        this.currentPage = 1;
        this.postsPerPage = 6;
        this.isLoading = false;
        this.hasMorePosts = true;
        this.currentCategory = 'all';
        this.currentSort = 'latest';
        this.currentView = 'list';
        this.currentTab = 'for-you';
        this.searchQuery = '';
        
        this.init();
    }

    async init() {
        this.setupEventListeners();
        await this.loadPosts();
        this.updateStats();
        this.hideLoadingScreen();
    }

    setupEventListeners() {
        // Search functionality
        const searchInput = document.getElementById('search-input');
        searchInput.addEventListener('input', this.debounce(() => {
            this.searchQuery = searchInput.value.toLowerCase();
            this.filterPosts();
        }, 300));

        // Category filtering
        document.querySelectorAll('.nav-link[data-category]').forEach(link => {
            link.addEventListener('click', (e) => {
                e.preventDefault();
                this.setActiveCategory(e.target.closest('.nav-link').dataset.category);
            });
        });

        // Sort functionality
        document.getElementById('sort-select').addEventListener('change', (e) => {
            this.currentSort = e.target.value;
            this.filterPosts();
        });

        // View toggle
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setActiveView(e.target.closest('.view-btn').dataset.view);
            });
        });

        // Tab functionality
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.setActiveTab(e.target.closest('.tab-btn').dataset.tab);
            });
        });

        // Write modal
        document.getElementById('write-btn').addEventListener('click', () => {
            this.openWriteModal();
        });

        document.getElementById('close-modal').addEventListener('click', () => {
            this.closeWriteModal();
        });

        // Mobile menu toggle
        document.getElementById('menu-toggle').addEventListener('click', () => {
            this.toggleMobileMenu();
        });

        // Post form
        document.getElementById('post-form').addEventListener('submit', (e) => {
            e.preventDefault();
            this.submitPost();
        });

        // Character counter
        document.getElementById('content').addEventListener('input', (e) => {
            this.updateCharCount(e.target.value.length);
        });

        // Load more
        document.getElementById('load-more-btn').addEventListener('click', () => {
            this.loadMorePosts();
        });

        // Scroll to top
        document.getElementById('scroll-to-top').addEventListener('click', () => {
            window.scrollTo({ top: 0, behavior: 'smooth' });
        });

        // Scroll handling
        window.addEventListener('scroll', () => {
            this.handleScroll();
        });

        // Modal close on outside click
        window.addEventListener('click', (e) => {
            if (e.target.classList.contains('modal')) {
                this.closeWriteModal();
            }
        });

        // Follow buttons
        document.querySelectorAll('.follow-btn').forEach(btn => {
            btn.addEventListener('click', (e) => {
                this.handleFollow(e.target);
            });
        });

        // Topic tags
        document.querySelectorAll('.topic-tag').forEach(tag => {
            tag.addEventListener('click', (e) => {
                e.preventDefault();
                this.handleTopicClick(e.target.textContent);
            });
        });

        // Staff picks
        document.querySelectorAll('.pick-item').forEach(item => {
            item.addEventListener('click', () => {
                this.showNotification('Staff picks coming soon!', 'info');
            });
        });
    }

    async loadPosts() {
        try {
            this.isLoading = true;
            const response = await fetch(API_URL + '/posts');
            const data = await response.json();
            
            this.posts = data;
            this.filteredPosts = [...this.posts];
            this.renderPosts();
            
        } catch (error) {
            console.error('Error loading posts:', error);
            this.showNotification('Failed to load posts', 'error');
        } finally {
            this.isLoading = false;
        }
    }

    filterPosts() {
        let filtered = [...this.posts];

        // Category filter
        if (this.currentCategory !== 'all') {
            filtered = filtered.filter(post => post.category === this.currentCategory);
        }

        // Search filter
        if (this.searchQuery) {
            filtered = filtered.filter(post => 
                post.title.toLowerCase().includes(this.searchQuery) ||
                post.content.toLowerCase().includes(this.searchQuery) ||
                post.author.toLowerCase().includes(this.searchQuery)
            );
        }

        // Sort
        switch (this.currentSort) {
            case 'latest':
                filtered.sort((a, b) => new Date(b.date) - new Date(a.date));
                break;
            case 'oldest':
                filtered.sort((a, b) => new Date(a.date) - new Date(b.date));
                break;
            case 'popular':
                filtered.sort((a, b) => (b.views || 0) - (a.views || 0));
                break;
            case 'title':
                filtered.sort((a, b) => a.title.localeCompare(b.title));
                break;
        }

        this.filteredPosts = filtered;
        this.currentPage = 1;
        this.renderPosts();
    }

    renderPosts() {
        const postsContainer = document.getElementById('blog-posts');
        const startIndex = 0;
        const endIndex = this.currentPage * this.postsPerPage;
        const postsToShow = this.filteredPosts.slice(startIndex, endIndex);

        if (postsToShow.length === 0) {
            document.getElementById('no-posts').style.display = 'block';
            postsContainer.innerHTML = '';
        } else {
            document.getElementById('no-posts').style.display = 'none';
            postsContainer.innerHTML = postsToShow.map(post => this.createPostHTML(post)).join('');
        }

        // Add click listeners to posts
        postsContainer.querySelectorAll('.post').forEach((postElement, index) => {
            postElement.addEventListener('click', () => {
                this.openPostDetail(postsToShow[index]);
            });
        });

        // Update load more button
        const loadMoreBtn = document.getElementById('load-more-btn');
        if (endIndex >= this.filteredPosts.length) {
            loadMoreBtn.style.display = 'none';
        } else {
            loadMoreBtn.style.display = 'block';
        }

        // Update view class
        postsContainer.className = `blog-posts ${this.currentView}-view`;
    }

    createPostHTML(post) {
        const date = new Date(post.date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'short',
            day: 'numeric'
        });

        return `
            <article class="post" data-id="${post.id}">
                <div class="post-image">
                    <img src="${post.imageUrl || 'https://via.placeholder.com/400x200/1a8917/ffffff?text=Blogify'}" alt="${post.title}">
                    <span class="post-category">${post.category}</span>
                </div>
                <div class="post-content">
                    <h3 class="post-title">${post.title}</h3>
                    <p class="post-excerpt">${post.content.substring(0, 150)}${post.content.length > 150 ? '...' : ''}</p>
                    <div class="post-meta">
                        <div class="post-author">
                            <div class="author-avatar">
                                ${post.author.charAt(0).toUpperCase()}
                            </div>
                            <span>${post.author}</span>
                        </div>
                        <div class="post-stats">
                            <span class="post-stat">
                                <i class="fas fa-calendar"></i>
                                ${date}
                            </span>
                            <span class="post-stat">
                                <i class="fas fa-eye"></i>
                                ${post.views || 0}
                            </span>
                            <span class="post-stat">
                                <i class="fas fa-heart"></i>
                                ${post.likes || 0}
                            </span>
                        </div>
                    </div>
                </div>
            </article>
        `;
    }

    setActiveCategory(category) {
        this.currentCategory = category;
        
        // Update active state in navigation
        document.querySelectorAll('.nav-link[data-category]').forEach(link => {
            link.closest('.nav-item').classList.remove('active');
        });
        
        const activeLink = document.querySelector(`.nav-link[data-category="${category}"]`);
        if (activeLink) {
            activeLink.closest('.nav-item').classList.add('active');
        }

        this.filterPosts();
        this.showNotification(`Showing ${category === 'all' ? 'all posts' : category} posts`, 'info');
    }

    setActiveView(view) {
        this.currentView = view;
        
        // Update active state
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        document.querySelector(`.view-btn[data-view="${view}"]`).classList.add('active');
        
        // Update posts container
        const postsContainer = document.getElementById('blog-posts');
        postsContainer.className = `blog-posts ${view}-view`;
    }

    setActiveTab(tab) {
        this.currentTab = tab;
        
        // Update active state
        document.querySelectorAll('.tab-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        
        document.querySelector(`.tab-btn[data-tab="${tab}"]`).classList.add('active');
        
        // Handle tab content (for future implementation)
        if (tab === 'featured') {
            this.showNotification('Featured posts coming soon!', 'info');
        }
    }

    async loadMorePosts() {
        if (this.isLoading || !this.hasMorePosts) return;

        this.isLoading = true;
        const loadMoreBtn = document.getElementById('load-more-btn');
        loadMoreBtn.innerHTML = '<span>Loading...</span><i class="fas fa-spinner fa-spin"></i>';
        loadMoreBtn.classList.add('loading');

        // Simulate loading delay
        await new Promise(resolve => setTimeout(resolve, 1000));

        this.currentPage++;
        this.renderPosts();

        loadMoreBtn.innerHTML = '<span>Load More Posts</span><i class="fas fa-chevron-down"></i>';
        loadMoreBtn.classList.remove('loading');
        this.isLoading = false;
    }

    openWriteModal() {
        document.getElementById('write-modal').classList.add('active');
        document.body.style.overflow = 'hidden';
        document.getElementById('title').focus();
    }

    closeWriteModal() {
        document.getElementById('write-modal').classList.remove('active');
        document.body.style.overflow = 'auto';
        document.getElementById('post-form').reset();
        this.updateCharCount(0);
    }

    async submitPost() {
        const formData = new FormData(document.getElementById('post-form'));
        const postData = {
            title: formData.get('title'),
            content: formData.get('content'),
            author: formData.get('author'),
            category: formData.get('category'),
            imageUrl: formData.get('imageUrl') || null,
            date: new Date().toISOString(),
            views: 0,
            likes: 0
        };

        try {
            const response = await fetch('API_URL + /posts', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify(postData)
            });

            if (response.ok) {
                this.showNotification('Post published successfully!', 'success');
                this.closeWriteModal();
                await this.loadPosts();
                this.updateStats();
            } else {
                throw new Error('Failed to publish post');
            }
        } catch (error) {
            console.error('Error publishing post:', error);
            this.showNotification('Failed to publish post', 'error');
        }
    }

    openPostDetail(post) {
        const modal = document.getElementById('post-detail-modal');
        const content = document.getElementById('post-detail-content');
        
        const date = new Date(post.date).toLocaleDateString('en-US', {
            year: 'numeric',
            month: 'long',
            day: 'numeric'
        });

        content.innerHTML = `
            <div class="post-detail-header">
                <h2>${post.title}</h2>
                <div class="post-detail-meta">
                    <div class="post-detail-author">
                        <div class="author-avatar">
                            ${post.author.charAt(0).toUpperCase()}
                        </div>
                        <div>
                            <span class="author-name">${post.author}</span>
                            <span class="post-date">${date}</span>
                        </div>
                    </div>
                    <div class="post-detail-stats">
                        <span><i class="fas fa-eye"></i> ${post.views || 0} views</span>
                        <span><i class="fas fa-heart"></i> ${post.likes || 0} likes</span>
                        <span class="post-category">${post.category}</span>
                    </div>
                </div>
            </div>
            ${post.imageUrl ? `<img src="${post.imageUrl}" alt="${post.title}" class="post-detail-image">` : ''}
            <div class="post-detail-content">
                ${post.content.split('\n').map(paragraph => `<p>${paragraph}</p>`).join('')}
            </div>
        `;

        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
    }

    toggleMobileMenu() {
        const sidebar = document.getElementById('left-sidebar');
        sidebar.classList.toggle('active');
    }

    updateCharCount(count) {
        document.getElementById('char-count').textContent = count;
    }

    updateStats() {
        const stats = {
            totalPosts: this.posts.length,
            totalAuthors: new Set(this.posts.map(post => post.author)).size,
            totalViews: this.posts.reduce((sum, post) => sum + (post.views || 0), 0)
        };

        document.getElementById('total-posts').textContent = stats.totalPosts;
        document.getElementById('total-authors').textContent = stats.totalAuthors;
        document.getElementById('total-views').textContent = stats.totalViews.toLocaleString();
    }

    handleFollow(button) {
        if (button.textContent === 'Follow') {
            button.textContent = 'Following';
            button.style.background = 'var(--success-color)';
            this.showNotification('You are now following this author!', 'success');
        } else {
            button.textContent = 'Follow';
            button.style.background = 'var(--primary-color)';
            this.showNotification('You unfollowed this author', 'info');
        }
    }

    handleTopicClick(topic) {
        this.showNotification(`Filtering by ${topic} coming soon!`, 'info');
    }

    handleScroll() {
        // Show/hide scroll to top button
        const scrollToTopBtn = document.getElementById('scroll-to-top');
        if (window.scrollY > 300) {
            scrollToTopBtn.classList.add('visible');
        } else {
            scrollToTopBtn.classList.remove('visible');
        }

        // Infinite scroll
        if (this.isLoading || !this.hasMorePosts) return;

        const { scrollTop, scrollHeight, clientHeight } = document.documentElement;
        if (scrollTop + clientHeight >= scrollHeight - 100) {
            this.loadMorePosts();
        }
    }

    showNotification(message, type = 'info') {
        const notification = document.createElement('div');
        notification.className = `notification notification-${type}`;
        notification.innerHTML = `
            <i class="fas fa-${this.getNotificationIcon(type)}"></i>
            <span>${message}</span>
        `;

        document.body.appendChild(notification);

        // Animate in
        setTimeout(() => notification.classList.add('show'), 100);

        // Remove after 3 seconds
        setTimeout(() => {
            notification.classList.remove('show');
            setTimeout(() => notification.remove(), 300);
        }, 3000);
    }

    getNotificationIcon(type) {
        switch (type) {
            case 'success': return 'check-circle';
            case 'error': return 'exclamation-circle';
            case 'warning': return 'exclamation-triangle';
            default: return 'info-circle';
        }
    }

    debounce(func, wait) {
        let timeout;
        return function executedFunction(...args) {
            const later = () => {
                clearTimeout(timeout);
                func(...args);
            };
            clearTimeout(timeout);
            timeout = setTimeout(later, wait);
        };
    }

    hideLoadingScreen() {
        setTimeout(() => {
            document.getElementById('loading-screen').classList.add('hidden');
        }, 1500);
    }
}

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    new Blogify();
});

// Add notification styles
const notificationStyles = `
    .notification {
        position: fixed;
        top: 20px;
        right: 20px;
        background: white;
        border-left: 4px solid var(--primary-color);
        padding: 1rem 1.5rem;
        border-radius: var(--border-radius);
        box-shadow: var(--shadow-lg);
        display: flex;
        align-items: center;
        gap: 0.75rem;
        z-index: 10000;
        transform: translateX(100%);
        transition: var(--transition);
        max-width: 300px;
    }

    .notification.show {
        transform: translateX(0);
    }

    .notification-success {
        border-left-color: var(--success-color);
    }

    .notification-error {
        border-left-color: var(--error-color);
    }

    .notification-warning {
        border-left-color: var(--warning-color);
    }

    .notification i {
        font-size: 1.2rem;
    }

    .notification-success i {
        color: var(--success-color);
    }

    .notification-error i {
        color: var(--error-color);
    }

    .notification-warning i {
        color: var(--warning-color);
    }

    .notification-info i {
        color: var(--primary-color);
    }
`;

const styleSheet = document.createElement('style');
styleSheet.textContent = notificationStyles;
document.head.appendChild(styleSheet); 