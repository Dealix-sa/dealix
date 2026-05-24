# Dealix Company Memory

Memory is the thing that compounds. Dealix's memory layer captures
every decision, every value-bearing event, every proof, every reusable
asset — and makes them queryable.

## Stores

| Store | What | Module |
|---|---|---|
| Decision log | One row per significant decision (who, why, evidence) | `dealix/registers/90_day_execution.yaml` |
| Value ledger | Tiered (estimated / verified / client_confirmed) | `dealix/registers/no_overclaim.yaml` |
| Proof Pack store | Every shipped Proof Pack | `dealix/execution_assurance/` |
| Capital Asset registry | Every reusable artifact | `dealix/registers/` (live YAMLs) |
| Audit trail | Every governance decision | `data/audit_log/` |

## Decision log

A decision log entry must include:
- `decision_id`
- `timestamp`
- `decider` (agent or human)
- `context_ref` (URL / file / commit)
- `evidence_refs` (list of source refs)
- `decision_text`
- `governance_decision` (auto_approved / pending_approval / approved_by_<user>)
- `reversal_plan` (how to undo)

## Value ledger tiers

| Tier | Evidence | Use case |
|---|---|---|
| estimated | self-reported, no source_ref required | Diagnostic Proof Packs |
| verified | source_ref required | Sprint Proof Packs |
| client_confirmed | source_ref + client_ref required | Retainer reviews |

## Proof Pack

Minimum score: 70. Required sections: executive summary, data sources
verified, findings with evidence, recommendations with estimates,
bilingual disclaimer.

## Capital Asset

Every paid engagement must register >= 1 capital asset. Asset types:
dashboard, scoring model, runbook, eval suite, dataset, integration.

## Querying

- Founder: read directly from registries.
- Agents: read via `dealix/registers/registry.py` API.
- Future: `apps/web/app/company-memory/` page surfaces the registry.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
