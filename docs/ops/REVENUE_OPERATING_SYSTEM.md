<!-- Owner: dealix-pm | Date: 2026-05-18 | Arabic primary | Workstream E — CEO Commercial Activation Plan -->
<!-- Operating runbook only — no product code, no new dashboard. Respects docs/ops/COMMERCIAL_FREEZE.md -->
<!-- Cadence references DAILY_OPERATING_LOOP.md, DAILY_COMMERCIAL_LOOP_AR.md, growth/DAILY_SCORECARD.md — does not duplicate them -->

# نظام تشغيل الإيراد — Revenue Operating System (Cadence Runbook)

> **هذه وثيقة تنسيق، وليست نظام التشغيل اليومي بحد ذاته.** الحلقة اليومية التفصيلية في
> [`DAILY_OPERATING_LOOP.md`](DAILY_OPERATING_LOOP.md) و
> [`DAILY_COMMERCIAL_LOOP_AR.md`](DAILY_COMMERCIAL_LOOP_AR.md)، وورقة النتائج في
> [`../growth/DAILY_SCORECARD.md`](../growth/DAILY_SCORECARD.md). هذه الوثيقة **تربط** تلك
> الحلقات بالوكلاء المتخصصين — ولا تكرّرها.
>
> **This is an orchestration runbook, not the daily operating loop itself.** The detailed daily
> loop lives in [`DAILY_OPERATING_LOOP.md`](DAILY_OPERATING_LOOP.md) and
> [`DAILY_COMMERCIAL_LOOP_AR.md`](DAILY_COMMERCIAL_LOOP_AR.md); the score sheet is
> [`../growth/DAILY_SCORECARD.md`](../growth/DAILY_SCORECARD.md). This document **ties** those
> loops to the specialized agents — it does not duplicate them.

---

## 0. القاعدة الأولى — The First Rule

**كل إجراء خارجي هو مسوّدة بانتظار موافقة المؤسس.** لا إرسال مباشر، لا شحن مباشر، لا واتساب
بارد — `no_live_send`، `no_live_charge`، `no_cold_whatsapp`. الوكلاء يولّدون مسوّدات وتوصيات
فقط؛ المؤسس وحده يضغط «إرسال». هذا قيد عقائدي مُنفَّذ في الكود، وليس تفضيلاً.

**Every external action is a draft awaiting founder approval.** No live send, no live charge,
no cold WhatsApp — `no_live_send`, `no_live_charge`, `no_cold_whatsapp`. The agents produce
drafts and recommendations only; the founder alone presses "send". This is a code-enforced
doctrine constraint, not a preference.

هذا النظام يعمل تحت [`COMMERCIAL_FREEZE.md`](COMMERCIAL_FREEZE.md): جهد بناء المنتج مُجمَّد؛
**كل** الطاقة في التشغيل والبيع. «الأتمتة الكاملة» هنا تعني آلة ذهاب-إلى-السوق منسَّقة بالوكلاء —
لا توسيعاً للمنتج.

---

## 1. الوكلاء المتخصصون وأدوارهم — The Specialized Agents

| الوكيل / Agent | الدور / Role | يلمس الكود؟ / Touches code? | المخرَج / Output |
|---|---|---|---|
| `dealix-sales` | يؤهّل القائمة الدافئة، يرتّب طابور التواصل، يصيغ العروض، يوصي بالرتبة | لا / no | **طابور مسوّدات** للمراجعة |
| `dealix-content` | يحدّث أصول البيع، منشورات LinkedIn، تسلسلات البريد، صفحات القطاعات | لا / no | أصول مُحدَّثة (مسوّدات) |
| `dealix-delivery` | يشغّل السبرنتات، يجمّع Proof Packs، يسجّل الأصول الرأسمالية | لا / no | تسليمات + قيود في السجلّات |
| `dealix-engineer` | يلمس الكود **فقط** للرتبة 0–1 + بنود P0/P1 | نعم — مقيَّد / yes — bounded | إصلاحات مُغطّاة باختبارات |
| `dealix-pm` | يملك الإيقاع، سجل الاحتكاك، المراجعة الأسبوعية، بوابات القرار | لا / no | نقطة المساءلة الواحدة |

