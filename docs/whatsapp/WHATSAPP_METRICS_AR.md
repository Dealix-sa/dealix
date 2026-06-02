# WhatsApp Metrics — مقاييس واتساب

## المقاييس

التجميع حتمي فوق مخازن JSONL عبر `metrics.compute_metrics`. **يُحتسَب فقط ما هو مُسجَّل فعلًا — لا أرقام قمع مُختلَقة.** المتاح عبر `GET /api/v1/whatsapp-client/metrics` (قراءة فقط)، ويغذّي سطح المؤسس ومولّد التقارير.

| المقياس | المصدر | المعنى |
|---|---|---|
| `new_sessions` | عدد الجلسات | عدد الجلسات المُسجَّلة |
| `inbound_messages` | الرسائل الواردة | عدد الرسائل الواردة |
| `completed_scans` | عدد التقييمات | عدد الفحوص المكتملة (`ClientAssessment`) |
| `recommendations_generated` | بطاقات `recommendation` | عدد بطاقات التوصية |
| `action_cards` | كل البطاقات | إجمالي البطاقات المُنشأة |
| `proposal_requests` | بطاقات `proposal` | عدد بطاقات العروض |
| `permission_cards` | بطاقات `permission` | عدد بطاقات الصلاحيات |
| `payment_handoffs` | بطاقات `payment_handoff` | عدد تحويلات الدفع |
| `support_tickets` | بطاقات `support_escalation` | عدد تذاكر الدعم |
| `human_handoffs` | جلسات `handoff_open` | عدد الجلسات المُحوَّلة لإنسان |
| `permissions_recorded` | عدد الصلاحيات | عدد سجلات الصلاحيات |
| `by_card_kind` | تكرار البطاقات | توزيع حسب نوع البطاقة |
| `by_intent` | تكرار النوايا الواردة | توزيع حسب النية |

يحمل المخرج كذلك `governance_decision = ALLOW`.

## مقاييس التجربة الجديرة بالمتابعة

مؤشرات تشغيلية يُشتقّ بعضها من الجدول أعلاه؛ تُقرأ كأنماط لا كوعود:

- **اكتمال الفحص:** `completed_scans` نسبةً إلى `new_sessions` — كم جلسة وصلت للقرار.
- **التوصية إلى العرض:** `proposal_requests` نسبةً إلى `recommendations_generated`.
- **سلامة الصلاحيات:** `permission_cards` و`permissions_recorded` — كم تكامل مرّ عبر البوابة الآمنة.
- **معدّل التحويل لإنسان:** `human_handoffs` نسبةً إلى `new_sessions` — مؤشر ثقة لا فشل (الوصول السريع لإنسان مقصود).
- **حِمل الدعم:** `support_tickets` وتوزيع `by_intent`.

> القيم تعكس فقط الأحداث المُسجَّلة. لا تُشتق نسب تحويل أو عائد كحقيقة؛ كل ما هو مشتق تقديري ويوصَف كنمط.

روابط: [تصنيف الدعم](./WHATSAPP_SUPPORT_ESCALATION_AR.md) · [التحويل إلى إنسان](./WHATSAPP_HUMAN_HANDOFF_AR.md) · [بطاقات الإجراء](./WHATSAPP_APPROVAL_CARDS_AR.md) · [النقطة `GET /api/v1/whatsapp-client/metrics`](./README.md).

---

## English

### The metrics

Aggregation is deterministic over JSONL stores via `metrics.compute_metrics`. **Only what is actually recorded is counted — no invented funnel numbers.** Available via `GET /api/v1/whatsapp-client/metrics` (read-only), feeding the founder surface and the reports generator.

| Metric | Source | Meaning |
|---|---|---|
| `new_sessions` | session count | Number of recorded sessions |
| `inbound_messages` | inbound messages | Number of inbound messages |
| `completed_scans` | assessment count | Number of completed scans (`ClientAssessment`) |
| `recommendations_generated` | `recommendation` cards | Number of recommendation cards |
| `action_cards` | all cards | Total cards created |
| `proposal_requests` | `proposal` cards | Number of proposal cards |
| `permission_cards` | `permission` cards | Number of permission cards |
| `payment_handoffs` | `payment_handoff` cards | Number of payment handoffs |
| `support_tickets` | `support_escalation` cards | Number of support tickets |
| `human_handoffs` | `handoff_open` sessions | Number of sessions handed to a human |
| `permissions_recorded` | permission count | Number of permission records |
| `by_card_kind` | card frequency | Distribution by card kind |
| `by_intent` | inbound intent frequency | Distribution by intent |

The output also carries `governance_decision = ALLOW`.

### Experience metrics to watch

Operational signals, some derived from the table above; read them as patterns, not promises:

- **Scan completion** — `completed_scans` relative to `new_sessions`: how many sessions reached a decision.
- **Recommendation to proposal** — `proposal_requests` relative to `recommendations_generated`.
- **Permission hygiene** — `permission_cards` and `permissions_recorded`: how many integrations went through the Secure Portal.
- **Human-handoff rate** — `human_handoffs` relative to `new_sessions`: a trust signal, not a failure (fast access to a human is intended).
- **Support load** — `support_tickets` and the `by_intent` distribution.

> Values reflect only recorded events. No conversion rate or ROI is derived as fact; anything derived is an estimate and described as a pattern.

Links: [Support triage](./WHATSAPP_SUPPORT_ESCALATION_AR.md) · [Human handoff](./WHATSAPP_HUMAN_HANDOFF_AR.md) · [Action cards](./WHATSAPP_APPROVAL_CARDS_AR.md) · endpoint `GET /api/v1/whatsapp-client/metrics` (see [README](./README.md)).

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
