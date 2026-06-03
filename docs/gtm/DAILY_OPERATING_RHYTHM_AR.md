# Daily Operating Rhythm — الإيقاع اليومي وحلقة التعلّم — Market Production OS

إيقاع يومي ثابت يحوّل طبقة السوق من "حماس" إلى "آلة". كل خطوة مسودة/تصنيف/تقرير —
لا إرسال إلا في النافذة المعتمدة بعد موافقة المؤسس.

A fixed daily rhythm that turns the market layer from enthusiasm into a machine.
Every step is draft / classify / report — sending happens only in the approved
window after founder approval.

---

## الإيقاع اليومي — The daily rhythm

| الوقت / Time | الخطوة / Step | المخرج / Output | الأداة / Tool |
| --- | --- | --- | --- |
| 07:30 | إشارات / Signals | prospects + إشارات وظائف عامة + محفّزات قطاعية | `radar_events/`, `gtm_os/records.py` |
| 08:30 | مسودات / Drafts | توليد 250 مسودة (`DAILY_DRAFT_MIX`) | `gtm_os/outreach_draft.py` |
| 09:00 | بوابات / Gates | brand + personalization + compliance + deliverability | `gtm_os/draft_quality_gate.py` |
| 10:00 | موافقة / Approval | اعتماد 30–50 مسودة | `approval_center/` |
| 11:00 | إرسال / Sending | دفعة معتمدة محدودة (ضمن التدرّج) | `gtm_os/sending_ramp.py` |
| 13:00 | ردود / Replies | تصنيف + إجراء تالٍ | `email/reply_classifier.py`, `gtm_os/records.route_reply` |
| 15:00 | قنوات أخرى / Other | شركاء + برس + إشارات وظائف | `partnership_os/`, `docs/BRAND_PRESS_KIT.md` |
| 18:00 | محتوى / Content | LinkedIn/proof/founder insights (مسودات) | `marketing_factory/`, `gtm_os/content_calendar.py` |
| 21:00 | تقرير / Report | أمر اليوم التجاري الواحد | `scripts/gtm_daily_command.py` |

**توزيع الـ250 مسودة (drafts, not sends):** 100 first_touch · 75 follow_up_1 ·
50 follow_up_2 · 15 proposal_intro · 10 close_loop.

**أمر اليوم (21:00):** `python3 scripts/gtm_daily_command.py` → `reports/gtm/GTM_DAILY_COMMAND.md`
يعرض: حالة الإنتاج، أعلى قائمة موافقة، خطة دفعة الإرسال (بعد الموافقة)، التنبيهات،
وتوصية الغد.

---

## حلقة التعلّم الأسبوعية — Weekly learning loop

كل أسبوع (الأحد بوابات):
- أوقف أسوأ 20% من الرسائل؛ ضاعِف أفضل 20%.
- حدّث: sector playbooks، objection bank، product catalog، pricing guardrails، proof library.
- اختر 3 أهداف برس و10 شركاء.

Each week: stop the worst 20% of messages, double the best 20%, refresh the
sector playbooks / objection bank / catalog / pricing guardrails / proof library,
and pick 3 press targets + 10 partners.

القاعدة المالية / Finance rule: إذا قناة تعطي ردودًا بلا اجتماعات لا تنخدع؛ وإذا قليلة
الحجم عالية التحويل ضاعِفها. راجع `auto_client_acquisition/operating_finance_os/`
و[`docs/FINANCE_DASHBOARD.md`](../FINANCE_DASHBOARD.md).

---

> لا إرسال خارجي إلا بموافقة المؤسس. No external send without founder approval.
>
> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
