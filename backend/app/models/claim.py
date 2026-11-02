import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class Claim(Base):
    __tablename__ = "claims"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    run_id = Column(String(36), ForeignKey("verification_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    
    claim_text = Column(Text, nullable=False)
    subject = Column(String(255), nullable=True)
    predicate = Column(String(255), nullable=True)
    object = Column(String(255), nullable=True)
    category = Column(String(100), default="general_fact", nullable=False)  # software_version, api_version, pricing, regulation, company_info, stats, etc.
    temporal_sensitivity = Column(String(20), default="MEDIUM", nullable=False)  # HIGH, MEDIUM, LOW
    status = Column(String(50), default="UNVERIFIED", index=True, nullable=False)  # CURRENT, OUTDATED, CONTRADICTED, UNVERIFIED, TIME_SENSITIVE
    
    mentioned_date = Column(String(100), nullable=True)
    mentioned_version = Column(String(100), nullable=True)
    verification_query = Column(Text, nullable=True)
    extraction_confidence = Column(Float, default=1.0, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    run = relationship("VerificationRun", back_populates="claims")
    evidence_items = relationship("Evidence", back_populates="claim", cascade="all, delete-orphan")
    assessment = relationship("ClaimAssessment", back_populates="claim", uselist=False, cascade="all, delete-orphan")
