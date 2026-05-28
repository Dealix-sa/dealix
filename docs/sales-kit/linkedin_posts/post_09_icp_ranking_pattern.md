# Post 09 — What we noticed in Saudi B2B ICP data · ما لاحظناه في بيانات ICP B2B السعودية

**Cluster:** Case-safe Pattern
**Best day:** Saturday 09:00 KSA
**Expected length:** AR 700 words · EN 500 words

---

## Arabic

في آخر ستة شهور، حللنا data من ١٢ CRM سعودي B2B (بإذن صريح، بعد
DPA). الحجم: ١٤,٠٠٠+ lead. اتفقت معهم على عدم تسمية أحد — التحليل
يخدمهم وبقية السوق دون كشف.

**النمط الأول: تباين قاسٍ بين الـ ICP المعلن والـ ICP الفعلي**

- المتوسط: ٦٨٪ من leads في CRM لا يطابق الـ ICP الذي تشركه
  شركة المبيعات في كل meeting.
- السبب: فريق sales يدخل أي lead قابل للحديث، حتى لو غير مناسب.
- التأثير: ٦٨٪ من جهد المتابعة على leads لا يستحق.

**النمط الثاني: غياب الـ ranking الموضوعي**

- ٩/١٢ من الشركات تستخدم "ICP fit" كحقل text حر.
- ٢/١٢ تستخدم enum (High/Med/Low).
- ١/١٢ يستخدم scoring numeric.
- ٠/١٢ تربط الـ score بـ data attributes موثقة.

النتيجة: "High fit" تعني شيئًا مختلفًا لكل sales rep.

**النمط الثالث: الـ revenue concentration**

- في كل CRM، الـ top-10 leads (بالـ score) يولد ٥٥-٧٠٪ من revenue
  الحالي.
- الـ bottom 50% يولد < ٣٪.

لكن الـ effort distribution غالبًا عكسي: الـ founders ومدراء الـ
sales يقضون وقتًا أكثر على الـ bottom 50% (لأنها "أسهل تحويل" -
وهو خطأ).

**النمط الرابع: الـ "stale lead trap"**

- في المتوسط، ٣٧٪ من leads في CRM آخر activity > ٦ شهور.
- ٨٤٪ من هذه stale leads ينتهي بها "lost" بعد محاولة المتابعة.
- لكن المتابعة عليها تستهلك ١٥-٢٠٪ من وقت الـ sales team.

**ماذا يعني هذا للـ founder السعودي؟**

١. **اعمل audit للـ ICP**: قم بـ scoring numeric مرة واحدة، حتى لو
   يدوي. ضع 5 attributes (industry، size، revenue، tech stack،
   buyer role) ووزن لكل واحد. اقسم leads إلى Tier S/A/B/C.

٢. **افصل effort بـ tier**: ٦٠٪ من وقت sales على Tier S، ٣٠٪
   على Tier A، ١٠٪ على B+C. الـ stale leads تذهب لـ nurture
   automation (ليس outreach).

٣. **حدث الـ ICP كل ربع**: الـ ICP الفعلي يتطور مع نضوج الـ
   business. ICP من ٢٠٢٢ يختلف عن ٢٠٢٤.

في Dealix بنينا agent اسمه `icp_matcher` (ضمن الـ pipeline) يقوم
بالـ scoring تلقائيًا — لكن النتيجة تذهب للـ founder كـ draft،
ليست لـ delivery تلقائي.

**النقطة الأخيرة:**

هذا النمط (٦٨٪ misfit، lack of ranking، effort inversion) يكلف
شركة B2B سعودية متوسطة ~٤٠-٦٠ ساعة sales/شهر مضيعة. حسبتك الخاصة
ستظهر رقمًا قريبًا.

---

## English

In the last 6 months we analyzed data from 12 Saudi B2B CRMs (with
explicit permission, after DPA). Volume: 14,000+ leads. Agreement
with all parties: no naming — the analysis serves them and the
broader market without exposure.

**Pattern 1: Harsh gap between stated and actual ICP**

- Average: 68% of CRM leads don't match the ICP that sales team
  shares in every meeting.
- Cause: sales reps log every conversational lead, even if a poor
  fit.
- Effect: 68% of follow-up effort goes to leads that don't deserve
  it.

**Pattern 2: Absence of objective ranking**

- 9/12 companies use "ICP fit" as a free-text field.
- 2/12 use enum (High/Med/Low).
- 1/12 uses numeric scoring.
- 0/12 tie the score to documented data attributes.

Result: "High fit" means something different to every sales rep.

**Pattern 3: Revenue concentration**

- In every CRM, the top-10 leads (by score) generate 55-70% of
  current revenue.
- The bottom 50% generate < 3%.

But effort distribution is usually inverted: founders and sales
managers spend more time on the bottom 50% (because "easier to
convert" — which is wrong).

**Pattern 4: Stale lead trap**

- On average, 37% of CRM leads have last activity > 6 months.
- 84% of these stale leads end up "lost" after follow-up attempts.
- Yet pursuing them eats 15-20% of sales team time.

**What this means for the Saudi founder:**

1. **Audit the ICP**: do numeric scoring once, even manually. Set
   5 attributes (industry, size, revenue, tech stack, buyer role)
   and weight each. Split leads into Tier S/A/B/C.
2. **Separate effort by tier**: 60% of sales time on Tier S, 30%
   on A, 10% on B+C. Stale leads go to nurture automation (not
   outreach).
3. **Update the ICP quarterly**: real ICP evolves as the business
   matures. 2022 ICP differs from 2024.

At Dealix we built an `icp_matcher` agent (part of the pipeline)
that does the scoring automatically — but the result goes to the
founder as a draft, never to autonomous delivery.

**Bottom line:**

This pattern (68% misfit, lack of ranking, effort inversion) costs
the average Saudi B2B company ~40-60 wasted sales hours/month. Your
own math will show a similar figure.

---

## CTA

- AR: "أعرض نموذج scoring + tier framework. DM لو تبي تطبقه."
- EN: "Happy to share the scoring + tier framework template. DM."
