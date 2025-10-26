"""
Database operations for AI Autograder using SQLite
"""
import aiosqlite
import json
from typing import List, Optional, Dict, Any
from datetime import datetime
from pathlib import Path

from config import DATABASE_DIR
from models import (
    RubricDB, ExamDB, SubmissionDB, QuestionResultDB,
    GradeStatus, QuestionType, ExtractedRubric,
    SubmissionResult, QuestionResult
)


DATABASE_PATH = DATABASE_DIR / "autograder.db"


class Database:
    """Database manager for autograder"""

    def __init__(self, db_path: Path = DATABASE_PATH):
        self.db_path = str(db_path)

    async def init_db(self):
        """Initialize database schema"""
        async with aiosqlite.connect(self.db_path) as db:
            # Rubrics table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS rubrics (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    name TEXT NOT NULL,
                    pdf_path TEXT NOT NULL,
                    extracted_json TEXT NOT NULL,
                    upload_date TIMESTAMP NOT NULL,
                    uploaded_by TEXT,
                    total_points REAL NOT NULL
                )
            """)

            # Exams table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS exams (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    exam_name TEXT NOT NULL,
                    rubric_id INTEGER NOT NULL,
                    date_created TIMESTAMP NOT NULL,
                    answer_key_json TEXT,
                    FOREIGN KEY (rubric_id) REFERENCES rubrics(id)
                )
            """)

            # Submissions table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS submissions (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    student_id TEXT NOT NULL,
                    exam_id INTEGER NOT NULL,
                    status TEXT NOT NULL,
                    total_score REAL,
                    total_possible REAL,
                    percentage REAL,
                    submitted_at TIMESTAMP NOT NULL,
                    graded_at TIMESTAMP,
                    processing_time_seconds REAL,
                    FOREIGN KEY (exam_id) REFERENCES exams(id)
                )
            """)

            # Question results table
            await db.execute("""
                CREATE TABLE IF NOT EXISTS question_results (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    submission_id INTEGER NOT NULL,
                    question_number INTEGER NOT NULL,
                    question_type TEXT NOT NULL,
                    student_answer_text TEXT,
                    points_earned REAL NOT NULL,
                    points_possible REAL NOT NULL,
                    criterion_scores TEXT,
                    overall_feedback TEXT NOT NULL,
                    image_path TEXT,
                    FOREIGN KEY (submission_id) REFERENCES submissions(id)
                )
            """)

            # Create indexes for better query performance
            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_submissions_student
                ON submissions(student_id)
            """)

            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_submissions_exam
                ON submissions(exam_id)
            """)

            await db.execute("""
                CREATE INDEX IF NOT EXISTS idx_question_results_submission
                ON question_results(submission_id)
            """)

            await db.commit()

    # ==================== Rubric Operations ====================

    async def create_rubric(self, rubric: RubricDB) -> int:
        """Create a new rubric and return its ID"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                INSERT INTO rubrics (name, pdf_path, extracted_json, upload_date, uploaded_by, total_points)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (
                rubric.name,
                rubric.pdf_path,
                rubric.extracted_json,
                rubric.upload_date.isoformat(),
                rubric.uploaded_by,
                rubric.total_points
            ))
            await db.commit()
            return cursor.lastrowid

    async def get_rubric(self, rubric_id: int) -> Optional[RubricDB]:
        """Get rubric by ID"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM rubrics WHERE id = ?
            """, (rubric_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return RubricDB(
                        id=row['id'],
                        name=row['name'],
                        pdf_path=row['pdf_path'],
                        extracted_json=row['extracted_json'],
                        upload_date=datetime.fromisoformat(row['upload_date']),
                        uploaded_by=row['uploaded_by'],
                        total_points=row['total_points']
                    )
                return None

    async def list_rubrics(self) -> List[RubricDB]:
        """List all rubrics"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM rubrics ORDER BY upload_date DESC
            """) as cursor:
                rows = await cursor.fetchall()
                return [
                    RubricDB(
                        id=row['id'],
                        name=row['name'],
                        pdf_path=row['pdf_path'],
                        extracted_json=row['extracted_json'],
                        upload_date=datetime.fromisoformat(row['upload_date']),
                        uploaded_by=row['uploaded_by'],
                        total_points=row['total_points']
                    )
                    for row in rows
                ]

    async def update_rubric(self, rubric_id: int, extracted_json: str, total_points: float) -> bool:
        """Update rubric's extracted data"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE rubrics
                SET extracted_json = ?, total_points = ?
                WHERE id = ?
            """, (extracted_json, total_points, rubric_id))
            await db.commit()
            return True

    async def delete_rubric(self, rubric_id: int) -> bool:
        """Delete a rubric"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM rubrics WHERE id = ?", (rubric_id,))
            await db.commit()
            return True

    # ==================== Exam Operations ====================

    async def create_exam(self, exam: ExamDB) -> int:
        """Create a new exam and return its ID"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                INSERT INTO exams (exam_name, rubric_id, date_created, answer_key_json)
                VALUES (?, ?, ?, ?)
            """, (
                exam.exam_name,
                exam.rubric_id,
                exam.date_created.isoformat(),
                exam.answer_key_json
            ))
            await db.commit()
            return cursor.lastrowid

    async def get_exam(self, exam_id: int) -> Optional[ExamDB]:
        """Get exam by ID"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM exams WHERE id = ?
            """, (exam_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return ExamDB(
                        id=row['id'],
                        exam_name=row['exam_name'],
                        rubric_id=row['rubric_id'],
                        date_created=datetime.fromisoformat(row['date_created']),
                        answer_key_json=row['answer_key_json']
                    )
                return None

    async def list_exams(self) -> List[ExamDB]:
        """List all exams"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM exams ORDER BY date_created DESC
            """) as cursor:
                rows = await cursor.fetchall()
                return [
                    ExamDB(
                        id=row['id'],
                        exam_name=row['exam_name'],
                        rubric_id=row['rubric_id'],
                        date_created=datetime.fromisoformat(row['date_created']),
                        answer_key_json=row['answer_key_json']
                    )
                    for row in rows
                ]

    async def update_answer_key(self, exam_id: int, answer_key_json: str) -> bool:
        """Update exam's answer key"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE exams SET answer_key_json = ? WHERE id = ?
            """, (answer_key_json, exam_id))
            await db.commit()
            return True

    # ==================== Submission Operations ====================

    async def create_submission(self, submission: SubmissionDB) -> int:
        """Create a new submission and return its ID"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                INSERT INTO submissions (
                    student_id, exam_id, status, total_score, total_possible,
                    percentage, submitted_at, graded_at, processing_time_seconds
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                submission.student_id,
                submission.exam_id,
                submission.status.value,
                submission.total_score,
                submission.total_possible,
                submission.percentage,
                submission.submitted_at.isoformat(),
                submission.graded_at.isoformat() if submission.graded_at else None,
                submission.processing_time_seconds
            ))
            await db.commit()
            return cursor.lastrowid

    async def get_submission(self, submission_id: int) -> Optional[SubmissionDB]:
        """Get submission by ID"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM submissions WHERE id = ?
            """, (submission_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return SubmissionDB(
                        id=row['id'],
                        student_id=row['student_id'],
                        exam_id=row['exam_id'],
                        status=GradeStatus(row['status']),
                        total_score=row['total_score'],
                        total_possible=row['total_possible'],
                        percentage=row['percentage'],
                        submitted_at=datetime.fromisoformat(row['submitted_at']),
                        graded_at=datetime.fromisoformat(row['graded_at']) if row['graded_at'] else None,
                        processing_time_seconds=row['processing_time_seconds']
                    )
                return None

    async def update_submission(
        self,
        submission_id: int,
        status: GradeStatus,
        total_score: Optional[float] = None,
        total_possible: Optional[float] = None,
        percentage: Optional[float] = None,
        graded_at: Optional[datetime] = None,
        processing_time: Optional[float] = None
    ) -> bool:
        """Update submission status and scores"""
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                UPDATE submissions
                SET status = ?, total_score = ?, total_possible = ?,
                    percentage = ?, graded_at = ?, processing_time_seconds = ?
                WHERE id = ?
            """, (
                status.value,
                total_score,
                total_possible,
                percentage,
                graded_at.isoformat() if graded_at else None,
                processing_time,
                submission_id
            ))
            await db.commit()
            return True

    async def get_student_submissions(self, student_id: str) -> List[SubmissionDB]:
        """Get all submissions for a student"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM submissions WHERE student_id = ? ORDER BY submitted_at DESC
            """, (student_id,)) as cursor:
                rows = await cursor.fetchall()
                return [self._row_to_submission(row) for row in rows]

    async def get_exam_submissions(self, exam_id: int) -> List[SubmissionDB]:
        """Get all submissions for an exam"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM submissions WHERE exam_id = ? ORDER BY submitted_at DESC
            """, (exam_id,)) as cursor:
                rows = await cursor.fetchall()
                return [self._row_to_submission(row) for row in rows]

    def _row_to_submission(self, row) -> SubmissionDB:
        """Convert database row to SubmissionDB"""
        return SubmissionDB(
            id=row['id'],
            student_id=row['student_id'],
            exam_id=row['exam_id'],
            status=GradeStatus(row['status']),
            total_score=row['total_score'],
            total_possible=row['total_possible'],
            percentage=row['percentage'],
            submitted_at=datetime.fromisoformat(row['submitted_at']),
            graded_at=datetime.fromisoformat(row['graded_at']) if row['graded_at'] else None,
            processing_time_seconds=row['processing_time_seconds']
        )

    # ==================== Question Result Operations ====================

    async def create_question_result(self, result: QuestionResultDB) -> int:
        """Create a question result"""
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                INSERT INTO question_results (
                    submission_id, question_number, question_type, student_answer_text,
                    points_earned, points_possible, criterion_scores, overall_feedback, image_path
                )
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                result.submission_id,
                result.question_number,
                result.question_type.value,
                result.student_answer_text,
                result.points_earned,
                result.points_possible,
                result.criterion_scores,
                result.overall_feedback,
                result.image_path
            ))
            await db.commit()
            return cursor.lastrowid

    async def get_submission_results(self, submission_id: int) -> List[QuestionResultDB]:
        """Get all question results for a submission"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT * FROM question_results WHERE submission_id = ? ORDER BY question_number
            """, (submission_id,)) as cursor:
                rows = await cursor.fetchall()
                return [
                    QuestionResultDB(
                        id=row['id'],
                        submission_id=row['submission_id'],
                        question_number=row['question_number'],
                        question_type=QuestionType(row['question_type']),
                        student_answer_text=row['student_answer_text'],
                        points_earned=row['points_earned'],
                        points_possible=row['points_possible'],
                        criterion_scores=row['criterion_scores'],
                        overall_feedback=row['overall_feedback'],
                        image_path=row['image_path']
                    )
                    for row in rows
                ]

    # ==================== Analytics Operations ====================

    async def get_exam_statistics(self, exam_id: int) -> Dict[str, Any]:
        """Get statistics for an exam"""
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row

            # Get overall stats
            async with db.execute("""
                SELECT
                    COUNT(*) as num_submissions,
                    AVG(total_score) as avg_score,
                    MIN(total_score) as min_score,
                    MAX(total_score) as max_score
                FROM submissions
                WHERE exam_id = ? AND status = 'completed'
            """, (exam_id,)) as cursor:
                stats = await cursor.fetchone()

            # Get question-level stats
            async with db.execute("""
                SELECT
                    question_number,
                    AVG(points_earned) as avg_score,
                    MIN(points_earned) as min_score,
                    MAX(points_earned) as max_score,
                    COUNT(*) as num_answers
                FROM question_results
                WHERE submission_id IN (
                    SELECT id FROM submissions WHERE exam_id = ?
                )
                GROUP BY question_number
                ORDER BY question_number
            """, (exam_id,)) as cursor:
                question_stats = await cursor.fetchall()

            return {
                "exam_id": exam_id,
                "num_submissions": stats['num_submissions'],
                "avg_score": stats['avg_score'],
                "min_score": stats['min_score'],
                "max_score": stats['max_score'],
                "question_stats": [dict(row) for row in question_stats]
            }


# Global database instance
db = Database()
