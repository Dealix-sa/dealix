# نظام نمو Dealix — Dealix Growth System

> Signal → Sprint → Retainer → Productize. One loop. Repeated.

## Purpose
Define the single growth loop Dealix runs. Reject every initiative that does not fit the loop.

## Owner
Founder/CEO.

## Inputs
- Founder content / network signals.
- Offer ladder (`docs/revenue/OFFER_LADDER.md`).
- Sprint factory state (`docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`).
- Offer evolution thresholds (`docs/revenue/OFFER_EVOLUTION_SYSTEM.md`).

## Outputs
- Loop velocity metrics (Signal → Sprint conversion, Sprint → Retainer conversion).
- Productization candidates list (Monthly Strategy Review).

## Rules
1. Every initiative must locate itself in one of the four loop stages. If it doesn't fit, it doesn't run.
2. Stages advance only when the prior stage produces evidence.
3. The loop runs sequentially, not in parallel, for any single customer.
4. Productization happens by threshold (10 successful runs), not by founder excitement.
5. Loop velocity is reported monthly; stalled stages are surfaced.

## Metrics
- Signal → Sprint conversion: target ≥ 25%.
- Sprint → Retainer conversion: target ≥ 30%.
- Time from Signal to Sprint start: target ≤ 21 days.
- Successful runs per offer: tracked to 3 / 5 / 10 thresholds.

## Cadence
Loop velocity measured weekly. Productization triggers reviewed monthly.

## Evidence
`dealix-ops-private/loop/YYYY-WW.json`, sprint records, retainer attach reports.

## Verifier
`make growth-loop-verify` — checks every active engagement is tagged to a loop stage.

## Runtime Command
`make loop-snapshot`

---

## The Loop

```
SIGNAL → SPRINT → RETAINER → PRODUCTIZE
  ↑                                |
  └────── feeds new signals ←──────┘
```

### Stage 1 — Signal
A signal is a written interest from an ICP-fit prospect. Sources:
- Founder content (LinkedIn posts, sector reports).
- Warm intros.
- Inbound from existing customers.
- Conference / event follow-ups (consented).

Output: a paid Signal Sample (smallest rung of `OFFER_LADDER.md`).

### Stage 2 — Sprint
A focused 4–6 week engagement (`Revenue Sprint` rung). Produces:
- Customer outcome (operational improvement).
- Anonymized evidence artifact (case-safe).
- Founder learning logged to the relevant doc.

### Stage 3 — Retainer
A `Revenue Desk` engagement attaching after the Sprint. The retainer institutionalizes the operational discipline introduced in the Sprint. MRR enters here, not before.

### Stage 4 — Productize
After 10 successful Sprint runs of the same shape, the offer graduates per `OFFER_EVOLUTION_SYSTEM.md`:
- 3 successes → document the playbook.
- 5 successes → standard template.
- 10 successes → automation candidate / packaged offer.

The productized version becomes a new signal source via published evidence.

## Loop velocity table (target)

| Transition | Target rate | Target time |
|---|---|---|
| Signal → Sprint | ≥ 25% | ≤ 21 days |
| Sprint → Retainer | ≥ 30% | ≤ 14 days after Sprint close |
| Successful Sprint → Evidence shipped | ≥ 90% | ≤ 14 days after delivery |
| Sprint successes → Productize threshold | track to 10 | quarterly review |

## Anti-patterns the loop prevents
- Selling a retainer to a customer who has not run a sprint (Trojan-horse risk).
- Skipping evidence to "save time" (kills the next signal cycle).
- Building product before 10 sprint runs (premature productization).

## What is NOT part of the loop
- Cold campaigns.
- Brand projects without a tied sprint.
- "Thought leadership" tours unattached to evidence.

## القواعد العربية
1. كل مبادرة تنتمي لمرحلة من اللوب. ما لا ينتمي، لا يُشغّل.
2. المراحل تتقدم بالدليل، لا بالنية.
3. الترقية إلى المنتج تأتي بالعتبة (10 جولات ناجحة)، لا بالحماس.

## Cross-links
- `STRATEGIC_THESIS.md`
- `docs/revenue/OFFER_LADDER.md`
- `docs/revenue/OFFER_EVOLUTION_SYSTEM.md`
- `docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`
- `MOAT_SYSTEM.md`
