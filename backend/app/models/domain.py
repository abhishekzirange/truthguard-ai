import uuid
from sqlalchemy import Column, String, Float
from app.database.session import Base


class SourceDomain(Base):
    __tablename__ = "source_domains"

    id = Column(String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    domain = Column(String(255), unique=True, index=True, nullable=False)
    source_type = Column(String(50), default="secondary", nullable=False)  # primary, authoritative, secondary, blog, low
    reliability_score = Column(Float, default=0.5, nullable=False)  # 0.0 to 1.0
    category = Column(String(100), nullable=True)

