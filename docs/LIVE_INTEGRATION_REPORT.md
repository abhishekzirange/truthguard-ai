# TruthGuard AI — Live Integration & Architecture Audit Report

**Date:** March 2026 / Hackathon Phase 2  
**Component Scope:** Tavily Search Adapter, Bifrost AI Gateway Adapter, Verification Service Engine  
**Status:** Hardened, Tested (13 Live-Transition Tests Passing), Operational  

---

## 1. Executive Summary

TruthGuard AI has transitioned from an offline deterministic architecture to a multi-tiered execution engine supporting **LIVE**, **PARTIAL**, and **OFFLINE** modes.

The integration layer enforces strict rules against silent fallbacks and fabricated provenance:
- **LIVE Mode:** Only declared when **both** Tavily Search (HTTP 200) and Bifrost AI Gateway (HTTP 200) succeed. Provenance: `LIVE_TAVILY_BIFROST`.
- **PARTIAL Mode:** Declared when exactly one external integration succeeds (e.g. Tavily search succeeds but Bifrost times out, or Bifrost succeeds against cached/local evidence). Records explicit failure diagnostics. Provenance: `PARTIAL_TAVILY_ONLY` or `PARTIAL_BIFROST_ONLY`.
- **OFFLINE Mode:** Declared when neither external API is active (e.g. unconfigured keys or offline benchmark runs). Relies on deterministic SemVer parsing (PEP 440), pattern consensus, and verified offline corpus. Provenance: `OFFLINE_DETERMINISTIC` or `OFFLINE_LOCAL`.

---

## 2. Tavily Search Integration Audit

### 2.1 Authentication & Configuration
- **Endpoint:** `POST https://api.tavily.com/search`
- **Key Injection:** JSON payload `{"api_key": "..."}`
- **Security Check:** API key is loaded server-side from environment (`TAVILY_API_KEY`). Never forwarded to or exposed in the frontend client.

### 2.2 Request & Response Schemas
- **Request Payload:**
  ```json
  {
    "api_key": "tvly-...",
    "query": "Python latest stable release documentation",
    "search_depth": "basic",
    "include_answer": false,
    "include_domains": [],
    "exclude_domains": [],
    "max_results": 5
  }
  ```
- **Response Validation:** Validated against `isinstance(data.get("results"), list)`.

### 2.3 Resiliency, Timeouts & Rate Limits
- **Network Timeout:** Configured with strict 10.0-second timeout via `httpx.AsyncClient(timeout=10.0)`.
- **Rate-Limit (HTTP 429) & Server Error (HTTP 5xx) Policy:**
  - Automated retry with exponential backoff: `attempt * 0.5s`.
  - Max retries: 2.
  - If rate limit persists: Returns structured dictionary `{"is_live": False, "live_success": False, "error_type": "TAVILY_RATE_LIMIT", "error": "Tavily API Rate Limit Exceeded (HTTP 429)"}`.
- **Unauthorized (HTTP 401):** Fails fast without retrying. Returns `TAVILY_AUTH_ERROR`.

### 2.4 External URL Security & Date Normalization
- **Scheme Whitelist:** Only `http` and `https` schemes are accepted. Any `javascript:`, `data:`, `file:`, or malformed URLs are strictly discarded.
- **Hostname Validation:** Requires non-empty, valid hostnames with standard TLDs.
- **Date Normalization:** ISO 8601 strings parsed safely via `datetime.fromisoformat`. **Missing dates remain `None`**; the engine strictly prohibits fabricating artificial publication dates.

---

## 3. Bifrost AI Gateway Integration Audit

