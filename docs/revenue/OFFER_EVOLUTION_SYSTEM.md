# نظام تطور العروض — Offer Evolution System

> 3 successes → doc. 5 successes → template. 10 successes → automate or productize.

## Purpose
Force offers to graduate based on evidence, not founder excitement. Prevent premature productization. Prevent indefinite project mode.

## Owner
Founder/CEO.

## Inputs
- Successful runs of each offer rung (from `OFFER_LADDER.md`).
- Sprint records (`docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`).
- Case-safe artifacts.
- Delivery time and margin actuals.

## Outputs
- Counter per offer-shape.
- Graduation events logged in Monthly Strategy Review.
- Productization candidates list.

## Rules
1. A "successful run" requires: paid in full, delivered to scope, case-safe artifact published.
2. Counters reset only by an A2 Go/No-Go gate; otherwise they accumulate.
3. Graduation actions happen by the Monthly Strategy Review after the threshold is reached. Not earlier, not silently.
4. An offer-shape that does not reach 3 successes within 12 months of first run enters a kill review.
5. Productization (10 successes) requires a written productization plan, capacity, and capital allocation before any external announcement.

## Metrics
- Counter per offer-shape (current count).
- Time from 1st to 3rd success (sets the rhythm).
- Productization conversion rate (10-success cohorts that ship productized version): track.

## Cadence
Counters updated Weekly. Graduation reviewed Monthly.

## Evidence
`dealix-ops-private/offers/counters.json` and graduation event files.

## Verifier
`make offer-evolution-verify` — checks counters match recorded successful runs.

## Runtime Command
`make offer-counter-refresh`

---

## The Three Thresholds

### Threshold 1 — 3 successes → DOC
At 3 successful runs of the same offer shape, Dealix produces:
- A written playbook in `docs/03_commercial_mvp/` describing scope, timeline, role, deliverables, and pitfalls.
- An updated `OFFER_LADDER.md` entry with refined price band and effort estimate.
- A case-safe template in `docs/case-studies/` (or sector report contribution).

### Threshold 2 — 5 successes → TEMPLATE
At 5 successful runs, Dealix produces:
- A standardized proposal template (`templates/PROPOSAL_<shape>.md.j2`).
- A delivery template (sprint plan, weekly cadence, artifacts list).
- A retainer attach script (talking points for the post-sprint retainer offer).

### Threshold 3 — 10 successes → AUTOMATE / PRODUCTIZE
At 10 successful runs, Dealix considers productization:
- Decide: Managed Pilot variant, Dealix OS module, or training course.
- Build the productized version on a declared bet in `STRATEGIC_BETS.md`.
- Capacity and capital allocated before any external launch.

## Counter rules
- Same "shape" means same problem, same delivery template, same artifact type. Different sectors with the same shape count to the same counter.
- A run that was paid but produced no artifact does not count (Trust failure).
- A run that produced an artifact but was discounted > 20% counts at half value (5 such runs = 2.5 toward the counter — round down at threshold checks).

## Graduation file template

```
# Offer Graduation — <offer-shape>
Threshold reached: 3 / 5 / 10
Date: YYYY-MM-DD
Triggering run id: <sprint id>

## Counter history (last 5 runs)
| Run id | Customer (anon) | Sector | SAR | Margin | Artifact |
|---|---|---|---|---|---|

## What graduates this month
- Doc updated: <path>
- Template created: <path>
- Productization plan: <path or "not yet">

## Capacity check
Hours / month required to maintain template: <N>
Owner: <name>

## Next steps
1.
2.
```

## What blocks graduation
- Trust dashboard has an open flag on a contributing run.
- Margin trend is degrading across the last 3 runs.
- Capacity to maintain the template does not exist.
- Founder cannot delegate; productization without delegation is not productization.

## Anti-patterns
- Productizing at 2 successes because the founder "feels good" about the shape.
- Refusing to productize at 10 successes because "every customer is different".
- Counting unpaid pilots toward the threshold.

## القواعد العربية
1. الجولة الناجحة: مدفوعة كاملةً، مسلَّمة، ودليل مجهول الهوية منشور.
2. العتبات: 3 → وثيقة، 5 → قالب، 10 → ترقية إلى منتج.
3. الترقية تتم في المراجعة الشهرية، لا تلقائيًا.

## Cross-links
- `OFFER_LADDER.md`
- `REVENUE_MODEL.md`
- `docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`
- `docs/founder/MONTHLY_STRATEGY_REVIEW.md`
- `docs/strategy/STRATEGIC_BETS.md`
