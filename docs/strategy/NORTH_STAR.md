# النجم القطبي — North Star Metric

> Paid sprints delivered with evidence, per quarter.

## Purpose
Lock a single metric that, when up and to the right, means Dealix is real. Everything else is downstream.

## Owner
Founder/CEO.

## Inputs
- Sprint completion records (`docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`).
- Payment records (`docs/finance/PAYMENT_RULES.md`, `INVOICE_WORKFLOW.md`).
- Evidence artifacts shipped (`docs/case-studies/`, `docs/14_trust_os/`).

## Outputs
- Quarterly north-star count: `dealix-ops-private/north-star/YYYY-Q.json`.
- Trend line refreshed Monthly.

## Rules
1. The metric is one number. It does not split.
2. A sprint counts only if all three conditions hold: paid in full, delivered to scope, evidence artifact published (anonymized).
3. Refunded sprints subtract from the count in the quarter of refund.
4. Internal sprints (Dealix-on-Dealix) do not count.
5. The metric changes by Monthly Strategy Review decision only, never ad hoc.

## Metrics
- Quarterly target: set in `STRATEGIC_BETS.md` per quarter.
- Floor target: ≥ 3 paid sprints with evidence per quarter (early stage).
- Stretch target: 12 per quarter (productized stage).

## Cadence
Counted weekly, reported monthly, reviewed quarterly.

## Evidence
`dealix-ops-private/north-star/`.

## Verifier
`make north-star-verify` — checks each counted sprint has payment + scope + evidence artifact links.

## Runtime Command
`make north-star-count`

---

## Definition

**Paid sprint delivered with evidence (PSDE)**

A unit of work that satisfies all of:
1. **Paid**: full payment received per `CASH_RULES.md` (deposit + final, or single payment).
2. **Delivered**: scope completed and accepted by the customer (signed acceptance or written confirmation).
3. **Evidence**: a case-safe artifact published — either a case study (`docs/case-studies/case_NNN_anonymized.md`), a sector report, or a trust pack section pointing to the work.

If any condition is missing, the sprint does not count.

## Why this metric

- Forces revenue, delivery, and proof to happen together.
- Resistant to vanity: cannot inflate with followers, leads, or pipeline.
- Aligned with the moat: every PSDE adds to the proof moat and the sector data moat.
- Recoverable: anyone reviewing the repo can verify the count by cross-checking artifacts.

## What this is NOT

- Not MRR (tracked separately in `MRR_DEFINITION.md`).
- Not "deals closed" — closed without delivery is not a north star.
- Not "case studies published" — case studies without paid delivery are content, not proof of business.

## Anti-patterns this metric prevents

- Counting unpaid pilots.
- Counting projects where the customer asked to remove evidence (no artifact = no count).
- Splitting one paid engagement into multiple sprints to inflate the count.

## Sub-KPIs that feed this metric
See `CEO_KPI_TREE.md` — Revenue, Delivery, Trust branches all feed PSDE.

## القواعد العربية
1. مقياس واحد لا يتجزأ.
2. السبرنت يُحتسب فقط إذا تحققت ثلاثة شروط: دفع كامل، تسليم مقبول، دليل منشور (مجهول الهوية).
3. السبرنت المسترد يُخصم من الربع الذي حدث فيه الاسترداد.

## Cross-links
- `CEO_KPI_TREE.md`
- `STRATEGIC_BETS.md`
- `docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`
- `docs/case-studies/`
