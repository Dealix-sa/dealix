# reports/customers — Customer-Level Rollups

## What lives here

This directory holds customer-level rollups: one view per customer that aggregates their journey across the offer ladder — diagnostic, sprint, proof pack, and any ongoing Managed Ops. It points back to the full customer workspace for detail.

Each rollup references:

- `customers/<name>/` — the authoritative workspace (intake through upsell), created by `create_customer_workspace.py`.
- The customer's position on the five-rung offer ladder (Free Diagnostic, Command Sprint, Data Pack, Managed Ops, Custom AI).
- Proof packs delivered and their value tiers.
- Paid events logged for the customer in `data/revenue/*.jsonl`.

## Customer workspace files referenced

| File | Role |
|---|---|
| `00_intake` | what the customer needs |
| `01_source_passport` | data provenance, permission, PII classification |
| `02_diagnostic_summary` | diagnostic scorecard result |
| `03_command_sprint_scope` | signed sprint scope |
| `09_delivery_log` | running delivery record |
| `10_proof_pack` | delivered proof pack |
| `11_upsell_recommendation` | next-offer recommendation (only if a real proof pack exists) |

## Rules

- The workspace under `customers/<name>/` is the source of truth; these rollups are read-only derivatives.
- No PII appears in a committed rollup; anonymized labels only.
- No guaranteed return is stated; value tiers only.
- No upsell is shown without a delivered proof pack behind it.

## Related

- `docs/04_delivery/PAID_SPRINT_HANDOFF.md` — workspace files and handoff.
- `docs/05_founder/REVENUE_COMMAND_CENTER.md` — the offer ladder.
- `reports/revenue/README.md`, `reports/delivery/README.md` — sibling report directories.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
