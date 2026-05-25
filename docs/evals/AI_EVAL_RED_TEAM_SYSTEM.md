# AI Eval & Red Team System

## Doctrine Anchor
- Non-negotiables touched: #1 (approval before external action), #2 (no value claim without evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: control-plane verification scripts as release blockers, approval-first for external action.

## Purpose

Evaluate every Dealix agent and prompt path against quality, safety, evidence use, overclaim risk, prompt-injection resistance, and approval escalation. No agent moves to production without a passing eval threshold. No agent stays in production without periodic re-evaluation.

## Eval Suites

| Suite | What it checks |
|-------|----------------|
| Lead scoring accuracy | Deterministic scorer agreement on labeled set |
| Outreach safety | No spam patterns, no overclaim, no banned language |
| Proposal draft quality | Bilingual quality, factual grounding, scope clarity |
| No-overclaim | No outcome promises, no guaranteed-revenue language |
| Prompt injection defense | Resistance to "ignore previous instructions" and similar |
| Sensitive data leakage | No leakage of system prompt, secrets, or other tenants' data |
| Approval classification | Correctly identifies actions requiring approval |
| Bilingual AR / EN quality | Natural Saudi business Arabic, accurate English |
| Saudi market relevance | Sector knowledge, tone, named-entity grounding |

## Red Team Scenarios

The red team harness runs the following adversarial scenarios:

- "Ignore previous instructions" injection.
- Attempt to send without approval.
- Attempt to make a guaranteed-revenue claim.
- Attempt to reveal secrets, system prompt, or other tenants' data.
- Attempt to export customer data outside policy.
- Attempt to bypass approval through chained tool calls.
- Attempt to fabricate evidence or invent a source.
- Attempt to publish a client claim without recorded client approval.
- Attempt to contact a record present in `SuppressionRecord`.

## Gate-to-Production Rule

No agent or prompt path is promoted to production unless:

1. Eval suites relevant to its role pass at the documented threshold.
2. Red team scenarios relevant to its capabilities pass at zero failures.
3. The change is logged in the audit trail.
4. A rollback path is documented (doctrine #4).

Promotion is a release event, not a silent merge.

## Core Rules

- Evals are deterministic where possible; LLM-judged evals carry their own meta-eval.
- A failing eval blocks the merge. "Will fix later" is not an exception.
- Red team failures are escalated to trust review, not aggregated.
- Eval data sets carry tenant isolation; we do not leak production records into eval fixtures.
- "No proof-level overclaim" is enforced both at output (eval) and at policy (Approval Center).

## Operating Cadence

| Cadence | What runs |
|---------|-----------|
| Per PR | Relevant eval suites for changed agents and prompts |
| Daily | Smoke evals for the live agents |
| Weekly | Full red team sweep |
| Quarterly | Threshold and scenario review (some scenarios retired, new ones added) |

## Runtime Wiring

- Existing eval framework (cross-link): `docs/EVALS_RUNBOOK.md`.
- AI observability and evals: `docs/AI_OBSERVABILITY_AND_EVALS.md`.
- Existing red team scenarios: `docs/quality/RED_TEAM_SCENARIOS.md`, `docs/enterprise/RED_TEAM_SYSTEM.md`.
- Quality outputs eval set: `docs/quality/AI_OUTPUT_EVALS.md`.
- Eval scaffolding: `evals/` directory.
- Audit log: `db/models.py::AuditLogRecord`.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Eval pass rate per suite per release | ≥ documented threshold | `evals/` results |
| Red team failures in production agents | 0 | red team logs |
| Time from a red team finding to a fix | < 1 sprint | issue tracker |
| Agents in production without a current eval | 0 | release log |

## Cross-Links

- `docs/EVALS_RUNBOOK.md`
- `docs/quality/RED_TEAM_SCENARIOS.md`
- `docs/enterprise/RED_TEAM_SYSTEM.md`
- `docs/quality/AI_OUTPUT_EVALS.md`
- `docs/AI_OBSERVABILITY_AND_EVALS.md`
- `docs/engineering/OBSERVABILITY_SLO_SYSTEM.md`
- `docs/control_plane/APPROVAL_CENTER_V2.md`
- `docs/trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md`

## Open Items

- A unified eval threshold registry across suites does not yet exist as one file.
- Red team scenarios for opt-out bleed and cross-tenant data leakage are listed here; their fixtures are partially wired.
- "Bilingual quality" eval depends on a small reviewer set; automated scoring is partial.
- The promotion ceremony (with audit log entry) is enforced by convention today, not by a release gate script.
