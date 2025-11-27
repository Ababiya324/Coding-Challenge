/**
 * The Invisible Edit - Interactive JavaScript
 * A Multimodal Project on Linguistic Identity
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize all components
    initNavbar();
    initStoryForm();
    initCharacterCount();
    initScrollAnimations();
    initImpactCounters();
    initSmoothScroll();
    initVideoHandler();
});

/**
 * Navbar scroll behavior
 */
function initNavbar() {
    const navbar = document.querySelector('.navbar');
    let lastScroll = 0;

    window.addEventListener('scroll', () => {
        const currentScroll = window.pageYOffset;

        if (currentScroll > 100) {
            navbar.style.boxShadow = '0 4px 20px rgba(0, 0, 0, 0.15)';
        } else {
            navbar.style.boxShadow = 'none';
        }

        lastScroll = currentScroll;
    });
}

/**
 * Story submission form handling
 */
function initStoryForm() {
    const form = document.getElementById('story-form');
    const successMessage = document.getElementById('success-message');

    if (!form) return;

    form.addEventListener('submit', function(e) {
        e.preventDefault();

        // Collect form data
        const formData = new FormData(form);
        const submission = {
            timestamp: new Date().toISOString(),
            experienceType: formData.get('experience-type'),
            story: formData.get('story'),
            feelings: formData.getAll('feelings'),
            languages: formData.get('languages'),
            messageToFaculty: formData.get('message')
        };

        // Store submission locally (in a real implementation, this would go to a server)
        saveSubmission(submission);

        // Show success message
        form.classList.add('hidden');
        successMessage.classList.remove('hidden');

        // Scroll to success message
        successMessage.scrollIntoView({ behavior: 'smooth', block: 'center' });

        console.log('Anonymous submission saved:', submission);
    });
}

/**
 * Save submission to localStorage (for demo purposes)
 * In production, this would send to a secure backend
 */
function saveSubmission(submission) {
    try {
        // Get existing submissions
        let submissions = JSON.parse(localStorage.getItem('invisibleEditSubmissions') || '[]');

        // Add new submission with anonymous ID
        submission.id = 'anon_' + Date.now() + '_' + Math.random().toString(36).substr(2, 9);
        submissions.push(submission);

        // Save back to localStorage
        localStorage.setItem('invisibleEditSubmissions', JSON.stringify(submissions));

        return true;
    } catch (error) {
        console.error('Error saving submission:', error);
        return false;
    }
}

/**
 * Reset form to allow another submission
 */
function resetForm() {
    const form = document.getElementById('story-form');
    const successMessage = document.getElementById('success-message');

    if (form && successMessage) {
        form.reset();
        form.classList.remove('hidden');
        successMessage.classList.add('hidden');

        // Reset character count
        const charCount = document.getElementById('char-count');
        if (charCount) charCount.textContent = '0';

        // Scroll to form
        form.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

// Make resetForm globally available
window.resetForm = resetForm;

/**
 * Character count for textarea
 */
function initCharacterCount() {
    const storyTextarea = document.getElementById('story');
    const charCount = document.getElementById('char-count');

    if (!storyTextarea || !charCount) return;

    storyTextarea.addEventListener('input', function() {
        const count = this.value.length;
        charCount.textContent = count;

        // Visual feedback when approaching limit
        if (count > 1800) {
            charCount.style.color = '#c9a227';
        } else if (count > 1950) {
            charCount.style.color = '#e74c3c';
        } else {
            charCount.style.color = '';
        }

        // Enforce max length
        if (count > 2000) {
            this.value = this.value.substring(0, 2000);
            charCount.textContent = '2000';
        }
    });
}

/**
 * Scroll-triggered animations
 */
function initScrollAnimations() {
    const animatedElements = document.querySelectorAll(
        '.problem-item, .scene, .concept-card, .framework-point, .reference'
    );

    // Add fade-in class to elements
    animatedElements.forEach(el => {
        el.classList.add('fade-in');
    });

    const observer = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                entry.target.classList.add('visible');
                observer.unobserve(entry.target);
            }
        });
    }, {
        threshold: 0.1,
        rootMargin: '0px 0px -50px 0px'
    });

    animatedElements.forEach(el => observer.observe(el));
}

/**
 * Animated counters for impact section
 */
function initImpactCounters() {
    const counters = document.querySelectorAll('.impact-number');

    const observerOptions = {
        threshold: 0.5
    };

    const counterObserver = new IntersectionObserver((entries) => {
        entries.forEach(entry => {
            if (entry.isIntersecting) {
                animateCounter(entry.target);
                counterObserver.unobserve(entry.target);
            }
        });
    }, observerOptions);

    counters.forEach(counter => counterObserver.observe(counter));
}

/**
 * Animate a single counter
 */
function animateCounter(element) {
    const target = parseInt(element.getAttribute('data-count'), 10);
    const duration = 2000; // 2 seconds
    const step = target / (duration / 16); // 60fps
    let current = 0;

    const timer = setInterval(() => {
        current += step;
        if (current >= target) {
            element.textContent = target;
            clearInterval(timer);
        } else {
            element.textContent = Math.floor(current);
        }
    }, 16);
}

/**
 * Smooth scrolling for anchor links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            e.preventDefault();
            const targetId = this.getAttribute('href');
            const targetElement = document.querySelector(targetId);

            if (targetElement) {
                const navbarHeight = document.querySelector('.navbar').offsetHeight;
                const targetPosition = targetElement.offsetTop - navbarHeight - 20;

                window.scrollTo({
                    top: targetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

/**
 * Video player handler
 */
function initVideoHandler() {
    const video = document.getElementById('main-video');
    const overlay = document.querySelector('.video-overlay-text');

    if (!video) return;

    // Hide overlay when video loads
    video.addEventListener('loadeddata', function() {
        if (overlay) {
            overlay.style.display = 'none';
        }
    });

    // Show overlay on error
    video.addEventListener('error', function() {
        if (overlay) {
            overlay.style.display = 'block';
        }
    });

    // Check if video source exists
    const source = video.querySelector('source');
    if (source && source.src) {
        // Try to load the video
        video.load();
    }
}

/**
 * Utility: Debounce function for performance
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
 * Export submissions (for administrators)
 * This function allows downloading all collected stories as JSON
 */
function exportSubmissions() {
    try {
        const submissions = JSON.parse(localStorage.getItem('invisibleEditSubmissions') || '[]');

        if (submissions.length === 0) {
            alert('No submissions to export.');
            return;
        }

        const dataStr = JSON.stringify(submissions, null, 2);
        const dataBlob = new Blob([dataStr], { type: 'application/json' });
        const url = URL.createObjectURL(dataBlob);

        const link = document.createElement('a');
        link.href = url;
        link.download = `invisible-edit-submissions-${new Date().toISOString().split('T')[0]}.json`;
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        URL.revokeObjectURL(url);

        console.log(`Exported ${submissions.length} submissions`);
    } catch (error) {
        console.error('Error exporting submissions:', error);
    }
}

// Make export function available globally (for admin use)
window.exportSubmissions = exportSubmissions;

/**
 * Get submission count (for display purposes)
 */
function getSubmissionCount() {
    try {
        const submissions = JSON.parse(localStorage.getItem('invisibleEditSubmissions') || '[]');
        return submissions.length;
    } catch (error) {
        return 0;
    }
}

// Log submission count on load (for development)
console.log(`The Invisible Edit: ${getSubmissionCount()} anonymous stories collected`);
