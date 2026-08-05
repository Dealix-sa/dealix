# Founder Bottleneck Removal — إزالة عنق الزجاجة من المؤسس

**Purpose / الغرض**
How to detect when the founder is the bottleneck and the playbook to delegate, automate, or eliminate the work — in that order of preference.
كيف يُكتشَف أن المؤسس عنق الزجاجة، وdاللعبة الكتيّبة للتفويض أو الأتمتة أو الإلغاء — بهذا الترتيب من التفضيل.

**Owner placeholder:** `<founder>` (self-detect) + Delivery Coordinator as second pair of eyes.
**Cadence:** Daily signal scan in `docs/ops/FOUNDER_DAILY_ANCHOR_AR.md`. Weekly explicit review. / فحص يومي للإشارات. مراجعة أسبوعية صريحة.
**KPIs:** (1) count of bottleneck signals open > 48h, (2) median TTR (time-to-resolve) per signal class, (3) ratio of "delegate / automate / eliminate" decisions per quarter.
**Risk if missing / مخاطر الغياب:** The founder is the bottleneck and is the last to know. Growth caps. Team morale erodes from waiting. / المؤسس عنق الزجاجة وآخر من يدري. النمو يتوقف. معنويات الفريق تتآكل من الانتظار.

---

## EN summary

Five signals tell you the founder has become the bottleneck. When two or more are simultaneously true for more than 48 hours, you execute the three-step playbook: **delegate** first, **automate** if it cannot be delegated, **eliminate** if it should not exist at all. The order matters — delegation is usually possible if a scorecard exists.

## ملخص بالعربية

خمس إشارات تخبرك أن المؤسس صار عنق الزجاجة. عند تحقق اثنتين أو أكثر معًا لأكثر من 48 ساعة، يُنفَّذ الكتيّب من ثلاث خطوات: **فوّض** أولًا، **أتمت** إن لم يمكن التفويض، **ألغِ** إن كان لا يجب أن يوجد أصلًا. الترتيب مهم — التفويض ممكن غالبًا إن كانت بطاقة الدور موجودة.

---

## الإشارات الخمس / The five signals

| # | Signal | Source | Threshold |
|---|---|---|---|
| S1 | عمق طابور الموافقات / Approval queue depth | `docs/governance/APPROVAL_MATRIX.md` + Deal Desk requests | > 3 items waiting > 24h |
| S2 | تأخّر ردّ المؤسس / Founder reply lag | inbox + customer chat | p50 > 6 working hours, or any single > 24h |
| S3 | فجوات في سجل القرار / Decision-log gap | `docs/founder/STRATEGIC_ASSUMPTIONS_REGISTER.md` + decision log | gap > 5 days without entry |
| S4 | إعادة عمل من المؤسس / Founder rework | `docs/founder/FOUNDER_TIME_AUDIT.md` rework column | > 20% of weekly DG hours are rework |
| S5 | اجتماعات قُدّمت بدون المؤسس وعلِقت / Meetings stalled awaiting founder | calendar + delivery coordinator notes | ≥ 2 stalled meetings in 7 days |

> Any two simultaneously true for > 48 hours triggers the playbook. / أي اثنتين متحققتين معًا لأكثر من 48 ساعة = تفعيل اللعبة.

---

## اللعبة من ثلاث خطوات / The three-step playbook

### Step 1 — Delegate / فوّض

اسأل بالترتيب:

1. هل يوجد scorecard لدور يستطيع تحمّل هذا العمل؟ (`docs/people/ROLE_SCORECARDS.md`)
2. إن لا — هل يوجد متعاقد نشط مؤهل؟
3. إن لا — هل يمكن كتابة scope مصغّر اليوم وفق `docs/people/CONTRACTOR_PLAYBOOK.md`؟

التفويض يتم في ثلاث حركات: scope مكتوب، إحاطة 30 دقيقة، أول تسليم خلال 7 أيام. لا «فوّضت» شفهيًا.

> Delegation is not "I told them once". It is: written scope, 30-min brief, first deliverable in 7 days.

### Step 2 — Automate / أتمت

إن كان العمل قابلًا للأتمتة بأمان (يحترم `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`):

1. هل يدخل العمل ضمن "L1 — assisted" أو أعلى وفق `docs/governance/AI_ACTION_LEVELS.md`؟ إن لا، لا أتمتة.
2. اكتب نمطًا قابلًا لإعادة الاستخدام في `docs/06_llm_gateway/PROMPT_REGISTRY.md`.
3. أضف فحوصات في `docs/06_llm_gateway/SCHEMA_VALIDATION.md` و `docs/10_tests/AGENT_TESTS.md`.
4. مرّر التغيير عبر `docs/ai_governance/AI_CHANGE_CONTROL.md`.

