# TruthGuard AI — Project Engineering & Ownership Guide

This guide explains how **TruthGuard AI** (*Don't Trust. Verify.*) is built, structured, and executed across the backend and frontend. Everything documented here corresponds directly to the implemented code in the repository so you can confidently explain and defend every component during technical reviews.

---

## 1. Overall Architecture

TruthGuard AI uses a two-part web architecture:
1. **Frontend (`frontend/src/`):** A React 19 + TypeScript single-page application built with Vite and Tailwind CSS. It collects user text, polls live integration health, and visualizes claim verdicts, freshness decay gauges, and citations.
2. **Backend (`backend/app/`):** A FastAPI server organized into API endpoints, orchestration services, verification engines, an HTTPX integration adapter for **Tavily Search API**, and SQLAlchemy ORM persistence backed by PostgreSQL or SQLite fallback.

In the **Tavily-only track**, responsibilities are strictly divided:
- **Tavily Search API** retrieves current web evidence (snippets, URLs, publication timestamps, and relevance scores).
- **TruthGuard AI's engines** parse claims, score source authority, apply deterministic version/price/consensus logic, and compute mathematical freshness scores.

*(An optional `BifrostAdapter` class remains in `backend/app/integrations/bifrost_adapter.py` as an inactive module when `BIFROST_API_KEY` is empty; it is not required or used in the Tavily-only setup.)*

---

## 2. Major Modules & Responsibilities

| Directory / File | Responsibility |
| :--- | :--- |
| `backend/app/main.py` | Creates the FastAPI app, configures CORS middleware, registers `/api/v1` routes, and runs `init_database()` during application startup lifespan. |
| `backend/app/core/config.py` | Loads `.env` settings via Pydantic `BaseSettings` (`DATABASE_URL`, `TAVILY_API_KEY`, server host/port, cache TTL, search limits). |
| `backend/app/core/security.py` | Detects prompt-injection patterns in retrieved web snippets (`detect_prompt_injection`) and neutralizes instruction strings (`sanitize_untrusted_text`). |
| `backend/app/database/session.py` | Configures the SQLAlchemy `engine`, `SessionLocal`, and `Base`, with fallback from PostgreSQL to local SQLite if initialization fails. |
| `backend/app/database/init_db.py` | Synchronizes Alembic migrations and seeds `source_domains` with initial authoritative domains (`DEFAULT_AUTHORITATIVE_DOMAINS`). |
| `backend/app/engines/extraction_engine.py` | Splits input text into atomic claims, detects version/date mentions, extracts Subject-Predicate-Object heuristics, and classifies category sensitivity. |
| `backend/app/engines/classification_engine.py` | Assigns one of 10 domain categories (e.g., `pricing`, `software_version`, `regulation`) and maps each to a default decay half-life (`CATEGORY_HALF_LIVES`). |
| `backend/app/engines/query_planner.py` | Converts extracted claim metadata into targeted search queries and preferred authoritative domains. |
| `backend/app/integrations/tavily_adapter.py` | Executes async `POST /search` requests to Tavily, handles retries and TTL caching, validates URLs (`http`/`https` only), and provides offline fallback data when keys are missing or calls fail. |
| `backend/app/engines/reliability_engine.py` | Evaluates source domain authority ($S \in [0.0, 1.0]$) from `KNOWN_DOMAIN_RELIABILITY`, `.gov`/`.edu` TLD rules, and title cues. |
| `backend/app/engines/deterministic_engine.py` | Classifies semantic version intent (`VersionIntent`), compares PEP 440 versions (`packaging.version`), and evaluates numeric pricing ranges. |
| `backend/app/engines/freshness_engine.py` | Implements exponential half-life decay and the weighted evidence quality score across retrieved sources. |
| `backend/app/engines/verification_engine.py` | Coordinates evidence sanitization, deterministic SemVer/price rules, optional LLM fallback, and rule-based semantic consensus (`_heuristic_consensus`). |
| `backend/app/services/verification_service.py` | Orchestrates an entire verification run from database creation to claim iteration, Tavily calls, assessment persistence, and final execution mode labeling. |
| `backend/app/services/history_service.py` | Queries paginated verification runs (`get_runs`) and individual run details (`get_run_by_id`). |
| `backend/app/services/metrics_service.py` | Aggregates total runs, claim status counts, average latency, average freshness, and category breakdowns for the dashboard and analytics views. |

---

## 3. Important Classes & Functions

- **`VerificationService.execute_verification(request)`** (`backend/app/services/verification_service.py`): The main pipeline entry point. Creates a `VerificationRun`, extracts claims, plans queries, calls Tavily per claim, scores sources, runs verification, saves all ORM rows, and assigns `execution_mode`.
- **`ClaimExtractionEngine.extract_claims(text, domain)`** (`backend/app/engines/extraction_engine.py`): Protects version dots (`<DOT>`), splits prose into atomic sentences, parses Subject-Predicate-Object triples (`_parse_spo`), and extracts `mentioned_version` and `mentioned_date`.
- **`QueryPlanner.plan_query(claim)`** (`backend/app/engines/query_planner.py`): Builds search strings tailored to category and intent. When `detect_version_intent` returns `VersionIntent.LATEST_ASSERTION`, it strips the stale version number from the subject (e.g., `"Python 3.11"` $\rightarrow$ `"Python latest stable release version official documentation"`) so search results surface current releases rather than only old docs.
- **`TavilyAdapter.search(query, claim_text, search_depth, max_results)`** (`backend/app/integrations/tavily_adapter.py`): Handles in-memory caching, authenticated HTTPX calls, retries, and `validate_and_sanitize_url`.
- **`DeterministicEngine.detect_version_intent(claim_text)` & `compare_software_versions(...)`** (`backend/app/engines/deterministic_engine.py`): Classifies assertions into `LATEST_ASSERTION`, `HISTORICAL_MILESTONE`, `COMPATIBILITY_ASSERTION`, or `AMBIGUOUS` before comparing PEP 440 versions, while filtering out calendar years, `DD.MM.YYYY` dates, unit values (`42.8 MB`), and identifier numbers (`PEP 664`).
- **`FreshnessEngine.calculate_freshness(...)` & `calculate_evidence_quality(...)`** (`backend/app/engines/freshness_engine.py`): Implements the two scoring formulas.

---

## 4. End-to-End Execution Flow

When a user clicks **Verify Answer** in `WorkspacePage.tsx`:
1. The frontend calls `POST /api/v1/verify` with `{ answer_text, domain, verification_depth, freshness_policy }`.
2. `VerificationService` inserts a `VerificationRun` (`status="PROCESSING"`) and logs a `STAGE_STARTED` event.
3. `ClaimExtractionEngine` splits `answer_text` into atomic claims and assigns `category`, `mentioned_version`, and `mentioned_date`.
4. For each extracted claim:
   - `QueryPlanner.plan_query()` creates a focused search string.
   - `TavilyAdapter.search()` calls Tavily (or falls back offline if unconfigured/errored).
   - `ReliabilityEngine.evaluate_source()` scores each returned URL's domain reliability $S$.
   - `ClaimVerificationEngine.verify_claim()` computes freshness and quality scores, runs `DeterministicEngine` checks if a version or price exists, and otherwise runs `_heuristic_consensus()`.
   - `Claim`, `Evidence`, and `ClaimAssessment` rows are persisted.
5. `VerificationService` determines `run.execution_mode` (`LIVE` vs `OFFLINE` or `PARTIAL`), aggregates summary counts/averages into `run.summary`, marks `COMPLETED`, and returns the full serialized `VerificationRunResponse`.
6. The frontend navigates to `/results/:id` and renders the execution banner, claim cards, and source links.

---

## 5. Tavily API Integration

- **Endpoint:** `POST https://api.tavily.com/search` (configured via `settings.TAVILY_BASE_URL`).
- **Authentication:** Passes `api_key` in the JSON request payload. Never logged or exposed to the frontend.
- **Retry & Timeout:** Up to 2 retries on HTTP `429` or `5xx` responses and request timeouts (15s HTTPX timeout) with short exponential backoff (`0.5s`, `1.0s`).
- **Caching:** Query results (keyed by lowercased query + search depth) are cached in `_SEARCH_CACHE` for `SEARCH_CACHE_TTL_HOURS` (default `24` hours).
- **URL Security Validation (`validate_and_sanitize_url`):** Only `http` and `https` schemes are allowed. Unsafe schemes (`javascript:`, `data:`, `file:`), invalid hostnames, and overly long domains (>253 chars) are rejected before storing `Evidence` or rendering links (`rel="noopener noreferrer"` in React).

---

## 6. Freshness Scoring Formula

`FreshnessEngine.calculate_freshness()` models age decay exponentially:

$$\text{Freshness} = 100 \times 2^{-\frac{\text{age\_days}}{\text{effective\_half\_life}}}$$

where `effective_half_life = CATEGORY_HALF_LIVES[category] * POLICY_MULTIPLIERS[policy]`:

- **Policy multipliers:** `strict = 0.5`, `standard = 1.0`, `relaxed = 1.5`.
- **Base category half-lives (`classification_engine.py`):**
  - `pricing`: 7 days
  - `time_sensitive_news`: 14 days
  - `software_version`, `api_version`: 30 days
  - `regulation`, `company_info`, `statistics`: 90 days
  - `technical_docs`: 180 days
  - `general_technical`: 365 days
  - `general_fact`: 730 days

If an evidence item has `published_at = None`, `calculate_freshness()` returns `None` (never inventing a timestamp), and the UI renders *"Insufficient Date Info"*.

---

## 7. Evidence-Quality Scoring Formula

`FreshnessEngine.calculate_evidence_quality()` computes a 0–100 weighted reliability score per evidence item:

$$\text{Evidence Quality} = 100 \times \left( 0.45 \cdot S + 0.35 \cdot R + 0.20 \cdot \frac{F}{100} \right)$$

- **$S \in [0.0, 1.0]$**: Domain reliability from `ReliabilityEngine` (e.g., `python.org`, `docs.python.org`, `sec.gov` = `1.0`; `reuters.com` = `0.90`; `stackoverflow.com` = `0.65`; unknown sites = `0.50` or `0.85` if title states official documentation).
- **$R \in [0.0, 1.0]$**: Relevance score returned by Tavily.
- **$F \in [0.0, 100.0]$**: Calculated freshness score (defaults to a neutral `50.0` baseline if publication date is `None`).

Scores are averaged across all retrieved evidence items in `FreshnessEngine.aggregate_scores()`.

---

## 8. Verification Verdict Logic

`ClaimVerificationEngine.verify_claim()` evaluates a claim through ordered stages:

1. **Empty Evidence Guard:** If no evidence exists, returns `UNVERIFIED` (evidence quality `15.0`).
2. **Evidence Sanitization:** Scans snippet text for prompt injection and strips HTML/control vectors.
3. **Deterministic Software Version Check (`DeterministicEngine.compare_software_versions`):**
   - If intent is `LATEST_ASSERTION`: compares `v_claim` against the highest valid release version in evidence. Same major.minor line $\rightarrow$ `CURRENT`; strictly older $\rightarrow$ `OUTDATED` (with dynamically generated correction `"<Subject> <latest_ver> is the current release."`).
   - If intent is `HISTORICAL_MILESTONE` (e.g., *"Kubernetes 1.20 deprecated dockershim"*): checks whether evidence confirms the claimed version + keywords $\rightarrow$ `CURRENT` (prevents false outdated alerts).
   - If intent is `COMPATIBILITY_ASSERTION`: confirms compatibility keywords $\rightarrow$ `CURRENT`.
   - If `AMBIGUOUS`: falls through to `UNVERIFIED` or semantic consensus rather than guessing.
4. **Deterministic Price Check (`DeterministicEngine.compare_prices`):** Extracts dollar/currency amounts from evidence (ignoring legacy-price sentences) and flags mismatches as `CONTRADICTED`.
5. **Heuristic Semantic Consensus (`_heuristic_consensus`):** Checks speculation cues (`UNVERIFIED`), terminated merger/year discrepancies/opposition pairs (`CONTRADICTED`), leadership departure/treaty invalidation/EOL markers (`OUTDATED`), and minimum keyword overlap before returning `CURRENT` or `UNVERIFIED`.

Verdict reasoning prefixes (`[LIVE TAVILY DETERMINISTIC]`, `[LIVE TAVILY CONSENSUS]`, `[OFFLINE DETERMINISTIC]`, `[OFFLINE HEURISTIC ANALYSIS]`) always reflect whether live Tavily evidence was used.

---

## 9. Database Schema (8 Relational Tables)

Defined in `backend/app/models/` and migrated via Alembic:

1. **`users`**: `id` (UUID PK), `email` (unique), `created_at`.
2. **`verification_runs`**: `id` (UUID PK), `user_id` (FK), `original_answer`, `domain`, `freshness_policy`, `verification_depth`, `verification_status`, `execution_mode` (`LIVE`, `PARTIAL`, `OFFLINE`), `integration_status` (JSON), `execution_time_ms`, `summary` (JSON), `error_message`, `created_at`, `completed_at`.
3. **`claims`**: `id` (UUID PK), `run_id` (FK cascade), `claim_text`, `subject`, `predicate`, `object`, `category`, `temporal_sensitivity`, `status`, `mentioned_date`, `mentioned_version`, `verification_query`, `extraction_confidence`, `created_at`.
4. **`evidence`**: `id` (UUID PK), `claim_id` (FK cascade), `source_title`, `source_url`, `source_domain`, `content_snippet`, `published_at`, `updated_at`, `retrieved_at`, `relevance_score`, `source_reliability_score`, `source_type`, `relationship_type`.
5. **`claim_assessments`**: `id` (UUID PK), `claim_id` (unique FK cascade), `verdict`, `provenance`, `freshness_score`, `evidence_quality_score`, `reasoning`, `suggested_correction`, `supporting_evidence_ids` (JSON), `contradicting_evidence_ids` (JSON), `missing_information` (JSON), `assessed_at`.
6. **`source_domains`**: `id` (UUID PK), `domain` (unique), `source_type`, `reliability_score`, `category`.
7. **`model_usage`**: `id` (UUID PK), `run_id` (FK cascade), `model`, `provider`, `input_tokens`, `output_tokens`, `estimated_cost`, `latency_ms`, `created_at`. Records `0` tokens and `$0.0` cost in deterministic/Tavily-only runs.
8. **`verification_events`**: `id` (UUID PK), `run_id` (FK cascade), `event_type`, `message`, `created_at`.

---

## 10. API Endpoints (`/api/v1`)

| Method & Route | Purpose |
| :--- | :--- |
| `POST /api/v1/verify` | Executes the full verification pipeline on `VerificationRequest` (`HTTP 201`). |
| `GET /api/v1/verify/{verification_id}` | Returns full `VerificationRunResponse` with nested claims, assessments, and evidence. |
| `GET /api/v1/verify/{verification_id}/claims` | Returns extracted `ClaimResponse` list for a run. |
| `POST /api/v1/verify/batch` | Verifies up to 10 `VerificationRequest` items sequentially. |
| `GET /api/v1/claims/{claim_id}/evidence` | Returns sorted `EvidenceResponse` items for a claim (used by Evidence Explorer). |
| `GET /api/v1/history` | Returns paginated `VerificationRunListItem` list ordered newest-first (`skip`, `limit`). |
| `GET /api/v1/metrics` | Returns aggregated `MetricsResponse` (counts, average latency, freshness, category distribution). |
| `GET /api/v1/integrations/status` | Pings Tavily (`TavilyAdapter.check_health()`), database engine, and returns sanitized diagnostics. |
| `GET /api/v1/health` | Lightweight database readiness probe (`{"status": "online", "database": "healthy"}`). |

---

## 11. Error Handling

- **External API Failures:** `TavilyAdapter` catches `401`/`403` (`TAVILY_AUTH_ERROR`), `429` (`TAVILY_RATE_LIMIT`), `httpx.TimeoutException` (`TAVILY_TIMEOUT`), and HTTP/network errors without crashing. Failures mark `live_success=False`, surface error messages inside `run.integration_status["tavily"]`, and downgrade `execution_mode` to `OFFLINE`.
- **Database Fallback:** `session.py` and `init_db.py` support PostgreSQL cleanly and fall back gracefully to local SQLite if a PostgreSQL server is absent.
- **API Validation:** FastAPI + Pydantic v2 enforce payload bounds (`answer_text` length 5–15,000 characters; `max_length=10` on batch requests) and return `422 Unprocessable Content` for invalid schemas or `404`/`500` with explicit error details.

---

## 12. Testing Approach

- **Automated Test Suite (`backend/tests/`):** 90 pytest cases covering:
  - 20 end-to-end verification scenario cases (`test_all_20_scenarios.py`)
  - Semantic version intent detection (`test_version_intent.py`)
  - URL scheme / hostname security validation (`test_url_security.py`)
  - Ambiguous & conflicting evidence handling (`test_ambiguous_conflicts.py`)
  - Failure resilience, retries, and `LIVE`/`OFFLINE` provenance transitions (`test_live_integrations.py`)
  - Database schema & Alembic migration checks (`test_database_migrations.py`)
  - `conftest.py` clears external keys via an `autouse` fixture so unit tests remain isolated from external network fluctuations.
- **Offline Quantitative Benchmarks (`backend/scripts/`):**
  - `run_benchmark.py` (`benchmark_100_claims.json`): 69% accuracy, 88% outdated recall/precision, 0.880 F1 (measured 2026-11-12).
  - `run_holdout_benchmark.py` (`holdout_100_claims.json`): 33% accuracy, 50% outdated recall, 57.14% precision, 0.533 F1 (measured 2026-11-12).

---

## 13. Known Limitations

- **Live Multi-Claim Benchmark Unmeasured:** Live Tavily accuracy across all 100 claims has not been systematically benchmarked yet; live behavior is demonstrated on selected cases (`Python 3.11 -> 3.15.2`, `Kubernetes 1.20`).
- **Rule-Based Nuance Ceiling:** Complex contradictions phrased outside SemVer, pricing, and semantic regex cues fall back to `UNVERIFIED` in deterministic-only mode.
- **Holdout Generalization Gap:** Unseen holdout claims without live retrieval yield 33% offline accuracy because unknown facts default to `UNVERIFIED`.
- **Snippet & Metadata Limits:** Pages lacking structured publication dates report `published_at = null`, and paywalled URLs limit retrieved content to search snippets.

---

## 14. Important Design Decisions

1. **Retrieval vs. Evaluation Separation:** Tavily is treated strictly as an evidence retriever, not an oracle. Verdicts are derived deterministically from retrieved text so every decision has a reproducible rule path and source URL.
2. **Strict `LIVE` vs. `OFFLINE` Provenance:** The backend and UI refuse to display `LIVE` unless an authenticated live Tavily search actually succeeded for the current run.
3. **Never Fabricate Missing Timestamps:** When retrieved web pages do not provide publication dates, TruthGuard preserves `None` (*Insufficient Date Info*) instead of substituting today's date, avoiding artificially inflated freshness scores.
4. **Intent-Aware SemVer Parsing:** Checking version intent before comparing releases stops historical statements like *"Kubernetes 1.20 deprecated dockershim"* from triggering false-positive outdated alerts.

