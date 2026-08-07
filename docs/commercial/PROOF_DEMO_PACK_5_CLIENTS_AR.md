# حزمة إثبات السوق — 5 عملاء تجريبيين (PROOF_DEMO_PACK_5_CLIENTS_AR)

> الوثيقة المرجعية لعرض الإثبات على عملاء سعوديين تجريبيين قبل التوسع التجاري.
> الحزمة client-facing، تُشارك في الاجتماع الأول أو demo فقط — لا تُرسل بدون موافقة.

## الغرض

إثبات أن نظام Dealix يولّد قيمة ملموسة ومُقاسة خلال 21 يومًا على 5 عملاء تجريبيين
(Founder-led + Revenue Intelligence + Proof Pack + Data Quality). الناتج: حزمة إثبات
قابلة للعرض لعميل مرشح ثاني، مع رقم محدد ومؤشرات L0–L5 — لا وعود تسويقية.

## مكوّنات الحزمة

| المكوّن | المحتوى | المسؤول |
|---|---|---|
| Founder Lead Pack | 5 حسابات تجريبية سعودية مع ICP و visible signal | Founder |
| Revenue Intelligence (RI) | تقرير محوَل من raw leads إلى scored leads + تصنيف A/B/C/D | OS Engine |
| Proof Pack | لكل عميل: before/after KPI + screenshot + timeline 21 يوم | Founder |
| Data Quality (DQ) | سجل مصادر البيانات + PDPL合规 status + dedupe log | OS Engine |

## معايير القبول

1. كل عميل من الـ 5 له dossier مكوّن من: ICP fit score، visible signal، weakness
   hypothesis، recommended offer، 21-day proof plan.
2. لا توجد claims من نوع "نزيد المبيعات X%" — فقط مؤشرات قابلة للقياس على البيانات
   الفعلية للعميل.
3. كل claim مرفق بـ evidence ref (path to screenshot/log/JSON export).
4. الحزمة تمر عبر `validate_docs_governance.py` بدون أخطاء.
5. لا تُشارك خارج Dealix بدون توقيع NDA.

## ترتيب الاستخدام

- **الاجتماع الأول مع عميل مرشح:** اعرض الحزمة كدليل على القدرة، ليس كـ pitch.
- **المفاوضات:** استخدم proof pack لكل عميل تجريبي كـ case study anonymized.
- **الدورة التجريبية للعميل الجديد:** ابدأ من نفس الـ template لكن ببيانات العميل.

## التوافق مع سياسات Dealix

- لا تتعارض مع `BAD_FIT_CLIENT_POLICY_AR.md` — كل عميل تجريبي يجب أن يمر ICP fit.
- لا تتعارض مع `APPROVAL_POLICY_AR.md` — الحزجة قبل النشر تمر بمراجعة founder.
- التوافق مع PDPL: بيانات العملاء التجريبيين إما public signals أو موافق عليها
  كتابيًا.

## روابط مرجعية

- [HOLDING_OFFER_MATRIX_AR.md](../strategic/HOLDING_OFFER_MATRIX_AR.md)
- [RETAINER_PILOT_MINI_AR.md](RETAINER_PILOT_MINI_AR.md)
- [DOCS_PUBLICATION_BOUNDARY_AR.md](../strategic/DOCS_PUBLICATION_BOUNDARY_AR.md)