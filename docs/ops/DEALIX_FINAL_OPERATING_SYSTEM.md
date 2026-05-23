# Dealix Final Operating System

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Saudi B2B Revenue Operating System.

Built on Trust · Driven by Growth · Closing Deals · Focused on Results · Global Mindset, Local Impact.

This is the meta document. It is the single index that summarizes
every pillar of the Dealix operating system and points to the
authoritative documentation for each. If a reader can read only one
document, they should read this one and then follow the links.

## What Dealix is

Dealix is the Saudi B2B Revenue Operating System. Our promise is
operational: a method for building revenue with intelligence, trust,
and audited discipline. We do not promise outcomes. We commit to a
method that has produced outcomes for the customers documented in
our proof library.

## The five pillars (brand)

| Pillar                          | What it means in operating terms                                         |
| ------------------------------- | ------------------------------------------------------------------------ |
| Built on Trust                  | Every external action is approved; the audit ledger is the proof.        |
| Driven by Growth                | KPIs are the language; experiments are the engine; lessons compound.     |
| Closing Deals                   | We measure won deal value and cash collected, not vanity activity.        |
| Focused on Results              | Sprint design is outcome-first; proof requires acceptance.                |
| Global Mindset, Local Impact     | Saudi-first delivery and sovereignty; international-quality engineering. |

## The trust plane (non-negotiables)

The trust plane is encoded in four files:

| Artifact                                  | Path                                           |
| ----------------------------------------- | ---------------------------------------------- |
| Policy                                     | `policies/dealix_control_policy.yaml`           |
| Registry                                   | `registries/agent_registry.yaml`                |
| Eval gate                                  | `evals/gates/dealix_agent_eval_gate.yaml`       |
| Audit                                      | `trust/approval_decisions.csv` (private ops)    |

Non-negotiables enforced across the artifacts:

1. A3 (autonomous external action) is banned.
2. No external sending without founder approval recorded in the
   audit ledger.
3. No proof publication without approval.
4. No pricing, contract, or payment-term commitments without
   founder approval.
5. No guaranteed revenue, sales, or meeting claims.
6. The private ops runtime lives outside the repo at
   `/opt/dealix-ops-private` (or `$PRIVATE_OPS`).

## Document index

### Trust

| Document                                                            | Purpose                                                |
| ------------------------------------------------------------------- | ------------------------------------------------------ |
| `docs/trust/POLICY_AS_CODE_V1.md`                                    | The 11 policy rules.                                   |
| `docs/trust/ULTIMATE_TRUST_PLANE.md`                                  | Meta architecture of the trust plane.                  |
| `docs/trust/FOUNDER_CONSOLE_TRUST_GATE.md`                            | How the console enforces trust.                        |
| `docs/trust/SUPPRESSION_SYSTEM.md`                                    | Suppression contract and lifecycle.                    |
| `docs/trust/NO_OVERCLAIM_POLICY.md`                                   | Approved vs disallowed phrasing.                       |
| `docs/trust/AUDIT_EVENT_MODEL.md`                                     | Audit ledger schema.                                   |

### Evals

| Document                                                            | Purpose                                                |
| ------------------------------------------------------------------- | ------------------------------------------------------ |
| `docs/evals/EVAL_GATE_V1.md`                                          | The 15 eval suites.                                    |
| `docs/evals/PROMPT_OUTPUT_EVAL_MATRIX.md`                             | Suite × failure mode × fixture mapping.                |

### Performance

| Document                                                            | Purpose                                                |
| ------------------------------------------------------------------- | ------------------------------------------------------ |
| `docs/performance/PERFORMANCE_IMPROVEMENT_OS.md`                       | The four-pillar performance loop.                      |
| `docs/performance/REVENUE_KPI_TREE.md`                                 | KPI tree from pipeline to cash.                        |
| `docs/performance/CONVERSION_DIAGNOSTICS.md`                           | Diagnostic moves at every funnel stage.                |
| `docs/performance/EXPERIMENT_BACKLOG.md`                               | Experiment discipline.                                 |
| `docs/performance/LEARNING_LOOP.md`                                    | Lessons → playbooks.                                   |
| `docs/performance/NEXT_BEST_ACTION_ENGINE.md`                          | Ranking layer for next moves.                          |
| `docs/performance/WIN_LOSS_ANALYSIS.md`                                | Late-funnel learning.                                  |
| `docs/performance/OBJECTION_ANALYTICS.md`                              | Objection coding and response library.                 |

### Data and runtime

| Document                                                            | Purpose                                                |
| ------------------------------------------------------------------- | ------------------------------------------------------ |
| `docs/data/POSTGRES_PRIMARY_MODE.md`                                  | Postgres primary; CSVs operational.                    |
| `docs/data/ULTIMATE_DATA_PLATFORM.md`                                  | The data layer architecture.                           |
| `docs/data/DATA_QUALITY_SYSTEM.md`                                     | DQ checks and score.                                    |
| `docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md`                         | Folder tree + CSV schemas.                              |
| `docs/runtime/WORKER_ORCHESTRATOR_V1.md`                                | Scheduling, state, kill switches.                       |
| `docs/runtime/ULTIMATE_WORKER_MESH.md`                                  | Mesh diagram and failure isolation.                    |

### Engineering

| Document                                                            | Purpose                                                |
| ------------------------------------------------------------------- | ------------------------------------------------------ |
| `docs/engineering/ULTIMATE_OBSERVABILITY_DORA.md`                      | Observability and DORA metrics.                         |
| `docs/engineering/DEPLOYMENT_AND_ROLLBACK_SYSTEM.md`                    | Deploy and rollback playbook.                           |

