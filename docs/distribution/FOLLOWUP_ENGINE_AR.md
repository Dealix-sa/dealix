# Follow-up Engine — محرّك المتابعة (Distribution OS v1)

**الغرض:** جدولة **المتابعات المستحقّة فقط** بإيقاع ثابت (cadence)، وتوليد مسودة المتابعة المناسبة لكل مرحلة. المحرّك **لا يرسل**؛ يكشف فقط ما حان وقته، ويترك الإرسال فعلاً بشرياً يدوياً بعد موافقة.

**المنفّذ:** [`scripts/generate_followup_queue.py`](../../scripts/generate_followup_queue.py) · المخطط: [`schemas/followup.schema.json`](../../schemas/followup.schema.json) · المخرَج: `reports/distribution/FOLLOWUP_QUEUE.md`.

**التشغيل:** `make followup-queue` (أو ضمن `make distribution-day`).

**مراجع:** النموذج: [DRAFT_SYSTEM_SPEC_AR.md](DRAFT_SYSTEM_SPEC_AR.md) · المراجعة: [DRAFT_APPROVAL_RUNBOOK_AR.md](DRAFT_APPROVAL_RUNBOOK_AR.md) · النظرة العامة: [PRODUCT_DISTRIBUTION_OS_AR.md](PRODUCT_DISTRIBUTION_OS_AR.md).

---

## 1) الإيقاع (Cadence)

| المُحفِّز | التوقيت | نوع المسودة (`draft_type`) |
|----------|---------|-----------------------------|
| أول تواصل | Day 0 | `outreach_first` |
| لا رد | D+2 | `outreach_followup_1` |
| لا رد | D+4 | `outreach_followup_2` |
| لا رد | D+7 | `breakup` (إغلاق مهذّب / إذن بالإغلاق) |
| وصل رد | عند الرد | `discovery_invite` |
| أُرسل عرض | بعد 48 ساعة | متابعة العرض (`proposal` follow-up) |
| أُرسل رابط دفع | بعد 24 ساعة | `payment_followup` |
| بدأ التشغيل (onboarding) | أسبوعياً | تقرير أسبوعي (`onboarding_message`) |
| عميل نشط | يوم 21–30 | `renewal_upsell` |

**مبدأ:** المتابعة تتوقف فور وصول رد — لا متابعة «عمياء» بعد تفاعل. رسالة `breakup` تطلب إذناً بالإغلاق بأدب، لا تضغط.

---

## 2) «المستحقّة فقط» (Due-only)

التقرير اليومي يعرض **ما حلّ موعده اليوم فقط**، لا كامل سجل المتابعات. هذا يمنع الإغراق ويحافظ على التركيز.

- متابعة موعدها غداً → **لا تظهر** اليوم.
- متابعة فات موعدها ولم تُعالَج → تظهر مُعلَّمة «متأخرة» (overdue).
- متابعة لمرشّح ردّ → **تُلغى** تلقائياً (لا تظهر).

كل عنصر مستحقّ يحمل: `prospect_id`، `company`، `draft_type`، تاريخ الاستحقاق، والقناة اليدوية المقترحة.

---

## 3) القنوات تبقى يدوية

كل متابعة تخرج مسودةً بالحالة `pending_approval` على قناة **يدوية** (`email` / `whatsapp_manual` / `linkedin_manual` / `phone_script`). لا يوجد إرسال آلي لأي متابعة، ولا جدولة إرسال. المحرّك يجدول **الظهور في الطابور**، لا الإرسال.

> الفرق الجوهري: نجدول **متى تُراجَع المتابعة**، لا **متى تُرسَل**. الإرسال قرار بشري في كل مرة.

---

## 4) شكل عنصر المتابعة (JSON)

التحقق عبر [`schemas/followup.schema.json`](../../schemas/followup.schema.json):

```json
{
  "followup_id": "fu_2026_0001",
  "prospect_id": "prs_2026_0042",
  "company": "Example Marketing Agency",
  "stage": "outreach_followup_1",
  "due_date": "2026-06-04",
  "channel": "email",
  "status": "due",
  "draft_id": "drf_2026_0009",
  "next_action": "راجع المسودة، وافِق، ثم انسخ وأرسِل يدوياً"
}
```

`status` ضمن: `due` (مستحقّة) · `overdue` (متأخرة) · `cancelled` (أُلغيت بعد رد) · `done` (عُولجت).

---

## 5) الاستخدام اليومي

1. `make followup-queue` (أو ضمن `make distribution-day`).
2. افتح `reports/distribution/FOLLOWUP_QUEUE.md`.
3. لكل عنصر مستحقّ: راجع مسودته في طابور المسودات → وافِق/عدّل/ارفض → انسخ وأرسِل **يدوياً** → علّم `done`.

الهدف اليومي المرجعي: معالجة ~5 متابعات مستحقّة (انظر [DRAFT_APPROVAL_RUNBOOK_AR.md](DRAFT_APPROVAL_RUNBOOK_AR.md) §4).

---

## 6) حدود صريحة

- لا إرسال آلي لأي متابعة.
- لا متابعة بعد رد (تُلغى).
- لا أكثر من مسار `breakup` واحد لكل مرشّح؛ بعده يُؤرشَف.
- لا PII في سجل المتابعات؛ الهوية مرجع عبر `prospect_id`.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

*يُبنى في هذا الـ PR. آخر تحديث: 2026-06-02.*
