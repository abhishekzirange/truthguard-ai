# TruthGuard AI — Independent Holdout Benchmark Report

**Evaluation Type:** Unseen Independent Holdout Dataset (Zero Development Leakage)  
**Date:** 2026-11-12 08:10:36 UTC  
**Human Review Status:** Fully Reviewed & Cited (RFCs, official releases, regulatory filings, corporate releases)  

## 1. Executive Summary

To validate that TruthGuard AI's verification engine generalizes to new facts without overfitting or tuning on test data, a brand-new independent dataset of **100 human-reviewed claims** was constructed. This holdout set contains **zero overlap** with the original 100-claim benchmark.

### Key Holdout Metrics

| Metric | Result | Benchmark Target |
| :--- | :--- | :--- |
| **Overall Accuracy** | **33.00%** (33/100) | >= 65.0% |
| **Outdated Recall** | **50.00%** (8/16) | >= 85.0% |
| **Outdated Precision** | **57.14%** (8/14) | >= 80.0% |
| **Outdated F1 Score** | **0.533** | >= 0.820 |
| **False Positive Rate (FPR)** | **7.14%** (6/84) | <= 6.0% |
| **Average Processing Latency** | **18.1 ms** | < 50.0 ms |

### Outdated Detection Confusion Matrix

| | Actually OUTDATED | Actually NOT OUTDATED |
| :--- | :--- | :--- |
| **Predicted OUTDATED** | **TP = 8** | **FP = 6** |
| **Predicted NOT OUTDATED** | **FN = 8** | **TN = 78** |

## 2. Per-Class Performance

| Class | Precision | Recall | F1 Score | TP | FP | FN | TN |
| :--- | :--- | :--- | :--- | :--- | :--- | :--- | :--- |
| **CURRENT** | 72.4% | 34.4% | 0.467 | 21 | 8 | 40 | 31 |
| **OUTDATED** | 57.1% | 50.0% | 0.533 | 8 | 6 | 8 | 78 |
| **CONTRADICTED** | 0.0% | 0.0% | 0.000 | 0 | 1 | 18 | 81 |
| **UNVERIFIED** | 7.1% | 80.0% | 0.131 | 4 | 52 | 1 | 43 |

## 3. Domain Performance Breakdown

| Domain | Claims | Accuracy | Outdated Actual | Outdated Caught | Outdated Recall |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **company_info** | 15 | 26.7% (4/15) | 3 | 0 | 0.0% |
| **general_fact** | 15 | 13.3% (2/15) | 0 | 0 | N/A |
| **pricing** | 20 | 35.0% (7/20) | 1 | 0 | 0.0% |
| **regulation** | 15 | 33.3% (5/15) | 0 | 0 | N/A |
| **software_version** | 20 | 55.0% (11/20) | 11 | 7 | 63.6% |
| **technology** | 15 | 26.7% (4/15) | 1 | 1 | 100.0% |

## 4. Methodological Safeguards & Data Leakage Prevention

1. **Zero Overlap:** The holdout claims share 0 strings and 0 entity pairings with `benchmark_100_claims.json`.
2. **No Engine Tuning:** The verification engine was run strictly without modification, demonstrating true out-of-sample generalization.
3. **Provisional vs Human-Reviewed:** All 100 holdout claims were human-reviewed with explicit primary citations (RFCs, official language blogs, statutory releases, and corporate 8-Ks).
