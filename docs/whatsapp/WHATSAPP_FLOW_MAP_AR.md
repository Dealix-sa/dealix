# WhatsApp Flow Map — خريطة تدفقات واتساب

## التدفقات الاثنا عشر

واتساب مجموعة محكومة من تدفقات الأعمال، وليست محادثة مفتوحة. لكل تدفّق: مُحفِّز، مدخلات مسموحة، شرط خروج، شرط تحويل إلى إنسان، وتدفّق تالٍ. المصدر الوحيد للحقيقة هو `auto_client_acquisition/whatsapp_client_os/flows.py`، والقيم أدناه مأخوذة حرفيًا من `flows_as_data()`. التدفّق التالي الفارغ يعني نهاية المسار.

| المعرّف (id) | العنوان | المُحفِّز (trigger_intent) | المدخلات المسموحة | شرط الخروج | شرط التحويل لإنسان | التدفّق التالي |
|---|---|---|---|---|---|---|
| `new_client_welcome` | ترحيب عميل جديد | `welcome` | `menu_number`, `free_text` | `menu_choice_made` | `explicit_human_request` | `readiness_scan` |
| `readiness_scan` | فحص الجاهزية | `start_scan` | `option_choice` | `all_axes_answered` | `sensitive_data_or_low_confidence` | `service_recommendation` |
| `service_recommendation` | توصية الخدمة | `recommend_me` | `option_choice` | `recommendation_shown` | `pricing_commitment` | `proposal_review` |
| `permission_collection` | جمع الصلاحيات | `give_permission` | `option_choice` | `portal_link_issued` | `secret_in_text` | `onboarding` |
| `draft_review` | مراجعة المسودات | `review_draft` | `approve`, `edit`, `reject` | `draft_approved_or_rejected` | `dissatisfied` | (نهاية) |
| `proposal_review` | مراجعة العرض | `review_proposal` | `option_choice` | `proposal_decision_made` | `pricing_commitment` | `payment_handoff` |
| `proof_pack_delivery` | تسليم حزمة الإثبات | `proof_pack` | `option_choice` | `proof_pack_opened` | `dissatisfied` | `renewal_upsell` |
| `payment_handoff` | تحويل الدفع | `start_payment` | `option_choice` | `secure_link_issued` | `billing_question` | `onboarding` |
| `onboarding` | بدء التشغيل | `give_permission` | `option_choice` | `onboarding_checklist_started` | `low_confidence` | `weekly_report` |
| `weekly_report` | التقرير الأسبوعي | `unknown` | `option_choice` | `report_delivered` | `dissatisfied` | `renewal_upsell` |
| `support_handoff` | الدعم والتصعيد | `request_support` | `option_choice`, `free_text` | `ticket_categorized` | `billing_or_urgent_complaint` | (نهاية) |
| `renewal_upsell` | التجديد والترقية | `renewal` | `option_choice` | `renewal_decision_made` | `pricing_commitment` | (نهاية) |

### ملاحظات على التوجيه

- يربط `flow_for_intent` كل نية بتدفّقها؛ النوايا غير المعروفة تعود إلى `new_client_welcome`.
- يعطي `next_flow` التدفّق التالي للتدفّق المكتمل (أو سلسلة فارغة للنهاية).
- المسار النموذجي: ترحيب ← فحص ← توصية ← مراجعة عرض ← تحويل دفع ← بدء تشغيل ← تقرير أسبوعي ← تجديد.
- يمكن دخول `permission_collection` من أي نقطة عند ذكر تكامل، ويخرج دائمًا برابط البوابة الآمنة (`portal_link_issued`) — لا يُجمَع سرّ في النص.
- `draft_review` و`support_handoff` و`renewal_upsell` تدفقات طرفية (نهاية المسار).

روابط: [نظرة عامة على النظام](./WHATSAPP_CLIENT_OS_AR.md) · [تجربة العميل](./WHATSAPP_CLIENT_EXPERIENCE_AR.md) · [بطاقات الإجراء](./WHATSAPP_APPROVAL_CARDS_AR.md) · [النقطة `GET /api/v1/whatsapp-client/flows`](./README.md).

---

## English

### The twelve flows

WhatsApp is a controlled set of business flows, not open chat. Each flow has a trigger, allowed inputs, an exit condition, a human-handoff condition, and a next flow. The single source of truth is `auto_client_acquisition/whatsapp_client_os/flows.py`; the values below are taken verbatim from `flows_as_data()`. An empty next flow is terminal.

| id | Title | trigger_intent | Allowed inputs | Exit condition | Handoff condition | Next flow |
|---|---|---|---|---|---|---|
| `new_client_welcome` | New Client Welcome | `welcome` | `menu_number`, `free_text` | `menu_choice_made` | `explicit_human_request` | `readiness_scan` |
| `readiness_scan` | Readiness Scan | `start_scan` | `option_choice` | `all_axes_answered` | `sensitive_data_or_low_confidence` | `service_recommendation` |
| `service_recommendation` | Service Recommendation | `recommend_me` | `option_choice` | `recommendation_shown` | `pricing_commitment` | `proposal_review` |
| `permission_collection` | Permission Collection | `give_permission` | `option_choice` | `portal_link_issued` | `secret_in_text` | `onboarding` |
| `draft_review` | Draft Review | `review_draft` | `approve`, `edit`, `reject` | `draft_approved_or_rejected` | `dissatisfied` | (terminal) |
| `proposal_review` | Proposal Review | `review_proposal` | `option_choice` | `proposal_decision_made` | `pricing_commitment` | `payment_handoff` |
| `proof_pack_delivery` | Proof Pack Delivery | `proof_pack` | `option_choice` | `proof_pack_opened` | `dissatisfied` | `renewal_upsell` |
| `payment_handoff` | Payment Handoff | `start_payment` | `option_choice` | `secure_link_issued` | `billing_question` | `onboarding` |
| `onboarding` | Onboarding | `give_permission` | `option_choice` | `onboarding_checklist_started` | `low_confidence` | `weekly_report` |
| `weekly_report` | Weekly Report | `unknown` | `option_choice` | `report_delivered` | `dissatisfied` | `renewal_upsell` |
| `support_handoff` | Support / Human Handoff | `request_support` | `option_choice`, `free_text` | `ticket_categorized` | `billing_or_urgent_complaint` | (terminal) |
| `renewal_upsell` | Renewal / Upsell | `renewal` | `option_choice` | `renewal_decision_made` | `pricing_commitment` | (terminal) |

### Routing notes

- `flow_for_intent` maps each intent to its flow; unknown intents fall back to `new_client_welcome`.
- `next_flow` returns the follow-on flow for a completed flow (or an empty string for terminal flows).
- Typical path: welcome → scan → recommendation → proposal review → payment handoff → onboarding → weekly report → renewal.
- `permission_collection` can be entered from any point when an integration is mentioned and always exits with a Secure Portal link (`portal_link_issued`) — no secret is collected in text.
- `draft_review`, `support_handoff`, and `renewal_upsell` are terminal flows.

Links: [System overview](./WHATSAPP_CLIENT_OS_AR.md) · [Client experience](./WHATSAPP_CLIENT_EXPERIENCE_AR.md) · [Action cards](./WHATSAPP_APPROVAL_CARDS_AR.md) · endpoint `GET /api/v1/whatsapp-client/flows` (see [README](./README.md)).

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
