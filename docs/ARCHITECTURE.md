# TruthGuard AI — System Architecture

## 1. Architectural Overview

TruthGuard AI is structured as a modular FastAPI monolith backed by a React + TypeScript single-page application. The architecture separates **external web retrieval** (Tavily Search API) from **verification evaluation** (deterministic PEP 440 version comparison, numeric price bounds, semantic consensus rules, and exponential freshness decay).

```
┌──────────────────────────────────────────────────────────────┐
│                  React + TypeScript Frontend                 │
│  Landing • Workspace • Results • Evidence Explorer • History │
│           Analytics • Dashboard • Settings                   │
└──────────────────────────────┬───────────────────────────────┘
                               │ REST / JSON (/api/v1)
┌──────────────────────────────▼───────────────────────────────┐
│                     FastAPI Backend                          │
│  • Request Validation (Pydantic v2)                          │
│  • VerificationService Orchestrator                          │
│  • ClaimExtractionEngine (sentence splitting & SPO triples)  │
│  • ClassificationEngine (domain category & sensitivity)      │
│  • QueryPlanner (targeted verification query synthesis)      │
│  • TavilyAdapter (POST /search + URL/SSRF sanitization)      │
│  • ReliabilityEngine (domain authority weighting S)          │
│  • DeterministicEngine (SemVer intent + numeric price logic) │
│  • ClaimVerificationEngine (consensus + reasoning synthesis) │
│  • FreshnessEngine (half-life decay & quality scoring)       │
└───────────────┬─────────────────────────────┬────────────────┘
                │                             │
                ▼                             ▼
┌───────────────────────────┐   ┌──────────────────────────────┐
│     Tavily Search API     │   │  PostgreSQL / SQLite Fallback │
│  Live web evidence fetch  │   │  SQLAlchemy ORM + Alembic    │
└───────────────────────────┘   └──────────────────────────────┘
```

## 2. Backend Module Layout (`backend/app`)

- **`api/v1/endpoints/`**: Route handlers for `/verify`, `/claims`, `/history`, `/metrics`, `/health`, and `/integrations/status`.
- **`core/`**: Typed environment configuration (`config.py`) and untrusted-evidence prompt-injection filtering (`security.py`).
- **`database/`**: SQLAlchemy engine setup (`session.py`) and Alembic-aware initialization + default authoritative domain seeding (`init_db.py`).
- **`models/`**: Eight relational tables tracking runs, extracted claims, evidence snippets, assessments, domain scores, events, usage records, and users.
- **`schemas/`**: Pydantic v2 validation schemas for request bounds and response serialization.
- **`integrations/tavily_adapter.py`**: Async HTTPX client calling `https://api.tavily.com/search` with retries on `429`/`5xx`, response URL scheme validation (`http`/`https` only), in-memory TTL caching, and explicit offline fallback when unconfigured or unreachable. *(Note: `bifrost_adapter.py` remains in the repository as an optional inactive adapter and is not required or enabled in the Tavily-only configuration.)*
- **`engines/`**: Modular claim parsing, classification, query planning, source scoring, deterministic version/price checks, freshness calculation, and verdict synthesis.
- **`services/`**: Database-backed orchestration (`verification_service.py`), run history queries (`history_service.py`), and telemetry aggregation (`metrics_service.py`).

## 3. Data Persistence

Database migrations are managed via **Alembic** (`backend/alembic/versions/`). PostgreSQL 16 is configured for Docker Compose deployments, with automatic SQLite fallback (`sqlite:///./truthguard.db`) for zero-setup local development and automated testing.
