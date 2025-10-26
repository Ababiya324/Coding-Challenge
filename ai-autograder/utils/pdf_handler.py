"""
PDF handling utilities for converting PDFs to images and extracting text
"""
import io
import base64
from pathlib import Path
from typing import List, Optional, Tuple
from PIL import Image
import PyPDF2

try:
    from pdf2image import convert_from_path
    PDF2IMAGE_AVAILABLE = True
except ImportError:
    PDF2IMAGE_AVAILABLE = False
    print("Warning: pdf2image not available. PDF to image conversion will be limited.")


class PDFHandler:
    """Handle PDF processing operations"""

    def __init__(self, dpi: int = 300, image_format: str = "png"):
        """
        Initialize PDF handler

        Args:
            dpi: DPI for image conversion (higher = better quality, larger file)
            image_format: Output format for images (png, jpg)
        """
        self.dpi = dpi
        self.image_format = image_format

    def convert_pdf_to_images(self, pdf_path: Path) -> List[Image.Image]:
        """
        Convert each PDF page to an image

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of PIL Image objects, one per page

        Raises:
            ValueError: If pdf2image is not available
            FileNotFoundError: If PDF file doesn't exist
        """
        if not PDF2IMAGE_AVAILABLE:
            raise ValueError(
                "pdf2image is not available. Please install: pip install pdf2image\n"
                "Also install poppler: https://github.com/oschwartz10612/poppler-windows/releases/"
            )

        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            images = convert_from_path(
                str(pdf_path),
                dpi=self.dpi,
                fmt=self.image_format
            )
            return images
        except Exception as e:
            raise RuntimeError(f"Failed to convert PDF to images: {str(e)}")

    def convert_pdf_to_base64_images(self, pdf_path: Path) -> List[str]:
        """
        Convert PDF pages to base64-encoded images for API transmission

        Args:
            pdf_path: Path to PDF file

        Returns:
            List of base64-encoded image strings
        """
        images = self.convert_pdf_to_images(pdf_path)
        base64_images = []

        for img in images:
            # Convert PIL Image to base64
            buffer = io.BytesIO()
            img.save(buffer, format=self.image_format.upper())
            img_bytes = buffer.getvalue()
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
            base64_images.append(img_base64)

        return base64_images

    def extract_text_from_pdf(self, pdf_path: Path) -> str:
        """
        Extract text directly from PDF (works for text-based PDFs, not scanned)

        Args:
            pdf_path: Path to PDF file

        Returns:
            Extracted text content

        Note:
            This is a fallback method for text-based PDFs. For scanned PDFs,
            use OCR or image-based extraction with Claude Vision.
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                text_parts = []

                for page_num, page in enumerate(reader.pages, 1):
                    page_text = page.extract_text()
                    if page_text.strip():
                        text_parts.append(f"=== Page {page_num} ===\n{page_text}\n")

                return "\n".join(text_parts)
        except Exception as e:
            raise RuntimeError(f"Failed to extract text from PDF: {str(e)}")

    def get_pdf_info(self, pdf_path: Path) -> dict:
        """
        Get metadata information about a PDF

        Args:
            pdf_path: Path to PDF file

        Returns:
            Dictionary with PDF information
        """
        if not pdf_path.exists():
            raise FileNotFoundError(f"PDF file not found: {pdf_path}")

        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)

                info = {
                    "num_pages": len(reader.pages),
                    "file_size_bytes": pdf_path.stat().st_size,
                    "file_size_mb": round(pdf_path.stat().st_size / (1024 * 1024), 2),
                }

                # Try to get metadata (may not always be available)
                if reader.metadata:
                    info.update({
                        "title": reader.metadata.get("/Title", "Unknown"),
                        "author": reader.metadata.get("/Author", "Unknown"),
                        "subject": reader.metadata.get("/Subject", ""),
                        "creator": reader.metadata.get("/Creator", ""),
                    })

                return info
        except Exception as e:
            raise RuntimeError(f"Failed to get PDF info: {str(e)}")

    def save_image_from_pdf(
        self,
        pdf_path: Path,
        page_number: int,
        output_path: Path
    ) -> Path:
        """
        Extract a specific page from PDF and save as image

        Args:
            pdf_path: Path to PDF file
            page_number: Page number (1-indexed)
            output_path: Where to save the image

        Returns:
            Path to saved image
        """
        images = self.convert_pdf_to_images(pdf_path)

        if page_number < 1 or page_number > len(images):
            raise ValueError(
                f"Page number {page_number} out of range (1-{len(images)})"
            )

        # Pages are 0-indexed in the list
        image = images[page_number - 1]
        image.save(output_path)

        return output_path

    def validate_pdf(self, pdf_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Validate if a file is a valid PDF

        Args:
            pdf_path: Path to PDF file

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not pdf_path.exists():
            return False, f"File not found: {pdf_path}"

        if pdf_path.suffix.lower() != '.pdf':
            return False, f"File is not a PDF: {pdf_path.suffix}"

        try:
            with open(pdf_path, 'rb') as file:
                reader = PyPDF2.PdfReader(file)
                num_pages = len(reader.pages)

                if num_pages == 0:
                    return False, "PDF has no pages"

            return True, None
        except Exception as e:
            return False, f"Invalid PDF: {str(e)}"


def create_pdf_handler(dpi: int = 300, image_format: str = "png") -> PDFHandler:
    """
    Factory function to create a PDFHandler instance

    Args:
        dpi: Resolution for image conversion
        image_format: Image format (png, jpg)

    Returns:
        PDFHandler instance
    """
    return PDFHandler(dpi=dpi, image_format=image_format)
