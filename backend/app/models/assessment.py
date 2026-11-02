import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Float, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.session import Base


class ClaimAssessment(Base):
    __tablename__ = "claim_assessments"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    claim_id = Column(String(36), ForeignKey("claims.id", ondelete="CASCADE"), unique=True, nullable=False, index=True)
    
    verdict = Column(String(50), nullable=False)  # CURRENT, OUTDATED, CONTRADICTED, UNVERIFIED, TIME_SENSITIVE
    provenance = Column(String(50), nullable=True, default="OFFLINE_DETERMINISTIC")  # LIVE_BIFROST, OFFLINE_DETERMINISTIC, OFFLINE_HEURISTIC_ANALYSIS, MOCK
    freshness_score = Column(Float, nullable=True)  # 0.0 - 100.0 or None if date unknown
    evidence_quality_score = Column(Float, nullable=True)  # 0.0 - 100.0
    reasoning = Column(Text, nullable=False)
    suggested_correction = Column(Text, nullable=True)
    
    supporting_evidence_ids = Column(JSON, default=list, nullable=False)
    contradicting_evidence_ids = Column(JSON, default=list, nullable=False)
    missing_information = Column(JSON, default=list, nullable=False)
    
    assessed_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    claim = relationship("Claim", back_populates="assessment")

