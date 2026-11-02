import logging
from app.database.session import engine, Base, SessionLocal
from app.models import SourceDomain

logger = logging.getLogger("truthguard.init_db")

DEFAULT_AUTHORITATIVE_DOMAINS = [
    # Primary tech & software registries
    {"domain": "python.org", "source_type": "primary", "reliability_score": 1.0, "category": "software"},
    {"domain": "docs.python.org", "source_type": "primary", "reliability_score": 1.0, "category": "software"},
    {"domain": "pypi.org", "source_type": "primary", "reliability_score": 1.0, "category": "software"},
    {"domain": "fastapi.tiangolo.com", "source_type": "primary", "reliability_score": 1.0, "category": "software"},
    {"domain": "github.com", "source_type": "primary", "reliability_score": 0.95, "category": "code_registry"},
    {"domain": "postgresql.org", "source_type": "primary", "reliability_score": 1.0, "category": "database"},
    {"domain": "react.dev", "source_type": "primary", "reliability_score": 1.0, "category": "software"},
    {"domain": "openai.com", "source_type": "primary", "reliability_score": 0.95, "category": "ai"},
    
    # Authoritative news & market sources
    {"domain": "reuters.com", "source_type": "authoritative", "reliability_score": 0.9, "category": "news"},
    {"domain": "bloomberg.com", "source_type": "authoritative", "reliability_score": 0.9, "category": "business"},
    {"domain": "techcrunch.com", "source_type": "authoritative", "reliability_score": 0.85, "category": "tech_news"},
    
    # Official government domains
    {"domain": "sec.gov", "source_type": "primary", "reliability_score": 1.0, "category": "regulation"},
    {"domain": "irs.gov", "source_type": "primary", "reliability_score": 1.0, "category": "regulation"},
    {"domain": "gov.uk", "source_type": "primary", "reliability_score": 1.0, "category": "regulation"},
    
    # Community & tech portals
    {"domain": "stackoverflow.com", "source_type": "community", "reliability_score": 0.65, "category": "q_and_a"},
    {"domain": "medium.com", "source_type": "blog", "reliability_score": 0.45, "category": "general"},
    {"domain": "dev.to", "source_type": "blog", "reliability_score": 0.5, "category": "tech_blog"},
]


def init_database():
    """Initializes tables and seeds initial domain reliability data."""
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing_count = db.query(SourceDomain).count()
        if existing_count == 0:
            for item in DEFAULT_AUTHORITATIVE_DOMAINS:
                domain_obj = SourceDomain(
                    domain=item["domain"],
                    source_type=item["source_type"],
                    reliability_score=item["reliability_score"],
                    category=item["category"],
                )
                db.add(domain_obj)
            db.commit()
            logger.info(f"Seeded {len(DEFAULT_AUTHORITATIVE_DOMAINS)} authoritative domains.")
    finally:
        db.close()


if __name__ == "__main__":
    init_database()
    print("Database tables initialized successfully!")
