// AI Exam Autograder - Frontend JavaScript

// ==================== Grading Page ====================

function initGradingPage() {
    const examSelect = document.getElementById('exam-select');
    const studentIdInput = document.getElementById('student-id');
    const imageUpload = document.getElementById('image-upload');
    const gradeButton = document.getElementById('grade-button');
    const imagePreview = document.getElementById('image-preview');
    const rubricPreview = document.getElementById('rubric-preview');
    const resultsSection = document.getElementById('results-section');
    const resultsContainer = document.getElementById('results-container');
    const loadingOverlay = document.getElementById('loading-overlay');

    let selectedFiles = [];

    // Exam selection handler
    if (examSelect) {
        examSelect.addEventListener('change', async function() {
            const examId = this.value;
            if (examId) {
                await loadRubricPreview(examId);
                checkFormValidity();
            } else {
                rubricPreview.style.display = 'none';
            }
        });
    }

    // Image upload handler
    if (imageUpload) {
        imageUpload.addEventListener('change', function(e) {
            selectedFiles = Array.from(e.target.files);
            displayImagePreviews(selectedFiles, imagePreview);
            checkFormValidity();
        });
    }

    // Check if form is valid
    function checkFormValidity() {
        const isValid = examSelect.value && studentIdInput.value && selectedFiles.length > 0;
        gradeButton.disabled = !isValid;
    }

    // Student ID input handler
    if (studentIdInput) {
        studentIdInput.addEventListener('input', checkFormValidity);
    }

    // Grade button handler
    if (gradeButton) {
        gradeButton.addEventListener('click', async function() {
            await gradeSubmission();
        });
    }

    // Load rubric preview
    async function loadRubricPreview(examId) {
        try {
            const response = await fetch(`/api/exams/${examId}`);
            const data = await response.json();

            if (data.rubric_id) {
                const rubricResponse = await fetch(`/api/rubrics/${data.rubric_id}`);
                const rubricData = await rubricResponse.json();

                displayRubricPreview(rubricData.extracted_data);
                rubricPreview.style.display = 'block';
            }
        } catch (error) {
            console.error('Failed to load rubric:', error);
        }
    }

    // Display rubric preview
    function displayRubricPreview(rubric) {
        const content = document.getElementById('rubric-content');

        let html = `
            <h4>${rubric.exam_metadata.title}</h4>
            <p><strong>Total Points:</strong> ${rubric.exam_metadata.total_points}</p>
            <p><strong>Questions:</strong> ${rubric.questions.length}</p>
            <div class="questions-list">
        `;

        rubric.questions.forEach(question => {
            html += `
                <div class="question-item">
                    <div class="question-header">
                        <span><strong>Question ${question.number}</strong></span>
                        <span class="question-type">${question.type}</span>
                        <span class="question-score">${question.points_possible} pts</span>
                    </div>
                    <p>${question.description.substring(0, 100)}${question.description.length > 100 ? '...' : ''}</p>
                </div>
            `;
        });

        html += '</div>';
        content.innerHTML = html;
    }

    // Grade submission
    async function gradeSubmission() {
        const examId = examSelect.value;
        const studentId = studentIdInput.value;

        // Show loading overlay
        loadingOverlay.style.display = 'flex';

        try {
            // Create form data
            const formData = new FormData();
            formData.append('student_id', studentId);
            formData.append('exam_id', examId);

            selectedFiles.forEach(file => {
                formData.append('images', file);
            });

            // Submit for grading
            const response = await fetch('/api/grade', {
                method: 'POST',
                body: formData
            });

            if (!response.ok) {
                throw new Error('Grading failed');
            }

            const result = await response.json();

            // Display results
            displayResults(result);
            resultsSection.style.display = 'block';
            resultsSection.scrollIntoView({ behavior: 'smooth' });

        } catch (error) {
            alert('Error grading submission: ' + error.message);
        } finally {
            loadingOverlay.style.display = 'none';
        }
    }

    // Display results
    function displayResults(result) {
        let html = `
            <div class="result-header">
                <div class="result-info">
                    <p><strong>Student ID:</strong> ${result.student_id}</p>
                    <p><strong>Exam:</strong> ${result.exam_name}</p>
                    <p><strong>Processing Time:</strong> ${result.processing_time_seconds.toFixed(2)}s</p>
                </div>
                <div class="result-score">
                    <div class="score-circle">
                        <span class="percentage">${result.percentage.toFixed(1)}%</span>
                        <span class="points">${result.total_score}/${result.total_possible}</span>
                    </div>
                    ${result.grade_letter ? `<div class="grade-letter">${result.grade_letter}</div>` : ''}
                </div>
            </div>

            <h3>Question Breakdown</h3>
        `;

        result.question_results.forEach(qr => {
            html += `
                <div class="question-result">
                    <div class="question-header">
                        <h4>Question ${qr.question_number}</h4>
                        <span class="question-score">
                            ${qr.points_earned}/${qr.points_possible} pts
                            (${((qr.points_earned / qr.points_possible) * 100).toFixed(1)}%)
                        </span>
                    </div>

                    ${qr.student_answer ? `
                        <div class="student-answer">
                            <h5>Student's Answer:</h5>
                            <pre>${qr.student_answer}</pre>
                        </div>
                    ` : ''}

                    ${qr.criterion_scores && qr.criterion_scores.length > 0 ? `
                        <div class="criterion-breakdown">
                            <h5>Criterion Breakdown:</h5>
                            <table class="criterion-table">
                                <thead>
                                    <tr>
                                        <th>Criterion</th>
                                        <th>Score</th>
                                        <th>Feedback</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    ${qr.criterion_scores.map(c => `
                                        <tr>
                                            <td>${c.criterion_name}</td>
                                            <td>${c.points_earned}/${c.points_possible}</td>
                                            <td>${c.specific_feedback}</td>
                                        </tr>
                                    `).join('')}
                                </tbody>
                            </table>
                        </div>
                    ` : ''}

                    <div class="feedback">
                        <h5>Feedback:</h5>
                        <p>${qr.feedback}</p>
                    </div>
                </div>
            `;
        });

        resultsContainer.innerHTML = html;
    }
}

