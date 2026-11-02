from typing import Dict, Any, List
from sqlalchemy.orm import Session
from sqlalchemy import func, desc
from app.models import VerificationRun, Claim, ClaimAssessment, ModelUsage


class MetricsService:
    @staticmethod
    def get_dashboard_metrics(db: Session) -> Dict[str, Any]:
        total_runs = db.query(VerificationRun).count()
        total_claims = db.query(Claim).count()

        # Status distribution
        statuses = (
            db.query(Claim.status, func.count(Claim.id))
            .group_by(Claim.status)
            .all()
        )
        status_map = {s: cnt for s, cnt in statuses}
        current_cnt = status_map.get("CURRENT", 0)
        outdated_cnt = status_map.get("OUTDATED", 0)
        contradicted_cnt = status_map.get("CONTRADICTED", 0)
        unverified_cnt = status_map.get("UNVERIFIED", 0)
        time_sensitive_cnt = status_map.get("TIME_SENSITIVE", 0)

        # Average latency
        avg_latency = db.query(func.avg(VerificationRun.execution_time_ms)).scalar() or 0.0

        # Average freshness score
        avg_freshness = db.query(func.avg(ClaimAssessment.freshness_score)).scalar()

        # Token usage & cost
        tokens_in = db.query(func.sum(ModelUsage.input_tokens)).scalar() or 0
        tokens_out = db.query(func.sum(ModelUsage.output_tokens)).scalar() or 0
        total_cost = db.query(func.sum(ModelUsage.estimated_cost)).scalar() or 0.0

        # Category distribution
        categories = (
            db.query(Claim.category, func.count(Claim.id))
            .group_by(Claim.category)
            .all()
        )
        cat_metrics = []
        for cat, cnt in categories:
            outdated_in_cat = (
                db.query(Claim)
                .filter(Claim.category == cat, Claim.status == "OUTDATED")
                .count()
            )
            cat_metrics.append({
                "category": cat,
                "count": cnt,
                "outdated_count": outdated_in_cat
            })

        # Recent Problematic claims
        problem_claims = (
            db.query(Claim)
            .filter(Claim.status.in_(["OUTDATED", "CONTRADICTED"]))
            .order_by(desc(Claim.created_at))
            .limit(10)
            .all()
        )
        recent_problems = []
        for c in problem_claims:
            recent_problems.append({
                "claim_text": c.claim_text,
                "status": c.status,
                "category": c.category,
                "verdict_reasoning": c.assessment.reasoning if c.assessment else "Superseded or contradicted by current sources.",
                "suggested_correction": c.assessment.suggested_correction if c.assessment else None,
                "created_at": c.created_at.isoformat()
            })

        return {
            "total_runs": total_runs,
            "total_claims": total_claims,
            "outdated_claims": outdated_cnt,
            "contradicted_claims": contradicted_cnt,
            "unverified_claims": unverified_cnt,
            "current_claims": current_cnt,
            "average_latency_ms": round(float(avg_latency), 1),
            "average_freshness_score": round(float(avg_freshness), 1) if avg_freshness is not None else None,
            "total_input_tokens": int(tokens_in),
            "total_output_tokens": int(tokens_out),
            "estimated_total_cost_usd": round(float(total_cost), 4),
            "status_distribution": {
                "current": current_cnt,
                "outdated": outdated_cnt,
                "contradicted": contradicted_cnt,
                "unverified": unverified_cnt,
                "time_sensitive": time_sensitive_cnt,
            },
            "category_distribution": cat_metrics,
            "recent_problematic_claims": recent_problems,
        }

