---
title: Bad Revenue Filter
owner: Founder
status: active
last_review: 2026-05-23
---

# Bad Revenue Filter — مُرشِّح الإيراد السيّئ

## Purpose

A short, brutal checklist. If any item triggers, Dealix does not take the money. Bad revenue costs more than it earns.

## Refuse if

1. **Out of scope.** Request needs cold WhatsApp blasting, scraping closed platforms, automated LinkedIn outreach, or any tactic listed in [docs/00_constitution/WHAT_DEALIX_REFUSES.md](../00_constitution/WHAT_DEALIX_REFUSES.md).
2. **No decision-maker.** Contact cannot say yes to a 499 SAR purchase.
3. **Unrealistic timeline.** Buyer demands delivery faster than the documented SLA without paying for an expedite.
4. **Ethical conflict.** Buyer's request involves deceiving a third party, scraping PII, or manipulating regulators.
5. **Compliance conflict.** Buyer asks Dealix to claim certifications, accreditations, or partnerships it does not hold.
6. **Revenue-claim demand.** Buyer requires Dealix to commit to a specific sales number as a contractual outcome.
7. **Non-aligned sector.** Sector falls outside the agreed taxonomy in [docs/02_saudi_positioning/SAUDI_SECTOR_TAXONOMY.md](../02_saudi_positioning/SAUDI_SECTOR_TAXONOMY.md) without explicit founder onboarding decision.
8. **Capacity conflict.** Accepting the deal would breach an existing client's SLA.
9. **Channel violation.** Buyer wants Dealix to send messages on their behalf without explicit, written authorization per channel.
10. **PDPL conflict.** Buyer wants to share or process data in a way that violates PDPL or other applicable Saudi law.

## How to refuse

Use the approved refusal phrasing from [docs/trust/SAFE_LANGUAGE_LIBRARY.md](../trust/SAFE_LANGUAGE_LIBRARY.md):

```
Thank you for the brief. This request falls outside what we deliver because [reason].
We can offer [alternative if any]. If that does not fit, we are not the right partner here.
```

AR equivalent provided in `dealix-ops-private/templates/refusals.md`.

## Operational steps

1. Run the filter at Reply stage (after first conversation).
2. Re-run at Proposal stage before drafting.
3. Trigger = stop. No proposal goes out.
4. Log refusals; track refusal rate as a health metric.

## Evidence

- Refusal note in `dealix-ops-private/revenue/refusals/YYYY-MM.md` with which trigger fired.
- Quarterly review of refusals to detect pattern shifts in inbound demand.

## Cross-links

- [docs/00_constitution/WHAT_DEALIX_REFUSES.md](../00_constitution/WHAT_DEALIX_REFUSES.md)
- [docs/00_constitution/GOOD_REVENUE_BAD_REVENUE.md](../00_constitution/GOOD_REVENUE_BAD_REVENUE.md)
- [REVENUE_CONTROL_SYSTEM.md](./REVENUE_CONTROL_SYSTEM.md) — R-04.
- [docs/trust/NO_OVERCLAIM_POLICY.md](../trust/NO_OVERCLAIM_POLICY.md)

## Owner & cadence

- Founder. Reviewed quarterly with refusal log.

## AR — ملخّص

مُرشِّح الإيراد السيّئ قائمة قصيرة وحاسمة: خارج النطاق، لا متّخذ قرار، توقيت غير واقعي، تعارض أخلاقي، تعارض امتثال، طلب ضمان مبيعات، قطاع غير مُتوافق، تعارض سعة، انتهاك قناة، تعارض حماية البيانات. أي بند = رفض. الرفض موثّق ومراجع ربعيًا. القيمة التقديرية ليست قيمة مُتحقَّقة.
