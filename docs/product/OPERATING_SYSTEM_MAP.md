# Dealix Operating System Map

Single **reference map** for how Dealix runs: intake → decision → execution → trust → output → learning.

## Input layer

- Request intake ([`../operations/REQUEST_INTAKE_SYSTEM.md`](../operations/REQUEST_INTAKE_SYSTEM.md))  
- Client intake (`clients/_TEMPLATE/` + workbench)  
- Data intake (exports, manifests)  
- Document intake (Company Brain paths)  

## Decision layer

- Qualification / client selection ([`../sales/QUALIFICATION_ENGINE.md`](../sales/QUALIFICATION_ENGINE.md))  
- Sellability ([`SELLABILITY_DECISION.md`](../company/SELLABILITY_DECISION.md))  
- Scope + change control ([`../delivery/SCOPE_ENGINE.md`](../delivery/SCOPE_ENGINE.md))  
- Governance decisions ([`GOVERNANCE_DECISION.md`](../governance/GOVERNANCE_DECISION.md), [`RUNTIME_GOVERNANCE.md`](../governance/RUNTIME_GOVERNANCE.md))  
- Build / product ([`BUILD_DECISION.md`](BUILD_DECISION.md))  
- Pricing ([`PRICING_DECISION.md`](../company/PRICING_DECISION.md))  
- Retainer / expansion ([`RETAINER_DECISION.md`](../growth/RETAINER_DECISION.md))  

## Execution layer

- Delivery workbench (`clients/<c>/<p>/`)  
- AI workforce / pipelines (repo modules: `*_os/`, services)  
- Workflow definitions (templates + code)  
- LLM gateway / model routing (see implementation + [`API_GOVERNANCE.md`](API_GOVERNANCE.md))  

## Trust layer

- Runtime governance, PII redaction, **permission mirroring**, audit logs, proof ledger ([`../company/OPERATING_LEDGER.md`](../company/OPERATING_LEDGER.md))  

## Output layer

- Reports, dashboards, drafts, workflows, assistants, **proof packs**  

## Learning layer

- Post-project review, **capital** ledger, feature backlog, playbook updates, market intelligence ([`../company/DEALIX_CAPITAL_MODEL.md`](../company/DEALIX_CAPITAL_MODEL.md))  

**Capability lens:** [`CAPABILITY_OPERATING_MODEL.md`](../company/CAPABILITY_OPERATING_MODEL.md).

---

## Document Standard Compliance

## Purpose
Defines this operating document's role inside Dealix Company OS.

## Owner
Sami (Founder). Reassign to the responsible operator when one is named.

## Review Cadence
Weekly until stable, then monthly.

## Inputs
- Relevant company data and signals.
- Founder decisions and customer evidence.

## Outputs
- Operating guidance, decisions, or templates produced by this document.
- Evidence captured for verification.

## Rules
- Must support revenue, delivery, trust, learning, or founder leverage.
- Must not introduce unsupported claims.
- Must preserve public/private boundaries.

## Metrics
- Completion status of the actions this document drives.
- Impact on revenue, delivery, trust, or founder leverage.

## Evidence
- Linked workflow, file, test output, customer interaction, or decision log.

## Last Reviewed
2026-05-23
