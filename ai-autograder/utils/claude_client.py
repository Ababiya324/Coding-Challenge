"""
Claude API client wrapper for interacting with Anthropic's API
"""
import json
import base64
from pathlib import Path
from typing import List, Dict, Any, Optional, Union
from anthropic import Anthropic, AsyncAnthropic
from PIL import Image

from config import settings


class ClaudeClient:
    """Wrapper for Claude API operations"""

    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Claude client

        Args:
            api_key: Anthropic API key (uses settings if not provided)
        """
        self.api_key = api_key or settings.ANTHROPIC_API_KEY
        self.client = Anthropic(api_key=self.api_key)
        self.async_client = AsyncAnthropic(api_key=self.api_key)
        self.model = settings.CLAUDE_MODEL
        self.max_tokens = settings.CLAUDE_MAX_TOKENS
        self.temperature = settings.CLAUDE_TEMPERATURE

    def _prepare_image_content(
        self,
        image_source: Union[str, Path, Image.Image],
        media_type: str = "image/png"
    ) -> dict:
        """
        Prepare image content for Claude API

        Args:
            image_source: Path to image, base64 string, or PIL Image
            media_type: MIME type of the image

        Returns:
            Image content dict for Claude API
        """
        # Handle PIL Image
        if isinstance(image_source, Image.Image):
            import io
            buffer = io.BytesIO()
            image_source.save(buffer, format="PNG")
            image_data = base64.b64encode(buffer.getvalue()).decode('utf-8')

        # Handle file path
        elif isinstance(image_source, (str, Path)) and Path(image_source).exists():
            image_path = Path(image_source)
            with open(image_path, 'rb') as f:
                image_data = base64.b64encode(f.read()).decode('utf-8')

            # Determine media type from extension
            ext_to_mime = {
                '.png': 'image/png',
                '.jpg': 'image/jpeg',
                '.jpeg': 'image/jpeg',
                '.gif': 'image/gif',
                '.webp': 'image/webp'
            }
            media_type = ext_to_mime.get(image_path.suffix.lower(), 'image/png')

        # Handle base64 string
        elif isinstance(image_source, str):
            image_data = image_source
        else:
            raise ValueError(f"Unsupported image source type: {type(image_source)}")

        return {
            "type": "image",
            "source": {
                "type": "base64",
                "media_type": media_type,
                "data": image_data
            }
        }

    async def send_message(
        self,
        prompt: str,
        images: Optional[List[Union[str, Path, Image.Image]]] = None,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Send a message to Claude with optional images

        Args:
            prompt: Text prompt
            images: Optional list of images (paths, base64, or PIL Images)
            system_prompt: Optional system prompt
            max_tokens: Max tokens (uses default if not specified)
            temperature: Temperature (uses default if not specified)

        Returns:
            Claude's response text
        """
        # Build message content
        content = []

        # Add images first if provided
        if images:
            for img in images:
                content.append(self._prepare_image_content(img))

        # Add text prompt
        content.append({
            "type": "text",
            "text": prompt
        })

        # Prepare API call parameters
        params = {
            "model": self.model,
            "max_tokens": max_tokens or self.max_tokens,
            "temperature": temperature if temperature is not None else self.temperature,
            "messages": [{"role": "user", "content": content}]
        }

        if system_prompt:
            params["system"] = system_prompt

        # Make API call
        response = await self.async_client.messages.create(**params)

        # Extract text from response
        return response.content[0].text

    async def send_message_sync(
        self,
        prompt: str,
        images: Optional[List[Union[str, Path, Image.Image]]] = None,
        system_prompt: Optional[str] = None,
        max_tokens: Optional[int] = None,
        temperature: Optional[float] = None
    ) -> str:
        """
        Synchronous version of send_message

        Args:
            prompt: Text prompt
            images: Optional list of images
            system_prompt: Optional system prompt
            max_tokens: Max tokens
            temperature: Temperature

        Returns:
            Claude's response text
        """
        # Build message content
        content = []

        # Add images first if provided
        if images:
            for img in images:
                content.append(self._prepare_image_content(img))

        # Add text prompt
        content.append({
            "type": "text",
            "text": prompt
        })

        # Prepare API call parameters
        params = {
            "model": self.model,
            "max_tokens": max_tokens or self.max_tokens,
            "temperature": temperature if temperature is not None else self.temperature,
            "messages": [{"role": "user", "content": content}]
        }

        if system_prompt:
            params["system"] = system_prompt

        # Make API call
        response = self.client.messages.create(**params)

        # Extract text from response
        return response.content[0].text

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
        # Claude sometimes wraps JSON in markdown code blocks
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


# Factory function
def create_claude_client(api_key: Optional[str] = None) -> ClaudeClient:
    """
    Create a ClaudeClient instance

    Args:
        api_key: Optional API key (uses settings if not provided)

    Returns:
        ClaudeClient instance
    """
    return ClaudeClient(api_key=api_key)
