from datetime import datetime
from typing import Optional, List, Literal
from pydantic import BaseModel, Field, ConfigDict
from app.schemas.evidence import EvidenceResponse


class ClaimBase(BaseModel):
    claim_text: str
    subject: Optional[str] = None
    predicate: Optional[str] = None
    object: Optional[str] = None
    category: str = "general_fact"
    temporal_sensitivity: Literal["HIGH", "MEDIUM", "LOW"] = "MEDIUM"
    mentioned_date: Optional[str] = None
    mentioned_version: Optional[str] = None
    verification_query: Optional[str] = None
    extraction_confidence: float = Field(default=1.0, ge=0.0, le=1.0)


class ClaimAssessmentSchema(BaseModel):
    verdict: Literal["CURRENT", "OUTDATED", "CONTRADICTED", "UNVERIFIED", "TIME_SENSITIVE"]
    freshness_score: Optional[float] = None
    evidence_quality_score: Optional[float] = None
    reasoning: str
    suggested_correction: Optional[str] = None
    supporting_evidence_ids: List[str] = []
    contradicting_evidence_ids: List[str] = []
    missing_information: List[str] = []
    assessed_at: Optional[datetime] = None

    model_config = ConfigDict(from_attributes=True)


class ClaimResponse(ClaimBase):
    id: str
    run_id: str
    status: Literal["CURRENT", "OUTDATED", "CONTRADICTED", "UNVERIFIED", "TIME_SENSITIVE"]
    created_at: datetime
    assessment: Optional[ClaimAssessmentSchema] = None
    evidence_count: int = 0
    evidence_items: List[EvidenceResponse] = []

    model_config = ConfigDict(from_attributes=True)
