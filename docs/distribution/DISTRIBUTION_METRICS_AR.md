# Distribution Metrics — مؤشرات التوزيع — Distribution Metrics

> Purpose — الغرض: يحدّد هذا المستند قوائم المؤشرات اليومية والأسبوعية لنظام تنفيذ الإيراد. المؤشرات تقيس **النشاط المُحوكَم** (مسودات مُولَّدة، مُعتمَدة، مُتابَعة)، لا تَعِد بنتائج مبيعات. الإيراد يُحتسَب فقط عند الدفع المُؤكَّد يدويًا.
>
> This document defines the daily and weekly metric lists for the Revenue Execution OS. Metrics measure governed activity (drafts generated, approved, followed up), not promised sales outcomes. Revenue counts only at manually-confirmed payment.

Cross-link — روابط: [WIN_LOSS_LEARNING_AR.md](./WIN_LOSS_LEARNING_AR.md) · [PAYMENT_HANDOFF_AR.md](./PAYMENT_HANDOFF_AR.md) · [DRAFT_QUALITY_POLICY_AR.md](./DRAFT_QUALITY_POLICY_AR.md) · [../08_value_os/VALUE_DASHBOARD.md](../08_value_os/VALUE_DASHBOARD.md) · [../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md](../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md).

---

## 1. الأداة — The tool

`make revx-verify` للتحقق من سلامة الطبقة، و`scripts/revenue_execution_metrics.py` يحسب المؤشرات ويكتبها إلى `reports/distribution/DISTRIBUTION_METRICS.md`. المؤشرات تُقرأ من مخازن `data/revenue_execution/*.jsonl`.

`scripts/revenue_execution_metrics.py` computes metrics and writes them to `reports/distribution/DISTRIBUTION_METRICS.md`, reading from the `data/revenue_execution/*.jsonl` stores. `make revx-verify` checks layer integrity.

---

## 2. المؤشرات اليومية — Daily metrics

تُقرأ ضمن الحلقة اليومية للمؤسس (راجع [DRAFT_APPROVAL_RUNBOOK_AR.md](./DRAFT_APPROVAL_RUNBOOK_AR.md)).

Read within the founder's daily loop.

| المؤشر — Metric | يقيس — Measures |
|---|---|
| `drafts_generated_today` | مسودات وُلِّدت اليوم |
| `drafts_pending_approval` | بانتظار قرار المؤسس |
| `drafts_approved_today` | اعتُمِدت اليوم |
| `drafts_rejected_today` | رُفِضت اليوم |
| `drafts_needs_edit_today` | تحتاج تعديلًا |
| `drafts_copied_manually_today` | نُسِخت وأُرسِلت يدويًا |
| `followups_due_today` | متابعات مستحقّة اليوم |
| `blocked_drafts_today` | مسودات حجبتها الحوكمة |
| `avg_draft_quality_score` | متوسّط درجة الجودة للدفعة |
| `proposals_pending_approval` | عروض بانتظار الموافقة |
| `payment_handoffs_pending` | تسليمات دفع بانتظار الموافقة |

> ملاحظة — Note: `drafts_copied_manually_today` هو مؤشر الإرسال الحقيقي — لأن النظام لا يرسل، الإرسال يساوي ما نسخه المؤسس يدويًا.

---

## 3. المؤشرات الأسبوعية — Weekly metrics

تُقرأ مع أسئلة التعلّم الأسبوعية (راجع [WIN_LOSS_LEARNING_AR.md](./WIN_LOSS_LEARNING_AR.md)).

Read with the weekly learning questions.

| المؤشر — Metric | يقيس — Measures |
|---|---|
| `approval_rate` | نسبة المعتمَد إلى المُولَّد |
| `block_rate` | نسبة المحجوب (مؤشر سلامة، الأعلى ليس دائمًا أسوأ) |
| `reply_rate` | نسبة الردود إلى ما نُسِخ يدويًا |
| `discovery_invites_sent` | دعوات استكشاف نُسِخت يدويًا |
| `proposals_sent` | عروض أُرسِلت يدويًا |
| `proposal_to_paid_rate` | نسبة العروض التي بلغت `paid` |
| `wins` / `losses` | عدد الكسب والخسارة |
| `top_loss_reason_code` | أكثر سبب خسارة تكرارًا |
| `sector_win_distribution` | توزيع الكسب على القطاعات |
| `capital_assets_deposited` | أصول رأسمالية أُودِعت (البند 11) |
| `proof_packs_completed` | حزم إثبات اكتملت (البند 10) |
| `revenue_confirmed_sar` | إيراد مُؤكَّد فقط (حالة `paid`) |

---

## 4. قواعد المؤشرات — Metric rules

- **الإيراد = `paid` فقط.** الحالات `sent`/`approved` ليست إيرادًا (راجع [PAYMENT_HANDOFF_AR.md](./PAYMENT_HANDOFF_AR.md)).
- **القيمة تُصنَّف** Estimated/Observed/Verified؛ لا يُجمَع التقديري مع المتحقَّق في رقم واحد (راجع [../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md](../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md)).
- **`block_rate` مؤشر سلامة لا فشل.** ارتفاعه قد يعني أن الحوكمة تعمل، أو أن مصدر الجهات يحتاج مراجعة.
- **لا مؤشر يَعِد بنتيجة.** نقيس النشاط المُحوكَم، لا «مبيعات مضمونة» (البند 5).

Revenue equals `paid` only; value is classified, never blending estimated with verified; `block_rate` is a safety signal, not a failure; no metric promises an outcome.

---

## 5. تفسير سليم — Reading the numbers honestly

- `approval_rate` منخفضة جدًا → القوالب تحتاج تحسينًا، أو القطاع غير مناسب.
- `block_rate` مرتفعة → راجع مصدر الجهات أو لغة القوالب (قد تحوي ادعاءات/قنوات ممنوعة).
- `reply_rate` منخفضة مع `proposal_to_paid_rate` عالية → المشكلة في القمة (التواصل)، لا في الإغلاق.
- كل تفسير يُربَط بإجراء في أسئلة التعلّم الأسبوعية.

Every interpretation links to an action in the weekly learning questions.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
