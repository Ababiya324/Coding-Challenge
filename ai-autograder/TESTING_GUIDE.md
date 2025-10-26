# Testing Guide - AI Exam Autograder

Complete guide for testing all features of the autograding system.

## Prerequisites

Before testing, ensure:
- [x] Application is running (`python app.py`)
- [x] Anthropic API key is configured in `.env`
- [x] Poppler is installed and in PATH
- [x] Browser is open to http://localhost:8000

## Test Plan

### Test 1: Rubric Upload & Extraction

**Objective:** Verify PDF rubric upload and AI extraction works correctly.

**Steps:**

1. Create a test PDF rubric or use SAMPLE_RUBRIC.md
   - Convert SAMPLE_RUBRIC.md to PDF using Word/Google Docs
   - Or create a simple rubric in any format

2. Navigate to `/rubric-upload`

3. Fill in rubric name: "Test Rubric 1"

4. Upload the PDF:
   - Drag and drop, or
   - Click to browse

5. Click "Upload & Extract Rubric"

**Expected Results:**
- Loading overlay appears
- After 30-60 seconds, extraction completes
- Preview shows:
  - Exam title
  - Total points
  - List of questions with point values
  - Grading criteria for free response questions
- Success message displayed

**Pass Criteria:**
- ✅ All questions extracted
- ✅ Point values correct
- ✅ Criteria visible for free response
- ✅ No errors in console

---

### Test 2: Exam Creation

**Objective:** Create an exam linked to uploaded rubric.

**Steps:**

1. After successful rubric upload (Test 1)

2. Click "Create Exam with This Rubric"

3. Enter exam name: "Midterm Exam - Test"

4. Click OK

**Expected Results:**
- Success alert appears
- Redirected to main grading page
- New exam appears in exam dropdown

**Pass Criteria:**
- ✅ Exam created successfully
- ✅ Exam appears in dropdown on grade page
- ✅ Exam linked to correct rubric

---

### Test 3: Code Tracing Question Setup

**Objective:** Set up answer key for code tracing questions.

**Steps:**

1. Use curl or Postman to set answer key:

```bash
curl -X PUT http://localhost:8000/api/exams/1/answer-key \
  -H "Content-Type: application/json" \
  -d '{
    "exam_id": 1,
    "answers": [
      {
        "question_number": 1,
        "question_type": "code_tracing",
        "code": "for i in range(3):\n    print(i * 2)",
        "points_possible": 15
      }
    ]
  }'
```

**Expected Results:**
- Success response: `{"status": "success", "message": "Answer key updated"}`
- Answer key stored in database

**Pass Criteria:**
- ✅ API returns success
- ✅ No errors

---

### Test 4: Grade Code Tracing Question

**Objective:** Grade a student's code tracing answer.

**Preparation:**
1. Create a test image:
   - Write on paper: "0\n2\n4"
   - Take a photo or scan
   - Save as test_answer_q1.jpg

**Steps:**

1. Go to main grading page

2. Select "Midterm Exam - Test"

3. Enter Student ID: "student001"

4. Upload the test image

5. Click "Grade Submission"

**Expected Results:**
- Loading overlay shows
- After 1-2 minutes, results appear
- Shows:
  - Total score
  - Question 1: Full points (if answer is correct)
  - Student's extracted answer
  - Expected answer
  - Feedback

**Pass Criteria:**
- ✅ Submission processes without errors
- ✅ Answer extracted correctly from image
- ✅ Comparison with expected output works
- ✅ Correct score awarded
- ✅ Feedback is relevant

---

### Test 5: Grade Free Response Question

**Objective:** Grade a free response answer using rubric criteria.

**Preparation:**
1. Create test answer image:
   - Write answer to BST question from SAMPLE_RUBRIC.md
   - Example: "A binary search tree maintains the property that left child < parent < right child..."
   - Take photo or scan
   - Save as test_answer_q2.jpg

**Steps:**

1. Grade page → Select exam

2. Student ID: "student002"

3. Upload test answer image

4. Click "Grade Submission"

**Expected Results:**
- Results show:
  - Criterion-by-criterion evaluation
  - Points per criterion
  - Specific feedback for each criterion
  - Overall feedback
  - Strengths and improvements
- Score matches rubric expectations

**Pass Criteria:**
- ✅ All criteria evaluated
- ✅ Points allocated correctly
- ✅ Feedback is specific and constructive
- ✅ Overall score calculated correctly

---

### Test 6: View Results Page

**Objective:** Verify results display correctly.

**Steps:**

1. After grading (Test 4 or 5)

2. Click on submission ID or navigate to `/results/{submission_id}`

