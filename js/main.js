/* ==========================================
   Language Identity Map - Main Application Logic
   ========================================== */

/**
 * Initialize application
 */
function initializeApp() {
    calculateStatistics();
    setupFilters();
    setupContributionForm();
    setupTooltips();
    loadUserSubmissions();
}

/**
 * Calculate and display statistics
 */
function calculateStatistics() {
    // Get all stories (including user submissions)
    const allStories = getAllStories();

    // Total stories
    const totalStories = allStories.length;
    document.getElementById('total-stories').textContent = totalStories;

    // Unique languages
    const languages = new Set();
    allStories.forEach(story => {
        story.languages.forEach(lang => languages.add(lang));
    });
    document.getElementById('total-languages').textContent = languages.size;

    // Shame percentage
    const shameStories = allStories.filter(s => s.experienceType === 'Linguistic Shame').length;
    const shamePercentage = Math.round((shameStories / totalStories) * 100);
    document.getElementById('shame-percentage').textContent = `${shamePercentage}%`;

    // Animate numbers
    animateNumbers();
}

/**
 * Animate counter numbers
 */
function animateNumbers() {
    const counters = document.querySelectorAll('.stat-number');
    counters.forEach(counter => {
        const target = counter.textContent;
        const isPercentage = target.includes('%');
        const targetValue = parseInt(target);

        if (!isNaN(targetValue)) {
            let current = 0;
            const increment = targetValue / 50;
            const timer = setInterval(() => {
                current += increment;
                if (current >= targetValue) {
                    counter.textContent = isPercentage ? `${targetValue}%` : targetValue;
                    clearInterval(timer);
                } else {
                    counter.textContent = isPercentage ? `${Math.floor(current)}%` : Math.floor(current);
                }
            }, 20);
        }
    });
}

/**
 * Get all stories including user submissions
 */
function getAllStories() {
    const userStories = getUserSubmissions();
    return [...storiesData, ...userStories];
}

/**
 * Setup filter event listeners
 */
function setupFilters() {
    const filterType = document.getElementById('filter-type');
    const filterLanguage = document.getElementById('filter-language');
    const filterBackground = document.getElementById('filter-background');

    [filterType, filterLanguage, filterBackground].forEach(filter => {
        filter.addEventListener('change', applyFilters);
    });
}

/**
 * Apply filters to stories
 */
function applyFilters() {
    const filterType = document.getElementById('filter-type').value;
    const filterLanguage = document.getElementById('filter-language').value;
    const filterBackground = document.getElementById('filter-background').value;

    let filtered = getAllStories();

    // Filter by experience type
    if (filterType !== 'all') {
        filtered = filtered.filter(story => story.experienceType === filterType);
    }

    // Filter by language
    if (filterLanguage !== 'all') {
        if (filterLanguage === 'Multilingual') {
            filtered = filtered.filter(story => story.languages.length >= 3);
        } else {
            filtered = filtered.filter(story => story.languages.includes(filterLanguage));
        }
    }

    // Filter by student background
    if (filterBackground !== 'all') {
        filtered = filtered.filter(story => {
            const profile = story.studentProfile.toLowerCase();
            if (filterBackground === 'Qatari') {
                return profile.includes('qatari');
            } else if (filterBackground === 'GCC') {
                return profile.includes('saudi') || profile.includes('emirati') ||
                       profile.includes('kuwaiti') || profile.includes('bahraini') ||
                       profile.includes('omani') || profile.includes('qatari');
            } else if (filterBackground === 'International') {
                return profile.includes('international');
            }
            return true;
        });
    }

    // Update map with filtered stories
    updateMapWithFilters(filtered);
}

/**
 * Reset all filters
 */
function resetFilters() {
    document.getElementById('filter-type').value = 'all';
    document.getElementById('filter-language').value = 'all';
    document.getElementById('filter-background').value = 'all';
    applyFilters();
}

/**
 * Setup contribution form
 */
function setupContributionForm() {
    const form = document.getElementById('contribution-form');
    form.addEventListener('submit', handleFormSubmission);
}

/**
 * Handle form submission
 */
function handleFormSubmission(event) {
    event.preventDefault();

    // Get form values
    const storyText = document.getElementById('story-text').value.trim();
    const location = document.getElementById('story-location').value;
    const experienceType = document.getElementById('story-type').value;
    const languagesInput = document.getElementById('story-languages').value.trim();
    const profile = document.getElementById('story-profile').value.trim() || 'Anonymous Student';

    // Validate
    if (!storyText || !location || !experienceType) {
        alert('Please fill in all required fields.');
        return;
    }

    // Parse languages
    const languages = languagesInput ?
        languagesInput.split(',').map(l => l.trim()).filter(l => l) :
        ['Not specified'];

    // Find location coordinates
    const locationData = campusLocations.find(loc => loc.name === location);
    const coordinates = locationData ?
        { x: locationData.x + (Math.random() - 0.5) * 4, y: locationData.y + (Math.random() - 0.5) * 4 } :
        { x: 50, y: 50 };

    // Create new story
    const newStory = {
        id: Date.now(),
        location: location,
        coordinates: coordinates,
        studentProfile: profile,
        languages: languages,
        experienceType: experienceType,
        story: storyText,
        academicConcept: getRelatedConcept(experienceType),
        timestamp: new Date().toISOString().split('T')[0],
        userSubmitted: true
    };

    // Save to localStorage
    saveUserSubmission(newStory);

    // Show success message
    showSuccessMessage();

    // Reset form
    form.reset();

    // Update map and statistics
    applyFilters();
    calculateStatistics();
}

