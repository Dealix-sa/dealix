# Productization Command Center

> Build only from what repeats. Productize what works.

## Today

| Field | Value |
|-------|-------|
| Workflows at 3 successes (documentable) | _list_ |
| Workflows at 5 successes (templatable) | _list_ |
| Workflows at 10 successes (automatable) | _list_ |
| Repeated customer asks (SaaS candidates) | _list_ |
| Active feature builds | _list_ |
| Feature builds blocked | _list_ |

## The Productization Stack

| File | Purpose |
|------|---------|
| `PRODUCTIZATION_ENGINE.md` | The rule: manual → document → template → automate |
| `FEATURE_INTAKE.md` | How a build request becomes a build |
| `BUILD_DEFER_KILL.md` | How we decide |
| `NO_OVERBUILD_POLICY.md` | What we refuse to build |
| `DORA_METRICS_POLICY.md` | Engineering health |
| `ENGINEERING_HEALTH_REVIEW.md` | Monthly review |
| `ROADMAP.md` | The current short list (not a long arc) |

## The Productization Rule

```
3 manual successes  →  document the workflow
5 successes         →  template the workflow
10 successes        →  automate the workflow
repeated customer ask  →  SaaS candidate (not yet built)
```

Anything below 3 successes is **not** ready to productize.
A "productized" workflow at 1 success is a mock-up, not a product.

## Metrics

- Workflows promoted to template this month
- Workflows promoted to automation this month
- Build-defer-kill ratio (ideally many kills, fewer builds)
- DORA: deployment frequency, lead time, change failure rate, restore time
- Founder hours on build vs revenue (target: revenue >> build pre-PMF)

## Linked Sources

- `dealix-ops-private/product/workflow_success_log.csv` — successes per
  workflow, dated and evidence-linked
- `dealix-ops-private/product/feature_intake.md` — current queue
