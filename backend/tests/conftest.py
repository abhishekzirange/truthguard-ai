import os
import pytest
from app.core.config import settings

@pytest.fixture(autouse=True)
def isolate_test_environment(monkeypatch):
    """
    Isolates automated unit test suites to use deterministic fixtures,
    preventing live external API calls during regression testing.
    Individual integration tests can explicitly patch and configure adapters.
    """
    monkeypatch.setattr(settings, "TAVILY_API_KEY", "")
    monkeypatch.setattr(settings, "BIFROST_API_KEY", "")