/**
 * Get related academic concept for experience type
 */
function getRelatedConcept(experienceType) {
    const concepts = {
        'Linguistic Shame': 'Linguistic Shame (Hillman, 2019)',
        'Linguistic Pride': 'Linguistic Pride and Identity Assertion',
        'Code-Switching': 'Translanguaging Practices (García & Wei)',
        'Identity Negotiation': 'Chronotope and Identity Navigation (Blommaert)'
    };
    return concepts[experienceType] || 'Multilingual Identity';
}

/**
 * Save user submission to localStorage
 */
function saveUserSubmission(story) {
    let submissions = getUserSubmissions();
    submissions.push(story);
    localStorage.setItem('languageMapSubmissions', JSON.stringify(submissions));
}

/**
 * Get user submissions from localStorage
 */
function getUserSubmissions() {
    const stored = localStorage.getItem('languageMapSubmissions');
    return stored ? JSON.parse(stored) : [];
}

/**
 * Load user submissions and add to map
 */
function loadUserSubmissions() {
    const submissions = getUserSubmissions();
    if (submissions.length > 0) {
        // Update map with all stories including submissions
        applyFilters();
    }
}

/**
 * Show success message
 */
function showSuccessMessage() {
    const successMessage = document.getElementById('submission-success');
    successMessage.style.display = 'block';

    // Scroll to success message
    successMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });

    // Hide after 5 seconds
    setTimeout(() => {
        successMessage.style.display = 'none';
    }, 5000);
}

/**
 * Setup tooltips for academic concepts
 */
function setupTooltips() {
    const tooltipElements = document.querySelectorAll('.tooltip');

    tooltipElements.forEach(element => {
        element.addEventListener('click', (event) => {
            showConceptTooltip(event, element.dataset.concept);
        });

        element.addEventListener('mouseenter', (event) => {
            showConceptTooltip(event, element.dataset.concept);
        });

        element.addEventListener('mouseleave', () => {
            hideConceptTooltip();
        });
    });
}

/**
 * Show concept tooltip
 */
function showConceptTooltip(event, conceptName) {
    const tooltip = document.getElementById('concept-tooltip');
    const title = document.getElementById('tooltip-title');
    const description = document.getElementById('tooltip-description');

    // Get concept definition
    const definition = academicConcepts[conceptName];
    if (!definition) return;

    // Set content
    title.textContent = conceptName;
    description.textContent = definition;

    // Position tooltip
    const rect = event.target.getBoundingClientRect();
    tooltip.style.top = `${rect.bottom + window.scrollY + 10}px`;
    tooltip.style.left = `${rect.left + window.scrollX}px`;
    tooltip.style.display = 'block';
}

/**
 * Hide concept tooltip
 */
function hideConceptTooltip() {
    const tooltip = document.getElementById('concept-tooltip');
    tooltip.style.display = 'none';
}

/**
 * Keyboard navigation for accessibility
 */
document.addEventListener('keydown', (event) => {
    const modal = document.getElementById('story-modal');
    if (modal.classList.contains('active')) {
        if (event.key === 'ArrowLeft') {
            navigateStory(-1);
        } else if (event.key === 'ArrowRight') {
            navigateStory(1);
        }
    }
});

/**
 * Intersection Observer for scroll animations
 */
function setupScrollAnimations() {
    const observerOptions = {
        threshold: 0.1,
        rootMargin: '0px 0px -100px 0px'
    };

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('fade-in');
            }
        });
    }, observerOptions);

    // Observe sections
    const sections = document.querySelectorAll('section');
    sections.forEach(section => observer.observe(section));
}

/**
 * Export data for analysis (future feature)
 */
function exportStories() {
    const allStories = getAllStories();
    const dataStr = JSON.stringify(allStories, null, 2);
    const dataBlob = new Blob([dataStr], { type: 'application/json' });

    const downloadLink = document.createElement('a');
    downloadLink.href = URL.createObjectURL(dataBlob);
    downloadLink.download = `language-identity-stories-${new Date().toISOString().split('T')[0]}.json`;
    downloadLink.click();
}

/**
 * Print statistics to console (for debugging)
 */
function printStatistics() {
    const allStories = getAllStories();

    console.group('Language Identity Map Statistics');
    console.log('Total Stories:', allStories.length);

    // Experience type breakdown
    const typeBreakdown = {};
    allStories.forEach(story => {
        typeBreakdown[story.experienceType] = (typeBreakdown[story.experienceType] || 0) + 1;
    });
    console.log('Experience Types:', typeBreakdown);

    // Language breakdown
    const langBreakdown = {};
    allStories.forEach(story => {
        story.languages.forEach(lang => {
            langBreakdown[lang] = (langBreakdown[lang] || 0) + 1;
        });
    });
    console.log('Languages:', langBreakdown);

    // Location breakdown
    const locationBreakdown = {};
    allStories.forEach(story => {
        locationBreakdown[story.location] = (locationBreakdown[story.location] || 0) + 1;
    });
    console.log('Locations:', locationBreakdown);

    console.groupEnd();
}

/**
 * Initialize on DOM ready
 */
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        initializeApp();
        setupScrollAnimations();
    });
} else {
    initializeApp();
    setupScrollAnimations();
}

// Make functions globally available
window.scrollToMap = scrollToMap;
window.closeModal = closeModal;
window.navigateStory = navigateStory;
window.resetFilters = resetFilters;
window.exportStories = exportStories;
window.printStatistics = printStatistics;
