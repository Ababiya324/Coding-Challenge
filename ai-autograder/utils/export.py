"""
Export utilities for generating CSV/Excel reports
"""
import csv
from pathlib import Path
from typing import List, Dict, Any
import pandas as pd
from datetime import datetime

from models import SubmissionResult, QuestionResult


class ResultsExporter:
    """Export grading results to various formats"""

    def __init__(self):
        """Initialize exporter"""
        pass

    def export_to_csv(
        self,
        results: List[SubmissionResult],
        output_path: Path,
        include_feedback: bool = True
    ) -> Path:
        """
        Export results to CSV file

        Args:
            results: List of submission results
            output_path: Where to save CSV
            include_feedback: Whether to include detailed feedback

        Returns:
            Path to saved CSV file
        """
        if not results:
            raise ValueError("No results to export")

        rows = []
        for result in results:
            base_row = {
                'Student ID': result.student_id,
                'Exam': result.exam_name,
                'Total Score': result.total_score,
                'Total Possible': result.total_possible,
                'Percentage': f"{result.percentage:.2f}%",
                'Grade': result.grade_letter or '',
                'Submitted At': result.submitted_at.strftime('%Y-%m-%d %H:%M:%S'),
                'Processing Time (s)': result.processing_time_seconds or 0
            }

            # Add question scores
            for q_result in result.question_results:
                q_num = q_result.question_number
                base_row[f'Q{q_num} Score'] = q_result.points_earned
                base_row[f'Q{q_num} Possible'] = q_result.points_possible
                base_row[f'Q{q_num} %'] = f"{q_result.percentage:.1f}%"

                if include_feedback:
                    base_row[f'Q{q_num} Feedback'] = q_result.feedback

            rows.append(base_row)

        # Write CSV
        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if rows:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

        return output_path

    def export_to_excel(
        self,
        results: List[SubmissionResult],
        output_path: Path
    ) -> Path:
        """
        Export results to Excel file with multiple sheets

        Args:
            results: List of submission results
            output_path: Where to save Excel file

        Returns:
            Path to saved Excel file
        """
        if not results:
            raise ValueError("No results to export")

        with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
            # Summary sheet
            summary_data = []
            for result in results:
                summary_data.append({
                    'Student ID': result.student_id,
                    'Total Score': result.total_score,
                    'Total Possible': result.total_possible,
                    'Percentage': result.percentage,
                    'Grade': result.grade_letter or '',
                    'Submitted': result.submitted_at,
                })

            summary_df = pd.DataFrame(summary_data)
            summary_df.to_excel(writer, sheet_name='Summary', index=False)

            # Question-by-question sheet
            question_data = []
            for result in results:
                for q_result in result.question_results:
                    question_data.append({
                        'Student ID': result.student_id,
                        'Question': q_result.question_number,
                        'Type': q_result.question_type.value,
                        'Score': q_result.points_earned,
                        'Possible': q_result.points_possible,
                        'Percentage': q_result.percentage,
                        'Feedback': q_result.feedback
                    })

            if question_data:
                question_df = pd.DataFrame(question_data)
                question_df.to_excel(writer, sheet_name='By Question', index=False)

            # Statistics sheet
            stats_data = self._calculate_statistics(results)
            if stats_data:
                stats_df = pd.DataFrame(stats_data)
                stats_df.to_excel(writer, sheet_name='Statistics', index=False)

        return output_path

    def _calculate_statistics(self, results: List[SubmissionResult]) -> List[Dict[str, Any]]:
        """
        Calculate statistics from results

        Args:
            results: List of submission results

        Returns:
            List of statistics dictionaries
        """
        if not results:
            return []

        stats = []

        # Overall statistics
        scores = [r.total_score for r in results]
        percentages = [r.percentage for r in results]

        stats.append({
            'Metric': 'Overall Average',
            'Value': f"{sum(percentages) / len(percentages):.2f}%"
        })

        stats.append({
            'Metric': 'Median Score',
            'Value': f"{sorted(percentages)[len(percentages) // 2]:.2f}%"
        })

        stats.append({
            'Metric': 'Highest Score',
            'Value': f"{max(percentages):.2f}%"
        })

        stats.append({
            'Metric': 'Lowest Score',
            'Value': f"{min(percentages):.2f}%"
        })

        # Grade distribution
        grade_counts = {}
        for result in results:
            grade = result.grade_letter or 'N/A'
            grade_counts[grade] = grade_counts.get(grade, 0) + 1

        for grade, count in sorted(grade_counts.items()):
            stats.append({
                'Metric': f'Grade {grade} Count',
                'Value': count
            })

        return stats

    def export_detailed_feedback(
        self,
        result: SubmissionResult,
        output_path: Path
    ) -> Path:
        """
        Export detailed feedback for a single submission to text file

        Args:
            result: Submission result
            output_path: Where to save feedback file

        Returns:
            Path to saved file
        """
        lines = [
            f"{'='*60}",
            f"GRADING FEEDBACK",
            f"{'='*60}",
            f"",
            f"Student ID: {result.student_id}",
            f"Exam: {result.exam_name}",
            f"Submitted: {result.submitted_at.strftime('%Y-%m-%d %H:%M:%S')}",
            f"",
            f"{'='*60}",
            f"OVERALL RESULTS",
            f"{'='*60}",
            f"Total Score: {result.total_score}/{result.total_possible}",
            f"Percentage: {result.percentage:.2f}%",
            f"Grade: {result.grade_letter or 'N/A'}",
            f"",
        ]

        # Question-by-question feedback
        lines.extend([
            f"{'='*60}",
            f"QUESTION-BY-QUESTION BREAKDOWN",
            f"{'='*60}",
            f""
        ])

        for q_result in result.question_results:
            lines.extend([
                f"Question {q_result.question_number} ({q_result.question_type.value})",
                f"{'-'*60}",
                f"Score: {q_result.points_earned}/{q_result.points_possible} ({q_result.percentage:.1f}%)",
                f"",
                f"Feedback:",
                q_result.feedback,
                f""
            ])

            # Include criterion breakdown for free response
            if q_result.criterion_scores:
                lines.append("Criterion Breakdown:")
                for criterion in q_result.criterion_scores:
                    lines.append(
                        f"  • {criterion.criterion_name}: "
                        f"{criterion.points_earned}/{criterion.points_possible} pts"
                    )
                    lines.append(f"    {criterion.specific_feedback}")
                lines.append("")

            lines.append("")

        # Write to file
        with open(output_path, 'w', encoding='utf-8') as f:
            f.write('\n'.join(lines))

        return output_path

    def create_gradebook_csv(
        self,
        results: List[SubmissionResult],
        output_path: Path
    ) -> Path:
        """
        Create a simple gradebook-style CSV (compatible with LMS import)

        Args:
            results: List of submission results
            output_path: Where to save CSV

        Returns:
            Path to saved CSV
        """
        rows = []
        for result in results:
            rows.append({
                'Student ID': result.student_id,
                'Score': result.total_score,
                'Points Possible': result.total_possible,
                'Percentage': result.percentage,
                'Grade': result.grade_letter or '',
                'Submitted': result.submitted_at.strftime('%Y-%m-%d %H:%M:%S')
            })

        with open(output_path, 'w', newline='', encoding='utf-8') as f:
            if rows:
                writer = csv.DictWriter(f, fieldnames=rows[0].keys())
                writer.writeheader()
                writer.writerows(rows)

        return output_path


def create_results_exporter() -> ResultsExporter:
    """
    Factory function to create ResultsExporter

    Returns:
        ResultsExporter instance
    """
    return ResultsExporter()
