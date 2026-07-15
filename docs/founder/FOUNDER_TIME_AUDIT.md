# Founder Time Audit — تدقيق وقت المؤسس

**الغرض / Purpose**
قالب أسبوعي لتسجيل كل ساعة وتصنيفها. ليس قائمة مهام — هو سجل ملاحظة لما حدث فعلًا.
Weekly template to log every working hour by category. Not a to-do list — a record of what actually happened.

**Owner placeholder:** `<founder>`
**Cadence:** إدخال يومي يستغرق < 4 دقائق. مراجعة أسبوعية يوم الأحد. Daily logging < 4 minutes. Weekly review on Sunday.
**KPIs:** (1) نسبة الساعات في "Revenue-direct + Customer", (2) عدد الساعات < 4 في "Personal" كإنذار, (3) عدد الإدخالات غير المصنّفة (هدف صفر).
**Risk if missing / مخاطر الغياب:** المؤسس يعتقد أنه يعمل على الأهم بينما يضيع الوقت في صيانة. The founder believes he is working on the highest priority while time leaks into maintenance.

---

## ملخص بالإنجليزية / EN summary

The Time Audit is a passive log, filled at the end of each working block. Each row is one block (15–180 minutes) with a single category. Multitasking is not a category — pick the dominant one. At the end of the week, totals roll up into the Leverage Dashboard.

---

## الفئات / Categories

| Code | الفئة (AR) | Category (EN) | Definition |
|---|---|---|---|
| RD | إيرادات مباشرة | Revenue-direct | مكالمة مع مشتري، إغلاق عرض، توقيع. Direct paying-customer conversation, close, signing. |
| CU | عميل | Customer | تسليم لعميل مدفوع، مراجعة، ضمان جودة. Delivery work, QA on live paid engagements. |
| BD | بناء | Building | نظام داخلي، توثيق، أتمتة، مراجعة كود. Internal system, doc, automation, code review. |
| DG | تفويض | Delegation | إحاطة فريق، فك انسداد، اعتماد مخرج. Briefing the team, unblocking, approving output. |
| LR | تعلّم | Learning | قراءة قطاع، تحليل منافس، دراسة قانون. Sector reading, competitor study, regulation review. |
| PR | شخصي | Personal | نوم، رياضة، عائلة، صلاة، طعام، صفاء. Sleep, exercise, family, prayer, food, clarity. |
| UN | غير مصنّف | Uncategorized | يجب أن يكون صفرًا في نهاية الأسبوع. Must be zero by end of week. |

---

## نموذج الإدخال اليومي / Daily entry table

```csv
date,block_start,block_end,minutes,category,one_line_what,delegable_yes_no
2026-05-24,07:30,08:15,45,LR,قراءة تقرير قطاع الصحة,no
2026-05-24,08:15,09:00,45,RD,مكالمة مع مدير عيادة في الرياض,no
2026-05-24,09:00,10:30,90,BD,تحديث Proposal OS schema,maybe
2026-05-24,10:30,11:00,30,DG,إحاطة الباحث على قائمة ICP جديدة,no
2026-05-24,11:00,12:30,90,CU,تسليم تقرير Revenue Intelligence لعميل #2,no
2026-05-24,12:30,13:30,60,PR,صلاة الظهر وغداء,no
2026-05-24,13:30,15:00,90,RD,عرض demo لمصنع في الدمام,no
2026-05-24,15:00,16:00,60,DG,مراجعة مقترح صمّمه Sales Asset Designer,no
2026-05-24,16:00,17:30,90,BD,صياغة قسم جديد في Trust Pack,yes
2026-05-24,17:30,18:00,30,DG,ردود على أسئلة الفريق,no
```

العمود `delegable_yes_no` هو السؤال الأهم. كل `yes` تعني هذه الساعة كان يجب ألا يقضيها المؤسس.

The `delegable_yes_no` column is the most important question. Every `yes` means the founder should not have spent this hour himself.