### 3.1 Authentication & Configuration
- **Endpoint:** `POST {BIFROST_BASE_URL}/chat/completions` (OpenAI-compatible gateway interface)
- **Authentication:** HTTP Header `Authorization: Bearer {BIFROST_API_KEY}`
- **Model:** `gpt-4o-mini` (configurable via `BIFROST_MODEL_NAME`)
- **Direct Provider Bypass Prevention:** All model inference calls must pass through the configured Bifrost Gateway URL (`settings.BIFROST_BASE_URL`). Direct provider endpoints (e.g. api.openai.com) are disallowed when Bifrost is enabled.

### 3.2 Structured JSON Schema & Markdown Fence Recovery
LLMs frequently wrap JSON responses in markdown fences (e.g., ````json { ... } ````). The Bifrost adapter implements `_clean_and_parse_json`:
```python
@staticmethod
def _clean_and_parse_json(text: str) -> Optional[Dict[str, Any]]:
    # Strips ```json ... ``` codeblocks and cleans whitespace
    cleaned = re.sub(r"^```(?:json)?\s*", "", text.strip(), flags=re.MULTILINE)
    cleaned = re.sub(r"```$", "", cleaned.strip(), flags=re.MULTILINE).strip()
    return json.loads(cleaned)
```
- If JSON parsing fails: Returns `{"success": False, "error_type": "BIFROST_INVALID_JSON_RESPONSE", "error": "Bifrost output could not be parsed as valid JSON"}`.

### 3.3 Token Usage & Cost Accounting
- The adapter extracts token telemetry from the standard gateway response:
  ```python
  usage = resp_data.get("usage", {})
  input_tokens = usage.get("prompt_tokens", 0)
  output_tokens = usage.get("completion_tokens", 0)
  ```
- Every verification run records input tokens, output tokens, model identifier, and cost directly in the `model_usages` table.

---

## 4. Execution Mode State Transitions

The table below illustrates how the verification engine dynamically and safely transitions between execution modes:

| Scenario | Tavily Status | Bifrost Status | Execution Mode | Claim Provenance | Fallback Strategy |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **All Systems Operational** | HTTP 200 OK | HTTP 200 OK | `LIVE` | `LIVE_TAVILY_BIFROST` | Live evidence analyzed by LLM consensus |
| **Bifrost Fails (429/500/Timeout)** | HTTP 200 OK | Failed / Timeout | `PARTIAL` | `PARTIAL_TAVILY_ONLY` | Live evidence evaluated via deterministic SemVer / pattern consensus |
| **Tavily Fails (429/500/Timeout)** | Failed / Timeout | HTTP 200 OK | `PARTIAL` | `PARTIAL_BIFROST_ONLY` | Local/cached evidence evaluated via live Bifrost LLM gateway |
| **No API Keys Configured** | Unconfigured | Unconfigured | `OFFLINE` | `OFFLINE_DETERMINISTIC` / `OFFLINE_LOCAL` | Deterministic PEP 440 comparison & offline corpus |

---

## 5. Evidence Quality & Data Integrity Guarantees

For every claim verified by the platform, the database captures:
1. `claim_text`: Original AI statement.
2. `verification_query`: Targeted, disambiguated search query.
3. `source_title`: Verified title of publication.
4. `source_url`: Normalized, safe HTTPS URL.
5. `source_domain`: Extracted domain name.
6. `published_at`: Canonical ISO publication timestamp, or `None` if absent.
7. `retrieved_at`: UTC retrieval timestamp.
8. `content_snippet`: Verbatim authoritative text excerpt.
9. `source_reliability_score`: Domain authority score (0.0 – 1.0).
10. `relevance_score`: Semantic relevance score (0.0 – 1.0).
11. `freshness_score`: Exponential decay score $S_f(t) = e^{-\lambda \Delta t}$.
12. `evidence_quality_score`: Corroboration and domain quality metric.
13. `status`: `CURRENT`, `OUTDATED`, `CONTRADICTED`, `UNVERIFIED`.
14. `reasoning` and `provenance`: Transparent audit chain.

**Integrity Mandate:** No dates, sources, citations, or confidence numbers are fabricated or artificially inflated.

