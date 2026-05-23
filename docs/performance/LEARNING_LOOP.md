# Learning Loop

DEALIX · INTELLIGENT DEALS. REAL GROWTH. · Driven by Growth · Focused on Results.

The Learning Loop is the discipline by which closed experiments
become permanent improvements in the revenue motion. Without an
explicit loop, lessons evaporate. With a loop, they compound.

The loop has four artifacts and one cadence.

## Artifacts

| Artifact                  | Location                                      | Purpose                                                  |
| ------------------------- | --------------------------------------------- | -------------------------------------------------------- |
| Experiment log            | `distribution/experiment_log.csv`             | Source of result bands.                                   |
| Close report (one page)   | Founder Console attachment per experiment id  | Hypothesis, cohort, result, lesson.                       |
| Lesson register           | `performance/lessons.csv` (private ops)       | Append-only ledger of lessons by KPI node.                |
| Playbook updates          | `docs/playbooks/...` (changes via PR)         | Permanent codification when a lesson is durable.          |

The lesson register is not in the bootstrap; it is created on first
write by the Performance Analyst. Schema:

| Column          | Notes                                                  |
| --------------- | ------------------------------------------------------ |
| `id`            | `lesson_yyyy_mm_id` format.                            |
| `experiment_id` | Source experiment id.                                  |
| `kpi_node`      | The KPI tree node the lesson is attached to.           |
| `cohort`        | Sector / channel / segment.                            |
| `lesson`        | One sentence.                                          |
| `confidence`    | `low`, `medium`, `high`.                               |
| `recorded_at`   | ISO ts.                                                |
| `owner`         | Accountable agent.                                     |

## Cadence

| Activity                  | Cadence  | Owner                  |
| ------------------------- | -------- | ---------------------- |
| Close report drafted      | At end of each experiment | Performance Analyst    |
| Lesson register append    | Weekly   | Performance Analyst    |
| Playbook update review    | Monthly  | Founder + agents       |
| Lesson archaeology        | Quarterly| Growth Strategist      |

## Lesson archaeology

The quarterly lesson archaeology walks the lesson register and asks
three questions for each lesson:

1. Has the lesson been honored in subsequent drafts and offers?
2. Has the lesson been contradicted by later experiments?
3. Has the lesson been codified into a playbook?

If a lesson has not been honored, the Growth Strategist raises a
trust flag at severity `medium`. If it has been contradicted, both
lessons remain in the register; a new experiment is queued to
resolve. If it has not been codified after two quarters, it is
either downgraded to `low` confidence or codified.

## Confidence levels

| Confidence | Meaning                                                                |
| ---------- | ---------------------------------------------------------------------- |
| low        | One experiment, small cohort, single window.                           |
| medium     | Two or more experiments, two cohorts or two windows, consistent result.|
| high       | Three or more experiments across cohorts, durable over a quarter.      |

Only `high` confidence lessons are reflected in external proof
language (and even then, only through the proof library gate).

## The cycle

```
hypothesis (backlog draft)
    │
    ▼
running (the experiment)
    │
    ▼
close report (one page)
    │
    ▼
lesson register (one row)
    │
    ▼
playbook update (a PR) -or- new experiment (back to backlog)
```

The cycle closes only when a lesson reaches one of two destinations:
a permanent playbook update or a follow-up experiment. Lessons that
sit in the register without a destination are work in progress.

## What lessons are not

| Not a lesson                                                | Why                                                                          |
| ----------------------------------------------------------- | ---------------------------------------------------------------------------- |
| "We should try X." (no experiment behind it)                | That is a hypothesis. Add it to the backlog.                                  |
| "Sector A is great." (no measured delta)                   | That is an impression. Lessons must carry a measured delta.                   |
| "We learned a lot." (no specific takeaway)                  | Lessons are one sentence with a verb and a noun.                              |
| "Avoid offering discounts." (already a policy)              | Restating a policy is not a lesson.                                          |
| "Our brand voice is good." (no measurement)                 | Not a lesson; a vibe check.                                                  |

## Founder Console exposure

The lesson register is not yet exposed via an endpoint. The
Performance Analyst surfaces lessons in the founder brief and in the
weekly scorecard refresh. A future endpoint
`/api/v1/internal/performance/lessons` is planned; until then the
file is read directly from the private ops runtime by the analyst.

## Discipline

1. Every closed experiment yields a close report.
2. Every close report yields a lesson register row.
3. Every register row points to a destination: codify or re-test.
4. Confidence rises with evidence, not with time alone.
5. Lessons are operational; external claims must still trace to the
   proof library, not to the lesson register.

## Reference

- `EXPERIMENT_BACKLOG.md` — where hypotheses live.
- `REVENUE_KPI_TREE.md` — which nodes a lesson can attach to.
- `WIN_LOSS_ANALYSIS.md` — how aggregate outcomes feed the loop.
- `NEXT_BEST_ACTION_ENGINE.md` — how the loop influences the next
  recommended action.
