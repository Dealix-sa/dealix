# reports/distribution/ — generated artifacts

These markdown reports are **generated** by the distribution scripts (and the
scheduled workflows). They are committed at a clean zero baseline; regenerate
them any time:

```bash
make distribution-day        # → DISTRIBUTION_DAY.md
make draft-quality           # → DRAFT_QUALITY_GATE.md
make distribution-metrics    # → DISTRIBUTION_METRICS.md
```

| Report | Script | Workflow |
|--------|--------|----------|
| `DISTRIBUTION_DAY.md` | `scripts/distribution_day.py` | `distribution_draft_day.yml` |
| `DRAFT_QUALITY_GATE.md` | `scripts/check_draft_quality.py` | `distribution_draft_day.yml` |
| `DISTRIBUTION_METRICS.md` | `scripts/distribution_metrics.py` | `distribution_draft_day.yml`, `distribution_weekly_review.yml` |

All three are read-only / draft-only. Numbers come only from the
`distribution_os` JSONL stores (in `var/`) and are never invented; nothing here
sends a message or charges a customer.
