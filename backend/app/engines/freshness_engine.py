import math
from datetime import datetime, timezone
from typing import Optional, Dict, Any, List
from app.engines.classification_engine import CATEGORY_HALF_LIVES


class FreshnessEngine:
    """
    Implements deterministic freshness and evidence quality scoring algorithms.
    """
    POLICY_MULTIPLIERS = {
        "strict": 0.5,
        "standard": 1.0,
        "relaxed": 1.5,
    }

    @classmethod
    def calculate_freshness(
        cls,
        evidence_date: Optional[datetime],
        category: str = "general_fact",
        policy: str = "standard",
        current_time: Optional[datetime] = None
    ) -> Optional[float]:
        """
        Calculates Freshness = 100 * 2^(-age_days / half_life_days).
        Returns None if evidence_date is unknown.
        """
        if not evidence_date:
            return None

        if current_time is None:
            current_time = datetime.now(timezone.utc)

        # Ensure timezone awareness
        if evidence_date.tzinfo is None:
            evidence_date = evidence_date.replace(tzinfo=timezone.utc)
        if current_time.tzinfo is None:
            current_time = current_time.replace(tzinfo=timezone.utc)

        age_seconds = (current_time - evidence_date).total_seconds()
        age_days = max(0.0, age_seconds / 86400.0)

        base_half_life = CATEGORY_HALF_LIVES.get(category, CATEGORY_HALF_LIVES["general_fact"])
        multiplier = cls.POLICY_MULTIPLIERS.get(policy.lower(), 1.0)
        effective_half_life = base_half_life * multiplier

        freshness = 100.0 * math.pow(2.0, -age_days / effective_half_life)
        return round(max(0.0, min(100.0, freshness)), 1)

    @classmethod
    def calculate_evidence_quality(
        cls,
        source_reliability: float,  # S in [0.0, 1.0]
        relevance_score: float,     # R in [0.0, 1.0]
        freshness_score: Optional[float]  # F in [0.0, 100.0] or None
    ) -> float:
        """
        Calculates Evidence Quality = 100 * (0.45*S + 0.35*R + 0.20*(F/100)).
        Uses neutral baseline (50.0) for F if freshness is unknown.
        """
        s = max(0.0, min(1.0, source_reliability))
        r = max(0.0, min(1.0, relevance_score))
        f = freshness_score if freshness_score is not None else 50.0
        f_norm = max(0.0, min(1.0, f / 100.0))

        quality = 100.0 * (0.45 * s + 0.35 * r + 0.20 * f_norm)
        return round(max(0.0, min(100.0, quality)), 1)

    @classmethod
    def aggregate_scores(
        cls,
        evidence_items: List[Dict[str, Any]],
        category: str,
        policy: str
    ) -> tuple[Optional[float], float]:
        """
        Computes aggregate freshness and evidence quality across multiple evidence items.
        """
        if not evidence_items:
            return None, 20.0

        freshness_scores = []
        quality_scores = []

        for item in evidence_items:
            f_score = cls.calculate_freshness(
                item.get("published_at"),
                category=category,
                policy=policy
            )
            q_score = cls.calculate_evidence_quality(
                item.get("source_reliability_score", 0.5),
                item.get("relevance_score", 0.5),
                f_score
            )
            if f_score is not None:
                freshness_scores.append(f_score)
            quality_scores.append(q_score)

        avg_freshness = round(sum(freshness_scores) / len(freshness_scores), 1) if freshness_scores else None
        avg_quality = round(sum(quality_scores) / len(quality_scores), 1) if quality_scores else 50.0

        return avg_freshness, avg_quality
