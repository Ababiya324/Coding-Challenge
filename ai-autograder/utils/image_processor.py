"""
Image processing utilities for handling exam submission images
"""
import io
import base64
from pathlib import Path
from typing import Optional, Tuple
from PIL import Image


class ImageProcessor:
    """Process and optimize images for AI analysis"""

    def __init__(self, max_size: int = 5 * 1024 * 1024):
        """
        Initialize image processor

        Args:
            max_size: Maximum file size in bytes (default 5MB)
        """
        self.max_size = max_size

    def validate_image(self, image_path: Path) -> Tuple[bool, Optional[str]]:
        """
        Validate if a file is a valid image

        Args:
            image_path: Path to image file

        Returns:
            Tuple of (is_valid, error_message)
        """
        if not image_path.exists():
            return False, f"File not found: {image_path}"

        allowed_extensions = {'.jpg', '.jpeg', '.png', '.tiff', '.bmp', '.gif'}
        if image_path.suffix.lower() not in allowed_extensions:
            return False, f"Unsupported image format: {image_path.suffix}"

        try:
            with Image.open(image_path) as img:
                img.verify()
            return True, None
        except Exception as e:
            return False, f"Invalid image: {str(e)}"

    def load_image(self, image_path: Path) -> Image.Image:
        """
        Load an image file

        Args:
            image_path: Path to image file

        Returns:
            PIL Image object

        Raises:
            FileNotFoundError: If image doesn't exist
            ValueError: If image is invalid
        """
        is_valid, error = self.validate_image(image_path)
        if not is_valid:
            raise ValueError(error)

        return Image.open(image_path)

    def resize_if_needed(
        self,
        image: Image.Image,
        max_width: int = 2048,
        max_height: int = 2048
    ) -> Image.Image:
        """
        Resize image if it exceeds maximum dimensions

        Args:
            image: PIL Image object
            max_width: Maximum width in pixels
            max_height: Maximum height in pixels

        Returns:
            Resized image (or original if within limits)
        """
        width, height = image.size

        if width <= max_width and height <= max_height:
            return image

        # Calculate scaling factor
        scale = min(max_width / width, max_height / height)
        new_width = int(width * scale)
        new_height = int(height * scale)

        return image.resize((new_width, new_height), Image.Resampling.LANCZOS)

    def optimize_for_api(
        self,
        image_path: Path,
        max_width: int = 2048,
        max_height: int = 2048,
        quality: int = 85
    ) -> Image.Image:
        """
        Optimize image for API transmission (resize, compress)

        Args:
            image_path: Path to image file
            max_width: Maximum width in pixels
            max_height: Maximum height in pixels
            quality: JPEG quality (1-100)

        Returns:
            Optimized PIL Image
        """
        image = self.load_image(image_path)

        # Convert to RGB if necessary (for JPEG compatibility)
        if image.mode not in ('RGB', 'L'):
            image = image.convert('RGB')

        # Resize if needed
        image = self.resize_if_needed(image, max_width, max_height)

        return image

    def image_to_base64(self, image: Image.Image, format: str = "PNG") -> str:
        """
        Convert PIL Image to base64 string

        Args:
            image: PIL Image object
            format: Output format (PNG, JPEG)

        Returns:
            Base64-encoded image string
        """
        buffer = io.BytesIO()
        image.save(buffer, format=format)
        img_bytes = buffer.getvalue()
        return base64.b64encode(img_bytes).decode('utf-8')

    def file_to_base64(
        self,
        image_path: Path,
        optimize: bool = True,
        max_width: int = 2048,
        max_height: int = 2048
    ) -> str:
        """
        Convert image file to base64 string

        Args:
            image_path: Path to image file
            optimize: Whether to optimize the image
            max_width: Maximum width if optimizing
            max_height: Maximum height if optimizing

        Returns:
            Base64-encoded image string
        """
        if optimize:
            image = self.optimize_for_api(image_path, max_width, max_height)
        else:
            image = self.load_image(image_path)

        # Determine format from file extension
        format = "PNG"
        if image_path.suffix.lower() in {'.jpg', '.jpeg'}:
            format = "JPEG"

        return self.image_to_base64(image, format)

    def save_base64_image(self, base64_string: str, output_path: Path) -> Path:
        """
        Save a base64-encoded image to file

        Args:
            base64_string: Base64-encoded image
            output_path: Where to save the image

        Returns:
            Path to saved image
        """
        img_data = base64.b64decode(base64_string)
        image = Image.open(io.BytesIO(img_data))
        image.save(output_path)
        return output_path

    def get_image_info(self, image_path: Path) -> dict:
        """
        Get metadata about an image

        Args:
            image_path: Path to image file

        Returns:
            Dictionary with image information
        """
        image = self.load_image(image_path)

        return {
            "width": image.width,
            "height": image.height,
            "mode": image.mode,
            "format": image.format,
            "file_size_bytes": image_path.stat().st_size,
            "file_size_kb": round(image_path.stat().st_size / 1024, 2),
        }

    def enhance_contrast(self, image: Image.Image, factor: float = 1.5) -> Image.Image:
        """
        Enhance image contrast for better text recognition

        Args:
            image: PIL Image object
            factor: Contrast enhancement factor (1.0 = no change)

        Returns:
            Enhanced image
        """
        from PIL import ImageEnhance

        enhancer = ImageEnhance.Contrast(image)
        return enhancer.enhance(factor)

    def enhance_sharpness(self, image: Image.Image, factor: float = 2.0) -> Image.Image:
        """
        Enhance image sharpness for better text recognition

        Args:
            image: PIL Image object
            factor: Sharpness enhancement factor (1.0 = no change)

        Returns:
            Enhanced image
        """
        from PIL import ImageEnhance

        enhancer = ImageEnhance.Sharpness(image)
        return enhancer.enhance(factor)

    def preprocess_for_ocr(self, image_path: Path) -> Image.Image:
        """
        Preprocess image for optimal OCR/text extraction

        Args:
            image_path: Path to image file

        Returns:
            Preprocessed image
        """
        image = self.load_image(image_path)

        # Convert to grayscale
        if image.mode != 'L':
            image = image.convert('L')

        # Enhance contrast and sharpness
        image = self.enhance_contrast(image, factor=1.5)
        image = self.enhance_sharpness(image, factor=2.0)

        return image


def create_image_processor(max_size: int = 5 * 1024 * 1024) -> ImageProcessor:
    """
    Factory function to create an ImageProcessor instance

    Args:
        max_size: Maximum file size in bytes

    Returns:
        ImageProcessor instance
    """
    return ImageProcessor(max_size=max_size)
