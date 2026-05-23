# DEALIX EXECUTION LEDGER

> Append-only record of every meaningful action the company takes.
> Used by the Founder Brief to compute "what changed this week".

## Format

Every entry is a single row. Never edit historical rows — append a correction row if needed.

```
YYYY-MM-DD | system | action | owner | status | link/evidence
```

- **system**: one of the 12 Super Systems (e.g. `revenue_os`, `trust_os`)
- **action**: short verb phrase ("Sent proposal to Client X", "Killed feature Y")
- **owner**: who did it (founder, agent name, contractor)
- **status**: `done` · `pending` · `approved` · `rejected` · `killed` · `deferred` · `blocked`
- **link**: PR, file path, invoice number, or N/A

## Active Ledger

```
2026-05-23 | company_os | Initialized 12 Super Systems + Founder Command OS | founder | done | docs/founder/CEO_OPERATING_SYSTEM.md
2026-05-23 | trust_os | Added approval_matrix.py + claim_guard.py + suppression.py + data_retention.py + evidence_pack.py + policy_engine.py | founder | done | dealix/trust/
2026-05-23 | trust_os | Added tests/trust/ (approval matrix, claim guard, suppression, retention, evidence pack, policy engine) | founder | done | tests/trust/
2026-05-23 | strategy_os | Locked North Star + Positioning + ICP + Competitive + Moat + Pricing + Product + GTM + 90-day strategic plan | founder | done | docs/strategy/
2026-05-23 | revenue_os | Defined Revenue Model + Sales Funnel + Pipeline Stages + Offer Ladder + Outbound Policy + Qualification + Proposal + Closing + Metrics | founder | done | docs/revenue/
2026-05-23 | acquisition_os | Defined Lead Sourcing + ICP Scoring + Sector Playbooks + Outreach Cadence + Sample Generation + Channel + Partner | founder | done | docs/acquisition/
2026-05-23 | delivery_os | Productized Revenue Sprint + Managed Pilot + Revenue Desk offers + playbooks + QA | founder | done | docs/delivery/
2026-05-23 | product_os | Locked Principles + Feature Intake + Build-Defer-Kill + Customer Feedback Loop + Release Policy + Product Metrics | founder | done | docs/product/
2026-05-23 | trust_os | Wrote Approval Matrix + No-Overclaim + Data Retention + Suppression List + Incident Response + Client Data Handling + Claims Guide + Public Repo Safety + AI Governance + Audit Policy | founder | done | docs/trust/
2026-05-23 | finance_os | Defined Billing + Payment + Invoice + Refund + MRR Definition + Financial Dashboard | founder | done | docs/finance/
2026-05-23 | client_success_os | Defined Onboarding + Weekly Report + Client Health + Feedback Loop + Retention + Renewal + Upsell + Testimonial Capture | founder | done | docs/client_success/
2026-05-23 | content_os | Defined Content Strategy + LinkedIn + X + Sector Report + Case Study + Proof Library + Founder Voice | founder | done | docs/content/
2026-05-23 | people_os | Defined Role Map + Hiring Triggers + 3 scorecards + Contractor Onboarding + Delegation Rules | founder | done | docs/people/
2026-05-23 | learning_os | Defined Experiment Log + Win/Loss + Message + Sector + Pricing + Agent Evals + Monthly Strategy Update | founder | done | docs/learning/
2026-05-23 | company_os | Added verify scripts (company_os, founder_os, revenue_os, delivery_os, trust_os, learning_os, public_safety) | founder | done | scripts/verify_*.py
2026-05-23 | company_os | Added GitHub workflow dealix-company-os.yml (structural + trust tests as required checks) | founder | done | .github/workflows/dealix-company-os.yml
2026-05-23 | company_os | Added readiness gates + 5 scorecards + 3 operating-loop checklists | founder | done | readiness/
```

## How To Append

1. After any meaningful action (sale, delivery, kill, approval, incident), add one row.
2. If the action created an artifact (PR, invoice, report), link it.
3. If the action was rejected or killed, record the reason in the action column.
4. Never edit older rows. If you misrecorded, add a correction row referring to the row date.

## Weekly Roll-Up

Every Sunday during the Weekly CEO Review:
- Count actions by system → confirm balance (no system starved, no system bloated)
- Count `killed` + `deferred` rows → confirm focus discipline
- Count `rejected` + `blocked` rows → identify systemic friction
- Promote learnings into `docs/learning/MONTHLY_STRATEGY_UPDATE.md`

## Decision Rule

If an action is **not** in this ledger within 24 hours, it did not happen for the company's purposes. The ledger is the company's memory.
