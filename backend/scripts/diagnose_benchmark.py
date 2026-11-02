import os
import sys
import json
import asyncio

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from app.database.session import SessionLocal
from app.services.verification_service import VerificationService
from app.schemas.verification import VerificationRequest
from app.database.init_db import init_database


async def diagnose():
    init_database()
    benchmark_file = os.path.join(os.path.dirname(__file__), "..", "tests", "data", "benchmark_100_claims.json")
    with open(benchmark_file, "r", encoding="utf-8") as f:
        claims = json.load(f)

    db = SessionLocal()
    service = VerificationService(db)

    print("Diagnosing mismatches:")
    mismatch_count = 0
    for idx, c in enumerate(claims):
        req = VerificationRequest(answer_text=c["claim_text"], domain=c["category"])
        run = await service.execute_verification(req)
        pred = run.claims[0].status if run.claims else "UNVERIFIED"
        gt = c["ground_truth_verdict"]
        if pred != gt and mismatch_count < 10:
            mismatch_count += 1
            print(f"[{c['id']}] Claim: {c['claim_text']}")
            print(f"   Ground Truth: {gt} | Predicted: {pred}")
            print(f"   Reasoning: {run.claims[0].assessment.reasoning if run.claims and run.claims[0].assessment else 'None'}\n")

    db.close()

if __name__ == "__main__":
    asyncio.run(diagnose())

