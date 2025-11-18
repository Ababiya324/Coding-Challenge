/* ==========================================
   Language Identity Map - Map Generation & Interaction
   ========================================== */

// Global variables
let currentStories = [];
let currentStoryIndex = 0;
let filteredStories = [];

/**
 * Initialize the campus map on page load
 */
function initializeMap() {
    const mapContainer = document.getElementById('campus-map');
    if (!mapContainer) return;

    // Create SVG element
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.setAttribute('class', 'map-svg');
    svg.setAttribute('viewBox', '0 0 100 100');
    svg.setAttribute('preserveAspectRatio', 'xMidYMid meet');

    // Add background
    const background = createSVGElement('rect', {
        x: 0,
        y: 0,
        width: 100,
        height: 100,
        fill: '#f8f9fa'
    });
    svg.appendChild(background);

    // Draw campus pathways
    drawPathways(svg);

    // Draw campus buildings
    drawBuildings(svg);

    // Draw stories as dots
    drawStoryDots(svg, storiesData);

    mapContainer.appendChild(svg);

    // Store original stories
    filteredStories = [...storiesData];
}

/**
 * Create SVG element with attributes
 */
function createSVGElement(type, attributes) {
    const element = document.createElementNS('http://www.w3.org/2000/svg', type);
    for (let key in attributes) {
        element.setAttribute(key, attributes[key]);
    }
    return element;
}

/**
 * Draw pathways connecting buildings
 */
function drawPathways(svg) {
    const pathways = [
        { x1: 35, y1: 50, x2: 52, y2: 50 },
        { x1: 52, y1: 50, x2: 65, y2: 45 },
        { x1: 52, y1: 50, x2: 45, y2: 65 },
        { x1: 65, y1: 45, x2: 73, y2: 59 },
        { x1: 52, y1: 50, x2: 55, y2: 30 }
    ];

    pathways.forEach(path => {
        const line = createSVGElement('line', {
            x1: path.x1,
            y1: path.y1,
            x2: path.x2,
            y2: path.y2,
            stroke: '#CCCCCC',
            'stroke-width': 1.5,
            'stroke-dasharray': '2,2'
        });
        svg.appendChild(line);
    });
}

/**
 * Draw campus buildings
 */
function drawBuildings(svg) {
    const buildings = [
        {
            id: 'academic',
            name: 'Academic\nBuilding',
            x: 25,
            y: 30,
            width: 20,
            height: 25,
            labelX: 35,
            labelY: 42.5
        },
        {
            id: 'uc',
            name: 'University\nCenter',
            x: 42,
            y: 42,
            width: 20,
            height: 18,
            labelX: 52,
            labelY: 51
        },
        {
            id: 'library',
            name: 'Library',
            x: 58,
            y: 28,
            width: 16,
            height: 20,
            labelX: 66,
            labelY: 38
        },
        {
            id: 'dining',
            name: 'Dining\nArea',
            x: 35,
            y: 58,
            width: 20,
            height: 15,
            labelX: 45,
            labelY: 65.5
        },
        {
            id: 'residence',
            name: 'Residence\nHalls',
            x: 65,
            y: 52,
            width: 18,
            height: 16,
            labelX: 74,
            labelY: 60
        },
        {
            id: 'outdoor',
            name: 'Outdoor\nSpaces',
            x: 48,
            y: 15,
            width: 14,
            height: 14,
            labelX: 55,
            labelY: 22
        }
    ];

    buildings.forEach(building => {
        // Building rectangle
        const rect = createSVGElement('rect', {
            class: 'campus-building',
            'data-location': building.name.replace('\n', ' '),
            x: building.x,
            y: building.y,
            width: building.width,
            height: building.height,
            rx: 1
        });

        rect.addEventListener('click', () => {
            const locationStories = filteredStories.filter(
                s => s.location === building.name.replace('\n', ' ')
            );
            if (locationStories.length > 0) {
                showStoriesAtLocation(locationStories);
            }
        });

        svg.appendChild(rect);

        // Building label (handle multi-line text)
        const lines = building.name.split('\n');
        const text = createSVGElement('text', {
            class: 'building-label',
            x: building.labelX,
            y: building.labelY - (lines.length > 1 ? 2 : 0)
        });

        lines.forEach((line, index) => {
            const tspan = createSVGElement('tspan', {
                x: building.labelX,
                dy: index === 0 ? 0 : 4
            });
            tspan.textContent = line;
            text.appendChild(tspan);
        });

        svg.appendChild(text);
    });
}

/**
 * Draw story dots on the map
 */
