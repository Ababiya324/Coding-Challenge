# Quick Start Guide - AI Exam Autograder

Get up and running in 5 minutes!

## Prerequisites Checklist

- [ ] Python 3.8+ installed
- [ ] Google Gemini API key (FREE!) ([Get one free](https://aistudio.google.com/app/apikey))
- [ ] Poppler installed (see below)

## Installation (Windows)

### 1. Install Poppler (Required for PDF Processing)

```bash
# Download from:
https://github.com/oschwartz10612/poppler-windows/releases/

# Extract to: C:\Program Files\poppler
# Add to PATH: C:\Program Files\poppler\Library\bin
```

### 2. Install Python Dependencies

```bash
cd ai-autograder
pip install -r requirements.txt
```

### 3. Configure API Key

```bash
# Copy the example file
copy .env.example .env

# Edit .env and add your API key:
# GEMINI_API_KEY=your_key_here
```

### 4. Run the Application

```bash
python app.py
```

Open browser to: **http://localhost:8000**

## First Time Usage

### Step 1: Upload a Rubric (2 minutes)

1. Click **Upload Rubric** in navigation
2. Enter name: "Test Exam"
3. Upload your PDF rubric
4. Wait for extraction (~30-60 seconds)
5. Click **Create Exam with This Rubric**

### Step 2: Grade a Submission (1-2 minutes)

1. Go to **Grade** page
2. Select your exam
3. Enter student ID: "student001"
4. Upload image(s) of student's exam
5. Click **Grade Submission**
6. Review results!

## Sample Rubric Format

Your PDF rubric should include:

```
Exam 2 - Data Structures
Total Points: 100

Question 1 (Code Tracing - 15 points)
Trace through the following code and write the output.

Question 2 (Free Response - 20 points)
Explain how a binary search tree works.

Grading Criteria:
- Technical Accuracy (10 pts): Correct explanation of BST properties
- Completeness (6 pts): Covers insertion, search, deletion
- Clarity (4 pts): Well-organized, clear writing
```

## Testing with Sample Data

### Sample Code Tracing Answer Key

```python
# Question 1 code:
for i in range(3):
    print(i * 2)

# Expected output:
0
2
4
```

Set via API or upload as answer key.

## Troubleshooting Quick Fixes

### "pdf2image not available"
→ Install Poppler (see Step 1)

### "Invalid API key"
→ Check your `.env` file

### Slow processing
→ Normal! First time takes longer. Subsequent grading is faster.

### Can't upload PDF
→ Check file size (<10MB)

## Next Steps

- Read full [README.md](README.md) for detailed documentation
- Check [API documentation](#) for programmatic access
- Explore analytics dashboard

## Getting Help

**Common Issues:**
1. Poppler not in PATH → Add to Windows environment variables
2. API rate limits → Wait a few seconds between requests
3. PDF extraction fails → Ensure PDF is text-based, not scanned image

**Still stuck?**
- Check console for error messages
- Review README.md
- Verify all dependencies installed

---

**Ready to grade 50+ students in minutes!** 🚀
