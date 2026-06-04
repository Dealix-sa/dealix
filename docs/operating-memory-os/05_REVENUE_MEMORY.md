# ذاكرة الإيراد | Revenue Memory

> **AR:** ذاكرة الإيراد تحفظ حركة الأنبوب والصفقات بصيغة منظمة: مرحلة الصفقة، قيمتها، احتماليتها، وحالة التحقق منها. الهدف صورة صادقة عن خط الإيراد بلا تضخيم ولا جذب وهمي، تبقى أداة تخطيط داخلية لا تُطلِق أي فعل خارجي.
>
> **EN:** Revenue Memory preserves pipeline and deal movement in a structured form: deal stage, amount, probability, and verification status. The goal is an honest picture of the revenue line — no inflation, no fake traction — and it stays an internal planning tool that triggers no external action.

## بنية السجل | Record Structure

| الحقل Field | الوصف Description |
|---|---|
| `id` | معرّف السجل / record id |
| `deal_stage` | opportunity \| proposal \| verbal \| closed-won \| closed-lost |
| `amount` | القيمة / amount |
| `currency` | العملة (SAR افتراضيًا) / currency |
| `probability` | احتمالية الإغلاق / close probability |
| `verified` | هل القيمة مؤكَّدة (bool) / is the value verified |
| `verification_ref` | مرجع التحقق / verification reference |
| `status` | draft \| approved \| archived |

## مراحل الأنبوب | Pipeline Stages

| المرحلة Stage | المعنى Meaning |
|---|---|
| `opportunity` | فرصة محتملة محدَّدة / identified opportunity |
| `proposal` | عرض قيد المراجعة من العميل / proposal under client review |
| `verbal` | موافقة مبدئية شفهية / verbal commitment |
| `closed-won` | إيراد مؤكَّد / confirmed revenue |
| `closed-lost` | فرصة خُسرت تُحفَظ للتعلّم / lost, kept for learning |

## كيف يُسجَّل حدث الإيراد | How a Revenue Event Is Recorded

1. **Draft** — يولّد الذكاء مسودة سجل من حدث حقيقي. / AI drafts from a real event.
2. **Validate** — تشغيل `operating_memory_validate.py`. / Validate structure.
3. **Approve** — يراجع المؤسس ويعتمد. / Founder approves.
4. **Aggregate** — يُجمَّع لتقدير الأنبوب المرجّح. / Aggregated into weighted pipeline.

## التقارير | Reporting

- الأنبوب المرجّح بالاحتمالية. / Probability-weighted pipeline.
- الإيراد المؤكَّد (`verified`) مقابل المتوقَّع. / Verified vs expected revenue.
- معدّل التحوّل بين المراحل. / Stage-to-stage conversion.

## حدود الأمان | Safety Boundaries

- لا جذب وهمي ولا أرقام مُختلقة. / No fake traction, no fabricated numbers.
- لا عائد مضمون؛ الاحتمالية تعكس الواقع. / No guaranteed ROI; probability reflects reality.
- AI prepares, Founder approves, Manual action only, No external sending.
- تخطيط داخلي فقط بلا أي حركة خارجية. / Internal planning only, no external action.
