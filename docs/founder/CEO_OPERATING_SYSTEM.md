# CEO Operating System

The rhythm that turns the founder into a CEO. A small, repeatable set of
inputs, rituals, and outputs — runnable solo, scalable when the team grows.

This OS does not duplicate operational work; it sits on top of the existing
operational stack and enforces **attention, decision quality, and capital
discipline**.

## Anchor sources

- Weekly review questions, scorecard rubric, and KPI targets: [`dealix/execution_assurance/registry.yaml`](../../dealix/execution_assurance/registry.yaml)
- Daily anchor (historical): [`docs/ops/FOUNDER_DAILY_ANCHOR_AR.md`](../ops/FOUNDER_DAILY_ANCHOR_AR.md)
- Pipeline source-of-truth CSV: [`docs/ops/pipeline_tracker.csv`](../ops/pipeline_tracker.csv)
- Strategic accounts CSV: [`docs/ops/CEO_TOP50_TRACKER.csv`](../ops/CEO_TOP50_TRACKER.csv)

## Daily — 30 minutes max

Trigger: morning, before any messages.

| Input | Source | Output |
|---|---|---|
| CEO Daily Brief | `scripts/founder_ceo_daily_brief.py` → `data/founder_briefs/ceo_daily_brief_<date>.md` | Today's top-3 focus |
| Pipeline signal | `/api/v1/founder/dashboard` (leads waiting >24h, renewals due, pending approvals) | Decisions / nudges queued |
| Decision queue | PRIVATE_OPS `ceo/decisions.jsonl` (last 5) | Confirm / reverse any |

See [CEO_DAILY_BRIEF_SYSTEM](CEO_DAILY_BRIEF_SYSTEM.md) for the brief schema.

## Weekly — 90 minutes, Friday afternoon

Trigger: Friday 14:00 KSA. Cron: `0 11 * * 5` UTC.

The review walks the questions in
[`dealix/execution_assurance/registry.yaml`](../../dealix/execution_assurance/registry.yaml)
under `weekly_ceo_review_questions_en` and grades each machine on the
0–5 maturity rubric (also in `registry.yaml`).

Outputs:

- Updated [FOUNDER_LEVERAGE_DASHBOARD](FOUNDER_LEVERAGE_DASHBOARD.md)
- Decisions appended to PRIVATE_OPS `ceo/decisions.jsonl`
- Capital re-allocation if any (see [../finance/CAPITAL_ALLOCATION_SYSTEM](../finance/CAPITAL_ALLOCATION_SYSTEM.md))
- Win/Loss notes ([../revenue/WIN_LOSS_REVIEW](../revenue/WIN_LOSS_REVIEW.md))

Full template: [CEO_WEEKLY_REVIEW](CEO_WEEKLY_REVIEW.md).

## Monthly — 2 hours, first Monday

- Strategic assumptions re-grade ([STRATEGIC_ASSUMPTIONS_REGISTER](STRATEGIC_ASSUMPTIONS_REGISTER.md))
- North Star metric trend ([../strategy/NORTH_STAR_METRIC](../strategy/NORTH_STAR_METRIC.md))
- Hire / automate / partner decisions logged ([../finance/HIRE_VS_AUTOMATE_VS_PARTNER](../finance/HIRE_VS_AUTOMATE_VS_PARTNER.md))
- Sector scale / fix / kill ([../strategy/BEACHHEAD_SECTOR_SCORECARD](../strategy/BEACHHEAD_SECTOR_SCORECARD.md))

## Quarterly — half-day

- Goal tree re-set ([../strategy/DEALIX_GOAL_TREE](../strategy/DEALIX_GOAL_TREE.md))
- Capital allocation snapshot ([../finance/CAPITAL_ALLOCATION_SYSTEM](../finance/CAPITAL_ALLOCATION_SYSTEM.md))
- Doctrine review (this file + [DO_NOT_SAY](DO_NOT_SAY.md))

## Tooling

| Ritual | Command |
|---|---|
| Daily brief | `make hyper-daily-brief` |
| Weekly leverage view | `make hyper-leverage` |
| Capital snapshot | `make hyper-capital` |
| Assumptions staleness | `make hyper-assumptions` |
| Sector scorecard | `make hyper-sectors` |
| Enterprise motion health | `make hyper-enterprise` |
| Verify whole layer | `make hyper-verify` |

## Non-negotiables

This OS records intent, decisions, and reviews. It does not send external
messages. It does not publish proof without ledger evidence. It does not
commit to payment terms. See [DO_NOT_SAY](DO_NOT_SAY.md) and
[`docs/00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md).
