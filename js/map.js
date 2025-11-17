/**
 * Language Identity Map - Map Functionality
 * Handles interactive campus map and story pins
 */

// Global state
let currentStories = [...stories]; // Copy of filtered stories
let currentLocationStories = []; // Stories at current clicked location
let currentStoryIndex = 0; // Index for modal navigation

/**
 * Initialize the map with story pins
 */
function initializeMap() {
    renderStoryPins(currentStories);
    updateStatistics(currentStories);
    updateResultsCounter(currentStories.length, stories.length);
}

/**
 * Render story pins on the map
 * @param {Array} storiesToRender - Array of story objects to display
 */
function renderStoryPins(storiesToRender) {
    const storyPinsContainer = document.getElementById('story-pins');
    if (!storyPinsContainer) return;

    // Clear existing pins
    storyPinsContainer.innerHTML = '';

    // Group stories by location
    const storiesByLocation = {};
    storiesToRender.forEach(story => {
        if (!storiesByLocation[story.location]) {
            storiesByLocation[story.location] = [];
        }
        storiesByLocation[story.location].push(story);
    });

    // Create pins for each location with stories
    Object.entries(storiesByLocation).forEach(([location, locationStories], index) => {
        const coords = locationCoordinates[location];
        if (!coords) return;

        // Determine primary experience type (most common)
        const experienceTypes = locationStories.map(s => s.experienceType);
        const primaryType = getMostCommon(experienceTypes);
        const color = experienceColors[primaryType];

        // Calculate pin size based on number of stories
        const baseRadius = 8;
        const radius = Math.min(baseRadius + (locationStories.length * 0.5), 15);

        // Create pin group
        const pinGroup = document.createElementNS('http://www.w3.org/2000/svg', 'g');
        pinGroup.setAttribute('class', 'story-pin');
        pinGroup.setAttribute('data-location', location);
        pinGroup.setAttribute('role', 'button');
        pinGroup.setAttribute('tabindex', '0');
        pinGroup.setAttribute('aria-label', `${location}: ${locationStories.length} stories`);

        // Create circle
        const circle = document.createElementNS('http://www.w3.org/2000/svg', 'circle');
        circle.setAttribute('cx', coords.x);
        circle.setAttribute('cy', coords.y);
        circle.setAttribute('r', radius);
        circle.setAttribute('fill', color);
        circle.setAttribute('stroke', 'white');
        circle.setAttribute('stroke-width', '2');
        circle.setAttribute('opacity', '0.9');

        // Create count label
        const text = document.createElementNS('http://www.w3.org/2000/svg', 'text');
        text.setAttribute('x', coords.x);
        text.setAttribute('y', coords.y);
        text.setAttribute('text-anchor', 'middle');
        text.setAttribute('dominant-baseline', 'middle');
        text.setAttribute('fill', 'white');
        text.setAttribute('font-size', '12');
        text.setAttribute('font-weight', 'bold');
        text.textContent = locationStories.length;

        // Add elements to group
        pinGroup.appendChild(circle);
        pinGroup.appendChild(text);

        // Add click handler
        pinGroup.addEventListener('click', () => showLocationStories(location, locationStories));
        pinGroup.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                showLocationStories(location, locationStories);
            }
        });

        // Add to container
        storyPinsContainer.appendChild(pinGroup);
    });
}

/**
 * Get most common item in array
 * @param {Array} arr - Array of items
 * @returns {*} Most common item
 */
function getMostCommon(arr) {
    const counts = {};
    arr.forEach(item => {
        counts[item] = (counts[item] || 0) + 1;
    });
    return Object.keys(counts).reduce((a, b) => counts[a] > counts[b] ? a : b);
}

/**
 * Show stories for a specific location
 * @param {string} location - Location name
 * @param {Array} locationStories - Stories at this location
 */
function showLocationStories(location, locationStories) {
    currentLocationStories = locationStories;
    currentStoryIndex = 0;
    displayStoryInModal(currentLocationStories[currentStoryIndex]);
}

