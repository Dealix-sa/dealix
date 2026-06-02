# WhatsApp Client OS — System Overview — نظرة عامة على نظام عميل واتساب

## النظرة العامة

نظام عميل واتساب هو واجهة التشغيل التي يلتقي عبرها عميل السوق السعودي بـ Dealix على واتساب. الفكرة المركزية: واتساب تدفقات محكومة وليس محادثة مفتوحة. كل رسالة واردة تمر في خط أنابيب ثابت، وكل مخرج للعميل يحمل قرار حوكمة، ولا يصدر من هذه الطبقة أي إرسال خارجي مباشر ولا أي خصم مالي.

### الأنظمة الخمسة

1. **نظام عميل واتساب (WhatsApp Client OS):** الواجهة الأمامية — التدفقات، فحص الجاهزية، التوصية، البطاقات. الوحدة: `auto_client_acquisition/whatsapp_client_os/`.
2. **البوابة الآمنة للعميل (Secure Client Portal):** المسار الوحيد للأسرار والمفاتيح والصلاحيات من المستوى L2 فأعلى والدفع والعقود. لا تُطلب مفاتيح أبدًا في نص واتساب.
3. **نظام تنفيذ الإيرادات (Revenue Execution OS):** المحرك الذي ينتج المسودات والعروض وحِزم الإثبات المرتبطة بسجل الخدمات `service_catalog`.
4. **غرفة قيادة المؤسس (Founder Control Room):** السطح الداخلي للمؤسس — المقاييس (`metrics.compute_metrics`) وملخصات التحويل والقوائم.
5. **التحويل إلى إنسان (Human Handoff):** التصعيد السريع عند الغضب أو الالتزام السعري أو البيانات الحساسة أو الطلب الصريح، مع موجز داخلي مُنقَّح.

### خط الأنابيب المحكوم

العقل (`brain.handle_message`) ليس نموذجًا لغويًا حرًا، بل سلسلة خطوات ثابتة:

```
normalize → identify session → classify intent → load state
→ secret-guard (route integrations to portal)
→ human-handoff check → choose allowed action / build card
→ outbound-guard → audit (redacted)
```

- **normalize:** تنقية النص وإزالة المعلومات الشخصية قبل أي معالجة (`sanitize_notes`).
- **identify:** التعرّف على الجلسة عبر `hash_wa_id` — يُخزَّن معرّف واتساب كتجزئة فقط، لا رقم خام.
- **classify:** تصنيف نية حتمي عبر `intent_router.classify_intent` (أرقام القائمة أولًا ثم كلمات مفتاحية). لا توجيه بنموذج مفتوح.
- **secret-guard:** أي ذكر لتكامل أو مفتاح يُحوَّل إلى البوابة الآمنة عبر `secret_guard`.
- **handoff:** فحص شروط التحويل إلى إنسان عبر `should_handoff`.
- **route:** اختيار الإجراء المسموح وبناء البطاقة من ضمن مجموعة محدّدة فقط.
- **outbound-guard:** كل نص صادر يمر عبر `guard_outbound` — يُحظَر النص الممنوع، ويُحوَّل الالتزام السعري إلى إنسان.
- **audit:** تسجيل مُنقَّح في مخازن JSONL، بدون أسرار وبدون نص خام.

### لماذا تدفقات وليس روبوت محادثة مفتوحًا

- **القابلية للتدقيق:** كل خطوة قابلة للتتبع وكل مخرج يحمل قرار حوكمة.
- **السلامة:** لا يمكن للعميل أن يدفع النظام إلى وعد سعري أو إرسال خارجي أو طلب مفتاح في النص.
- **الاتساق:** التوصيات مربوطة بسجل الخدمات القانوني — لا عروض ولا أسعار مُختلَقة.
- **الثقة:** الوصول السريع إلى إنسان بعد بلوغ حدود الروبوت يرفع الثقة بدل أن يحبسها.

روابط: [خريطة التدفقات](./WHATSAPP_FLOW_MAP_AR.md) · [قواعد المحادثة](./WHATSAPP_CONVERSATION_POLICY_AR.md) · [البنود غير القابلة للتفاوض](../00_constitution/NON_NEGOTIABLES.md) · سجل الخدمات `auto_client_acquisition/service_catalog/`.

---

## English

### Overview

The WhatsApp Client OS is the operating surface where a Saudi B2B client meets Dealix on WhatsApp. The central idea: WhatsApp is controlled flows, not open chat. Every inbound message runs through a fixed pipeline, every client-facing output carries a `governance_decision`, and no live external send or charge originates from this layer.

### The five systems

1. **WhatsApp Client OS** — the front door: flows, readiness scan, recommendation, cards. Module: `auto_client_acquisition/whatsapp_client_os/`.
2. **Secure Client Portal** — the only path for secrets, keys, L2+ permissions, payment, and contracts. Keys are never requested in WhatsApp text.
3. **Revenue Execution OS** — the engine that produces drafts, proposals, and proof packs tied to the `service_catalog`.
4. **Founder Control Room** — the internal surface: metrics (`metrics.compute_metrics`), handoff briefs, and queues.
5. **Human Handoff** — fast escalation on anger, pricing commitment, sensitive data, or explicit request, with a redacted internal brief.

### The controlled pipeline

The brain (`brain.handle_message`) is not a free LLM; it is a fixed sequence:

```
normalize → identify session → classify intent → load state
→ secret-guard (route integrations to portal)
→ human-handoff check → choose allowed action / build card
→ outbound-guard → audit (redacted)
```

- **normalize** — sanitize and PII-redact the text (`sanitize_notes`) before any processing.
- **identify** — resolve the session via `hash_wa_id`; the WhatsApp id is stored as a hash only, never a raw number.
- **classify** — deterministic intent classification via `intent_router.classify_intent` (menu numbers first, then keywords). No open-model routing.
- **secret-guard** — any integration or key mention is routed to the Secure Portal via `secret_guard`.
- **handoff** — evaluate human-handoff triggers via `should_handoff`.
- **route** — pick an allowed action and build a card from a fixed set only.
- **outbound-guard** — every outbound text passes `guard_outbound`: forbidden language is blocked, pricing commitments route to a human.
- **audit** — redacted logging to JSONL stores, with no secrets and no raw text.

### Why flows, not an open chatbot

- **Auditability** — every step is traceable; every output carries a `governance_decision`.
- **Safety** — a client cannot push the system into a price promise, an external send, or a key-in-text request.
- **Consistency** — recommendations are bound to the canonical catalog; no invented offers or prices.
- **Trust** — fast access to a human once the bot hits its limits raises trust rather than trapping it.

Links: [Flow map](./WHATSAPP_FLOW_MAP_AR.md) · [Conversation policy](./WHATSAPP_CONVERSATION_POLICY_AR.md) · [Non-negotiables](../00_constitution/NON_NEGOTIABLES.md) · catalog `auto_client_acquisition/service_catalog/`.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
