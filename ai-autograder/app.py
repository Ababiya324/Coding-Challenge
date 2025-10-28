"""
FastAPI application for AI Exam Autograder
Main entry point with all API endpoints
"""
import json
import shutil
from pathlib import Path
from typing import List, Optional
from datetime import datetime
import asyncio

from fastapi import FastAPI, File, UploadFile, Form, HTTPException, BackgroundTasks
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import FileResponse, JSONResponse
from fastapi import Request
import uvicorn

from config import (
    settings,
    RUBRICS_DIR,
    UPLOADS_DIR,
    ANSWER_KEYS_DIR,
    BASE_DIR
)
from database import db
from models import (
    RubricUploadResponse,
    ExamCreateRequest,
    GradeSubmissionRequest,
    SubmissionResult,
    QuestionResult,
    GradeStatus,
    RubricDB,
    ExamDB,
    SubmissionDB,
    QuestionResultDB,
    ExtractedRubric,
    AnswerKey,
    QuestionType
)
from utils.pdf_handler import create_pdf_handler
from utils.gemini_client import create_gemini_client
from utils.image_processor import create_image_processor
from utils.export import create_results_exporter
from graders.rubric_parser import create_rubric_parser
from graders.code_tracer import create_code_tracer_grader
from graders.free_response import create_free_response_grader


# Initialize FastAPI app
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="AI-powered exam autograding system with PDF rubric support"
)

# Mount static files
app.mount("/static", StaticFiles(directory=str(BASE_DIR / "static")), name="static")

# Setup templates
templates = Jinja2Templates(directory=str(BASE_DIR / "templates"))

# Initialize utilities
pdf_handler = create_pdf_handler(dpi=settings.PDF_DPI, image_format=settings.PDF_FORMAT)
gemini_client = create_gemini_client()
image_processor = create_image_processor()
results_exporter = create_results_exporter()

# Initialize graders
rubric_parser = create_rubric_parser(gemini_client, pdf_handler)
code_tracer = create_code_tracer_grader(gemini_client)
free_response_grader = create_free_response_grader(gemini_client)


# ==================== Startup/Shutdown Events ====================

@app.on_event("startup")
async def startup_event():
    """Initialize database on startup"""
    await db.init_db()
    print(f"✓ {settings.APP_NAME} started successfully")
    print(f"✓ Database initialized at: {db.db_path}")


# ==================== Web Interface Routes ====================

@app.get("/")
async def index(request: Request):
    """Main grading interface"""
    # Get list of exams for selection
    exams = await db.list_exams()

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "app_name": settings.APP_NAME,
            "exams": exams
        }
    )


@app.get("/rubric-upload")
async def rubric_upload_page(request: Request):
    """Rubric upload interface"""
    return templates.TemplateResponse(
        "rubric_upload.html",
        {
            "request": request,
            "app_name": settings.APP_NAME
        }
    )


@app.get("/results/{submission_id}")
async def results_page(request: Request, submission_id: int):
    """View detailed results for a submission"""
    submission = await db.get_submission(submission_id)

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    # Get exam info
    exam = await db.get_exam(submission.exam_id)

    # Get question results
    question_results = await db.get_submission_results(submission_id)

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "app_name": settings.APP_NAME,
            "submission": submission,
            "exam": exam,
            "question_results": question_results
        }
    )


@app.get("/analytics")
async def analytics_page(request: Request):
    """Analytics dashboard"""
    exams = await db.list_exams()

    return templates.TemplateResponse(
        "analytics.html",
        {
            "request": request,
            "app_name": settings.APP_NAME,
            "exams": exams
        }
    )


# ==================== API Endpoints - Rubric Management ====================

@app.post("/api/rubrics/upload", response_model=RubricUploadResponse)
async def upload_rubric(
    name: str = Form(...),
    file: UploadFile = File(...)
):
    """
    Upload and parse a PDF rubric

    Args:
        name: Name for this rubric
        file: PDF file

    Returns:
        RubricUploadResponse with extracted data
    """
    # Validate file
    if not file.filename.endswith('.pdf'):
        raise HTTPException(status_code=400, detail="File must be a PDF")

    # Save uploaded PDF
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    pdf_filename = f"{name.replace(' ', '_')}_{timestamp}.pdf"
    pdf_path = RUBRICS_DIR / pdf_filename

    try:
        # Save file
        with open(pdf_path, 'wb') as f:
            shutil.copyfileobj(file.file, f)

        # Parse rubric
        print(f"Parsing rubric: {name}")
        extracted_rubric = await rubric_parser.parse_rubric_pdf(pdf_path, name)

        # Validate rubric
        extracted_rubric = await rubric_parser.validate_and_fix_rubric(extracted_rubric, pdf_path)

        # Save to database
        rubric_db = RubricDB(
            name=name,
            pdf_path=str(pdf_path),
            extracted_json=extracted_rubric.model_dump_json(),
            upload_date=datetime.now(),
            uploaded_by="admin",  # TODO: Add user authentication
            total_points=extracted_rubric.exam_metadata.total_points
        )

        rubric_id = await db.create_rubric(rubric_db)

        # Save JSON version
        json_path = pdf_path.with_suffix('.json')
        rubric_parser.save_rubric_json(extracted_rubric, json_path)

        return RubricUploadResponse(
            rubric_id=rubric_id,
            name=name,
            total_points=extracted_rubric.exam_metadata.total_points,
            num_questions=len(extracted_rubric.questions),
            extracted_data=extracted_rubric,
            pdf_path=str(pdf_path),
            upload_date=rubric_db.upload_date
        )

    except Exception as e:
        # Clean up file on error
        if pdf_path.exists():
            pdf_path.unlink()
        raise HTTPException(status_code=500, detail=f"Failed to process rubric: {str(e)}")


