# Eval Gate v1

The Eval Gate is the policy file that says, for each agent, what evaluation must pass before the agent is permitted to dispatch.

**Source of truth:** `evals/gates/dealix_agent_eval_gate.yaml`
**Owner:** Engineering Lead + Founder
**Trust gate:** A2 — gate thresholds are policy and require founder approval.

## File structure

```yaml
version: 1.0.0
last_reviewed_by: founder
last_reviewed_at: 2026-04-01T08:00:00Z

defaults:
  suite_pass_threshold: 0.95
  red_team_defence_threshold: 1.00
  drift_max_drop_points: 5
  freshness_max_hours: 168

agents:
  brand_guardian:
    suites:
      - brand_guardian_eval_v1
      - brand_guardian_red_team_v1
    thresholds:
      brand_guardian_eval_v1: 0.97
      brand_guardian_red_team_v1: 1.00
    on_fail: kill_and_notify_founder

  growth_strategist:
    suites:
      - growth_strategist_eval_v1
    thresholds:
      growth_strategist_eval_v1: 0.90
    on_fail: pause_and_notify_owner
```

## Gate phases

| Phase | When | Effect |
|-------|------|--------|
| Pre-merge | PR opened | Block merge if any required suite fails |
| Pre-deploy | Before runtime activation | Block activation if any required suite fails |
| Continuous | Nightly | Notify and possibly kill on regression |
| On-incident | After any agent incident | Spot eval; reactivation requires pass |

## on_fail strategies

| Strategy | Effect |
|----------|--------|
| `block` | Action denied until pass |
| `pause_and_notify_owner` | Agent paused; owner notified |
| `kill_and_notify_founder` | Agent killed; founder notified |
| `flag_only` | Logged; no action (rare; only for advisory suites) |

The default for agents with `external_action_allowed: false` is `pause_and_notify_owner`. For agents that touch financial or external surfaces, the default is `kill_and_notify_founder`.

## Drift detection

A nightly job compares each suite's pass rate to the trailing-7-day median. A drop greater than `drift_max_drop_points` triggers an alert. Three consecutive drift alerts trigger the agent's `on_fail` strategy.

## Freshness

Suites must be re-run within `freshness_max_hours`. A stale suite cannot certify an agent. The runtime treats stale certification as no certification.

## NIST AI RMF posture

- **Measure.** Continuous suite execution scores agent behaviour.
- **Manage.** `on_fail` strategies are the predeclared response.
- **Govern.** Thresholds are versioned and founder-approved.

## Failure modes

- **Suite gaming:** prompts tuned to suite, not to behaviour. Detection: red-team divergence. Recovery: suite expansion; threshold raised; founder review.
- **Threshold creep down:** thresholds lowered over time to keep agents green. Detection: quarterly review. Recovery: founder freezes thresholds; root cause filed.
- **Suite outage:** suite cannot run (test infra broken). Detection: monitor. Recovery: agents move to manual-fallback; runtime denies until restored.

## Recovery path

If the gate file is invalid or the suite infra is down, all agents fail closed. Manual operation continues.

## Metrics

- Gate version in production.
- Suite pass rate per agent (current and trailing 7 days).
- Drift alerts per quarter.
- Threshold changes per quarter (target: low).

## Disclaimer

The gate enforces tested behaviour. It does not guarantee correct behaviour in novel cases. Estimated value is not Verified value.
