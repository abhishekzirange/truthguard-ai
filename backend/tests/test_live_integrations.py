import pytest
from unittest.mock import patch
import httpx
from app.integrations.tavily_adapter import TavilyAdapter
from app.integrations.bifrost_adapter import BifrostAdapter
from app.services.verification_service import VerificationService
from app.schemas.verification import VerificationRequest
from app.database.session import SessionLocal


class TestLiveIntegrationFailuresAndTransitions:
    """
    Test suite for Phase 2: Live Integration Hardening, Error Resilience,
    and Live/Partial/Offline Execution Mode Transitions.
    """

    # 1. Tavily Authentication Failure
    @pytest.mark.asyncio
    async def test_tavily_auth_failure(self):
        adapter = TavilyAdapter(api_key="tvly-invalid-key")
        mock_response = httpx.Response(
            401,
            text="Unauthorized",
            request=httpx.Request("POST", "https://api.tavily.com/search")
        )

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            res = await adapter.search("python latest version")
            assert res["is_live"] is False
            assert res["live_success"] is False
            assert res["error_type"] == "TAVILY_AUTH_ERROR"
            assert "TAVILY_AUTH_ERROR" in res["error"]

    # 2. Bifrost Authentication Failure
    @pytest.mark.asyncio
    async def test_bifrost_auth_failure(self):
        adapter = BifrostAdapter(api_key="sk-invalid-bifrost-key")
        mock_response = httpx.Response(
            401,
            text='{"error": {"message": "Invalid API Key"}}',
            request=httpx.Request("POST", "https://api.bifrost.io/v1/chat/completions")
        )

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            res = await adapter.generate_structured_json("System", "User")
            assert res["success"] is False
            assert res["is_live"] is False
            assert res["error_type"] == "BIFROST_AUTH_ERROR"
            assert "BIFROST_AUTH_ERROR" in res["error"]

    # 3. Tavily Rate Limit (HTTP 429) Handling
    @pytest.mark.asyncio
    async def test_tavily_rate_limit(self):
        adapter = TavilyAdapter(api_key="tvly-test-key")
        mock_response = httpx.Response(
            429,
            text="Rate Limit Exceeded",
            request=httpx.Request("POST", "https://api.tavily.com/search")
        )

        with patch("httpx.AsyncClient.post", return_value=mock_response), \
             patch("asyncio.sleep", return_value=None):
            res = await adapter.search("fastapi documentation")
            assert res["is_live"] is False
            assert res["live_success"] is False
            assert res["error_type"] == "TAVILY_RATE_LIMIT"

    # 4. Bifrost Rate Limit (HTTP 429) Handling
    @pytest.mark.asyncio
    async def test_bifrost_rate_limit(self):
        adapter = BifrostAdapter(api_key="sk-test-key")
        mock_response = httpx.Response(
            429,
            text='{"error": "Too Many Requests"}',
            request=httpx.Request("POST", "https://api.bifrost.io/v1/chat/completions")
        )

        with patch("httpx.AsyncClient.post", return_value=mock_response), \
             patch("asyncio.sleep", return_value=None):
            res = await adapter.generate_structured_json("System", "User")
            assert res["success"] is False
            assert res["is_live"] is False
            assert res["error_type"] == "BIFROST_RATE_LIMIT"

    # 5. Tavily Timeout Handling
    @pytest.mark.asyncio
    async def test_tavily_timeout(self):
        adapter = TavilyAdapter(api_key="tvly-test-key")
        with patch("httpx.AsyncClient.post", side_effect=httpx.TimeoutException("Timeout")), \
             patch("asyncio.sleep", return_value=None):
            res = await adapter.search("react 19 release")
            assert res["is_live"] is False
            assert res["live_success"] is False
            assert res["error_type"] == "TAVILY_TIMEOUT"

    # 6. Bifrost Timeout Handling
    @pytest.mark.asyncio
    async def test_bifrost_timeout(self):
        adapter = BifrostAdapter(api_key="sk-test-key")
        with patch("httpx.AsyncClient.post", side_effect=httpx.TimeoutException("Timeout")), \
             patch("asyncio.sleep", return_value=None):
            res = await adapter.generate_structured_json("System", "User")
            assert res["success"] is False
            assert res["is_live"] is False
            assert res["error_type"] == "BIFROST_TIMEOUT"

    # 7. Bifrost Invalid Structured JSON Handling
    @pytest.mark.asyncio
    async def test_bifrost_invalid_json_handling(self):
        adapter = BifrostAdapter(api_key="sk-test-key")
        mock_response = httpx.Response(
            200,
            json={
                "choices": [{"message": {"content": "This is plain conversational text without valid JSON."}}],
                "usage": {"prompt_tokens": 100, "completion_tokens": 20}
            },
            request=httpx.Request("POST", "https://api.bifrost.io/v1/chat/completions")
        )

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            res = await adapter.generate_structured_json("System", "User")
            assert res["success"] is False
            assert res["error_type"] == "BIFROST_INVALID_JSON_RESPONSE"
            assert res["content"] is None

    # 8. Bifrost Markdown-Fenced JSON Recovery
    @pytest.mark.asyncio
    async def test_bifrost_markdown_fenced_json_recovery(self):
        adapter = BifrostAdapter(api_key="sk-test-key")
        fenced_payload = '```json\n{"verdict": "CURRENT", "reasoning": "Documented correctly."}\n```'
        mock_response = httpx.Response(
            200,
            json={
                "choices": [{"message": {"content": fenced_payload}}],
                "usage": {"prompt_tokens": 80, "completion_tokens": 25}
            },
            request=httpx.Request("POST", "https://api.bifrost.io/v1/chat/completions")
        )

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            res = await adapter.generate_structured_json("System", "User")
            assert res["success"] is True
            assert res["content"]["verdict"] == "CURRENT"
            assert res["content"]["reasoning"] == "Documented correctly."

    # 9. Empty Search Results Handled Gracefully
    @pytest.mark.asyncio
    async def test_empty_search_results(self):
        adapter = TavilyAdapter(api_key="tvly-test-key")
        mock_response = httpx.Response(
            200,
            json={"results": []},
            request=httpx.Request("POST", "https://api.tavily.com/search")
        )

        with patch("httpx.AsyncClient.post", return_value=mock_response):
            res = await adapter.search("asdkfjhasdlkfjh12341234obscure")
            assert res["is_live"] is True
            assert len(res["results"]) == 0

    # 10. Missing Publication Date Not Fabricated
    def test_missing_publication_date_no_fabrication(self):
        adapter = TavilyAdapter()
        raw = [{"title": "Post", "url": "https://example.com/doc", "content": "Text", "published_date": None, "score": 0.9}]
        normalized = adapter._normalize_results(raw)
        assert len(normalized) == 1
        assert normalized[0]["published_at"] is None

    # 11. Live-to-Partial Failure Transition: Tavily Live, Bifrost Fails
    @pytest.mark.asyncio
    async def test_live_to_partial_transition_bifrost_fails(self):
        db = SessionLocal()
        try:
            service = VerificationService(db)
            service.tavily_adapter.api_key = "tvly-valid"
            service.bifrost_adapter.api_key = "sk-valid"

            # Mock Tavily success
            mock_tavily = httpx.Response(
                200,
                json={
                    "results": [{
                        "title": "Python 3.13 Docs",
                        "url": "https://docs.python.org/3/whatsnew/3.13.html",
                        "content": "Python 3.13 is the newest release. Python 3.11 is now security-only.",
                        "published_date": "2024-10-07T00:00:00Z",
                        "score": 0.95
                    }]
                },
                request=httpx.Request("POST", "https://api.tavily.com/search")
            )

            # Mock Bifrost failure (500 Internal Server Error)
            mock_bifrost = httpx.Response(
                500,
                text="Internal Server Error",
                request=httpx.Request("POST", "https://api.bifrost.io/v1/chat/completions")
            )

            async def mock_post(url, **kwargs):
                if "tavily" in str(url):
                    return mock_tavily
                return mock_bifrost

            with patch("httpx.AsyncClient.post", side_effect=mock_post), \
                 patch("asyncio.sleep", return_value=None):
                req = VerificationRequest(answer_text="Python 3.11 is the latest stable Python release.", domain="technology")
                run = await service.execute_verification(req)

                # Should be PARTIAL, not LIVE
                assert run.execution_mode == "PARTIAL"
                assert run.integration_status["tavily"]["status"] == "HEALTHY"
                assert run.integration_status["bifrost"]["status"] == "FAILED"
                # Provenance must NOT be LIVE_TAVILY_BIFROST
                assert run.claims[0].assessment.provenance != "LIVE_TAVILY_BIFROST"
        finally:
            db.close()

    # 12. Live-to-Offline Behavior When Keys Unconfigured
    @pytest.mark.asyncio
    async def test_live_to_offline_behavior_unconfigured(self):
        db = SessionLocal()
        try:
            service = VerificationService(db)
            service.tavily_adapter.api_key = ""
            service.bifrost_adapter.api_key = ""

            req = VerificationRequest(answer_text="FastAPI is a Python web framework.", domain="technology")
            run = await service.execute_verification(req)

            assert run.execution_mode == "OFFLINE"
            assert run.integration_status["tavily"]["status"] == "UNCONFIGURED"
            assert run.integration_status["bifrost"]["status"] == "UNCONFIGURED"
            assert run.claims[0].assessment.provenance in ["OFFLINE_LOCAL", "OFFLINE_DETERMINISTIC", "OFFLINE_HEURISTIC_ANALYSIS"]
            assert "LIVE" not in run.claims[0].assessment.provenance
        finally:
            db.close()

    # 13. No Fabricated Live Provenance
    @pytest.mark.asyncio
    async def test_no_fabricated_live_provenance(self):
        db = SessionLocal()
        try:
            service = VerificationService(db)
            service.tavily_adapter.api_key = ""
            service.bifrost_adapter.api_key = ""

            req = VerificationRequest(answer_text="Kubernetes 1.20 deprecated dockershim.", domain="technology")
            run = await service.execute_verification(req)

            assert run.execution_mode != "LIVE"
            assert run.claims[0].assessment.provenance == "OFFLINE_DETERMINISTIC"
            assert "LIVE" not in run.claims[0].assessment.provenance
        finally:
            db.close()
