# Client Tiering — تصنيف العملاء

## Purpose
Tier every active client so the founder spends time where it matters. Tiering is by strategic value and current state, not by deal size alone. Four tiers, clear thresholds, named action.

## Owner
Founder. Reviewed monthly.

## Inputs
- Engagement value (annualized).
- Strategic value (sector signal, reference, productization input).
- Health score from `docs/client_success/CLIENT_HEALTH_SCORE.md`.
- Renewal probability.

## Outputs
- Tier assigned per client.
- Action cadence per tier.
- Founder calendar allocation per tier.

## The Four Tiers
| Tier | Definition | Founder time/week | Cadence |
|---|---|---|---|
| **Strategic** | High strategic value (reference, productization input, sector authority) OR ≥ 30k SAR/month | ≥ 2 hours | Weekly call + weekly report |
| **Growth** | Stable, expanding scope, ≥ 10k SAR/month | 1 hour | Bi-weekly call + weekly report |
| **Maintenance** | Stable, no expansion, < 10k SAR/month | 30 minutes | Monthly call + weekly report |
| **At-Risk** | Health score < 40 OR escalation in last 30 days | ≥ 2 hours until resolved | Daily until resolved |

## Rules
1. No more than 5 Strategic clients at any time pre-hire; founder cannot serve more.
2. Tier upgrade requires evidence (signed scope, stated reference willingness).
3. Tier downgrade requires explicit decision (no drift).
4. At-Risk overrides all other tiers until resolved.
5. Founder calendar must reflect tier allocation; weekly review of calendar vs tier plan.
6. The disclosure "Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة" applies to projected revenue figures.

## Metrics
- Count per tier.
- Founder time-actual vs time-plan per tier (variance ≤ 20%).
- Tier movement up vs down (quarterly).
- At-Risk resolution time (target ≤ 14 days).

## Cadence
- Monthly tier review.
- Weekly Strategic check-in.
- Bi-weekly Growth check-in.

## Evidence
- `evidence/client-success/tiering/<YYYY-MM>.md` snapshot.

## Verifier
Founder.

## Runtime Command
`make tier-review` — lists current tiering, founder time variance, flags drift.

## Arabic Summary — ملخص عربي
أربع فئات للعملاء: استراتيجي، نمو، صيانة، خطر. الوقت الذي يخصصه المؤسس يتبع الفئة، لا حجم الصفقة فقط. الخطر يتجاوز كل الفئات حتى يُحل. القيم التقديرية ليست مُتحقَّقة.
