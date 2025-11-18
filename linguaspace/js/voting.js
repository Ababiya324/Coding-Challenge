// LinguaSpace - Voting System
// Handles upvotes/downvotes with localStorage persistence

class VotingSystem {
    constructor() {
        this.votes = this.loadVotes();
    }

    // Load votes from localStorage
    loadVotes() {
        const saved = localStorage.getItem('linguaspace_votes');
        return saved ? JSON.parse(saved) : { posts: {}, comments: {} };
    }

    // Save votes to localStorage
    saveVotes() {
        localStorage.setItem('linguaspace_votes', JSON.stringify(this.votes));
    }

    // Get vote for a post
    getPostVote(postId) {
        return this.votes.posts[postId] || null;
    }

    // Get vote for a comment
    getCommentVote(commentId) {
        return this.votes.comments[commentId] || null;
    }

    // Vote on a post
    votePost(postId, voteType) {
        const currentVote = this.votes.posts[postId];

        if (currentVote === voteType) {
            // Remove vote if clicking same button
            delete this.votes.posts[postId];
            this.saveVotes();
            return null;
        } else {
            // Set new vote
            this.votes.posts[postId] = voteType;
            this.saveVotes();
            return voteType;
        }
    }

    // Vote on a comment
    voteComment(commentId, voteType) {
        const currentVote = this.votes.comments[commentId];

        if (currentVote === voteType) {
            // Remove vote if clicking same button
            delete this.votes.comments[commentId];
            this.saveVotes();
            return null;
        } else {
            // Set new vote
            this.votes.comments[commentId] = voteType;
            this.saveVotes();
            return voteType;
        }
    }

    // Calculate net vote count
    calculateVoteCount(baseUpvotes, baseDownvotes, currentVote) {
        let upvotes = baseUpvotes;
        let downvotes = baseDownvotes;

        if (currentVote === 'up') {
            upvotes += 1;
        } else if (currentVote === 'down') {
            downvotes += 1;
        }

        return upvotes - downvotes;
    }
}

// Initialize voting system
const votingSystem = new VotingSystem();

// Handle post vote
function handlePostVote(postId, voteType, event) {
    event.stopPropagation();

    const post = window.linguaSpaceData.posts.find(p => p.id === postId);
    if (!post) return;

    const newVote = votingSystem.votePost(postId, voteType);

    // Update UI
    updatePostVoteUI(postId, newVote, post);

    // Animate vote button
    const btn = event.currentTarget;
    btn.classList.remove('animate-up', 'animate-down');
    void btn.offsetWidth; // Trigger reflow
    btn.classList.add(voteType === 'up' ? 'animate-up' : 'animate-down');

    // Show toast
    if (newVote) {
        showToast(voteType === 'up' ? '⬆️ Upvoted!' : '⬇️ Downvoted!', 'success');
    }
}

// Update post vote UI
function updatePostVoteUI(postId, currentVote, post) {
    const voteCount = votingSystem.calculateVoteCount(
        post.upvotes,
        post.downvotes,
        currentVote
    );

    // Update all instances of this post's vote count
    const voteCountElements = document.querySelectorAll(`[data-post-id="${postId}"] .vote-count`);
    voteCountElements.forEach(el => {
        el.textContent = voteCount;
    });

    // Update button states
    const upvoteButtons = document.querySelectorAll(`[data-post-id="${postId}"] .vote-btn.upvote`);
    const downvoteButtons = document.querySelectorAll(`[data-post-id="${postId}"] .vote-btn.downvote`);

    upvoteButtons.forEach(btn => {
        btn.classList.toggle('voted', currentVote === 'up');
    });

    downvoteButtons.forEach(btn => {
        btn.classList.toggle('voted', currentVote === 'down');
    });
}

// Handle comment vote
function handleCommentVote(commentId, voteType, event) {
    event.stopPropagation();

    const comment = window.linguaSpaceData.comments.find(c => c.id === commentId);
    if (!comment) return;

    const newVote = votingSystem.voteComment(commentId, voteType);

    // Update UI
    updateCommentVoteUI(commentId, newVote, comment);

    // Animate vote button
    const btn = event.currentTarget;
    btn.classList.remove('animate-up', 'animate-down');
    void btn.offsetWidth; // Trigger reflow
    btn.classList.add(voteType === 'up' ? 'animate-up' : 'animate-down');
}

// Update comment vote UI
function updateCommentVoteUI(commentId, currentVote, comment) {
    const voteCount = votingSystem.calculateVoteCount(
        comment.upvotes,
        comment.downvotes,
        currentVote
    );

    // Update vote count
    const voteCountEl = document.querySelector(`[data-comment-id="${commentId}"] .comment-vote-count`);
    if (voteCountEl) {
        voteCountEl.textContent = voteCount;
    }

    // Update button states
    const upvoteBtn = document.querySelector(`[data-comment-id="${commentId}"] .comment-vote-btn[data-vote="up"]`);
    const downvoteBtn = document.querySelector(`[data-comment-id="${commentId}"] .comment-vote-btn[data-vote="down"]`);

    if (upvoteBtn) {
        upvoteBtn.classList.toggle('voted', currentVote === 'up');
    }

    if (downvoteBtn) {
        downvoteBtn.classList.toggle('voted', currentVote === 'down');
    }
}

// Show toast notification
function showToast(message, type = 'info') {
    const toast = document.getElementById('toast');
    toast.textContent = message;
    toast.className = 'toast show ' + type;

    setTimeout(() => {
        toast.classList.remove('show');
        toast.classList.add('hide');
    }, 2000);

    setTimeout(() => {
        toast.className = 'toast';
    }, 2300);
}

// Export for use in other modules
window.votingSystem = votingSystem;
window.handlePostVote = handlePostVote;
window.handleCommentVote = handleCommentVote;
window.showToast = showToast;
