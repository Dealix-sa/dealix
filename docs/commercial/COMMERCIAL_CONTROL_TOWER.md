# Dealix — برج التحكم التجاري — Commercial Control Tower
<!-- PHASE 3 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> نقطة الحقيقة التجارية: KPIs · نجاح العميل · Benchmark · Productization.
> يكمّل [`DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md`](DEALIX_COMMERCIAL_SCALE_SYSTEM_AR.md).

---

## 1. النظام اليومي — Daily System

scorecard يومي + مراجعة أسبوعية. تفاصيل التنفيذ اليومي في
[`DAILY_SCORECARD.md`](DAILY_SCORECARD.md).

---

## 2. أهم KPIs

**الاكتساب — Acquisition**
- touches/day · reply rate · positive reply rate · demo booked rate ·
  partner conversations

**المبيعات — Sales**
- demo → scope · scope → invoice · invoice → paid · paid → proof delivered

**التسليم — Delivery**
- time-to-first-proof · proof QA score · client value confirmation

**التوسّع — Expansion**
- proof → sprint proposal · sprint proposal → won · proof → referral ·
  proof → retainer candidate

**الأمان — Safety**
- blocked risky actions · approval compliance · unsupported claims caught ·
  fake proof = 0 · cold WhatsApp = 0

---

## 3. دورة نجاح العميل — Customer Success Loop

بعد تسليم Proof Pack، لا تقل "خلصنا":

| اليوم | الإجراء |
|-------|---------|
| Day 0 | Delivery call |
| Day 2 | Value confirmation |
| Day 5 | Sprint recommendation |
| Day 10 | Referral ask |
| Day 21 | Retainer proposal |
| Day 30 | Executive value memo |

كل Proof Pack ينتج مخرجاً واحداً على الأقل — انظر
[`PROOF_PACK_STANDARD.md`](PROOF_PACK_STANDARD.md) §4.

---

## 4. Benchmark Engine

بعد 10–20 مشروعاً، اجمع (بشكل مجهول الهوية / k-anonymous):

- Common follow-up gaps
- Common CRM missing fields
- Common approval risks
- Average time-to-proof
- Common objection patterns
- Sprint-to-retainer rate
- Data quality score

ثم انشر تقريراً مرجعياً: **"State of Post-Lead Revenue Ops in Saudi SMEs"**
أو **"Saudi Governed AI Ops Benchmark"**. هنا تتحول Dealix من "شركة تبيع
خدمة" إلى **مرجع سوقي**.

---

## 5. مسار التحويل إلى منتج — Productization Path

لا تقفز إلى SaaS:

```
Stage 1: Internal tools
Stage 2: Client-visible reports
Stage 3: Client workspace
Stage 4: Partner portal
Stage 5: Self-serve modules
Stage 6: SaaS
```

**قاعدة البناء — the build rule:**

| التكرار | المخرج |
|---------|--------|
| workflow جديد | checklist |
| تكرّر مرتين | template |
| تكرّر 3 مرات | automation |
| تكرّر مع عميلين | internal module |
| تكرّر مع 3 عملاء + retainers | product feature |

لا تُبنى أتمتة قبل ظهور طلب حقيقي — انظر
[`docs/sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`](../sales-kit/CONDITIONAL_BUILD_TRIGGERS.md).

---

## 6. المراجعة الأسبوعية — Weekly Review

كل أسبوع: scorecard، friction log، الاعتراضات الجديدة، تقدّم النتائج الخمس
(انظر [`CURRENT_DIRECTION.md`](CURRENT_DIRECTION.md) §1)، وقرار التركيز
للأسبوع التالي.

---

*Estimated outcomes are not guaranteed outcomes — النتائج التقديرية ليست
نتائج مضمونة.*
