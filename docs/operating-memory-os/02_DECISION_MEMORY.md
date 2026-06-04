# ذاكرة القرار | Decision Memory

> **AR:** ذاكرة القرار هي السجل الذي يوثّق كل قرار تشغيلي مهم في Dealix: ماذا تقرّر، ولماذا، وما البدائل، وما النتيجة. الهدف منع تكرار النقاش نفسه ومنح المؤسس مرجعًا واضحًا قابلًا للاسترجاع.
>
> **EN:** Decision Memory is the record that documents every significant operating decision in Dealix: what was decided, why, the alternatives, and the outcome. The goal is to prevent re-litigating the same debate and give the founder a clear, recallable reference.

## بنية السجل | Record Structure

| الحقل Field | الوصف Description |
|---|---|
| `id` | معرّف القرار / decision id |
| `decision` | القرار بجملة واحدة / one-line decision |
| `context` | السياق والمشكلة / context and problem |
| `alternatives[]` | البدائل المدروسة / alternatives considered |
| `rationale` | الأساس المنطقي / rationale |
| `outcome` | النتيجة (تُحدَّث لاحقًا) / outcome (updated later) |
| `review_date` | موعد المراجعة / review date |
| `status` | draft \| approved \| archived |

## كيف يُسجَّل القرار | How a Decision Is Recorded

1. **Draft** — يولّد الذكاء مسودة قرار من النقاش الجاري. / AI drafts the decision from the discussion.
2. **Validate** — تشغيل `operating_memory_validate.py` للتأكد من البنية. / Validate structure.
3. **Approve** — يراجع المؤسس ويعتمد؛ يُملأ `approved_by`. / Founder approves; `approved_by` set.
4. **Store** — يُضاف إلى دفتر القرارات بطابع زمني. / Append to the decision ledger with a timestamp.

## كيف يُسترجع القرار | How a Decision Is Recalled

- البحث بالقطاع/الموضوع/التاريخ قبل اتخاذ قرار مشابه. / Search by topic/sector/date before a similar decision.
- ربط القرار الجديد بالقرار السابق عبر `id`. / Link new decisions to prior ones via `id`.
- مراجعة `outcome` لتقييم جودة القرارات السابقة. / Review `outcome` to assess prior decision quality.

## مثال | Example

```json
{
  "id": "dec-2026-014",
  "type": "decision",
  "decision": "Prioritize logistics vertical for Q3 outreach drafts",
  "context": "Two verticals scored similarly; limited founder time",
  "alternatives": ["retail", "logistics", "both in parallel"],
  "rationale": "Higher warm-intro density and clearer pain signal",
  "outcome": "pending",
  "review_date": "2026-09-01",
  "status": "draft"
}
```

## حدود الأمان | Safety Boundaries

- القرار قد يوصي بفعل، لكن **لا فعل خارجي ينفَّذ تلقائيًا**. / A decision may recommend an action, but no external action executes automatically.
- AI prepares, Founder approves, Manual action only, No external sending.
- لا ادعاءات نتائج مضمونة في حقل `outcome`. / No guaranteed-result claims in `outcome`.
