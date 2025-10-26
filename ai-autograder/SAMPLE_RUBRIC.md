# Sample Exam Rubric

This is a text representation of what your PDF rubric should look like.
You can create a PDF version of this for testing.

---

## Computer Science Exam 2 - Data Structures & Algorithms

**Course:** CS 201
**Total Points:** 100
**Date:** Fall 2024

---

### Question 1: Code Tracing (15 points)

Trace through the following Python code and write exactly what it outputs:

```python
def mystery(n):
    result = []
    for i in range(n):
        if i % 2 == 0:
            result.append(i * 2)
    return result

print(mystery(5))
```

**Grading:**
- Full credit (15 pts): Correct output `[0, 4, 8]`
- Partial credit (8 pts): Correct values but wrong format
- No credit (0 pts): Incorrect output

---

### Question 2: Free Response - Binary Search Trees (25 points)

Explain how a binary search tree (BST) works and describe the process of inserting a new node.

**Grading Criteria:**

1. **Technical Accuracy (12 points)**
   - Full credit: Correctly explains BST property (left < parent < right) and insertion algorithm
   - Partial credit (6 pts): Explains BST property but insertion is incomplete
   - No credit: Incorrect or missing explanation

2. **Completeness (8 points)**
   - Full credit: Covers node comparison, traversal, and placement
   - Partial credit (4 pts): Missing one or more key concepts
   - No credit: Incomplete answer

3. **Clarity and Organization (5 points)**
   - Full credit: Well-structured, clear explanation with examples
   - Partial credit (3 pts): Understandable but lacks organization
   - No credit: Confusing or poorly written

**Common Mistakes to Watch For:**
- Confusing BST with balanced trees
- Not explaining the comparison process
- Missing the recursive nature of insertion

---

### Question 3: Algorithm Analysis (20 points)

What is the time complexity of binary search on a sorted array? Explain your reasoning.

**Grading Criteria:**

1. **Correct Answer (10 points)**
   - Full credit: O(log n) with correct reasoning
   - Partial credit (5 pts): O(log n) but incomplete reasoning
   - No credit: Wrong answer

2. **Explanation Quality (10 points)**
   - Full credit: Clearly explains halving the search space each iteration
   - Partial credit (5 pts): Basic explanation, missing details
   - No credit: No explanation or incorrect reasoning

---

### Question 4: Code Tracing - Recursion (15 points)

Trace through this recursive function with input `factorial(4)`:

```python
def factorial(n):
    if n <= 1:
        return 1
    return n * factorial(n - 1)
```

Write each recursive call and its return value.

**Grading:**
- Full credit (15 pts): Shows all calls: factorial(4)→4*factorial(3)→4*3*factorial(2)→4*3*2*factorial(1)→4*3*2*1=24
- Partial credit (10 pts): Correct final answer but missing intermediate steps
- Partial credit (5 pts): Shows recursion concept but incorrect values
- No credit: Incorrect understanding of recursion

---

### Question 5: Data Structure Selection (25 points)

You need to implement a web browser's back button functionality. Which data structure would you use and why? Describe how push and pop operations would work.

**Grading Criteria:**

1. **Data Structure Choice (10 points)**
   - Full credit: Stack with correct reasoning
   - Partial credit (5 pts): Stack mentioned but weak reasoning
   - No credit: Wrong data structure

2. **Implementation Description (10 points)**
   - Full credit: Clearly describes push (visit page), pop (back button)
   - Partial credit (5 pts): Basic understanding, missing details
   - No credit: Incorrect or missing

3. **Understanding of Operations (5 points)**
   - Full credit: Explains LIFO behavior and O(1) operations
   - Partial credit (3 pts): Mentions operations but not complexity
   - No credit: Missing or incorrect

---

## Grading Notes

- **Partial credit** should be awarded for demonstrated understanding even if answer is incomplete
- **Clarity matters**: Deduct points for extremely unclear explanations only if specified in rubric
- **Show your work**: Students should receive more credit for showing their reasoning
- **Common mistakes**: Don't overly penalize common conceptual errors unless they indicate fundamental misunderstanding

---

**Total Points: 100**

**Grading Scale:**
- A: 90-100
- B: 80-89
- C: 70-79
- D: 60-69
- F: <60
