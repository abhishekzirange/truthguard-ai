import os
import tempfile
import pytest
from sqlalchemy import inspect, create_engine
from alembic.config import Config
from alembic import command
from app.database.init_db import init_database


class TestDatabaseMigrations:
    """Test suite for Fix 5: Safe Database Migrations and Alembic Synchronization."""

    @pytest.fixture
    def temp_sqlite_db(self):
        with tempfile.NamedTemporaryFile(suffix=".db", delete=False) as f:
            db_path = f.name
        yield db_path
        if os.path.exists(db_path):
            try:
                os.remove(db_path)
            except Exception:
                pass

    def test_upgrade_and_downgrade_cycle(self, temp_sqlite_db):
        clean_path = temp_sqlite_db.replace("\\", "/")
        db_url = f"sqlite:///{clean_path}"
        backend_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        alembic_ini_path = os.path.join(backend_dir, "alembic.ini")

        cfg = Config(alembic_ini_path)
        cfg.set_main_option("sqlalchemy.url", db_url)

        # 1. Upgrade to head
        command.upgrade(cfg, "head")
        engine = create_engine(db_url)
        inspector = inspect(engine)
        tables_after_upgrade = inspector.get_table_names()

        assert "verification_runs" in tables_after_upgrade
        assert "claims" in tables_after_upgrade
        assert "claim_assessments" in tables_after_upgrade
        assert "evidence" in tables_after_upgrade
        assert "source_domains" in tables_after_upgrade
        assert "alembic_version" in tables_after_upgrade

        # Verify provenance column exists in claim_assessments and execution_mode in verification_runs
        cols = [c["name"] for c in inspector.get_columns("claim_assessments")]
        assert "provenance" in cols

        run_cols = [c["name"] for c in inspector.get_columns("verification_runs")]
        assert "execution_mode" in run_cols
        assert "integration_status" in run_cols

        # 2. Downgrade to base
        command.downgrade(cfg, "base")
        inspector_post_downgrade = inspect(engine)
        tables_post_downgrade = inspector_post_downgrade.get_table_names()
        assert "verification_runs" not in tables_post_downgrade
        assert "claims" not in tables_post_downgrade

        # 3. Re-upgrade to head
        command.upgrade(cfg, "head")
        inspector_reup = inspect(engine)
        assert "verification_runs" in inspector_reup.get_table_names()

    def test_init_database_idempotency(self, temp_sqlite_db):
        clean_path = temp_sqlite_db.replace("\\", "/")
        db_url = f"sqlite:///{clean_path}"
        engine = create_engine(db_url)

        # First initialization
        init_database(engine_to_use=engine, db_url_to_use=db_url)
        tables_first = inspect(engine).get_table_names()
        assert "verification_runs" in tables_first
        assert "source_domains" in tables_first

        # Second initialization should not raise duplicate table error
        init_database(engine_to_use=engine, db_url_to_use=db_url)
        tables_second = inspect(engine).get_table_names()
        assert tables_first == tables_second
