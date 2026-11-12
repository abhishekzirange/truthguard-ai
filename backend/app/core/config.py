from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    PROJECT_NAME: str = "TruthGuard AI"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    # Environment & Server
    BACKEND_HOST: str = "0.0.0.0"
    BACKEND_PORT: int = 8000
    FRONTEND_URL: str = "http://localhost:5173"
    LOG_LEVEL: str = "INFO"
    
    # Database
    DATABASE_URL: str = "sqlite:///./truthguard.db"
    
    # Tavily Web Search
    TAVILY_API_KEY: Optional[str] = None
    TAVILY_BASE_URL: str = "https://api.tavily.com"
    SEARCH_RESULTS_PER_CLAIM: int = 5
    SEARCH_CACHE_TTL_HOURS: int = 24
    
    # Bifrost AI Gateway (OpenAI Compatible)
    BIFROST_BASE_URL: str = "https://api.bifrost.ai/v1"
    BIFROST_API_KEY: Optional[str] = None
    BIFROST_MODEL: str = "gpt-4o-mini"
    BIFROST_TIMEOUT_SECONDS: float = 30.0
    
    # Verification Pipeline Defaults
    DEFAULT_VERIFICATION_DEPTH: str = "standard"  # quick, standard, deep
    DEFAULT_FRESHNESS_POLICY: str = "standard"    # strict, standard, relaxed
    MAX_CLAIMS_PER_RUN: int = 15

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )


settings = Settings()

