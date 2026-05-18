# Client Ledger

Unified view of **accounts** (anonymize in shared repos). Health aligns with [`../growth/CLIENT_HEALTH_SCORE.md`](../growth/CLIENT_HEALTH_SCORE.md).

## Client status

```text
Lead
Qualified
Proposal
Paid
In Delivery
Delivered
Proof Delivered
Retainer Offered
Retainer
Dormant
```

## Client health bands

```text
80+ = Expand
60–79 = Nurture
40–59 = Risk
<40 = Churn likely
```

| Client | Sector | Service | Status | Revenue | QA | Proof | Health | Next Step |
|--------|--------|---------|--------|--------:|---:|-------|-------:|-----------|
| Client A | B2B Services | Lead Intelligence | Delivered | 9500 | 91 | Yes | 85 | Pilot |

**Notes:** Revenue = illustrative; replace with your CRM totals / SAR.

---

## Sales-Kit Activation Log

### 2026-05-18 — Workstream C: Rung 0–1 sales-kit assembled and activated

Audited `docs/sales-kit/` against the rung 0–1 funnel (warm-list targeting →
first-touch → qualification → free Mini Diagnostic → demo → objection handling
→ 499 SAR Sprint proposal/agreement → close → follow-up). Verdict: funnel
coherent and doctrine-clean; two gaps closed.

- **Rewrote** `docs/sales-kit/START_HERE.md` — replaced stale "1-riyal test →
  cold messages" framing with the doctrine-clean warm-list motion; now a single
  ordered 11-step index linking every funnel-stage asset for rung 0–1.
- **Created** `docs/sales-kit/FREE_DIAGNOSTIC_OFFER.md` — rung 0 offer doc
  (was referenced by WARM_LIST_WORKFLOW.md but missing); bilingual, scope +
  exclusions + 24h delivery path + diagnostic-to-Sprint gate.
- **Created** `docs/sales-kit/QUALIFICATION_CHECKLIST.md` — founder-facing
  8-question checklist mirroring `sales_os/qualification.qualify(...)`; the five
  decisions, the hard-refusal rule, and logging.
- **Verified** warm-list path runnable: `dealix_leads_20_real.md` /
  `dealix_leads_50_expanded.md` feed `data/warm_list.csv` →
  `scripts/warm_list_outreach.py` → bilingual drafts (founder approval only).

Founder can run the rung 0–1 motion today. No external messages drafted or
sent — kit assembly only.
