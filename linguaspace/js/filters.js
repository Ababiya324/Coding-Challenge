// LinguaSpace - Filters & Sorting System
// Handles post filtering, sorting, and search

let activeFilters = {
    category: 'all',
    language: 'all',
    experience: 'all',
    search: ''
};

let currentSort = 'hot';

// Filter posts based on active filters
function filterPosts() {
    let filtered = [...window.linguaSpaceData.posts];

    // Category filter
    if (activeFilters.category !== 'all') {
        filtered = filtered.filter(p => p.category === activeFilters.category);
    }

    // Language filter
    if (activeFilters.language !== 'all') {
        filtered = filtered.filter(p =>
            p.languages.includes(activeFilters.language) ||
            (activeFilters.language === 'Multilingual' && p.languages.length > 1)
        );
    }

    // Experience filter
    if (activeFilters.experience !== 'all') {
        filtered = filtered.filter(p => p.experienceType === activeFilters.experience);
    }

    // Search filter
    if (activeFilters.search) {
        const searchLower = activeFilters.search.toLowerCase();
        filtered = filtered.filter(p =>
            p.title.toLowerCase().includes(searchLower) ||
            p.content.toLowerCase().includes(searchLower) ||
            p.username.toLowerCase().includes(searchLower) ||
            p.languages.some(lang => lang.toLowerCase().includes(searchLower))
        );
    }

    return filtered;
}

// Sort posts
function sortPosts(posts, sortMethod) {
    const sorted = [...posts];

    switch (sortMethod) {
        case 'new':
            return sorted.sort((a, b) =>
                new Date(b.timePosted) - new Date(a.timePosted)
            );

        case 'top-week':
        case 'top-month':
        case 'top-all':
            return sorted.sort((a, b) => {
                const aVote = votingSystem.getPostVote(a.id);
                const bVote = votingSystem.getPostVote(b.id);
                const aCount = votingSystem.calculateVoteCount(a.upvotes, a.downvotes, aVote);
                const bCount = votingSystem.calculateVoteCount(b.upvotes, b.downvotes, bVote);
                return bCount - aCount;
            });

        case 'hot':
        default:
            // Hot algorithm: combines votes and recency
            return sorted.sort((a, b) => {
                const aVote = votingSystem.getPostVote(a.id);
                const bVote = votingSystem.getPostVote(b.id);
                const aScore = votingSystem.calculateVoteCount(a.upvotes, a.downvotes, aVote);
                const bScore = votingSystem.calculateVoteCount(b.upvotes, b.downvotes, bVote);

                const aAge = (Date.now() - new Date(a.timePosted)) / (1000 * 60 * 60); // hours
                const bAge = (Date.now() - new Date(b.timePosted)) / (1000 * 60 * 60);

                const aHot = aScore / Math.pow(aAge + 2, 1.5);
                const bHot = bScore / Math.pow(bAge + 2, 1.5);

                return bHot - aHot;
            });
    }
}

// Apply filters and update display
function applyFilters() {
    // Filter posts
    let filtered = filterPosts();

    // Sort posts
    filtered = sortPosts(filtered, currentSort);

    // Update display
    window.currentPosts = filtered;
    displayedPostCount = POSTS_PER_LOAD;
    renderPostsFeed(filtered);

    // Update active filters display
    updateActiveFiltersDisplay();
}

// Update active filters display
function updateActiveFiltersDisplay() {
    const container = document.getElementById('activeFilters');
    const filters = [];

    if (activeFilters.category !== 'all') {
        const category = window.linguaSpaceData.categories.find(c => c.id === activeFilters.category);
        if (category) {
            filters.push({ key: 'category', label: category.name });
        }
    }

    if (activeFilters.language !== 'all') {
        filters.push({ key: 'language', label: `Language: ${activeFilters.language}` });
    }

    if (activeFilters.experience !== 'all') {
        filters.push({ key: 'experience', label: `Type: ${activeFilters.experience}` });
    }

    if (activeFilters.search) {
        filters.push({ key: 'search', label: `Search: "${activeFilters.search}"` });
    }

    if (filters.length === 0) {
        container.innerHTML = '';
        return;
    }

    container.innerHTML = filters.map(filter => `
        <span class="filter-tag">
            ${filter.label}
            <button onclick="removeFilter('${filter.key}')" aria-label="Remove filter">×</button>
        </span>
    `).join('');
}

// Remove specific filter
function removeFilter(filterKey) {
    if (filterKey === 'category') {
        activeFilters.category = 'all';
        document.getElementById('categoryFilter').value = 'all';
    } else if (filterKey === 'language') {
        activeFilters.language = 'all';
        document.getElementById('languageFilter').value = 'all';
    } else if (filterKey === 'experience') {
        activeFilters.experience = 'all';
        document.getElementById('experienceFilter').value = 'all';
    } else if (filterKey === 'search') {
        activeFilters.search = '';
        document.getElementById('searchInput').value = '';
    }

    applyFilters();
}

// Clear all filters
function clearAllFilters() {
    activeFilters = {
        category: 'all',
        language: 'all',
        experience: 'all',
        search: ''
    };

    document.getElementById('categoryFilter').value = 'all';
    document.getElementById('languageFilter').value = 'all';
    document.getElementById('experienceFilter').value = 'all';
    document.getElementById('searchInput').value = '';

    applyFilters();
    showToast('🔄 Filters cleared', 'info');
}

// Handle category filter change
function handleCategoryFilter(event) {
    activeFilters.category = event.target.value;
    applyFilters();
}

// Handle language filter change
function handleLanguageFilter(event) {
    activeFilters.language = event.target.value;
    applyFilters();
}

// Handle experience filter change
function handleExperienceFilter(event) {
    activeFilters.experience = event.target.value;
    applyFilters();
}

// Handle search input
function handleSearch(event) {
    activeFilters.search = event.target.value;
    applyFilters();
}

// Handle sort change
function handleSortChange(event) {
    currentSort = event.target.value;
    applyFilters();
}

// Filter by category (from category card click)
function filterByCategory(categoryId) {
    activeFilters.category = categoryId;
    document.getElementById('categoryFilter').value = categoryId;

    // Scroll to posts section
    document.getElementById('filterBar').scrollIntoView({ behavior: 'smooth' });

    applyFilters();
}

// Initialize filters
function initializeFilters() {
    // Category filter
    document.getElementById('categoryFilter').addEventListener('change', handleCategoryFilter);

    // Language filter
    document.getElementById('languageFilter').addEventListener('change', handleLanguageFilter);

    // Experience filter
    document.getElementById('experienceFilter').addEventListener('change', handleExperienceFilter);

    // Search input with debounce
    let searchTimeout;
    document.getElementById('searchInput').addEventListener('input', (event) => {
        clearTimeout(searchTimeout);
        searchTimeout = setTimeout(() => handleSearch(event), 300);
    });

    // Sort select
    document.getElementById('sortSelect').addEventListener('change', handleSortChange);

    // Clear filters button
    document.getElementById('clearFilters').addEventListener('click', clearAllFilters);

    // Load more button
    document.getElementById('loadMoreBtn').addEventListener('click', loadMorePosts);

    // Comment sort
    document.getElementById('commentSort').addEventListener('change', handleCommentSort);
}

// Export functions
window.applyFilters = applyFilters;
window.filterByCategory = filterByCategory;
window.removeFilter = removeFilter;
window.clearAllFilters = clearAllFilters;
window.initializeFilters = initializeFilters;