@app.get("/api/rubrics/{rubric_id}")
async def get_rubric(rubric_id: int):
    """Get rubric details"""
    rubric = await db.get_rubric(rubric_id)

    if not rubric:
        raise HTTPException(status_code=404, detail="Rubric not found")

    # Parse extracted JSON
    extracted_data = json.loads(rubric.extracted_json)

    return {
        "rubric_id": rubric.id,
        "name": rubric.name,
        "total_points": rubric.total_points,
        "upload_date": rubric.upload_date,
        "extracted_data": extracted_data,
        "pdf_path": rubric.pdf_path
    }


@app.get("/api/rubrics")
async def list_rubrics():
    """List all rubrics"""
    rubrics = await db.list_rubrics()

    return {
        "rubrics": [
            {
                "rubric_id": r.id,
                "name": r.name,
                "total_points": r.total_points,
                "upload_date": r.upload_date,
                "num_questions": len(json.loads(r.extracted_json).get('questions', []))
            }
            for r in rubrics
        ]
    }


@app.get("/api/rubrics/{rubric_id}/pdf")
async def download_rubric_pdf(rubric_id: int):
    """Download original rubric PDF"""
    rubric = await db.get_rubric(rubric_id)

    if not rubric:
        raise HTTPException(status_code=404, detail="Rubric not found")

    pdf_path = Path(rubric.pdf_path)
    if not pdf_path.exists():
        raise HTTPException(status_code=404, detail="PDF file not found")

    return FileResponse(pdf_path, media_type="application/pdf", filename=pdf_path.name)


@app.put("/api/rubrics/{rubric_id}")
async def update_rubric(rubric_id: int, rubric_data: dict):
    """Update rubric's extracted data (manual corrections)"""
    rubric = await db.get_rubric(rubric_id)

    if not rubric:
        raise HTTPException(status_code=404, detail="Rubric not found")

    try:
        # Validate updated data
        extracted_rubric = ExtractedRubric(**rubric_data)

        # Update database
        await db.update_rubric(
            rubric_id,
            extracted_rubric.model_dump_json(),
            extracted_rubric.exam_metadata.total_points
        )

        return {"status": "success", "message": "Rubric updated"}

    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Invalid rubric data: {str(e)}")


@app.delete("/api/rubrics/{rubric_id}")
async def delete_rubric(rubric_id: int):
    """Delete a rubric"""
    rubric = await db.get_rubric(rubric_id)

    if not rubric:
        raise HTTPException(status_code=404, detail="Rubric not found")

    # Delete files
    pdf_path = Path(rubric.pdf_path)
    if pdf_path.exists():
        pdf_path.unlink()

    json_path = pdf_path.with_suffix('.json')
    if json_path.exists():
        json_path.unlink()

    # Delete from database
    await db.delete_rubric(rubric_id)

    return {"status": "success", "message": "Rubric deleted"}


# ==================== API Endpoints - Exam Management ====================

@app.post("/api/exams")
async def create_exam(exam_request: ExamCreateRequest):
    """Create a new exam"""
    # Verify rubric exists
    rubric = await db.get_rubric(exam_request.rubric_id)
    if not rubric:
        raise HTTPException(status_code=404, detail="Rubric not found")

    # Create exam
    exam_db = ExamDB(
        exam_name=exam_request.exam_name,
        rubric_id=exam_request.rubric_id,
        date_created=exam_request.date or datetime.now(),
        answer_key_json=None
    )

    exam_id = await db.create_exam(exam_db)

    return {
        "exam_id": exam_id,
        "exam_name": exam_request.exam_name,
        "rubric_id": exam_request.rubric_id,
        "date_created": exam_db.date_created
    }


