# TruthGuard AI — Frontend Application

React 19 + TypeScript + Vite single-page interface for **TruthGuard AI** (*Don't Trust. Verify.*).

## Local Development

```bash
npm install
npm run dev
```

Runs the Vite development server at `http://localhost:5173`. By default, API requests target `http://localhost:8000/api/v1` (configurable via `VITE_API_BASE_URL`).

## Checks & Production Build

```bash
# Run linter
npm run lint

# Type-check & build production bundle
npm run build
```

## Key Views

- **`/` (`LandingPage`)**: Problem statement, verification workflow, and sample claim demonstration.
- **`/workspace` (`WorkspacePage`)**: Answer submission form, domain and freshness policy selectors, and live Tavily connectivity badge.
- **`/results/:id` (`ResultsPage`)**: Execution mode banner (`LIVE` vs `OFFLINE`), claim verdicts, reasoning, and evidence-backed corrections.
- **`/evidence/:id` (`EvidenceExplorerPage`)**: Three-column comparison linking claims, retrieved Tavily sources, and mathematical quality scores.
- **`/dashboard` & `/analytics`**: Run telemetry and category breakdown charts.
- **`/history`**: Searchable audit trail of past verification runs.
- **`/settings`**: Integration connectivity diagnostics and configured half-life decay policies.
