from datetime import datetime
from typing import Optional, Literal
from pydantic import BaseModel, Field, ConfigDict


class EvidenceBase(BaseModel):
    source_title: str
    source_url: str
    source_domain: str
    content_snippet: str
    published_at: Optional[datetime] = None
    updated_at: Optional[datetime] = None
    relevance_score: float = Field(default=0.5, ge=0.0, le=1.0)
    source_reliability_score: float = Field(default=0.5, ge=0.0, le=1.0)
    source_type: str = "secondary"
    relationship_type: Literal["SUPPORTING", "CONTRADICTING", "NEUTRAL"] = "SUPPORTING"


class EvidenceCreate(EvidenceBase):
    claim_id: str


class EvidenceResponse(EvidenceBase):
    id: str
    claim_id: str
    retrieved_at: datetime

    model_config = ConfigDict(from_attributes=True)
