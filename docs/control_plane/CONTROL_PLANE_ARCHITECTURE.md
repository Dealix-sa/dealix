# Control Plane Architecture

The control plane is the management layer above Dealix's twelve operating
systems. It collects state, classifies decisions, routes approvals, raises
risks, scores systems, and emits the daily CEO brief.

## Modules

| Module | Responsibility |
|---|---|
| `control_plane/company_state.py` | Single typed truth across systems |
| `control_plane/metrics_collector.py` | Build `CompanyState` from inputs |
| `control_plane/ceo_brief.py` | Render Daily CEO Brief from state |
| `control_plane/decision_engine.py` | Classify BUILD / FIX / KILL / DEFER |
| `control_plane/approval_router.py` | Route to A0 / A1 / A2 / A3 |
| `control_plane/risk_engine.py` | Map signals to typed Risks |
| `control_plane/system_scorecard.py` | Score each OS and aggregate |
| `control_plane/learning_router.py` | Convert weekly inputs to decisions |

## Data Flow

```
inputs (CRM, billing, CI, repo, ledgers)
  → MetricsCollector
  → CompanyState
  → DecisionEngine + RiskEngine + ApprovalRouter
  → CEO Brief + Risk Log + Approvals Waiting + Focus Queue
  → Founder reviews → decisions → execution
  → LearningRouter (weekly) → updates to OS docs and templates
```

## Invariants

1. Trust OS overrides every other engine. A Trust violation always returns
   `REJECT` or `ESCALATE`.
2. Unknown actions default to A2 (explicit approval), never A0.
3. `CompanyState` is the only allowed input to `render_daily_brief`.
4. No engine performs I/O. All I/O is at the edges (collectors, writers).
5. The doctrine files (`DEALIX_OPERATING_DOCTRINE.md`,
   `DEALIX_COMPANY_OS_SCORECARD.md`) are the human-readable spec; the code
   in `control_plane/` is the executable contract.
