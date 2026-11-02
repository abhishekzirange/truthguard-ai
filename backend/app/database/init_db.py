import os
import logging
from sqlalchemy import inspect, create_engine
from sqlalchemy.orm import sessionmaker
from alembic.config import Config
from alembic import command
from app.database.session import engine as default_engine, SessionLocal as default_SessionLocal
from app.core.config import settings
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


def init_database(engine_to_use=None, db_url_to_use=None):
    """
    Safely initializes tables using Alembic migrations without duplicate table conflicts,
    and seeds initial domain reliability data.
    """
    current_engine = engine_to_use or default_engine
    db_url = db_url_to_use or (str(current_engine.url) if hasattr(current_engine, "url") else settings.DATABASE_URL)
    
    inspector = inspect(current_engine)
    existing_tables = inspector.get_table_names()
    
    backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", ".."))
    alembic_ini_path = os.path.join(backend_dir, "alembic.ini")

    if os.path.exists(alembic_ini_path):
        alembic_cfg = Config(alembic_ini_path)
        alembic_cfg.set_main_option("sqlalchemy.url", db_url)
        
        if "alembic_version" not in existing_tables:
            if "verification_runs" in existing_tables or "claims" in existing_tables:
                logger.info("Existing schema detected without alembic_version; stamping head.")
                command.stamp(alembic_cfg, "head")
            else:
                logger.info("Clean database detected; applying Alembic migrations to head.")
                command.upgrade(alembic_cfg, "head")
        else:
            logger.info("Alembic version table detected; upgrading to head.")
            command.upgrade(alembic_cfg, "head")
    else:
        logger.warning(f"alembic.ini not found at {alembic_ini_path}; falling back to metadata create_all.")
        from app.database.session import Base
        Base.metadata.create_all(bind=current_engine)

    # Seed default authoritative domains if not present
    if engine_to_use:
        session_factory = sessionmaker(autocommit=False, autoflush=False, bind=engine_to_use)
        db = session_factory()
    else:
        db = default_SessionLocal()

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
    print("Database tables initialized successfully via Alembic migrations!")