### Finance

| Document                                                            | Purpose                                                |
| ------------------------------------------------------------------- | ------------------------------------------------------ |
| `docs/finance/ULTIMATE_FINANCE_OS.md`                                  | Finance discipline.                                    |
| `docs/finance/AI_UNIT_ECONOMICS_SYSTEM.md`                              | Cost per deal tracking.                                |
| `docs/finance/REVENUE_RECOGNITION_NOTES.md`                            | Revenue recognition.                                    |

### Customer success

| Document                                                            | Purpose                                                |
| ------------------------------------------------------------------- | ------------------------------------------------------ |
| `docs/customer_success/CUSTOMER_SUCCESS_OS.md`                         | Overall CS discipline.                                  |
| `docs/customer_success/CLIENT_HEALTH_SCORE_SYSTEM.md`                  | Per-client scoring.                                     |
| `docs/customer_success/REFERRAL_SYSTEM.md`                              | Partner referrals.                                      |
| `docs/customer_success/RENEWAL_AND_EXPANSION_OS.md`                     | Renewal and expansion motion.                           |

### Delivery

| Document                                                            | Purpose                                                |
| ------------------------------------------------------------------- | ------------------------------------------------------ |
| `docs/delivery/ULTIMATE_DELIVERY_OS.md`                                 | Sprint OS.                                              |
| `docs/delivery/CLIENT_ONBOARDING_OS.md`                                 | First-five-days discipline.                             |
| `docs/delivery/HANDOFF_AND_QA_SYSTEM.md`                                | The QA gate.                                            |

### Security

| Document                                                            | Purpose                                                |
| ------------------------------------------------------------------- | ------------------------------------------------------ |
| `docs/security/ULTIMATE_SECURITY_GOVERNANCE.md`                         | Security model and principles.                          |
| `docs/security/PRODUCTION_SECURITY_GATE.md`                              | Production posture check.                              |
| `docs/security/INTERNAL_API_AUTH_GATE.md`                               | Internal API auth.                                      |
| `docs/security/BRANCH_PROTECTION_REQUIRED_CHECKS.md`                    | CI required checks.                                     |
| `docs/security/INCIDENT_RESPONSE_OS.md`                                  | Incident response.                                      |
| `docs/security/BACKUP_AND_RESTORE_OS.md`                                 | Backup and restore.                                     |
| `docs/security/ACCESS_CONTROL_MODEL.md`                                  | Access control.                                         |

### Ops

| Document                                                            | Purpose                                                |
| ------------------------------------------------------------------- | ------------------------------------------------------ |
| `docs/ops/DEALIX_MARKET_ENTRY_OPERATING_STACK.md`                       | Overview tying brand, positioning, intelligence, product, revenue, delivery, finance, customer success. |
| `docs/ops/DEALIX_FINAL_OPERATING_SYSTEM.md`                              | This document.                                          |
| `docs/ops/CLAUDE_CODE_EXECUTION_REPORT.md`                              | Execution log for the build.                            |

## Configuration surface

| Variable                              | Purpose                                                        |
| ------------------------------------- | -------------------------------------------------------------- |
| `DEALIX_INTERNAL_TOKEN`                | Auth for the Founder Console internal API.                     |
| `PRIVATE_OPS` / `DEALIX_PRIVATE_OPS_DIR`| Path to the private ops runtime.                              |
| `DEALIX_POLICY_FILE`                   | Override path to the policy file.                              |
| `DEALIX_AGENT_REGISTRY`                | Override path to the agent registry.                           |
| `DEALIX_PRIMARY_STORE`                 | Defaults to `postgres`; surfaced in `/data/summary`.            |

## The four required CI workflows

| Workflow                                                | Required check                            |
| ------------------------------------------------------- | ----------------------------------------- |
| `.github/workflows/dealix-company-os.yml`                | `dealix-company-os`                       |
| `.github/workflows/dealix-sovereign-operating-stack.yml` | `dealix-sovereign-operating-stack`        |
| `.github/workflows/dealix-market-entry-stack.yml`        | `dealix-market-entry-stack`               |
| `.github/workflows/dealix-brand-growth-operating-layer.yml` | `dealix-brand-growth-operating-layer`  |

See `docs/security/BRANCH_PROTECTION_REQUIRED_CHECKS.md`.

## How to operate the system

Daily:

1. Read the founder brief (assembled by the CEO Copilot).
2. Triage the approvals queue.
3. Review at-risk clients (CS).
4. Review trust flags and incidents.

Weekly:

1. Refresh the four-pillar scorecard.
2. Walk the diagnostic for the worst-trending KPI.
3. Review experiments (open and recently closed).
4. Review the Win/Loss summary.
5. Review the eval gate status.

Monthly:

1. Walk the full KPI tree.
2. Rebalance the sector portfolio.
3. Close the finance month.
4. Review customer health deep-dive.
5. Review AI unit economics.

Quarterly:

1. Sovereign readiness review.
2. Backup and restore drill.
3. Access control drill.
4. Offer ladder review.
5. Policy / registry / eval gate review.

## Discipline

1. The trust plane is the constraint.
2. The Founder Console is the only mutation surface.
3. The audit ledger is the spine.
4. The runtime lives outside the repo.
5. Documentation traces to code and to operating CSVs.

## What this system is not

- It is not a chatbot.
- It is not an autopilot.
- It is not a generic CRM.
- It is not a marketing claim.
- It is not anywhere close to "done" — it is intentionally
  versioned, audited, and improved.

DEALIX · INTELLIGENT DEALS. REAL GROWTH.
