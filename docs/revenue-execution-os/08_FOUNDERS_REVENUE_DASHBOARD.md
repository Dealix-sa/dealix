# Founder's Revenue Dashboard — لوحة إيرادات المؤسس

## الغرض (AR)
يصف هذا المستند المقاييس التي يُنتجها `scripts/founder_revenue_dashboard.py`. اللوحة تعطي المؤسس صورة يومية واحدة عن حالة الدخل، مصدرها سجل الأحداث اليدوية فقط. اللوحة **تقرأ وتلخّص فقط** ولا ترسل أي شيء خارجيًا.

## Purpose (EN)
This document describes the metrics produced by `scripts/founder_revenue_dashboard.py`. The dashboard gives the founder a single daily picture of revenue health, sourced only from the manual events ledger. The dashboard **only reads and summarizes** — it never sends anything externally.

## المقاييس / Metrics

| المقياس / Metric | الوصف / Description |
|---|---|
| drafts_generated_today | عدد المسودات المُولّدة اليوم / Drafts generated today |
| founder_actions_today | عدد إجراءات المؤسس اليوم / Founder actions today |
| approved_manual_actions | الإجراءات اليدوية المعتمدة / Approved manual actions |
| manual_sends_recorded | الإرسالات اليدوية المسجّلة / Manual sends recorded |
| positive_replies_recorded | الردود الإيجابية المسجّلة / Positive replies recorded |
| discovery_calls_booked | مكالمات الاكتشاف المحجوزة / Discovery calls booked |
| diagnostics_sold | التشخيصات المباعة / Diagnostics sold |
| pilots_proposed | التجارب المعروضة / Pilots proposed |
| pilots_sold | التجارب المباعة / Pilots sold |
| retainers_started | العقود الشهرية المبدوءة / Retainers started |
| pipeline_value_sar | قيمة خط الأنابيب المتوقعة بالريال / Weighted pipeline value (SAR) |
| realized_revenue_sar | الإيراد المحقق بالريال / Realized revenue (SAR) |
| top_vertical | القطاع الأعلى أداءً / Top-performing vertical |
| top_channel | القناة الأعلى أداءً / Top-performing channel |
| top_objection | الاعتراض الأكثر تكرارًا / Most frequent objection |
| stuck_stage | المرحلة الأكثر تعثرًا / Most stalled stage |
| next_best_action | الإجراء التالي الأفضل المقترح / Suggested next best action |

## كيف تُقرأ اللوحة / How to Read It
- **مقاييس النشاط** (drafts, founder_actions, manual_sends): هل الزخم اليومي كافٍ؟
- **مقاييس التحويل** (positive_replies → diagnostics_sold → pilots_sold → retainers_started): أين تتسرب الصفقات؟
- **مقاييس القيمة** (pipeline_value_sar, realized_revenue_sar): المتوقع مقابل المحقق.
- **مقاييس التوجيه** (top_vertical, top_channel, top_objection, stuck_stage, next_best_action): أين نركّز غدًا.

## السلامة / Safety
- اللوحة تلخّص بيانات مسجّلة يدويًا فقط؛ لا كشط ولا إرسال.
- `next_best_action` اقتراح للمؤسس فقط، لا يُنفَّذ تلقائيًا.

The dashboard summarizes manually recorded data only; no scraping, no sending. `next_best_action` is a suggestion to the founder, never auto-executed.