**حدّ `dealix-engineer` تحت التجميد — Engineer scope under the freeze.** بموجب
[`COMMERCIAL_FREEZE.md`](COMMERCIAL_FREEZE.md)، المهندس يعمل **فقط** على: إنهاء تسليم الرتبة 0–1
(عرض Proof Pack/التشخيص بصيغة HTML/PDF، رابط تدقيق الدفع←التسليم)، وإصلاحات P0/P1 (بناء معطّل،
بوابة معطّلة، أمان/عقيدة). لا رُتب 2–5، لا لوحات جديدة، لا تجميل واجهة.

---

## 2. الحلقة اليومية — The Daily Loop

تُشغَّل كل يوم عمل (أحد–خميس). الإيقاع التفصيلي بالساعة في
[`DAILY_OPERATING_LOOP.md`](DAILY_OPERATING_LOOP.md). الجدول التالي يُسنِد كل خطوة إلى وكيلها.

Runs every business day (Sun–Thu). The hour-by-hour rhythm is in
[`DAILY_OPERATING_LOOP.md`](DAILY_OPERATING_LOOP.md). The table below assigns each step to its
agent.

| # | الخطوة / Step | الوكيل / Agent | المخرَج / Output |
|---|---|---|---|
| 1 | فحص الأنظمة + مراجعة خط الأنابيب / systems check + pipeline review | `dealix-pm` | متابعات اليوم محدَّدة |
| 2 | اختيار أفضل 10 أهداف من القائمة الدافئة + تأهيلها / pick top 10 warm targets + qualify | `dealix-sales` | درجات تأهيل (`qualification.py`) |
| 3 | صياغة طابور التواصل (10 رسائل) + 5 متابعات / draft outreach queue + 5 follow-ups | `dealix-sales` | **مسوّدات** — لا إرسال |
| 4 | إرفاق أصل إثبات واحد لكل هدف / attach one proof asset per target | `dealix-content` | أصول مرفقة بالمسوّدات |
| 5 | مراجعة المؤسس + الموافقة على المسوّدات / founder reviews + approves drafts | **المؤسس / Founder** | إرسالات معتمدة فقط |
| 6 | معالجة الردود + حجز العروض التوضيحية / handle replies + book demos | `dealix-sales` + المؤسس | عروض محجوزة |
| 7 | تجهيز/تمرين تسليم السبرنت (بيانات عيّنة مُنقَّحة) / sprint delivery prep or dry-run (redacted sample data) | `dealix-delivery` | حركة تسليم مُتمرَّن عليها |
| 8 | تحديث المحتوى (أيام الإثنين/الأربعاء/الجمعة فقط) / content refresh (M/W/F) | `dealix-content` | منشور/أصل مسوّدة |
| 9 | بطاقة نهاية اليوم / end-of-day scorecard | `dealix-pm` | [`../growth/DAILY_SCORECARD.md`](../growth/DAILY_SCORECARD.md) مُعبّأة |

**سجل الاحتكاك — Friction log.** أي خطوة تتعثّر (رسالة بصفر ردود، عرض توضيحي بلا حضور، اعتراض
متكرر، عائق تسليم) تُسجَّل بواسطة `dealix-pm`. سجل الاحتكاك يُغذّي المراجعة الأسبوعية (§3) وقد
يُطلِق إعادة كتابة محتوى من `dealix-content`.

---

## 3. حلقة المراجعة الأسبوعية للتحسين الذاتي — Weekly Self-Improvement Review

تُشغَّل بعد ظهر الجمعة. يقودها `dealix-pm`. تحوّل سجل الاحتكاك إلى **قرار واحد**.

Runs Friday afternoon, led by `dealix-pm`. Turns the friction log into **one decision**.

