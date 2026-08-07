# H1 — Sending Ramp OS — منحنى الإرسال الآمن للسمعة

> طبقة **Market Production OS**. هذه وثيقة **رابطة**: تشرح كيف نخطّط حجم الإرسال اليومي بأمان للسمعة، وتربط الوحدات القائمة ولا تكرّرها. المصدر البرمجي الموثوق هو الكود لا هذه الوثيقة. الخطة **ليست إرسالًا** — المؤسس يوافق.

## 1. المبدأ الحاكم — خطة لا إرسال (AR)

`auto_client_acquisition/gtm_os/sending_ramp.py` هو **مخطِّط فقط**: دالة `plan_sending_batches()` تُرجِع دفعات (`batches`) ولا تُرسل أبدًا. **250 مسودة/يوم هدف إنتاجي مقبول؛ 250 إرسالًا/يوم من دومين بارد خطر على السمعة.** المنحنى يقرّر كم مسودة **معتمَدة** يجوز إرسالها اليوم بحسب عمر الدومين وصحته. كل إرسال خارجي يتطلّب موافقة المؤسس عبر `auto_client_acquisition/approval_center/` ووجود رابط إلغاء اشتراك. المسودات تأتي من المصنع في [COLD_EMAIL_DRAFT_FACTORY_AR.md](COLD_EMAIL_DRAFT_FACTORY_AR.md). لا scraping ولا قوائم مشتراة.

## 1. Governing Principle — A Plan, Not a Send (EN)

`auto_client_acquisition/gtm_os/sending_ramp.py` is a **planner only**: `plan_sending_batches()` returns `batches` and never sends. **250 drafts/day is a fine production target; 250 sends/day from a cold domain is a reputation risk.** The curve decides how many **approved** drafts may be sent today, given the domain's age and health. Every external send requires founder approval via `auto_client_acquisition/approval_center/` and a present unsubscribe link. Drafts arrive from the factory in [COLD_EMAIL_DRAFT_FACTORY_AR.md](COLD_EMAIL_DRAFT_FACTORY_AR.md). No scraping, no purchased lists.

## 2. منحنى الترقّي — RAMP_CURVE (AR)

المنحنى ثابت `RAMP_CURVE` في `sending_ramp.py`، ويُقرأ بدالة `ramp_stage_for(domain_age_days)`. العمر = أيام منذ أول إرسال من الدومين.

| المرحلة | عمر الدومين (يوم) | الحد الأقصى/يوم | شرط |
|---|---|---|---|
| أسبوع 0 — تهيئة | 0–6 | ≤ 20 | إحماء بطيء |
| أسبوع 1 | 7–13 | ≤ 50 | — |
| أسبوع 2 | 14–20 | ≤ 100 | — |
| أسبوع 3 | 21–27 | ≤ 150 | — |
| أسبوع 4+ | 28+ | ≤ 250 | **بصحة سليمة فقط** |

عند أسبوع 4+، الـ250 الكاملة لا تُتاح إلا حين تكون الصحة `healthy`؛ وإلا يهبط السقف الفعّال إلى **150** (`_FULL_VOLUME_FLOOR_WHEN_DEGRADED`).

## 2. The Ramp Curve — RAMP_CURVE (EN)

The curve is the `RAMP_CURVE` constant in `sending_ramp.py`, read by `ramp_stage_for(domain_age_days)`. Age = days since the domain's first send.

| Stage | Domain age (days) | Max/day | Condition |
|---|---|---|---|
| Week 0 — warm-up | 0–6 | ≤ 20 | Slow warm-up |
| Week 1 | 7–13 | ≤ 50 | — |
| Week 2 | 14–20 | ≤ 100 | — |
| Week 3 | 21–27 | ≤ 150 | — |
| Week 4+ | 28+ | ≤ 250 | **Healthy only** |

At week 4+, the full 250 is only available when health is `healthy`; otherwise the effective cap falls back to **150** (`_FULL_VOLUME_FLOOR_WHEN_DEGRADED`).