/**
 * Display a story in the modal
 * @param {Object} story - Story object to display
 */
function displayStoryInModal(story) {
    const modalOverlay = document.getElementById('modalOverlay');
    const modalBody = document.getElementById('modalBody');

    // Build experience type class name
    const typeClass = story.experienceType.toLowerCase().replace(/\s+/g, '-');

    // Create modal content
    modalBody.innerHTML = `
        <h2 class="modal-profile" id="modalTitle">${story.studentProfile}</h2>
        <div class="modal-meta">
            <span class="story-tag type ${getTypeClass(story.experienceType)}">${story.experienceType}</span>
            ${story.languages.map(lang => `<span class="story-tag">${lang}</span>`).join('')}
            <span class="story-tag">📍 ${story.location}</span>
        </div>
        <div class="modal-story">
            ${story.story}
        </div>
        <div class="modal-concept">
            <strong>Academic Context:</strong> ${story.academicConcept}
        </div>
    `;

    // Update navigation
    updateModalNavigation();

    // Show modal
    modalOverlay.classList.remove('hidden');

    // Focus on modal for accessibility
    setTimeout(() => {
        const closeButton = document.querySelector('.modal-close');
        if (closeButton) closeButton.focus();
    }, 100);
}

/**
 * Get CSS class for experience type
 * @param {string} type - Experience type
 * @returns {string} CSS class name
 */
function getTypeClass(type) {
    const map = {
        'Linguistic Shame': 'shame',
        'Linguistic Pride': 'pride',
        'Code-Switching': 'switching',
        'Identity Negotiation': 'negotiation'
    };
    return map[type] || '';
}

/**
 * Update modal navigation buttons
 */
function updateModalNavigation() {
    const prevBtn = document.getElementById('prevStoryBtn');
    const nextBtn = document.getElementById('nextStoryBtn');
    const counter = document.getElementById('storyCounter');

    if (!prevBtn || !nextBtn || !counter) return;

    // Update counter
    counter.textContent = `${currentStoryIndex + 1} of ${currentLocationStories.length}`;

    // Update button states
    prevBtn.disabled = currentStoryIndex === 0;
    nextBtn.disabled = currentStoryIndex === currentLocationStories.length - 1;
}

/**
 * Navigate between stories in modal
 * @param {number} direction - -1 for previous, 1 for next
 */
function navigateStory(direction) {
    const newIndex = currentStoryIndex + direction;

    if (newIndex >= 0 && newIndex < currentLocationStories.length) {
        currentStoryIndex = newIndex;
        displayStoryInModal(currentLocationStories[currentStoryIndex]);
    }
}

/**
 * Close the modal
 */
function closeModal() {
    const modalOverlay = document.getElementById('modalOverlay');

    // Add closing animation
    modalOverlay.classList.add('closing');

    setTimeout(() => {
        modalOverlay.classList.remove('closing');
        modalOverlay.classList.add('hidden');
    }, 300);
}

/**
 * Update statistics dashboard
 * @param {Array} storiesToCount - Stories to count
 */
function updateStatistics(storiesToCount) {
    // Total stories
    const totalStoriesEl = document.getElementById('totalStories');
    if (totalStoriesEl) {
        animateCounter(totalStoriesEl, storiesToCount.length);
    }

    // Unique languages
    const languages = new Set();
    storiesToCount.forEach(story => {
        story.languages.forEach(lang => languages.add(lang));
    });
    const languagesCountEl = document.getElementById('languagesCount');
    if (languagesCountEl) {
        animateCounter(languagesCountEl, languages.size);
    }

    // Unique locations
    const locations = new Set(storiesToCount.map(s => s.location));
    const locationsCountEl = document.getElementById('locationsCount');
    if (locationsCountEl) {
        animateCounter(locationsCountEl, locations.size);
    }
}

