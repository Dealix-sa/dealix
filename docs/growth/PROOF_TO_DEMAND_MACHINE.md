# Proof to Demand Machine

**Owner:** Founder + Content Lead
**Source of truth:** This doc + `docs/07_proof_os/`

## Purpose

The Proof to Demand Machine turns completed Proof Packs into demand-generating distribution. Every closed sprint produces a Proof Pack (dated, anonymized record of what was delivered and what was observed). This machine takes the Proof Pack, extracts the publishable artifact, and routes it through the appropriate distribution channels — Nurture, ABM, Content, and direct outbound — to lift demand among similar accounts.

Proof is Dealix's primary demand-generation asset. This machine is how proof compounds into pipeline.

## Inputs

- **Closed Proof Packs** from `docs/07_proof_os/PROOF_PACK_STANDARD.md`.
- **Customer authorization status** — anonymized by default; named only with written customer authorization.
- **Account scoring state** — to identify similar accounts that benefit from this proof.
- **Active sector content calendar** — from `docs/growth/CONTENT_CALENDAR_MONTH_1.md`.

## Outputs

- **Anonymized case-safe summary** — a 500-700 word publishable artifact per Proof Pack (template: `docs/case-studies/case_NNN_anonymized.md`).
- **Distribution route** — Nurture (for similar Tier-A/B accounts), ABM (for strategic accounts with relevant pattern), Content (for public sector publication), Direct outbound (for triggered accounts in the same pattern).
- **Founder LinkedIn post** referencing the proof (anonymized).
- **Sector report contribution** — aggregated pattern feed for the next Sector Scorecard.

## Source of truth

This doc + Proof Pack records + the case study ledger.

## Approval class

- **A2** — Anonymized case-safe summary (Founder + Brand Lead).
- **A3** — Named customer case study (Founder only; requires written customer authorization).
- **A2** — Distribution per channel (per machine's own gate).

## Trust gate

- **Anonymization mandatory** unless explicit written customer authorization to name.
- **No invented metrics.** Every number in the Proof Pack content must source to a dated record.
- **Estimated vs Verified separation.** Each number is labeled.
- **Customer review opportunity** — even anonymized content is offered to the customer for review before publication.
- **No identifying detail** — sector + size + timing combinations are checked for deanonymization risk.

## Owner

- **Code owner:** Operations Engineering.
- **Operational owner:** Founder + Brand Lead.

## Worker script (placeholder)

`workers/proof_to_demand_worker.py` (planned). On Proof Pack publication, generates case-safe draft, queues for approval, plans distribution.

## KPI

| Metric | Target |
|---|---|
| Proof Pack to case-safe summary latency | <= 14 days |
| Case-safe summary approval rate (no revision) | >= 70 percent |
| Customer-named case study rate (of completed sprints) | observed; goal 1 per quarter |
| Proof-driven reply lift (vs non-proof-driven outbound) | observed |
| Deanonymization audit pass | 100 percent |

## Failure mode

- Case-safe summary contains a deanonymizing detail (industry + city + size + timing).
- A number in the summary cannot be sourced.
- Customer is not given review opportunity; named in a post without authorization.
- Proof Pack content used in a distribution channel without approval.

## Recovery path

1. Pull the offending artifact; re-anonymize; re-publish.
2. Re-source every number against the dated record.
3. Explicit written authorization workflow for any named case study.
4. Re-enforce the per-channel approval gate.

## What this machine does NOT do

- It does not invent or extrapolate sprint outcomes.
- It does not name customers without written authorization.
- It does not auto-distribute Proof Pack content.
- It does not aggregate confidential metrics into public reports.

## Cross-links

- Proof Pack standard: `docs/07_proof_os/PROOF_PACK_STANDARD.md`
- Case-safe summary template: `docs/07_proof_os/CASE_SAFE_SUMMARY.md`
- Distribution War Machine: `docs/growth/DISTRIBUTION_WAR_MACHINE.md`
- Content to Demand Engine: `docs/growth/CONTENT_TO_DEMAND_ENGINE.md`

## Disclaimer

Dealix does not guarantee demand lift from any Proof Pack. Outcomes published in Proof Packs are sprint-specific and not predictive of future engagements. Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
