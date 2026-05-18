# دليل بناء القائمة الدافئة · Warm List Sourcing Guide

> هذا الدليل يشرح كيف يبني المؤسس قائمة 50+ اسماً حقيقياً في `data/warm_list.csv`.
> الوكيل بنى السقالة فقط (الرؤوس + الشرائح) — **الأسماء الحقيقية يملؤها المؤسس**.
>
> This guide explains how the founder builds a 50+ real-name list in `data/warm_list.csv`.
> The agent built only the scaffold (headers + segments) — **the founder fills real names**.

---

## لماذا قائمة دافئة فقط · Why warm-only

العقيدة تمنع التواصل البارد والـ scraping وأتمتة LinkedIn/WhatsApp. لذلك كل اسم
في القائمة يجب أن يكون **معرفة حقيقية مسبقة** للمؤسس — لا أسماء مشتراة، لا قوائم
منسوخة، لا استخراج آلي.

Doctrine forbids cold outreach, scraping, and LinkedIn/WhatsApp automation. Every
name must be a **real prior relationship** of the founder — no purchased lists, no
copied lists, no automated extraction.

## مصادر الأسماء · Where to source names

1. **الإحالات / Referrals** — اسأل 5-10 من شبكتك الأقرب: "من تعرف يعاني من فوضى
   في إدارة العملاء المحتملين؟" الإحالة الموثوقة أقوى مدخل.
2. **جهات اتصال LEAP / الفعاليات / LEAP & event contacts** — بطاقات وتعريفات من
   LEAP وملتقيات الأعمال؛ تواصل سبق وتم وجهاً لوجه.
3. **اتصالات LinkedIn من الدرجة الأولى / LinkedIn 1st-degree** — فقط من تعرفهم
   فعلياً. لا أتمتة، لا رسائل جماعية — نسخ يدوي اسم اسم.
4. **زملاء سابقون / Past colleagues** — من عملت معهم سابقاً وانتقلوا لشركات ضمن ICP.
5. **عملاء / شركاء سابقون / Past clients & partners** — علاقة عمل قائمة وثقة موجودة.

## فلتر ICP — من يدخل القائمة · The ICP filter

أدخل الاسم فقط إذا تحقق أغلب هذه الشروط · Add a name only if most of these hold:

- شركة B2B سعودية، حجم تقريبي **10-80 موظف**.
- لديها **ألم واضح** في إدارة العملاء المحتملين / فوضى بيانات / متابعة ضائعة.
- يوجد **صاحب قرار** يمكن الوصول إليه (مالك / GM / COO / رئيس نمو).
- لديها **بيانات أو عملية موجودة** (CRM، أو حتى جداول Excel).
- القطاع ضمن الشرائح المستهدفة المبذورة في الـ CSV:
  `b2b_services` · `saas` · `distribution_wholesale` · `professional_consulting` · `logistics`.
- **يقبل الحوكمة** — لا يطلب scraping أو واتساب بارد أو ضمان مبيعات.

إذا فشل اسم في فلتر ICP، لا تحذفه — ضعه في ورقة منفصلة كـ "إحالة محتملة لاحقاً".

If a name fails the ICP filter, do not delete it — park it as a future referral source.

## كيف تملأ الـ CSV · How to fill the CSV

- الرؤوس ثابتة: `name,role,company,sector,relationship,city,linkedin_url,notes` — لا تغيّرها.
- عمود `sector` و`notes` فيهما تلميحات شرائح مبذورة — استبدل التلميح ببياناتك.
- عمود `relationship`: استخدم `warm` أو `active` أو `cold` (تجنّب `cold` — العقيدة).
- الهدف: **50+ صفاً ممتلئاً** موزعاً عبر الشرائح الخمس (~10-11 لكل شريحة).

بعد الملء، شغّل · After filling, run:

```bash
python scripts/warm_list_outreach.py
```

ينتج `data/outreach/warm_list_drafts.md` — مسودات ثنائية اللغة **لمراجعة المؤسس فقط**،
لا إرسال آلي. راجع شارة التأهيل قبل أي تواصل، وأرسل ~5 يومياً يدوياً بصوتك.

This produces `data/outreach/warm_list_drafts.md` — bilingual drafts **for founder
review only**, no automated send. Check the qualification badge before reaching out,
and send ~5/day manually in your own voice.

---

_Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة._
