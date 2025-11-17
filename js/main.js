/**
 * Language Identity Map - Main Application Logic
 * Handles filtering, form submission, and app initialization
 */

// Initialize app when DOM is loaded
document.addEventListener('DOMContentLoaded', () => {
    initializeApp();
    setupEventListeners();
    loadStoredStories();
});

/**
 * Initialize the application
 */
function initializeApp() {
    // Initialize map with all stories
    initializeMap();

    // Setup scroll reveal animations
    setupScrollReveal();

    // Load any stories from localStorage
    loadStoredStories();
}

/**
 * Setup all event listeners
 */
function setupEventListeners() {
    // Filter controls
    const experienceFilter = document.getElementById('experienceFilter');
    const languageFilter = document.getElementById('languageFilter');
    const backgroundFilter = document.getElementById('backgroundFilter');

    if (experienceFilter) {
        experienceFilter.addEventListener('change', applyFilters);
    }
    if (languageFilter) {
        languageFilter.addEventListener('change', applyFilters);
    }
    if (backgroundFilter) {
        backgroundFilter.addEventListener('change', applyFilters);
    }

    // Contribution form
    const contributionForm = document.getElementById('contributionForm');
    if (contributionForm) {
        contributionForm.addEventListener('submit', handleFormSubmission);
    }

    // Map location clicks (for accessibility)
    setupMapLocationHandlers();
}

/**
 * Setup handlers for map locations
 */
function setupMapLocationHandlers() {
    const locations = document.querySelectorAll('.map-location');

    locations.forEach(location => {
        location.setAttribute('role', 'button');
        location.setAttribute('tabindex', '0');

        const locationName = location.getAttribute('data-location');

        location.addEventListener('click', () => {
            handleLocationClick(locationName);
        });

        location.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                handleLocationClick(locationName);
            }
        });
    });
}

/**
 * Handle click on map location
 * @param {string} locationName - Name of the location
 */
function handleLocationClick(locationName) {
    // Find stories at this location
    const locationStories = currentStories.filter(s => s.location === locationName);

    if (locationStories.length > 0) {
        showLocationStories(locationName, locationStories);
    } else {
        // Show message if no stories at this location
        alert(`No stories at ${locationName} match the current filters.`);
    }
}

/**
 * Apply filters to stories
 */
function applyFilters() {
    const experienceType = document.getElementById('experienceFilter').value;
    const language = document.getElementById('languageFilter').value;
    const background = document.getElementById('backgroundFilter').value;

    // Start with all stories
    let filtered = [...stories];

    // Apply experience type filter
    if (experienceType !== 'all') {
        filtered = filtered.filter(story => story.experienceType === experienceType);
    }

    // Apply language filter
    if (language !== 'all') {
        if (language === 'Multilingual') {
            filtered = filtered.filter(story => story.languages.length > 1);
        } else {
            filtered = filtered.filter(story => story.languages.includes(language));
        }
    }

    // Apply background filter
    if (background !== 'all') {
        filtered = filtered.filter(story => story.background === background);
    }

    // Update current stories
    currentStories = filtered;

    // Re-render map and statistics
    renderStoryPins(filtered);
    updateStatistics(filtered);
    updateResultsCounter(filtered.length, stories.length);

    // If in list view, update list
    const listView = document.getElementById('listView');
    if (listView && !listView.classList.contains('hidden')) {
        renderStoryList(filtered);
    }
}

/**
 * Reset all filters
 */
function resetFilters() {
    document.getElementById('experienceFilter').value = 'all';
    document.getElementById('languageFilter').value = 'all';
    document.getElementById('backgroundFilter').value = 'all';

    // Reapply filters (will show all stories)
    applyFilters();
}

/**
 * Handle contribution form submission
 * @param {Event} e - Form submit event
 */
function handleFormSubmission(e) {
    e.preventDefault();

    // Get form data
    const formData = {
        id: Date.now(), // Simple unique ID
        studentProfile: document.getElementById('studentProfile').value.trim(),
        location: document.getElementById('location').value,
        experienceType: document.getElementById('experienceType').value,
        languages: document.getElementById('languages').value.split(',').map(l => l.trim()),
        story: document.getElementById('story').value.trim(),
        coordinates: locationCoordinates[document.getElementById('location').value],
        academicConcept: 'User Contribution',
        timestamp: new Date().toISOString().split('T')[0],
        background: 'International' // Default for user submissions
    };

    // Validate
    if (!formData.studentProfile || !formData.location || !formData.experienceType ||
        formData.languages.length === 0 || !formData.story) {
        showFormError('Please fill in all required fields.');
        return;
    }

    // Save to localStorage
    saveStoryToLocalStorage(formData);

    // Add to stories array
    stories.push(formData);
    currentStories.push(formData);

    // Re-render map
    renderStoryPins(currentStories);
    updateStatistics(currentStories);
    updateResultsCounter(currentStories.length, stories.length);

    // Show success message
    showSuccessMessage();

    // Reset form
    document.getElementById('contributionForm').reset();

    // Scroll to map to see the new story
    setTimeout(() => {
        scrollToMap();
    }, 2000);
}

/**
 * Save story to localStorage
 * @param {Object} story - Story object to save
 */
function saveStoryToLocalStorage(story) {
    try {
        const stored = localStorage.getItem('userStories');
        const userStories = stored ? JSON.parse(stored) : [];
        userStories.push(story);
        localStorage.setItem('userStories', JSON.stringify(userStories));
    } catch (error) {
        console.error('Error saving to localStorage:', error);
    }
}

