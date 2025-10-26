"""
Code Tracing Grader - Executes code and compares with student's answer
"""
import io
import sys
import ast
import contextlib
from typing import Dict, Any, Optional, Tuple
from pathlib import Path
from difflib import SequenceMatcher

from config import CODE_TRACING_EXTRACTION_PROMPT, settings
from models import CodeTracingGradeResult, CodeTracingExtraction, QuestionType
from utils.claude_client import ClaudeClient


class CodeExecutionError(Exception):
    """Custom exception for code execution errors"""
    pass


class CodeTracerGrader:
    """
    Grades code tracing questions by:
    1. Extracting student's written answer from image
    2. Executing the code to get actual output
    3. Comparing student's answer with actual output
    """

    def __init__(self, claude_client: ClaudeClient):
        """
        Initialize code tracer grader

        Args:
            claude_client: Claude API client for answer extraction
        """
        self.claude = claude_client
        self.execution_timeout = settings.CODE_EXECUTION_TIMEOUT
        self.similarity_threshold = settings.SIMILARITY_THRESHOLD

    async def grade_code_tracing(
        self,
        code: str,
        student_image_path: Path,
        points_possible: float,
        question_description: str = ""
    ) -> CodeTracingGradeResult:
        """
        Grade a code tracing question

        Args:
            code: The code to trace/execute
            student_image_path: Path to image of student's answer
            points_possible: Maximum points for this question
            question_description: Optional question text

        Returns:
            CodeTracingGradeResult with grading details
        """
        # Step 1: Extract student's written answer from image
        try:
            extraction = await self._extract_student_answer(
                student_image_path,
                question_description
            )
            student_answer = extraction.extracted_answer.strip()
        except Exception as e:
            return CodeTracingGradeResult(
                student_answer="[Failed to extract]",
                expected_answer="",
                is_correct=False,
                points_earned=0.0,
                points_possible=points_possible,
                percentage=0.0,
                feedback=f"Error extracting student answer: {str(e)}",
                execution_error=str(e)
            )

        # Step 2: Execute the code to get expected output
        try:
            execution_result = self._execute_code(code)
            expected_output = execution_result['output'].strip()
            execution_error = execution_result.get('error')
        except Exception as e:
            return CodeTracingGradeResult(
                student_answer=student_answer,
                expected_answer="[Execution failed]",
                is_correct=False,
                points_earned=0.0,
                points_possible=points_possible,
                percentage=0.0,
                feedback=f"Error executing code: {str(e)}",
                execution_error=str(e)
            )

        # Step 3: Compare student answer with expected output
        is_correct, similarity, feedback = self._compare_answers(
            student_answer,
            expected_output
        )

        # Step 4: Calculate score
        if is_correct:
            points_earned = points_possible
        elif similarity >= 0.7:  # Partial credit for close answers
            points_earned = points_possible * 0.5
        else:
            points_earned = 0.0

        percentage = (points_earned / points_possible * 100) if points_possible > 0 else 0

        return CodeTracingGradeResult(
            student_answer=student_answer,
            expected_answer=expected_output,
            is_correct=is_correct,
            points_earned=points_earned,
            points_possible=points_possible,
            percentage=percentage,
            feedback=feedback,
            execution_output=expected_output,
            execution_error=execution_error
        )

    async def _extract_student_answer(
        self,
        image_path: Path,
        question_description: str
    ) -> CodeTracingExtraction:
        """
        Extract student's written answer from image using Claude Vision

        Args:
            image_path: Path to student answer image
            question_description: Question text

        Returns:
            CodeTracingExtraction with extracted answer
        """
        prompt = CODE_TRACING_EXTRACTION_PROMPT.format(
            question_description=question_description
        )

        try:
            result = await self.claude.extract_student_answer(
                image=image_path,
                prompt=prompt
            )
            return CodeTracingExtraction(**result)
        except Exception as e:
            raise RuntimeError(f"Failed to extract student answer: {str(e)}")

    def _execute_code(self, code: str) -> Dict[str, Any]:
        """
        Safely execute Python code and capture output

        Args:
            code: Python code to execute

        Returns:
            Dict with 'output' and optional 'error'

        Note:
            This is a basic sandbox. For production, consider using
            a more robust sandboxing solution.
        """
        # Validate code doesn't contain dangerous operations
        try:
            self._validate_code_safety(code)
        except ValueError as e:
            return {
                'output': '',
                'error': f"Code validation failed: {str(e)}"
            }

        # Capture stdout
        output_buffer = io.StringIO()
        error_message = None

        try:
            # Redirect stdout
            with contextlib.redirect_stdout(output_buffer):
                # Create restricted execution environment
                exec_globals = {
                    '__builtins__': {
                        'print': print,
                        'range': range,
                        'len': len,
                        'str': str,
                        'int': int,
                        'float': float,
                        'list': list,
                        'dict': dict,
                        'set': set,
                        'tuple': tuple,
                        'True': True,
                        'False': False,
                        'None': None,
                        'sum': sum,
                        'min': min,
                        'max': max,
                        'abs': abs,
                        'enumerate': enumerate,
                        'zip': zip,
                        'sorted': sorted,
                        'reversed': reversed,
                    }
                }

                # Execute the code
                exec(code, exec_globals)

        except Exception as e:
            error_message = f"{type(e).__name__}: {str(e)}"

        output = output_buffer.getvalue()

        return {
            'output': output,
            'error': error_message
        }

    def _validate_code_safety(self, code: str) -> None:
        """
        Basic validation to prevent dangerous code execution

        Args:
            code: Code to validate

        Raises:
            ValueError: If code contains forbidden operations
        """
        # List of forbidden keywords/modules
        forbidden = [
            'import os',
            'import sys',
            'import subprocess',
            'import shutil',
            '__import__',
            'eval',
            'exec',
            'compile',
            'open(',
            'file(',
            'input(',
            'raw_input(',
            'breakpoint(',
        ]

        code_lower = code.lower()
        for forbidden_item in forbidden:
            if forbidden_item.lower() in code_lower:
                raise ValueError(f"Forbidden operation: {forbidden_item}")

        # Try to parse as valid Python
        try:
            ast.parse(code)
        except SyntaxError as e:
            raise ValueError(f"Invalid Python syntax: {str(e)}")

    def _compare_answers(
        self,
        student_answer: str,
        expected_output: str
    ) -> Tuple[bool, float, str]:
        """
        Compare student's answer with expected output

        Args:
            student_answer: What student wrote
            expected_output: Actual code output

        Returns:
            Tuple of (is_correct, similarity_score, feedback)
        """
        # Normalize both answers
        student_normalized = self._normalize_output(student_answer)
        expected_normalized = self._normalize_output(expected_output)

        # Exact match
        if student_normalized == expected_normalized:
            return True, 1.0, "Correct! Your answer matches the expected output exactly."

        # Calculate similarity
        similarity = SequenceMatcher(None, student_normalized, expected_normalized).ratio()

        # Check if it's close enough
        if similarity >= self.similarity_threshold:
            return True, similarity, (
                f"Correct! Your answer is very close to the expected output "
                f"(similarity: {similarity:.1%})."
            )

        # Not close enough
        feedback_parts = [
            f"Incorrect. Your answer doesn't match the expected output.",
            f"\nYour answer:\n{student_answer}",
            f"\nExpected output:\n{expected_output}",
            f"\nSimilarity: {similarity:.1%}"
        ]

        # Provide hints about differences
        if len(student_normalized) != len(expected_normalized):
            feedback_parts.append(
                f"\nNote: Length difference (yours: {len(student_normalized)} chars, "
                f"expected: {len(expected_normalized)} chars)"
            )

        return False, similarity, "\n".join(feedback_parts)

    def _normalize_output(self, text: str) -> str:
        """
        Normalize output for comparison (remove extra whitespace, etc.)

        Args:
            text: Text to normalize

        Returns:
            Normalized text
        """
        # Split into lines
        lines = text.split('\n')

        # Strip whitespace from each line
        lines = [line.strip() for line in lines]

        # Remove empty lines
        lines = [line for line in lines if line]

        # Join back
        return '\n'.join(lines)

    def grade_with_expected_output(
        self,
        expected_output: str,
        student_answer: str,
        points_possible: float
    ) -> CodeTracingGradeResult:
        """
        Grade when you already know the expected output (no execution needed)

        Args:
            expected_output: The correct answer
            student_answer: Student's extracted answer
            points_possible: Maximum points

        Returns:
            CodeTracingGradeResult
        """
        is_correct, similarity, feedback = self._compare_answers(
            student_answer,
            expected_output
        )

        if is_correct:
            points_earned = points_possible
        elif similarity >= 0.7:
            points_earned = points_possible * 0.5
        else:
            points_earned = 0.0

        percentage = (points_earned / points_possible * 100) if points_possible > 0 else 0

        return CodeTracingGradeResult(
            student_answer=student_answer,
            expected_answer=expected_output,
            is_correct=is_correct,
            points_earned=points_earned,
            points_possible=points_possible,
            percentage=percentage,
            feedback=feedback,
            execution_output=expected_output
        )


def create_code_tracer_grader(claude_client: ClaudeClient) -> CodeTracerGrader:
    """
    Factory function to create CodeTracerGrader

    Args:
        claude_client: Claude API client

    Returns:
        CodeTracerGrader instance
    """
    return CodeTracerGrader(claude_client=claude_client)
