# Eval and Red Team System

> DEALIX — INTELLIGENT DEALS. REAL GROWTH.
> The Eval and Red Team System runs the eval gate against agent
> outputs and conducts adversarial probes against the operating
> loop. It blocks agent outputs on regression.

## Agent Contract (Eval Guardian)

| Field                       | Value                                                                  |
|-----------------------------|------------------------------------------------------------------------|
| `id`                        | `eval_guardian`                                                        |
| `name`                      | Eval Guardian                                                          |
| `purpose`                   | Run eval gate suites; block agent outputs on regression.               |
| `approval_class_max`        | A1                                                                     |
| `tools`                     | `eval_runner`, `eval_status_writer`, `red_team_scenarios`              |
| `outputs`                   | `evals/eval_status.csv`, `evals/eval_history.csv`, `evals/red_team_findings.csv` |
| `external_action_allowed`   | false                                                                  |
| `kill_switch`               | true                                                                   |
| `eval_required`             | false                                                                  |
| `audit_required`            | true                                                                   |
| `owner`                     | founder                                                                |
| `allowed_write_targets`     | `evals/`                                                               |
| `KPI`                       | Eval coverage (rules with active eval paths), regression block rate, time-to-restore after regression |
| `failure_mode`              | Eval suite drift; missed regression; red team scenario coverage gaps |

## Purpose

The Eval Guardian is the agent that runs the eval gate defined in
`evals/gates/dealix_agent_eval_gate.yaml`. It also coordinates the
red team scenarios — adversarial probes against the operating
loop. When an eval fails or a red team scenario uncovers a gap,
the Eval Guardian blocks the affected agent's outputs until the
gap is closed.

## Responsibilities

- Run the eval gate on schedule and on demand.
- Block agent outputs that fail eval.
- Coordinate red team scenarios across the operating system.
- Maintain the eval suite — add new tests when a new policy rule
  or refusal marker is added.
- Maintain `evals/eval_status.csv` as the current state of every
  eval suite.

## Tools

- `eval_runner` — runs eval suites.
- `eval_status_writer` — writes to `evals/eval_status.csv`.
- `red_team_scenarios` — read access to red team scenario
  definitions.

The agent cannot send, post, or commit anything externally.

## Outputs

- `evals/eval_status.csv` — current state of every eval suite.
- `evals/eval_history.csv` — historical eval runs.
- `evals/red_team_findings.csv` — findings from red team
  scenarios.

## External Action

Always `false`.

## Kill Switch

The founder can pause the Eval Guardian. Pausing it pauses all
agents whose `eval_required: true` (effectively the entire
operating system); pausing is a critical-severity action.

## Eval Requirements

The Eval Guardian itself does not have `eval_required: true` in
the registry, because it runs the evals. Its outputs are audited
by the audit ledger; correctness of the eval suite is reviewed
manually by the founder during the quarterly registry review.

## Audit Requirements

Every eval run, every regression flagged, and every red team
scenario writes an audit entry.

## Owner

Founder.

## Allowed Write Targets

`evals/` only.

## KPI

- Eval coverage: percentage of policy rules and refusal markers
  with an active eval path. Target 1.00.
- Regression block rate: percentage of regressions that were
  blocked at eval time (vs. discovered after publication). Target
  ≥ 0.95.
- Time-to-restore: from regression detected to remediation merged
  and eval green. A founder-set service level.

## Failure Modes

- Eval suite drift — a policy rule is added but no eval path is
  added. Mitigation: the verifier
  `scripts/verify_eval_gate.py` checks that every rule has a
  corresponding eval; missing paths fail the verifier.
- Missed regression — the eval suite passes but the production
  artefact fails. Mitigation: the prompt-output verifier
  (`scripts/verify_prompt_output_quality.py`) cross-checks
  published artefacts against the eval rules and flags drift.
- Red team scenario coverage gap. Mitigation: scenarios are
  reviewed quarterly; new scenarios are added when a new attack
  pattern is observed.

## Red Team Scenarios

The red team scenarios are adversarial probes designed to break the
operating system in controlled ways. Categories:

- **Prompt injection.** Adversarial inputs designed to bypass
  agent guardrails (e.g. "ignore previous instructions").
- **Suppression bypass.** Drafts crafted to match a suppressed
  identity through obfuscation.
- **Proof publication bypass.** Attempts to publish proof without
  approval by routing through a different surface.
- **Guaranteed-outcome injection.** Attempts to slip
  guaranteed-outcome wording past the claims-safety eval.
- **Policy escalation.** Attempts to enable A3, disable the kill
  switch, or expand allowed write targets without founder
  approval.
- **PDPL probe.** Attempts to extract identifiable buyer data
  through scorecards or content artefacts.

Each scenario has a defined expected outcome (the system blocks
the probe and logs the attempt). A scenario whose expected outcome
does not occur is a critical finding.

## Red Team Cadence

- Per-release: scenarios run as part of the release gate.
- Monthly: a full scenario sweep.
- Quarterly: a red team review with the founder, the Trust
  Guardian, and the Security Guardian.
- Annually: external red team review (planned, not yet conducted).

## Cross-Agent Dependencies

- Reads outputs from every agent.
- Writes status that every agent reads (eval-required agents pause
  on regression).
- Coordinates with the Trust Guardian on policy coverage.
- Coordinates with the Security Guardian on PDPL and data
  protection scenarios.

## Operating Cadence

- Continuous: eval suites run on every artefact transition.
- Daily: eval status summary.
- Weekly: regression review.
- Monthly: full red team scenario sweep.
- Quarterly: registry and scenario review with the founder.

## Banned Behaviours

- Disabling its own eval suites.
- Marking an eval as passed without running it.
- Bypassing the audit ledger.
- Writing outside `evals/`.

## Failure Response

If a regression is detected:

1. The affected agent is paused.
2. The trust ledger records the regression.
3. The remediation is drafted, reviewed, and merged.
4. The eval suite is re-run.
5. The agent is restored after eval passes.

If a red team scenario succeeds (the system fails to block the
probe):

1. The trust ledger records the finding as critical.
2. The relevant agent and policy rule are reviewed.
3. The remediation is drafted.
4. The eval suite is upgraded.
5. The system is restored after the upgraded eval passes.

## Why Eval and Red Team Together

Evals catch known regressions. Red team scenarios catch unknown
ones. Running both, with the same agent coordinating, keeps the
operating system honest against both kinds of failure. An operating
system with eval but no red team is brittle; an operating system
with red team but no eval is unstable.

## Cross-References

- Eval gate: `evals/gates/dealix_agent_eval_gate.yaml`.
- Trust contract: `policies/dealix_control_policy.yaml`.
- Agent registry: `registries/agent_registry.yaml`.
- Trust Guardian: `docs/ai/TRUST_GUARDIAN_AGENT.md`.
- Security Guardian: `docs/ai/SECURITY_GUARDIAN.md`.
