# TruthGuard AI — Project Blueprint

## 1. Executive Summary
**Product Name:** TruthGuard AI  
**Tagline:** Don't Trust. Verify.  
**Theme:** Build a Stale-Answer Detector for AI Applications  
**Category:** AI Reliability / AI Answer Verification / Information Freshness Intelligence  

LLMs suffer from knowledge cutoff, hallucination of version numbers, stale pricing, and obsolete regulatory and executive information. TruthGuard AI operates as an autonomous verification layer: given any AI-generated response, it extracts atomic factual assertions, determines their temporal sensitivity, plans and queries Tavily for live authoritative web evidence, invokes Bifrost AI Gateway for structured claim reasoning, runs deterministic comparison engines (semantic versioning, numeric pricing, temporal dates), and computes transparent freshness scores ($Freshness = 100 \times 2^{-\Delta t / t_{half}}$) and evidence quality metrics.

## 2. Key Differentiation
1. **Atomic Claim Extraction:** Decomposes complex prose into independently verifiable subject-predicate-object triples with temporal annotations.
2. **Deterministic + Neural Hybrid:** Version comparison uses semver parsing, price checks use numeric bounds, dates use timeline logic, and nuanced semantic claims use LLM reasoning through Bifrost.
3. **Transparent Evidence Attribution:** Every claim links directly to primary sources (official registries, documentation, gov sites) with exact snippets, publication dates, and reliability rankings.
4. **Prompt Injection Hardened:** All retrieved web text is isolated in strict data payloads and validated against hallucinated evidence IDs.
5. **Explainable Freshness Formula:** Distinguishes between truth, freshness, and evidence quality. Older evidence does not falsely mark stable facts as outdated, while fast-changing claims (pricing, versions) are rigorously evaluated against category half-lives.

## 3. Core Verification Pipeline
```
[User AI-Generated Text]
         │
         ▼
[Input Processing & Sanitization]
         │
         ▼
[Claim Extraction Engine] ───► Structured Atomic Claims (Pydantic)
         │
         ▼
[Claim Classification & Temporal Sensitivity] (High / Medium / Low)
         │
         ▼
[Search Query Planner] ───► Focused Disambiguated Queries
         │
         ▼
[Tavily Search Adapter] ───► Live Web Evidence (with fallback & cache)
         │
         ▼
[Evidence Normalization & Source Reliability Ranking]
         │
         ▼
[Verification & Contradiction Engine] ───► Deterministic (SemVer, Price, Date)
         │                                + Bifrost LLM Structured Reasoning
         ▼
[Freshness & Quality Scoring Engine] ───► Freshness (0-100) + Quality (0-100)
         │
         ▼
[Report & Correction Generator] ───► Structured Verification Run & History
```

## 4. User Personas
- **AI Application Developers:** Test and guardrail prompt outputs in production to prevent user misinformation.
- **Enterprise Researchers & Analysts:** Instantly audit LLM-synthesized market, regulatory, and pricing data.
- **End Users & Judges:** Paste any LLM answer and receive verifiable truth with clickable primary sources.
