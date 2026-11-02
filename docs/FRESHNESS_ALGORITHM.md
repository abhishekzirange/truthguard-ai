# TruthGuard AI — Freshness & Evidence Quality Scoring Algorithm

## 1. Freshness Scoring Formula
TruthGuard AI models information freshness using radioactive exponential decay. The freshness of a piece of retrieved evidence decreases exponentially as the time elapsed between its publication/update and the current verification date increases.

$$\text{Freshness} = 100 \times 2^{-\frac{\text{age\_days}}{\text{half\_life\_days}}}$$

Where:
- $\text{age\_days} = \max(0, (\text{Current Timestamp} - \text{Evidence Timestamp}) \text{ in days})$
- $\text{half\_life\_days}$ is determined by the claim's domain and category.

### Configurable Half-Life Defaults:
| Category | Default Half-Life | Rationale |
| :--- | :--- | :--- |
| **Product Pricing** | 7 days | Prices change weekly or with promotions. |
| **Software Versions** | 30 days | Fast-release cycles and dependency patches. |
| **API Documentation** | 30 days | Breaking changes, deprecations, new endpoints. |
| **Regulations & Policy** | 90 days | Regulatory announcements vs implementation windows. |
| **Company Leadership** | 90 days | Executive changes, board movements, acquisitions. |
| **Statistics & Market Data** | 90 days | Quarterly earnings and economic indicators. |
| **General Technical Facts**| 365 days | Stable architectural paradigms and foundational specs. |
| **General Factual Facts**  | 730 days | Historical and established scientific assertions. |

### Freshness Policy Multipliers:
Users can adjust the verification freshness policy:
- **Strict:** Multiplies half-life by $0.5$ (information ages twice as fast).
- **Standard:** Multiplies half-life by $1.0$ (baseline).
- **Relaxed:** Multiplies half-life by $1.5$ (information tolerated longer).

### Handling Unknown Publication Dates:
If an evidence source does not contain an authoritative publication or update date:
- Freshness is explicitly marked as `null` / `UNKNOWN`.
- The system **never** fabricates a publication date or assumes the retrieval date is the publication date.
- The UI renders an **"Insufficient Date Information"** badge.

---

## 2. Evidence Quality Scoring Formula
Evidence Quality measures the epistemic weight of retrieved sources independently of their temporal freshness. A high-quality source might be older, while a very fresh source might be a low-reliability discussion forum.

$$\text{Evidence Quality} = 100 \times \left( 0.45 \cdot S + 0.35 \cdot R + 0.20 \cdot \frac{F}{100} \right)$$

Where:
- $S \in [0.0, 1.0]$ is the **Source Reliability Score** (domain authority, primary vs secondary source, official docs vs blogs).
- $R \in [0.0, 1.0]$ is the **Claim Relevance Score** (semantic overlap and directness of answer).
- $F \in [0, 100]$ is the **Freshness Score** (or a baseline neutral value of 50 if date is unknown).

### Source Reliability Scoring ($S$):
- **1.00:** Official primary source registry / documentation (e.g., `python.org`, `fastapi.tiangolo.com`, `pypi.org`, `github.com/org/repo/releases`, `.gov`, `.edu`).
- **0.80:** Recognized authoritative news & tech publishers (e.g., `reuters.com`, `bloomberg.com`, `techcrunch.com`).
- **0.60:** Community tech portals (e.g., `stackoverflow.com`, `medium.com`, `dev.to`).
- **0.40:** General secondary web sources.
- **0.20:** Unverified blogs or dynamic social aggregator pages.

---

## 3. Important Epistemic Distinctions
- **Freshness $\ne$ Truth:** A claim can be historically true and perpetually valid (e.g., "PostgreSQL supports JSONB") even if the retrieved supporting documentation is 3 years old.
- **Evidence Quality $\ne$ Truth:** A beautifully written, high-authority document can describe a previous version or repealed law.
- **TruthGuard evaluates:**
  1. Semantic consistency between claim and current evidence.
  2. Temporal precedence (does newer evidence supersede the claim?).
  3. Deterministic boundaries (semver comparison, price difference).
