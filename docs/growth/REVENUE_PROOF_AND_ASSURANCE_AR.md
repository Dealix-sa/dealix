# Revenue Proof & Assurance — إثبات وضمان الإيراد

> Sections 38–39. ما هو الإيراد الحقيقي مقابل vanity، RevenueRecord schema، طبقة Revenue Assurance، Revenue Quality Score، وأنماط الرفض.
> Module path: `dealix/growth_os/revenue_assurance/`

---

## مقدّمة — Introduction

في Dealix، "الإيراد" ليس رقماً على شريحة. هو سجلّ موقَّع، له مصدر، له تكلفة تسليم معروفة، وله جودة قابلة للقياس. هذه الوثيقة تعرّف الحدّ الفاصل بين الإيراد الحقيقي والإيراد الزائف.

At Dealix, revenue is not a slide number — it is a signed record, sourced, with known delivery cost, and a measurable quality score.

---

## الإيراد الحقيقي مقابل Vanity — Section 38

### إيراد حقيقي (Real Revenue)

- نقد فعلي مُحَوَّل أو فاتورة مُؤكَّدة بسجلّ بنكي.
- له `OfferCard` مرجعي و `AttributionRecord`.
- تكلفة التسليم معروفة (delivery_cost_band).
- صفقة موقَّعة من الطرفين.
- يمرّ بطبقة Revenue Assurance.

### Vanity (لا يُحتسب)

- LOI أو "Letter of Intent" بلا توقيع نهائي.
- "Verbal commitment" بلا فاتورة.
- صفقة بعمولة مرتدّة (clawback) مرتفعة الاحتمال.
- إيراد بتكلفة تسليم تتجاوز السعر (loss-making).
- "Pipeline value" قبل proposal موقَّع.
- إيراد من مصدر يخالف Constitution (راجع `docs/00_constitution/GOOD_REVENUE_BAD_REVENUE.md`).

---

## RevenueRecord JSON Example

```json
{
  "revenue_id": "REV-2026-0231",
  "deal_id": "DEAL-2026-0089",
  "client_label": "Agency X",
  "amount_sar": 30000,
  "currency": "SAR",
  "revenue_type": "one_off",
  "offer_id": "OFF-GOV-SNAP-001",
  "signed_at": "2026-05-12T14:22:00+03:00",
  "invoiced_at": "2026-05-13T10:00:00+03:00",
  "paid_at": null,
  "payment_status": "invoiced_unpaid",
  "delivery_cost_estimate_sar": 6500,
  "gross_margin_estimate_pct": 78,
  "attribution_record_id": "ATR-2026-0231",
  "source_signal_id": "SIG-2026-0117",
  "channel": "abm_direct",
  "asset_ids": ["CON-GEO-0004"],
  "agent_ids": ["message_drafter_agent", "proposal_drafter_agent"],
  "partner_id": null,
  "quality_score": 72,
  "quality_factors": {
    "recurrence": "one_off",
    "expansion_potential": "medium",
    "margin": "high",
    "strategic_fit": "high",
    "collection_confidence": "medium"
  },
  "assurance_checks": {
    "claim_safety_pass": true,
    "pdpl_pass": true,
    "delivery_capacity_pass": true,
    "constitution_pass": true
  },
  "disclosures": [
    "Estimated margin until reconciliation.",
    "Quality score is a Dealix internal metric, not GAAP."
  ]
}
```

---

## Revenue Assurance Layer — Section 39

طبقة تعترض كل صفقة قبل تسجيلها كإيراد. تتكون من 5 بوّابات:

| Gate | Check | Pass Criteria | Fail Action |
|---|---|---|---|
| G1 — Offer Match | هل OfferCard معتمد ومسعَّر؟ | offer_status == "validated" | إرجاع للمؤسس |
| G2 — Claim Safety | كل ادعاء في المقترح مدعوم؟ | claim_ledger.all_sourced | حجب التوقيع |
| G3 — PDPL & Privacy | هل البيانات الشخصيّة مُصنَّفة؟ | pdpl_classification_complete | تأجيل التسليم |
| G4 — Delivery Capacity | هل لدينا قدرة تسليم خلال SLA؟ | capacity_estimate_pass | تأجيل التوقيع أو reprice |
| G5 — Constitution Fit | لا تعارض مع `WHAT_DEALIX_REFUSES.md` | no_refusal_match | رفض الصفقة |

كل بوّابة تنتج `AssuranceCheckRecord` يدخل في `RevenueRecord.assurance_checks`.

---

## Revenue Quality Score — RQS

صيغة داخليّة (0–100) تقيس جودة كل ريال، ليست GAAP، لا تُسوَّق خارجيّاً كأرقام مالية.

### الصيغة

```
RQS = 0.30 × Recurrence
    + 0.20 × ExpansionPotential
    + 0.20 × Margin
    + 0.15 × StrategicFit
    + 0.15 × CollectionConfidence
```

كل عامل يُسجَّل 0–100.

| Factor | 100 | 50 | 0 |
|---|---|---|---|
| Recurrence | retainer ≥ 12 شهر | retainer 3–6 شهر | one-off |
| ExpansionPotential | مسار توسعة موثَّق | محتمل | غير واضح |
| Margin | ≥ 70% | 40–69% | < 40% |
| StrategicFit | ICP أساسي + offer أساسي | ICP أساسي فقط | خارج الـ ICP |
| CollectionConfidence | مدفوع مقدّماً | net-30 | net-90+ |

### مثال مقارن — Worked Example

**A) 10,000 ر.س one-off Sprint**
- Recurrence: 0 (one-off).
- ExpansionPotential: 50 (محتمل).
- Margin: 80 → 100.
- StrategicFit: 100 (ICP أساسي).
- CollectionConfidence: 100 (مدفوع مقدّماً).
- **RQS = 0.30×0 + 0.20×50 + 0.20×100 + 0.15×100 + 0.15×100 = 0 + 10 + 20 + 15 + 15 = 60**

**B) 10,000 ر.س/شهر Retainer (12 شهر)**
- Recurrence: 100.
- ExpansionPotential: 100.
- Margin: 70 → 100.
- StrategicFit: 100.
- CollectionConfidence: 75 (net-30).
- **RQS = 0.30×100 + 0.20×100 + 0.20×100 + 0.15×100 + 0.15×75 = 30 + 20 + 20 + 15 + 11.25 = 96.25**

> الخلاصة: نفس القيمة الإسميّة للشهر الأول، لكن جودة الإيراد B تساوي تقريباً 1.6× جودة A.

---

## Anti-patterns & Refusal Triggers

| Anti-pattern | علامة | رد Dealix |
|---|---|---|
| "احسب pipeline كإيراد" | عرض LOI كأرقام مغلقة | رفض في G1 |
| "خصم 50% لإغلاق الشهر" | margin يهبط تحت 40% | reprice أو رفض |
| "نضمن نتيجة بالأرقام" | ادعاء بلا مصدر | رفض في G2 |
| "نسلّم بدون proof pack" | حذف موثَّق الادعاءات | رفض في Constitution |
| "نقبل عميل خارج ICP" | fit_score < 50 | تحذير + توثيق المخاطر |
| "ندفع عمولة لشريك بدون عقد" | بلا PartnerAgreement | رفض في G5 |

---

## How to verify

```bash
bash scripts/growth_os_master_verify.sh
```

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
