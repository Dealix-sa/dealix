# Targeting Scorecard

> كل شركة لها score، وكل score له سبب، وكل target له evidence.

The scorecard turns a company profile into an auditable score out of 100. The
weights live in `data/targeting/scoring_weights.yml`; the engine is
`scripts/targeting_scorecard.py`.

```
score = Σ axis_points (each capped at axis max) − penalties, clamped to [0,100]
```

---

## Positive axes (max 100)

| Axis | Points | What it measures |
|------|--------|------------------|
| ICP Fit | 25 | match to the Ideal Customer Profile (sector `icp_weight` × 25, +b2b) |
| Pain Signal | 20 | observable problems Dealix can solve (`signals.yml` pain signals) |
| Timing / Intent | 15 | hiring, growth, partnership, tech, news signals |
| Access | 10 | quality of the official contact channel |
| Dealix OS Fit | 10 | how cleanly the pain maps to an OS angle |
| Evidence Confidence | 10 | number of independent sources (`evidence_count × 3`, capped) |
| Strategic Value | 10 | market density (`cities.yml`) + partner potential |

---

## Penalties (subtractive)

| Reason | Penalty |
|--------|---------|
| Single source only | −10 |
| No official website | −10 |
| No pain signal | −15 |
| Sensitive sector | −15 |
| Weak contact channel | −10 |
| Compliance risk (personal phone / robots ignored) | **reject** |
| Generic-message risk (thin pain + thin evidence) | −10 |

A `reject` zeroes the score and removes the company from outreach.

---

## Decision bands

| Score | Grade | Decision | AR |
|-------|-------|----------|----|
| 90–100 | A+ | review today | راجع اليوم |
| 80–89 | A | strong target | هدف قوي |
| 70–79 | B | needs more research | يحتاج بحث إضافي |
| 60–69 | C | nurture later | رعاية لاحقًا |
| < 60 | D | do not target now | لا يُستهدف الآن |

Founder shortlist = grade **A and up**, top **20** (configurable).

---

## Run

```bash
python scripts/targeting_scorecard.py \
  --in data/targeting/company_master.jsonl --out data/targeting/out --top 80
```

Output `out/ranked_targets.csv` carries the top axis reasons per company so the
score is explainable at a glance. The full per-axis breakdown + reasons is
available from `score_company()` programmatically.

---

## Acceptance (scoring)

- [ ] Every company has a score in `[0, 100]`.
- [ ] Every score has per-axis reasons.
- [ ] Every penalty is itemized.
- [ ] Compliance-risk companies are rejected, never surfaced.

Tested by `tests/test_targeting_scorecard.py`.
