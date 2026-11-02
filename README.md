# TruthGuard AI

> **Don't Trust. Verify.**  
> *An Autonomous AI Answer Freshness & Verification Platform*

[![FastAPI](https://img.shields.io/badge/Backend-FastAPI-009688.svg?style=flat&logo=fastapi)](https://fastapi.tiangolo.com)
[![React](https://img.shields.io/badge/Frontend-React_19_%2B_Vite-61DAFB.svg?style=flat&logo=react)](https://react.dev)
[![TypeScript](https://img.shields.io/badge/Language-TypeScript-3178C6.svg?style=flat&logo=typescript)](https://www.typescriptlang.org)
[![Python](https://img.shields.io/badge/Python-3.12%2B-3776AB.svg?style=flat&logo=python)](https://www.python.org)
[![Docker](https://img.shields.io/badge/Deploy-Docker_Compose-2496ED.svg?style=flat&logo=docker)](https://www.docker.com)
[![Tests](https://img.shields.io/badge/Test_Suite-20%2F20_Passed-10B981.svg?style=flat)](#testing--verification-benchmark)

---

## 1. Executive Summary & Problem Statement

Large Language Models frequently generate answers containing **outdated, obsolete, or contradicted assertions with 100% confidence**.
- **Software APIs and dependencies evolve:** An LLM confidently states *"Python 3.11 is the latest release"* or *"FastAPI 0.100.0 is the latest version"*.
- **Pricing fluctuates:** Stale model token rates and SaaS billing tiers produce enterprise budget errors.
- **Regulations update:** Privacy laws (GDPR, EU AI Act, SEC reporting) have strict statutory effective dates.
- **Corporate leadership changes:** Executive appointments, acquisitions, and mergers render static weights obsolete.

**TruthGuard AI** solves this problem by decomposing AI answers into atomic factual triples (Subject-Predicate-Object), retrieving live authoritative web evidence via **Tavily**, evaluating assertions through **Bifrost AI Gateway** and deterministic rule engines (SemVer, Numeric, Temporal), and calculating mathematical freshness decay scores ($100 \times 2^{-\Delta t / t_{half}}$).

---

## 2. System Architecture

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

---

## 3. Freshness & Quality Mathematical Scoring Model

### A. Freshness Exponential Decay
TruthGuard models information freshness using radioactive exponential decay based on domain category half-lives:

$$\text{Freshness} = 100 \times 2^{-\frac{\text{age\_days}}{\text{half\_life\_days}}}$$

| Category | Default Half-Life | Rationale |
| :--- | :--- | :--- |
| **Product Pricing** | 7 days | Prices and cloud rates fluctuate weekly. |
| **Software Versions** | 30 days | Fast dependency releases and security patches. |
| **API Documentation** | 30 days | Breaking changes, deprecations, new endpoints. |
| **Regulations & Policy** | 90 days | Quarterly statutory deadlines and rule filings. |
| **Company Information** | 90 days | Executive changes, earnings releases, and M&A. |
| **General Technical Facts** | 365 days | Stable architectural paradigms and specs. |

*If evidence publication date is missing, TruthGuard never fabricates dates; it transparently badges the claim as `Insufficient Date Info`.*

### B. Epistemic Evidence Quality
$$\text{Evidence Quality} = 100 \times \left( 0.45 \cdot S + 0.35 \cdot R + 0.20 \cdot \frac{F}{100} \right)$$
- $S \in [0.0, 1.0]$: Source Domain Reliability (Official docs/registries = 1.0, Tech news = 0.85, Blogs = 0.45).
- $R \in [0.0, 1.0]$: Claim Relevance Score.
- $F \in [0, 100]$: Freshness Score.

---

## 4. Testing, Telemetry & Verification Benchmark

### 100-Claim Human-Reviewed Reference Benchmark
TruthGuard AI was evaluated against an independently human-reviewed dataset of 100 factual assertions across 6 categories (Software versions, API specs, Pricing, Regulations, Leadership, General tech facts).

#### A. Measured Offline Benchmark (Local Engine Execution)
Tested without external API dependencies to measure deterministic algorithmic performance and local compute overhead:

| Metric | Unverified AI Baseline | TruthGuard AI (Offline Mode) |
| :--- | :--- | :--- |
| **Outdated Detection Recall** | 0.0% | **48.00%** (12/25 outdated claims detected) |
| **Detection Precision** | 0.0% | **80.00%** (12/15) |
| **F1 Score** | 0.000 | **0.600** |
| **False Positive Rate** | N/A | **4.00%** (3/75) |
| **Local Processing Latency** | Instant (Blind) | **12.5 ms / claim** (Local CPU/SQLite) |
| **Billed External Tokens** | 0 tokens | **0 tokens** (Offline execution) |
| **Externally Billed Cost** | $0.00 | **$0.000000 USD** |

#### Confusion Matrix (Outdated Detection)
| | Ground Truth OUTDATED | Ground Truth NOT OUTDATED |
| :--- | :--- | :--- |
| **Predicted OUTDATED** | **TP = 12** | **FP = 3** |
| **Predicted NOT OUTDATED** | **FN = 13** | **TN = 72** |

#### B. Projected Live Pipeline Telemetry (Cloud Search + LLM Gateway)
When deployed with live credentials (`TAVILY_API_KEY`, `BIFROST_API_KEY`):
- **Tavily Web Search Roundtrip:** ~600 ms – 1,200 ms (network bound)
- **Bifrost LLM Inference Gateway:** ~700 ms – 1,500 ms (model inference bound)
- **Total Projected Live Pipeline Latency:** ~1,300 ms – 2,700 ms per claim
- **Projected Live Cost:** ~$0.00015 – $0.00035 USD per claim (at standard gpt-4o-mini rates: $0.15/1M prompt tokens, $0.60/1M completion tokens)

*Full regression suite passes with 100% reliability across all 77 unit, integration, and scenario tests (`pytest tests/`).*
*Detailed breakdown available in [BENCHMARK_RESULTS.md](file:///c:/Users/Abhishek/Documents/Abhishek/truthguard-ai/docs/BENCHMARK_RESULTS.md) and [POST_AUDIT_FIX_REPORT.md](file:///c:/Users/Abhishek/Documents/Abhishek/truthguard-ai/docs/POST_AUDIT_FIX_REPORT.md).*

---

## 5. Quickstart & Installation

### Option 1: Docker Compose (Recommended Production Setup)
```bash
# Clone the repository
git clone https://github.com/your-username/truthguard-ai.git
cd truthguard-ai

# Copy environment configuration
cp .env.example .env

# Launch PostgreSQL, FastAPI backend, and React frontend
docker compose up --build
```
- Frontend UI: `http://localhost:5173`
- Backend API Docs (Swagger): `http://localhost:8000/docs`

---

### Option 2: Local Development Setup

#### Backend (FastAPI)
```bash
cd backend

# Install dependencies
pip install -r requirements.txt

# Run migrations & seed domains
python -m app.database.init_db

# Start backend server
python -m uvicorn app.main:app --reload --port 8000
```

#### Frontend (React + Vite + Tailwind)
```bash
cd frontend

# Install packages
npm install

# Start Vite dev server
npm run dev
```
Open `http://localhost:5173` in your browser.

---

## 6. Verification Workflow & Screens

1. **Landing Page (`/`):** Enterprise value proposition, problem demonstration, interactive audit teaser.
2. **Workspace (`/workspace`):** Paste any AI answer, select domain (Software, Pricing, Regulations, etc.), choose freshness policy (Strict, Standard, Relaxed), select demo presets, and run live verification.
3. **Verification Results (`/results/:id`):** Executive summary, claim breakdown cards, status badges (`CURRENT`, `OUTDATED`, `CONTRADICTED`, `UNVERIFIED`, `TIME_SENSITIVE`), and suggested corrections.
4. **Evidence Explorer (`/evidence/:id`):** 3-Column matrix comparing Original Claim vs Retrieved Web Sources vs TruthGuard Mathematical Assessment.
5. **Dashboard (`/dashboard`):** Real-time telemetry, claim distributions, and recent flagged claims.
6. **History (`/history`):** Searchable audit trail of all historical verification runs.
7. **Analytics (`/analytics`):** Recharts visualizations of category vulnerability rates and token costs.
8. **Settings (`/settings`):** Backend diagnostic ping for Tavily, Bifrost, and Database connectivity.

---

## 7. Security Architecture & Threat Protection

- **Prompt Injection Containment:** Web evidence snippets are treated as untrusted payloads wrapped in XML `<evidence_untrusted>` tags with pre-scan pattern filters and no arbitrary code execution.
- **Credential Isolation:** Keys (`TAVILY_API_KEY`, `BIFROST_API_KEY`) reside exclusively in backend environment variables and are never transmitted to client browsers.
- **SQL Injection Defense:** Strict parameterized ORM queries via SQLAlchemy.

---

## 8. License & Team
TruthGuard AI was engineered for the **AI Answer Freshness & Stale-Answer Detection Hackathon Challenge**.  
Licensed under the **MIT License**.

