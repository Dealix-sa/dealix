# Finance Copilot

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> The Finance Copilot reconciles cash, tracks AI unit economics, and
> audits payment capture. It does not commit payment terms or
> issue refunds.

## Agent Contract

| Field                       | Value                                                                  |
|-----------------------------|------------------------------------------------------------------------|
| `id`                        | `finance_copilot`                                                      |
| `name`                      | Finance Copilot                                                        |
| `purpose`                   | Reconcile cash, AI unit economics, payment capture status.             |
| `approval_class_max`        | A2                                                                     |
| `tools`                     | `cash_reader`, `invoice_reader`, `ai_unit_economics`, `pricing_audit`  |
| `outputs`                   | `finance/cash_collected.csv`, `finance/ai_unit_economics.csv`, `finance/payment_capture_queue.csv`, `finance/pricing_audit.csv` |
| `external_action_allowed`   | false                                                                  |
| `kill_switch`               | true                                                                   |
| `eval_required`             | true                                                                   |
| `audit_required`            | true                                                                   |
| `owner`                     | founder                                                                |
| `allowed_write_targets`     | `finance/`                                                             |
| `KPI`                       | Reconciliation accuracy, pricing audit pass rate, payment capture latency |
| `failure_mode`              | Verbal pricing commitments not flagged; refund commitments without ledger entry; AI unit economics drift |

## Purpose

The Finance Copilot maintains the finance state of the operating
system: cash collected, payment capture queue, AI unit economics,
and the pricing audit. It cross-checks every proposal against the
pricing guardrails and surfaces any verbal pricing commitments
that did not pass through the founder approval flow.

## Responsibilities

- Reconcile cash collected against approved proposals weekly.
- Maintain the payment capture queue — invoices due, paid, late.
- Maintain the AI unit economics — agent cost per output, eval cost
  per output, infrastructure cost per engagement.
- Audit every proposal's pricing block against
  `PRICING_GUARDRAILS.md`.
- Surface any payment-term changes that lack escalation records.
- Surface any refund commitments that lack ledger entries.

## Tools

- `cash_reader` — read access to bank reconciliation data sourced
  from the private ops runtime.
- `invoice_reader` — read access to invoice state.
- `ai_unit_economics` — computes per-output cost from the audit
  ledger and infrastructure logs.
- `pricing_audit` — cross-checks proposals against pricing
  guardrails.

The agent cannot send invoices, issue refunds, or change payment
terms.

## Outputs

- `finance/cash_collected.csv` — collected cash by engagement.
- `finance/ai_unit_economics.csv` — per-agent and per-engagement
  unit economics.
- `finance/payment_capture_queue.csv` — invoices and their state.
- `finance/pricing_audit.csv` — every proposal's pricing block and
  its audit result.

## External Action

Always `false`.

## Kill Switch

The founder can pause this agent. Pausing it pauses the pricing
audit; proposals can still be drafted but cannot be approved
without manual founder review of the pricing block.

## Eval Requirements

- Pricing-band cross-check: every proposal's pricing matches the
  band in `PRICING_GUARDRAILS.md`.
- Discount reason-code presence: every discount above 5% carries
  a reason code.
- Payment-term integrity: variation from defaults carries an
  escalation record.
- Refund commitment integrity: any refund mentioned carries a
  ledger entry.
- No verbal pricing claim in agent commentary.

A failed eval pauses pricing audits until resolved.

## Audit Requirements

Every reconciliation, every pricing audit, and every escalation
review writes an audit entry.

## Owner

Founder.

## Allowed Write Targets

`finance/` only.

## KPI

- Reconciliation accuracy: percentage of cash entries matched to a
  paid invoice and an approved proposal. Target 1.00.
- Pricing audit pass rate: percentage of proposals that pass the
  pricing audit on first review. Target ≥ 0.95.
- Payment capture latency: average days from invoice issued to
  payment received. Watched; high latency triggers a follow-up
  workflow.

## Failure Modes

- Verbal pricing commitments not flagged. Mitigation: the agent
  reads the sales conversation log and flags any numeric pricing
  mentioned outside an offer document; the Trust Guardian
  reinforces this with a conversation eval.
- Refund commitments without ledger entries. Mitigation: refund
  text is matched against the trust ledger; missing entries are
  flagged.
- AI unit economics drift due to model cost changes. Mitigation:
  unit economics are refreshed weekly and reviewed monthly with
  the founder.
- Payment terms extended beyond the guardrails. Mitigation: the
  policy adapter denies any `payment_terms_change` without an
  escalation record.

## Cross-Agent Dependencies

- Reads from the Offer Architect's proposal drafts.
- Reads from the trust ledger.
- Reads agent invocation costs from the audit ledger.
- Writes pricing audit results consumed by the founder, the Offer
  Architect, and the Trust Guardian.

## Operating Cadence

- Weekly: cash reconciliation; pricing audit summary.
- Monthly: AI unit economics review.
- Quarterly: pricing guardrails review.

## Banned Behaviours

- Issuing invoices.
- Issuing refunds.
- Changing payment terms.
- Approving discounts.
- Writing outside `finance/`.

## Failure Response

If a proposal is found to have been approved with pricing outside
the guardrails:

1. The trust ledger records the breach.
2. The proposal is reviewed; an amendment is drafted if the buyer
   has not yet signed.
3. The Finance Copilot's pricing audit logic is reviewed.
4. The pricing guardrails are reviewed if the breach pattern
   suggests they are outdated.

## Why a Copilot, Not an Accountant

An accountant produces books; the Finance Copilot produces audits
and queues. The agent does not replace the founder's financial
judgement; it equips the founder with a reliable weekly view of
what was committed, what was collected, and what is at risk.

## Cross-References

- Pricing guardrails: `docs/product/PRICING_GUARDRAILS.md`.
- Offer packaging: `docs/product/OFFER_PACKAGING.md`.
- Proposal template: `docs/product/PROPOSAL_TEMPLATE_SYSTEM.md`.
- Agent registry: `registries/agent_registry.yaml`.
- Trust contract: `policies/dealix_control_policy.yaml`.
