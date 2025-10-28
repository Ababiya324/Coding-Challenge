"""
PDF Rubric Parser - Extracts grading criteria from professor's PDF rubrics
"""
import json
from pathlib import Path
from typing import List, Dict, Any, Optional
from PIL import Image

from config import RUBRIC_EXTRACTION_PROMPT
from models import ExtractedRubric, ExamMetadata, RubricQuestion
from utils.pdf_handler import PDFHandler
from utils.gemini_client import GeminiClient


class RubricParser:
    """
    Extracts and structures grading criteria from PDF rubrics using Gemini Vision
    """

    def __init__(self, gemini_client: GeminiClient, pdf_handler: PDFHandler):
        """
        Initialize rubric parser

        Args:
            gemini_client: Gemini API client
            pdf_handler: PDF processing handler
        """
        self.gemini = gemini_client
        self.pdf_handler = pdf_handler

    async def parse_rubric_pdf(
        self,
        pdf_path: Path,
        rubric_name: Optional[str] = None
    ) -> ExtractedRubric:
        """
        Parse a PDF rubric and extract all grading criteria

        Args:
            pdf_path: Path to PDF rubric file
            rubric_name: Optional name for the rubric

        Returns:
            ExtractedRubric object with structured data

        Raises:
            ValueError: If PDF is invalid
            RuntimeError: If extraction fails
        """
        # Validate PDF
        is_valid, error = self.pdf_handler.validate_pdf(pdf_path)
        if not is_valid:
            raise ValueError(f"Invalid PDF: {error}")

        # Get PDF info
        pdf_info = self.pdf_handler.get_pdf_info(pdf_path)
        num_pages = pdf_info['num_pages']

        print(f"Processing rubric PDF: {pdf_path.name}")
        print(f"  Pages: {num_pages}")

        # Convert PDF to images
        try:
            images = self.pdf_handler.convert_pdf_to_images(pdf_path)
        except Exception as e:
            raise RuntimeError(f"Failed to convert PDF to images: {str(e)}")

        # Extract data from each page
        page_extractions = []
        for page_num, image in enumerate(images, 1):
            print(f"  Extracting page {page_num}/{num_pages}...")

            try:
                page_data = await self._extract_page(image, page_num)
                page_extractions.append(page_data)
            except Exception as e:
                print(f"    Warning: Failed to extract page {page_num}: {str(e)}")
                continue

        # Combine multi-page extractions
        combined_rubric = self._combine_pages(page_extractions, rubric_name)

        print(f"  ✓ Extraction complete: {len(combined_rubric.questions)} questions found")

        return combined_rubric

    async def _extract_page(self, image: Image.Image, page_number: int) -> dict:
        """
        Extract rubric data from a single PDF page

        Args:
            image: PIL Image of the page
            page_number: Page number

        Returns:
            Extracted data for this page
        """
        prompt = RUBRIC_EXTRACTION_PROMPT

        try:
            result = await self.gemini.extract_rubric_from_image(
                image=image,
                prompt=prompt
            )
            return result
        except json.JSONDecodeError as e:
            raise RuntimeError(f"Failed to parse JSON from Gemini response: {str(e)}")
        except Exception as e:
            raise RuntimeError(f"Failed to extract rubric from page: {str(e)}")

    def _combine_pages(
        self,
        page_extractions: List[dict],
        rubric_name: Optional[str] = None
    ) -> ExtractedRubric:
        """
        Combine extractions from multiple pages into a single rubric

        Args:
            page_extractions: List of extraction results from each page
            rubric_name: Optional name override

        Returns:
            Combined ExtractedRubric
        """
        if not page_extractions:
            raise ValueError("No pages were successfully extracted")

        # Use first page's metadata as base
        first_page = page_extractions[0]
        metadata = first_page.get('exam_metadata', {})

        # Override name if provided
        if rubric_name:
            metadata['title'] = rubric_name

        # Collect all questions from all pages
        all_questions = []
        for page_data in page_extractions:
            questions = page_data.get('questions', [])
            all_questions.extend(questions)

        # Remove duplicate questions (by question number)
        seen_numbers = set()
        unique_questions = []
        for q in all_questions:
            q_num = q.get('number')
            if q_num and q_num not in seen_numbers:
                seen_numbers.add(q_num)
                unique_questions.append(q)

        # Sort by question number
        unique_questions.sort(key=lambda q: q.get('number', 0))

        # Calculate total points
        total_points = sum(q.get('points_possible', 0) for q in unique_questions)

        # Override total_points in metadata if calculated
        if total_points > 0:
            metadata['total_points'] = total_points

        # Create structured objects
        try:
            exam_metadata = ExamMetadata(**metadata)
            rubric_questions = [RubricQuestion(**q) for q in unique_questions]

            return ExtractedRubric(
                exam_metadata=exam_metadata,
                questions=rubric_questions
            )
        except Exception as e:
            raise RuntimeError(f"Failed to create structured rubric: {str(e)}")

    def save_rubric_json(self, rubric: ExtractedRubric, output_path: Path) -> Path:
        """
        Save extracted rubric as JSON file

        Args:
            rubric: Extracted rubric
            output_path: Where to save JSON

        Returns:
            Path to saved file
        """
        # Convert to dict
        rubric_dict = rubric.model_dump()

        # Save as pretty-printed JSON
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(rubric_dict, f, indent=2, ensure_ascii=False)

        return output_path

    def load_rubric_json(self, json_path: Path) -> ExtractedRubric:
        """
        Load rubric from JSON file

        Args:
            json_path: Path to JSON file

        Returns:
            ExtractedRubric object
        """
        with open(json_path, 'r', encoding='utf-8') as f:
            data = json.load(f)

        return ExtractedRubric(**data)

    async def validate_and_fix_rubric(
        self,
        rubric: ExtractedRubric,
        pdf_path: Optional[Path] = None
    ) -> ExtractedRubric:
        """
        Validate rubric and attempt to fix common issues

        Args:
            rubric: Extracted rubric
            pdf_path: Optional path to original PDF for re-extraction

        Returns:
            Validated/fixed rubric
        """
        issues = []

        # Check for missing critical fields
        if not rubric.exam_metadata.title:
            issues.append("Missing exam title")

        if rubric.exam_metadata.total_points <= 0:
            issues.append("Total points is zero or negative")

        if not rubric.questions:
            issues.append("No questions found")

        # Check question numbering
        numbers = [q.number for q in rubric.questions]
        if len(numbers) != len(set(numbers)):
            issues.append("Duplicate question numbers found")

        # Check for questions without grading criteria
        for q in rubric.questions:
            if q.type.value == "free_response" and not q.grading_criteria:
                issues.append(f"Question {q.number} has no grading criteria")

        if issues:
            print(f"⚠ Rubric validation found {len(issues)} issue(s):")
            for issue in issues:
                print(f"    - {issue}")

        return rubric

    def get_question_by_number(
        self,
        rubric: ExtractedRubric,
        question_number: int
    ) -> Optional[RubricQuestion]:
        """
        Get a specific question from rubric

        Args:
            rubric: Extracted rubric
            question_number: Question number to find

        Returns:
            RubricQuestion or None if not found
        """
        for question in rubric.questions:
            if question.number == question_number:
                return question
        return None

    def get_rubric_summary(self, rubric: ExtractedRubric) -> str:
        """
        Generate a human-readable summary of the rubric

        Args:
            rubric: Extracted rubric

        Returns:
            Formatted summary string
        """
        lines = [
            f"=== {rubric.exam_metadata.title} ===",
            f"Total Points: {rubric.exam_metadata.total_points}",
            f"Number of Questions: {len(rubric.questions)}",
            ""
        ]

        for q in rubric.questions:
            lines.append(f"Question {q.number} ({q.type.value}) - {q.points_possible} pts")
            if q.grading_criteria:
                lines.append(f"  Criteria: {len(q.grading_criteria)} dimensions")
                for criterion in q.grading_criteria:
                    lines.append(f"    - {criterion.criterion}: {criterion.points} pts")
            lines.append("")

        return "\n".join(lines)


def create_rubric_parser(
    gemini_client: GeminiClient,
    pdf_handler: PDFHandler
) -> RubricParser:
    """
    Factory function to create a RubricParser

    Args:
        gemini_client: Gemini API client
        pdf_handler: PDF handler

    Returns:
        RubricParser instance
    """
    return RubricParser(gemini_client=gemini_client, pdf_handler=pdf_handler)
