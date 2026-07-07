# Saudi Opportunity Command Room — Master Plan

> Draft-first, approval-guarded. This system scores companies, drafts outreach,
> and produces reports. It **never** sends anything externally.

## One-liner

Dealix builds a **Saudi Opportunity Graph** and a daily command room that turns
market signals into scored companies, partner candidates, approval-ready
outreach drafts, next actions, and weekly proof packs.

## Why this, not "auto-send"

The strongest version is **not** uncontrolled live outbound. It is:

> full automated targeting + full segmentation + full drafting + full reporting
> + full proof pack — **with human approval before any send.**

This protects reputation and legal posture (PDPL, platform terms) while making
Dealix a real daily machine. It extends the existing
`dealix/revenue_ops_autopilot` layer and the AI Outreach Targeting OS rather
than adding scattered tools.

## Target customers

**A. Foreign B2B companies entering Saudi** — SaaS, AI, healthtech, logistics
tech, enterprise software, compliance tools, event/tourism and industrial
suppliers.

**B. Saudi companies needing revenue recovery** — clinics, training centers,
B2B service firms, agencies, legal/accounting offices, logistics, contractors,
local SaaS/tech.

**C. B2G-ready companies** — foreign suppliers, Saudi vendors, consultants, and
enterprise/industrial/health/education/logistics companies needing readiness
support.

## Value proposition

- **Foreign:** "Before you spend heavily on Saudi setup or hiring, get a 14-day
  Saudi Opportunity Command Room: target accounts, partner candidates, fit
  scoring, outreach drafts, B2B/B2G readiness, and a decision memo."
- **Saudi:** "Dealix shows where revenue is leaking — lost follow-ups, scattered
  WhatsApp, stalled proposals, missed next actions — then runs a daily command
  room to recover opportunities."

## The Saudi Opportunity Graph (the moat)

The graph links companies to signals, personas, pains, offers, partner paths,
drafts, evidence, risk, and next actions. Every daily cycle enriches it, so the
competitive advantage compounds over time. It lives in
`dealix/opportunity_graph/` with a JSON store under `data/opportunity_graph/`.

Nodes: `OpportunityCompany`, `OpportunitySignal`, `OutreachDraft`,
`DailyCommandReport`, `ProofPack` (see `schemas.py`).

## Scoring model (deterministic, no paid APIs)

```
total = fit + signal + urgency + value + accessibility - trust_risk
```

Bands: `>=80 hot` · `>=60 warm` · `>=40 research` · `else not_fit`.

Sub-scores are keyword-derived and fully deterministic — the same input always
yields the same output. See `scoring.py`.

## Segments

`foreign_saas_ai_entering_saudi`, `foreign_supplier_needing_distributor`,
`saudi_clinic_revenue_leak`, `saudi_training_or_b2b_service_growth`,
`b2g_readiness_candidate`, `rhq_vendor_or_partner_candidate`,
`event_expo_tourism_supplier`, `not_fit`.

## Daily machine

`collect → normalize → score → segment → draft → approval queue → report`

Run:

```bash
python scripts/commercial/seed_saudi_opportunity_graph.py
python scripts/commercial/run_daily_opportunity_targeting.py --mode draft-only --limit 50
python scripts/commercial/generate_daily_command_report.py --weekly-proof-pack
```

Outputs (all gitignored except the seed CSV):

- `data/opportunity_graph/opportunities.json`
- `data/opportunity_graph/outreach_drafts.json`
- `data/opportunity_graph/approvals.json`
- `reports/opportunity_command/daily/<date>.md`
- `reports/opportunity_command/weekly/<date>_proof_pack.md`

## Approval policy

Every target and every outbound message requires explicit human approval.
Approval statuses: `pending → approved | rejected | revise`. A draft can only be
recorded as sent (`mark_sent`) when it is **approved** and a **human sender** is
named — and even then the system only records a manual send; it does not send.
See `HUMAN_APPROVAL_AND_OUTBOUND_POLICY.md`.

## Proof pack

Weekly evidence pack built purely from store counts (companies scored, drafts,
approvals) — no fabricated metrics, estimates flagged. See
`reports/weekly_proof_pack.py`.

## API surface

Admin-key protected, self-prefixed `/api/v1/opportunity-command`:
`GET /today`, `GET /companies`, `POST /import`, `POST /score`, `GET /drafts`,
`POST /draft/{id}/approve`, `POST /draft/{id}/reject`,
`POST /draft/{id}/mark-sent`, `GET /proof-pack`.

## Packaging (hypothesis pricing — not guarantees)

| Offer | Audience | Shape | Guidance (SAR) |
|---|---|---|---|
| Diagnostic | Any | Scoping | 0–1,500 |
| Revenue Leak Scanner | Saudi | 7-day scanner | 1,500–5,000 |
| Saudi Expansion Radar | Foreign | 14-day sprint | 5,000–35,000 |
| Opportunity Command Room build | Any | 30-day build | 25,000–90,000 |
| Command Room retainer | Any | Monthly | 3,000–25,000/mo |
| Enterprise | Any | Custom | Custom |

All pricing is a starting hypothesis ("we expect", "the goal is", "we will
measure") — never a guarantee.

## 14-day sprint → 30-day retainer path

1. **Days 1–3:** seed + score, agree ICPs and segments.
2. **Days 4–9:** enrich signals, draft outreach, founder approves in the queue.
3. **Days 10–14:** decision memo + first proof pack.
4. **Retainer:** daily command report, approved drafts, weekly proof pack,
   partner watchlist.
