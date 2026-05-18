# Decision Ledger

Material decisions only (sell / don’t sell / build / block / price / enterprise). IDs: `D-###`.

## Every entry must include

```text
Decision
Context
Evidence
Risk
Owner
Outcome
Review Date (if time-bound)
```

| ID | Date | Decision | Context | Evidence | Risk | Owner | Outcome |
|----|------|-----------|---------|----------|------|-------|---------|
| D-001 | | Sell Lead Intelligence officially | Readiness stable | demo + QA + proof templates | Low | | Official |
| D-002 | | Do not build WhatsApp auto-send now | Compliance + product focus | governance policy; no repeat demand | High | | Blocked |
| D-003 | 2026-05-18 | GO on the founder-led rung 0-1 selling motion; NO-GO on payment capture until founder gates close | Commercial-activation program complete (narrative, delivery, sales kit) | Workstreams A/B/C shipped; sales kit doctrine-clean; rung 0-1 delivery renders | Medium | Founder | Partial-GO |

Tie to [`../company/DECISION_OPERATING_SYSTEM.md`](../company/DECISION_OPERATING_SYSTEM.md).

---

## Go/No-Go Assessment — first paid pilot (2026-05-18)

Workstream E of the commercial-activation program. Read-only evaluation —
no new build (commercial freeze active).

### GO — ready now (founder can start today)
- **Narrative** — sales kit + launch content unified to the governed-ops
  doctrine (Workstream A, ledger G-003). No autonomous-rep / "1 SAR" /
  guaranteed-outcome claims remain.
- **Sales kit** — rung 0-1 funnel assembled end to end: `START_HERE.md` →
  warm list → `QUALIFICATION_CHECKLIST.md` → `FREE_DIAGNOSTIC_OFFER.md` →
  demo script → objection handler → 499 SAR Sprint agreement (Workstream C).
- **Delivery** — rung 0-1 deliverables render to customer-facing bilingual
  HTML/PDF; payment→delivery audit link writes to the ledgers (Workstream B).
- **Daily machine** — `scripts/daily_operate.sh`, the durable approval
  queue, and `/api/v1/founder/daily-brief` run the Commercial Proof Loop.

### NO-GO — blocks payment capture (founder action, runs in parallel)
- **Moyasar KYC** — commercial registration + IBAN. Until done, run in
  `test` mode only; no real payout possible.
- **Launch Gates 1-3** (`docs/sales-kit/DEALIX_LAUNCH_GATES.md`) — verify
  Railway deploy, register the Moyasar webhook, run the 1-SAR end-to-end
  payment test.
- **Legal** — DPA signature + lawyer review of privacy/terms before the
  first paid deal.
- **Engineering drills** (P1) — k6 load, rollback, backup-restore on
  staging. Not blocking the motion; close before scale.

### Verdict
**Partial-GO.** Start the founder-led motion immediately (warm list →
free diagnostic → Sprint proposal). The 499 SAR payment can be *requested*
but only *captured* once Moyasar KYC + Gates 1-3 close. Freeze exit
condition stays: first paid pilot delivered + customer-approved Proof Pack.
