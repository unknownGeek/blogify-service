
// console.log("API_URL is:", window.API_URL);

const API_URL = window.API_URL;

const formatter = new Intl.NumberFormat("en", {
  notation: "compact",
  maximumFractionDigits: 1
});


function formatNumber(num) {
    return formatter.format(num);
}

// --- Blogify Post Detail Loader for post.html ---
function getQueryParam(name) {
    const url = new URL(window.location.href);
    return url.searchParams.get(name);
}

async function loadPostDetail() {
    // Only run on post.html
    if (!window.location.pathname.endsWith('post.html')) return;
    const postId = getQueryParam('id');
    if (!postId) return;
    const res = await fetch(`${API_URL}/posts/${postId}`);
    if (!res.ok) return;
    const post = await res.json();
    const main = document.getElementById('post-detail-main');
    if (!main) return;
    main.style.display = 'block';
    // Header image
    document.getElementById('post-detail-header').innerHTML = post.imageUrl ? `<img src="${post.imageUrl}" alt="${post.title}">` : '';
    // Title
    document.getElementById('post-detail-title').textContent = post.title;
    // Meta
    const date = new Date(post.date).toLocaleDateString('en-US', { year: 'numeric', month: 'long', day: 'numeric' });
    document.getElementById('post-detail-meta').innerHTML = `
        <div class="author-avatar">${post.author.charAt(0).toUpperCase()}</div>
        <div>
            <div><strong>${post.author}</strong></div>
            <div>${date} <span class="post-detail-category">${post.category}</span></div>
        </div>
    `;
    // Body - handle both plain text and HTML content
    const contentElement = document.getElementById('post-detail-body');
    console.log('Post content received:', post.content);
    console.log('Content type:', typeof post.content);
    console.log('Content length:', post.content.length);
    
    if (post.content.includes('<p>') || post.content.includes('<h2>') || post.content.includes('<ul>')) {
        // Content already contains HTML, render it directly
        console.log('Rendering as HTML content');
        contentElement.innerHTML = post.content;
        
        // Force a reflow to ensure content is visible
        contentElement.style.display = 'none';
        contentElement.offsetHeight; // Trigger reflow
        contentElement.style.display = 'block';
        
        console.log('Content element height after rendering:', contentElement.offsetHeight);
        console.log('Content element scroll height:', contentElement.scrollHeight);
    } else {
        // Plain text content, split by newlines and wrap in p tags
        console.log('Rendering as plain text content');
        contentElement.innerHTML = post.content.split('\n').map(p => `<p>${p}</p>`).join('');
    }
    // Stats
    document.getElementById('post-detail-stats').innerHTML = `
        <span><i class="fas fa-eye"></i> ${post.views || 0} views</span>
        <span><i class="fas fa-heart"></i> ${post.likes || 0} likes</span>
    `;

    // Comments Section
    const commentsDiv = document.getElementById('post-detail-comments');
        if (Array.isArray(post.comments) && post.comments.length > 0) {
            commentsDiv.innerHTML = `
                <div class="collapsible-header" id="comments-header">
                    <span>Comments <span class="collapsible-arrow" id="comments-arrow">▼</span></span>
                </div>
                <div class="comments-list">
                    ${post.comments.map(c => `
                        <div class="comment-item">
                            <div class="comment-avatar">${c.author.charAt(0).toUpperCase()}</div>
                            <div class="comment-content">
                                <div class="comment-author">${c.author}</div>
                                <div class="comment-date">${c.date}</div>
                                <div class="comment-text">${c.content}</div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            commentsDiv.innerHTML = '';
        }

    // Reviews Section
    const reviewsDiv = document.getElementById('post-detail-reviews');
        if (Array.isArray(post.reviews) && post.reviews.length > 0) {
            reviewsDiv.innerHTML = `
                <div class="collapsible-header" id="reviews-header">
                    <span>Reviews <span class="collapsible-arrow" id="reviews-arrow">▼</span></span>
                </div>
                <div class="reviews-list">
                    ${post.reviews.map(r => `
                        <div class="review-item">
                            <div class="review-avatar">${r.reviewer.charAt(0).toUpperCase()}</div>
                            <div class="review-content">
                                <div class="review-author">${r.reviewer}</div>
                                <div class="review-rating">${'★'.repeat(r.rating)}${'☆'.repeat(5 - r.rating)}</div>
                                <div class="review-summary">${r.summary}</div>
                            </div>
                        </div>
                    `).join('')}
                </div>
            `;
        } else {
            reviewsDiv.innerHTML = '';
        }

    // Collapsible logic for comments
    const commentsHeader = document.getElementById('comments-header');
    if (commentsHeader) {
        commentsHeader.addEventListener('click', function() {
            const section = commentsDiv;
            const arrow = document.getElementById('comments-arrow');
            section.classList.toggle('collapsed');
            if (section.classList.contains('collapsed')) {
                arrow.style.transform = 'rotate(-90deg)';
            } else {
                arrow.style.transform = 'rotate(0deg)';
            }
        });
    }
    // Collapsible logic for reviews
    const reviewsHeader = document.getElementById('reviews-header');
    if (reviewsHeader) {
        reviewsHeader.addEventListener('click', function() {
            const section = reviewsDiv;
            const arrow = document.getElementById('reviews-arrow');
            section.classList.toggle('collapsed');
            if (section.classList.contains('collapsed')) {
                arrow.style.transform = 'rotate(-90deg)';
            } else {
                arrow.style.transform = 'rotate(0deg)';
            }
        });
    }
}

