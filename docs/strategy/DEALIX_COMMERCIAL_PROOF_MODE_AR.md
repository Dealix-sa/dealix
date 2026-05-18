# Dealix — Commercial Proof Mode — وضع الإثبات التجاري

> Version 1 — 2026-05-18 — Canonical strategy doc for the current company
> phase. Aligns the founder strategy memo with the repo. Pricing-of-record
> stays the 7-offer registry in
> [`../COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) §1
> (`auto_client_acquisition/service_catalog/registry.py`).

This document is the **single source of truth** for what Dealix does now,
what it does not do, and how the offer ladder, SOAEN, and the non-negotiables
fit together. Every founder-led handoff should start here.

هذه الوثيقة هي **المصدر الوحيد للحقيقة** لمرحلة الشركة الحالية.

---

## 1. The phase declaration — إعلان المرحلة

Dealix is **not in build mode** anymore. Dealix is in **Commercial Proof Mode**:

Dealix الآن ليست في مرحلة بناء features. Dealix في مرحلة **إثبات تجاري**:

```
بيع Pilot / Diagnostic صغير
  → تسليم أول Proof Pack
  → تحويله إلى Sprint / Retainer / Partner
  → تكرار نفس الـworkflow
  → بعدها فقط نبني modules أو features
```

The rule for the phase — القاعدة الحاكمة:

> عميل واضح · ألم واضح · عرض صغير · ديمو 12 دقيقة · دفع أو commitment ·
> Proof Pack · ثم Sprint / Retainer / Partner Loop.

---

## 2. Positioning — التموضع

Dealix is **not** sold as an "AI platform", a chatbot, an AI agency, or an
automation reseller. It is sold as:

> **Dealix = Post-Lead Revenue & Governed AI Operations OS**
>
> Dealix يثبت ماذا يحدث بعد وصول الـlead، ويحوّل المتابعة والـAI من فوضى
> إلى workflow محكوم: مصدر، مالك، موافقة، دليل، وخطوة تالية.

The market one-liner — الجملة السوقية:

> الإعلانات تجلب الاهتمام. لكن الإيراد يُخسر بعد وصول الـlead: من رد؟ من تابع؟
> ما الرسالة التالية؟ من يوافق؟ أين الدليل؟

---

## 3. The SOAEN Standard — معيار SOAEN

Every lead, AI action, and external draft passes the SOAEN check:
**S**ource · **O**wner · **A**pproval · **E**vidence · **N**ext Action
(مصدر · مالك · موافقة · دليل · خطوة تالية).

Full definition: [`../00_constitution/SOAEN_STANDARD.md`](../00_constitution/SOAEN_STANDARD.md).
SOAEN is already enforced in `dealix/commercial_ops/doctrine.py`.

---

## 4. The offer ladder — سُلَّم العروض

One offer per maturity stage. Each rung unlocks **only** after real evidence
from the rung below. The **catalog-of-record** is the 7-offer registry in
[`../COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) §1 — registry
prices are authoritative; this table is the maturity narrative on top of it.

| Rung | Offer (AR / EN) | `service_id` | Price (SAR) | Price status | Unlock trigger |
|---|---|---|---|---|---|
| 0 | التشخيص المجاني / Free Mini Diagnostic | `free_mini_diagnostic` | 0 | fixed (free) | 3 diagnostics delivered |
| 1 | سبرنت إثبات الإيرادات 7 أيام / 7-Day Revenue Proof Sprint | `revenue_proof_sprint_499` | **499** — locked | fixed; no change without ≥3 paid pilots | 1 paid pilot + customer-confirmed Proof Pack |
| 2 | حزمة من البيانات إلى الإيراد / Data-to-Revenue Pack | `data_to_revenue_pack_1500` | 1,500 | fixed | 3 paid pilots in same sector |
| 3 | عمليات النمو الشهرية / Growth Ops Monthly | `growth_ops_monthly_2999` | 2,999 /mo | fixed | 3+ consecutive retainer months |
| — | إضافة دعم العمليات / Support OS Add-on | `support_os_addon_1500` | 1,500 /mo | fixed (add-on, attaches to rung 3+) | — |
| 4 | غرفة قيادة الإدارة / Executive Command Center | `executive_command_center_7500` | 7,500 /mo | fixed | proven retainer + executive-confirmed value reports |
| 5 | شريك وكالة وبناء ذكاء مخصص / Agency Partner & Custom AI Build | `agency_partner_os` | custom | governed estimate per engagement | 3 paid pilots delivered + signed permission to publish |

Pricing rule — قاعدة التسعير: لا تخفض السعر أولاً، خفّض النطاق أولاً
(بدل خصم 50% → نراجع 10 leads فقط).

---

## 5. The 11 non-negotiables — الـ11 غير قابلة للتفاوض

