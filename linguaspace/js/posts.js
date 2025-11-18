// LinguaSpace - Posts System
// Handles post display and rendering

let currentPosts = [];
let displayedPostCount = 10;
const POSTS_PER_LOAD = 10;

// Render post card
function renderPostCard(post) {
    const category = window.linguaSpaceData.categories.find(c => c.id === post.category);
    const userVote = votingSystem.getPostVote(post.id);
    const voteCount = votingSystem.calculateVoteCount(
        post.upvotes,
        post.downvotes,
        userVote
    );

    return `
        <article class="post-card" data-post-id="${post.id}" onclick="openPostDetail(${post.id})">
            <div class="vote-section">
                <button
                    class="vote-btn upvote ${userVote === 'up' ? 'voted' : ''}"
                    onclick="handlePostVote(${post.id}, 'up', event)"
                    aria-label="Upvote post">
                    ⬆
                </button>
                <span class="vote-count">${voteCount}</span>
                <button
                    class="vote-btn downvote ${userVote === 'down' ? 'voted' : ''}"
                    onclick="handlePostVote(${post.id}, 'down', event)"
                    aria-label="Downvote post">
                    ⬇
                </button>
            </div>

            <div class="post-content">
                <div class="post-header">
                    <span class="post-category">${category.icon} ${category.name}</span>
                    <div class="post-meta">
                        <span class="post-username">u/${post.username}</span>
                        <span class="post-time">${timeAgo(post.timePosted)}</span>
                    </div>
                    ${post.featured ? '<span class="featured-badge">⭐ Story of the Week</span>' : ''}
                </div>

                <h3 class="post-title">${escapeHtml(post.title)}</h3>

                <p class="post-preview">${escapeHtml(post.content)}</p>

                <div class="post-tags">
                    ${post.languages.map(lang => `<span class="tag language-tag">🏷️ ${lang}</span>`).join('')}
                    ${post.academicConcept ? `<span class="tag concept-tag">💡 ${post.academicConcept}</span>` : ''}
                    ${post.translanguaging ? '<span class="tag experience-tag">🌐 Translanguaging</span>' : ''}
                </div>

                <div class="post-actions">
                    <button class="post-action" onclick="openPostDetail(${post.id}, event)">
                        💬 ${post.commentCount} comments
                    </button>
                    <button class="post-action" onclick="sharePost(${post.id}, event)">
                        📤 Share
                    </button>
                    <button class="post-action" onclick="savePost(${post.id}, event)">
                        🔖 Save
                    </button>
                </div>
            </div>
        </article>
    `;
}

// Render posts feed
function renderPostsFeed(posts) {
    const postsFeed = document.getElementById('postsFeed');
    const postsToShow = posts.slice(0, displayedPostCount);

    if (posts.length === 0) {
        postsFeed.innerHTML = `
            <div class="empty-state">
                <div class="empty-state-icon">🔍</div>
                <h3>No stories found</h3>
                <p>Try adjusting your filters or search terms.</p>
            </div>
        `;
        document.getElementById('loadMoreBtn').style.display = 'none';
        return;
    }

    postsFeed.innerHTML = postsToShow.map(post => renderPostCard(post)).join('');

    // Show/hide load more button
    const loadMoreBtn = document.getElementById('loadMoreBtn');
    loadMoreBtn.style.display = displayedPostCount < posts.length ? 'block' : 'none';

    // Add staggered animation
    setTimeout(() => {
        const cards = postsFeed.querySelectorAll('.post-card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in-up');
            }, index * 50);
        });
    }, 10);
}

// Load more posts
function loadMorePosts() {
    displayedPostCount += POSTS_PER_LOAD;
    renderPostsFeed(currentPosts);
}

// Render categories grid
function renderCategories() {
    const categoriesGrid = document.getElementById('categoriesGrid');
    const categories = window.linguaSpaceData.categories;

    categoriesGrid.innerHTML = categories.map(category => {
        const categoryPosts = window.linguaSpaceData.posts.filter(p => p.category === category.id);
        const hotPost = categoryPosts.sort((a, b) => b.upvotes - a.upvotes)[0];

        return `
            <div class="category-card" data-category="${category.id}" onclick="filterByCategory('${category.id}')">
                <div class="category-header">
                    <span class="category-icon">${category.icon}</span>
                    <h4 class="category-name">${category.name}</h4>
                </div>
                <p class="category-description">${category.description}</p>
                <div class="category-stats">
                    <span class="category-post-count">📊 ${categoryPosts.length} posts</span>
                    ${hotPost ? `<span class="category-hot">🔥 ${hotPost.title}</span>` : ''}
                </div>
            </div>
        `;
    }).join('');

    // Add staggered animation
    setTimeout(() => {
        const cards = categoriesGrid.querySelectorAll('.category-card');
        cards.forEach((card, index) => {
            setTimeout(() => {
                card.classList.add('fade-in-up');
            }, index * 80);
        });
    }, 10);
}

