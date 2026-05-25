---
title: Offer Evolution System
owner: Founder
status: active
last_review: 2026-05-23
---

# Offer Evolution System — نظام تطوير العروض

## Purpose

Offers get better only if win/loss data feeds back into them. This page is the loop: collect, classify, decide, ship.

## Inputs (collected continuously)

| Source | Captured as |
|---|---|
| Won deals | `dealix-ops-private/revenue/wins/<deal_id>.md` — what tipped the buyer over |
| Lost deals | `dealix-ops-private/revenue/losses/<deal_id>.md` — reason category + one-paragraph narrative |
| Refusals | `dealix-ops-private/revenue/refusals/YYYY-MM.md` — which filter fired |
| Delivered feedback | `dealix-ops-private/delivery/feedback/<deal_id>.md` — buyer's verdict post-handover |
| Pricing pushback | tagged on proposal record |
| Out-of-scope asks | tagged on intake record |

## Loss categories (closed set)

- Price ceiling
- Timeline mismatch
- Trust signal missing (case studies, references)
- Decision delayed (no rejection, no commitment)
- Scope misfit
- Lost to internal team
- Lost to named competitor
- Other (free text, requires founder review)

## Quarterly review

Cadence: first Sunday of each quarter, 90 minutes.

1. Read all loss narratives from the quarter.
2. Cluster reasons; weight by deal value.
3. Decide: keep, tune, retire, or add a rung.
4. Update the affected offer docs ([OFFER_LADDER.md](./OFFER_LADDER.md), [docs/offers/revenue_sprint/](../offers/revenue_sprint/)) by pull request.
5. Update [docs/trust/SAFE_LANGUAGE_LIBRARY.md](../trust/SAFE_LANGUAGE_LIBRARY.md) if buyer language has shifted.

## Decisions Dealix will not make

- Discounting below the documented band by policy. Discounts happen by exception only, A2.
- Adding banned tactics to win a deal.
- Promising outcomes that violate [NO_OVERCLAIM_POLICY.md](../trust/NO_OVERCLAIM_POLICY.md).

## Evidence

- Quarterly review file: `dealix-ops-private/revenue/quarterly/YYYY-QN.md` with decisions + diffs.
- Pull requests to offer docs reference the review file.

## Cross-links

- [REVENUE_METRICS.md](./REVENUE_METRICS.md) — win rate trend.
- [PIPELINE_STAGES.md](./PIPELINE_STAGES.md) — stage-to-stage conversion drives where to focus.
- [OFFER_LADDER.md](./OFFER_LADDER.md)
- [BAD_REVENUE_FILTER.md](./BAD_REVENUE_FILTER.md) — track if filter is too tight or too loose.

## Owner & cadence

- Founder. Quarterly.

## AR — ملخّص

نظام تطوير العروض حلقة: مكاسب، خسائر، رفض، ملاحظات تسليم، ضغط تسعير، طلبات خارج النطاق. مراجعة ربعية تُصنّف وتقرّر: إبقاء، تعديل، تقاعد، أو إضافة درجة جديدة. التغييرات تنعكس في وثائق العرض بطلب دمج. القيمة التقديرية ليست قيمة مُتحقَّقة.
