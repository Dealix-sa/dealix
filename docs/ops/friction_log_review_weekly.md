# Friction Log — Weekly Review SOP

**Purpose:** كل أربعاء 09:00، المؤسس يراجع friction_log من آخر 7 أيام ويقرر: **نبني الحل، نؤجل، أو نتجاهل.**

**Master plan:** [/MASTER_PLAN.md](../../MASTER_PLAN.md)

---

## القاعدة الذهبية

> Friction log = **البيانات الحقيقية** التي تحرك قرارات البناء. ليس "ما يزعجني"، بل "ما يكسر العملية مع عميل دافع".

**لا feature جديد** يُبنى إلا إذا له ≥ 3 friction events من ≥ 2 عملاء مختلفين دافعين، أو ≥ 1 event severity=high.

---

## الإجراء (15 دقيقة كل أربعاء)

### الخطوة 1 — اقرأ آخر 7 أيام
```bash
python -c "
from auto_client_acquisition.friction_log.aggregator import aggregate
result = aggregate(customer_id='dealix_internal', window_days=7)
print(result.to_json(indent=2))
"
```

أو افتح `var/friction_log.jsonl` يدوياً واقرأ الـ entries.

### الخطوة 2 — صنّف كل entry في 3 مجموعات

| المجموعة | المعيار | الإجراء |
|---|---|---|
| 🔴 **نبني الآن** | severity=high أو ≥ 3 events متشابهة من ≥ 2 عملاء دافعين | إنشاء P0 task لـ dealix-engineer + commit في الأسبوع |
| 🟡 **نؤجل لـ G الحالي** | severity=medium + 1-2 events فقط | سجل في `docs/ops/deferred_builds.md` للمراجعة في الـ gate التالي |
| ⚪ **نتجاهل** | severity=low أو user error أو شيء خارج scope | احذف من الانتباه — لا تتابع |

### الخطوة 3 — وثّق القرار

في `docs/ops/COMPANY_CONTROL_CENTER.md`، أضف صفّ تحت "Weekly Friction Decisions":

```
| Date | Friction Event | Severity | Decision | Owner | Due |
|---|---|---|---|---|---|
| 2026-MM-DD | <kind from log> | high/med/low | BUILD/DEFER/IGNORE | self/agent | YYYY-MM-DD |
```

### الخطوة 4 — إذا BUILD، فوّض لـ dealix-engineer

```
Task: <kind> — معالجة friction event #<id>
Context:
- <عدد events> events في <window_days> days
- ≥ <X> عملاء دافعين متأثرون
- severity=<high/med>
- المعالجة المطلوبة: <اقتراح فني محدد>
Constraints:
- MASTER_PLAN.md في freeze — هذا استثناء معتمد لأنه friction حقيقي من عميل دافع
- يلتزم بـ 11 non-negotiable
- يضيف tests لكل دالة عامة جديدة
Deliverable: PR draft في 3-5 أيام
```

---

## ما لا يُعتبر friction "حقيقي"

- "أنا أحب لو الواجهة أحلى" — UX preference، ليس friction
- "ربما لو كان عندنا feature X..." — تفكير افتراضي، ليس event
- "العميل قال demo طويل" — feedback عام، ليس friction قابل للقياس
- "أتمنى لو كان أسرع" — performance gripe بدون رقم محدد

friction **حقيقي** = حدث محدد، عميل محدد، أثر محدد (وقت ضائع، خطأ، اعتراض من العميل).

---

## مقاييس الصحة الأسبوعية

في نهاية المراجعة، سجّل في تقرير الأسبوع:

| المقياس | الهدف | هذا الأسبوع |
|---|---|---|
| إجمالي friction events | < 20 | ___ |
| Severity=high events | 0 | ___ |
| Events تم build لها | حسب الحاجة | ___ |
| Events تم defer لها | ≤ 5 | ___ |
| Avg sprint delivery hours | ≤ 5 | ___ |
| Concurrent sprints | ≤ 4 | ___ |

إذا **avg sprint delivery > 5 ساعات** → triggered automation discussion في الأسبوع التالي.

إذا **concurrent sprints ≥ 4** → STOP بيع Sprint جديد حتى أحدها يكتمل.

---

## السجل التاريخي

| الأسبوع | تاريخ | events | build | defer | ignore | قرار رئيسي |
|---|---|---|---|---|---|---|
| (ابدأ من هنا أول مراجعة) | 2026-MM-DD | __ | __ | __ | __ | __ |

---

*Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة*

*Version 1.0 — 2026-05-24 — New SOP per MASTER_PLAN.md*
