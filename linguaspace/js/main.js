// LinguaSpace - Main Application
// Initializes the application and handles global functionality

// ========== INITIALIZATION ==========

document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
});

function initializeApp() {
    // Initialize filters
    initializeFilters();

    // Render initial content
    renderFeaturedPost();
    renderCategories();
    renderStats();
    renderTrendingTopics();

    // Apply initial filters (shows all posts)
    applyFilters();

    // Setup event listeners
    setupEventListeners();

    // Setup modal close handlers
    setupModals();

    // Generate initial anonymous username
    generateAnonymousUsername();

    console.log('🗣️ LinguaSpace initialized successfully!');
}

// ========== EVENT LISTENERS ==========

function setupEventListeners() {
    // Share story button
    document.getElementById('shareStoryBtn').addEventListener('click', openShareModal);

    // Navigation links
    document.querySelectorAll('.nav-link').forEach(link => {
        link.addEventListener('click', handleNavigation);
    });

    // Quick links in sidebar
    document.querySelectorAll('.links-list a').forEach(link => {
        link.addEventListener('click', handleNavigation);
    });

    // Share story form
    document.getElementById('shareStoryForm').addEventListener('submit', handleStorySubmission);

    // Username regenerate button
    document.getElementById('regenerateUsername').addEventListener('click', generateAnonymousUsername);

    // Character counters
    document.getElementById('storyTitle').addEventListener('input', updateCharCount);
    document.getElementById('storyContent').addEventListener('input', updateCharCount);
}

// ========== NAVIGATION ==========

function handleNavigation(event) {
    event.preventDefault();
    const page = event.target.dataset.page;

    // Update active nav link
    document.querySelectorAll('.nav-link').forEach(link => {
        link.classList.remove('active');
    });
    if (event.target.classList.contains('nav-link')) {
        event.target.classList.add('active');
    }

    // Hide all pages
    document.getElementById('heroSection').style.display = 'none';
    document.getElementById('categoriesSection').style.display = 'none';
    document.getElementById('filterBar').style.display = 'none';
    document.getElementById('activeFilters').style.display = 'none';
    document.querySelector('.posts-section').style.display = 'none';
    document.getElementById('aboutPage').style.display = 'none';
    document.getElementById('guidelinesPage').style.display = 'none';

    // Show selected page
    switch (page) {
        case 'home':
            document.getElementById('heroSection').style.display = 'block';
            document.getElementById('categoriesSection').style.display = 'block';
            document.getElementById('filterBar').style.display = 'flex';
            document.getElementById('activeFilters').style.display = 'flex';
            document.querySelector('.posts-section').style.display = 'block';
            break;

        case 'categories':
            document.getElementById('categoriesSection').style.display = 'block';
            document.getElementById('filterBar').style.display = 'flex';
            document.getElementById('activeFilters').style.display = 'flex';
            document.querySelector('.posts-section').style.display = 'block';
            break;

        case 'about':
            document.getElementById('aboutPage').style.display = 'block';
            break;

        case 'guidelines':
            document.getElementById('guidelinesPage').style.display = 'block';
            break;
    }

    // Scroll to top
    window.scrollTo({ top: 0, behavior: 'smooth' });
}

// ========== MODALS ==========

function setupModals() {
    // Close buttons
    document.querySelectorAll('.modal-close').forEach(button => {
        button.addEventListener('click', () => {
            closeAllModals();
        });
    });

    // Click outside modal to close
    document.querySelectorAll('.modal').forEach(modal => {
        modal.addEventListener('click', (event) => {
            if (event.target === modal) {
                closeAllModals();
            }
        });
    });

    // Escape key to close modals
    document.addEventListener('keydown', (event) => {
        if (event.key === 'Escape') {
            closeAllModals();
        }
    });
}

function closeAllModals() {
    document.querySelectorAll('.modal').forEach(modal => {
        modal.classList.remove('show');
    });
    document.body.style.overflow = 'auto';
}

// ========== SHARE STORY MODAL ==========

function openShareModal() {
    const modal = document.getElementById('shareModal');
    modal.classList.add('show');
    document.body.style.overflow = 'hidden';

    // Reset form
    document.getElementById('shareStoryForm').reset();
    generateAnonymousUsername();
}

function closeShareModal() {
    const modal = document.getElementById('shareModal');
    modal.classList.remove('show');
    document.body.style.overflow = 'auto';
}

// Generate anonymous username
function generateAnonymousUsername() {
    const adjectives = ['Multilingual', 'Bilingual', 'Trilingual', 'Linguistic', 'Global', 'International', 'Cultural', 'Diverse', 'Polyglot', 'Transnational'];
    const nouns = ['Student', 'Scholar', 'Voice', 'Soul', 'Identity', 'Nomad', 'Citizen', 'Explorer', 'Thinker', 'Speaker'];
    const number = Math.floor(Math.random() * 100);

    const username = `${adjectives[Math.floor(Math.random() * adjectives.length)]}${nouns[Math.floor(Math.random() * nouns.length)]}_${number}`;

    document.getElementById('anonymousUsername').value = username;
}

// Update character count
function updateCharCount(event) {
    const input = event.target;
    const maxLength = input.getAttribute('maxlength');
    const currentLength = input.value.length;
    const counterId = input.id + 'Count';
    const counter = document.getElementById(counterId);

    if (counter) {
        counter.textContent = currentLength;

        // Change color if near limit
        if (currentLength > maxLength * 0.9) {
            counter.style.color = 'var(--accent-color)';
        } else {
            counter.style.color = 'var(--text-secondary)';
        }
    }
}

