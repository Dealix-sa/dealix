# Website Funnel Map — Dealix Self-Growth OS

خريطة الصفحات والقمع الذاتي. كل صفحة لها **CTA واحد** يقود إلى:
Business OS Score، أو Diagnostic، أو Command Sprint. **لا صفحة بدون CTA.**

---

## القمع (Self-Selling Funnel)

```
Visitor
 → Free Score / Diagnostic
 → Personalized Result
 → Sample Command Pack
 → Book Diagnostic
 → Command Sprint Checkout
 → Intake Form
 → Delivery Workspace
 → Proof Pack
 → Managed OS Upsell
```

---

## الصفحات المطلوبة

| الصفحة | الدور | CTA |
|---|---|---|
| `/ar` | الواجهة | ابدأ تشخيص Dealix |
| `/ar/platform` | شرح المنصة | احصل على Business OS Score |
| `/ar/command-sprint` | العرض الدخولي | ابدأ Command Sprint |
| `/ar/business-os-score` | أداة مجانية | احصل على Business OS Score |
| `/ar/revenue-leakage-calculator` | أداة مجانية | احصل على Revenue Leakage Score |
| `/ar/proof-gap-audit` | أداة مجانية | احصل على Proof Register |
| `/ar/industries/consulting` | قطاع | ابدأ تشخيص Dealix |
| `/ar/industries/training` | قطاع | ابدأ تشخيص Dealix |
| `/ar/industries/marketing-agencies` | قطاع | ابدأ تشخيص Dealix |
| `/ar/industries/it-services` | قطاع | ابدأ تشخيص Dealix |
| `/ar/pricing` | التسعير | ابدأ Command Sprint |
| `/ar/security` | الثقة | ابدأ تشخيص Dealix |
| `/ar/proof` | Proof ledger عام | ابدأ تشخيص Dealix |
| `/ar/start` | نقطة بدء موحّدة | ابدأ تشخيص Dealix |

> صفحات القطاعات تُولَّد بنيتها عبر
> `python3 scripts/growth/generate_sector_pages.py`
> → [`reports/growth/sector_pages/`](../../reports/growth/sector_pages/).

---

## بنية كل صفحة (إلزامية)

1. Pain headline · 2. Specific outcome · 3. How Dealix works ·
4. Sample output · 5. Trust/gates · 6. Offer · 7. **CTA واحد** ·
8. FAQ objection handling.

---

## Trust Assets (تبيع بصمت)

Security Overview · Privacy Overview · Human Approval Policy · No-Spam
Policy · Claims Register · Data Retention · Sample DPA · Proof Policy ·
AI Usage Policy.

> كثير منها موجود بالفعل: [`docs/SECURITY_GUIDE.md`](../SECURITY_GUIDE.md)،
> [`docs/PRIVACY_POLICY_v2.md`](../PRIVACY_POLICY_v2.md)،
> [`docs/DATA_RETENTION_POLICY.md`](../DATA_RETENTION_POLICY.md)،
> [`docs/DPA_PILOT_TEMPLATE.md`](../DPA_PILOT_TEMPLATE.md). اربط لها، لا تكرّرها.

نفس مبدأ least-privilege المعمول به في workflows (تقليل صلاحيات
GITHUB_TOKEN، عدم تخزين أسرار كنص صريح) ينعكس على أي automation للنمو:
محوكم وبأقل صلاحية.

---

## Self-Serve Checkout

```
Choose Command Sprint → Pay → Fill Intake → Select delivery start date
→ Receive workspace link → Founder review → Delivery starts
```

> الدفع عبر مزوّد سعودي حسب الإعداد (Moyasar/Tap/HyperPay). الفاتورة وحالة
> الدفع وملف العميل مربوطة. انظر [`docs/BILLING_MOYASAR_RUNBOOK.md`](../BILLING_MOYASAR_RUNBOOK.md)
> و[`docs/MOYASAR_E2E_GUIDE.md`](../MOYASAR_E2E_GUIDE.md).

---

## القاعدة العليا

كل صفحة تحوّل إلى **lead مؤهل** أو **Sprint مدفوع**. لا تشتيت، CTA واحد.
