# Hermes Execution Backlog

This backlog turns Hermes from a governed foundation into a practical founder operating layer. Work should be delivered in small PRs after the foundation merges.

## P0 — Foundation hardening

| Item | Outcome | Acceptance check |
| --- | --- | --- |
| Verify manifest in CI | Prevent broken agent registry | `python scripts/verify_hermes_layer.py` passes |
| Generate review artifacts | Founder sees useful output | `python scripts/hermes_review_runner.py --out-dir data/hermes` creates digest and JSONL |
| Keep local outputs ignored | Avoid committing working data | `data/*` remains ignored |
| Document server runbook | Repeatable setup | Runbook explains commands and rollback |

## P1 — Founder digest

| Item | Outcome | Acceptance check |
| --- | --- | --- |
| Add digest sections | Revenue, ops, market, finance, product | Digest has fixed headings |
| Add unresolved item tracking | Founder sees pending decisions | JSONL contains open/closed status |
| Add weekly priority queue | Strategic focus | Weekly artifact ranks opportunities |

## P2 — Read-only connectors

| Item | Outcome | Acceptance check |
| --- | --- | --- |
| GitHub PR reader | Product QA and security notes | PR review artifact generated |
| Repo health reader | Ops readiness notes | Health artifact generated |
| Cost snapshot reader | Provider/cost notes | Cost artifact generated from local or exported data |
| Market input folder | Market analyst can process curated sources | Markdown inputs produce market notes |

## P3 — Governance and approvals

| Item | Outcome | Acceptance check |
| --- | --- | --- |
| Review record status transitions | New, reviewed, approved, rejected | Schema and verifier updated |
| Approval registry | Founder-approved items are traceable | Approval JSONL generated |
| Risk policy checks | Prevent accidental expansion | CI blocks missing risk fields |

## P4 — Cockpit and reporting

| Item | Outcome | Acceptance check |
| --- | --- | --- |
| Founder cockpit JSON export | Frontend can render Hermes status | `landing/assets/data/hermes-status.json` generated |
| Weekly board | Shows top opportunities and blockers | Markdown artifact generated |
| Cost and model dashboard | Tracks provider usage | Cost artifact exists and has trend fields |

## P5 — Controlled workflow expansion

Only after P0-P4 are reliable:

| Item | Outcome | Acceptance check |
| --- | --- | --- |
| LangGraph review checkpoints | Multi-step review flow | Checkpointed graph pauses for review |
| OpenAI Agents SDK guardrails | Safer agent IO | Input/output guardrail tests pass |
| CrewAI role process | Repeatable role crew | Crew outputs same artifact contract |

## Do not do yet

- Do not add live customer-facing automation before approval registry exists.
- Do not add writable integrations before read-only artifacts are useful.
- Do not add multiple frameworks in one PR.
- Do not commit generated founder or customer artifacts.