---

## ملخص أسبوعي / Weekly rollup

```csv
week_of,RD_hours,CU_hours,BD_hours,DG_hours,LR_hours,PR_hours,UN_hours,total_hours,delegable_yes_count,delegable_yes_hours
2026-05-24,21,11,9,6,3,52,0,102,4,7.5
```

> ساعات الشخصي تشمل ساعات النوم لتعكس استدامة الجدول الفعلي. هدف PR ≥ 49 ساعة/أسبوع (7 × 7).
> Personal hours include sleep to reflect schedule sustainability. PR target ≥ 49 hr/week (7 × 7).

---

## مصفوفة التقييم الذاتي / Self-scoring matrix

في نهاية الأسبوع، يجيب المؤسس على ست عبارات بدرجة 1–5 (1 = لا، 5 = نعم بقوة):

| # | العبارة (AR) | Statement (EN) |
|---|---|---|
| 1 | كل ساعة `RD` كانت مع مشترٍ حقيقي مؤهَّل. | Every `RD` hour was with a qualified buyer. |
| 2 | لم أعد عمل أحد في الفريق هذا الأسبوع. | I did not redo any team member's work this week. |
| 3 | أعرف اسم وعمر أقدم عنصر في طابور الموافقات. | I know the name and age of the oldest item in the approval queue. |
| 4 | تنفسّت بعمق خمس مرات على الأقل قبل اجتماع صعب. | I took five deep breaths before at least one hard meeting. |
| 5 | أكلت وصليت دون لمس الهاتف ثلاث مرات هذا الأسبوع. | I ate and prayed without touching my phone at least three times this week. |
| 6 | لدي قرار واحد سيُحرر 5 ساعات في الأسبوع القادم. | I have one decision queued that will free 5+ hours next week. |

- **مجموع ≥ 24** صحي.
- **18–23** راقب — اختر بندًا واحدًا للأسبوع القادم.
- **< 18** أوقف التزامًا خارجيًا واحدًا وشغّل playbook إزالة عنق الزجاجة.

---

## قواعد التسجيل / Logging rules

### AR

- إدخالاتك فقط — لا تطلب من المساعد ملءها.
- كتلة بحد أدنى 15 دقيقة. أقل من ذلك = تشتّت، اجمعها في كتلة DG.
- لا يوجد "اجتماعات" كفئة — كل اجتماع له فئة. مع عميل = RD أو CU. مع فريق = DG. مع نفسك = BD أو LR.
- إذا انتهى الأسبوع و UN > 0، أعد تصنيف. لا تترك أي ساعة بلا تفسير.

### EN

- Your entries only — do not have an assistant fill this.
- Minimum block 15 minutes. Less than that is fragmentation; roll up under DG.
- "Meetings" is not a category. With a buyer = RD/CU. With team = DG. With yourself = BD/LR.
- If the week ends with UN > 0, recategorize. No hour is left unexplained.

---

## ربط مع الأنظمة الأخرى / Ties to other systems

- المجاميع الأسبوعية تُدخل في `docs/founder/FOUNDER_LEVERAGE_DASHBOARD.md`.
- النسب الشهرية تُدخل في `docs/company/MONTHLY_EXECUTIVE_NARRATIVE.md`.
- كل بند `delegable: yes` يجب أن يظهر كمهمة في playbook التفويض في `docs/people/FOUNDER_BOTTLENECK_REMOVAL.md`.

---

## Disclosure / إفصاح

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

## Related canonical docs

- `docs/founder/FOUNDER_LEVERAGE_DASHBOARD.md`
- `docs/founder/CEO_ATTENTION_BUDGET.md`
- `docs/team/founder_sop.md`
- `docs/ops/FOUNDER_DAILY_ANCHOR_AR.md`
- `docs/ops/FOUNDER_WEEKLY_METRICS_AR.md`
- `docs/people/FOUNDER_BOTTLENECK_REMOVAL.md`
