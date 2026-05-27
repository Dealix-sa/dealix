# Hermes Founder Cockpit Plan

The Founder Cockpit is a future private view for Hermes review summaries. It should show priorities, review status, and next work items without exposing private data.

## Goal

Give the founder one place to see:

- Recent Hermes reviews.
- Items needing attention.
- Highest-value opportunities.
- Readiness concerns.
- Suggested next PRs.

## Initial data sources

Start from local artifacts:

- `data/hermes/review_records.jsonl`
- `data/hermes/founder_digest.md`
- `data/hermes/weekly_strategy.md`

Keep private working files local.

## Suggested cards

| Card | Purpose | Source |
| --- | --- | --- |
| Agent status | Registered agents and last run time | review records |
| Open reviews | Founder decisions pending | review records |
| Opportunities | Ranked commercial items | future revenue artifact |
| Readiness | Product and operations notes | future ops artifact |
| Cost notes | Provider and margin notes | future finance artifact |
| Next PR queue | Recommended implementation order | weekly strategy |

## Private export plan

Future script:

```text
scripts/export_hermes_cockpit.py
```

Suggested private output:

```text
data/hermes/hermes-status.json
```

Use private local output first. Add public/static exports only after a redaction step exists.

## JSON shape

```json
{
  "generated_at": "ISO-8601 timestamp",
  "mode": "dry_run",
  "agents_total": 8,
  "reviews_total": 8,
  "open_reviews": 8,
  "high_risk_reviews": 0,
  "top_next_steps": [
    "Connect read-only PR review source",
    "Add founder digest sections",
    "Add weekly strategy artifact"
  ]
}
```

## Acceptance criteria

- Export runs locally without network calls.
- Export contains no secrets.
- Export avoids private customer information.
- View can render with missing optional fields.
- CI checks JSON validity when the exporter is added.

## Future enhancements

1. Trend fields by week.
2. Agent health history.
3. Issue and PR links for follow-up work.
4. Provider usage summary after cost telemetry exists.
5. Vertical opportunity status for Saudi sectors.
