# Founder Console v1

## Purpose

The Founder Console is the single screen where Sami runs the company.
v1 is the read-only layout: 10 pages that map to the operating loops of
Dealix and pull from the internal API layer.

v2 (this branch) adds the runtime layer — internal endpoints, action
buttons, source-of-truth map, verifier, and CI gate. See:

- `docs/api/INTERNAL_API_LAYER_V1.md`
- `docs/frontend/APPROVAL_ACTION_FLOW.md`
- `docs/runtime/FOUNDER_CONSOLE_SOURCE_OF_TRUTH.md`
- `docs/frontend/FOUNDER_CONSOLE_PRODUCTION_GATE.md`

## Pages

| Route | Purpose |
| --- | --- |
| `/ceo` | One top action + headline counters |
| `/sales-cockpit` | Funnel-stage counters and lead pipeline |
| `/approvals` | Approve, reject, edit, escalate, defer |
| `/workers` | Worker health snapshots |
| `/trust` | Open trust flags and policy outcomes |
| `/finance` | Cash, MRR, pipeline, follow-ups |
| `/distribution` | Channels, sectors, experiments |
| `/delivery` | Active delivery queue |
| `/retention` | Renewal + churn risk queue |
| `/proof` | Proof library (case studies, evidence) |

## Layout

All pages render inside `<FounderShell>` (in `apps/web/components/founder-shell.tsx`).
The shell provides the page chrome + nav rail and is the only place that
should hard-code the route list.

## Data Flow

```
React server component
  → lib/dealix-runtime.ts (typed fetchers)
  → /api/v1/internal/* (FastAPI)
  → source-of-truth worker / queue / table
```

Action buttons use `lib/dealix-actions.ts` which POSTs to the same
internal API. The frontend never writes directly to the database and
never calls external services itself.

## Rules

- Numbers shown in the UI must come from a documented internal endpoint,
  not hard-coded in the page.
- Action buttons must pass through the Trust Plane on the backend.
- Every page must declare its source in the source-of-truth map.
- A `npm run build` failure on `apps/web` blocks merging via the
  `Dealix Founder Console v2 Checks` workflow.