// ==================== Rubric Upload Page ====================

function initRubricUploadPage() {
    const uploadForm = document.getElementById('rubric-upload-form');
    const fileUploadArea = document.getElementById('file-upload-area');
    const pdfUpload = document.getElementById('pdf-upload');
    const loadingOverlay = document.getElementById('loading-overlay');
    const previewSection = document.getElementById('preview-section');
    const rubricsList = document.getElementById('rubrics-list');

    let currentRubricId = null;

    // Load existing rubrics
    loadExistingRubrics();

    // File upload drag and drop
    if (fileUploadArea) {
        fileUploadArea.addEventListener('dragover', function(e) {
            e.preventDefault();
            this.style.borderColor = 'var(--primary-color)';
        });

        fileUploadArea.addEventListener('dragleave', function(e) {
            e.preventDefault();
            this.style.borderColor = 'var(--border-color)';
        });

        fileUploadArea.addEventListener('drop', function(e) {
            e.preventDefault();
            this.style.borderColor = 'var(--border-color)';

            const files = e.dataTransfer.files;
            if (files.length > 0 && files[0].type === 'application/pdf') {
                pdfUpload.files = files;
                updateFileInfo(files[0]);
            }
        });
    }

    // File input change
    if (pdfUpload) {
        pdfUpload.addEventListener('change', function(e) {
            if (e.target.files.length > 0) {
                updateFileInfo(e.target.files[0]);
            }
        });
    }

    // Update file info display
    function updateFileInfo(file) {
        const placeholder = fileUploadArea.querySelector('.upload-placeholder');
        const fileInfo = fileUploadArea.querySelector('.file-info');
        const fileName = fileInfo.querySelector('.file-name');

        placeholder.style.display = 'none';
        fileInfo.style.display = 'flex';
        fileName.textContent = file.name;
    }

    // Remove file
    const removeBtn = document.querySelector('.btn-remove');
    if (removeBtn) {
        removeBtn.addEventListener('click', function(e) {
            e.preventDefault();
            pdfUpload.value = '';
            const placeholder = fileUploadArea.querySelector('.upload-placeholder');
            const fileInfo = fileUploadArea.querySelector('.file-info');
            placeholder.style.display = 'block';
            fileInfo.style.display = 'none';
        });
    }

    // Form submission
    if (uploadForm) {
        uploadForm.addEventListener('submit', async function(e) {
            e.preventDefault();

            const formData = new FormData(this);
            loadingOverlay.style.display = 'flex';

            try {
                const response = await fetch('/api/rubrics/upload', {
                    method: 'POST',
                    body: formData
                });

                if (!response.ok) {
                    throw new Error('Upload failed');
                }

                const result = await response.json();
                currentRubricId = result.rubric_id;

                // Display success and preview
                displayRubricPreview(result);
                previewSection.style.display = 'block';
                previewSection.scrollIntoView({ behavior: 'smooth' });

                // Reload rubrics list
                loadExistingRubrics();

            } catch (error) {
                alert('Error uploading rubric: ' + error.message);
            } finally {
                loadingOverlay.style.display = 'none';
            }
        });
    }

    // Display rubric preview after extraction
    function displayRubricPreview(result) {
        const statusDiv = document.getElementById('extraction-status');
        const previewContent = document.getElementById('rubric-preview-content');

        statusDiv.innerHTML = `
            <div class="status-message status-success">
                ✓ Successfully extracted rubric with ${result.num_questions} questions (${result.total_points} points)
            </div>
        `;

        let html = `
            <h3>${result.extracted_data.exam_metadata.title}</h3>
            <p><strong>Total Points:</strong> ${result.total_points}</p>
            <p><strong>Questions:</strong> ${result.num_questions}</p>

            <div class="questions-list">
        `;

        result.extracted_data.questions.forEach(question => {
            html += `
                <div class="question-item">
                    <div class="question-header">
                        <strong>Question ${question.number}</strong>
                        <span class="question-type">${question.type}</span>
                        <span class="question-score">${question.points_possible} pts</span>
                    </div>
                    <p><strong>Description:</strong> ${question.description}</p>

                    ${question.grading_criteria && question.grading_criteria.length > 0 ? `
                        <div style="margin-top: 0.5rem;">
                            <strong>Grading Criteria:</strong>
                            <ul>
                                ${question.grading_criteria.map(c => `
                                    <li>${c.criterion} (${c.points} pts): ${c.full_credit}</li>
                                `).join('')}
                            </ul>
                        </div>
                    ` : ''}
                </div>
            `;
        });

        html += '</div>';
        previewContent.innerHTML = html;
    }

    // Create exam button
    const createExamBtn = document.getElementById('create-exam-button');
    if (createExamBtn) {
        createExamBtn.addEventListener('click', async function() {
            if (!currentRubricId) return;

            const examName = prompt('Enter exam name:');
            if (!examName) return;

            try {
                const response = await fetch('/api/exams', {
                    method: 'POST',
                    headers: {
                        'Content-Type': 'application/json'
                    },
                    body: JSON.stringify({
                        exam_name: examName,
                        rubric_id: currentRubricId
                    })
                });

                if (!response.ok) {
                    throw new Error('Failed to create exam');
                }

                alert('Exam created successfully! You can now grade submissions.');
                window.location.href = '/';

            } catch (error) {
                alert('Error creating exam: ' + error.message);
            }
        });
    }

    // Load existing rubrics
    async function loadExistingRubrics() {
        try {
            const response = await fetch('/api/rubrics');
            const data = await response.json();

            if (data.rubrics && data.rubrics.length > 0) {
                let html = '<div class="rubrics-grid">';

                data.rubrics.forEach(rubric => {
                    html += `
                        <div class="rubric-card">
                            <h4>${rubric.name}</h4>
                            <p>Total Points: ${rubric.total_points}</p>
                            <p>Questions: ${rubric.num_questions}</p>
                            <p>Uploaded: ${new Date(rubric.upload_date).toLocaleDateString()}</p>
                            <div class="button-group">
                                <button class="btn btn-secondary" onclick="viewRubric(${rubric.rubric_id})">View</button>
                                <button class="btn btn-primary" onclick="createExamFromRubric(${rubric.rubric_id}, '${rubric.name}')">Create Exam</button>
                            </div>
                        </div>
                    `;
                });

                html += '</div>';
                rubricsList.innerHTML = html;
            } else {
                rubricsList.innerHTML = '<p>No rubrics uploaded yet.</p>';
            }
        } catch (error) {
            console.error('Failed to load rubrics:', error);
        }
    }
}

