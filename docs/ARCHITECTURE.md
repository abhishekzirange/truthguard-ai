# TruthGuard AI — System Architecture

## 1. Architectural Philosophy
TruthGuard AI is engineered as a **Modular Monolith** prioritizing reliability, low latency, and clear separation of concerns. The backend is written in Python (FastAPI, SQLAlchemy, Pydantic v2) and the frontend is an enterprise dark-mode SPA built with React 19, TypeScript, Tailwind CSS, Lucide icons, and Recharts.

```
┌────────────────────────────────────────────────────────┐
│             TruthGuard React / TS Frontend             │
│   Landing • Dashboard • Workspace • Results • History  │
└───────────────────────────┬────────────────────────────┘
                            │ REST / JSON (HTTPX / TanStack Query)
┌───────────────────────────▼────────────────────────────┐
│                  FastAPI Application                   │
│   ┌────────────────────────────────────────────────┐   │
│   │ API Router (/api/v1/verify, /claims, /history)  │   │
│   └───────────────────────┬────────────────────────┘   │
│                           │                            │
│   ┌───────────────────────▼────────────────────────┐   │
│   │ Verification Pipeline Orchestrator             │   │
│   │  • Input Processor & Sanitizer                 │   │
│   │  • Claim Extraction Engine                     │   │
│   │  • Claim Classification & Temporal Analyzer    │   │
│   │  • Search Query Planner                        │   │
│   │  • Evidence Normalization & Source Reliability │   │
│   │  • Hybrid Verification Engine                  │   │
│   │    - Deterministic Engine (SemVer, Price, Date)│   │
│   │    - Bifrost AI Gateway Adapter (LLM Reasoning)│   │
│   │  • Freshness & Evidence Quality Engine         │   │
│   │  • Correction Generator                        │   │
│   └───────────────────────┬────────────────────────┘   │
│                           │                            │
│   ┌───────────────────────┴────────────────────────┐   │
│   │ External Integrations                          │   │
│   │  • Tavily Web Search API (Live Retrieval)      │   │
│   │  • Bifrost AI Gateway (OpenAI-compatible)      │   │
│   │  • PostgreSQL / SQLite Persistence (SQLAlchemy)│   │
│   └────────────────────────────────────────────────┘   │
└────────────────────────────────────────────────────────┘
```

## 2. Component Breakdown

### A. FastAPI Backend Core (`backend/app`)
- **`api/v1`**: API endpoints with request/response schemas, CORS, rate limits, and health checks.
- **`core`**: Configuration (`config.py`), security (`security.py`), and logging.
- **`database`**: Database session factory, base model, Alembic migrations.
- **`models`**: SQLAlchemy relational models (`users`, `verification_runs`, `claims`, `evidence`, `claim_assessments`, `source_domains`, `model_usage`, `verification_events`).
- **`schemas`**: Strict Pydantic v2 schemas for all payloads, ensuring runtime integrity and typed serialization.
- **`integrations`**:
  - `tavily_adapter.py`: HTTPX client querying Tavily `/search` with query refinement, depth selection, domain scoring, deduplication, retry, and mock fallback.
  - `bifrost_adapter.py`: Client for Bifrost AI Gateway, enforcing structured JSON schemas, prompt isolation, retry, token usage and cost accounting.
- **`engines`**:
  - `extraction_engine.py`: Extracts atomic factual claims with subject, predicate, object, category, date/version mentions.
  - `classification_engine.py`: Classifies claims into categories and assigns temporal sensitivity.
  - `query_planner.py`: Generates targeted disambiguated web queries per claim.
  - `reliability_engine.py`: Scores domain authority (official docs vs blogs).
  - `deterministic_engine.py`: Semantic version comparison (`packaging.version`), numeric price bounds, date offsets.
  - `freshness_engine.py`: Implements $Freshness = 100 \times 2^{-\Delta t / t_{half}}$ and Evidence Quality.
  - `verification_engine.py`: Merges deterministic outputs with Bifrost assessment to produce verdicts: `CURRENT`, `OUTDATED`, `CONTRADICTED`, `UNVERIFIED`, `TIME_SENSITIVE`.
  - `report_generator.py`: Assembles full verification summary, statistics, and corrected text.

### B. React Frontend (`frontend/src`)
- **Landing Page**: Enterprise hero, problem statement, interactive feature breakdown, live example.
- **Main Dashboard**: High-level telemetry, run metrics, claim breakdown, problem claim highlights.
- **Verification Workspace**: Input text area, domain picker, depth selector, freshness policy selector, sample presets (e.g., Python 3.11 stale version claim, price changes, API changes), real pipeline progress indicators.
- **Verification Results**: Executive verdict card, claim-by-claim analysis, freshness gauge, evidence quality score, suggested corrections, citations.
- **Evidence Explorer**: Interactive 3-way view (Claim vs Evidence vs Assessment).
- **History**: Searchable and paginated historical verification runs.
- **Analytics**: Recharts visualizations for category distribution, freshness trends, latency, cost.
- **Settings**: Integration diagnostics for Bifrost & Tavily, threshold configurations.

## 3. Data Persistence Design
PostgreSQL 16 relational database with UUID primary keys, foreign key constraints, indexes on verification runs and timestamps, and JSON fields for structured metadata. Includes automatic fallback to SQLite for local lightweight testing if PostgreSQL is not running.

