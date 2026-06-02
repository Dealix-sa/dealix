# WhatsApp Client OS — Documentation Index — فهرس توثيق نظام عميل واتساب

نظام عميل واتساب (WhatsApp Client OS) هو تجربة تشغيل المبيعات والمتابعة على واتساب لعملاء Dealix من شركات السوق السعودي. ليس روبوت محادثة مفتوحًا، بل مجموعة محكومة من تدفقات الأعمال: يبدأ العميل على واتساب، يجري فحص جاهزية، يستلم توصية خدمة مرتبطة بسجل الخدمات القانوني، يمنح الصلاحيات بأمان (الأسرار عبر البوابة الآمنة فقط)، يراجع المسودات والعروض وحِزم الإثبات، ويُحوَّل إلى إنسان عند الحاجة. كل مخرج يحمل قرار حوكمة (`governance_decision`)، ولا يصدر أي إرسال خارجي مباشر ولا أي خصم مالي من هذه الطبقة.

This documentation set describes the WhatsApp Client OS — the client-facing sales-operations and follow-up experience on WhatsApp for Dealix's Saudi B2B customers. It is a controlled set of business flows (not an open chatbot): a client starts on WhatsApp, runs a readiness scan, receives a catalog-tied service recommendation, grants permissions safely (secrets via the Secure Portal only), reviews drafts, proposals, and proof packs, and is escalated to a human when needed. Every output carries a `governance_decision`; no live external send or charge originates from this layer.

## الوثائق — Documents

| # | File | الموضوع — Topic |
|---|---|---|
| 1 | [WHATSAPP_CLIENT_OS_AR.md](./WHATSAPP_CLIENT_OS_AR.md) | نظرة عامة على الأنظمة الخمسة وخط الأنابيب المحكوم — System overview, 5 systems, controlled pipeline |
| 2 | [WHATSAPP_CONVERSATION_POLICY_AR.md](./WHATSAPP_CONVERSATION_POLICY_AR.md) | قواعد المحادثة — Conversation rules |
| 3 | [WHATSAPP_FLOW_MAP_AR.md](./WHATSAPP_FLOW_MAP_AR.md) | خريطة الـ١٢ تدفّقًا — The 12-flow map |
| 4 | [WHATSAPP_CLIENT_EXPERIENCE_AR.md](./WHATSAPP_CLIENT_EXPERIENCE_AR.md) | تجربة العميل من Lead إلى عميل — Lead-to-client journey |
| 5 | [WHATSAPP_TEMPLATE_LIBRARY_AR.md](./WHATSAPP_TEMPLATE_LIBRARY_AR.md) | مكتبة القوالب ونبرة العلامة — Template library + tone |
| 6 | [WHATSAPP_APPROVAL_CARDS_AR.md](./WHATSAPP_APPROVAL_CARDS_AR.md) | بطاقات الإجراء والاعتماد — Action + approval cards |
| 7 | [WHATSAPP_PERMISSION_ONBOARDING_AR.md](./WHATSAPP_PERMISSION_ONBOARDING_AR.md) | سُلّم الصلاحيات L0–L5 والبوابة الآمنة — Permission ladder + Secure Portal |
| 8 | [WHATSAPP_SECURITY_PRIVACY_AR.md](./WHATSAPP_SECURITY_PRIVACY_AR.md) | الأمان والخصوصية — Security + privacy |
| 9 | [WHATSAPP_HUMAN_HANDOFF_AR.md](./WHATSAPP_HUMAN_HANDOFF_AR.md) | التحويل إلى إنسان — Human handoff |
| 10 | [WHATSAPP_SUPPORT_ESCALATION_AR.md](./WHATSAPP_SUPPORT_ESCALATION_AR.md) | تصنيف الدعم والتصعيد — Support triage + escalation |
| 11 | [WHATSAPP_METRICS_AR.md](./WHATSAPP_METRICS_AR.md) | المقاييس — Metrics |
| 12 | [WHATSAPP_AGENT_REGISTRY_AR.md](./WHATSAPP_AGENT_REGISTRY_AR.md) | سجل وكلاء واتساب العشرة — The 10 WhatsApp agents |

> ترقيم الملفات في الجدول يبدأ من ١، أما هذا الملف (README) فهو الفهرس رقم صفر. The numbered entries map to docs 2–13 in the build list; this README is the index.

## النقاط النهائية — Endpoints

تحت البادئة `/api/v1/whatsapp-client` (المصدر: `api/routers/whatsapp_client.py`). All endpoints return a `governance_decision`. The router never sends or charges.

```
POST /api/v1/whatsapp-client/message         معالجة رسالة واردة عبر العقل المحكوم — process one inbound message
POST /api/v1/whatsapp-client/scan            تقييم فحص جاهزية كامل (١٠ محاور) — score a full 10-axis readiness scan
POST /api/v1/whatsapp-client/triage          فرز سريع ٤ أسئلة "اقترح علي" — quick 4-question "recommend for me"
GET  /api/v1/whatsapp-client/scan/questions  تعريفات أسئلة الفحص والفرز — scan + triage question definitions
GET  /api/v1/whatsapp-client/flows           خريطة التدفقات المحكومة — the controlled flow map
GET  /api/v1/whatsapp-client/metrics         تجميع للمؤسس (قراءة فقط) — founder-facing aggregation (read-only)
GET  /api/v1/whatsapp-client/webhook         تحقق Meta (echo challenge) — Meta verification handshake
POST /api/v1/whatsapp-client/webhook         معالجة رسالة واردة بدون إرسال — inbound processing (no send)
```

## مصدر الحقيقة — Source of truth

- الوحدة البرمجية — Module: `auto_client_acquisition/whatsapp_client_os/`
- سجل الخدمات القانوني — Canonical catalog: `auto_client_acquisition/service_catalog/`
- البنود غير القابلة للتفاوض — Non-negotiables: [docs/00_constitution/NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md)
- حارس العقيدة — Doctrine guard: `tests/test_no_secrets_in_whatsapp.py`

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