// Helper functions for rubric management
async function viewRubric(rubricId) {
    window.open(`/api/rubrics/${rubricId}/pdf`, '_blank');
}

async function createExamFromRubric(rubricId, rubricName) {
    const examName = prompt(`Enter exam name (using rubric: ${rubricName}):`);
    if (!examName) return;

    try {
        const response = await fetch('/api/exams', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                exam_name: examName,
                rubric_id: rubricId
            })
        });

        if (!response.ok) {
            throw new Error('Failed to create exam');
        }

        alert('Exam created successfully!');
        window.location.href = '/';

    } catch (error) {
        alert('Error: ' + error.message);
    }
}

// ==================== Analytics Page ====================

function initAnalyticsPage() {
    const examSelect = document.getElementById('exam-select-analytics');
    const statsOverview = document.getElementById('stats-overview');
    const statsGrid = document.getElementById('stats-grid');
    const questionStats = document.getElementById('question-stats');
    const questionStatsContent = document.getElementById('question-stats-content');

    if (examSelect) {
        examSelect.addEventListener('change', async function() {
            const examId = this.value;
            if (examId) {
                await loadAnalytics(examId);
            } else {
                statsOverview.style.display = 'none';
                questionStats.style.display = 'none';
            }
        });
    }

    async function loadAnalytics(examId) {
        try {
            const response = await fetch(`/api/analytics/exam/${examId}`);
            const data = await response.json();

            displayStatistics(data);
            statsOverview.style.display = 'block';
            questionStats.style.display = 'block';

        } catch (error) {
            console.error('Failed to load analytics:', error);
        }
    }

    function displayStatistics(data) {
        // Overall statistics
        let html = `
            <div class="stat-card">
                <div class="stat-value">${data.num_submissions || 0}</div>
                <div class="stat-label">Submissions</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${(data.avg_score || 0).toFixed(1)}%</div>
                <div class="stat-label">Average Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${(data.max_score || 0).toFixed(1)}%</div>
                <div class="stat-label">Highest Score</div>
            </div>
            <div class="stat-card">
                <div class="stat-value">${(data.min_score || 0).toFixed(1)}%</div>
                <div class="stat-label">Lowest Score</div>
            </div>
        `;
        statsGrid.innerHTML = html;

        // Question statistics
        if (data.question_stats && data.question_stats.length > 0) {
            let qHtml = '<table class="criterion-table"><thead><tr><th>Question</th><th>Avg Score</th><th>Min</th><th>Max</th><th>Submissions</th></tr></thead><tbody>';

            data.question_stats.forEach(qs => {
                qHtml += `
                    <tr>
                        <td>Question ${qs.question_number}</td>
                        <td>${(qs.avg_score || 0).toFixed(2)}</td>
                        <td>${(qs.min_score || 0).toFixed(2)}</td>
                        <td>${(qs.max_score || 0).toFixed(2)}</td>
                        <td>${qs.num_answers || 0}</td>
                    </tr>
                `;
            });

            qHtml += '</tbody></table>';
            questionStatsContent.innerHTML = qHtml;
        }
    }
}

// ==================== Utility Functions ====================

function displayImagePreviews(files, container) {
    container.innerHTML = '';

    files.forEach((file, index) => {
        const reader = new FileReader();
        reader.onload = function(e) {
            const div = document.createElement('div');
            div.className = 'image-preview-item';
            div.innerHTML = `
                <img src="${e.target.result}" alt="Preview ${index + 1}">
                <p>Question ${index + 1}</p>
            `;
            container.appendChild(div);
        };
        reader.readAsDataURL(file);
    });
}
