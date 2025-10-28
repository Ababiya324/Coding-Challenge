# AI Exam Autograder with PDF Rubric Upload

A comprehensive AI-powered exam autograding system that handles multiple question types with PDF rubric support. Built with FastAPI, Google Gemini AI, and modern web technologies.

## Features

### Core Capabilities

✅ **PDF Rubric Upload & Parsing**
- Upload rubrics as PDF files
- AI-powered extraction of grading criteria
- Support for tables, bullet points, and paragraph formats
- Automatic structuring of point values and expectations

✅ **Code Tracing Questions**
- Automatic code execution to verify answers
- Extraction of student answers from images
- Comparison with expected output
- Partial credit for close answers

✅ **Free Response Questions**
- AI-powered grading using uploaded rubric
- Criterion-by-criterion evaluation
- Detailed feedback and justification
- Strengths and improvement suggestions

✅ **Modern Web Interface**
- Clean, responsive design
- Drag-and-drop file upload
- Real-time progress tracking
- Detailed results visualization

✅ **Analytics Dashboard**
- Exam-level statistics
- Question-by-question analysis
- Grade distribution
- Performance insights

## System Architecture

```
ai-autograder/
├── app.py                      # FastAPI main application
├── requirements.txt            # Python dependencies
├── config.py                   # Configuration & settings
├── database.py                 # SQLite operations
├── models.py                   # Pydantic data models
├── .env                        # Environment variables (create from .env.example)
├── graders/
│   ├── rubric_parser.py       # PDF rubric extraction
│   ├── code_tracer.py         # Code tracing grader
│   └── free_response.py       # Free response grader
├── utils/
│   ├── pdf_handler.py         # PDF processing
│   ├── image_processor.py     # Image handling
│   ├── claude_client.py       # Claude API wrapper
│   └── export.py              # CSV/Excel export
├── static/
│   ├── css/style.css          # Styling
│   └── js/app.js              # Frontend logic
├── templates/
│   ├── index.html             # Grading interface
│   ├── rubric_upload.html     # Rubric upload page
│   ├── results.html           # Results display
│   └── analytics.html         # Analytics dashboard
└── data/
    ├── rubrics/               # Stored rubrics
    ├── uploads/               # Uploaded images
    └── database/              # SQLite database
```

## Installation & Setup

### Prerequisites

- Python 3.8 or higher
- Google Gemini API key (FREE!) ([Get one here](https://aistudio.google.com/app/apikey))
- Poppler (for PDF processing)

### Step 1: Install Python Dependencies

```bash
cd ai-autograder
pip install -r requirements.txt
```

### Step 2: Install Poppler (for PDF to Image Conversion)

**Windows:**
1. Download Poppler from: https://github.com/oschwartz10612/poppler-windows/releases/
2. Extract to `C:\Program Files\poppler`
3. Add `C:\Program Files\poppler\Library\bin` to your PATH

**macOS:**
```bash
brew install poppler
```

**Linux:**
```bash
sudo apt-get install poppler-utils
```

### Step 3: Configure Environment

1. Copy `.env.example` to `.env`:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Google Gemini API key (FREE!):
```
GEMINI_API_KEY=your_actual_api_key_here
```

### Step 4: Run the Application

```bash
python app.py
```

The application will start at: **http://localhost:8000**

## Usage Guide

### 1. Upload a Rubric

1. Navigate to **Upload Rubric** page
2. Enter a name for your rubric (e.g., "Exam 2 - Data Structures")
3. Drag and drop your PDF rubric or click to browse
4. Click **Upload & Extract Rubric**
5. Wait for AI to extract grading criteria (takes 30-60 seconds)
6. Review the extracted rubric
7. Click **Create Exam with This Rubric**

### 2. Create an Exam

After uploading a rubric:

1. Enter an exam name (e.g., "Midterm Exam - Fall 2024")
2. The exam will be linked to your rubric
3. (Optional) Upload an answer key for code tracing questions

### 3. Grade Student Submissions

1. Go to the main **Grade** page
2. Select your exam from the dropdown
3. Enter student ID
4. Upload images of the student's exam:
   - One image per question, or
   - Single PDF with all pages
5. Click **Grade Submission**
6. Wait for grading to complete (1-2 minutes per submission)
7. Review detailed results

### 4. View Results

Results include:
- **Overall score** and percentage
- **Letter grade**
- **Question-by-question breakdown**
- **Criterion evaluations** (for free response)
- **Specific feedback** for each question
- **Strengths and areas for improvement**

### 5. Analytics

1. Navigate to **Analytics** page
2. Select an exam
3. View:
   - Overall statistics (average, min, max scores)
   - Question-level performance
   - Grade distribution

## Answer Keys for Code Tracing

For code tracing questions, you need to provide either:

1. **The code to execute** (system runs it and compares output)
2. **Expected output** (if code can't be executed)

### Setting Answer Keys via API:

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
        "points_possible": 8
      },
      {
        "question_number": 2,
        "question_type": "code_tracing",
        "expected_output": "0\n2\n4",
        "points_possible": 8
      }
    ]
  }'
