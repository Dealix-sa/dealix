# Distribution Metrics — مقاييس التصريف (Distribution OS v1)

**الغرض:** ما يقيسه النظام كل يوم: حجم المسودات وتوزيعها، المتابعات المستحقّة، والقِمع الذي يهمّ المؤسس فعلاً (ردود، مكالمات اكتشاف، عروض، روابط دفع، فوز/خسارة). **أرقام الإيراد لا تُختَرع أبداً** — تأتي من دفع/أدلة فقط.

**المنفّذ:** [`scripts/distribution_metrics.py`](../../scripts/distribution_metrics.py) · المخرَج: `reports/distribution/DISTRIBUTION_METRICS.md`.

**التشغيل:** `make distribution-metrics` (أو ضمن `make distribution-day`).

**مراجع:** النموذج: [DRAFT_SYSTEM_SPEC_AR.md](DRAFT_SYSTEM_SPEC_AR.md) · المتابعة: [FOLLOWUP_ENGINE_AR.md](FOLLOWUP_ENGINE_AR.md) · النظرة العامة: [PRODUCT_DISTRIBUTION_OS_AR.md](PRODUCT_DISTRIBUTION_OS_AR.md) · القِمع التجاري الأشمل: [NORTH_STAR_METRICS_AR.md](../commercial/NORTH_STAR_METRICS_AR.md).

---

## 1) مقاييس المسودات (نشاط الماكينة)

| المقياس | التعريف |
|---------|---------|
| المسودات المُولَّدة | عدد المسودات التي أنتجها المولّد اليوم |
| حسب الحالة (by status) | توزيع على `generated` / `pending_approval` / `approved` / `needs_edit` / `rejected` / `copied_manually` / `replied` / `archived` |
| حسب النوع (by type) | توزيع على `outreach_first` … `renewal_upsell` |
| حسب القناة (by channel) | توزيع على القنوات اليدوية (`email` / `whatsapp_manual` / `linkedin_manual` / `phone_script` / `proposal_pdf` / `internal_note`) |

هذه مقاييس **نشاط** (هل الماكينة تعمل؟)، لا مقاييس نتيجة.

---

## 2) المتابعات المستحقّة

| المقياس | التعريف |
|---------|---------|
| متابعات مستحقّة اليوم | عدد عناصر `due` في طابور المتابعة |
| متأخرة (overdue) | عناصر فات موعدها ولم تُعالَج |
| أُلغيت بعد رد | متابعات توقفت لأن المرشّح ردّ |

المصدر: [FOLLOWUP_ENGINE_AR.md](FOLLOWUP_ENGINE_AR.md).

---

## 3) القِمع الذي يهمّ المؤسس (نتائج)

| مرحلة القِمع | المقياس | المصدر |
|--------------|---------|--------|
| ردود (replies) | عدد المسودات بالحالة `replied` | حالة المسودة |
| مكالمات اكتشاف (discovery booked) | عدد مكالمات الاكتشاف المحجوزة | تسجيل المؤسس |
| عروض (proposals) | عدد العروض المُرسلة يدوياً | [PROPOSAL_FACTORY_AR.md](PROPOSAL_FACTORY_AR.md) |
| روابط دفع (payment links) | عدد روابط الدفع المُرسلة | تسجيل المؤسس |
| فوز/خسارة (won / lost) | الصفقات المغلقة فوزاً أو خسارة | مسار الأدلة التجاري |

**قاعدة:** «won» لا يُسجَّل إلا بعد `payment_received` حقيقي. ربط هذه الأرقام بمسار الأدلة في [DAILY_COMMERCIAL_LOOP_AR.md](../ops/DAILY_COMMERCIAL_LOOP_AR.md) — لا ازدواج مصدر حقيقة.

---

## 4) قاعدة الإيراد: لا أرقام مخترعة

> أي رقم إيراد أو pipeline في تقارير التصريف يأتي **حصراً** من دفع مؤكّد أو حدث إثبات حقيقي. لا يخترع النظام إيراداً ولا معدل تحويل ولا ROI.

- لا «متوسط صفقة» مُقدَّر يُعرَض كحقيقة.
- لا معدل رد/تحويل يُكتب كوعد — يُعرَض كنمط مُلاحَظ فقط.
- صفوف القوالب وأسماء التشغيل (مثل أيام التشغيل الداخلية) **لا تُحسب** في القِمع — تماماً كما في مسار الأدلة التجاري.

---

## 5) شكل المخرَج

`reports/distribution/DISTRIBUTION_METRICS.md` (مثال مبسّط):

```text
# Distribution Metrics — 2026-06-02

## Drafts
generated_today: 18
by_status: {pending_approval: 12, approved: 4, rejected: 2}
by_type:   {outreach_first: 8, outreach_followup_1: 5, proposal: 1, ...}
by_channel:{email: 11, linkedin_manual: 4, whatsapp_manual: 3}

## Follow-ups
due_today: 5
overdue: 1

## Funnel (from evidence only)
replies: 3
discovery_booked: 2
proposals_sent: 1
payment_links_sent: 0
won: 0   lost: 0
```

---

## 6) كيف تقرأ المقاييس

| إشارة | تفسير |
|-------|--------|
| رفض = 0 باستمرار | مراجعة سطحية — ارفع التدقيق ([DRAFT_APPROVAL_RUNBOOK_AR.md](DRAFT_APPROVAL_RUNBOOK_AR.md)) |
| متابعات متأخرة تتراكم | لم تُعالَج المتابعات المستحقّة — أولوية الغد |
| ردود > 0 لكن discovery = 0 | المشكلة في الانتقال من رد إلى مكالمة، لا في التواصل |
| won يتقدّم على proof | راجع — لا توسعة قبل Proof ([PROOF_PACK_FACTORY_AR.md](PROOF_PACK_FACTORY_AR.md)) |

---

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

*يُبنى في هذا الـ PR. آخر تحديث: 2026-06-02.*
