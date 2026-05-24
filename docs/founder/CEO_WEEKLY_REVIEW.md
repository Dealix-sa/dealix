# CEO Weekly Review

The Sunday 09:00 review. Required, even when nothing went wrong.

## Purpose

Force a once-a-week pause to look at trend lines instead of point-in-time
numbers. Confirm the operating system is still pointed at the right
beachhead and the right KPIs.

## Owner

Founder.

## Cadence

Sunday 09:00 Asia/Riyadh. Lasts 60 minutes. Skipping it counts as a
failure mode in `docs/governance/RISK_REGISTER.md`.

## Source of Truth

- Last 7 daily briefs (`data/founder_briefs/`)
- Decision log delta (`docs/founder/CEO_DECISION_LOG.md`)
- Drift report (`docs/ops/DEALIX_FINAL_READINESS_REPORT.md`)
- Friction log (per-customer issues raised)

## Inputs

- KPI 7-day trend
- Pipeline conversion delta
- Approval queue throughput
- Agent eval drift (if any)

## Outputs

- A one-paragraph summary written into this file (rolling, last 8 weeks
  retained)
- An updated "next week's top three"
- Any new decisions added to the decision log

## KPI

- Review held on Sunday (52/52 weeks/year goal)
- Top three for the next week recorded by Sunday 11:00
- Trend report exported by Sunday 12:00

## Trust Boundary

Internal only. Nothing from this review leaves the company without going
through `docs/trust/LIVE_SEND_SAFETY_GATE.md`.

## Failure Mode

- Review skipped → recovery path triggers.
- Review held but no top-three recorded → counted as half-done.
- Decisions not written down → not made.

## Recovery Path

1. If skipped, hold it Monday. Note the slip in this file.
2. If skipped twice in a row, treat as a CEO OS failure and escalate via
   `docs/governance/INCIDENT_RESPONSE.md`.

## Verification

```bash
make business-os
python scripts/verify_everything.py --layer ceo_operating_system
```

## Next Action

Sunday morning, open this file. Write last week's summary. Pick next
week's top three. Close the laptop.
