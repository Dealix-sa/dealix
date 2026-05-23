# Experiment System

Real growth needs structured experiments — not vibes, not "let's try
something this week".

The public schema lives here. The actual experiments are logged in the
**private** founder repo as `learning/experiment_log.md`.

## Experiment Format

| Field      | Description              |
|------------|--------------------------|
| Hypothesis | What we believe          |
| Segment    | Who we test              |
| Action     | What we do               |
| Metric     | What we measure          |
| Result     | What happened            |
| Decision   | Build / Fix / Kill / Defer |

## Example

| Field      | Value                                                                  |
|------------|------------------------------------------------------------------------|
| Hypothesis | ERP providers respond better to "qualified Saudi B2B opportunities" than "AI revenue system". |
| Segment    | ERP/CRM Saudi companies.                                               |
| Action     | Send 25 DMs.                                                           |
| Metric     | Reply rate.                                                            |
| Result     | Pending.                                                               |
| Decision   | Pending.                                                               |

## Cadence Rule

At least **one experiment per week** must be running. An empty
experiment log for two consecutive weeks is itself an escalation
(`docs/ops/ESCALATION_MATRIX.md`, Yellow).

## Decision Discipline

Every closed experiment must end with one of:

- **Build**  -- promote into a template / workflow / product feature.
- **Fix**    -- the result was negative due to execution, not hypothesis.
- **Kill**   -- the hypothesis is wrong; stop.
- **Defer**  -- inconclusive; schedule re-run with sharper metric.

"Inconclusive" without a deferred re-run date is not allowed.