function drawStoryDots(svg, stories) {
    // Remove existing dots
    const existingDots = svg.querySelectorAll('.story-dot');
    existingDots.forEach(dot => dot.remove());

    stories.forEach((story, index) => {
        const dot = createSVGElement('circle', {
            class: `story-dot ${getExperienceClass(story.experienceType)} appear`,
            cx: story.coordinates.x,
            cy: story.coordinates.y,
            r: 2.5,
            'data-story-id': story.id
        });

        dot.addEventListener('click', () => {
            showStoryModal(story, stories);
        });

        dot.addEventListener('mouseenter', (e) => {
            showQuickPreview(e, story);
        });

        dot.addEventListener('mouseleave', () => {
            hideQuickPreview();
        });

        svg.appendChild(dot);
    });

    // Update story counter
    updateStoryCounter(stories.length);
}

/**
 * Get CSS class for experience type
 */
function getExperienceClass(type) {
    const classMap = {
        'Linguistic Shame': 'shame',
        'Linguistic Pride': 'pride',
        'Code-Switching': 'code-switching',
        'Identity Negotiation': 'negotiation'
    };
    return classMap[type] || '';
}

/**
 * Show quick preview tooltip on hover
 */
function showQuickPreview(event, story) {
    // Simple title attribute for now
    event.target.setAttribute('title', `${story.studentProfile} - ${story.experienceType}`);
}

/**
 * Hide quick preview tooltip
 */
function hideQuickPreview() {
    // Handled by browser
}

/**
 * Show stories at a specific location
 */
function showStoriesAtLocation(stories) {
    if (stories.length > 0) {
        showStoryModal(stories[0], stories);
    }
}

/**
 * Show story modal
 */
function showStoryModal(story, storiesAtLocation = [story]) {
    currentStories = storiesAtLocation;
    currentStoryIndex = currentStories.findIndex(s => s.id === story.id);

    const modal = document.getElementById('story-modal');
    const modalBody = document.getElementById('modal-body');

    // Build modal content
    modalBody.innerHTML = `
        <div class="story-header">
            <div class="story-profile">${escapeHtml(story.studentProfile)}</div>
        </div>
        <div class="story-meta">
            <span class="story-tag ${getExperienceClass(story.experienceType)}">${escapeHtml(story.experienceType)}</span>
            ${story.languages.map(lang => `<span class="story-tag language">${escapeHtml(lang)}</span>`).join('')}
            <span class="story-tag location">📍 ${escapeHtml(story.location)}</span>
        </div>
        <div class="story-text">${escapeHtml(story.story)}</div>
        <div class="story-concept">
            <strong>Academic Context:</strong> ${escapeHtml(story.academicConcept)}
        </div>
    `;

    // Update navigation buttons
    updateNavigationButtons();

    // Show modal
    modal.classList.add('active');
    document.body.style.overflow = 'hidden'; // Prevent background scrolling

    // Set focus to modal for accessibility
    modal.focus();
}

/**
 * Close modal
 */
function closeModal() {
    const modal = document.getElementById('story-modal');
    modal.classList.remove('active');
    document.body.style.overflow = ''; // Restore scrolling
}

/**
 * Navigate between stories in modal
 */
function navigateStory(direction) {
    currentStoryIndex += direction;

    if (currentStoryIndex < 0) {
        currentStoryIndex = 0;
    } else if (currentStoryIndex >= currentStories.length) {
        currentStoryIndex = currentStories.length - 1;
    }

    const story = currentStories[currentStoryIndex];
    showStoryModal(story, currentStories);
}

/**
 * Update navigation button states
 */
function updateNavigationButtons() {
    const prevButton = document.getElementById('prev-story');
    const nextButton = document.getElementById('next-story');

    prevButton.disabled = currentStoryIndex === 0;
    nextButton.disabled = currentStoryIndex === currentStories.length - 1;

    // Update button text to show position
    if (currentStories.length > 1) {
        prevButton.textContent = `← Previous ${currentStoryIndex > 0 ? `(${currentStoryIndex})` : ''}`;
        nextButton.textContent = `Next ${currentStoryIndex < currentStories.length - 1 ? `(${currentStories.length - currentStoryIndex - 1})` : ''} →`;
    }
}

/**
 * Update story counter display
 */
function updateStoryCounter(count) {
    const counter = document.getElementById('visible-stories-count');
    if (counter) {
        counter.textContent = count;
    }
}

/**
 * Redraw map with filtered stories
 */
function updateMapWithFilters(stories) {
    filteredStories = stories;
    const svg = document.querySelector('.map-svg');
    if (svg) {
        drawStoryDots(svg, stories);
    }
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Smooth scroll to map section
 */
function scrollToMap() {
    const mapSection = document.getElementById('map-section');
    if (mapSection) {
        mapSection.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * Close modal on Escape key
 */
document.addEventListener('keydown', (event) => {
    if (event.key === 'Escape') {
        closeModal();
    }
});

/**
 * Initialize map when DOM is loaded
 */
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeMap);
} else {
    initializeMap();
}
