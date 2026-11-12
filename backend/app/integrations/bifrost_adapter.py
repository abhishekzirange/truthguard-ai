import re
import json
import time
import asyncio
import logging
from typing import Dict, Any, Optional
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
    with structured JSON validation, cost estimation, retry policies, and failure resilience.
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

    @staticmethod
    def _clean_and_parse_json(raw: str) -> tuple[bool, Any, Optional[str]]:
        """Cleans and extracts JSON objects from raw model completions."""
        if not raw or not raw.strip():
            return False, None, "Empty response content"

        clean = raw.strip()
        # Strip markdown fences
        if clean.startswith("```"):
            clean = re.sub(r"^```(?:json)?\s*", "", clean, flags=re.IGNORECASE)
            clean = re.sub(r"\s*```$", "", clean)

        try:
            return True, json.loads(clean), None
        except Exception as e:
            match = re.search(r"(\{.*\})", clean, re.DOTALL)
            if match:
                try:
                    return True, json.loads(match.group(1)), None
                except Exception:
                    pass
            return False, None, f"JSON parse error: {str(e)}"

    async def generate_structured_json(
        self,
        system_prompt: str,
        user_prompt: str,
        temperature: float = 0.0,
        response_schema: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Sends a request to Bifrost AI Gateway and expects a structured JSON response.
        Tracks token usage, latency, cost estimation, and handles retries.
        """
        start_time = time.time()

        # If Bifrost is not configured with an API key
        if not self.api_key or self.api_key.strip() == "":
            latency_ms = int((time.time() - start_time) * 1000)
            return {
                "success": False,
                "is_live": False,
                "live_success": False,
                "error": "BIFROST_KEY_NOT_CONFIGURED: Bifrost API key is unconfigured",
                "error_type": "BIFROST_KEY_NOT_CONFIGURED",
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

        max_retries = 2
        last_error = None
        last_error_type = None

        for attempt in range(max_retries + 1):
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
                        
                        # Validate and parse JSON content
                        parse_ok, parsed_json, parse_err = self._clean_and_parse_json(raw_content)
                        if not parse_ok:
                            return {
                                "success": False,
                                "is_live": True,
                                "live_success": False,
                                "error": f"BIFROST_INVALID_JSON_RESPONSE: {parse_err}",
                                "error_type": "BIFROST_INVALID_JSON_RESPONSE",
                                "content": None,
                                "usage": {
                                    "input_tokens": data.get("usage", {}).get("prompt_tokens", 0),
                                    "output_tokens": data.get("usage", {}).get("completion_tokens", 0),
                                    "estimated_cost": 0.0,
                                    "latency_ms": latency_ms,
                                    "model": self.model,
                                    "provider": "bifrost"
                                }
                            }

                        # Extract usage
                        usage_data = data.get("usage", {})
                        input_tokens = usage_data.get("prompt_tokens", 0)
                        output_tokens = usage_data.get("completion_tokens", 0)
                        cost = self._calculate_cost(input_tokens, output_tokens)

                        return {
                            "success": True,
                            "is_live": True,
                            "live_success": True,
                            "error": None,
                            "error_type": None,
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
                    elif response.status_code in (401, 403):
                        last_error = f"BIFROST_AUTH_ERROR: Authentication failed (HTTP {response.status_code})"
                        last_error_type = "BIFROST_AUTH_ERROR"
                        break
                    elif response.status_code == 429:
                        last_error = "BIFROST_RATE_LIMIT: Gateway rate limit exceeded (HTTP 429)"
                        last_error_type = "BIFROST_RATE_LIMIT"
                        if attempt < max_retries:
                            await asyncio.sleep(0.5 * (2 ** attempt))
                            continue
                    else:
                        last_error = f"BIFROST_HTTP_ERROR: Gateway returned HTTP {response.status_code}"
                        last_error_type = "BIFROST_HTTP_ERROR"
                        if response.status_code >= 500 and attempt < max_retries:
                            await asyncio.sleep(0.5 * (2 ** attempt))
                            continue
                        break

            except httpx.TimeoutException:
                last_error = "BIFROST_TIMEOUT: Request timed out"
                last_error_type = "BIFROST_TIMEOUT"
                if attempt < max_retries:
                    await asyncio.sleep(0.5 * (2 ** attempt))
                    continue
            except Exception as e:
                last_error = f"BIFROST_NETWORK_ERROR: {str(e)}"
                last_error_type = "BIFROST_NETWORK_ERROR"
                break

        latency_ms = int((time.time() - start_time) * 1000)
        return {
            "success": False,
            "is_live": False,
            "live_success": False,
            "error": last_error,
            "error_type": last_error_type,
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

