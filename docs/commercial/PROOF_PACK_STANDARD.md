# Dealix — معيار Proof Pack — Proof Pack Standard
<!-- PHASE 3 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> الـProof Pack هو **المنتج الحقيقي الأول** لـDealix. كل مشروع ينتج Proof
> Pack. انظر أيضاً [`docs/ROI_PROOF_PACK.md`](../ROI_PROOF_PACK.md) و
> [`operations/PROOF_STACK_ORDER_AR.md`](operations/PROOF_STACK_ORDER_AR.md).

---

## 1. أقسام Proof Pack — The Sections

1. Context — السياق
2. Inputs reviewed — المدخلات المُراجَعة
3. Lead / workflow status — حالة الـlead / الـworkflow
4. Source quality — جودة المصدر
5. Owner gaps — فجوات الملكية
6. Approval risks — مخاطر الموافقة
7. Follow-up gaps — فجوات المتابعة
8. Draft messages — رسائل مسودة (draft_only)
9. Recommended next actions — الخطوات التالية الموصى بها
10. Truth labels — وسوم الحقيقة
11. Upgrade path — مسار الترقية

كل قسم يُقرأ عبر معيار SOAEN — انظر
[`CURRENT_DIRECTION.md`](CURRENT_DIRECTION.md) §3.

---

## 2. وسوم الحقيقة — Truth Labels

كل رقم أو ادعاء في Proof Pack يحمل وسماً صريحاً:

| الوسم | المعنى |
|-------|--------|
| Estimate | تقدير — `is_estimate` |
| Observed | ملاحَظ في البيانات |
| Client-confirmed | مؤكَّد من العميل |
| Payment-confirmed | مؤكَّد بدفعة فعلية |
| Repeated workflow | workflow متكرر |
| Retainer-ready | جاهز لـretainer |

**مثال:**

```
Follow-up gap:   Observed
Potential value: Estimate
Client pain:     Client-confirmed
Revenue:         Payment-confirmed only
```

لا يُعرض رقم تقديري كحقيقة. هذا يحمي اختبار `no_fake_proof` و
`no_unverified_outcomes`.

---

## 3. Authority Engine — كل Proof Pack يصبح محتوى

```
Proof Pack
   → anonymized insight
      → LinkedIn post
      → newsletter
      → partner asset
      → case-style post
      → webinar slide
      → objection answer
```

**مثال آمن:**

> في workflow راجعناه لوكالة محلية، المشكلة لم تكن في الإعلان — بل في غياب
> owner بعد وصول الـlead.

**ممنوع:** اسم عميل بلا إذن · رقم غير موثق · نتيجة مالية غير مثبتة · شعار
بلا موافقة.

---

## 4. مخرج إلزامي — Mandatory Output

كل Proof Pack **يجب** أن ينتج واحداً على الأقل من:

- Sprint proposal
- Retainer candidate
- Referral
- Partner intro
- Anonymous insight
- Benchmark data point

لا Proof Pack ينتهي بـ"خلصنا" — انظر دورة نجاح العميل في
[`COMMERCIAL_CONTROL_TOWER.md`](COMMERCIAL_CONTROL_TOWER.md).

---

*No fake proof · Estimated outcomes are not guaranteed outcomes — النتائج
التقديرية ليست نتائج مضمونة.*
