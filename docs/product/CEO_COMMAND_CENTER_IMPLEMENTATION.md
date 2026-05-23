# CEO Command Center — Implementation Spec

## Purpose
Give the Dealix founder a single screen to run the company as a 24/7 revenue
factory. One screen → one Top Action → one approval queue → one cash view.

## Rule
The CEO **approves and decides.** The system **prepares and routes.** Every
external-impact action goes through Approval Center. No autonomous external
sends. No bypass.

## Required Panels (15)
1. Top CEO Action — the single most important thing to do now.
2. Revenue Funnel — lead intelligence → payment capture.
3. Approval Inbox — pending approvals waiting on founder.
4. Lead Intelligence — discovered / scored / A-leads today.
5. Outreach Ready — drafts queued for approval.
6. Follow-ups Due — what's due today.
7. Positive Replies — what came back warm.
8. Samples Due — sample delivery queue.
9. Proposals Due — proposals to render and send.
10. Payment Capture — owed / collected / overdue.
11. Delivery Queue — paid customers in flight.
12. Retention Queue — at-risk / due for check-in.
13. Trust Flags — ALLOW · DENY · ESCALATE counters.
14. Worker Health — 24/7 machine status.
15. Cash Snapshot — cash · MRR · pipeline · runway.

## Required Actions (9)
- Approve outreach
- Reject outreach
- Request edit
- Approve proposal
- Push payment
- Trigger sample
- Start delivery
- Ask retainer
- Escalate trust issue

## Frontend
- Route: `apps/web/app/ceo/page.tsx`
- Components: `apps/web/components/ceo/{CEOTopAction,KPIGrid,WorkerHealthSummary}.tsx`
- Styling: existing `.card` / `.grid` / `.kpi` / `.metric-grid` from `apps/web/app/globals.css` (no Tailwind).

## Backend Anchors
- `GET /api/v1/business-now/snapshot` — primary CEO summary source
- `GET /api/v1/founder/dashboard` — founder-facing aggregates
- `GET /api/v1/command-center` — command center
- `GET /api/v1/approvals` — approval inbox
- `GET /api/v1/observability/workers` — worker health
- `GET /api/v1/finance` — cash + MRR + runway
- `GET /api/v1/revenue-pipeline` — pipeline movement

See `docs/api/FRONTEND_API_CONTRACT.md` for the per-panel mapping and gaps.

## Certification Gate
Page is **F1** (buildable) when `npm run build` in apps/web passes. **F2**
when the page exists and the nav loads it. **F3** when each panel has a
documented backend endpoint or a tracked gap. **F5** when the page renders
live data from the API.
