// LinguaSpace - Comments System
// Handles comment display and threading

// Format time ago
function timeAgo(dateString) {
    const date = new Date(dateString);
    const now = new Date();
    const seconds = Math.floor((now - date) / 1000);

    const intervals = {
        year: 31536000,
        month: 2592000,
        week: 604800,
        day: 86400,
        hour: 3600,
        minute: 60
    };

    for (const [unit, secondsInUnit] of Object.entries(intervals)) {
        const interval = Math.floor(seconds / secondsInUnit);
        if (interval >= 1) {
            return interval === 1 ? `1 ${unit} ago` : `${interval} ${unit}s ago`;
        }
    }

    return 'just now';
}

// Render comments for a post
function renderComments(postId, sortBy = 'best') {
    const commentsContainer = document.getElementById('commentsContainer');
    const postComments = window.linguaSpaceData.comments.filter(c => c.postId === postId);

    if (postComments.length === 0) {
        commentsContainer.innerHTML = '<p class="empty-state">No comments yet. Be the first to comment!</p>';
        return;
    }

    // Sort comments
    const sortedComments = sortComments(postComments, sortBy);

    // Build comment tree
    const commentTree = buildCommentTree(sortedComments);

    // Render comment tree
    commentsContainer.innerHTML = commentTree.map(comment => renderComment(comment, 0)).join('');
}

// Sort comments
function sortComments(comments, sortBy) {
    const commentsWithVotes = comments.map(comment => {
        const userVote = votingSystem.getCommentVote(comment.id);
        const voteCount = votingSystem.calculateVoteCount(
            comment.upvotes,
            comment.downvotes,
            userVote
        );
        return { ...comment, voteCount };
    });

    switch (sortBy) {
        case 'new':
            return commentsWithVotes.sort((a, b) =>
                new Date(b.timePosted) - new Date(a.timePosted)
            );
        case 'controversial':
            return commentsWithVotes.sort((a, b) => {
                const aControversy = Math.min(a.upvotes, a.downvotes);
                const bControversy = Math.min(b.upvotes, b.downvotes);
                return bControversy - aControversy;
            });
        case 'best':
        default:
            return commentsWithVotes.sort((a, b) => b.voteCount - a.voteCount);
    }
}

// Build comment tree (nested structure)
function buildCommentTree(comments) {
    const commentMap = {};
    const tree = [];

    // Create map of all comments
    comments.forEach(comment => {
        commentMap[comment.id] = { ...comment, replies: [] };
    });

    // Build tree structure
    comments.forEach(comment => {
        if (comment.parentId === null) {
            tree.push(commentMap[comment.id]);
        } else if (commentMap[comment.parentId]) {
            commentMap[comment.parentId].replies.push(commentMap[comment.id]);
        }
    });

    return tree;
}

// Render a single comment with nesting
function renderComment(comment, depth) {
    const userVote = votingSystem.getCommentVote(comment.id);
    const voteCount = votingSystem.calculateVoteCount(
        comment.upvotes,
        comment.downvotes,
        userVote
    );

    const nestingClass = depth === 0 ? '' : depth === 1 ? 'nested' : 'nested-2';
    const maxDepth = 2;

    const html = `
        <div class="comment ${nestingClass}" data-comment-id="${comment.id}">
            <div class="comment-header">
                <span class="comment-username">u/${comment.username}</span>
                <span class="comment-time">${timeAgo(comment.timePosted)}</span>
            </div>
            <div class="comment-content">${escapeHtml(comment.content)}</div>
            <div class="comment-actions">
                <div class="comment-vote">
                    <button
                        class="comment-vote-btn ${userVote === 'up' ? 'voted' : ''}"
                        data-vote="up"
                        onclick="handleCommentVote(${comment.id}, 'up', event)"
                        aria-label="Upvote comment">
                        ⬆
                    </button>
                    <span class="comment-vote-count">${voteCount}</span>
                    <button
                        class="comment-vote-btn ${userVote === 'down' ? 'voted' : ''}"
                        data-vote="down"
                        onclick="handleCommentVote(${comment.id}, 'down', event)"
                        aria-label="Downvote comment">
                        ⬇
                    </button>
                </div>
                <button class="comment-reply-btn" onclick="showReplyForm(${comment.id})">
                    Reply
                </button>
            </div>
        </div>
        ${comment.replies && depth < maxDepth ? comment.replies.map(reply => renderComment(reply, depth + 1)).join('') : ''}
    `;

    return html;
}

// Show reply form (placeholder for demo)
function showReplyForm(commentId) {
    showToast('💬 Reply feature coming soon! This is a demo.', 'info');
}

// Handle comment sort change
function handleCommentSort() {
    const sortSelect = document.getElementById('commentSort');
    const modal = document.getElementById('postModal');
    const postId = parseInt(modal.dataset.postId);

    if (postId) {
        renderComments(postId, sortSelect.value);
    }
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Export functions
window.renderComments = renderComments;
window.handleCommentSort = handleCommentSort;
window.showReplyForm = showReplyForm;
window.timeAgo = timeAgo;
window.escapeHtml = escapeHtml;