// Handle story submission
function handleStorySubmission(event) {
    event.preventDefault();

    // Get form data
    const category = document.getElementById('storyCategory').value;
    const title = document.getElementById('storyTitle').value;
    const content = document.getElementById('storyContent').value;
    const username = document.getElementById('anonymousUsername').value;
    const experienceType = document.getElementById('experienceType').value;

    // Get selected languages
    const languages = Array.from(document.querySelectorAll('input[name="language"]:checked'))
        .map(checkbox => checkbox.value);

    if (languages.length === 0) {
        showToast('⚠️ Please select at least one language', 'error');
        return;
    }

    // Create new post
    const newPost = {
        id: window.linguaSpaceData.posts.length + 1,
        category: category,
        username: username,
        title: title,
        content: content,
        languages: languages,
        experienceType: experienceType,
        upvotes: 1,
        downvotes: 0,
        commentCount: 0,
        timePosted: new Date().toISOString(),
        academicConcept: null,
        translanguaging: languages.length > 1,
        featured: false
    };

    // Add to posts array
    window.linguaSpaceData.posts.unshift(newPost);

    // Save to localStorage
    saveUserPost(newPost);

    // Show success animation
    showSuccessConfetti();

    // Close modal
    setTimeout(() => {
        closeShareModal();

        // Navigate to home and refresh
        document.querySelector('.nav-link[data-page="home"]').click();
        applyFilters();

        // Show success toast
        showToast('🎉 Your story has been shared! Thank you for contributing.', 'success');
    }, 1500);
}

// Save user post to localStorage
function saveUserPost(post) {
    const userPosts = JSON.parse(localStorage.getItem('linguaspace_user_posts') || '[]');
    userPosts.push(post);
    localStorage.setItem('linguaspace_user_posts', JSON.stringify(userPosts));
}

// Show success confetti
function showSuccessConfetti() {
    const colors = ['#FF6B6B', '#5865F2', '#2ECC71', '#FFD700', '#9B59B6'];

    for (let i = 0; i < 50; i++) {
        setTimeout(() => {
            const confetti = document.createElement('div');
            confetti.className = 'confetti';
            confetti.style.left = Math.random() * 100 + '%';
            confetti.style.background = colors[Math.floor(Math.random() * colors.length)];
            confetti.style.animationDelay = Math.random() * 0.5 + 's';
            confetti.style.animationDuration = (Math.random() * 2 + 2) + 's';
            document.body.appendChild(confetti);

            setTimeout(() => confetti.remove(), 5000);
        }, i * 30);
    }
}

// ========== ACADEMIC CONCEPTS ==========

function showAcademicConcepts() {
    // Scroll to about section or show modal with concepts
    document.querySelector('.nav-link[data-page="about"]').click();
    setTimeout(() => {
        document.querySelector('.concept-card').scrollIntoView({ behavior: 'smooth' });
    }, 100);
}

function showResources() {
    showToast('📚 Resources section coming soon! This is a demo.', 'info');
}

// ========== UTILITY FUNCTIONS ==========

// Load user posts from localStorage
function loadUserPosts() {
    const userPosts = JSON.parse(localStorage.getItem('linguaspace_user_posts') || '[]');

    // Merge user posts with default posts (user posts first)
    if (userPosts.length > 0) {
        window.linguaSpaceData.posts = [...userPosts, ...window.linguaSpaceData.posts.filter(
            p => !userPosts.some(up => up.id === p.id)
        )];
    }
}

// Check if user has visited before
function checkFirstVisit() {
    const hasVisited = localStorage.getItem('linguaspace_visited');

    if (!hasVisited) {
        // First visit - show welcome message
        setTimeout(() => {
            showToast('👋 Welcome to LinguaSpace! Share your linguistic identity story.', 'success');
        }, 1000);

        localStorage.setItem('linguaspace_visited', 'true');
    }
}

// Load user posts on init
loadUserPosts();
checkFirstVisit();

// ========== KEYBOARD NAVIGATION ==========

document.addEventListener('keydown', (event) => {
    // Ctrl/Cmd + K for search
    if ((event.ctrlKey || event.metaKey) && event.key === 'k') {
        event.preventDefault();
        document.getElementById('searchInput').focus();
    }

    // Ctrl/Cmd + N for new post
    if ((event.ctrlKey || event.metaKey) && event.key === 'n') {
        event.preventDefault();
        openShareModal();
    }
});

// ========== EXPORT FUNCTIONS ==========

window.openShareModal = openShareModal;
window.closeShareModal = closeShareModal;
window.generateAnonymousUsername = generateAnonymousUsername;
window.showAcademicConcepts = showAcademicConcepts;
window.showResources = showResources;
window.closeAllModals = closeAllModals;

console.log('%c🗣️ LinguaSpace', 'font-size: 24px; font-weight: bold; color: #5865F2;');
console.log('%cWhere Multilingual Voices Find Community', 'font-size: 14px; color: #7F8C8D;');
console.log('\nKeyboard Shortcuts:');
console.log('  Ctrl/Cmd + K: Focus search');
console.log('  Ctrl/Cmd + N: New post');
console.log('  Escape: Close modals');
