"""
Free Response Grader - Grades essay-style answers using AI and PDF rubric
"""
import json
from pathlib import Path
from typing import Dict, Any, Optional, List

from config import FREE_RESPONSE_GRADING_PROMPT
from models import (
    FreeResponseGradeResult,
    RubricQuestion,
    CriterionEvaluation,
    QuestionType
)
from utils.claude_client import ClaudeClient


class FreeResponseGrader:
    """
    Grades free response questions using AI and professor's rubric from PDF
    """

    def __init__(self, claude_client: ClaudeClient):
        """
        Initialize free response grader

        Args:
            claude_client: Claude API client
        """
        self.claude = claude_client

    async def grade_with_rubric(
        self,
        student_image_path: Path,
        rubric_question: RubricQuestion
    ) -> FreeResponseGradeResult:
        """
        Grade a free response answer using the professor's rubric

        Args:
            student_image_path: Path to image of student's answer
            rubric_question: Question definition with grading criteria from rubric

        Returns:
            FreeResponseGradeResult with detailed grading
        """
        # Build grading prompt with rubric criteria
        prompt = self._build_grading_prompt(rubric_question)

        try:
            # Send to Claude for grading
            result = await self.claude.grade_free_response(
                student_image=student_image_path,
                prompt=prompt
            )

            # Parse and validate result
            grade_result = self._parse_grading_result(result, rubric_question)

            return grade_result

        except Exception as e:
            # Return error result
            return FreeResponseGradeResult(
                student_response_extracted=f"[Error: {str(e)}]",
                criterion_evaluations=[],
                total_score=0.0,
                total_possible=rubric_question.points_possible,
                percentage=0.0,
                overall_feedback=f"Error grading response: {str(e)}",
                strengths=[],
                areas_for_improvement=["Unable to grade due to error"]
            )

    def _build_grading_prompt(self, rubric_question: RubricQuestion) -> str:
        """
        Build a grading prompt using the rubric criteria

        Args:
            rubric_question: Question with grading criteria

        Returns:
            Formatted prompt for Claude
        """
        # Format rubric criteria
        criteria_text = self._format_criteria(rubric_question)

        # Build prompt
        prompt = FREE_RESPONSE_GRADING_PROMPT.format(
            question_description=rubric_question.description,
            points_possible=rubric_question.points_possible,
            rubric_criteria=criteria_text
        )

        return prompt

    def _format_criteria(self, rubric_question: RubricQuestion) -> str:
        """
        Format grading criteria into readable text

        Args:
            rubric_question: Question with criteria

        Returns:
            Formatted criteria text
        """
        if not rubric_question.grading_criteria:
            return f"""
No specific criteria provided. Grade based on:
- Technical accuracy
- Completeness of answer
- Clarity of explanation
- Correct use of terminology

Total Points: {rubric_question.points_possible}
"""

        lines = [
            f"Total Points for Question: {rubric_question.points_possible}",
            "",
            "Grading Criteria:"
        ]

        for i, criterion in enumerate(rubric_question.grading_criteria, 1):
            lines.append(f"\n{i}. {criterion.criterion} ({criterion.points} points)")
            lines.append(f"   Full Credit: {criterion.full_credit}")

            if criterion.partial_credit:
                lines.append(f"   Partial Credit: {criterion.partial_credit}")

            if criterion.no_credit:
                lines.append(f"   No Credit: {criterion.no_credit}")

        if rubric_question.special_notes:
            lines.append(f"\nSpecial Notes: {rubric_question.special_notes}")

        return "\n".join(lines)

    def _parse_grading_result(
        self,
        result: Dict[str, Any],
        rubric_question: RubricQuestion
    ) -> FreeResponseGradeResult:
        """
        Parse Claude's grading result and validate

        Args:
            result: Raw result dict from Claude
            rubric_question: Original question for validation

        Returns:
            Validated FreeResponseGradeResult
        """
        try:
            # Parse criterion evaluations
            criterion_evals = [
                CriterionEvaluation(**eval_data)
                for eval_data in result.get('criterion_evaluations', [])
            ]

            # Validate total score doesn't exceed maximum
            total_score = result.get('total_score', 0.0)
            total_possible = rubric_question.points_possible

            if total_score > total_possible:
                print(f"Warning: Total score ({total_score}) exceeds maximum ({total_possible}). Capping.")
                total_score = total_possible

            # Calculate percentage
            percentage = (total_score / total_possible * 100) if total_possible > 0 else 0

            # Create result
            return FreeResponseGradeResult(
                student_response_extracted=result.get('student_response_extracted', ''),
                criterion_evaluations=criterion_evals,
                total_score=total_score,
                total_possible=total_possible,
                percentage=percentage,
                overall_feedback=result.get('overall_feedback', ''),
                strengths=result.get('strengths', []),
                areas_for_improvement=result.get('areas_for_improvement', []),
                grade_letter=result.get('grade_letter')
            )

        except Exception as e:
            raise RuntimeError(f"Failed to parse grading result: {str(e)}")

    async def grade_without_rubric(
        self,
        student_image_path: Path,
        question_description: str,
        points_possible: float,
        expected_answer: Optional[str] = None
    ) -> FreeResponseGradeResult:
        """
        Grade a free response when no detailed rubric is available

        Args:
            student_image_path: Path to student answer image
            question_description: Question text
            points_possible: Maximum points
            expected_answer: Optional model answer

        Returns:
            FreeResponseGradeResult
        """
        # Build basic grading prompt
        prompt = f"""
Grade this free response answer.

QUESTION: {question_description}

POINTS POSSIBLE: {points_possible}

{"MODEL ANSWER: " + expected_answer if expected_answer else ""}

GRADING GUIDELINES:
- Technical accuracy (40%)
- Completeness (30%)
- Clarity and organization (20%)
- Use of correct terminology (10%)

STUDENT'S ANSWER: [See image]

Provide detailed grading in JSON format with:
- student_response_extracted: transcribed answer
- criterion_evaluations: array of evaluations for each aspect
- total_score: numeric score
- overall_feedback: constructive feedback
- strengths: what they did well
- areas_for_improvement: what to improve
"""

        try:
            result = await self.claude.grade_free_response(
                student_image=student_image_path,
                prompt=prompt
            )

            # Create basic rubric question for parsing
            from models import RubricQuestion, GradingCriterion

            basic_rubric = RubricQuestion(
                number=1,
                type=QuestionType.FREE_RESPONSE,
                points_possible=points_possible,
                description=question_description,
                grading_criteria=[]
            )

            return self._parse_grading_result(result, basic_rubric)

        except Exception as e:
            return FreeResponseGradeResult(
                student_response_extracted=f"[Error: {str(e)}]",
                criterion_evaluations=[],
                total_score=0.0,
                total_possible=points_possible,
                percentage=0.0,
                overall_feedback=f"Error grading response: {str(e)}",
                strengths=[],
                areas_for_improvement=[]
            )

    def calculate_grade_letter(self, percentage: float) -> str:
        """
        Convert percentage to letter grade

        Args:
            percentage: Score percentage

        Returns:
            Letter grade (A, B, C, D, F)
        """
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

    def format_feedback(self, result: FreeResponseGradeResult) -> str:
        """
        Format grading result into human-readable feedback

        Args:
            result: Grading result

        Returns:
            Formatted feedback text
        """
        lines = [
            f"=== Free Response Grading Results ===",
            f"",
            f"Score: {result.total_score}/{result.total_possible} ({result.percentage:.1f}%)",
            ""
        ]

        if result.grade_letter:
            lines.append(f"Grade: {result.grade_letter}")
            lines.append("")

        # Criterion breakdown
        if result.criterion_evaluations:
            lines.append("Criterion Breakdown:")
            for eval in result.criterion_evaluations:
                lines.append(
                    f"  • {eval.criterion_name}: {eval.points_earned}/{eval.points_possible} pts"
                )
                lines.append(f"    {eval.specific_feedback}")
            lines.append("")

        # Overall feedback
        lines.append("Overall Feedback:")
        lines.append(result.overall_feedback)
        lines.append("")

        # Strengths
        if result.strengths:
            lines.append("Strengths:")
            for strength in result.strengths:
                lines.append(f"  ✓ {strength}")
            lines.append("")

        # Areas for improvement
        if result.areas_for_improvement:
            lines.append("Areas for Improvement:")
            for area in result.areas_for_improvement:
                lines.append(f"  → {area}")
            lines.append("")

        return "\n".join(lines)


def create_free_response_grader(claude_client: ClaudeClient) -> FreeResponseGrader:
    """
    Factory function to create FreeResponseGrader

    Args:
        claude_client: Claude API client

    Returns:
        FreeResponseGrader instance
    """
    return FreeResponseGrader(claude_client=claude_client)
