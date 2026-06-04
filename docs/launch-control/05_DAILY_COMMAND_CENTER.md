# Daily Command Center — مركز القيادة اليومي

> The fixed daily rhythm. Automatable steps name the exact command. Every outreach step is manual and follows founder approval. No step in this routine sends an external message automatically.
>
> الإيقاع اليومي الثابت. الخطوات القابلة للأتمتة تذكر الأمر الدقيق. كل خطوة تواصل يدوية وتتبع موافقة المؤسس. لا خطوة في هذا الروتين ترسل رسالة خارجية تلقائيًا.

---

## EN — Daily timetable

| Time | Step | Type | Command / action |
|---|---|---|---|
| 08:00 | Generate today's drafts | Automated | `python scripts/commercial_generate_400_drafts.py` |
| 08:15 | Safety check | Automated | `python scripts/commercial_safety_audit.py` (must be zero violations) |
| 08:30 | Review top 50 | Manual | Read `outputs/commercial_launch/latest/top_50_priority.md`; approve/reject each |
| 10:00 | Manual outreach | Manual | Founder personally sends approved drafts, one at a time |
| 13:00 | Discovery & follow-ups | Manual | Run discovery calls; follow up on replies |
| 16:00 | Content & social | Manual | Post approved content from `outputs/media_social/` by hand |
| 18:00 | CRM update | Manual | Update stages, reply classification, disqualifications in CRM |
| 20:00 | Daily metrics & next actions | Automated + Manual | Review `outputs/commercial_launch/latest/daily_metrics.json`; write tomorrow's top 3 |

### Daily gate
Do not start the 10:00 manual outreach until the 08:15 safety audit reports **zero** violations and the drafts you are sending are marked approved by you. No draft is auto-sent at any point.

### Optional full verification (start of day)
`python scripts/final_launch_control_verify.py` — runs the master check and writes to `outputs/final_launch_control/`.

---

## AR — الجدول اليومي

| الوقت | الخطوة | النوع | الأمر / الإجراء |
|---|---|---|---|
| 08:00 | توليد مسودات اليوم | آلي | `python scripts/commercial_generate_400_drafts.py` |
| 08:15 | فحص الأمان | آلي | `python scripts/commercial_safety_audit.py` (يجب صفر مخالفات) |
| 08:30 | مراجعة أعلى 50 | يدوي | اقرأ `outputs/commercial_launch/latest/top_50_priority.md`؛ اعتمد/ارفض كلًا |
| 10:00 | التواصل اليدوي | يدوي | يرسل المؤسس المسودات المعتمدة شخصيًا، واحدة تلو الأخرى |
| 13:00 | الاستكشاف والمتابعات | يدوي | إجراء مكالمات الاستكشاف؛ متابعة الردود |
| 16:00 | المحتوى والتواصل الاجتماعي | يدوي | نشر المحتوى المعتمد من `outputs/media_social/` يدويًا |
| 18:00 | تحديث CRM | يدوي | تحديث المراحل، تصنيف الردود، الاستبعادات في CRM |
| 20:00 | المقاييس اليومية والإجراءات التالية | آلي + يدوي | مراجعة `outputs/commercial_launch/latest/daily_metrics.json`؛ كتابة أعلى 3 للغد |

### البوابة اليومية
لا تبدأ تواصل الساعة 10:00 اليدوي حتى يُبلّغ تدقيق أمان الساعة 08:15 عن **صفر** مخالفات وتكون المسودات التي ترسلها معتمدة منك. لا تُرسَل أي مسودة تلقائيًا في أي وقت.

### تحقق كامل اختياري (بداية اليوم)
`python scripts/final_launch_control_verify.py` — يشغّل الفحص الرئيسي ويكتب إلى `outputs/final_launch_control/`.

---

Related: [Evidence Pack](03_EVIDENCE_PACK.md) · [Founder Execution Checklist](07_FOUNDER_EXECUTION_CHECKLIST.md) · [Failure Response Playbook](06_FAILURE_RESPONSE_PLAYBOOK.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