ليست كل المهام تستحق الأتمتة. الكثير منها يكلّف أكثر من تفويضها.

### Step 3 — Eliminate / ألغِ

اسأل: لو لم نفعل هذا أبدًا، ماذا يحدث؟

| Possible answer | Action |
|---|---|
| لا شيء قابل للقياس / Nothing measurable | ألغِ المهمة. |
| فقدان قيمة صغيرة / Small value loss | ألغِ، أو خفّض التكرار بشدة. |
| فقدان قيمة كبيرة / Material value loss | ارجع إلى الخطوة 1 أو 2. لا تلغِ. |
| كسر للحوكمة / Governance break | لا تلغِ. هذا عمل لازم. |

الإلغاء قرار مكتوب، يُسجَّل في `docs/memory/delivery_lessons.md` أو ما يناسب من سجلات الذاكرة.

---

## بطاقة قرار العنق / Bottleneck decision card

```yaml
bottleneck_id: BR-YYYYMMDD-NN
signals_triggered: [S1, S2, ...]
duration_hours: <number>
work_in_question: <one line>
analysis:
  delegable: yes | no | not-yet
  delegable_to_role: <role>
  scorecard_exists: yes | no
  automatable: yes | no | risky
  eliminable: yes | no
decision: delegate | automate | eliminate
decision_rationale: |
  <one paragraph>
owner_of_new_state: <role>
expected_first_delivery: <date>
post_action_check_date: <date, 14 days later>
status: open | in-flight | closed
```

---

## أنماط شائعة وحلولها / Common patterns and their resolutions

| Pattern | What's happening | Default move |
|---|---|---|
| Founder approves every social post | Trust review centralized in founder | Delegate to Trust/QA Reviewer with a written checklist. |
| Founder writes every proposal | Proposal templating is incomplete | Build templates + delegate filling to Sales Asset Designer. |
| Founder schedules every demo | Calendar coordination eating attention | Delegate to RevOps Assistant; founder owns the conversation, not the logistics. |
| Founder reviews every CRM update | Data hygiene unclear to team | Write data-handling rule; delegate to RevOps Assistant. |
| Founder is in every customer call | No second voice on the team | Bring Delivery Coordinator into pilot calls in observer mode for 30 days. |

---

## القواعد التي لا تُكسر / Hard rules

- لا تفوّض عملًا تحت `docs/team/founder_sop.md#must-never-delegate-without-a-written-rule`.
- لا تأتمت عملًا يتطلب موافقة بشري وفق `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`.
- لا تلغِ عملًا لمجرد أنه مزعج. ألغ فقط ما لا قيمة له.
- لا تفوّض عملًا بدون scorecard مكتوب. إن لم يوجد، اكتبه أولًا.
- لا تجعل «الفريق صغير» سببًا لعدم التفويض. حتى متعاقد واحد كافٍ لإزالة 5 ساعات أسبوعيًا.

> Do not delegate work that `docs/team/founder_sop.md` lists as undelegable. Do not automate human-in-the-loop work. Do not eliminate work just because it is annoying. Do not delegate without a scorecard. Do not let "the team is small" be the excuse — even one contractor frees 5 hours/week.

---

## ربط مع الأنظمة الأخرى / Ties

- إشارات يومية: `docs/ops/FOUNDER_DAILY_ANCHOR_AR.md`.
- ميزانية الانتباه: `docs/founder/CEO_ATTENTION_BUDGET.md`.
- تدقيق الوقت: `docs/founder/FOUNDER_TIME_AUDIT.md`.
- بطاقات الأدوار: `docs/people/ROLE_SCORECARDS.md`.
- كتيب المتعاقدين: `docs/people/CONTRACTOR_PLAYBOOK.md`.
- ضبط التغيير AI: `docs/ai_governance/AI_CHANGE_CONTROL.md`.

---

## Disclosure / إفصاح

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.

## Related canonical docs

- `docs/team/founder_sop.md`
- `docs/founder/FOUNDER_LEVERAGE_DASHBOARD.md`
- `docs/founder/FOUNDER_TIME_AUDIT.md`
- `docs/founder/CEO_ATTENTION_BUDGET.md`
- `docs/people/ROLE_SCORECARDS.md`
- `docs/people/CONTRACTOR_PLAYBOOK.md`
- `docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md`
- `docs/governance/APPROVAL_MATRIX.md`
- `docs/ai_governance/AI_CHANGE_CONTROL.md`
