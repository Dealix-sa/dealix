# Dealix Worker Orchestrator

The worker orchestrator is the runtime that keeps long-running machines
(crons, queue consumers, schedulers) honest.

## Machines

Source of truth: `registries/machine_registry.yaml`.

Each machine entry carries: owner, schedule, entrypoint, KPI, kill switch,
audit requirement, failure mode.

## Operating model

- Every machine is identifiable (`machine_id`).
- Every machine writes a heartbeat to `data/heartbeats/<machine_id>.json`.
- Every machine respects a kill switch (env var or sentinel file).
- Every machine logs to the central audit trail.

## Backbone machines (today)

| Machine | Schedule | Entrypoint |
|---|---|---|
| founder-commercial-day | 07:00 Asia/Riyadh | `scripts/run_founder_commercial_day.sh` |
| ops-autopilot-evening | 20:00 Asia/Riyadh | `scripts/founder_evening_evidence.py` |
| approval-center-worker | continuous | `dealix/governance/approvals.py` |
| ci-everything-nightly | 02:00 UTC | `.github/workflows/dealix-everything.yml` |
| company-os-daily | 06:00 UTC | `.github/workflows/dealix-company-os.yml` |
| weekly-executive-checklist | Sunday 08:00 Asia/Riyadh | `scripts/run_executive_weekly_checklist.sh` |

## Failure handling

| Failure mode | Action |
|---|---|
| `log_and_retry_next_day` | record + retry next scheduled tick |
| `alert_founder` | record + notify founder via approval queue |
| `hold_and_alert_founder` | record + freeze downstream consumers |
| `github_actions_alert` | rely on GitHub Actions notifications |

## Verifier

`make worker-orchestrator` runs `scripts/verifiers/verify_worker_orchestrator.py`.

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*
