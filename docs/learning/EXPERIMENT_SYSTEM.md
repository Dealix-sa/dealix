# Experiment System — نظام التجارب

## Purpose
Define how Dealix runs disciplined experiments: hypothesis stated, metric named, sample sized, duration set, kill rule defined. Experiments without these are guesses.

## Owner
Founder.

## Inputs
- Hypothesis from any operator.
- Open questions from the weekly intelligence review.
- Sprint defects or successes that suggest a testable change.

## Outputs
- Experiment register entries.
- Closed-experiment conclusions in `docs/learning/COMPANY_MEMORY.md`.

## Rules (numbered)
1. Every experiment has a written hypothesis before it starts.
2. Every experiment names one primary metric and one guardrail metric.
3. Every experiment has a sample size and a duration before it starts.
4. Every experiment has a kill rule: a condition under which we stop early.
5. No experiment runs against client artifacts without explicit consent if results affect the client.
6. Experiments are closed with a written conclusion, regardless of outcome.

## Metrics
- Experiments closed with a conclusion (target greater than or equal to 80 percent).
- Experiments that hit kill rule (target less than 40 percent; higher means hypotheses are too weak).
- Mean time from hypothesis to start.

## Cadence
At least one new or closed experiment per week.

## Evidence (paths)
- `docs/learning/registers/experiments/EX-NNNN.md`
- `docs/learning/COMPANY_MEMORY.md` for conclusions.

## Verifier
Founder.

## Runtime Command
`make learning.experiment.new TITLE=<t>` scaffolds an experiment file.

## Experiment file structure

```
ID: EX-NNNN
Title: short
Hypothesis: <if we change X, we expect metric Y to move in direction Z by magnitude W>
Primary metric: <single number, measurable>
Guardrail metric: <metric that must NOT degrade>
Sample size: <N sprints / N messages / N rows>
Duration: <start date, end date>
Kill rule: <condition that stops the experiment before duration>
Owner: <name>
Status: open | closed
Conclusion: <written after close: did the hypothesis hold? what is the operating change?>
```

## Sample size guidance

For sprint-level experiments: 5 sprints minimum, 10 preferred. Below 5, results are anecdotal.

For message-level experiments: 50 messages per variant minimum. We are measuring direction, not precision; we do not need power calculations for the magnitudes Dealix experiments typically observe.

For row-level experiments (scoring rubric changes): 200 rows minimum, sampled across at least 3 sprints.

## Kill rules

Default kill rules to consider for any experiment:

- Guardrail metric degrades by more than X percent: stop.
- Operator workload exceeds the agreed budget by more than 20 percent: stop.
- Client complaint received: stop and review.
- Half the duration elapsed and primary metric trend is opposite of hypothesis: stop.

## Worked example

ID: EX-0007
Title: Three-variant vs two-variant message packs
Hypothesis: If we ship three variants per channel instead of two, client-reported reply rates will improve by at least 15 percent over 8 sprints, without increasing operator hours by more than 15 percent.
Primary metric: client-reported reply rate at 30-day check-in.
Guardrail metric: operator hours per sprint.
Sample size: 8 sprints.
Duration: 2026-06-01 to 2026-07-26.
Kill rule: operator hours per sprint exceed 20 percent of baseline at midpoint.
Owner: Head of Delivery.
Status: open.

## Operating substance
Experiments are how Dealix replaces "I think this would work" with "we ran it and learned X". The cost of an experiment is small relative to the cost of running a process for a year on a wrong assumption.

The kill rule is the most-skipped element and the most important. Without a kill rule, experiments run too long, drain operator attention, and produce ambiguous results. With a kill rule, we either learn or we save the cost.

Closed-with-conclusion is mandatory. An experiment that quietly ended is worse than an experiment that was killed; it consumed effort and produced no signal. Even negative results (hypothesis did not hold) are valuable when they are written down.

The cadence of one experiment per week is achievable because experiments do not need to be large. A two-week, eight-sprint experiment is normal. Running one at a time is fine. Stacking too many is the failure mode.

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