// Run loader for post.html
if (window.location.pathname.endsWith('post.html')) {
    document.addEventListener('DOMContentLoaded', loadPostDetail);
}
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
    this.currentView = 'grid';
        this.currentTab = 'for-you';
        this.searchQuery = '';
        
        // Loading messages for the loading screen
        this.loadingMessages = [
            "Preparing your reading experience...",
            "Loading amazing stories...",
            "Setting up your personal feed...",
            "Gathering fresh content...",
            "Almost ready...",
            "Welcome to Blogify!"
        ];
        this.currentMessageIndex = 0;
        
        // Enhanced loading messages - professional and sophisticated
        this.enhancedMessages = [
            "Preparing your reading experience...",
            "Loading amazing stories...",
            "Welcome to Blogify!"
        ];
        
        // Dynamic loading messages that change based on progress
        this.dynamicMessages = [
            "Crafting beautiful layouts...",
            "Indexing amazing content...",
            "Blogify is ready!"
        ];
        
        this.init();
    }

    async init() {
        this.setupEventListeners();
        
        // Check if user has already seen the loading screen in this session
        const hasSeenLoading = sessionStorage.getItem('blogify_loading_seen');
        
        if (hasSeenLoading) {
            // User has already seen loading screen, hide it immediately
            this.hideLoadingScreen();
            // Ensure main content is visible
            const mainContent = document.querySelector('.main-content');
            if (mainContent) {
                mainContent.style.display = 'block';
            }
        } else {
            // First time visit, show loading screen
            this.startLoadingMessages();
            this.startLoadingTimer();
            
            // Mark that user has seen the loading screen
            sessionStorage.setItem('blogify_loading_seen', 'true');
        }
        
        // Load posts in parallel
        await this.loadPosts();
        this.updateStats();
        
        // Mark that posts are loaded
        this.postsLoaded = true;

        // Set grid view button as active on load
        document.querySelectorAll('.view-btn').forEach(btn => {
            btn.classList.remove('active');
        });
        const gridBtn = document.querySelector('.view-btn[data-view="grid"]');
        if (gridBtn) gridBtn.classList.add('active');
        // Set posts container class
        const postsContainer = document.getElementById('blog-posts');
        if (postsContainer) postsContainer.className = 'blog-posts grid-view';
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

        // Handle spinner for loading more
        let spinner = document.getElementById('load-more-spinner');
        if (!spinner) {
            spinner = document.createElement('div');
            spinner.id = 'load-more-spinner';
            spinner.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            spinner.style.display = 'none';
            spinner.style.textAlign = 'center';
            spinner.style.margin = '2rem auto';
            spinner.style.fontSize = '2rem';
            postsContainer.parentNode.insertBefore(spinner, postsContainer.nextSibling);
        }
        // Hide spinner by default
        spinner.style.display = 'none';

        // Hide the old load more button if it exists
        const loadMoreBtn = document.getElementById('load-more-btn');
        if (loadMoreBtn) loadMoreBtn.style.display = 'none';

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
                                ${formatNumber(post.views || 0)}
                            </span>
                            <span class="post-stat">
                                <i class="fas fa-heart"></i>
                                ${formatNumber(post.likes || 0)}
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
        let spinner = document.getElementById('load-more-spinner');
        if (!spinner) {
            spinner = document.createElement('div');
            spinner.id = 'load-more-spinner';
            spinner.innerHTML = '<i class="fas fa-spinner fa-spin"></i>';
            spinner.style.textAlign = 'center';
            spinner.style.margin = '2rem auto';
            spinner.style.fontSize = '2rem';
            document.getElementById('blog-posts').parentNode.insertBefore(spinner, document.getElementById('blog-posts').nextSibling);
        }
        spinner.style.display = 'block';

        // Simulate loading delay
        await new Promise(resolve => setTimeout(resolve, 1000));

        this.currentPage++;
        this.renderPosts();

        spinner.style.display = 'none';
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
        // Estimate read time (assume 200 words/min)
        const wordCount = post.content.split(/\s+/).length;
        const readTime = Math.max(1, Math.round(wordCount / 200));
        const maxExcerptLength = 900;
        // Show only excerpt (up to maxExcerptLength chars, no line breaks)
        let excerpt = post.content.replace(/\n/g, ' ');
        if (excerpt.length > maxExcerptLength) {
            excerpt = excerpt.substring(0, maxExcerptLength) + '...';
        }
        content.innerHTML = `
            <div class="popup-card">
                ${post.imageUrl ? `<img src="${post.imageUrl}" alt="${post.title}" class="popup-image">` : ''}
                <h2 class="popup-title">${post.title}</h2>
                <div class="popup-meta-row">
                    <div class="popup-author-avatar">${post.author.charAt(0).toUpperCase()}</div>
                    <div class="popup-author-info">
                        <div class="popup-author-name">${post.author}</div>
                        <div class="popup-date">${date}</div>
                    </div>
                    <div class="popup-meta-stats">
                        <span><i class="fas fa-eye"></i> ${formatNumber(post.views || 0)}</span>
                        <span><i class="fas fa-heart"></i> ${formatNumber(post.likes || 0)}</span>
                        <span><i class="fas fa-clock"></i> ${readTime} min read</span>
                    </div>
                </div>
                <div class="popup-body">
                    <p>${excerpt}</p>
                </div>
                <div class="popup-actions">
                    <a href="post.html?id=${post.id}" class="read-detail-btn">
                        <i class="fas fa-book-open"></i> Read in Detail
                    </a>
                </div>
            </div>
        `;
        // Add floating particles for insane effect
        const insaneParticles = [];
        const insaneParticleColors = [
            'rgba(26,137,23,0.18)',
            'rgba(180,236,81,0.18)',
            'rgba(26,137,23,0.13)',
            'rgba(255,255,255,0.18)'
        ];
        for (let i = 0; i < 12; i++) {
            const p = document.createElement('div');
            p.className = 'insane-particle';
            p.style.width = `${8 + Math.random() * 18}px`;
            p.style.height = p.style.width;
            p.style.background = insaneParticleColors[Math.floor(Math.random() * insaneParticleColors.length)];
            p.style.left = `${10 + Math.random() * 80}%`;
            p.style.top = `${10 + Math.random() * 80}%`;
            p.style.animationDuration = `${4 + Math.random() * 4}s`;
            document.querySelector('.post-detail-content').appendChild(p);
            insaneParticles.push(p);
        }
        // Show modal
        modal.style.display = 'block';
        setTimeout(() => modal.classList.add('active'), 10);
        document.body.style.overflow = 'hidden';
        // Close logic
        const closeBtn = document.getElementById('close-post-modal');
        if (closeBtn) {
            closeBtn.onclick = () => {
                modal.classList.remove('active');
                setTimeout(() => { modal.style.display = 'none'; }, 300);
                document.body.style.overflow = 'auto';
                // Remove insane particles
                insaneParticles.forEach(p => p.remove());
            };
        }
        // Also close on clicking outside modal-content
        modal.onclick = (e) => {
            if (e.target === modal) {
                modal.classList.remove('active');
                setTimeout(() => { modal.style.display = 'none'; }, 300);
                document.body.style.overflow = 'auto';
                insaneParticles.forEach(p => p.remove());
            }
        };
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

        document.getElementById('total-posts').textContent = formatNumber(stats.totalPosts);
        document.getElementById('total-authors').textContent = formatNumber(stats.totalAuthors);
        document.getElementById('total-views').textContent = formatNumber(stats.totalViews);
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

    startLoadingMessages() {
        // Initialize the first message properly
        this.initializeFirstMessage();
        
        // Start cycling after a delay to avoid immediate repetition
        setTimeout(() => {
            this.cycleLoadingMessage();
            // Change message every 1.2 seconds for 3 messages
            this.messageInterval = setInterval(() => {
                this.cycleLoadingMessage();
            }, 1200);
        }, 1500);
        
        // Add interactive effects to floating cards
        this.addCardInteractions();
        
        // Add subtle parallax effect
        this.addParallaxEffect();
        
        // Add dynamic particle effects
        this.addDynamicParticles();
        
        // Add energy pulse effects
        this.addEnergyPulse();
    }
    
    addDynamicParticles() {
        // Create additional particles dynamically
        setInterval(() => {
            this.createParticle();
        }, 2000);
    }
    

    
    addEnergyPulse() {
        // Create energy pulse effect
        setInterval(() => {
            this.createEnergyPulse();
        }, 1500);
    }
    
    createEnergyPulse() {
        const pulse = document.createElement('div');
        pulse.className = 'energy-pulse';
        pulse.style.cssText = `
            position: absolute;
            top: 50%;
            left: 50%;
            width: 10px;
            height: 10px;
            background: radial-gradient(circle, rgba(255, 255, 255, 0.8) 0%, transparent 70%);
            border-radius: 50%;
            pointer-events: none;
            z-index: 1;
            transform: translate(-50%, -50%);
        `;
        
        document.querySelector('.loading-screen').appendChild(pulse);
        
        // Animate pulse
        const animation = pulse.animate([
            { 
                transform: 'translate(-50%, -50%) scale(0)',
                opacity: 1 
            },
            { 
                transform: 'translate(-50%, -50%) scale(50)',
                opacity: 0 
            }
        ], {
            duration: 2000,
            easing: 'ease-out'
        });
        
        // Remove pulse after animation
        animation.onfinish = () => pulse.remove();
    }
    
    createParticle() {
        const particle = document.createElement('div');
        particle.className = 'dynamic-particle';
        particle.style.cssText = `
            position: absolute;
            width: 3px;
            height: 3px;
            background: rgba(255, 255, 255, 0.6);
            border-radius: 50%;
            pointer-events: none;
            z-index: 1;
        `;
        
        // Random position
        particle.style.left = Math.random() * 100 + '%';
        particle.style.top = '100%';
        
        document.querySelector('.loading-screen').appendChild(particle);
        
        // Animate particle
        const animation = particle.animate([
            { transform: 'translateY(0px)', opacity: 1 },
            { transform: 'translateY(-100vh)', opacity: 0 }
        ], {
            duration: 3000,
            easing: 'ease-out'
        });
        
        // Remove particle after animation
        animation.onfinish = () => particle.remove();
    }
    
    addCardInteractions() {
        const cards = document.querySelectorAll('.floating-card');
        cards.forEach((card, index) => {
            // Add hover effect
            card.addEventListener('mouseenter', () => {
                card.style.transform = 'scale(1.05) rotate(0deg)';
                card.style.zIndex = '10';
            });
            
            card.addEventListener('mouseleave', () => {
                card.style.transform = 'scale(1) rotate(0deg)';
                card.style.zIndex = '1';
            });
            
            // Add click effect
            card.addEventListener('click', () => {
                card.style.transform = 'scale(0.95)';
                setTimeout(() => {
                    card.style.transform = 'scale(1)';
                }, 150);
            });
        });
    }
    
    addParallaxEffect() {
        document.addEventListener('mousemove', (e) => {
            const cards = document.querySelectorAll('.floating-card');
            const mouseX = e.clientX / window.innerWidth;
            const mouseY = e.clientY / window.innerHeight;
            
            cards.forEach((card, index) => {
                const speed = (index + 1) * 0.3;
                const x = (mouseX - 0.5) * speed;
                const y = (mouseY - 0.5) * speed;
                
                // Apply parallax without interfering with existing animations
                card.style.setProperty('--parallax-x', `${x}px`);
                card.style.setProperty('--parallax-y', `${y}px`);
            });
        });
    }

    initializeFirstMessage() {
        const messageElement = document.getElementById('loading-message');
        if (!messageElement) return;
        
        const messageText = messageElement.querySelector('.message-text');
        if (!messageText) return;
        
        // Set the first message from our array
        messageText.textContent = this.enhancedMessages[0];
        
        // Reset the index to start from the beginning
        this.currentMessageIndex = 0;
    }

    startLoadingTimer() {
        // Always wait the full 4 seconds, regardless of when posts load
        this.loadingTimer = setTimeout(() => {
            this.hideLoadingScreen();
        }, 4000);
    }

    cycleLoadingMessage() {
        const messageElement = document.getElementById('loading-message');
        if (!messageElement) return;
        
        // Get the message text element
        const messageText = messageElement.querySelector('.message-text');
        if (!messageText) return;
        
        // Create insane exit animation
        messageText.style.animation = 'none';
        messageText.style.transform = 'scale(1.2) rotate(5deg)';
        messageText.style.filter = 'blur(3px)';
        messageElement.style.opacity = '0';
        
        setTimeout(() => {
            // Update message with enhanced version
            this.currentMessageIndex = (this.currentMessageIndex + 1) % this.enhancedMessages.length;
            
            // If we've shown all messages, don't cycle further
            if (this.currentMessageIndex === 0) {
                // Keep the last message visible
                messageText.textContent = this.enhancedMessages[2];
                this.currentMessageIndex = 2;
            } else {
                messageText.textContent = this.enhancedMessages[this.currentMessageIndex];
            }
            
            // Reset styles
            messageText.style.transform = 'scale(0.8) rotate(-5deg)';
            messageText.style.filter = 'blur(0px)';
            messageElement.style.opacity = '1';
            
            // Add insane entrance animation
            messageText.style.animation = 'messageEntrance 0.6s ease-out forwards';
            
            // Create explosion effect
            this.createMessageExplosion(messageElement);
            
            // Reset animation after entrance
            setTimeout(() => {
                messageText.style.animation = 'messageGlow 2s ease-in-out infinite';
            }, 600);
        }, 300);
    }
    
    createMessageExplosion() {
        // Create particle explosion effect
        for (let i = 0; i < 8; i++) {
            const particle = document.createElement('div');
            particle.className = 'explosion-particle';
            particle.style.cssText = `
                position: absolute;
                width: 6px;
                height: 6px;
                background: linear-gradient(135deg, #667eea, #764ba2, #4facfe);
                border-radius: 50%;
                pointer-events: none;
                z-index: 10;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                box-shadow: 0 0 12px rgba(102, 126, 234, 0.6);
            `;
            
            document.querySelector('.loading-screen').appendChild(particle);
            
            // Random direction
            const angle = (i / 8) * Math.PI * 2;
            const distance = 50 + Math.random() * 30;
            const x = Math.cos(angle) * distance;
            const y = Math.sin(angle) * distance;
            
            // Animate explosion
            const animation = particle.animate([
                { 
                    transform: 'translate(-50%, -50%) scale(1)',
                    opacity: 1 
                },
                { 
                    transform: `translate(calc(-50% + ${x}px), calc(-50% + ${y}px)) scale(0)`,
                    opacity: 0 
                }
            ], {
                duration: 800,
                easing: 'ease-out'
            });
            
            // Remove particle after animation
            animation.onfinish = () => particle.remove();
        }
    }

    hideLoadingScreen() {
        // Clear the message interval
        if (this.messageInterval) {
            clearInterval(this.messageInterval);
        }
        
        // Clear the loading timer
        if (this.loadingTimer) {
            clearTimeout(this.loadingTimer);
        }
        
        // Hide the loading screen immediately
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            loadingScreen.classList.add('hidden');
            // Also set display to none as a fallback
            loadingScreen.style.display = 'none';
        }
    }
    
    // Method to reset loading screen state (for testing or manual reset)
    resetLoadingScreen() {
        sessionStorage.removeItem('blogify_loading_seen');
        location.reload();
    }
    
    // Method to manually show loading screen again (for testing)
    showLoadingScreenAgain() {
        sessionStorage.removeItem('blogify_loading_seen');
        const loadingScreen = document.getElementById('loading-screen');
        if (loadingScreen) {
            loadingScreen.classList.remove('hidden');
        }
        this.startLoadingMessages();
        this.startLoadingTimer();
        sessionStorage.setItem('blogify_loading_seen', 'true');
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