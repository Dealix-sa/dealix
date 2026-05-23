# Agent Readiness System

## Purpose
Decide whether a given workflow is safe to delegate to an AI agent (sub-agent in Claude Code, automation in n8n, etc.).

## Readiness dimensions
1. **Workflow definition clarity**: written, repeatable, deterministic intent.
2. **Boundary**: agent's read/write scope is clearly defined.
3. **Failure mode tolerance**: a wrong action can be reversed without external impact.
4. **Audit trail**: every agent action lands in a log.
5. **Human-in-the-loop**: external actions still require founder.

## Readiness levels
- **L0 — Not ready**: agent assistance only via drafts the founder reviews.
- **L1 — Assist**: agent drafts; founder approves; founder executes.
- **L2 — Local**: agent runs against `dealix-ops-private/` files; no external effect.
- **L3 — Public**: agent commits to the public repo via PR; founder merges.
- **L4 — External**: agent acts externally with founder confirmation per action.
- **L5 — Autonomous**: not granted in foreseeable horizon for Dealix.

## Per sub-agent (current state)
- delivery sub-agent: L2.
- sales sub-agent: L1 / L2 (drafts proposals; never sends).
- engineer sub-agent: L3.
- content sub-agent: L3 (PR to public repo with founder review).
- pm sub-agent: L2.

## Promotion rules
- A sub-agent stays at its current level for at least 30 days of clean operation before promotion.
- Promotion is recorded in `people/access_log.csv`.
- Demotion is immediate if any escape is detected; recorded in `trust/approval_log.csv` with reason.

## Anti-patterns
- "It's worked before, give it more access."
- Granting access for convenience under deadline pressure.
- Forgetting to revoke after the task.
