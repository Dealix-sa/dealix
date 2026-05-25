# Experiment Engine

## Doctrine Anchor
- Non-negotiables touched: #2 (no measured value claim without source evidence), #5 (no proof-level overclaiming).
- Frozen decisions touched: control-plane verification scripts as release blockers.

## Purpose

Run controlled experiments across sectors, buyer titles, message angles, offers, prices, sample types, follow-up cadences, channels, and call-to-actions. Every change to commercial motion that affects external behavior is an experiment with a hypothesis, a sample size, a success metric, a decision date, and a recorded outcome.

## Experiment Types

- **Sector experiment**: which sectors respond to which framing.
- **Buyer title experiment**: who in the buying unit responds.
- **Message angle experiment**: pain-led vs proof-led vs trend-led framing.
- **CTA experiment**: "15-minute call" vs "sample" vs "sector report".
- **Offer experiment**: which rung of the offer ladder converts.
- **Price experiment**: list price vs anchored bundle vs introductory rate.
- **Sample experiment**: which sample artifact shape drives proposal requests.
- **Follow-up cadence experiment**: 3-touch vs 5-touch vs 7-touch.
- **Channel experiment**: email vs LinkedIn vs referral vs content inbound.

## Required Fields per Experiment

| Field | Description |
|-------|-------------|
| `hypothesis` | Single sentence: change X → expect Y |
| `variable` | The one thing varied |
| `control` | What we compared against |
| `sample_size` | Minimum n before reading the result |
| `success_metric` | The single metric that decides |
| `decision_date` | When we read and decide |
| `result` | Observed numbers with source links |
| `decision` | Adopt / reject / iterate / pause |
| `owner` | Who runs it |
| `evidence_link` | Where the raw data lives |

## Success Metrics

- Reply rate
- Positive reply rate
- Sample request rate
- Proposal rate
- Payment conversion
- Complaint / opt-out rate (guardrail — never trade conversion for trust damage)
- Cycle time from first touch to proposal

## Core Rules

- No scaling of a channel or motion without an experiment record.
- No comparing experiments with different control conditions or sample sizes.
- Every experiment has a kill condition — a complaint / opt-out / bounce rate above threshold ends the experiment even if conversion looks good.
- Experiments touching external sends require approval batches at the same rate they would without an experiment.
- "Result inconclusive" is a valid outcome; do not adopt on insufficient evidence.

## Runtime Wiring

- Eval harness scaffolding: `evals/`.
- Deterministic baseline scoring (the control for many experiments): `auto_client_acquisition/crm_v10/lead_scoring.py` and `auto_client_acquisition/icp_scorer.py`.
- Revenue events (where outcomes live): `auto_client_acquisition/revenue_memory/event_store.py`.
- Audit log (where decisions live): `db/models.py::AuditLogRecord`.

## Experiment Registry (today: a YAML or markdown register; eventually a table)

- Today: experiments are documented under `docs/growth/` and similar locations as the team runs them.
- Target: a single `evals/experiment_registry.yaml` plus a CLI to read and decide.

## Metrics

| Metric | Target | Source |
|--------|--------|--------|
| Active experiments | 3–7 at any time | registry |
| Experiments that closed with a decision | 100% by decision date | registry |
| Experiments adopted at scale without sufficient sample | 0 | weekly review |
| Experiments killed by guardrail | tracked; investigated | registry |

## Cross-Links

- `docs/distribution/DEALIX_DISTRIBUTION_OS.md`
- `docs/distribution/EMAIL_DELIVERABILITY_SYSTEM.md`
- `docs/evals/AI_EVAL_RED_TEAM_SYSTEM.md`
- `docs/EVALS_RUNBOOK.md`
- `docs/founder/REVENUE_WAR_ROOM_OS.md`

## Open Items

- A single experiment registry file does not yet exist.
- A CLI to render the next week of experiments and the past week's decisions is not yet built.
- Guardrail thresholds (complaint rate, bounce rate, opt-out spike) are defined in `docs/distribution/EMAIL_DELIVERABILITY_SYSTEM.md` but not enforced at registry close-out time.
