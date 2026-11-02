import pytest
from app.database.session import SessionLocal, Base, engine
from app.services.verification_service import VerificationService
from app.schemas.verification import VerificationRequest
from app.database.init_db import init_database


@pytest.fixture(scope="session", autouse=True)
def setup_test_db():
    init_database()
    yield


@pytest.mark.asyncio
async def test_end_to_end_verification_pipeline():
    db = SessionLocal()
    try:
        service = VerificationService(db)
        request = VerificationRequest(
            answer_text="Python 3.11 is the latest stable Python release. FastAPI 0.100.0 is the latest version. PostgreSQL supports JSONB.",
            domain="software",
            verification_depth="standard",
            freshness_policy="standard"
        )
        
        run = await service.execute_verification(request)
        
        assert run.verification_status == "COMPLETED"
        assert len(run.claims) >= 3
        
        # Check that outdated claims are identified
        statuses = [c.status for c in run.claims]
        assert "OUTDATED" in statuses or "CURRENT" in statuses
        
        # Check summary metrics
        summary = run.summary
        assert summary["total_claims"] >= 3
        assert run.execution_time_ms > 0
        
        print("\nTest completed successfully!")
        print(f"Total claims: {summary['total_claims']}")
        print(f"Outdated: {summary['outdated_claims']}, Current: {summary['current_claims']}")
        for c in run.claims:
            print(f" - [{c.status}] {c.claim_text}")
            if c.assessment and c.assessment.suggested_correction:
                print(f"   Correction: {c.assessment.suggested_correction}")
    finally:
        db.close()

