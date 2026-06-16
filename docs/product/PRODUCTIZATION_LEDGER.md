# Productization Ledger

| Manual Step | Repeated Count | Time Cost | Risk | Revenue Link | Decision |
|---|---:|---:|---|---|---|
| CSV cleanup | 3 | 6h/project | medium | Lead Sprint | Build import_preview |
| Proof report writing | 3 | 4h/project | low | all sprints | Build report generator |
| Claims review | 5 | 1h/project | high | outreach | Build forbidden_claims in draft_gate |

## Decision

```text
Repeated 3x + revenue link + time/risk = build
```

Do **not** build a feature because you imagined it — only because repetition or major risk proves it.

## First backlog snapshot

**P0**

- `data_os.import_preview`  
- `data_os.data_quality_score`  
- `governance_os.policy_check`  
- `governance_os` / PII hints  
- `revenue_os.scoring`  
- `revenue_os` outreach drafts (safe, draft-only)  
- `reporting_os.proof_pack`  
- `delivery_os` QA paths  

**P1**

- founder command center (surfaced)  
- client_workspace v1  
- proof / capital ledgers in product UI  
- proposal / weekly report helpers  

**P2**

- Company Brain basic RAG  
- support reply suggestions  
- workflow runtime  
- prompt registry hardening  
- llm_gateway cost guard  

Do not start P2 before P0/P1 sell and prove value.

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
