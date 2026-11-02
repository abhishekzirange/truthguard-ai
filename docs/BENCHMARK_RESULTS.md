# TruthGuard AI — Benchmark Evaluation Report

**Evaluation Mode:** OFFLINE LOCAL DETERMINISTIC & HEURISTIC MODE  
**Date:** 2026-11-02 16:18:49 UTC  

## 1. Classification Metrics (100 Human-Reviewed Claims)

| Metric | Result | Target Benchmark |
| :--- | :--- | :--- |
| **Overall Accuracy** | **57.00%** (57/100) | >= 90.0% |
| **Outdated Detection Recall** | **48.00%** (12/25) | >= 90.0% |
| **Outdated Detection Precision** | **80.00%** | >= 85.0% |
| **F1 Score** | **0.600** | >= 0.880 |
| **False Positive Rate** | **4.00%** (3/75) | <= 5.0% |

### Confusion Matrix (Outdated Detection)

| | Actually OUTDATED | Actually NOT OUTDATED |
| :--- | :--- | :--- |
| **Predicted OUTDATED** | **TP = 12** | **FP = 3** |
| **Predicted NOT OUTDATED** | **FN = 13** | **TN = 72** |

## 2. Latency and Telemetry Audit

### A. Offline Local Processing Latency
- **Local CPU/Database Processing Latency:** 12.5 ms / claim
- **Total Benchmark Runtime (100 Claims):** 1.33 seconds
- **External Network Calls:** 0
- **External Billed Tokens:** 0 input, 0 output
- **Externally Billed Cost:** $0.000000 USD (Offline Local Execution — 0 External Tokens Billed)

### B. Live Verification Telemetry (Network + LLM Gateway Projections)
- **Tavily Web Search Roundtrip:** ~600 ms – 1,200 ms (network bound)
- **Bifrost LLM Inference Gateway:** ~700 ms – 1,500 ms (model inference bound)
- **Total Projected Live Pipeline Latency:** ~1,300 ms – 2,700 ms per claim
- **Projected Live Cost:** ~$0.00015 – $0.00035 USD per claim (at gpt-4o-mini rates of $0.15/1M input, $0.60/1M output)

## 3. Comparison to Unverified AI Baseline

| Metric | Unverified AI Baseline | TruthGuard AI |
| :--- | :--- | :--- |
| **Outdated Detection Recall** | 0.0% (assumes all answers current) | **48.0%** |
| **Hallucination Interception** | None | **Autonomous** |
| **Evidence Transparency** | 0 citations | **100% Primary Citations** |
| **Freshness Explainability** | Black Box | **Exponential Half-Life Model** |
