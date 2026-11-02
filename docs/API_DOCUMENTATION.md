# TruthGuard AI — REST API Documentation

Base URL: `http://localhost:8000/api/v1`

## 1. Endpoints Overview

| Method | Path | Description |
| :--- | :--- | :--- |
| `POST` | `/verify` | Run verification on an AI-generated answer. |
| `GET` | `/verify/{verification_id}` | Retrieve full status, claims, and assessments for a run. |
| `GET` | `/verify/{verification_id}/claims` | Retrieve claims extracted for a specific run. |
| `GET` | `/claims/{claim_id}/evidence` | Retrieve raw evidence items supporting or contradicting a claim. |
| `POST` | `/verify/batch` | Submit multiple answers for batch verification. |
| `GET` | `/history` | List previous verification runs with pagination. |
| `GET` | `/metrics` | Retrieve aggregated dashboard telemetry and analytics. |
| `GET` | `/health` | Application health and database readiness check. |
| `GET` | `/integrations/status` | Real-time connection diagnostic for Tavily & Bifrost. |

---

## 2. Request & Response Examples

### `POST /api/v1/verify`
**Request Payload:**
```json
{
  "answer_text": "Python 3.11 is the latest stable Python release. FastAPI 0.100.0 is the latest version. PostgreSQL supports JSONB.",
  "domain": "software",
  "verification_depth": "standard",
  "freshness_policy": "standard"
}
```

**Response (200 OK):**
```json
{
  "id": "c8b417c8-724f-4d92-9694-df0a28f8f2b7",
  "original_answer": "Python 3.11 is the latest stable Python release. FastAPI 0.100.0 is the latest version. PostgreSQL supports JSONB.",
  "domain": "software",
  "freshness_policy": "standard",
  "verification_status": "COMPLETED",
  "execution_time_ms": 2150,
  "summary": {
    "total_claims": 3,
    "current_claims": 1,
    "outdated_claims": 2,
    "contradicted_claims": 0,
    "unverified_claims": 0,
    "time_sensitive_claims": 0,
    "overall_freshness_score": 68.4,
    "overall_evidence_quality_score": 88.5
  },
  "claims": [
    {
      "id": "972ba9a1-0f73-4552-b883-8cfb6bf01a33",
      "claim_text": "Python 3.11 is the latest stable Python release.",
      "subject": "Python",
      "predicate": "is latest stable release",
      "object": "3.11",
      "category": "software_version",
      "temporal_sensitivity": "HIGH",
      "verdict": "OUTDATED",
      "freshness_score": 52.1,
      "evidence_quality_score": 92.0,
      "reasoning": "Python 3.12 and 3.13 have been released as official stable versions on python.org.",
      "suggested_correction": "Python 3.12 or 3.13 is the latest stable Python release.",
      "evidence_count": 3
    }
  ],
  "created_at": "2026-11-02T11:45:00Z"
}
```

### `GET /api/v1/integrations/status`
**Response (200 OK):**
```json
{
  "tavily": {
    "configured": true,
    "reachable": true,
    "latency_ms": 142,
    "message": "Connected to Tavily API"
  },
  "bifrost": {
    "configured": true,
    "reachable": true,
    "latency_ms": 185,
    "model": "gpt-4o-mini",
    "message": "Connected to Bifrost Gateway"
  },
  "database": {
    "status": "connected",
    "dialect": "postgresql"
  }
}
```
