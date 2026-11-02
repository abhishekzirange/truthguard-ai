# TruthGuard AI — Verification & Contradiction Engine

## 1. Verdict Taxonomy
Every extracted claim is assigned one of five strict statuses:

| Verdict | Definition | Example |
| :--- | :--- | :--- |
| **CURRENT** | Supported by reliable, up-to-date evidence with no material newer contradiction. | "PostgreSQL supports JSONB indexing." |
| **OUTDATED** | The claim was previously true or valid, but authoritative newer evidence shows it has been superseded. | "Python 3.11 is the latest stable Python release." (Superseded by Python 3.12 / 3.13) |
| **CONTRADICTED**| Direct, factual conflict with retrieved evidence regardless of time or versions. | "FastAPI is a PHP framework." or "OpenAI API token price is $50 per token." |
| **UNVERIFIED** | Insufficient credible evidence found to confirm or refute the claim. | "Startup X will acquire Company Y next quarter." |
| **TIME_SENSITIVE**| Claim's validity depends on an unspecified timeframe, date anchor, or ephemeral context. | "Interest rates are currently at an all-time low." |

## 2. Hybrid Verification Architecture
TruthGuard AI does not rely exclusively on LLM prompts for reasoning. It combines:
1. **Deterministic Rule Engines** for precision engineering (SemVer, Numeric, Date).
2. **Neural Reasoning (via Bifrost AI Gateway)** for semantic understanding, contextual nuance, and claim decomposition.

```
                  ┌────────────────────────┐
                  │    Extracted Claim     │
                  └───────────┬────────────┘
                              │
                  ┌───────────▼────────────┐
                  │   Category Detection   │
                  └───────────┬────────────┘
                              │
        ┌─────────────────────┴─────────────────────┐
        ▼                                           ▼
[Version / Price / Date Claim]             [Semantic / Fact Claim]
        │                                           │
┌───────▼──────────────────────┐            ┌───────▼──────────────────────┐
│ Deterministic Checks Engine  │            │ Bifrost LLM Structured Eval │
│ • SemVer comparison          │            │ • JSON schema validation     │
│ • Numeric price delta        │            │ • Evidence ID linking        │
│ • Date interval check        │            │ • Contradiction reasoning    │
└───────┬──────────────────────┘            └───────┬──────────────────────┘
        │                                           │
        └─────────────────────┬─────────────────────┘
                              │
                  ┌───────────▼────────────┐
                  │ Consensus Arbitrator   │
                  │ Final Verdict + Reason │
                  │ + Suggested Correction │
                  └────────────────────────┘
```

## 3. Deterministic Algorithms

### Semantic Version Comparison
- Extracts software name and version tokens (e.g., `3.11`, `0.100.0`, `v2.4.1`).
- Uses PEP 440 and SemVer standard parsers (`packaging.version.Version`).
- Compares claimed version $V_{claim}$ against highest authoritative release version $V_{current}$ discovered in official repositories (PyPI, GitHub releases, docs):
  - If $V_{claim} < V_{current}$, and the claim asserts "latest", "current", or "newest": status is **OUTDATED**; suggested correction specifies $V_{current}$.
  - If $V_{claim} == V_{current}$: status is **CURRENT**.
  - If $V_{claim}$ does not exist or invalid: **CONTRADICTED** or **UNVERIFIED**.

### Pricing Checks
- Normalizes currency and numeric values.
- If claimed price differs from official manufacturer/API tier documentation by more than threshold $\delta > 0.01$, flag as **CONTRADICTED** or **OUTDATED** depending on date of pricing update.

### Prompt Injection Shield
Retrieved evidence texts are treated as **Untrusted Data Payloads**. They are strictly wrapped in XML data wrappers `<evidence_data id="..."></evidence_data>` and filtered for adversarial prompt override keywords (`"ignore previous instructions"`, `"system prompt"`, `"you are now"`). The LLM is constrained to output solely validated JSON with real referenced evidence IDs.
