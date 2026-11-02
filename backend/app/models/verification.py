import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship
from app.database.session import Base


class VerificationRun(Base):
    __tablename__ = "verification_runs"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(String(36), ForeignKey("users.id", ondelete="SET NULL"), nullable=True, index=True)
    original_answer = Column(Text, nullable=False)
    domain = Column(String(100), default="general", nullable=False)
    freshness_policy = Column(String(50), default="standard", nullable=False)
    verification_depth = Column(String(50), default="standard", nullable=False)
    verification_status = Column(String(50), default="PENDING", index=True, nullable=False)  # PENDING, PROCESSING, COMPLETED, FAILED
    
    execution_time_ms = Column(Integer, nullable=True)
    summary = Column(JSON, nullable=True)  # Store summary metrics {total, outdated, current, etc.}
    error_message = Column(Text, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True, nullable=False)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    claims = relationship("Claim", back_populates="run", cascade="all, delete-orphan", order_by="Claim.created_at")
    model_usages = relationship("ModelUsage", back_populates="run", cascade="all, delete-orphan")
    events = relationship("VerificationEvent", back_populates="run", cascade="all, delete-orphan", order_by="VerificationEvent.created_at")
