# Company Data Architecture

## Purpose
Define the data architecture for the whole company: what entities exist, where they live, who owns them, and how they flow.

## Domains
1. **Pipeline** — companies we are pursuing.
2. **Revenue** — actions, proposals, cash collected, pipeline value, MRR.
3. **Finance** — expenses, unit economics, discounts.
4. **Trust** — approvals, risk register, claim reviews, redactions.
5. **Delivery** — samples, QA scores, client folders.
6. **Content** — proof library, calendar, published log.
7. **Productization** — candidates, repeated workflows.
8. **People** — delegation, contractors, access.
9. **Partners** — pipeline, tracker.
10. **Evidence** — execution evidence ledger.

## Source of truth
Every entity has ONE canonical store. No duplication.

| Entity | Canonical store | Format | Owner |
|---|---|---|---|
| Pipeline opportunity | `dealix-ops-private/pipeline/pipeline_tracker.csv` | CSV | Founder |
| Revenue action | `dealix-ops-private/revenue/revenue_action_log.csv` | CSV | Founder |
| Proposal | `dealix-ops-private/sales/proposal_tracker.csv` | CSV | Founder |
| Cash collected | `dealix-ops-private/revenue/cash_collected.csv` | CSV | Founder |
| MRR | `dealix-ops-private/revenue/mrr_tracker.csv` | CSV | Founder |
| Expense | `dealix-ops-private/finance/expenses.csv` | CSV | Founder |
| Approval | `dealix-ops-private/trust/approval_log.csv` | CSV | Founder |
| Risk | `dealix-ops-private/trust/risk_register.csv` | CSV | Founder |
| Evidence | `dealix-ops-private/evidence/execution_evidence_ledger.csv` | CSV | Founder |

## Schemas
JSON Schemas in `schemas/` describe the columns, types, and constraints for each CSV.

## Identity
- `company` is the natural key for a pipeline opportunity until a deal number is assigned.
- `client` is the natural key for delivery and revenue once a proposal is accepted.
- `evidence_path` is the natural key for evidence rows.

## Refreshness expectations
See `docs/data/DATA_FRESHNESS_POLICY.md`.

## Privacy
See `docs/data/DATA_PRIVACY_BOUNDARY.md` and `docs/data/DATA_MINIMIZATION_RETENTION.md`.

## Validation
- `python ops_runtime/data_validator.py --root ../dealix-ops-private` validates every CSV against its schema.
- `python scripts/audit_private_data_quality.py --root ../dealix-ops-private` runs deeper quality checks.

## Export
- `python scripts/export_company_snapshot.py --root ../dealix-ops-private --out ../dealix-ops-private/exports/snapshot.json`
  produces a local-only JSON snapshot for analysis. Never publish this file.