/**
 * Load stories from localStorage
 */
function loadStoredStories() {
    try {
        const stored = localStorage.getItem('userStories');
        if (stored) {
            const userStories = JSON.parse(stored);
            userStories.forEach(story => {
                // Check if story already exists (avoid duplicates)
                if (!stories.find(s => s.id === story.id)) {
                    stories.push(story);
                    currentStories.push(story);
                }
            });

            // Re-render if we loaded any stories
            if (userStories.length > 0) {
                renderStoryPins(currentStories);
                updateStatistics(currentStories);
                updateResultsCounter(currentStories.length, stories.length);
            }
        }
    } catch (error) {
        console.error('Error loading from localStorage:', error);
    }
}

/**
 * Show form error message
 * @param {string} message - Error message to display
 */
function showFormError(message) {
    // Create or update error message
    let errorDiv = document.querySelector('.form-error');
    if (!errorDiv) {
        errorDiv = document.createElement('div');
        errorDiv.className = 'form-error shake';
        errorDiv.style.cssText = 'background-color: #fee; color: #c00; padding: 1rem; border-radius: 8px; margin-bottom: 1rem; border-left: 4px solid #c00;';
        const form = document.getElementById('contributionForm');
        form.insertBefore(errorDiv, form.firstChild);
    }

    errorDiv.textContent = message;

    // Remove after 5 seconds
    setTimeout(() => {
        errorDiv.remove();
    }, 5000);
}

/**
 * Show success message after form submission
 */
function showSuccessMessage() {
    const successMessage = document.getElementById('successMessage');
    if (successMessage) {
        successMessage.classList.remove('hidden');

        // Hide after 5 seconds
        setTimeout(() => {
            successMessage.classList.add('hidden');
        }, 5000);
    }
}

/**
 * Setup scroll reveal animations
 */
function setupScrollReveal() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('revealed');
            }
        });
    }, observerOptions);

    // Observe sections
    const sections = document.querySelectorAll('.about-section, .contribution-section');
    sections.forEach(section => {
        section.classList.add('scroll-reveal');
        observer.observe(section);
    });
}

/**
 * Setup tooltip interactions
 */
function setupTooltips() {
    const tooltips = document.querySelectorAll('.tooltip');

    tooltips.forEach(tooltip => {
        tooltip.addEventListener('mouseenter', (e) => {
            const tooltipText = tooltip.querySelector('.tooltip-text');
            if (tooltipText) {
                tooltipText.style.visibility = 'visible';
                tooltipText.style.opacity = '1';
            }
        });

        tooltip.addEventListener('mouseleave', (e) => {
            const tooltipText = tooltip.querySelector('.tooltip-text');
            if (tooltipText) {
                tooltipText.style.visibility = 'hidden';
                tooltipText.style.opacity = '0';
            }
        });

        // Keyboard accessibility
        tooltip.setAttribute('tabindex', '0');
        tooltip.addEventListener('focus', (e) => {
            const tooltipText = tooltip.querySelector('.tooltip-text');
            if (tooltipText) {
                tooltipText.style.visibility = 'visible';
                tooltipText.style.opacity = '1';
            }
        });

        tooltip.addEventListener('blur', (e) => {
            const tooltipText = tooltip.querySelector('.tooltip-text');
            if (tooltipText) {
                tooltipText.style.visibility = 'hidden';
                tooltipText.style.opacity = '0';
            }
        });
    });
}

// Initialize tooltips when DOM is ready
document.addEventListener('DOMContentLoaded', setupTooltips);

/**
 * Debounce function for performance optimization
 * @param {Function} func - Function to debounce
 * @param {number} wait - Wait time in milliseconds
 * @returns {Function} Debounced function
 */
function debounce(func, wait) {
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

/**
 * Detect if element is in viewport
 * @param {HTMLElement} element - Element to check
 * @returns {boolean} True if in viewport
 */
function isInViewport(element) {
    const rect = element.getBoundingClientRect();
    return (
        rect.top >= 0 &&
        rect.left >= 0 &&
        rect.bottom <= (window.innerHeight || document.documentElement.clientHeight) &&
        rect.right <= (window.innerWidth || document.documentElement.clientWidth)
    );
}

/**
 * Analytics tracking (placeholder for future implementation)
 * @param {string} event - Event name
 * @param {Object} data - Event data
 */
function trackEvent(event, data) {
    // In production, this would send to analytics service
    console.log('Event:', event, data);
}

// Track page views and interactions
window.addEventListener('load', () => {
    trackEvent('page_view', { page: 'Language Identity Map' });
});

// Handle print styles
window.addEventListener('beforeprint', () => {
    // Expand all collapsed sections before printing
    const modals = document.querySelectorAll('.modal-overlay');
    modals.forEach(modal => modal.classList.add('hidden'));
});

// Performance: Lazy load images if added in future
if ('loading' in HTMLImageElement.prototype) {
    const images = document.querySelectorAll('img[loading="lazy"]');
    images.forEach(img => {
        img.src = img.dataset.src;
    });
} else {
    // Fallback for browsers that don't support lazy loading
    const script = document.createElement('script');
    script.src = 'https://cdn.jsdelivr.net/npm/lazysizes@5/lazysizes.min.js';
    document.body.appendChild(script);
}

// Export for testing (if needed)
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        applyFilters,
        resetFilters,
        handleFormSubmission,
        saveStoryToLocalStorage,
        loadStoredStories
    };
}
