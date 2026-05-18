# Dealix — Launch Runbook — دليل الإطلاق

> Reconciled 2026-05-18 to the canonical doctrine. Source of truth:
> [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md) and
> [`../POSITIONING_AND_ICP.md`](../POSITIONING_AND_ICP.md).
> The previous version sold a "1 SAR pilot" and SaaS tiers 999/2,999/7,999
> SAR/mo with auto-reply/auto-booking — that narrative is retired. It violated
> the no-auto-send rule and the no-overclaim register
> (`dealix/registers/no_overclaim.yaml`).

**الدكترينة في سطر:** Dealix رادار عمليات بالذكاء الاصطناعي للشركات السعودية
B2B. ينتج **مسودات** قرارات ورسائل وإثبات نتائج — **لا يرسل أي رسالة دون
موافقة بشرية**. العربية أولاً، بلا ضمانات، بلا ادعاءات مبالغ فيها.

**Doctrine in one line:** Dealix is an approval-first AI Ops radar for Saudi
B2B. It produces **drafts** of decisions, messages, and proof — it **never
auto-sends**. Arabic-first, no guarantees, no overclaims.

---

## نطاق هذا الإطلاق — Launch scope

هذا الإطلاق يستهدف **أول Pilot مدفوع واحد** ضمن مسار الإطلاق التجاري
(Workstream W1)، تحت التجميد التجاري النشط
([`../ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md)).

- باب الدخول: **التشخيص المجاني للعمليات بالذكاء الاصطناعي** (15 دقيقة).
- العرض القابل للبيع: **7-Day Revenue Proof Sprint بـ 499 ريال** (الدرجة 1).
- لا "1 ريال"، لا باقات SaaS بأسعار ثابتة، لا عرض للدرجات 2–5 خارج شروط فتحها.
- شرط الخروج من التجميد: تسليم أول Pilot مدفوع + Proof Pack موافَق عليه من
  العميل (مستوى إثبات L3 أو أعلى).

This launch targets **one first paid pilot** under the active Commercial
Freeze. The only sellable offer is the 499 SAR 7-Day Revenue Proof Sprint;
rungs 2–5 are not pitched outside their stated entry conditions.

---

## سلم الخدمات الست — The 6-rung offer ladder

| الدرجة | الخدمة | السعر | متى تُفتح |
|--------|--------|-------|-----------|
| 0 | AI Ops Diagnostic | مجاني | متاح الآن — باب الدخول |
| 1 | 7-Day Revenue Proof Sprint | **499 SAR** | متاح الآن — Pilot Gate |
| 2 | Data-to-Revenue Pack | 1,500 SAR | بعد Sprint موثّق |
| 3 | Managed Revenue Ops | 2,999–4,999 SAR/شهر | بعد pilot ناجح |
| 4 | Executive Command Center | 7,500–15,000 SAR/شهر | بعد 3 pilots |
| 5 | Agency Partner OS | مخصص + rev-share 15–30% | بعد 3 proof packs |

كل درجة تُفتح فقط بعد إثبات حقيقي من الدرجة السابقة. التفاصيل الكاملة
ومقاييس الإثبات في [`../OFFER_LADDER_AND_PRICING.md`](../OFFER_LADDER_AND_PRICING.md).

> **ملاحظة نمط التسليم:** الدرجتان 0 و1 تُسلَّمان عبر منتج مُتحقَّق منه. الدرجات
> 3–5 اليوم بقيادة المؤسس / شبه-مؤتمتة — لا تُعرض كخدمات مُدارة بالكامل.

---

## نظرة عامة على الأسبوع — Week-at-a-glance

| اليوم | الهدف الأساسي |
|-------|----------------|
| يوم 0 | تجهيز قبل الإطلاق + اختبار مسار الدفع 499 ريال |
| يوم 1 | منشور إطلاق المؤسس + أول دفعة رسائل مخصصة |
| يوم 2–3 | متابعة + حجز أول تشخيصات مجانية |
| يوم 4–5 | تنفيذ التشخيصات + عرض Proof Sprint بـ 499 ريال |
| يوم 6–7 | إقفال أول Pilot مدفوع + بدء التسليم |

---

## يوم 0 — التجهيز قبل الإطلاق — Pre-launch checklist

العمل المسموح به هنا هو **إنهاء تسليم الدرجة 0–1 فقط** كما يسمح التجميد.
لا بناء قدرات للدرجات 2–5، لا dashboards جديدة، لا إعادة تصميم واجهات.

1. **التشخيص المجاني جاهز** — صفحة `/diagnostic.html` تستقبل 6 أسئلة وتُنتج
   تقريراً تشخيصياً من صفحة واحدة + 3 أولويات. مراجعة يدوية 30 دقيقة قبل
   الإرسال للعميل.
2. **مسار الدفع 499 ريال** — تأكد أن فاتورة الـ 499 ريال للـ Proof Sprint
   تُولَّد وتُدفع، وأن تأكيد الدفع يُسجَّل في سجل التسليم
   ([`../ledgers/DELIVERY_LEDGER.md`](../ledgers/DELIVERY_LEDGER.md)).
   **لا تُنشئ أو تَعرض خطة دفع بـ 1 ريال** — هذا السعر مُلغى.
3. **قائمة الدخول الدافئة** — جهّز قائمة الشركات والوكالات في
   [`../ops/pipeline_tracker.csv`](../ops/pipeline_tracker.csv). فقط شرائح
   متوافقة: مؤسسون + حسابات أعمال + شركاء محتملون. لا استخراج بيانات
   (no scraping)، لا قوائم B2C جماهيرية.
4. **محتوى الإطلاق** — كل المنشورات والرسائل جاهزة في
   [`../ops/launch_content_queue.md`](../ops/launch_content_queue.md)
   بصيغتها النهائية بالعربية. راجعها قبل النشر.
5. **سجلات جاهزة** — تأكد أن سجل الطلبات والتسليم والإثبات في
   [`../ledgers/`](../ledgers/) جاهزة للتدوين.

---

## يوم 1 — الإطلاق — Launch day

1. **منشور الإطلاق** — انشر POST 1 من
   [`../ops/launch_content_queue.md`](../ops/launch_content_queue.md) على
   LinkedIn/X بين 9–11 ص بتوقيت السعودية.
2. **الدفعة الأولى من الرسائل** — أرسل LINKEDIN DM #1 (الدخول الدافئ عبر
   معرفة المؤسس) — **بحد أقصى 5 رسائل مخصصة في الساعة**. كل رسالة تُكتب
   وتُرسَل يدوياً من المؤسس.
3. **سجّل كل رسالة** في [`../ops/pipeline_tracker.csv`](../ops/pipeline_tracker.csv).
4. **سرعة الرد** — عند وصول رد، تابِع خلال 30 دقيقة. سرعة الرد للمؤسس أهم من
   سرعة الإرسال.

> **قاعدة الأتمتة:** Dealix لا يرسل أي رسالة خارجية — لا واتساب، لا LinkedIn،
> لا بريد. كل تواصل يدوي بقيادة المؤسس. لا أتمتة تواصل بارد.

---

## يوم 2–3 — المتابعة + حجز التشخيصات

1. اتبع إيقاع المتابعة (Day +2 / +5 / +10) من
   [`../ops/launch_content_queue.md`](../ops/launch_content_queue.md).
2. الهدف: حجز أول **تشخيصات مجانية** (15 دقيقة) على pipeline فعلي للعميل.
3. احترم طلبات إيقاف التواصل فوراً — حالة `opted_out`، ولا تواصل مجدداً.
4. انشر POST 3 (زاوية المشكلة) لتغذية الوعي.

---

## يوم 4–5 — تنفيذ التشخيص + عرض Proof Sprint

1. **نفّذ التشخيص المجاني** — سلّم تقرير صفحة واحدة + 3 أولويات + توصية
   الخطوة التالية. مقياس النجاح: هل أوصل العميل إلى عرض الـ 499 ريال؟
2. **اعرض 7-Day Revenue Proof Sprint** — السعر 499 ريال، دفعة واحدة مسبقة،
   المدة 7 أيام تقويمية. المخرجات: تقرير تشخيصي مفصل، 5 مسودات رسائل جاهزة
   للموافقة، Proof Pack يوم 7، تقرير تنفيذي، خطة 30 يوم.
3. **اللغة المسموحة:** "فرص مُثبتة بأدلة" — **لا** "نضمن مبيعات" ولا أي وعد
   بأرقام مبيعات أو نسب تحويل. القيمة المذكورة دائماً تقديرية.
4. انشر POST 5 (عرض Proof Sprint) إن لزم.

---

## يوم 6–7 — إقفال أول Pilot + بدء التسليم

1. **الإقفال** — العميل يدفع 499 ريال مسبقاً. سجّل الطلب في
   [`../ledgers/REQUEST_LEDGER.md`](../ledgers/REQUEST_LEDGER.md) والتسليم في
   [`../ledgers/DELIVERY_LEDGER.md`](../ledgers/DELIVERY_LEDGER.md).
2. **بدء التسليم** — اطلب وصولاً للـ pipeline الحالي + قائمة العملاء
   المحتملين + حالة 3 صفقات حالية.
3. **حدود الـ Sprint** — لا إرسال مباشر (draft_only)، لا ضمان صفقات، لا وصول
   للأنظمة الداخلية للعميل.
4. انشر POST 7 (ملخّص الأسبوع) بأرقام فعلية من لوحة النتائج.

---

## ما بعد الإطلاق — After the launch

- **شرط الخروج من التجميد:** تسليم Pilot واحد مدفوع + Proof Pack موافَق عليه
  من العميل (L3+). عند تحققه، تحكم خطة الـ 90 يوم
  ([`../90_DAY_BUSINESS_EXECUTION_PLAN.md`](../90_DAY_BUSINESS_EXECUTION_PLAN.md))
  ما الذي يُفتح بعدها.
- **الترقية** — بعد Sprint موثّق فقط: → Data-to-Revenue Pack (1,500 ريال) أو
  Managed Revenue Ops (2,999–4,999 ريال/شهر). لا ترقية قبل نتيجة موثقة.
- **شراكة الوكالات** — تُفتح بعد 3 Proof Packs موثقة + اتفاقية موقّعة، بنموذج
  rev-share 15–30%. لا أرقام عمولة محددة قبل اتفاقية موقّعة.

---

## قواعد لا يُتنازل عنها — Non-negotiables

1. **لا إرسال تلقائي.** Dealix ينتج مسودات فقط؛ المؤسس/العميل يوافق ويرسل.
2. **لا "1 ريال" ولا باقات SaaS ثابتة.** باب الدخول تشخيص مجاني ثم 499 ريال.
3. **لا ضمانات.** "فرص مُثبتة بأدلة" بدل "نضمن مبيعات".
4. **لا استخراج بيانات، لا تواصل بارد عبر واتساب، لا أتمتة LinkedIn.**
5. **لا بيانات شخصية (PII)** في أي محتوى عام أو case study.
6. **العربية أولاً** في كل مخرج موجّه لقارئ سعودي.

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