// Render featured post
function renderFeaturedPost() {
    const featuredPost = window.linguaSpaceData.posts.find(p => p.featured);
    if (!featuredPost) return;

    const container = document.getElementById('featuredPostContainer');
    container.innerHTML = renderPostCard(featuredPost);
}

// Open post detail modal
function openPostDetail(postId, event) {
    if (event) {
        event.stopPropagation();
    }

    const post = window.linguaSpaceData.posts.find(p => p.id === postId);
    if (!post) return;

    const category = window.linguaSpaceData.categories.find(c => c.id === post.category);
    const userVote = votingSystem.getPostVote(post.id);
    const voteCount = votingSystem.calculateVoteCount(
        post.upvotes,
        post.downvotes,
        userVote
    );

    const modal = document.getElementById('postModal');
    modal.dataset.postId = postId;

    const detailContainer = document.getElementById('postDetailContainer');
    detailContainer.innerHTML = `
        <div class="post-detail" data-post-id="${post.id}">
            <div class="post-header">
                <span class="post-category">${category.icon} ${category.name}</span>
                <div class="post-meta">
                    <span class="post-username">u/${post.username}</span>
                    <span class="post-time">${timeAgo(post.timePosted)}</span>
                </div>
            </div>

            <h2 class="post-title" id="postModalTitle">${escapeHtml(post.title)}</h2>

            <div class="post-content-full">${escapeHtml(post.content)}</div>

            <div class="post-tags">
                ${post.languages.map(lang => `<span class="tag language-tag">🏷️ ${lang}</span>`).join('')}
                ${post.academicConcept ? `<span class="tag concept-tag">💡 ${post.academicConcept}</span>` : ''}
                ${post.translanguaging ? '<span class="tag experience-tag">🌐 Translanguaging</span>' : ''}
            </div>

            <div class="post-actions">
                <div class="vote-section" style="flex-direction: row;">
                    <button
                        class="vote-btn upvote ${userVote === 'up' ? 'voted' : ''}"
                        onclick="handlePostVote(${post.id}, 'up', event)"
                        aria-label="Upvote post">
                        ⬆
                    </button>
                    <span class="vote-count">${voteCount}</span>
                    <button
                        class="vote-btn downvote ${userVote === 'down' ? 'voted' : ''}"
                        onclick="handlePostVote(${post.id}, 'down', event)"
                        aria-label="Downvote post">
                        ⬇
                    </button>
                </div>
                <button class="post-action" onclick="sharePost(${post.id}, event)">
                    📤 Share
                </button>
                <button class="post-action" onclick="savePost(${post.id}, event)">
                    🔖 Save
                </button>
            </div>
        </div>
    `;

    // Render comments
    renderComments(postId, 'best');

    // Show modal
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';
}

// Close post detail modal
function closePostModal() {
    const modal = document.getElementById('postModal');
    modal.classList.remove('show');
    document.body.style.overflow = 'auto';
}

// Share post (placeholder)
function sharePost(postId, event) {
    event.stopPropagation();
    const post = window.linguaSpaceData.posts.find(p => p.id === postId);
    if (post) {
        showToast('🔗 Link copied to clipboard! (Demo)', 'success');
    }
}

// Save post (placeholder)
function savePost(postId, event) {
    event.stopPropagation();
    const saved = JSON.parse(localStorage.getItem('linguaspace_saved') || '[]');

    if (saved.includes(postId)) {
        const index = saved.indexOf(postId);
        saved.splice(index, 1);
        showToast('🔖 Post unsaved', 'info');
    } else {
        saved.push(postId);
        showToast('🔖 Post saved!', 'success');
    }

    localStorage.setItem('linguaspace_saved', JSON.stringify(saved));
}

// Render stats
function renderStats() {
    const totalPosts = window.linguaSpaceData.posts.length;
    const totalComments = window.linguaSpaceData.comments.length;

    document.getElementById('totalPosts').textContent = totalPosts;
    document.getElementById('totalComments').textContent = totalComments;
}

// Render trending topics
function renderTrendingTopics() {
    const trendingList = document.getElementById('trendingTopics');
    trendingList.innerHTML = window.linguaSpaceData.trendingTopics.map(topic => `
        <li>
            <span class="trending-tag">${topic.tag}</span>
            <span class="trending-count">${topic.count} stories</span>
        </li>
    `).join('');
}

// Export functions
window.renderPostCard = renderPostCard;
window.renderPostsFeed = renderPostsFeed;
window.loadMorePosts = loadMorePosts;
window.renderCategories = renderCategories;
window.renderFeaturedPost = renderFeaturedPost;
window.openPostDetail = openPostDetail;
window.closePostModal = closePostModal;
window.sharePost = sharePost;
window.savePost = savePost;
window.renderStats = renderStats;
window.renderTrendingTopics = renderTrendingTopics;
window.currentPosts = currentPosts;