| السؤال / Question | المصدر / Source |
|---|---|
| أفضل قطاع هذا الأسبوع؟ / best segment? | درجات `qualification.py` + التحويلات |
| أفضل رسالة؟ / best message? | معدّلات الرد لكل مسوّدة |
| أسوأ قناة؟ / worst channel? | توزيع القنوات في [`../growth/DAILY_SCORECARD.md`](../growth/DAILY_SCORECARD.md) |
| أعلى اعتراض؟ / top objection? | سجل الاحتكاك + [`reply_handling_log.md`](reply_handling_log.md) |

**القرار الواحد — The one decision.** اختر إجراءً واحداً فقط:

1. **ضاعِف** على أفضل قطاع/رسالة. / **Double down** on the best segment/message.
2. **أصلِح الرسالة** التي لا تُحقّق ردوداً (تفويض `dealix-content`). / **Fix the message**.
3. **غيّر الـ ICP** إن كان القطاع لا يحوّل. / **Change the ICP**.
4. **حسّن الإثبات** — أصل بيع أقوى (تفويض `dealix-content` + `dealix-delivery`). / **Improve proof**.
5. **أوقِف القناة** الأضعف. / **Kill the channel**.

يُسجَّل القرار في [`../ledgers/DECISION_LEDGER.md`](../ledgers/DECISION_LEDGER.md) ويُعاد ضبط
النموذج المالي في [`../ledgers/FINANCIAL_MODEL_AND_UNIT_ECONOMICS.md`](../ledgers/FINANCIAL_MODEL_AND_UNIT_ECONOMICS.md) §2
بأرقام القائمة الدافئة الحقيقية.

---

## 4. بوابات القرار الثلاث — The Three Decision Gates

من خطة التدشين التجاري. لا تُتجاوَز بوابة دون مالك وإجراء تالٍ.

From the Commercial Activation Plan. No gate is bypassed without an owner and a next action.

| البوابة / Gate | متى / When | القاعدة / Rule |
|---|---|---|
| **1 — بوابة الجاهزية / Readiness** | بعد تقييم بوابات الجاهزية | أي بوابة **حمراء** تُوقف التواصل الخارجي حتى تُسنَد لمالك. |
| **2 — بوابة التسليم / Delivery** | بعد إنهاء تسليم الرتبة 0–1 | اختبارات اللوائح غير القابلة للتفاوض (`tests/test_no_*.py`، `tests/governance/`) **خضراء** — وإلا لا يُشحَن التسليم. |
| **3 — بوابة الإثبات / Proof** | عند تسليم أول Pilot | لا اعتماد L3+ ← شخّص في سجل الاحتكاك، **لا تُعلِن الخروج من التجميد**. |

**شرط الخروج من التجميد — Freeze exit.** Pilot مدفوع واحد مُسلَّم + Proof Pack معتمد من العميل
بمستوى L3+. عندها فقط تحكم [`../90_DAY_BUSINESS_EXECUTION_PLAN.md`](../90_DAY_BUSINESS_EXECUTION_PLAN.md)
وقد تفتح مُطلِقات البناء المشروط الرتبة 2.

---

## 5. الضوابط العقائدية — Doctrine Guards (always-on)

- كل مخرَج خارجي = مسوّدة بانتظار موافقة المؤسس (`no_live_send`).
- لا شحن مباشر؛ Moyasar في وضع الاختبار حتى يقلبه المؤسس يدوياً (`no_live_charge`).
- لا واتساب بارد، لا كشط، لا أتمتة LinkedIn (`no_cold_whatsapp`, `no_scraping`).
- لا ادعاءات بلا مصدر، لا نتائج غير مُتحقَّقة، لا لغة عائد/إيراد مضمون.
- كل عميل يمرّ عبر `qualification.py` — يريد كشطاً أو ضماناً ← `REJECT`.
- كل ارتباط مدفوع يُنتج Proof Pack (L3+) وأصلاً رأسمالياً واحداً على الأقل.
- `dealix-engineer` لا يلمس إلا الرتبة 0–1 و P0/P1 تحت التجميد.

> **النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.**
