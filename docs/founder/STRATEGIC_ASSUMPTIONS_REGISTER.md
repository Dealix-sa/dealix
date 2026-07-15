# Strategic Assumptions Register — سجل الافتراضات الاستراتيجية

**Purpose / الغرض**
Append-only register of the strategic bets Dealix is making (sector picks, pricing posture, GTM bets). Every bet is testable and tied to evidence required to validate or invalidate it.

**Owner placeholder:** `<founder>`
**Cadence:** Weekly review on Sunday; new rows added any day, never edited in place — only status transitions.
**KPIs:** (1) % of open assumptions with an evidence_required field filled, (2) median age of `open` assumptions in days, (3) count of `invalidated` rows that triggered a documented decision change.
**Risk if missing:** Strategy drifts. Decisions are made on stale intuitions. The same bet is re-litigated weekly without a record.

---

## EN — How to use

1. Add a new row only. Never overwrite a row — change `status` and append `closed_at` instead.
2. One assumption per row. If you find yourself writing "and", split it.
3. `evidence_required` must be concrete (e.g., "3 paid pilots in clinics within 60 days"), not abstract ("market interest").
4. Linked decision points to the doc or commit where this assumption was acted on.

## AR — طريقة الاستخدام

1. أضف صفًا جديدًا فقط. لا تستبدل صفًا — غيّر `status` وأضف `closed_at`.
2. افتراض واحد لكل صف. إذا وجدت نفسك تكتب «و»، قسّمها.
3. `evidence_required` يجب أن يكون ملموسًا (مثال: «3 تجارب مدفوعة في عيادات خلال 60 يومًا»)، وليس مجردًا («اهتمام السوق»).
4. `linked_decision` يشير إلى المستند أو الـ commit الذي بُني على هذا الافتراض.

---

## Schema / الهيكل

| Field | Type | Notes |
|---|---|---|
| `id` | string | `ASM-YYYYMMDD-NN` |
| `assumption_en` | text | One sentence. |
| `assumption_ar` | text | جملة واحدة. |
| `confidence` | enum | `low` / `med` / `high` |
| `evidence_required` | text | Concrete signal that would validate or invalidate. |
| `owner` | string | Role placeholder. |
| `review_date` | date | Next review checkpoint. |
| `status` | enum | `open` / `validated` / `invalidated` / `retired` |
| `linked_decision` | path | Relative path to the decision doc, PR, or commit. |
| `closed_at` | date | Filled only when status leaves `open`. |

---

## Seed rows / الصفوف الأولية

### ASM-20260524-01

- **assumption_en:** Saudi mid-market clinics (15–60 staff) will pay for a Revenue Intelligence sprint at the published mid-tier price within 30 days of a referred intro.
- **assumption_ar:** عيادات السوق المتوسطة في السعودية (15–60 موظفًا) ستدفع مقابل سبرنت Revenue Intelligence بالسعر المتوسط المُعلَن خلال 30 يومًا من إحالة موصى بها.
- **confidence:** med
- **evidence_required:** 2 paid sprints from this segment, both sourced via referral, both closed within 30 days of first contact.
- **owner:** `<founder>`
- **review_date:** 2026-06-21
- **status:** open
- **linked_decision:** `docs/strategy/VERTICAL_PLAYBOOKS.md`
- **closed_at:** —

### ASM-20260524-02

- **assumption_en:** A fixed-scope diagnostic priced as a small entry deliverable converts to a paid sprint at a rate high enough to justify the diagnostic margin.
- **assumption_ar:** التشخيص بنطاق ثابت بسعر دخول صغير يتحوّل إلى سبرنت مدفوع بمعدل يبرر هامش التشخيص.
- **confidence:** low
- **evidence_required:** Conversion ratio measured across the first 6 diagnostics; floor target documented in `docs/company/PRICING_DECISION.md` once observed.
- **owner:** `<founder>`
- **review_date:** 2026-07-05
- **status:** open
- **linked_decision:** `docs/03_commercial_mvp/SPRINT_PRICING_LOGIC.md`
- **closed_at:** —

### ASM-20260524-03

