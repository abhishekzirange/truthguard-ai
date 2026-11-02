from datetime import datetime
from typing import Optional, List, Dict, Any, Literal
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.claim import ClaimResponse


class VerificationRequest(BaseModel):
    answer_text: str = Field(..., min_length=5, max_length=15000, description="The AI-generated answer text to verify")
    domain: str = Field(default="general", description="Verification domain, e.g. technology, software, business, pricing, regulation")
    verification_depth: Literal["quick", "standard", "deep"] = "standard"
    freshness_policy: Literal["strict", "standard", "relaxed"] = "standard"


class BatchVerificationRequest(BaseModel):
    items: List[VerificationRequest] = Field(..., max_length=10)


class VerificationSummary(BaseModel):
    total_claims: int = 0
    current_claims: int = 0
    outdated_claims: int = 0
    contradicted_claims: int = 0
    unverified_claims: int = 0
    time_sensitive_claims: int = 0
    overall_freshness_score: Optional[float] = None
    overall_evidence_quality_score: Optional[float] = None


class VerificationRunResponse(BaseModel):
    id: str
    original_answer: str
    domain: str
    freshness_policy: str
    verification_depth: str
    verification_status: Literal["PENDING", "PROCESSING", "COMPLETED", "FAILED"]
    execution_time_ms: Optional[int] = None
    summary: Optional[VerificationSummary] = None
    error_message: Optional[str] = None
    created_at: datetime
    completed_at: Optional[datetime] = None
    claims: List[ClaimResponse] = []

    model_config = ConfigDict(from_attributes=True)


class VerificationRunListItem(BaseModel):
    id: str
    original_answer: str
    domain: str
    freshness_policy: str
    verification_status: str
    execution_time_ms: Optional[int] = None
    total_claims: int = 0
    outdated_count: int = 0
    current_count: int = 0
    contradicted_count: int = 0
    created_at: datetime
    completed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)