**Expected Results:**
- Page displays:
  - Student ID
  - Exam name
  - Total score with percentage
  - Grade letter
  - Question breakdown
  - Detailed feedback
  - Criterion tables (for free response)

**Pass Criteria:**
- ✅ All information displays correctly
- ✅ Layout is clean and readable
- ✅ Print button works
- ✅ No broken images or missing data

---

### Test 7: Analytics Dashboard

**Objective:** Verify analytics calculations.

**Preparation:**
- Grade at least 3 submissions with different scores

**Steps:**

1. Navigate to `/analytics`

2. Select exam from dropdown

**Expected Results:**
- Statistics display:
  - Number of submissions
  - Average score
  - Min/max scores
  - Question-level statistics
  - Grade distribution

**Pass Criteria:**
- ✅ Calculations are accurate
- ✅ All stats display
- ✅ No divide-by-zero errors
- ✅ Data matches actual submissions

---

### Test 8: Multiple Question Types

**Objective:** Grade an exam with both code tracing and free response.

**Preparation:**
1. Create rubric with:
   - Question 1: Code tracing (15 pts)
   - Question 2: Free response (25 pts)
2. Create answer key for Q1
3. Prepare two answer images (one per question)

**Steps:**

1. Upload rubric

2. Create exam

3. Set answer key

4. Grade submission with both images

**Expected Results:**
- Both questions graded correctly
- Each uses appropriate grading method
- Total score combines both correctly

**Pass Criteria:**
- ✅ Code tracing uses execution/comparison
- ✅ Free response uses rubric criteria
- ✅ Scores calculated correctly
- ✅ Both feedbacks relevant

---

### Test 9: Error Handling

**Objective:** Verify system handles errors gracefully.

**Test Cases:**

**9a. Upload non-PDF file**
- Try uploading .txt or .jpg as rubric
- Expected: Error message, upload rejected

**9b. Upload corrupted PDF**
- Upload invalid PDF
- Expected: Error message, graceful failure

**9c. Grade without images**
- Try to grade with no images uploaded
- Expected: Button disabled or validation error

**9d. Invalid student ID**
- Leave student ID empty
- Expected: Validation error

**9e. Missing answer key**
- Try to grade code tracing without answer key
- Expected: Error message explaining missing key

**Pass Criteria:**
- ✅ All errors handled gracefully
- ✅ User-friendly error messages
- ✅ No system crashes
- ✅ Can recover and continue

---

### Test 10: Edge Cases

**Test Cases:**

**10a. Multi-page rubric**
- Upload 3-page PDF rubric
- Expected: All pages processed, questions combined

**10b. Large images**
- Upload high-resolution images (5MB+)
- Expected: Processing works (may be slower)

**10c. Handwritten answers**
- Upload handwritten answers (clear handwriting)
- Expected: OCR/extraction works reasonably well

**10d. Partial answers**
- Submit incomplete answers
- Expected: Partial credit awarded, feedback notes missing parts

**10e. Perfect answer**
- Submit textbook-perfect answer
- Expected: Full points, positive feedback

**Pass Criteria:**
- ✅ System handles edge cases
- ✅ No crashes
- ✅ Reasonable behavior for each case

---

## Performance Testing

### Test 11: Speed Benchmarks

**Single Submission:**
- Expected: 1-2 minutes
- Measure: Time from submit to results

**Rubric Extraction:**
- Expected: 30-60 seconds per page
- Measure: Upload to preview

**Batch Processing:**
- Grade 10 submissions sequentially
- Expected: ~10-20 minutes
- Track: Average time per submission

---

## Regression Testing

After any code changes, re-run:
- Test 1 (Rubric upload)
- Test 4 (Code tracing)
- Test 5 (Free response)
- Test 9 (Error handling)

---

## Test Data

### Sample Correct Answers

**Code Tracing (Question 1):**
```
0
2
4
```

**Free Response (Question 2):**
```
A binary search tree (BST) is a data structure where each node
has at most two children. The BST property states that all nodes
in the left subtree have values less than the parent, and all
nodes in the right subtree have values greater than the parent.

To insert a new node:
1. Start at the root
2. Compare the new value with current node
3. If smaller, go left; if larger, go right
4. Repeat until finding an empty spot
5. Insert the new node there

This maintains the BST property and allows O(log n) search time
in balanced trees.
```

---

## Reporting Issues

When reporting bugs, include:
1. Test number
2. Steps taken
3. Expected vs actual result
4. Screenshots
5. Console errors
6. Browser and OS

---

## Success Criteria

System is production-ready when:
- ✅ All 10 tests pass
- ✅ No critical bugs
- ✅ Performance acceptable
- ✅ Error handling robust
- ✅ Documentation complete
