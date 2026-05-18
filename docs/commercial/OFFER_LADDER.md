# Dealix — السلم التجاري — Offer Ladder
<!-- PHASE 3 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> **مصدر الحقيقة الوحيد للتسعير — single source of truth for pricing:**
> [`docs/OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md)
> والسجل البرمجي في
> [`docs/COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) §1
> (`service_catalog/registry.py`).
>
> هذه الوثيقة **تعكس** السلم الرسمي ولا تنشئ أسعاراً جديدة. أي رقم هنا يجب أن
> يطابق المصدر — عند أي تعارض، **المصدر صحيح وهذه الوثيقة خطأ**.

> **قاعدة ذهبية:** كل درجة تُفتح فقط بعد إثبات حقيقي من الدرجة السابقة. لا
> ترقية قبل نتيجة موثقة. لا ضمانات. لا ادعاءات مبالغ فيها.

---

## 1. السلم الرسمي — The Canonical Ladder

```
[0] Free AI Ops Diagnostic          مجاني            ← باب الدخول
[1] 7-Day Revenue Proof Sprint      499 SAR          ← Pilot Gate
[2] Data-to-Revenue Pack            1,500 SAR        ← Upsell بعد Sprint
[3] Managed Revenue Ops             2,999–4,999 SAR/شهر ← بعد pilot
[4] Executive Command Center        7,500–15,000 SAR/شهر ← بعد 3 pilots
[5] Agency Partner OS               مخصص + rev-share 15–30% ← بعد 3 proof packs
```

| الخدمة | السعر | الوضع | نمط التسليم |
|--------|-------|-------|------------|
| AI Ops Diagnostic | مجاني | متاح الآن | منتج مُتحقَّق منه |
| 7-Day Revenue Proof Sprint | 499 SAR | متاح الآن | منتج مُتحقَّق منه |
| Data-to-Revenue Pack | 1,500 SAR | بعد تأهيل | بقيادة المؤسس |
| Managed Revenue Ops | 2,999–4,999 SAR/شهر | بعد pilot | بقيادة المؤسس / شبه-مؤتمت |
| Executive Command Center | 7,500–15,000 SAR/شهر | بعد 3 pilots | بقيادة المؤسس / شبه-مؤتمت |
| Agency Partner OS | مخصص + rev-share | بعد 3 proof packs | بقيادة المؤسس / شبه-مؤتمت |

**إفصاح نمط التسليم:** الدرجتان 0 و1 تُسلَّمان عبر منتج مُتحقَّق منه. الدرجات
3–5 اليوم **بقيادة المؤسس / شبه-مؤتمتة** — ليست خدمات مُدارة بالكامل، وتُفتح
فقط عند استيفاء شروط الدخول.

---

## 2. العرض الذي تبدأ به — The Entry Offer

ابدأ صغيراً وواضحاً. لا تبدأ بـ"اشترك في المنصة".

**العرض العملي الأول — Agency Proof Pilot / 10-Lead Follow-up Audit**
يُسلَّم **عبر الدرجة 1 (7-Day Revenue Proof Sprint — 499 SAR)**. هذا ليس سعراً
جديداً — هو نفس الـSprint بنطاق ابتدائي واضح:

**المخرجات:**

- 10 leads / opportunities reviewed
- Lead status board
- Follow-up drafts (draft_only — لا إرسال مباشر)
- Approval risks
- Evidence gaps
- Proof Pack يوم 7
- Next action recommendation

---

## 3. قاعدة التفاوض — The Negotiation Rule

> **لا تخفض السعر أولاً. خفّض النطاق أولاً.**
> Don't cut price first — cut scope first.

بدل الخصم:

- نبدأ بـ10 leads فقط.
- نبدأ بعميل واحد فقط.
- نبدأ Proof Pack واحداً فقط.

السلم نفسه ثابت — التسعير محكوم باختبار `no_hidden_pricing`. المرونة في
**النطاق**، لا في الرقم.

---

## 4. مسار الترقية — Upgrade Path

```
Free Diagnostic
   → 499 Sprint (Proof Pack)
      → 1,500 Data-to-Revenue Pack
         → 2,999–4,999/mo Managed Revenue Ops
            → 7,500–15,000/mo Executive Command Center
               → Agency Partner OS (rev-share)
```

كل ترقية مشروطة بإثبات موثق من الدرجة السابقة — انظر
[`PROOF_PACK_STANDARD.md`](PROOF_PACK_STANDARD.md) و
[`COMMERCIAL_CONTROL_TOWER.md`](COMMERCIAL_CONTROL_TOWER.md).

---

*No guaranteed claims · Missing data = insufficient_data · النتائج التقديرية
ليست نتائج مضمونة.*
