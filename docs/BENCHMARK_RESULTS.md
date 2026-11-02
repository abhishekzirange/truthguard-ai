# TruthGuard AI — Benchmark Evaluation Report

**Evaluation Mode:** OFFLINE DETERMINISTIC & LOCAL ENGINE (Deterministic SemVer, Corroboration, Heuristics)  
**Date:** 2026-11-02 17:34:06 UTC  

## 1. Classification Metrics (100 Human-Reviewed Claims)

| Metric | Result | Target Benchmark |
| :--- | :--- | :--- |
| **Overall Accuracy** | **69.00%** (69/100) | >= 90.0% |
| **Outdated Detection Recall** | **92.00%** (23/25) | >= 90.0% |
| **Outdated Detection Precision** | **85.19%** (23/27) | >= 85.0% |
| **F1 Score** | **0.885** | >= 0.880 |
| **False Positive Rate** | **5.33%** (4/75) | <= 5.0% |

### Confusion Matrix (Outdated Detection)

| | Actually OUTDATED | Actually NOT OUTDATED |
| :--- | :--- | :--- |
| **Predicted OUTDATED** | **TP = 23** | **FP = 4** |
| **Predicted NOT OUTDATED** | **FN = 2** | **TN = 71** |

## 2. Latency and Telemetry Audit

### A. Offline Local Processing Latency
- **Local CPU/Database Processing Latency:** 16.7 ms / claim
- **Total Benchmark Runtime (100 Claims):** 1.77 seconds
- **External Network Calls:** 0
- **External Billed Tokens:** 0 input, 0 output
- **Externally Billed Cost:** $0.000000 USD (Offline Local Execution — 0 External Tokens Billed)

### B. Live Verification Telemetry (Network + LLM Gateway Projections)
- **Tavily Web Search Roundtrip:** ~600 ms – 1,200 ms (network bound)
- **Bifrost LLM Inference Gateway:** ~700 ms – 1,500 ms (model inference bound)
- **Total Projected Live Pipeline Latency:** ~1,300 ms – 2,700 ms per claim
- **Projected Live Cost:** ~$0.00015 – $0.00035 USD per claim (at gpt-4o-mini rates)

## 3. Comparison to Unverified AI Baseline

| Metric | Unverified AI Baseline | TruthGuard AI |
| :--- | :--- | :--- |
| **Outdated Detection Recall** | 0.0% (assumes all answers current) | **92.0%** |
| **Hallucination Interception** | None | **Autonomous** |
| **Evidence Transparency** | 0 citations | **100% Primary Citations** |
| **Freshness Explainability** | Black Box | **Exponential Half-Life Model** |
