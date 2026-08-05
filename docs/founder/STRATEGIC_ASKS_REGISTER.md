# Strategic Asks Register — سجل الطلبات الاستراتيجية

**Purpose / الغرض**
Append-only register of asks the founder makes of advisors, board members, customers-as-referrers, and the wider network. Tracks intros, advice, capital, and partnership opens.
سجل بالإضافة فقط للطلبات التي يطرحها المؤسس على المستشارين، المجلس، العملاء كمحيلين، والشبكة. يتتبع المعرفات، المشورة، رأس المال، وفتح الشراكات.

**Owner placeholder:** `<founder>`
**Cadence:** New asks any day. Weekly review Sunday. Quarterly cleanup of `parked`. / إضافة في أي يوم. مراجعة أسبوعية. تنظيف ربعي للطلبات المؤجَّلة.
**KPIs:** (1) عدد الطلبات `open` لأكثر من 21 يومًا (يجب أن يبقى < 5), (2) معدل النجاح للطلبات `done` (نسبة التي أنتجت مخرجًا قابلًا للقياس), (3) عدد الطلبات لكل مستشار (تجنّب الإفراط).
**Risk if missing / مخاطر الغياب:** The founder under-asks, or asks the same person three times without remembering. Trust capital leaks. / المؤسس يطلب أقل مما يجب، أو يطلب من نفس الشخص ثلاث مرات دون أن يتذكر. رأس مال الثقة يتسرّب.

---

## EN — How to use

1. Append a new row. Do not edit existing rows except to advance `status` and fill `closed_at` + `outcome`.
2. An ask must name a target role or person type — never "someone in healthcare".
3. Urgency is honest. `high` means the ask has a deadline in < 14 days.
4. Outcomes are written even when the ask was declined or ignored. "No response" is a valid outcome.
5. Never ask the same individual for more than one open ask at a time.

## AR — طريقة الاستخدام

1. أضف صفًا جديدًا. لا تعدّل صفًا قائمًا إلا لتحديث `status` وملء `closed_at` و `outcome`.
2. كل طلب يسمّي دورًا أو نوع شخص — وليس «شخص ما في الصحة».
3. العجلة صادقة. `high` تعني الطلب له موعد نهائي خلال 14 يومًا.
4. تُكتب النتيجة حتى لو رُفض الطلب أو أُهمل. «لا رد» نتيجة صالحة.
5. لا تطلب من نفس الشخص أكثر من طلب مفتوح واحد في الوقت ذاته.

---

## Schema / الهيكل

| Field | Type | Notes |
|---|---|---|
| `id` | string | `ASK-YYYYMMDD-NN` |
| `ask_en` | text | One sentence. Verb first. |
| `ask_ar` | text | جملة واحدة. الفعل أولًا. |
| `target` | string | Role / person type, not full PII. e.g. `Riyadh-based clinic operator advisor`. |
| `urgency` | enum | `low` / `med` / `high` |
| `status` | enum | `open` / `in-flight` / `done` / `parked` |
| `owner` | string | Role placeholder. Default `<founder>`. |
| `opened_at` | date | When the ask was first articulated. |
| `closed_at` | date | When status left `open` or `in-flight`. |
| `outcome` | text | What actually happened. "No response by day 21" is valid. |
| `category` | enum | `intro` / `advice` / `capital` / `partner` / `talent` |

---

## Seed rows / أمثلة مبدئية

### ASK-20260524-01

- **ask_en:** Request a warm intro to one clinic-chain operator in Riyadh open to a Revenue Intelligence sprint.
- **ask_ar:** طلب إحالة دافئة إلى مشغّل سلسلة عيادات في الرياض منفتح على سبرنت Revenue Intelligence.
- **target:** Healthcare-sector advisor in the network.
- **urgency:** med
- **status:** open
- **owner:** `<founder>`
- **opened_at:** 2026-05-24
- **closed_at:** —
- **outcome:** —
- **category:** intro

### ASK-20260524-02

- **ask_en:** Ask one finance-advisor contact to review the unit economics in `docs/sales-kit/dealix_financial_model.md` and flag two errors.
- **ask_ar:** اطلب من مستشار مالي مراجعة اقتصاديات الوحدة في `docs/sales-kit/dealix_financial_model.md` ووضع علامة على خطأين.
- **target:** Independent finance advisor.
- **urgency:** low
- **status:** open
- **owner:** `<founder>`
- **opened_at:** 2026-05-24
- **closed_at:** —
- **outcome:** —
- **category:** advice

### ASK-20260524-03

- **ask_en:** Approach one Saudi B2B agency about a referral arrangement, no commercial commitments in writing yet.
- **ask_ar:** اطرق باب وكالة سعودية B2B واحدة لترتيب إحالة، بدون التزامات تجارية مكتوبة بعد.
- **target:** Saudi marketing/B2B agency principal.
- **urgency:** med
- **status:** open
- **owner:** `<founder>`
- **opened_at:** 2026-05-24
- **closed_at:** —
- **outcome:** —
- **category:** partner

### ASK-20260524-04

- **ask_en:** Identify one Saudi B2B Researcher candidate via a known network referral; do not post publicly yet.
- **ask_ar:** التعرّف على مرشّح واحد لدور Saudi B2B Researcher عبر إحالة شبكة موثوقة؛ لا تنشر إعلانًا عامًا بعد.
- **target:** Person in the founder's direct network with strong sector knowledge.
- **urgency:** high
- **status:** open
- **owner:** `<founder>`
- **opened_at:** 2026-05-24
- **closed_at:** —
- **outcome:** —
- **category:** talent

---

## آداب الطلب / Ask hygiene

### AR

- اجعل الطلب محددًا. «نصيحة» ليست طلبًا — «راجع هذا المستند خلال 7 أيام وأشر لخطأين» طلب.
- اشكر بنتيجة، لا برسالة شكر مجردة. أرسل تحديثًا بعد 14 يومًا يقول ما حدث.
- لا تطلب من شخص اعتذر مرتين متتاليتين. هذا ليس "غير مهتم"، بل احترام.
- لا تطلب رأس مال قبل أن يكون لديك سؤال واضح: كم، لماذا، إلى متى، بأي شروط ممكنة.

### EN

- Make the ask specific. "Advice" is not an ask — "review this doc in 7 days and flag two errors" is.
- Thank with an outcome, not a thank-you message. Send a 14-day follow-up that says what happened.
- Do not ask someone who has politely declined twice. That is respect, not "not interested".
- Do not ask for capital before you have a clear question: how much, why, by when, on what terms.

---

## Aggregate report (weekly) / تقرير مجمَّع أسبوعي

Each Sunday, the founder pulls four numbers:

| Metric | Number |
|---|---|
| Open asks > 21 days | <n> |
| Asks closed this week | <n> |
| Done-rate (`done` ÷ closed) | <pct> |
| Unique people asked this week | <n> |

> If "Unique people asked this week" = 0 for two weeks in a row, the founder is hoarding asks. That is a signal as severe as a bottleneck. / إذا كان «الأشخاص المختلفون الذين طُلب منهم هذا الأسبوع» = 0 لأسبوعين متتاليين، فالمؤسس يكنز الطلبات. هذه إشارة بشدة عنق الزجاجة.

---

## Disclosure / إفصاح

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

## Related canonical docs

- `docs/founder/STRATEGIC_ASSUMPTIONS_REGISTER.md`
- `docs/founder/FOUNDER_LEVERAGE_DASHBOARD.md`
- `docs/strategy/CEO_STRATEGY.md`
- `docs/company/DECISION_RULES.md`
- `docs/strategy/PARTNERSHIPS.md`
