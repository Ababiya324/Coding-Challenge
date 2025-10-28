"""
Gemini API client wrapper for interacting with Google's Generative AI
"""
import json
import base64
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
import google.generativeai as genai
from PIL import Image

from config import settings


class GeminiClient:
    """Wrapper for Gemini API operations"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini client

        Args:
            api_key: Google API key (uses settings if not provided)
        """
        self.api_key = api_key or settings.GEMINI_API_KEY
        genai.configure(api_key=self.api_key)
        self.model_name = settings.GEMINI_MODEL
        self.max_tokens = settings.GEMINI_MAX_TOKENS
        self.temperature = settings.GEMINI_TEMPERATURE

        # Initialize model
        self.model = genai.GenerativeModel(self.model_name)

    def _prepare_image_content(
        self,
        image_source: Union[str, Path, Image.Image]
    ) -> Image.Image:
        """
        Prepare image for Gemini API

        Args:
            image_source: Path to image, base64 string, or PIL Image

        Returns:
            PIL Image object
        """
        # Handle PIL Image
        if isinstance(image_source, Image.Image):
            return image_source

        # Handle file path
        elif isinstance(image_source, (str, Path)):
            image_path = Path(image_source)
            if image_path.exists():
                return Image.open(image_path)
            else:
                # Might be base64 string
                try:
                    img_data = base64.b64decode(image_source)
                    import io
                    return Image.open(io.BytesIO(img_data))
                except:
                    raise ValueError(f"Invalid image source: {image_source}")
        else:
            raise ValueError(f"Unsupported image source type: {type(image_source)}")

    async def send_message(
        self,
        prompt: str,
        images: Optional[List[Union[str, Path, Image.Image]]] = None,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Send a message to Gemini with optional images

        Args:
            prompt: Text prompt
            images: Optional list of images (paths, base64, or PIL Images)
            system_prompt: Optional system prompt (prepended to user prompt)
            max_tokens: Max tokens (uses default if not specified)
            temperature: Temperature (uses default if not specified)

        Returns:
            Gemini's response text
        """
        # Combine system prompt with user prompt if provided
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        else:
            full_prompt = prompt

        # Build content list
        content = []

        # Add images first if provided
        if images:
            for img in images:
                pil_image = self._prepare_image_content(img)
                content.append(pil_image)

        # Add text prompt
        content.append(full_prompt)

        # Configure generation
        generation_config = genai.GenerationConfig(
            max_output_tokens=max_tokens or self.max_tokens,
            temperature=temperature if temperature is not None else self.temperature,
        )

        try:
            # Generate response
            response = self.model.generate_content(
                content,
                generation_config=generation_config
            )

            return response.text

        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")

    def send_message_sync(
        self,
        prompt: str,
        images: Optional[List[Union[str, Path, Image.Image]]] = None,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Synchronous version of send_message
        (Gemini SDK is synchronous by default)

        Args:
            prompt: Text prompt
            images: Optional list of images
            system_prompt: Optional system prompt
            max_tokens: Max tokens
            temperature: Temperature

        Returns:
            Gemini's response text
        """
        # Combine system prompt with user prompt if provided
        if system_prompt:
            full_prompt = f"{system_prompt}\n\n{prompt}"
        else:
            full_prompt = prompt

        # Build content list
        content = []

        # Add images first if provided
        if images:
            for img in images:
                pil_image = self._prepare_image_content(img)
                content.append(pil_image)

        # Add text prompt
        content.append(full_prompt)

        # Configure generation
        generation_config = genai.GenerationConfig(
            max_output_tokens=max_tokens or self.max_tokens,
            temperature=temperature if temperature is not None else self.temperature,
        )

        try:
            # Generate response
            response = self.model.generate_content(
                content,
                generation_config=generation_config
            )

            return response.text

        except Exception as e:
            raise RuntimeError(f"Gemini API error: {str(e)}")

    async def extract_json_response(
        self,
        prompt: str,
        images: Optional[List[Union[str, Path, Image.Image]]] = None,
        system_prompt: Optional[str] = None
    ) -> dict:
        """
        Send message and parse JSON response

        Args:
            prompt: Text prompt (should request JSON format)
            images: Optional images
            system_prompt: Optional system prompt

        Returns:
            Parsed JSON response

        Raises:
            json.JSONDecodeError: If response is not valid JSON
        """
        response_text = await self.send_message(
            prompt=prompt,
            images=images,
            system_prompt=system_prompt
        )

        # Try to extract JSON from response
        # Gemini sometimes wraps JSON in markdown code blocks
        if "```json" in response_text:
            # Extract JSON from code block
            start = response_text.find("```json") + 7
            end = response_text.find("```", start)
            json_text = response_text[start:end].strip()
        elif "```" in response_text:
            # Generic code block
            start = response_text.find("```") + 3
            end = response_text.find("```", start)
            json_text = response_text[start:end].strip()
        else:
            json_text = response_text.strip()

        return json.loads(json_text)

    async def extract_rubric_from_image(
        self,
        image: Union[str, Path, Image.Image],
        prompt: str
    ) -> dict:
        """
        Extract rubric data from a PDF page image

        Args:
            image: PDF page image
            prompt: Extraction prompt

        Returns:
            Extracted rubric data as dict
        """
        return await self.extract_json_response(
            prompt=prompt,
            images=[image]
        )

    async def grade_free_response(
        self,
        student_image: Union[str, Path, Image.Image],
        prompt: str
    ) -> dict:
        """
        Grade a free response answer using rubric

        Args:
            student_image: Image of student's answer
            prompt: Grading prompt with rubric

        Returns:
            Grading result as dict
        """
        return await self.extract_json_response(
            prompt=prompt,
            images=[student_image]
        )

    async def extract_student_answer(
        self,
        image: Union[str, Path, Image.Image],
        prompt: str
    ) -> dict:
        """
        Extract student's written answer from image

        Args:
            image: Image of student's answer
            prompt: Extraction prompt

        Returns:
            Extracted answer data as dict
        """
        return await self.extract_json_response(
            prompt=prompt,
            images=[image]
        )

    async def analyze_batch(
        self,
        prompts_and_images: List[tuple[str, Optional[List[Union[str, Path, Image.Image]]]]],
        max_concurrent: int = 5
    ) -> List[str]:
        """
        Process multiple prompts concurrently (with rate limiting)

        Args:
            prompts_and_images: List of (prompt, images) tuples
            max_concurrent: Maximum concurrent requests

        Returns:
            List of responses in same order as inputs
        """
        import asyncio

        semaphore = asyncio.Semaphore(max_concurrent)

        async def process_one(prompt: str, images: Optional[List]) -> str:
            async with semaphore:
                return await self.send_message(prompt=prompt, images=images)

        tasks = [
            process_one(prompt, images)
            for prompt, images in prompts_and_images
        ]

        return await asyncio.gather(*tasks)


# Factory function - keeping same name for compatibility
def create_claude_client(api_key: Optional[str] = None) -> GeminiClient:
    """
    Create a GeminiClient instance (named for backward compatibility)

    Args:
        api_key: Optional API key (uses settings if not provided)

    Returns:
        GeminiClient instance
    """
    return GeminiClient(api_key=api_key)


# Alias for clarity
def create_gemini_client(api_key: Optional[str] = None) -> GeminiClient:
    """
    Create a GeminiClient instance

    Args:
        api_key: Optional API key (uses settings if not provided)

    Returns:
        GeminiClient instance
    """
    return GeminiClient(api_key=api_key)
