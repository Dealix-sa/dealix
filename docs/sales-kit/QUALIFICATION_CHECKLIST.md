# Qualification Checklist — قائمة التأهيل (8 أسئلة)

> **دكترين (2026-05-18):** كل جهة تمرّ بهذه البوابة قبل أي مسودة عرض. التأهيل
> يُشغَّل عبر `auto_client_acquisition/sales_os/qualification.qualify(...)`؛
> هذا المستند هو الواجهة البشرية لنفس البوابة. لا تواصل بارد، لا أتمتة، لا
> وعود بأرقام. النتائج التقديرية ليست نتائج مضمونة.
>
> Cross-link: [START_HERE.md](START_HERE.md) · [WARM_LIST_WORKFLOW.md](WARM_LIST_WORKFLOW.md) · [FREE_DIAGNOSTIC_OFFER.md](FREE_DIAGNOSTIC_OFFER.md) · [dealix_objection_handler.md](dealix_objection_handler.md)

---

## 1. متى تُشغّل البوابة — When to run

تُشغَّل البوابة على **كل** جهة تتجاوز "أخبرني أكثر" — بعد مكالمة التأهيل
(20 دقيقة) أو بعد تعبئة نموذج طلب التشخيص. لا يُكتَب أي عرض قبل قرار البوابة.

---

## 2. الأسئلة الثمانية — The eight questions

يملأ المؤسس هذا الجدول أثناء/بعد مكالمة التأهيل. كل بند: نعم / لا / غير واضح.

| # | السؤال | English | الإجابة |
|---|--------|---------|---------|
| 1 | `pain_clear` — هل الألم محدّد وملموس؟ | Is the revenue pain clear and concrete? | ☐ |
| 2 | `owner_present` — هل صاحب القرار حاضر؟ | Is the decision owner present? | ☐ |
| 3 | `data_available` — هل بيانات الفرص جاهزة؟ | Is opportunity data available? | ☐ |
| 4 | `accepts_governance` — هل يقبل الحوكمة (اعتماد بشري لكل إرسال)؟ | Do they accept governance (human sign-off on every send)? | ☐ |
| 5 | `has_budget` — هل لديهم ميزانية للسبرنت 499 ريال؟ | Do they have budget for the 499 SAR sprint? | ☐ |
| 6 | `wants_safe_methods` — هل يطلبون طرقاً آمنة (لا scraping/spam/ضمانات)؟ | Do they want safe methods (no scraping/spam/guarantees)? | ☐ |
| 7 | `proof_path_visible` — هل مسار حزمة الإثبات واضح؟ | Is the Proof Pack path visible? | ☐ |
| 8 | `retainer_path_visible` — هل يوجد مسار محتمل لاشتراك لاحق؟ | Is a retainer path visible? | ☐ |

---

## 3. القرارات الخمسة — The five decisions

`qualify(...)` يعيد أحد خمسة قرارات. المؤسس لا يخترع قراراً سادساً.

| القرار | المعنى | الخطوة التالية |
|--------|--------|----------------|
| **ACCEPT** | الألم واضح + مالك حاضر + بيانات جاهزة. يناسب المنتج. | أرسل رابط طلب التشخيص المجاني. ابدأ ساعة 24 ساعة عند التعبئة. |
| **DIAGNOSTIC_ONLY** | يناسب التشخيص فقط؛ لا تعرض السبرنت بعد. | شغّل التشخيص المجاني. حقل التوصية عند التسليم يقرّر دعوة السبرنت. |
| **REFRAME** | نيّة حقيقية، إطار خاطئ — يطلب خدمة لا نقدّمها لكن الحاجة الأساسية تناسبنا. | أرسل ملاحظة إعادة تأطير من 3 أسطر. أعد تشغيل `qualify` بالإطار الجديد. |
| **REJECT** | خارج النطاق: تواصل بارد، أتمتة LinkedIn، ضمان مبيعات، إثراء قوائم مسروقة. | رفض مهذّب مع ذكر القاعدة الدستورية بإيجاز. سجّل في `friction_log`. لا متابعة. |
| **REFER_OUT** | الحاجة مشروعة لكن شريك آخر أنسب. | حوّل للشريك. سجّل في `referral_ledger`. لا رسوم على الإحالة الصادرة بدون اتفاق متبادل مكتوب. |

---

## 4. قاعدة الرفض الصريح — The hard refusal rule

إذا ذكر طلب الجهة (`raw_request_text`) أياً مما يلي → **REJECT فوري**:
- واتساب بارد / Cold WhatsApp.
- أتمتة LinkedIn / LinkedIn automation.
- scraping أو تجميع قوائم.
- ضمان مبيعات / guaranteed sales.

**صيغة الرفض النظيف:**
> Dealix لا يقدّم [scraping / واتساب بارد / أتمتة LinkedIn / ضمان مبيعات].
> البديل الآمن هو [مخرجات مسودة فقط / تواصل قائم على الموافقة / فرص مدعّمة
> بالأدلة]. هل تريد أن أصيغ العرض البديل؟

---

## 5. التسجيل — Logging

كل قرار يُسجَّل في `proof_ledger` كـ `event=qualify_decision` مع
`engagement_id`. قرار REJECT يُسجَّل أيضاً في `friction_log` مع السبب
مجهّل الهوية (قطاع، حجم، سبب الرفض) — بدون اسم شخصي.

---

**Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.**