## 3. بوابة صحة الدومين (AR)

`BLOCKING_HEALTH = {unhealthy, bounce_spike, spam_warning}`. أي حالة منها **تحجب كل الإرسال** اليوم: الخطة تعود بـ `blocked = true`، `scheduled_count = 0`، و`governance_decision = "BLOCK"`، مع سبب ثنائي اللغة حتى المعالجة. الصحة المتدهورة (غير حاجبة) عند أسبوع 4+ تخفض السقف إلى 150 بدل المنع الكامل. مراقبة الصحة وقواعد التسليم في [DELIVERABILITY_AND_COMPLIANCE_AR.md](DELIVERABILITY_AND_COMPLIANCE_AR.md) و[../../ops/EMAIL_DELIVERABILITY.md](../../ops/EMAIL_DELIVERABILITY.md).

## 3. Domain Health Gating (EN)

`BLOCKING_HEALTH = {unhealthy, bounce_spike, spam_warning}`. Any of these **blocks all sending** today: the plan returns `blocked = true`, `scheduled_count = 0`, and `governance_decision = "BLOCK"`, with a bilingual reason, until remediated. Degraded (non-blocking) health at week 4+ lowers the cap to 150 rather than blocking outright. Health monitoring and the deliverability rules live in [DELIVERABILITY_AND_COMPLIANCE_AR.md](DELIVERABILITY_AND_COMPLIANCE_AR.md) and [../../ops/EMAIL_DELIVERABILITY.md](../../ops/EMAIL_DELIVERABILITY.md).

## 4. شروط الأهلية لكل مسودة (AR)

تمر المسودات المعتمَدة (`ApprovedDraftRef`) بأربعة فلاتر قبل الجدولة، وتُسجَّل المستبعَدات في `excluded`:

| الاستبعاد | الشرط |
|---|---|
| `not_approved` | `approval_status != "approved"` — لم يوافق المؤسس بعد |
| `missing_unsubscribe` | `unsubscribe_included = false` — لا إرسال بلا opt-out |
| `suppression_hit` | المستلم في قائمة الكبح |
| `frequency_cap` | المستلم تواصلنا معه حديثًا (سقف تكرار لكل مستلم) |

ثم `scheduled = eligible[:cap]`، وتُقطَّع الدفعات بحجم `batch_size` (افتراضي 25) في نافذة `business_hours_ksa`. الحارسات في `guardrails` كلها `true`: لا إرسال بلا موافقة، لا إرسال بلا opt-out، الكبح مُنفَّذ، سقف التكرار مُنفَّذ، صحة الدومين مُبوَّبة، المنحنى مُنفَّذ.

## 4. Per-Draft Eligibility (EN)

Approved drafts (`ApprovedDraftRef`) pass four filters before scheduling; rejects are recorded in `excluded`:

| Exclusion | Condition |
|---|---|
| `not_approved` | `approval_status != "approved"` — founder has not approved yet |
| `missing_unsubscribe` | `unsubscribe_included = false` — no send without an opt-out |
| `suppression_hit` | Recipient is on the suppression list |
| `frequency_cap` | Recipient was contacted recently (per-recipient frequency cap) |

Then `scheduled = eligible[:cap]`, batched at `batch_size` (default 25) in the `business_hours_ksa` window. Every flag in `guardrails` is `true`: no send without approval, no send without opt-out, suppression enforced, frequency cap enforced, domain health gated, ramp curve enforced.

## 5. سقف التكرار والكبح (AR)

**سقف التكرار لكل مستلم:** تُمرَّر مجموعة `recently_contacted_refs` إلى المخطِّط؛ أي مستلم فيها يُستبعَد بـ `frequency_cap` — لا نطرق الباب نفسه مرتين في نافذة قصيرة. **الكبح فوري وقطعي:** تُمرَّر `suppression_refs`، وأي مستلم في قائمة الكبح يُستبعَد بـ `suppression_hit`. أسباب الكبح (`SUPPRESSION_REASONS`): `unsubscribe`, `complaint`, `bounce`, `angry`, `manual`، وهي `permanent = true` افتراضيًا. منطق توليد الكبح من الردود في [REPLY_HANDLING_OS_AR.md](REPLY_HANDLING_OS_AR.md).

