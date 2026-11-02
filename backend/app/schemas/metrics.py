from typing import List, Dict, Any, Optional
from pydantic import BaseModel


class StatusDistribution(BaseModel):
    current: int = 0
    outdated: int = 0
    contradicted: int = 0
    unverified: int = 0
    time_sensitive: int = 0


class CategoryMetric(BaseModel):
    category: str
    count: int
    outdated_count: int


class ProblematicClaim(BaseModel):
    claim_text: str
    status: str
    category: str
    verdict_reasoning: str
    suggested_correction: Optional[str] = None
    created_at: str


class MetricsResponse(BaseModel):
    total_runs: int = 0
    total_claims: int = 0
    outdated_claims: int = 0
    contradicted_claims: int = 0
    unverified_claims: int = 0
    current_claims: int = 0
    average_latency_ms: float = 0.0
    average_freshness_score: Optional[float] = None
    total_input_tokens: int = 0
    total_output_tokens: int = 0
    estimated_total_cost_usd: float = 0.0
    status_distribution: StatusDistribution
    category_distribution: List[CategoryMetric] = []
    recent_problematic_claims: List[ProblematicClaim] = []
