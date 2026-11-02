# TruthGuard AI — Live Benchmark Results

**Status:** `LIVE BENCHMARK NOT RUN`  
**Date:** 2026-11-02 17:34:06 UTC  
**Audit Finding:** LIVE BENCHMARK NOT RUN: Credentials missing or unconfigured in .env (TAVILY_API_KEY is not configured in .env; BIFROST_API_KEY is not configured in .env). Real external API calls were not made.  

## Technical Audit Disclosure

- **Tavily Search API:** Unconfigured (`TAVILY_API_KEY` is empty).
- **Bifrost AI Gateway:** Unconfigured (`BIFROST_API_KEY` is empty).
- **External API Requests Made:** 0
- **External Tokens Billed:** 0
- **Actual External Cost Incurred:** $0.000000 USD

In accordance with hackathon evaluation guidelines and technical integrity standards, offline deterministic results are NEVER fabricated or presented as live external API benchmarks.

To execute the live verification benchmark:
1. Set valid `TAVILY_API_KEY` in `.env`.
2. Set valid `BIFROST_API_KEY` and `BIFROST_BASE_URL` in `.env`.
3. Run: `python backend/scripts/run_benchmark.py --mode live`

For verified offline benchmark metrics (92.0% recall, 85.2% precision, 0.885 F1), see [docs/BENCHMARK_RESULTS.md](BENCHMARK_RESULTS.md).
