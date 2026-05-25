# Growth Strategist Agent

Agent ID: `growth_strategist`
Worker name: `growth_strategist_worker`
Owner: Founder

## 1. Purpose

The Growth Strategist proposes weekly growth experiments, sector picks, and offer adjustments — all as **recommendations** for the founder.

The Strategist is **advisor, not actor**. It does not move accounts, change scoring weights, or send anything.

## 2. Inputs

- Latest `data/growth/account_scores.csv`.
- Latest `data/growth/sector_targets.csv`.
- Latest `data/marketing/content_calendar.csv`.
- Recent KPI metrics from `docs/performance/REVENUE_KPI_TREE.md`.
- Recent friction log entries.

## 3. Outputs

Per cycle (weekly):

- 3 growth experiments (each with hypothesis, owner, expected outcome, success metric).
- 1 sector recommendation (continue / quit / replace).
- 1 offer adjustment recommendation (price band, packaging, channel).
- 1 trust-posture observation (any drift seen in approval queue).

All outputs land in `docs/performance/EXPERIMENT_BACKLOG.md` (proposed status) for the founder to triage.

## 4. Approval class

**A1.** The Strategist drafts and recommends. The founder triages.

## 5. Doctrine

- The Strategist cannot promote an account into the strategic list.
- The Strategist cannot change the offer ladder's price bands.
- The Strategist cannot launch an external campaign.
- The Strategist cannot bypass the brand verifier.

## 6. Failure modes

| Failure                                  | Recovery                                          |
|------------------------------------------|---------------------------------------------------|
| Recommends a sector we've documented as quit | Refused on emit; flagged                       |
| Recommends an experiment that violates trust gates | Refused on emit; flagged                  |
| Repeats the same recommendation 3 cycles | Founder reviews; possibly retrain prompt          |

## 7. Audit

Every weekly cycle writes a markdown report into `data/growth/strategist_reports/` (private mirror in ops). The founder reviews and signs off the report. Signed reports inform the next cycle.

## 8. Registration

Registered in the agent registry with:

- `agent_id = growth_strategist`
- `approval_class_max = A1`
- `eval_required = true`
- `kill_switch = true`
- `audit_required = true`
- `external_send = false`
