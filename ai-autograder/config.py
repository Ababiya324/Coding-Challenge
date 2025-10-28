"""
Configuration settings for AI Autograder
"""
import os
from pathlib import Path
from pydantic_settings import BaseSettings
from typing import Optional

# Base directory paths
BASE_DIR = Path(__file__).resolve().parent
DATA_DIR = BASE_DIR / "data"
RUBRICS_DIR = DATA_DIR / "rubrics"
ANSWER_KEYS_DIR = DATA_DIR / "answer_keys"
UPLOADS_DIR = DATA_DIR / "uploads"
DATABASE_DIR = DATA_DIR / "database"

# Ensure all directories exist
for directory in [DATA_DIR, RUBRICS_DIR, ANSWER_KEYS_DIR, UPLOADS_DIR, DATABASE_DIR]:
    directory.mkdir(parents=True, exist_ok=True)


class Settings(BaseSettings):
    """Application settings loaded from environment variables"""

    # API Keys
    GEMINI_API_KEY: str

    # Gemini API Settings
    GEMINI_MODEL: str = "gemini-1.5-flash"  # Free tier model with vision support
    GEMINI_MAX_TOKENS: int = 8192
    GEMINI_TEMPERATURE: float = 0.0

    # Database
    DATABASE_URL: str = f"sqlite:///{DATABASE_DIR / 'autograder.db'}"

    # File Upload Settings
    MAX_UPLOAD_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_IMAGE_EXTENSIONS: set = {".jpg", ".jpeg", ".png", ".pdf", ".tiff"}
    ALLOWED_PDF_EXTENSIONS: set = {".pdf"}

    # PDF Processing
    PDF_DPI: int = 300  # High quality for OCR
    PDF_FORMAT: str = "png"

    # Grading Settings
    CODE_EXECUTION_TIMEOUT: int = 5  # seconds
    SIMILARITY_THRESHOLD: float = 0.85  # For answer matching

    # Application Settings
    APP_NAME: str = "AI Exam Autograder"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = False

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"


# Initialize settings
settings = Settings()


# Rubric extraction prompt template
RUBRIC_EXTRACTION_PROMPT = """You are analyzing a professor's exam rubric PDF. Extract ALL grading information with high precision.

PDF PAGE: [The image shows a page from the rubric]

Extract and structure the following information:

1. **Exam Information:**
   - Exam name/title
   - Course name/code (if mentioned)
   - Total points possible
   - Any general instructions or notes

2. **For EACH Question:**
   - Question number
   - Question type (code tracing, free response, multiple choice, short answer, etc.)
   - Point value
   - Complete question text/description
   - Specific grading criteria

3. **For FREE RESPONSE questions specifically:**
   - Break down into grading dimensions/criteria (e.g., technical accuracy, completeness, clarity)
   - Points allocated to each criterion
   - What constitutes full credit vs partial credit vs no credit
   - Common mistakes to watch for (if mentioned)
   - Example answers or key points expected (if provided)

4. **For CODE TRACING questions:**
   - Expected outputs or answer format
   - Partial credit rules
   - Whether formatting/spacing matters
   - Any specific grading notes

5. **For any OTHER question types:**
   - Extract all relevant grading information
   - Note any special instructions

RESPOND IN THIS EXACT JSON FORMAT:
{
  "exam_metadata": {
    "title": "exam title here",
    "course": "course name/code if mentioned",
    "total_points": numeric value,
    "instructions": "any general instructions",
    "page_number": current page number (if indicated)
  },
  "questions": [
    {
      "number": question number as integer,
      "type": "code_tracing" or "free_response" or "multiple_choice" or "short_answer",
      "points_possible": numeric point value,
      "description": "complete question text",
      "grading_criteria": [
        {
          "criterion": "name of criterion (e.g., 'Technical Accuracy', 'Completeness')",
          "points": numeric points for this criterion,
          "full_credit": "description of what earns full points",
          "partial_credit": "description of partial credit conditions",
          "no_credit": "description of what earns no points"
        }
      ],
      "special_notes": "any additional grading notes"
    }
  ]
}

IMPORTANT INSTRUCTIONS:
- Extract ALL information visible on this page
- If this is a multi-page rubric, focus only on THIS page's content
- Preserve exact wording from the rubric where possible
- If certain fields are not present, use null or empty string
- Be precise with numeric values (points)
- If a question has sub-parts, include them as separate entries or note them in the description
"""


# Free response grading prompt template
FREE_RESPONSE_GRADING_PROMPT = """You are grading a student's free response answer using the professor's official rubric.

QUESTION INFORMATION:
{question_description}

POINTS POSSIBLE: {points_possible}

PROFESSOR'S GRADING RUBRIC:
{rubric_criteria}

STUDENT'S ANSWER: [See the attached image]

YOUR GRADING TASK:
1. Carefully read and extract the student's complete written response from the image
2. Evaluate the response against EACH criterion specified in the professor's rubric
3. Assign points for each criterion based on the rubric's expectations for full/partial/no credit
4. Provide specific, constructive feedback justifying each score
5. Calculate the total score
6. Provide overall feedback and suggestions for improvement

RESPOND IN THIS EXACT JSON FORMAT:
{{
  "student_response_extracted": "The complete text of what the student wrote (transcribed from image)",
  "criterion_evaluations": [
    {{
      "criterion_name": "Name of the criterion",
      "points_earned": numeric value,
      "points_possible": numeric value,
      "justification": "Detailed explanation of why this score was given",
      "specific_feedback": "Constructive feedback for the student on this criterion",
      "rubric_alignment": "How the response met/didn't meet the rubric expectations"
    }}
  ],
  "total_score": numeric total points earned,
  "total_possible": numeric total points possible,
  "percentage": numeric percentage (total_score/total_possible * 100),
  "overall_feedback": "Overall assessment of the student's response",
  "strengths": ["specific strength 1", "specific strength 2"],
  "areas_for_improvement": ["specific area 1", "specific area 2"],
  "grade_letter": "Letter grade if applicable (A, B, C, D, F or null)"
}}

GRADING GUIDELINES:
- Be fair and consistent with the rubric
- Give partial credit where appropriate according to rubric guidelines
- Provide specific, actionable feedback
- If the student's answer is partially correct, explain what's missing
- If handwriting is unclear, note this but do your best to interpret
- Focus on the substance of the answer, not minor grammar/spelling unless the rubric specifies this
"""


# Code tracing grading prompt template
CODE_TRACING_EXTRACTION_PROMPT = """You are extracting a student's answer from their exam image for a code tracing question.

QUESTION DESCRIPTION: {question_description}

TASK: Extract the student's written answer/output for this code tracing question from the image.

The student was asked to trace through code and write what the output would be. This might include:
- Print statements output
- Variable values at certain points
- Return values
- Loop iteration results
- Any other code execution results

STUDENT'S ANSWER IMAGE: [See attached image]

RESPOND IN THIS JSON FORMAT:
{{
  "extracted_answer": "The student's complete written answer exactly as shown",
  "answer_format": "description of how the answer is formatted (e.g., 'line by line output', 'single value', 'list of values')",
  "confidence": "high/medium/low - your confidence in the extraction accuracy",
  "notes": "any relevant notes about handwriting clarity, formatting, etc."
}}

EXTRACTION GUIDELINES:
- Extract EXACTLY what the student wrote
- Preserve line breaks, spacing, and formatting where relevant
- If handwriting is unclear, make your best interpretation and note it
- If parts are illegible, indicate this clearly
- Do not evaluate correctness - only extract what's written
"""
