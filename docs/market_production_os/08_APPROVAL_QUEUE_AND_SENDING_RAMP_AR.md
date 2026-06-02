# Approval Queue & Sending Ramp OS — بوابة الموافقة وتدرّج الإرسال — Approval Queue & Sending Ramp OS

> الموضع في العمود الفقري: المكوّنان الثامن والتاسع في طبقة *Market Production OS*.
> راجع [`00_MARKET_PRODUCTION_OS_MASTER_AR.md`](00_MARKET_PRODUCTION_OS_MASTER_AR.md) §0 (التدرّج) و§7 (شرط الإرسال).

هذا المستند يحدّد **البوابة البشرية الوحيدة للإرسال**. المصنع (المكوّن 6) ينتج، البوابة (المكوّن 7)
تفلتر، وهنا **يقرّر المؤسس** ماذا يُرسل ضمن سقف يومي متدرّج. القاعدة الحاكمة:

> **250 مسودة/يوم · 0 إرسال تلقائي.** لا تتحوّل مسودة إلى إرسال إلا بقرار المؤسس،
> وضمن سقف الأسبوع، وبعد استيفاء شروط الإرسال الستة. `MAX_AUTO_SENDS = 0` في كل البيئات.

البوابة تُركّب نواتين موجودتين: `approval_center` (السياسة/المتجر/العارض/قواعد المؤسس) و
`safe_send_gateway` للإرسال المعتمد. لا واجهة جديدة — تُعرَض ضمن `/ops/approvals`.

---

## 1. التقرير اليومي للمؤسس (Daily Approval Report)

يُبنى من المسودات `compliance_status = pass` فقط، ويعرض ما يلزم لقرار سريع وواثق:

| القسم | المحتوى |
|---|---|
| Top-50 drafts | أفضل 50 مسودة مرتّبة (score + personalization + positive-reply المتوقّع) |
| High-risk drafts | مسودات `risk_level = high` معزولة وموسومة بالسبب |
| أفضل قطاع اليوم | القطاع الأعلى جودة إشارة/قبول متوقّع |
| أفضل عرض اليوم | الدرجة الأنسب من السلّم الخماسي حسب الإشارات |
| دفعة الإرسال المقترَحة | اقتراح ضمن سقف الأسبوع فقط (لا يتجاوزه) |
| تحذيرات do-not-contact | أي تطابق مع suppression أو حظر |
| تحذيرات deliverability | حالة DNS/سمعة الدومين + أي إنذار مزوّد |

> الترتيب اقتراح للمساعدة، لا قرار. المؤسس يبقى صاحب الكلمة الأخيرة على كل مسودة.

---

## 2. قرارات المؤسس (Founder Decisions)

لكل مسودة، يختار المؤسس قرارًا واحدًا. القرارات تُسجَّل عبر `schemas/approval_action.schema.json`:

| القرار | الأثر |
|---|---|
| `approve` | تصبح مؤهَّلة للإرسال ضمن السقف (لا تُرسَل فورًا بالضرورة) |
| `reject` | تُرفَض وتُؤرشَف مع السبب |
| `rewrite` | تُعاد للمصنع لإعادة صياغة كاملة |
| `shorten` | تُعاد لتقصير المحتوى |
| `make_formal` | تُعاد بنبرة أكثر رسمية |
| `change_offer` | تبديل العرض من السلّم الخماسي |
| `move_to_nurture` | الجهة غير جاهزة الآن → `nurture` |
| `do_not_contact` | حظر نهائي + إضافة لقائمة suppression |

- أي قرار غير `approve` لا يُنتِج إرسالًا — المسودة تخرج من مسار اليوم أو تعود للمصنع.
- قرار `do_not_contact` نهائي ويُحدّث `schemas/suppression.schema.json` فورًا.
- قواعد المؤسس المتكرّرة (مثل «دائمًا formal لقطاع البنوك») تُدار في `approval_center/founder_rules`.

---

## 3. تدرّج الإرسال (Sending Ramp)

السقف **حدّ أقصى للإرسال اليدوي المعتمد**، وليس إرسالًا تلقائيًا. مطابق للمرجع الرئيسي §0 حرفيًا:

| المرحلة | Drafts/day | Sends/day (سقف) | الهدف |
|---|---:|---:|---|
| Week 0 | 250 | 0–20 | اختبار الجودة والرسائل |
| Week 1 | 250 | 25–50 | warm-up وإثبات أولي |
| Week 2 | 250 | 50–100 | توسيع بحذر |
| Week 3 | 250 | 100–150 | حسب صحة الدومين |
| Week 4+ | 250+ | 150–250 | فقط إذا السمعة ممتازة |

