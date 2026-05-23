# Founder Console v1

## Purpose

Give the founder one internal console to operate Dealix as a 24/7 revenue
company. The console **shows decisions**, not raw files. Every page reads
from `/api/v1/internal/founder/*` through the single adapter at
`apps/web/lib/dealix-runtime.ts`. Backend access is gated by
`require_super_admin`.

## Scope of v1

Phase 1 (this version) is **read-only**. The console renders KPI tiles,
queues, and health summaries. No external-impact action can be triggered
from any page. Phase 3 of `docs/runtime/FOUNDER_CONSOLE_RUNTIME_BINDING_PLAN.md`
introduces controlled actions through the existing `dealix/trust/`
ApprovalCenter and PolicyEvaluator.

## Pages

| Route | Purpose |
|-------|---------|
| `/ceo` | Top CEO action, company status, revenue snapshot, trust flags, worker health |
| `/sales-cockpit` | Lead intelligence, approved outreach, sent outreach, replies, samples, proposals, payment capture |
| `/approvals` | A1/A2/A3 actions requiring review. Wraps existing `OversightQueue` + `ApprovalDecisionModal` |
| `/workers` | Runtime worker status, failures, last run, backlog |
| `/trust` | Suppression, approval breaches, overclaim risks, AI eval status, incidents |
| `/finance` | Cash, MRR, pipeline, weighted pipeline, payment follow-ups, expenses |
| `/distribution` | Channel performance, sector performance, experiments, double-down decisions |
| `/delivery` | Paid or approved delivery queue, QA, handoff, client feedback |
| `/retention` | Health score, retainer ask, renewal, referral, expansion |
| `/proof` | Approved proof, anonymized proof, case study candidates, proof-to-demand assets |

## Layout

Every page renders through the shared `FounderShell` server component
(`apps/web/components/founder-shell.tsx`). The shell provides a sidebar
with the 10 routes above and a main content area.

```
+-------------------+-------------------------------------+
| Dealix Founder    | <page title>                        |
| ---               |                                     |
| CEO               |  <page content cards>               |
| Sales             |                                     |
| Approvals         |                                     |
| Workers           |                                     |
| Trust             |                                     |
| Finance           |                                     |
| Distribution      |                                     |
| Delivery          |                                     |
| Retention         |                                     |
| Proof             |                                     |
+-------------------+-------------------------------------+
```

## Styling

The console **does not** use Tailwind. It uses the project's existing
custom CSS in `apps/web/app/globals.css`, including:

- `.card` — white card with 1px border and 12px radius
- `.grid` — display grid with 16px gap
- `.founder-shell`, `.founder-sidebar`, `.founder-nav`, `.founder-main` —
  added for the console shell
- `.kpi`, `.kpi-value`, `.muted` — small additions for KPI tiles

No new dependencies. No PostCSS changes. No design system migration.

## Data flow

```
+---------------------+      safeGet<T>()      +-------------------------------+
| Next.js page (RSC)  | --------------------> | /api/v1/internal/founder/...  |
|                     |   fallback on error    |                               |
+---------------------+                         +-------------------------------+
                                                          |
                                                          v
                                                require_super_admin
                                                          |
                                                          v
                                                placeholder JSON
                                                (Phase 1 returns
                                                 static shapes;
                                                 Phase 2 wires real
                                                 data sources)
```

All pages are server components. Network calls go through
`safeGet<T>(path, fallback)` so a 401/403 (expected during local browser
dev where no super-admin token is sent) renders the fallback instead of
crashing the page.

## Non-goals for v1

- No Tailwind
- No client-side state library
- No mobile-first redesign of existing pages (`/control-plane`, `/agents`, `/safety`, etc. remain untouched)
- No SaaS dashboard for external customers
- No marketing pages
- No POST/PATCH endpoints — all interactions are read-only
- No real Trust Plane enforcement on action buttons (Phase 3)

## Rule

Founder Console shows decisions, not raw files.
