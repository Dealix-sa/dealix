# Experiment Backlog

The Dealix experiment backlog. Sorted by (impact × confidence ÷ effort). Capped at 2 in-flight at any time.

## 1. Schema

```
experiment_id, title, status, bottleneck,
hypothesis, owner, time_box_days,
success_metric, kill_criterion, rollback_plan,
started_at, ended_at, decision, learning_link
```

`status` is one of: `proposed | active | scaled | killed | fixed`.

## 2. Doctrine

- **No more than 2 active.** Forces focus.
- **Every active experiment has a kill criterion.** Date-bounded.
- **Every closed experiment has a learning note** in `LEARNING_LOOP.md`.

## 3. Seeded backlog (proposed, illustrative)

### E-001 — Subject line A/B for P-CRO outbound

- **Status:** proposed
- **Bottleneck:** Sent → Reply < 8%
- **Hypothesis:** Subject lines that include a KSA mega-project reference reply 1.5x more than generic "open pipeline question" lines.
- **Owner:** Founder
- **Time-box:** 14 days
- **Success metric:** Reply rate ≥ 12% in the variant arm
- **Kill criterion:** Reply rate < 8% across both arms after 14 days
- **Rollback:** Revert all approved drafts to the baseline subject

### E-002 — Bilingual proof pack vs. EN-only

- **Status:** proposed
- **Bottleneck:** Sample → Proposal < 50%
- **Hypothesis:** Buyers asked to provide a sample receiving a bilingual Proof Pack convert to Proposal 1.3x more than EN-only.
- **Owner:** Founder + Distribution Operator
- **Time-box:** 21 days
- **Success metric:** Proposal conversion ≥ 60% in the bilingual arm
- **Kill criterion:** No statistical difference after 21 days
- **Rollback:** Revert to EN-only proof pack as default

### E-003 — Reduce first-touch length to ≤ 80 words for LinkedIn

- **Status:** proposed
- **Bottleneck:** Sent → Reply on LinkedIn channel < 5%
- **Hypothesis:** Cutting LinkedIn first-touch length by 30% lifts reply rate.
- **Owner:** Founder
- **Time-box:** 14 days
- **Success metric:** Reply rate ≥ 8% on LinkedIn arm
- **Kill criterion:** Reply rate < 4% on the shortened arm
- **Rollback:** Revert length cap

## 4. Active experiments

(none — populate as the loop runs)

## 5. Closed experiments

(none — populate as experiments end)

## 6. Learning

See `LEARNING_LOOP.md` for accumulated learning from closed experiments.