- **assumption_en:** Founder-only delivery can sustain three concurrent active customers in the first 30 days without breaching governance or response-time commitments.
- **assumption_ar:** التسليم بواسطة المؤسس وحده يمكنه تحمّل ثلاثة عملاء نشطين بالتوازي في أول 30 يومًا دون خرق الحوكمة أو التزامات وقت الاستجابة.
- **confidence:** med
- **evidence_required:** Time-audit log for 4 consecutive weeks shows founder hours under cap and zero governance-event escalations.
- **owner:** `<founder>`
- **review_date:** 2026-06-24
- **status:** open
- **linked_decision:** `docs/V14_FOUNDER_DAILY_OPS.md`
- **closed_at:** —

---

---

## Operating guardrails / ضوابط التشغيل

### EN

- An assumption without an `evidence_required` line is not eligible to drive a spend or hire decision.
- `confidence: high` is reserved for assumptions backed by at least two independent observations from paid customers — not pilots, not interest, not signal.
- An `invalidated` row must produce a linked decision change within 14 days, or the register is failing its purpose.
- A `retired` row is one that is no longer relevant — not one that turned out to be wrong. Wrong rows are `invalidated`.
- No assumption may promise a sales number, conversion rate, or guaranteed customer outcome. Frame as observation targets, not promises.

### AR

- لا يحق لافتراض بلا `evidence_required` أن يدفع قرار إنفاق أو توظيف.
- `confidence: high` محجوز للافتراضات المدعومة بملاحظتين مستقلتين على الأقل من عملاء مدفوعين — وليس تجارب، وليس اهتمام، وليس إشارات.
- الصف `invalidated` يجب أن يُنتج تغييرًا في قرار موثّق خلال 14 يومًا، وإلا فالسجل يفشل في غرضه.
- الصف `retired` لم يعد ذا صلة — وليس صفًا تبيّن خطؤه. الصفوف الخاطئة تأخذ `invalidated`.
- لا يجوز لأي افتراض أن يَعِد برقم مبيعات أو معدل تحويل أو نتيجة عميل مضمونة. صِغ الافتراض كهدف ملاحظة، لا كوعد.

---

## Review ritual / طقس المراجعة

### EN

Weekly review covers, in order:

1. New rows added in the past 7 days — verify `evidence_required` is concrete.
2. Rows whose `review_date` has passed — promote, demote, invalidate, or retire.
3. `open` rows older than 60 days with no movement — these are the dangerous ones.
4. `invalidated` rows from the prior 30 days — confirm each produced a linked decision change.

### AR

المراجعة الأسبوعية تغطّي بالترتيب:

1. الصفوف الجديدة المضافة في آخر 7 أيام — تأكد أن `evidence_required` ملموس.
2. الصفوف التي مرّ موعد مراجعتها — رفّع أو خفّض أو أبطل أو أحِل إلى التقاعد.
3. الصفوف `open` الأقدم من 60 يومًا دون حراك — هذه هي الأخطر.
4. الصفوف `invalidated` من آخر 30 يومًا — تأكد أن كلًّا منها أنتج تغيير قرار موثّق.

---

## Cross-references inside Dealix / الإحالات داخل Dealix

- Every `open` assumption that drives a hiring decision must appear in `docs/company/HIRING_TRIGGERS.md`.
- Every `open` assumption that drives a pricing change must appear in `docs/company/PRICING_DECISION.md`.
- Every `invalidated` assumption must produce a lesson in `docs/memory/sales_lessons.md` or `docs/memory/pricing_lessons.md` as appropriate.

---

## Disclosure / إفصاح

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

## Related canonical docs

- `docs/company/DECISION_RULES.md`
- `docs/company/RISK_REGISTER.md`
- `docs/strategy/CEO_STRATEGY.md`
- `docs/company/PRICING_DECISION.md`
- `docs/V14_FOUNDER_DAILY_OPS.md`
- `docs/company/HIRING_TRIGGERS.md`
- `docs/memory/sales_lessons.md`
- `docs/founder/FOUNDER_LEVERAGE_DASHBOARD.md`
- `docs/founder/STRATEGIC_ASKS_REGISTER.md`