@app.get("/api/exams")
async def list_exams():
    """List all exams"""
    exams = await db.list_exams()

    result = []
    for exam in exams:
        rubric = await db.get_rubric(exam.rubric_id)
        result.append({
            "exam_id": exam.id,
            "exam_name": exam.exam_name,
            "rubric_id": exam.rubric_id,
            "rubric_name": rubric.name if rubric else "Unknown",
            "date_created": exam.date_created
        })

    return {"exams": result}


@app.get("/api/exams/{exam_id}")
async def get_exam(exam_id: int):
    """Get exam details"""
    exam = await db.get_exam(exam_id)

    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    rubric = await db.get_rubric(exam.rubric_id)

    return {
        "exam_id": exam.id,
        "exam_name": exam.exam_name,
        "rubric_id": exam.rubric_id,
        "rubric_name": rubric.name if rubric else "Unknown",
        "date_created": exam.date_created,
        "answer_key": json.loads(exam.answer_key_json) if exam.answer_key_json else None
    }


@app.put("/api/exams/{exam_id}/answer-key")
async def update_answer_key(exam_id: int, answer_key: AnswerKey):
    """Update exam's answer key for code tracing questions"""
    exam = await db.get_exam(exam_id)

    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    # Save answer key
    await db.update_answer_key(exam_id, answer_key.model_dump_json())

    return {"status": "success", "message": "Answer key updated"}


# ==================== API Endpoints - Grading ====================

@app.post("/api/grade")
async def grade_submission(
    student_id: str = Form(...),
    exam_id: int = Form(...),
    images: List[UploadFile] = File(...)
):
    """
    Grade a student submission

    Args:
        student_id: Student identifier
        exam_id: Exam ID
        images: List of image files (one per question or combined)

    Returns:
        Submission result
    """
    start_time = datetime.now()

    # Get exam and rubric
    exam = await db.get_exam(exam_id)
    if not exam:
        raise HTTPException(status_code=404, detail="Exam not found")

    rubric = await db.get_rubric(exam.rubric_id)
    if not rubric:
        raise HTTPException(status_code=404, detail="Rubric not found")

    extracted_rubric = ExtractedRubric(**json.loads(rubric.extracted_json))

    # Create submission record
    submission_db = SubmissionDB(
        student_id=student_id,
        exam_id=exam_id,
        status=GradeStatus.PROCESSING,
        submitted_at=datetime.now()
    )
    submission_id = await db.create_submission(submission_db)

    try:
        # Save uploaded images
        image_paths = []
        for i, image_file in enumerate(images):
            # Save image
            img_filename = f"submission_{submission_id}_q{i+1}_{image_file.filename}"
            img_path = UPLOADS_DIR / img_filename

            with open(img_path, 'wb') as f:
                shutil.copyfileobj(image_file.file, f)

            image_paths.append(img_path)

        # Get answer key if available
        answer_key = None
        if exam.answer_key_json:
            answer_key = AnswerKey(**json.loads(exam.answer_key_json))

        # Grade each question
        question_results = []
        total_score = 0.0
        total_possible = 0.0

        for i, question in enumerate(extracted_rubric.questions):
            # Determine which image to use (assume one image per question for now)
            img_path = image_paths[min(i, len(image_paths) - 1)]

            # Grade based on question type
            if question.type == QuestionType.CODE_TRACING:
                result = await grade_code_tracing_question(
                    question, img_path, answer_key
                )
            elif question.type == QuestionType.FREE_RESPONSE:
                result = await grade_free_response_question(
                    question, img_path
                )
            else:
                # Unsupported type - skip
                continue

            # Save question result
            question_result_db = QuestionResultDB(
                submission_id=submission_id,
                question_number=question.number,
                question_type=question.type,
                student_answer_text=result.get('student_answer', ''),
                points_earned=result['points_earned'],
                points_possible=result['points_possible'],
                criterion_scores=json.dumps(result.get('criterion_scores', [])),
                overall_feedback=result['feedback'],
                image_path=str(img_path)
            )
            await db.create_question_result(question_result_db)

            question_results.append(result)
            total_score += result['points_earned']
            total_possible += result['points_possible']

        # Calculate final scores
        percentage = (total_score / total_possible * 100) if total_possible > 0 else 0
        grade_letter = calculate_grade_letter(percentage)

        # Update submission
        processing_time = (datetime.now() - start_time).total_seconds()
        await db.update_submission(
            submission_id,
            status=GradeStatus.COMPLETED,
            total_score=total_score,
            total_possible=total_possible,
            percentage=percentage,
            graded_at=datetime.now(),
            processing_time=processing_time
        )

        return {
            "submission_id": submission_id,
            "student_id": student_id,
            "exam_id": exam_id,
            "exam_name": exam.exam_name,
            "status": "completed",
            "total_score": total_score,
            "total_possible": total_possible,
            "percentage": percentage,
            "grade_letter": grade_letter,
            "question_results": question_results,
            "processing_time_seconds": processing_time
        }

    except Exception as e:
        # Update submission as error
        await db.update_submission(submission_id, status=GradeStatus.ERROR)
        raise HTTPException(status_code=500, detail=f"Grading failed: {str(e)}")