```

## API Endpoints

### Rubric Management

```
POST   /api/rubrics/upload          # Upload PDF rubric
GET    /api/rubrics                 # List all rubrics
GET    /api/rubrics/{id}            # Get rubric details
GET    /api/rubrics/{id}/pdf        # Download original PDF
PUT    /api/rubrics/{id}            # Update rubric
DELETE /api/rubrics/{id}            # Delete rubric
```

### Exam Management

```
POST   /api/exams                   # Create exam
GET    /api/exams                   # List all exams
GET    /api/exams/{id}              # Get exam details
PUT    /api/exams/{id}/answer-key   # Set answer key
```

### Grading

```
POST   /api/grade                   # Grade a submission
GET    /api/submissions/{id}        # Get submission results
```

### Analytics

```
GET    /api/analytics/exam/{id}     # Get exam statistics
```

## Configuration

### Environment Variables

Edit `.env` to customize:

```bash
# API Settings
GEMINI_API_KEY=your_key
GEMINI_MODEL=gemini-1.5-flash  # FREE tier

# PDF Processing
PDF_DPI=300                # Higher = better quality, larger files

# Grading
SIMILARITY_THRESHOLD=0.85  # For answer matching (0.0-1.0)
CODE_EXECUTION_TIMEOUT=5   # Max code execution time (seconds)
```

## Troubleshooting

### "pdf2image not available" Error

**Solution:** Install Poppler (see Installation Step 2)

### "Invalid API key" Error

**Solution:** Check your `.env` file has the correct `GEMINI_API_KEY`

### Rubric extraction fails

**Possible causes:**
- PDF is scanned at low quality → Use higher DPI (300+)
- PDF is password protected → Remove protection
- PDF has complex layouts → Try splitting into simpler pages

**Solution:** Check the PDF manually, ensure it's readable

### Code execution fails

**Possible causes:**
- Code has forbidden operations (file I/O, imports)
- Code has syntax errors

**Solution:** Provide expected output instead of code for complex cases

### Images not uploading

**Possible causes:**
- File size too large (max 10MB by default)
- Unsupported format

**Solution:**
- Compress images
- Use supported formats: JPG, PNG, PDF

## Security Notes

### Code Execution Sandbox

The code tracer uses a basic Python sandbox that:
- ✅ Allows: basic operations, loops, functions, print
- ❌ Blocks: file I/O, imports, system commands

**For production use:**
- Consider using Docker containers
- Implement stricter sandboxing
- Add execution time limits per student

### API Key Security

- **Never commit** `.env` to version control
- Use environment-specific API keys
- Rotate keys regularly

## Performance

### Typical Processing Times

- **Rubric extraction:** 30-60 seconds (one-time per rubric)
- **Single submission:** 1-2 minutes
- **Batch of 50 students:** 15-20 minutes

### Optimization Tips

1. **Batch processing:** Grade multiple students sequentially
2. **Image quality:** Use 300 DPI for balance between quality and speed
3. **Concurrent requests:** The system can handle multiple submissions in parallel

## Export Options

### Export Results to CSV

Results can be exported for:
- Learning Management Systems (LMS)
- Spreadsheet analysis
- Record keeping

(Export functionality is built-in but UI is not yet implemented - use API directly)

## Extending the System

### Adding New Question Types

1. Create a new grader in `graders/`
2. Implement the grading logic
3. Add to `QuestionType` enum in `models.py`
4. Update `app.py` to handle the new type

### Custom Rubric Formats

Modify `RUBRIC_EXTRACTION_PROMPT` in `config.py` to match your rubric style.

## Support

### Common Issues

- Check the console for detailed error messages
- Verify all dependencies are installed
- Ensure Poppler is in your PATH

### Getting Help

- Review this README
- Check the code comments
- Submit issues with:
  - Error messages
  - Steps to reproduce
  - Your environment (OS, Python version)

## License

This project is provided as-is for educational and internal use.

## Credits

Built with:
- FastAPI - Web framework
- Anthropic Claude - AI grading
- SQLite - Database
- pdf2image - PDF processing
- Pillow - Image handling

---

**Version:** 1.0.0
**Last Updated:** 2024