Full list and CI test mapping live in
[`../COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) §3:
`no_live_send` · `no_live_charge` · `no_cold_whatsapp` · `no_scraping` ·
`no_fake_proof` · `no_unconsented_data` · `no_unverified_outcomes` ·
`no_hidden_pricing` · `no_silent_failures` · `no_unbounded_agents` ·
`no_unaudited_changes`.

> Dealix لا يؤتمت الفوضى. Dealix يحكم الـworkflow قبل الأتمتة.

---

## 6. The first wedge — الشريحة الأولى

Primary wedge: **agencies + marketing service providers** — they buy, refer,
re-sell, and bundle Dealix. Entry offer: **10-Lead Follow-up Audit / Agency
Proof Pilot** (Rung 1).

رسالة الوكالات: أنتم تجيبون الاهتمام، Dealix يثبت ماذا حدث بعد الاهتمام.
الـCTA: خلونا نجرب على عميل واحد فقط.

---

## 7. The daily motion — التشغيل اليومي

Minimum daily commercial output (under 10 touches = day under-executed):

- 10 human-approved touches (5 warm · 3 targeted emails · 1 LinkedIn manual · 1 partner conversation)
- 5 follow-ups · 1 LinkedIn post · 1 X post · 1 scorecard update

Forbidden — ممنوع: scraping · mass DMs · cold WhatsApp · LinkedIn automation ·
live Gmail send · live charge · fake proof · guaranteed-ROI claims.

Tracked in the **Commercial Control Tower** —
[`../ops/daily_scorecard.md`](../ops/daily_scorecard.md).

---

## 8. The 7 / 30 / 90-day plan — خطة 7 / 30 / 90 يوم

**7 days:** 50 touches · 25 follow-ups · 5 partner conversations ·
2-3 demos · 1 paid pilot or written commitment · 1 Proof Pack · 1 anonymized insight.

**30 days:** 100-200 targeted touches · 10-20 partner conversations ·
5-8 demos · 2-3 scopes · 1-3 paid pilots · 1-2 Proof Packs · 1 clear ICP ·
1 winning message · 1 partner loop.

**90 days:** 5-8 paid pilots · 2 diagnostics · 1 sprint · 1 retainer
candidate · 10 active partners · Proof Pack library · objection library ·
mini benchmark report · repeatable sales script.

---

## 9. Reconciliation Log — سجل المواءمة

Conflicts found between the founder memo and the repo, and how they resolved:

| Conflict | Resolution |
|---|---|
| Memo proposed a new "SOAEN Standard" framework | SOAEN already exists in `dealix/commercial_ops/doctrine.py`; canonicalized into `SOAEN_STANDARD.md` — documented, not invented. |
| Memo ladder (499 / 990 / 4,999-15,000 / 25,000+ / 4,999-35,000-mo) vs repo registry (0 / 499 / 1,500 / 2,999 / 1,500 / 7,500 / custom) | Registry is authoritative (`COMMERCIAL_WIRING_MAP.md` §1: "the code, not the table, is wrong"). Ladder §4 keeps registry prices. |
| Memo "990 Starter / Agency Proof Lite" | Folded into Rung 2 as a scoped low-end variant — not a separate rung. |
| Memo "Diagnostic 4,999-15,000" and "Sprint 25,000+" | Treated as custom engagement value ranges at the Rung 4-5 tier — estimate ranges, not productized catalog prices. No 7th rung; no fixed "Custom Enterprise" tier (doctrine forbids it). |
| Memo "Retainer 4,999-35,000/mo" | A range spanning Rungs 3-5, governed by delivery history. |
| `COMPANY_SERVICE_LADDER.md` had a 5-rung table diverging from the 7-offer registry | Updated to the reconciled 6-rung + add-on table above. |
| Two Proof Pack templates (`proof_pack.md`, `proof_pack_2.md`) | `proof_pack_2.md` extended to the 11-section Commercial Proof Mode standard with 6 Truth Labels. |
| Affiliate workflow referenced in memo | Already exists at `../empire/AFFILIATE_NETWORK.md`; extended rather than duplicated. |

---

## 10. Linked docs — وثائق مرتبطة

| Topic | Doc |
|---|---|
| SOAEN framework | [`../00_constitution/SOAEN_STANDARD.md`](../00_constitution/SOAEN_STANDARD.md) |
| 11 non-negotiables + wiring | [`../COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) |
| Offer ladder (rung detail) | [`../COMPANY_SERVICE_LADDER.md`](../COMPANY_SERVICE_LADDER.md) |
| Proof Pack standard | [`../templates/proof_pack_2.md`](../templates/proof_pack_2.md) |
| Commercial Control Tower | [`../ops/daily_scorecard.md`](../ops/daily_scorecard.md) |
| Governed affiliate network | [`../empire/AFFILIATE_NETWORK.md`](../empire/AFFILIATE_NETWORK.md) |
| Constitution layer | [`../00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md) |

---

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
