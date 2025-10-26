"""
Pydantic models for data validation and API schemas
"""
from pydantic import BaseModel, Field, validator
from typing import List, Optional, Dict, Any
from datetime import datetime
from enum import Enum


class QuestionType(str, Enum):
    """Supported question types"""
    CODE_TRACING = "code_tracing"
    FREE_RESPONSE = "free_response"
    MULTIPLE_CHOICE = "multiple_choice"
    SHORT_ANSWER = "short_answer"


class GradeStatus(str, Enum):
    """Grading status"""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    ERROR = "error"


# ==================== Rubric Models ====================

class GradingCriterion(BaseModel):
    """Individual grading criterion from rubric"""
    criterion: str = Field(..., description="Name of the criterion")
    points: float = Field(..., description="Points allocated to this criterion")
    full_credit: str = Field(..., description="What earns full credit")
    partial_credit: Optional[str] = Field(None, description="Partial credit conditions")
    no_credit: Optional[str] = Field(None, description="What earns no credit")


class RubricQuestion(BaseModel):
    """Question definition from rubric"""
    number: int = Field(..., description="Question number")
    type: QuestionType = Field(..., description="Question type")
    points_possible: float = Field(..., description="Total points for this question")
    description: str = Field(..., description="Question text/description")
    grading_criteria: List[GradingCriterion] = Field(
        default_factory=list,
        description="Grading criteria for this question"
    )
    special_notes: Optional[str] = Field(None, description="Additional grading notes")


class ExamMetadata(BaseModel):
    """Exam metadata from rubric"""
    title: str = Field(..., description="Exam title")
    course: Optional[str] = Field(None, description="Course name/code")
    total_points: float = Field(..., description="Total points possible")
    instructions: Optional[str] = Field(None, description="General instructions")
    page_number: Optional[int] = Field(None, description="Page number if multi-page")


class ExtractedRubric(BaseModel):
    """Complete extracted rubric from PDF"""
    exam_metadata: ExamMetadata
    questions: List[RubricQuestion]


class RubricUploadResponse(BaseModel):
    """Response after rubric upload"""
    rubric_id: int
    name: str
    total_points: float
    num_questions: int
    extracted_data: ExtractedRubric
    pdf_path: str
    upload_date: datetime


# ==================== Grading Models ====================

class CriterionEvaluation(BaseModel):
    """Evaluation of a single criterion"""
    criterion_name: str
    points_earned: float
    points_possible: float
    justification: str
    specific_feedback: str
    rubric_alignment: Optional[str] = None


class FreeResponseGradeResult(BaseModel):
    """Result of grading a free response question"""
    student_response_extracted: str
    criterion_evaluations: List[CriterionEvaluation]
    total_score: float
    total_possible: float
    percentage: float
    overall_feedback: str
    strengths: List[str]
    areas_for_improvement: List[str]
    grade_letter: Optional[str] = None


class CodeTracingExtraction(BaseModel):
    """Extracted answer from code tracing question"""
    extracted_answer: str
    answer_format: str
    confidence: str
    notes: Optional[str] = None


class CodeTracingGradeResult(BaseModel):
    """Result of grading a code tracing question"""
    student_answer: str
    expected_answer: str
    is_correct: bool
    points_earned: float
    points_possible: float
    percentage: float
    feedback: str
    execution_output: Optional[str] = None
    execution_error: Optional[str] = None


class QuestionResult(BaseModel):
    """Result for a single question"""
    question_number: int
    question_type: QuestionType
    points_earned: float
    points_possible: float
    percentage: float
    feedback: str
    criterion_scores: Optional[List[CriterionEvaluation]] = None
    student_answer: Optional[str] = None
    expected_answer: Optional[str] = None


class SubmissionResult(BaseModel):
    """Complete grading result for a submission"""
    submission_id: int
    student_id: str
    exam_id: int
    exam_name: str
    status: GradeStatus
    total_score: float
    total_possible: float
    percentage: float
    grade_letter: Optional[str] = None
    question_results: List[QuestionResult]
    submitted_at: datetime
    graded_at: Optional[datetime] = None
    processing_time_seconds: Optional[float] = None


# ==================== API Request Models ====================

class RubricUploadRequest(BaseModel):
    """Request to upload a rubric"""
    name: str = Field(..., description="Name for this rubric")


class ExamCreateRequest(BaseModel):
    """Request to create an exam"""
    exam_name: str = Field(..., description="Name of the exam")
    rubric_id: int = Field(..., description="ID of the rubric to use")
    date: Optional[datetime] = Field(default_factory=datetime.now)


class GradeSubmissionRequest(BaseModel):
    """Request to grade a submission"""
    student_id: str = Field(..., description="Student identifier")
    exam_id: int = Field(..., description="Exam ID")
    # Images will be uploaded as multipart files


class AnswerKeyEntry(BaseModel):
    """Answer key for a code tracing question"""
    question_number: int
    question_type: QuestionType
    code: Optional[str] = Field(None, description="Code to execute for tracing")
    expected_output: Optional[str] = Field(None, description="Expected output")
    points_possible: float


class AnswerKey(BaseModel):
    """Answer key for an exam"""
    exam_id: int
    answers: List[AnswerKeyEntry]


# ==================== Database Models ====================

class RubricDB(BaseModel):
    """Rubric database model"""
    id: Optional[int] = None
    name: str
    pdf_path: str
    extracted_json: str  # JSON string of ExtractedRubric
    upload_date: datetime
    uploaded_by: Optional[str] = None
    total_points: float


class ExamDB(BaseModel):
    """Exam database model"""
    id: Optional[int] = None
    exam_name: str
    rubric_id: int
    date_created: datetime
    answer_key_json: Optional[str] = None  # JSON string of AnswerKey


class SubmissionDB(BaseModel):
    """Submission database model"""
    id: Optional[int] = None
    student_id: str
    exam_id: int
    status: GradeStatus
    total_score: Optional[float] = None
    total_possible: Optional[float] = None
    percentage: Optional[float] = None
    submitted_at: datetime
    graded_at: Optional[datetime] = None
    processing_time_seconds: Optional[float] = None


class QuestionResultDB(BaseModel):
    """Question result database model"""
    id: Optional[int] = None
    submission_id: int
    question_number: int
    question_type: QuestionType
    student_answer_text: Optional[str] = None
    points_earned: float
    points_possible: float
    criterion_scores: Optional[str] = None  # JSON string
    overall_feedback: str
    image_path: Optional[str] = None


# ==================== Analytics Models ====================

class QuestionStatistics(BaseModel):
    """Statistics for a question"""
    question_number: int
    average_score: float
    median_score: float
    max_score: float
    min_score: float
    std_deviation: float
    num_submissions: int


class ExamStatistics(BaseModel):
    """Statistics for an exam"""
    exam_id: int
    exam_name: str
    num_submissions: int
    average_score: float
    median_score: float
    std_deviation: float
    question_stats: List[QuestionStatistics]
    grade_distribution: Dict[str, int]  # Letter grade -> count
