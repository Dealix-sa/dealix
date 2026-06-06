# Dealix — Platform Source of Truth / مصدر الحقيقة للمنصة

**Status:** canonical · **Owner:** Founder · **Opened:** 2026-06-06
**Rule:** if any other document contradicts this file, this file wins. Update
this file first, then cascade.

> Companions:
> [`MODULE_STATUS_MAP.md`](MODULE_STATUS_MAP.md) ·
> [`LAUNCH_CONTROL_TOWER.md`](LAUNCH_CONTROL_TOWER.md) ·
> [`../03_governance/CLAIMS_REGISTER.md`](../03_governance/CLAIMS_REGISTER.md) ·
> [`../SERVICE_TRUTH_REPORT.md`](../SERVICE_TRUTH_REPORT.md) ·
> [`../00_foundation/`](../00_foundation/) (constitution layer)

---

## 1. What Dealix is / ما هي Dealix

Dealix is a **governed operating layer** for revenue work — not a generic AI
tool, not a chatbot, not "CRM only". It connects the columns of the operating
equation and refuses to ship any of them in isolation.

**Operating equation / معادلة التشغيل:**

```
Data + Workflow + AI + Human Approval + Governance + Proof
```

> Any missing column = a demo or a risk, not a product.
> أي عمود ناقص = demo أو مخاطرة، وليس منتج.

**AR:** Dealix طبقة تشغيل محكومة للإيرادات — تربط البيانات بالـ workflow
بالـ AI بموافقة بشرية بحوكمة بإثبات. القيمة قابلة للقياس، والـ Proof يسبق
الادّعاء.

---

## 2. The strategic wedge / الـ Wedge الاستراتيجي

The first offer that leads the whole system is the **Revenue Intelligence
Sprint** (productized as the **Command Sprint**): close to the money, fast
Proof, low risk to the customer.

- See [`../00_foundation/STRATEGIC_WEDGE.md`](../00_foundation/STRATEGIC_WEDGE.md)
- Productized one-pager: [`../../sales/COMMAND_SPRINT_ONE_PAGER.md`](../../sales/COMMAND_SPRINT_ONE_PAGER.md)
- 7-day delivery: [`../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md)

---

## 3. The offer ladder / سلم العروض

Single source for offers is [`../OFFER_LADDER.md`](../OFFER_LADDER.md). Summary:

| Rung | Offer | Price band | Promise (result, not guarantee) |
|---|---|---|---|
| 0 | Free Diagnostic | Free | "See where revenue leaks before you spend anything" |
| 1 | Command Sprint (Revenue Intelligence Sprint) | entry | "First evidenced opportunities + Proof Pack in days" |
| 2 | Data / Revenue Pack | mid | "A cleaned, scored, owned data asset" |
| 3 | Managed Business OS | monthly | "Ongoing governed revenue ops under approval" |
| 4 | Custom AI / Enterprise | custom | "Private deploy, SSO, advanced PDPL, custom integrations" |

All outcome phrasing is **estimated, not guaranteed** — see the disclaimer in
§5 and the [`../03_governance/CLAIMS_REGISTER.md`](../03_governance/CLAIMS_REGISTER.md).

---

## 4. What Dealix refuses / ما نرفضه

From [`../00_foundation/WHAT_DEALIX_REFUSES.md`](../00_foundation/WHAT_DEALIX_REFUSES.md)
and [`../00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md):

- **No scraping.** Data enters only via `client_upload`, `crm_export`, or
  `manual_entry` with a signed Source Passport.
- **No cold WhatsApp / no LinkedIn automation / no bulk outreach.**
- **No auto-send.** Every external message is a draft for founder approval.
- **No guaranteed sales / no guaranteed revenue.** Estimates carry `~` and a
  disclaimer.
- **No fake proof.** No customer name/logo/metric is published without
  `consent_for_publication=True` on every event **and** recorded founder
  approval.
- **No agent without identity.** Both sides of any workflow have a named owner.

---

## 5. The non-negotiable disclaimer / إخلاء المسؤولية

> **EN:** Estimated outcomes are not guaranteed outcomes.
> **AR:** النتائج التقديرية ليست نتائج مضمونة.

This line must accompany any number that describes a future or projected
result, on every customer-facing surface.

---

## 6. Module truth / حقيقة الوحدات

The honest, audited status of every module lives in
[`MODULE_STATUS_MAP.md`](MODULE_STATUS_MAP.md), grounded in
[`../SERVICE_TRUTH_REPORT.md`](../SERVICE_TRUTH_REPORT.md). Future / planned
modules are **never** shown as LIVE on any customer surface.

---

## 7. Launch posture / وضع الإطلاق

- **Private Launch:** founder-led, manual, first 3 customers delivered by hand.
  Gate = [`LAUNCH_CONTROL_TOWER.md`](LAUNCH_CONTROL_TOWER.md) Private column.
- **Public Launch:** only after 3 paid Command Sprints + 3 Proof Packs + 1
  case-safe story + `npm run build` PASS + readiness score 85+.

Run the gates:

```bash
python scripts/verify_dealix_positioning.py
python scripts/verify_dealix_module_status.py
python scripts/verify_dealix_growth_assets.py
python scripts/verify_dealix_launch_readiness.py
```
