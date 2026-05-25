# شجرة مؤشرات الأداء — CEO KPI Tree

> One north-star metric branches into five sub-trees. Every KPI traces upward.

## Purpose
Make the relationship between the north star and every operational metric explicit. No orphan metrics. No vanity numbers.

## Owner
Founder/CEO.

## Inputs
- North-star definition (`docs/strategy/NORTH_STAR.md`)
- Revenue metrics (`docs/revenue/REVENUE_METRICS.md`)
- Delivery metrics (sprint factory)
- Trust metrics (`docs/14_trust_os/TRUST_DASHBOARD.md`)
- Learning metrics (`docs/learning/`)

## Outputs
- Weekly KPI snapshot in `dealix-ops-private/kpi/YYYY-WW.json`
- Tree drift report (KPI moved > 20% week-over-week)

## Rules
1. Every KPI on the tree has: definition, formula, source, owner, target, current.
2. No KPI exists without a parent (except the north star).
3. If a sub-KPI is green but its parent is red, the sub-KPI is mis-defined — fix the definition.
4. Vanity metrics (followers, impressions, page views in isolation) do not enter the tree.
5. Targets are reset quarterly, not monthly. Monthly is for actuals, not goal-shifting.

## Metrics
- Tree coverage: 100% of KPIs have all six fields filled.
- Tree freshness: every KPI updated ≤ 7 days.
- Tree integrity: zero orphan KPIs.

## Cadence
Weekly snapshot. Quarterly target reset.

## Evidence
`dealix-ops-private/kpi/` — JSON snapshots per week.

## Verifier
`make kpi-tree-verify` — checks coverage, freshness, integrity.

## Runtime Command
`make kpi-snapshot`

---

## The Tree

```
NORTH STAR
  └─ Paid Sprints Delivered with Evidence (per quarter)
       │
       ├─ REVENUE
       │    ├─ Qualified leads / week
       │    ├─ Proposal-to-payment rate
       │    ├─ Average sprint value (SAR)
       │    ├─ Retainer attach rate (post-sprint)
       │    └─ MRR (recurring retainers only)
       │
       ├─ DELIVERY
       │    ├─ Sprints on-time %
       │    ├─ Sprint-to-evidence rate (proof shipped)
       │    ├─ Delivery NPS (post-sprint, ≥ 5 responses)
       │    └─ Defect/refund rate
       │
       ├─ TRUST
       │    ├─ Trust artifacts shipped / quarter
       │    ├─ Open compliance flags
       │    ├─ Disclosure coverage on customer-facing docs (%)
       │    └─ Refund incidents / quarter
       │
       ├─ LEARNING
       │    ├─ Docs updated from delivery / week
       │    ├─ Offer-evolution events (3/5/10 thresholds)
       │    └─ Kill decisions logged / month
       │
       └─ FOUNDER LEVERAGE
            ├─ Revenue per founder-hour (rolling 30d)
            ├─ % founder time on A-tier work
            └─ Sprint count not requiring founder execution
```

## KPI definition template
```json
{
  "id": "REV-PROP-PAY",
  "name": "Proposal-to-payment rate",
  "definition": "Paid proposals / Sent proposals, rolling 30 days",
  "formula": "count(paid) / count(sent)",
  "source": "docs/revenue/PIPELINE_STAGES.md",
  "owner": "Founder/CEO",
  "target_q": 0.30,
  "current": 0.00,
  "updated": "YYYY-MM-DD"
}
```

## Anti-vanity filter
A KPI enters the tree only if it answers yes to: Does a 20% move change a Founder decision this quarter?

## القواعد العربية
1. لكل مؤشر تعريف، مصدر، مالك، وهدف.
2. لا مؤشرات يتيمة. كل فرع يعود إلى النجم القطبي.
3. مؤشرات الغرور (متابعون، مشاهدات) لا تدخل الشجرة.

## Cross-links
- `docs/strategy/NORTH_STAR.md`
- `docs/revenue/REVENUE_METRICS.md`
- `docs/founder/FOUNDER_LEVERAGE_INDEX.md`
- `docs/14_trust_os/TRUST_DASHBOARD.md`