async def grade_code_tracing_question(question, image_path, answer_key):
    """Grade a code tracing question"""
    # Find answer in answer key
    if answer_key:
        answer_entry = next(
            (a for a in answer_key.answers if a.question_number == question.number),
            None
        )

        if answer_entry and answer_entry.code:
            # Execute code and grade
            result = await code_tracer.grade_code_tracing(
                code=answer_entry.code,
                student_image_path=image_path,
                points_possible=question.points_possible,
                question_description=question.description
            )
        elif answer_entry and answer_entry.expected_output:
            # Extract answer and compare with expected
            extraction = await code_tracer._extract_student_answer(
                image_path,
                question.description
            )
            result = code_tracer.grade_with_expected_output(
                expected_output=answer_entry.expected_output,
                student_answer=extraction.extracted_answer,
                points_possible=question.points_possible
            )
        else:
            raise ValueError(f"No answer key found for question {question.number}")
    else:
        raise ValueError(f"Answer key required for code tracing question {question.number}")

    return {
        'question_number': question.number,
        'points_earned': result.points_earned,
        'points_possible': result.points_possible,
        'feedback': result.feedback,
        'student_answer': result.student_answer,
        'expected_answer': result.expected_answer
    }


async def grade_free_response_question(question, image_path):
    """Grade a free response question"""
    result = await free_response_grader.grade_with_rubric(
        student_image_path=image_path,
        rubric_question=question
    )

    return {
        'question_number': question.number,
        'points_earned': result.total_score,
        'points_possible': result.total_possible,
        'feedback': result.overall_feedback,
        'student_answer': result.student_response_extracted,
        'criterion_scores': [c.model_dump() for c in result.criterion_evaluations]
    }


def calculate_grade_letter(percentage: float) -> str:
    """Convert percentage to letter grade"""
    if percentage >= 90:
        return "A"
    elif percentage >= 80:
        return "B"
    elif percentage >= 70:
        return "C"
    elif percentage >= 60:
        return "D"
    else:
        return "F"


@app.get("/api/submissions/{submission_id}")
async def get_submission_details(submission_id: int):
    """Get detailed submission results"""
    submission = await db.get_submission(submission_id)

    if not submission:
        raise HTTPException(status_code=404, detail="Submission not found")

    # Get exam info
    exam = await db.get_exam(submission.exam_id)

    # Get question results
    question_results = await db.get_submission_results(submission_id)

    return {
        "submission_id": submission.id,
        "student_id": submission.student_id,
        "exam_id": submission.exam_id,
        "exam_name": exam.exam_name if exam else "Unknown",
        "status": submission.status.value,
        "total_score": submission.total_score,
        "total_possible": submission.total_possible,
        "percentage": submission.percentage,
        "submitted_at": submission.submitted_at,
        "graded_at": submission.graded_at,
        "processing_time_seconds": submission.processing_time_seconds,
        "question_results": [
            {
                "question_number": qr.question_number,
                "question_type": qr.question_type.value,
                "points_earned": qr.points_earned,
                "points_possible": qr.points_possible,
                "feedback": qr.overall_feedback,
                "student_answer": qr.student_answer_text,
                "criterion_scores": json.loads(qr.criterion_scores) if qr.criterion_scores else []
            }
            for qr in question_results
        ]
    }


# ==================== API Endpoints - Analytics ====================

@app.get("/api/analytics/exam/{exam_id}")
async def get_exam_analytics(exam_id: int):
    """Get analytics for an exam"""
    stats = await db.get_exam_statistics(exam_id)
    return stats


# ==================== API Endpoints - Export ====================

@app.get("/api/export/csv/{exam_id}")
async def export_exam_to_csv(exam_id: int):
    """Export exam results to CSV"""
    # Get all submissions for exam
    submissions = await db.get_exam_submissions(exam_id)

    if not submissions:
        raise HTTPException(status_code=404, detail="No submissions found")

    # Build results list
    # (This is simplified - in production you'd build full SubmissionResult objects)

    # Generate CSV
    output_path = UPLOADS_DIR / f"exam_{exam_id}_results.csv"
    # results_exporter.export_to_csv(results, output_path)

    return FileResponse(output_path, media_type="text/csv", filename=output_path.name)


# ==================== Main ====================

if __name__ == "__main__":
    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
