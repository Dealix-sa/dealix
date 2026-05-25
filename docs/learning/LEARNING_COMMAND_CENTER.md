# Learning Command Center — مركز قيادة التعلّم

## Purpose
The weekly learning loop: one decision recorded, one playbook update, one experiment launched or closed. The Learning Command Center is the rhythm that compounds Dealix's operating advantage.

## Owner
Founder.

## Inputs
- Weekly intelligence review notes.
- Sprint folders closed in the last week.
- Open experiments.
- Incident log entries.

## Outputs
- One decision logged in `docs/learning/COMPANY_MEMORY.md` per week.
- One playbook, checklist, or template updated per week.
- One experiment launched or one closed per week.

## Rules (numbered)
1. The weekly loop is not optional. Skipped weeks are logged as such.
2. The decision must be specific and dated. Vague decisions do not count.
3. The update must be a concrete diff to a file. "We will improve X" does not count.
4. The experiment must follow `EXPERIMENT_SYSTEM.md` with hypothesis, metric, sample, duration, kill rule.
5. Decisions, updates, and experiments are cross-linked.
6. The Command Center is reviewed Sunday with the founder reading the week's three artifacts aloud.

## Metrics
- Weeks with all three artifacts (target greater than or equal to 90 percent).
- Decisions that survived 90 days without reversal.
- Experiments closed with a clear conclusion (target greater than or equal to 80 percent).

## Cadence
Weekly. Sunday review.

## Evidence (paths)
- `docs/learning/COMPANY_MEMORY.md`
- `docs/learning/EXPERIMENT_SYSTEM.md`
- The updated playbook file path each week.

## Verifier
Founder.

## Runtime Command
`make learning.weekly.scaffold` writes the three artifact skeletons for the week.

## The three artifacts

**Artifact 1 — One decision.** A specific operating decision made this week. Examples: changed scoring weight on signal-recency, narrowed sector focus to two sectors for the quarter, added a new banned phrase. The decision is dated, owned, and includes the reasoning. Logged in `COMPANY_MEMORY.md`.

**Artifact 2 — One playbook update.** A concrete diff to a checklist, template, or runbook. Examples: added "verify exclusion list against intake" to the QA checklist, updated the safe language library with two new entries, reordered handoff agenda. The update is shipped to the file the same week.

**Artifact 3 — One experiment.** Either a new experiment launched or an existing experiment closed. Following `EXPERIMENT_SYSTEM.md`. Examples: testing two-variant vs three-variant message packs on a 5-sprint sample; testing a new sector for first-engagement viability.

## Sunday review structure

The Sunday review takes 60 minutes. The founder opens the week's three artifacts and reads them. Then opens the trust dashboard, the AI dashboard, and the open-incident log. Then writes a 200-word reflection into the weekly intelligence review file. The reflection answers: what surprised me this week, what pattern is forming, what is the highest-leverage change for next week.

## Operating substance
The single biggest predictor of a service business compounding over time is whether the team learns from each engagement. Most do not because they have no rhythm. The Learning Command Center is that rhythm.

The three artifacts are deliberately small. One decision, one update, one experiment per week is sustainable. Three is more than zero, less than five. Over a year it is 50 decisions, 50 updates, 50 experiments. That is the operating advantage being compounded.

The artifacts must be specific. Vague decisions and aspirational updates are the enemy. A decision that cannot be checked in 90 days for whether it was followed is not a decision. An update that cannot be diffed against a file is not an update. We refuse vagueness.

The Sunday review is short and unglamorous. It is also the highest-leverage hour of the week. Without it, the artifacts accumulate without being internalized. With it, they become the operator's default thinking.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
