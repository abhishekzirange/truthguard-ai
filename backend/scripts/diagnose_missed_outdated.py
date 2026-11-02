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
    with open("tests/data/benchmark_100_claims.json", "r", encoding="utf-8") as f:
        claims = json.load(f)
    db = SessionLocal()
    service = VerificationService(db)
    missed = []
    for c in claims:
        if c["ground_truth_verdict"] == "OUTDATED":
            req = VerificationRequest(answer_text=c["claim_text"], domain=c["category"])
            run = await service.execute_verification(req)
            pred = run.claims[0].status if run.claims else "UNVERIFIED"
            reasoning = run.claims[0].assessment.reasoning if (run.claims and run.claims[0].assessment) else ""
            if pred != "OUTDATED":
                missed.append({
                    "id": c["id"],
                    "claim_text": c["claim_text"],
                    "category": c["category"],
                    "ground_truth": c["ground_truth_verdict"],
                    "predicted": pred,
                    "reasoning": reasoning
                })
    db.close()
    print(f"Total missed outdated claims: {len(missed)}")
    for idx, m in enumerate(missed, 1):
        print(f"{idx}. [{m['id']}] {m['claim_text']}")
        print(f"   Category: {m['category']}")
        print(f"   Predicted: {m['predicted']}")
        print(f"   Reasoning: {m['reasoning']}\n")


if __name__ == "__main__":
    asyncio.run(diagnose())

