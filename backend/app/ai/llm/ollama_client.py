"""
Async HTTP client for Ollama LLM server.
Communicates with Ollama API endpoint (`/api/generate`) with timeout & JSON response parsing.
"""

import json
from typing import Any, Dict, Optional
import httpx
import structlog

from app.core.config import settings

logger = structlog.get_logger(__name__)


class OllamaClient:
    """HTTP client for Ollama LLM service."""

    def __init__(
        self,
        base_url: str = settings.OLLAMA_BASE_URL,
        model: str = settings.OLLAMA_MODEL,
        timeout: int = settings.OLLAMA_TIMEOUT,
    ) -> None:
        self.base_url = base_url.rstrip("/")
        self.model = model
        self.timeout = timeout

    async def generate_json(self, prompt: str, system_prompt: Optional[str] = None) -> Optional[Dict[str, Any]]:
        """
        Send prompt to Ollama requesting a JSON formatted response.
        """
        endpoint = f"{self.base_url}/api/generate"
        payload = {
            "model": self.model,
            "prompt": prompt,
            "format": "json",
            "stream": False,
        }
        if system_prompt:
            payload["system"] = system_prompt

        try:
            async with httpx.AsyncClient(timeout=float(self.timeout)) as client:
                logger.info("Sending prompt to Ollama", model=self.model, url=endpoint)
                response = await client.post(endpoint, json=payload)
                response.raise_for_status()

                data = response.json()
                raw_response = data.get("response", "")
                
                # Parse JSON string returned by LLM
                parsed_json = json.loads(raw_response)
                return parsed_json
        except (httpx.HTTPError, json.JSONDecodeError) as e:
            logger.error("Ollama LLM generation failed or timed out", error=str(e))
            return None


ollama_client = OllamaClient()
