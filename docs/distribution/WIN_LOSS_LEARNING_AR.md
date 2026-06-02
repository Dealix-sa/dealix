# Win/Loss Learning — تعلّم الكسب والخسارة — Win/Loss Learning

> Purpose — الغرض: يحدّد هذا المستند ما يُسجَّل لكل نتيجة (كسب/خسارة)، وأسئلة التعلّم الأسبوعية التي تُحوِّل النتائج إلى تحسين للقوالب والقطاعات والعروض. التعلّم مبني على أدلة مسجّلة، لا على انطباعات.
>
> This document defines what to record per outcome (win/loss) and the weekly learning questions that turn outcomes into improvements to templates, sectors, and offers. Learning is built on recorded evidence, not impressions.

Cross-link — روابط: [SECTOR_PRIORITIZATION_AR.md](./SECTOR_PRIORITIZATION_AR.md) · [DRAFT_QUALITY_POLICY_AR.md](./DRAFT_QUALITY_POLICY_AR.md) · [PROPOSAL_FACTORY_AR.md](./PROPOSAL_FACTORY_AR.md) · [DISTRIBUTION_METRICS_AR.md](./DISTRIBUTION_METRICS_AR.md) · [../09_capital_os/CAPITAL_OS.md](../09_capital_os/CAPITAL_OS.md).

---

## 1. أين يُسجَّل — Where it is recorded

تُسجَّل النتائج في `data/revenue_execution/win_loss.jsonl` (قابل للتجاوز عبر `DEALIX_REVX_WIN_LOSS_PATH`)، وتُلخَّص في `reports/distribution/WIN_LOSS_LEARNING.md` ضمن الدورة اليومية. لا بيانات شخصية في السجل؛ يُشار للعميل بمعرّف مجهول (البند 6).

Outcomes are recorded in `data/revenue_execution/win_loss.jsonl`, summarized in `reports/distribution/WIN_LOSS_LEARNING.md`. No PII in the record; the customer is referenced by an anonymized id.

---

## 2. ما يُسجَّل لكل نتيجة — What to record per outcome

| الحقل — Field | الوصف — Description |
|---|---|
| `outcome` | `won` أو `lost` |
| `sector` | القطاع (لتحديث الترتيب) |
| `rung` | درجة العرض على السلّم الخماسي |
| `stage_reached` | أبعد مرحلة بلغها في خط الأنابيب |
| `first_draft_type` | نوع أول مسودة فتحت العلاقة |
| `draft_quality_score` | درجة جودة المسودة الفاتحة |
| `time_to_outcome_days` | الأيام من التواصل الأول للنتيجة |
| `reason_code` | سبب مُصنَّف (انظر §3) |
| `value_evidence_level` | L0–L5 للقيمة المُثبتة (للكسب) |
| `notes` | ملاحظة موجزة بلا بيانات شخصية |

تُغذّي هذه الحقول تحديث ترتيب القطاعات (راجع [SECTOR_PRIORITIZATION_AR.md](./SECTOR_PRIORITIZATION_AR.md)) وتحسين القوالب.

These fields feed sector re-ranking and template improvement.

---

## 3. رموز الأسباب — Reason codes

| الرمز — Code | المعنى — Meaning |
|---|---|
| `price` | السعر/الميزانية |
| `timing` | التوقيت غير مناسب |
| `scope_fit` | النطاق لا يطابق الحاجة |
| `decision_maker` | لم نصل لصاحب القرار |
| `trust` | حاجز ثقة/إثبات |
| `competitor` | اختار بديلًا |
| `no_response` | لا ردّ حتى رسالة الإنهاء |
| `data_readiness` | مشكلة جاهزية بيانات (يحوّل لـ Data Pack) |
| `proven_value` | كسب بفضل قيمة مُثبتة (للكسب) |

> رمز `data_readiness` غالبًا ليس خسارة بل إعادة توجيه — A `data_readiness` code is often not a loss but a redirect إلى Rung 2 (Data-to-Revenue Pack).

---

## 4. أسئلة التعلّم الأسبوعية — Weekly learning questions

مرّة أسبوعيًا، يقرأ المؤسس التقرير ويجيب:

Once a week, the founder reads the report and answers:

1. أي قطاع أعطى أعلى نسبة كسب هذا الأسبوع؟ هل نرفع ترتيبه؟
2. أي نوع مسودة فاتحة ارتبط بأكثر الردود؟ هل نعمّمه؟
3. ما أكثر `reason_code` تكرارًا في الخسارة؟ ما الإجراء المضاد؟
4. هل درجة جودة المسودة ترتبط فعلًا بالكسب؟ هل نضبط البوابة؟
5. أي درجة على السلّم الخماسي تُغلَق أسرع؟ هل نبدأ منها؟
6. ما الأصل الرأسمالي الذي أنتجه كسب هذا الأسبوع (البند 11)؟
7. هل ظهر أي طلب يخالف القواعد الـ11؟ كيف رُفِض وسُجِّل؟

السؤال 7 إلزامي — Question 7 is mandatory: كل طلب يخالف غير القابل للتفاوض يُسجَّل رفضه (مثل طلب كَشط أو إرسال بارد) كي يصبح إشارة، لا حدثًا منسيًّا.

---

## 5. من التعلّم إلى الإجراء — From learning to action

| الملاحظة — Observation | الإجراء — Action |
|---|---|
| قطاع يكسب باستمرار | ارفع درجته في `data/distribution/sectors.yaml` |
| نوع مسودة يفشل دائمًا | راجع قالبه أو أوقفه |
| سبب خسارة متكرّر = `price` | راجع الدرجة الافتتاحية للقطاع |
| كسب بقيمة L3+ | رشّحه لحالة دراسية عند L4 + إذن |

كل تغيير في القطاعات أو القوالب يُراجَع يدويًا؛ لا تحديث آلي للأوزان دون قرار المؤسس.

Every sector or template change is reviewed manually; no automatic weight update without the founder's decision.

---

## 6. ربط الأصل الرأسمالي — Capital asset link

كل كسب يُفترَض أن يودِع أصلًا رأسماليًا (البند 11): قاعدة ترتيب، قالب رابح، رؤية قطاعية. يُسجَّل في `capital_os` (راجع [../09_capital_os/CAPITAL_OS.md](../09_capital_os/CAPITAL_OS.md)) ويُربَط بسجل الكسب.

Every win is expected to deposit a Capital Asset (non-negotiable #11): a scoring rule, a winning template, a sector insight. It is recorded in `capital_os` and linked to the win record.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