## 5. Frequency Cap and Suppression (EN)

**Per-recipient frequency cap:** pass `recently_contacted_refs` to the planner; any recipient in it is excluded as `frequency_cap` — we do not knock the same door twice in a short window. **Suppression is immediate and absolute:** pass `suppression_refs`, and any recipient on the suppression list is excluded as `suppression_hit`. Suppression reasons (`SUPPRESSION_REASONS`): `unsubscribe`, `complaint`, `bounce`, `angry`, `manual`, all `permanent = true` by default. The logic that produces suppression from replies lives in [REPLY_HANDLING_OS_AR.md](REPLY_HANDLING_OS_AR.md).

## 6. التسليم عبر البوابة الآمنة (AR)

الخطة لا تُرسل. حين يوافق المؤسس، يمرّ كل إرسال خارجي عبر `auto_client_acquisition/safe_send_gateway/` (`doctrine.py`, `middleware.py`)، التي تطبّق بنود العقيدة (لا واتساب بارد، لا أتمتة LinkedIn، لا scraping، لا إرسال خارجي بلا موافقة) وتعيد أسبابًا ثنائية اللغة عند الرفض. أي بحث عن شركة على LinkedIn يكون **manual LinkedIn company search (founder-approved per call)** فقط. فحص التسليم التشغيلي في `auto_client_acquisition/email/deliverability_check.py`.

## 6. Sending via the Safe Gateway (EN)

The plan does not send. When the founder approves, every external send passes through `auto_client_acquisition/safe_send_gateway/` (`doctrine.py`, `middleware.py`), which enforces the doctrine (no cold WhatsApp, no LinkedIn automation, no scraping, no external send without approval) and returns bilingual reasons on refusal. Any LinkedIn lookup is **manual LinkedIn company search (founder-approved per call)** only. The operational deliverability check lives in `auto_client_acquisition/email/deliverability_check.py`.

## 7. تشغيل المخطِّط (AR)

الأمر اليومي الكامل `scripts/gtm_daily_command.py` يقرأ المسودات، يشغّل البوابة، ثم يخطّط دفعة آمنة ويكتب أمرًا واحدًا للمؤسس في `reports/gtm/GTM_DAILY_COMMAND.md`. مخطط `sending_plan.schema.json` في `dealix/contracts/schemas/`.

```text
python3 scripts/gtm_daily_command.py --domain-age-days 10 --domain-health healthy
```

## 7. Running the Planner (EN)

The full daily command `scripts/gtm_daily_command.py` reads drafts, runs the gate, then plans a safe batch and writes one founder order to `reports/gtm/GTM_DAILY_COMMAND.md`. The `sending_plan.schema.json` lives in `dealix/contracts/schemas/`.

```text
python3 scripts/gtm_daily_command.py --domain-age-days 10 --domain-health healthy
```

## روابط مرجعية / Related

- [COLD_EMAIL_DRAFT_FACTORY_AR.md](COLD_EMAIL_DRAFT_FACTORY_AR.md) — مصنع المسودات / the draft factory.
- [DELIVERABILITY_AND_COMPLIANCE_AR.md](DELIVERABILITY_AND_COMPLIANCE_AR.md) — التسليم والامتثال / deliverability + compliance.
- [REPLY_HANDLING_OS_AR.md](REPLY_HANDLING_OS_AR.md) — معالجة الردود والكبح / replies + suppression.
- [../../ops/EMAIL_DELIVERABILITY.md](../../ops/EMAIL_DELIVERABILITY.md) — قائمة التسليم التشغيلية / ops deliverability checklist.
- [../../05_governance_os/APPROVAL_POLICY.md](../../05_governance_os/APPROVAL_POLICY.md) — سياسة الموافقة / approval policy.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
