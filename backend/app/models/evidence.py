import uuid
from datetime import datetime, timezone
from sqlalchemy import Column, String, DateTime, Float, Text, ForeignKey
from sqlalchemy.orm import relationship
from app.database.session import Base


class Evidence(Base):
    __tablename__ = "evidence"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    claim_id = Column(String(36), ForeignKey("claims.id", ondelete="CASCADE"), nullable=False, index=True)
    
    source_title = Column(Text, nullable=False)
    source_url = Column(Text, nullable=False)
    source_domain = Column(String(255), index=True, nullable=False)
    content_snippet = Column(Text, nullable=False)
    
    published_at = Column(DateTime, nullable=True)
    updated_at = Column(DateTime, nullable=True)
    retrieved_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), nullable=False)
    
    relevance_score = Column(Float, default=0.5, nullable=False)
    source_reliability_score = Column(Float, default=0.5, nullable=False)
    source_type = Column(String(50), default="secondary", nullable=False)  # primary, secondary, community, unverified
    relationship_type = Column(String(50), default="SUPPORTING", nullable=False)  # SUPPORTING, CONTRADICTING, NEUTRAL
    
    # Relationships
    claim = relationship("Claim", back_populates="evidence_items")

