# START HERE — Dealix Sales Kit (Rung 0–1)

**مرحباً سامي.** هذي نقطة الدخول الوحيدة لحزمة المبيعات. اقرأها مرة واحدة،
ثم اتبع الملفات بالترتيب أدناه. كل ما تحتاجه لإغلاق أول سبرنت إثبات إيراد
موجود هنا.

> **دكترين (محدّث 2026-05-18):** Dealix = عمليات إيراد و AI مُحوكَمة. النظام
> يحلّل ويرتّب ويصيغ المسودات؛ المؤسس يراجع ويعتمد كل إجراء خارجي. **لا
> تواصل بارد، لا أتمتة LinkedIn/واتساب، لا إرسال تلقائي، لا وعود بأرقام، لا
> سعر "1 ريال" معروض على أي عميل.** النتائج التقديرية ليست نتائج مضمونة.

---

## الهدف — The goal

**أول سبرنت إثبات إيراد (499 ريال) مدفوع، ثم حزمة إثبات → خروج من التجميد.**

المسار (rung 0 → rung 1):

```
قائمة دافئة → رسالة أولى (سطر واحد) → رد → بوابة تأهيل
  → تشخيص مصغّر مجاني (rung 0, 0 ريال)
  → جلسة مراجعة / demo
  → سبرنت إثبات إيراد 7 أيام (rung 1, 499 ريال)
  → دفعة 50% → تنفيذ → حزمة إثبات → دفعة 50%
```

---

## شغّلها بهذا الترتيب — Run them in this order

| # | المرحلة | الملف | متى |
|---|---------|-------|-----|
| 1 | **استهداف القائمة الدافئة** | [WARM_LIST_WORKFLOW.md](WARM_LIST_WORKFLOW.md) | اقرأه أولاً — يحدّد القواعد والإيقاع |
| 2 | **بناء القائمة** | [dealix_leads_20_real.md](dealix_leads_20_real.md) · [dealix_leads_50_expanded.md](dealix_leads_50_expanded.md) | مرجع بحث — اختر من تربطك بهم علاقة فعلية فقط |
| 3 | **توليد مسودات التواصل** | `scripts/warm_list_outreach.py` (يقرأ `data/warm_list.csv`) | يولّد مسودات ثنائية اللغة مع شارة قرار التأهيل |
| 4 | **التواصل الأول** | [WARM_LIST_WORKFLOW.md](WARM_LIST_WORKFLOW.md) §2 — السطر الواحد | 5 جهات/يوم، 4 أيام، رسالة واحدة لكل جهة |
| 5 | **معالجة الردود** | [WARM_LIST_WORKFLOW.md](WARM_LIST_WORKFLOW.md) §4 · [dealix_objection_handler.md](dealix_objection_handler.md) | عند كل رد |
| 6 | **بوابة التأهيل** | [QUALIFICATION_CHECKLIST.md](QUALIFICATION_CHECKLIST.md) | على كل جهة تتجاوز "أخبرني أكثر" |
| 7 | **عرض التشخيص المجاني** | [FREE_DIAGNOSTIC_OFFER.md](FREE_DIAGNOSTIC_OFFER.md) | للقرارات ACCEPT / DIAGNOSTIC_ONLY |
| 8 | **جلسة المراجعة / Demo** | [dealix_demo_script_30min.md](dealix_demo_script_30min.md) | ≤ 30 دقيقة، يُختَم بـ "موافق على التشخيص" |
| 9 | **عرض السبرنت 499 ريال** | [dealix_pilot_agreement.md](dealix_pilot_agreement.md) | بعد التشخيص، عند توصية ACCEPT |
| 10 | **المتابعة** | [dealix_followup_cadence.md](dealix_followup_cadence.md) · [dealix_email_drip_sequences.md](dealix_email_drip_sequences.md) | بعد كل تفاعل بدون إغلاق |
| 11 | **الإغلاق والتفعيل** | [CUSTOMER_1_GO_LIVE_RUNBOOK.md](CUSTOMER_1_GO_LIVE_RUNBOOK.md) · [dealix_pilot_agreement.md](dealix_pilot_agreement.md) | عند القبول — دفعة 50/50 |

أدوات مساندة: [DAILY_EXECUTION_SCHEDULE_AR.md](DAILY_EXECUTION_SCHEDULE_AR.md) (جدول يومي) ·
[dealix_battlecards.md](dealix_battlecards.md) (مقارنات المنافسين) ·
[dealix_14day_tracker.html](dealix_14day_tracker.html) (متابع pipeline) ·
[OUTREACH_DRAFTS_QUEUED.md](OUTREACH_DRAFTS_QUEUED.md) (المسودات بانتظار اعتمادك).

---

## الإيقاع اليومي — Daily rhythm

- **5 جهات/يوم** من القائمة الدافئة، رسالة واحدة لكل جهة. لا 10 في يوم.
- **رسالة ثانية فقط** عند رد الجهة، أو نافذة متابعة مُتفَّق عليها صراحةً.
- **كل مسودة تمرّ ببوابة التأهيل** قبل إرسالها.
- **التشخيص خلال 24 ساعة** من تعبئة نموذج الطلب.
- **السبرنت = 7 أيام، 499 ريال ثابت، 50/50** — لا خصم، لا "شهر تجربة".

---

## ما لا تفعله هذي الحزمة — What this kit refuses

- لا تواصل بارد. الجهات في القائمة الدافئة لها علاقة سابقة فعلية فقط.
- لا أتمتة إرسال — كل رسالة يكتبها/يعتمدها المؤسس.
- لا scraping، لا تجميع قوائم، لا أتمتة LinkedIn/واتساب.
- لا ضمان مبيعات، لا وعود بأرقام، لا سعر "1 ريال" معروض.
- لا عمل من الطبقات 2–5 — هذي الحزمة لـ rung 0–1 فقط.

عند طلب يخالف ما سبق: استخدم صيغة الرفض النظيف في
[QUALIFICATION_CHECKLIST.md](QUALIFICATION_CHECKLIST.md) §4.

---

## الخطوة الأولى الآن — Your first step

افتح [WARM_LIST_WORKFLOW.md](WARM_LIST_WORKFLOW.md)، ثم عبّئ `data/warm_list.csv`
بـ 20 جهة تربطك بها علاقة فعلية، وشغّل `python scripts/warm_list_outreach.py`.

**كل المخرجات مسودات بانتظار اعتمادك. لا إرسال خارجي تلقائي — أبداً.**

---

*آخر تحديث: 2026-05-18 | Workstream C — Sales-Kit Activation | يغطي rung 0–1*
