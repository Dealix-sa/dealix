# Frontend Certification System

## Purpose
Certify that the Dealix frontend is real, buildable, connected, useful, and
safe. Each level is a hard gate.

## Levels

### F0 — Missing
No frontend app or routes exist.

### F1 — Buildable
- `npm install` (or `npm ci`) and `npm run build` pass in `apps/web`.
- CI workflow `dealix-frontend.yml` runs on every PR and main push.

### F2 — Route Complete
- All P0 founder routes exist (`/ceo`, `/sales-cockpit`, `/approvals`,
  `/distribution`, `/workers`, `/trust`, `/finance`).
- `scripts/verify_frontend_api_contract.py` exits 0.
- Each page renders without runtime error in `next start`.

### F3 — API Contracted
- Every page panel maps to a backend endpoint in
  `docs/api/FRONTEND_API_CONTRACT.md`, or to a tracked gap.
- `lib/api.ts` and `lib/types.ts` cover the contract types.
- Gaps list is shorter than 5 items.

### F4 — Quality Checked
- Lighthouse on landing P0 pages passes the thresholds in `lighthouserc.js`
  (performance ≥ 0.75, accessibility ≥ 0.85, SEO ≥ 0.85).
- Pa11y passes WCAG 2.1 AA (advisory mode during ramp-up).
- No `console.error` on page load.

### F5 — Operational
- Each founder page reads **live** data from the API (no `// TODO: live wire`).
- Approval actions (approve / reject / edit) commit through
  `/api/v1/approvals` and update audit sink.
- At least one external action has been gated and approved end-to-end.

## Rule
- Dealix frontend is not "production-ready" until **F1 + F2 + F3** pass.
- F4 and F5 unlock after the first paying customer cycle.
- Every PR that touches `apps/web/` must keep F1 + F2 green.

## Current state (2026-05)
- F1 ✅ once `dealix-frontend.yml` is wired and green
- F2 ✅ this PR adds the 7 founder routes
- F3 🚧 contract written; gaps tracked in `FRONTEND_API_CONTRACT.md`
- F4 ⏳ landing covered by `lighthouse_ci.yml`; founder apps/web not yet
- F5 ⏳ requires live API wiring

## How to certify locally
```bash
make frontend-routes        # regenerate generated inventory
make frontend-certify       # contract + generated inventory + npm build
```
