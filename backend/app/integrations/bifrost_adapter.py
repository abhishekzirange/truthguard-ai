import json
import time
import logging
from typing import Dict, Any, Optional, List
import httpx
from app.core.config import settings

logger = logging.getLogger("truthguard.bifrost")

# Approximate pricing per 1M tokens for common gateway models
MODEL_COST_PER_1M = {
    "gpt-4o": {"input": 2.50, "output": 10.00},
    "gpt-4o-mini": {"input": 0.15, "output": 0.60},
    "claude-3-5-sonnet": {"input": 3.00, "output": 15.00},
    "default": {"input": 0.50, "output": 1.50},
}


class BifrostAdapter:
    """
    Adapter for the Bifrost AI Gateway implementing standard OpenAI-compatible completions
    with structured JSON validation, cost estimation, and failure resilience.
    """
    def __init__(
        self,
        base_url: Optional[str] = None,
        api_key: Optional[str] = None,
        model: Optional[str] = None,
        timeout: Optional[float] = None,
    ):
        self.base_url = (base_url or settings.BIFROST_BASE_URL).rstrip("/")
        self.api_key = api_key or settings.BIFROST_API_KEY
        self.model = model or settings.BIFROST_MODEL
        self.timeout = timeout or settings.BIFROST_TIMEOUT_SECONDS

    async def generate_structured_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
        response_schema: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Sends a request to Bifrost AI Gateway and expects a structured JSON response.
        Tracks token usage, latency, and estimated cost.
        """
        start_time = time.time()

        # If Bifrost is not configured with an API key, we return a fallback response marker
        if not self.api_key or self.api_key.strip() == "":
            logger.info("Bifrost API key not configured; using deterministic inference engine.")
            latency_ms = int((time.time() - start_time) * 1000)
            return {
                "success": False,
                "error": "BIFROST_API_KEY_NOT_CONFIGURED",
                "content": None,
                "usage": {
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "estimated_cost": 0.0,
                    "latency_ms": latency_ms,
                    "model": self.model,
                    "provider": "bifrost"
                }
            }

        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }

        messages = [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ]

        payload: Dict[str, Any] = {
            "model": self.model,
            "messages": messages,
            "temperature": temperature,
            "response_format": {"type": "json_object"},
        }

        try:
            async with httpx.AsyncClient(timeout=self.timeout) as client:
                response = await client.post(
                    f"{self.base_url}/chat/completions",
                    headers=headers,
                    json=payload,
                )
                latency_ms = int((time.time() - start_time) * 1000)

                if response.status_code == 200:
                    data = response.json()
                    choice = data.get("choices", [{}])[0]
                    raw_content = choice.get("message", {}).get("content", "{}")
                    parsed_json = json.loads(raw_content)

                    # Extract usage
                    usage_data = data.get("usage", {})
                    input_tokens = usage_data.get("prompt_tokens", 0)
                    output_tokens = usage_data.get("completion_tokens", 0)
                    cost = self._calculate_cost(input_tokens, output_tokens)

                    return {
                        "success": True,
                        "error": None,
                        "content": parsed_json,
                        "usage": {
                            "input_tokens": input_tokens,
                            "output_tokens": output_tokens,
                            "estimated_cost": cost,
                            "latency_ms": latency_ms,
                            "model": self.model,
                            "provider": "bifrost"
                        }
                    }
                else:
                    error_msg = f"Bifrost Gateway HTTP {response.status_code}: {response.text}"
                    logger.error(error_msg)
                    return {
                        "success": False,
                        "error": error_msg,
                        "content": None,
                        "usage": {
                            "input_tokens": 0,
                            "output_tokens": 0,
                            "estimated_cost": 0.0,
                            "latency_ms": latency_ms,
                            "model": self.model,
                            "provider": "bifrost"
                        }
                    }

        except httpx.TimeoutException:
            latency_ms = int((time.time() - start_time) * 1000)
            logger.warning(f"Bifrost request timed out after {self.timeout}s")
            return {
                "success": False,
                "error": "BIFROST_GATEWAY_TIMEOUT",
                "content": None,
                "usage": {
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "estimated_cost": 0.0,
                    "latency_ms": latency_ms,
                    "model": self.model,
                    "provider": "bifrost"
                }
            }
        except Exception as e:
            latency_ms = int((time.time() - start_time) * 1000)
            logger.exception(f"Bifrost adapter exception: {e}")
            return {
                "success": False,
                "error": str(e),
                "content": None,
                "usage": {
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "estimated_cost": 0.0,
                    "latency_ms": latency_ms,
                    "model": self.model,
                    "provider": "bifrost"
                }
            }

    async def check_health(self) -> Dict[str, Any]:
        """Diagnostic check for Bifrost AI Gateway connectivity."""
        if not self.api_key:
            return {
                "configured": False,
                "reachable": False,
                "latency_ms": None,
                "message": "BIFROST_API_KEY is not configured in .env",
                "details": {"model": self.model, "base_url": self.base_url}
            }
        start = time.time()
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json",
        }
        try:
            async with httpx.AsyncClient(timeout=6.0) as client:
                res = await client.get(f"{self.base_url}/models", headers=headers)
                latency = int((time.time() - start) * 1000)
                if res.status_code in (200, 201):
                    return {
                        "configured": True,
                        "reachable": True,
                        "latency_ms": latency,
                        "message": f"Connected to Bifrost Gateway ({self.model})",
                        "details": {"model": self.model, "base_url": self.base_url}
                    }
                return {
                    "configured": True,
                    "reachable": False,
                    "latency_ms": latency,
                    "message": f"Bifrost returned HTTP {res.status_code}",
                    "details": {"status_code": res.status_code}
                }
        except Exception as e:
            return {
                "configured": True,
                "reachable": False,
                "latency_ms": None,
                "message": f"Bifrost connection error: {str(e)}",
                "details": {"base_url": self.base_url}
            }

    def _calculate_cost(self, input_tokens: int, output_tokens: int) -> float:
        rates = MODEL_COST_PER_1M.get(self.model, MODEL_COST_PER_1M["default"])
        input_cost = (input_tokens / 1_000_000.0) * rates["input"]
        output_cost = (output_tokens / 1_000_000.0) * rates["output"]
        return round(input_cost + output_cost, 6)