- التقدّم بين المراحل **مشروط بصحة الدومين**، لا بمرور الزمن وحده.
- أي تدهور في مقاييس صحة الدومين → تجميد أو خفض السقف فورًا (المكوّن 7 §5).
- السقف اليومي يُطبَّق في `safe_send_gateway`؛ تجاوزه مستحيل تصميمًا.

---

## 4. شرط الإرسال (كلها معًا)

لا تُرسَل مسودة معتمدة إلا إذا تحقّقت **الشروط الستة مجتمعةً**:

```txt
send_allowed = (
  approval             AND   # قرار approve من المؤسس
  unsubscribe_included AND   # رابط إلغاء اشتراك فعّال
  domain_health_ok     AND   # DNS + سمعة الدومين سليمة
  suppression_check    AND   # المستلِم ليس في قائمة الحظر
  personalization >= P1 AND  # تخصيص لا يقل عن P1
  risk_level in {low, medium}  # لا مخاطر عالية
)
```

غياب أي شرط واحد → **لا إرسال**، حتى لو وافق المؤسس. الشروط تُفحَص لحظة الإرسال، لا وقت الاعتماد فقط
(الحالة قد تتغيّر بين اللحظتين — مثلًا تدهور سمعة الدومين أو إضافة الجهة لقائمة suppression).

---

## 5. مراجعة صحة الدومين قبل/أثناء الإرسال

قبل تنفيذ الدفعة المعتمدة، يتحقّق `safe_send_gateway` من صحة الدومين الحيّة:

- إذا كان معدّل شكوى السبام ≥ 0.3% أو ظهر تحذير مزوّد → الدفعة تتوقّف وتُرفَع للمؤسس.
- يُسجَّل كل إرسال فعلي عبر `schemas/sending_batch.schema.json` (الجهة، العرض، الوقت، الدومين).
- النتائج (ارتداد/شكوى/رد) تغذّي المراجعة الأسبوعية وقرار رفع/خفض السقف للأسبوع القادم.

> صحة الدومين شرط حيّ مستمر، لا فحص لمرة واحدة. الإرسال يخدم السمعة طويلة الأمد، لا الرقم اليومي.

---

## 6. المبدأ المعماري — لماذا بوابة بشرية؟

| السبب | الأثر |
|---|---|
| السمعة أصل لا يُستبدَل | إرسال سيّئ واحد يضرّ الدومين أسابيع |
| المؤسس يرى السياق الكامل | قرار بشري يفوق أي قاعدة آلية في الحالات الحدّية |
| التدقيق قبل الفعل | كل إرسال مسبوق بقرار موثّق — لا خرق صامت |
| الالتزام بالعقيدة | اللاء رقم 8: لا إجراء خارجي بدون موافقة |

---

## 7. الربط مع الطبقات الأخرى

- المدخل: مسودات `pass` من [`07_COMPLIANCE_DELIVERABILITY_OS_AR.md`](07_COMPLIANCE_DELIVERABILITY_OS_AR.md).
- النواة: `approval_center` (`approval_policy`/`approval_store`/`approval_renderer`/`founder_rules`) + `safe_send_gateway`.
- الواجهة: تبويب `/ops/approvals` (موجود — لا واجهة جديدة).
- المخرج: المرسَل ينتقل إلى [`04_PROSPECT_RESEARCH_OS_AR.md`](04_PROSPECT_RESEARCH_OS_AR.md) §4 (`sent → replied`) ثم طبقة الردود.
- العقيدة: المرجع الرئيسي §0 + §7 + اللاء رقم 8.

---

## EN summary

`Approval Queue & Sending Ramp OS` covers the eighth and ninth Market Production OS components —
the **only human gate for sending**. The factory produces, the gate filters, and here the founder
decides what sends within a daily, ramped cap: **250 drafts/day, 0 auto-sends**, in every
environment. The daily report (built from `pass` drafts only) shows the Top-50 drafts, isolated
high-risk drafts, the best sector and offer today, a suggested sending batch within the week's cap,
and do-not-contact plus deliverability warnings. Founder decisions are approve, reject, rewrite,
shorten, make formal, change offer, move to nurture, and do_not_contact; only approve makes a draft
eligible to send. The Sending Ramp mirrors the master table — Week 0 sends 0–20 through Week 4+ at
150–250 — and progression is gated on domain health, not elapsed time. No approved draft sends
unless all six conditions hold together (approval, unsubscribe_included, domain_health_ok,
suppression_check, personalization ≥ P1, risk_level in {low, medium}), re-checked at send time via
`safe_send_gateway`. The gate reuses `approval_center` and `safe_send_gateway` and surfaces under
`/ops/approvals` — no new UI. Reputation is a non-replaceable asset; sending serves long-term
deliverability, never the daily count.

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.