/**
 * Animate counter from 0 to target number
 * @param {HTMLElement} element - Element to update
 * @param {number} target - Target number
 */
function animateCounter(element, target) {
    const duration = 1000;
    const start = 0;
    const increment = target / (duration / 16);
    let current = start;

    const timer = setInterval(() => {
        current += increment;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

/**
 * Update results counter
 * @param {number} filtered - Number of filtered stories
 * @param {number} total - Total number of stories
 */
function updateResultsCounter(filtered, total) {
    const filteredCountEl = document.getElementById('filteredCount');
    const totalCountEl = document.getElementById('totalCount');

    if (filteredCountEl) filteredCountEl.textContent = filtered;
    if (totalCountEl) totalCountEl.textContent = total;
}

/**
 * Switch between map and list view
 * @param {string} view - 'map' or 'list'
 */
function switchView(view) {
    const mapView = document.getElementById('mapView');
    const listView = document.getElementById('listView');
    const mapBtn = document.getElementById('mapViewBtn');
    const listBtn = document.getElementById('listViewBtn');

    if (view === 'map') {
        mapView.classList.remove('hidden');
        listView.classList.add('hidden');
        mapBtn.classList.add('active');
        listBtn.classList.remove('active');
    } else {
        mapView.classList.add('hidden');
        listView.classList.remove('hidden');
        mapBtn.classList.remove('active');
        listBtn.classList.add('active');
        renderStoryList(currentStories);
    }
}

/**
 * Render stories in list view
 * @param {Array} storiesToRender - Stories to display in list
 */
function renderStoryList(storiesToRender) {
    const storyList = document.getElementById('storyList');
    if (!storyList) return;

    storyList.innerHTML = '';

    if (storiesToRender.length === 0) {
        storyList.innerHTML = '<p style="text-align: center; padding: 2rem; color: var(--gray-500);">No stories match the current filters.</p>';
        return;
    }

    storiesToRender.forEach(story => {
        const card = document.createElement('div');
        card.className = `story-card ${getTypeClass(story.experienceType)}`;
        card.setAttribute('role', 'button');
        card.setAttribute('tabindex', '0');
        card.setAttribute('aria-label', `Story from ${story.studentProfile}`);

        card.innerHTML = `
            <div class="story-card-header">
                <div class="story-profile">${story.studentProfile}</div>
                <div class="story-meta">
                    <span class="story-tag type ${getTypeClass(story.experienceType)}">${story.experienceType}</span>
                    ${story.languages.map(lang => `<span class="story-tag">${lang}</span>`).join('')}
                </div>
            </div>
            <div class="story-location">📍 ${story.location}</div>
            <div class="story-text">${story.story}</div>
        `;

        card.addEventListener('click', () => {
            currentLocationStories = [story];
            currentStoryIndex = 0;
            displayStoryInModal(story);
        });

        card.addEventListener('keypress', (e) => {
            if (e.key === 'Enter' || e.key === ' ') {
                e.preventDefault();
                currentLocationStories = [story];
                currentStoryIndex = 0;
                displayStoryInModal(story);
            }
        });

        storyList.appendChild(card);
    });
}

/**
 * Smooth scroll to map section
 */
function scrollToMap() {
    const mapSection = document.getElementById('mapSection');
    if (mapSection) {
        mapSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Close modal on escape key
document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape') {
        const modalOverlay = document.getElementById('modalOverlay');
        if (modalOverlay && !modalOverlay.classList.contains('hidden')) {
            closeModal();
        }
    }
});

// Close modal when clicking outside
document.addEventListener('click', (e) => {
    const modalOverlay = document.getElementById('modalOverlay');
    if (e.target === modalOverlay) {
        closeModal();
    }
});

// Export functions for use in main.js
if (typeof module !== 'undefined' && module.exports) {
    module.exports = {
        initializeMap,
        renderStoryPins,
        switchView,
        closeModal,
        navigateStory
    };
}
