# Revenue Factory OS

The Revenue Factory is the assembly line that turns a qualified signal into a paid invoice. It is not a CRM. It is a sequence of stages, each with explicit inputs, outputs, owners, and trust gates.

**Source of truth:** `$PRIVATE_OPS/revenue_factory_state.csv`
**Owner:** Founder + Revenue Lead
**Trust gate:** No external action (proposal sent, invoice issued, contract executed) without founder approval class A1 or A2.

## Stages

| # | Stage | Input | Output | Approval class |
|---|-------|-------|--------|---------------|
| 1 | Signal capture | Inbound or sourced lead | Row in `signals.csv` | A0 |
| 2 | Qualification | Signal + ICP fit check | Qualified opportunity | A0 |
| 3 | Sample / diagnostic | Qualified opportunity | Case-safe diagnostic | A1 |
| 4 | Proposal | Diagnostic accepted | Drafted proposal | A1 |
| 5 | Negotiation | Proposal sent | Term sheet | A2 |
| 6 | Close | Term sheet accepted | Signed contract | A2 |
| 7 | Invoice | Signed contract | Issued invoice | A2 |
| 8 | Cash | Issued invoice | Collected payment | A0 (verify only) |

A3 actions are never permitted in this factory. Every transition is logged in `$PRIVATE_OPS/revenue_factory_log.csv` with timestamp, agent id, approval class, and trust-gate decision.

## Why a factory model

A factory exposes the rate-limiting station. If proposals stall, the bottleneck is stage 4. If cash stalls, the bottleneck is stage 8. Without stage-by-stage instrumentation, the founder cannot tell whether the problem is sourcing, qualification, or close discipline. The factory model replaces opinion with throughput data.

## Inputs to each station

- **Signal capture:** structured fields only (company, sector, contact role, observed trigger). No scraped data, no purchased lists. Every signal carries provenance.
- **Qualification:** ICP-fit score against `docs/02_saudi_positioning/SAUDI_SECTOR_TAXONOMY.md` and budget / authority / need / timing notes.
- **Sample / diagnostic:** see `docs/revenue/SAMPLE_FACTORY.md`.
- **Proposal:** see `docs/revenue/PROPOSAL_FACTORY.md`.

## Outputs

Each row in `revenue_factory_state.csv` carries: `opportunity_id`, `stage`, `entered_at`, `owner`, `last_approval_class`, `trust_gate_pass`, `value_estimate_sar`, `value_observed_sar`, `value_verified_sar`. Estimated value is not Verified value.

## Failure modes

- **Stage skip:** an opportunity jumps from qualification to invoice without proposal. Detection: row missing proposal artifact. Recovery: factory roll-back; opportunity returns to stage 3 and the owner is notified.
- **Approval-class drift:** an A0 agent attempts an A2 action. Detection: policy engine in `policies/dealix_control_policy.yaml`. Recovery: action blocked; audit row written; founder notified.
- **Stale opportunity:** more than 14 days in any stage. Detection: nightly job. Recovery: forced status review or archive.

## Recovery path

If the factory halts (policy engine outage, registry corruption, runtime mesh failure), the founder runs the manual recovery in `docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md`. No automated retry. No silent advance.

## Metrics

The factory reports five KPIs daily:

1. Signal-to-qualified conversion rate (estimate).
2. Qualified-to-proposal conversion rate (estimate).
3. Proposal-to-close conversion rate (estimate).
4. Time-in-stage by stage.
5. Cash collected this month vs prior month (verified).

These feed `docs/performance/REVENUE_KPI_TREE.md`.

## Disclaimer

Dealix does not guarantee sales, meetings, or conversion rates. The Revenue Factory reports measured throughput, not promised revenue. All published metrics are estimated unless tagged Verified.
