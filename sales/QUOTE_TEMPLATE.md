# قالب عرض السعر — Dealix Quote Template (AR/EN)

> **DRAFT — مسودة.** مشاركة أي سعر مع العميل تتطلب موافقة المؤسس (بوابة بشرية — `os/01_CLAUDE.md`).
> هذا القالب مرجع بشري. لتوليد عرض مملوء تلقائيًا:
> `python scripts/generate_quote.py --client "<NAME>" --offer <OFFER_KEY> --package <PACKAGE_KEY>`

كل الأسعار **قبل الضريبة (ex-VAT)**؛ تُضاف ضريبة القيمة المضافة 15% حسب أنظمة ZATCA.

---

# عرض سعر — Dealix | Quote — {{CLIENT_NAME}}

**التاريخ / Date:** {{DATE}}  
**صالح حتى / Valid until:** {{DATE + 30 days}}  
**العملة / Currency:** SAR — ex-VAT (+15% VAT)

**العرض / Offer:** {{OFFER_NAME_AR}} — {{OFFER_NAME_EN}}

## 1. رسوم التأسيس / Setup (one-off)

| البند / Item | المبلغ (ex-VAT) | VAT 15% | الإجمالي / Total |
|---|--:|--:|--:|
| Setup | {{SETUP_EX_VAT}} SAR | {{SETUP_VAT}} | {{SETUP_TOTAL}} SAR |

## 2. الاشتراك الشهري / Monthly subscription

| البند / Item | المبلغ (ex-VAT) | VAT 15% | الإجمالي / Total |
|---|--:|--:|--:|
| Monthly | {{MONTHLY_EX_VAT}} SAR | {{MONTHLY_VAT}} | {{MONTHLY_TOTAL}} SAR |
| Annual prepay (12×, −10%) | {{ANNUAL_EX_VAT}} SAR (ex-VAT) | | |

> **الاستخدام / Usage:** يشمل {{INCLUDED_UNITS}} عملية شهريًا. كل {{BLOCK}} عملية إضافية = {{OVERAGE}} ر.س (ex-VAT) — لا خصم على التجاوز.
> الحد الأدنى للعقد: 6 أشهر (الأفضل 12). الدفع شهري مقدم. إلغاء مبكر = شهرين كتعويض.

## 3. جدول الدفع / Payment schedule (50/30/20)

| المرحلة / Milestone | % | المبلغ (ex-VAT) | الإجمالي / Total |
|---|--:|--:|--:|
| عند التوقيع / On signing | 50% | {{M1_EX_VAT}} SAR | {{M1_TOTAL}} SAR |
| بعد تسليم MVP/Pilot / After MVP/Pilot | 30% | {{M2_EX_VAT}} SAR | {{M2_TOTAL}} SAR |
| عند الإطلاق / On launch | 20% | {{M3_EX_VAT}} SAR | {{M3_TOTAL}} SAR |

## 4. الخطوة التالية / Next step

1. راجعوا العرض واطرحوا أي أسئلة / Review and ask questions.
2. عند الموافقة نرسل Service Agreement / On approval we send the agreement.
3. نحدد kickoff فور التوقيع والدفعة الأولى / Kickoff on signing + first payment.

---
*أسعار تقديرية (ex-VAT) صالحة 30 يوم. تُضاف ضريبة القيمة المضافة 15% حسب أنظمة ZATCA.
فاتورة رسمية ZATCA تُصدر بعد توقيع العقد. / Estimates, ex-VAT, valid 30 days.*
