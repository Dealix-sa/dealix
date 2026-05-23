# Account Scoring Model | نموذج تقييم الحسابات

## Purpose | الغرض
Score every Saudi B2B account on a single 0-100 scale, then bucket into A / B / C
/ Reject. The score decides which machine the account enters and how much founder
attention it deserves.

The score never claims revenue, never commits to a deal, and never bypasses
approval.

## Inputs | المدخلات
- Sector ranking
- ICP segmentation
- Buyer persona match
- Trigger events
- Competitive presence
- Proof artifact match
- Partner relationship signal

## Scoring fields | حقول التقييم
| Field | Range | Weight | Description |
|---|---|---|---|
| Saudi relevance | 0-10 | 10% | KSA HQ, branch, buyer presence, spend signal |
| B2B fit | 0-10 | 10% | sells to businesses, not consumers |
| High-ticket potential | 0-10 | 15% | estimated deal size based on public signals |
| Buyer clarity | 0-10 | 12% | named decision maker identifiable |
| Pain urgency | 0-10 | 15% | triggers in last 90 days |
| Outreach fit | 0-10 | 8% | channel openness (LinkedIn / email / form) |
| Proof fit | 0-10 | 10% | Dealix has a relevant proof artifact |
| Partner potential | 0-10 | 5% | channel multiplier vs direct sale |
| Delivery complexity | 0-10 | 8% | inverse score: simpler = higher |
| Trust risk | 0-10 | 7% | inverse score: lower risk = higher |
| **Final priority** | 0-100 | — | weighted sum |

## Bucketing | التصنيف
- **A** (>= 75): top priority, ABM Strategic Account Machine
- **B** (55-74): standard outbound queue
- **C** (35-54): nurture only
- **Reject** (< 35 OR trust risk >= 8): excluded, reason logged, 90-day cooldown

## Tie-breakers | كسر التعادل
- Higher Saudi relevance wins
- Then higher buyer clarity
- Then more recent trigger event

## Recalibration | إعادة المعايرة
- Daily: scores refreshed for accounts with new triggers
- Weekly: full re-rank of A and B buckets
- Monthly: founder reviews weighting and may adjust (A1 internal change,
  weights publication is A2)

## Decision rules | قواعد القرار
- A-bucket → ABM machine, founder-touched
- B-bucket → Outbound machine, drafts auto-generated
- C-bucket → Nurture machine, low-cadence
- Reject → excluded, reason logged, cooldown enforced
- Trust risk overrides everything: any account with trust risk >= 8 is auto-Reject

## Data source | مصدر البيانات
`intelligence.accounts`, `intelligence.scores`, `intelligence.trigger_events`,
`proof.artifacts`, `partners.relationships`.

## Approval class | فئة الموافقة
- A1: scoring refresh, bucket changes inside the existing weighting model
- A2: weighting change, new field added, threshold change
- A3: scoring rule applied to a regulated sector / government account

## Trust gate | بوابة الثقة
- Score must cite at least 3 evidence rows
- No score is presented as a revenue forecast — only a priority
- Trust risk field can never be auto-overridden
- Policy snapshot + audit row per recalibration

## Owner | المالك
Founder owns the weighting model. Worker runs the math.

## Worker name
`intelligence.account_scorer`

## KPI | المؤشرات
- A-bucket → proposal conversion rate (rolling 90d)
- A-bucket → paid conversion rate
- Reject precision: % of rejects that did not later become A/B
- Drift: % weekly bucket movement (should be modest, < 25%)

## Failure mode | حالات الفشل
- Score inflation from a single overweighted source
- Trust risk field decayed silently
- A-bucket overflows founder capacity

## Recovery path | مسار الاسترداد
- Per-source contribution cap inside each field
- Trust risk recomputed monthly from fresh sources
- A-bucket cap: max 50 active accounts at once; overflow demoted to B with
  reason logged
