import pytest
from app.integrations.tavily_adapter import TavilyAdapter


class TestExternalUrlSecurity:
    """Security test suite for Fix 2: External URL Validation and Sanitization."""

    @pytest.fixture
    def adapter(self):
        return TavilyAdapter()

    # 1. Safe Schemes (HTTP / HTTPS)
    def test_valid_https_url(self, adapter):
        res = adapter.validate_and_sanitize_url("https://docs.python.org/3/whatsnew/3.13.html")
        assert res is not None
        clean_url, domain = res
        assert clean_url == "https://docs.python.org/3/whatsnew/3.13.html"
        assert domain == "docs.python.org"

    def test_valid_http_url(self, adapter):
        res = adapter.validate_and_sanitize_url("http://example.org/spec")
        assert res is not None
        clean_url, domain = res
        assert clean_url == "http://example.org/spec"
        assert domain == "example.org"

    def test_strip_www_prefix(self, adapter):
        res = adapter.validate_and_sanitize_url("https://www.reuters.com/technology/article")
        assert res is not None
        clean_url, domain = res
        assert domain == "reuters.com"

    # 2. Rejection of Unsafe Schemes
    def test_reject_javascript_scheme(self, adapter):
        res = adapter.validate_and_sanitize_url("javascript:alert(document.cookie)")
        assert res is None

    def test_reject_data_scheme(self, adapter):
        res = adapter.validate_and_sanitize_url("data:text/html;base64,PHNjcmlwdD5hbGVydCgxKTwvc2NyaXB0Pg==")
        assert res is None

    def test_reject_file_scheme(self, adapter):
        res = adapter.validate_and_sanitize_url("file:///etc/passwd")
        assert res is None

    def test_reject_vbscript_scheme(self, adapter):
        res = adapter.validate_and_sanitize_url("vbscript:msgbox(1)")
        assert res is None

    # 3. Hostname & Syntax Validation
    def test_reject_empty_and_non_string(self, adapter):
        assert adapter.validate_and_sanitize_url("") is None
        assert adapter.validate_and_sanitize_url(None) is None
        assert adapter.validate_and_sanitize_url(12345) is None

    def test_reject_control_characters_in_hostname(self, adapter):
        res = adapter.validate_and_sanitize_url("https://malicious<script>.com/path")
        assert res is None

    def test_reject_single_word_non_localhost_hostname(self, adapter):
        res = adapter.validate_and_sanitize_url("https://internalhost/path")
        assert res is None

    def test_allow_localhost(self, adapter):
        res = adapter.validate_and_sanitize_url("http://localhost:8000/docs")
        assert res is not None
        clean_url, domain = res
        assert domain == "localhost"

    # 4. Integration with Results Normalization
    def test_normalize_results_filters_malicious_urls(self, adapter):
        raw_items = [
            {"title": "Valid Source", "url": "https://fastapi.tiangolo.com/", "content": "FastAPI doc", "score": 0.95},
            {"title": "XSS Attempt", "url": "javascript:fetch('//attacker.com')", "content": "Bad link", "score": 0.9},
            {"title": "File Leak", "url": "file:///C:/Windows/System32", "content": "Local file", "score": 0.8},
            {"title": "Data URI", "url": "data:text/plain;hello", "content": "Inline data", "score": 0.5},
        ]
        sanitized = adapter._normalize_results(raw_items)
        assert len(sanitized) == 1
        assert sanitized[0]["url"] == "https://fastapi.tiangolo.com/"
        assert sanitized[0]["domain"] == "fastapi.tiangolo.com"

