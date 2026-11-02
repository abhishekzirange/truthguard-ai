from typing import List, Optional
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app.models import VerificationRun, Claim


class HistoryService:
    @staticmethod
    def get_runs(db: Session, skip: int = 0, limit: int = 50) -> List[dict]:
        runs = (
            db.query(VerificationRun)
            .order_by(desc(VerificationRun.created_at))
            .offset(skip)
            .limit(limit)
            .all()
        )
        results = []
        for r in runs:
            summary = r.summary or {}
            results.append({
                "id": r.id,
                "original_answer": r.original_answer,
                "domain": r.domain,
                "freshness_policy": r.freshness_policy,
                "verification_status": r.verification_status,
                "execution_time_ms": r.execution_time_ms,
                "total_claims": summary.get("total_claims", len(r.claims)),
                "outdated_count": summary.get("outdated_claims", 0),
                "current_count": summary.get("current_claims", 0),
                "contradicted_count": summary.get("contradicted_claims", 0),
                "created_at": r.created_at,
                "completed_at": r.completed_at,
            })
        return results

    @staticmethod
    def get_run_by_id(db: Session, run_id: str) -> Optional[VerificationRun]:
        return db.query(VerificationRun).filter(VerificationRun.id == run_id).first()
