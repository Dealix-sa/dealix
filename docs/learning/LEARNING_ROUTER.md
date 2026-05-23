---
title: Learning Router
owner: Learning Lead
status: active
last_review: 2026-05-23
---

# Learning Router — موجّه إشارات التعلّم

## Purpose

Every signal Dealix produces must land in exactly one bucket. The router defines the buckets, the tag taxonomy, and the rule that promotes a recurring signal into an asset.

## Learning Rule (verbatim)

- Issue once = log it
- Twice = checklist item
- Three times = playbook update
- Five times = template
- Ten times = automate/productize

## Buckets

| Bucket | Destination doc / artifact | Promotion target |
|---|---|---|
| Experiment outcome | [EXPERIMENT_SYSTEM.md](./EXPERIMENT_SYSTEM.md) | playbook section |
| Win/loss reason | [WIN_LOSS_REVIEW.md](./WIN_LOSS_REVIEW.md) | sales checklist |
| Message variant performance | [MESSAGE_PERFORMANCE.md](./MESSAGE_PERFORMANCE.md) | message template |
| Sector traction | [SECTOR_PERFORMANCE.md](./SECTOR_PERFORMANCE.md) | sector report |
| Pricing signal | [PRICING_LEARNING.md](./PRICING_LEARNING.md) | pricing logic update |
| Productization candidate | [docs/09_capital_os/PRODUCTIZATION_LEDGER.md](../09_capital_os/PRODUCTIZATION_LEDGER.md) | productized asset |
| Delivery anomaly | [docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md) | runbook step |
| Trust / safety signal | [docs/trust/TRUST_COMMAND_CENTER.md](../trust/TRUST_COMMAND_CENTER.md) | control update |

## Tag taxonomy

`signal:` `pipeline | message | sector | price | delivery | win_loss | trust | productize`
`severity:` `info | repeat | pattern | systemic`
`status:` `logged | checklist | playbook | template | productized | killed`

## Operations

1. Anyone in the team writes a one-line signal: tag, evidence link, observed-by, date.
2. Router owner reviews intake daily, assigns to bucket, applies severity.
3. On the third occurrence of the same pattern, owner files a playbook PR. On the fifth, a template. On the tenth, a productization row.
4. Promotions are visible in the weekly review.

## Evidence

- Router intake file: `dealix-ops-private/learning/router_intake.csv`.
- Promotion log: `dealix-ops-private/learning/promotions.md` — one row per promotion, with commit SHA and decision date.
- Killed signals (decided to stop tracking) are kept with reason.

## Owner & cadence

- Learning Lead reviews intake daily.
- Promotion decisions confirmed at the Sunday review.

## AR — ملخّص

موجّه التعلّم يحدّد سلال الإشارات (تجربة، فوز/خسارة، رسالة، قطاع، سعر، تسليم، ثقة، منتج) والوسوم والحالات. كل إشارة تدخل بوسم، وتترقّى وفق قاعدة 1-2-3-5-10 إلى قائمة تحقق ثم playbook ثم قالب ثم منتج. القيمة التقديرية ليست قيمة مُتحقَّقة.
