# Workflow Risk Classification

## Risk Classes

| Class | Definition | Examples |
|---|---|---|
| Low | Reversible, internal, no client impact | Internal scoring, drafting for review |
| Medium | Reversible but client-visible if released | First outbound, internal recommendation |
| High | Hard to reverse, client-visible | Proposals, pricing, public claims |
| Critical | Legal, financial, or regulatory impact | Contracts, refunds, regulator contact, data exports |

## Automation Levels

| Level | Meaning |
|---|---|
| L0 | Manual only — no AI execution |
| L1 | AI drafts, human edits, human sends |
| L2 | AI drafts, human approves, AI sends |
| L3 | AI executes; human reviews logs after the fact |

## Classification Table

| Workflow | Risk | Automation Level | Approval |
|---|---:|---:|---|
| Lead scoring | Low | L3 | A0 |
| Internal recommendation | Low | L3 | A0 |
| Message drafting | Medium | L1 | A1 |
| First outbound (no claims) | Medium | L2 | A1 |
| First outbound (with claims) | Medium | L1 | A2 |
| Proposal generation | High | L2 | A2 |
| Public claim / website edit | High | L1 | A2 |
| Pricing change (public) | High | L0 | A3 |
| Contract changes | Critical | L0 | A3 |
| Refunds | Critical | L0 | A3 |
| Regulator / government contact | Critical | L0 | A3 |
| Client data export | Critical | L0 | A3 |

## Rule

A workflow cannot be promoted to a higher automation level without:
1. A measured eval result on the agent involved.
2. A 30-day clean Trust incident record.
3. A founder decision recorded in `DECISION_LOG.md`.

## Demotion Rule

Any Trust incident in a workflow triggers an immediate demotion of one level
(e.g., L3 → L2). The demotion stands until the eval and incident gates pass.
