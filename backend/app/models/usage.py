import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class ModelUsage(Base):
    __tablename__ = "model_usage"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    run_id = Column(String(36), ForeignKey("verification_runs.id", ondelete="CASCADE"), nullable=False, index=True)
    
    model = Column(String(100), nullable=False)
    provider = Column(String(100), default="bifrost", nullable=False)
    input_tokens = Column(Integer, default=0, nullable=False)
    output_tokens = Column(Integer, default=0, nullable=False)
    estimated_cost = Column(Float, default=0.0, nullable=False)
    latency_ms = Column(Integer, default=0, nullable=False)
    
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)

    # Relationships
    run = relationship("VerificationRun", back_populates="model_usages")

