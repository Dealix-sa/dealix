# WhatsApp Human Handoff — التحويل إلى إنسان على واتساب

## المبدأ

الروبوت يجب أن يعرف متى يتوقف ويُدخل إنسانًا. الوصول السريع إلى إنسان بعد بلوغ الروبوت حدوده يرفع الثقة، لذلك التحويل صريح وسريع ومعروض دائمًا. المنطق في `auto_client_acquisition/whatsapp_client_os/human_handoff.py` عبر `should_handoff`.

## مُحفِّزات التحويل (`HandoffReason`)

| المُحفِّز | متى يُطلَق |
|---|---|
| `angry` | غضب أو استياء حاد (غاضب، زعلان، angry، furious) |
| `pricing_commitment` | طلب سعر نهائي أو التزام بسعر |
| `legal_contract` | عقد، اتفاقية، التزام قانوني، NDA، SLA |
| `sensitive_data` | بيانات بنكية، رقم هوية، آيبان، بطاقة (national id، iban) |
| `data_deletion` | طلب حذف بيانات (احذف بياناتي، delete my data) |
| `dissatisfied` | عدم رضا صريح (غير راضٍ، not satisfied) |
| `low_confidence` | ثقة تصنيف منخفضة (يُمرَّر من العقل) |
| `loop_limit` | تكرار ≥ ٣ أدوار بلا حلّ (`_LOOP_LIMIT = 3`) |
| `explicit_request` | طلب صريح لإنسان (أبغى شخص، كلموني، human، call me) |

> `low_confidence` و`loop_limit` ليسا نمطين نصّيين، بل يُمرَّران من العقل: الأول عند نية مجهولة بثقة < 0.4، والثاني عند بلوغ عدّاد الأدوار ثلاثة.

## رسالة العميل عند التحويل

العربية (`client_handoff_message("ar")`): «أحتاج أُدخل أحد من الفريق عشان نرد عليك بدقة. جهّزت لهم ملخص المحادثة والنقطة المطلوبة.»

English (`client_handoff_message("en")`): "I'll bring a teammate in so we answer you precisely. I've prepared a summary of the conversation and the point you need."

## الموجز الداخلي للتحويل (`build_handoff_brief`)

موجز للمؤسس/الفريق، نصّه مُنقَّح مسبقًا من البيانات الشخصية. الحقول:

| الحقل | المحتوى |
|---|---|
| `session_id` | معرّف الجلسة |
| `company` | اسم الشركة (إن وُجد) |
| `reasons` | قائمة مُحفِّزات التحويل |
| `last_message_redacted` | آخر رسالة بعد التنقيح |
| `suggested_response_ar` | رد مقترح بالعربية (اختياري) |
| `risk` | `high` إذا كان السبب غضبًا/قانونيًا/بيانات حساسة/حذفًا، وإلا `medium` |
| `next_action` | `call_or_approve_proposal_range` |

القرار المرافق للتحويل هو `ESCALATE`، وتُعلَّم الجلسة بـ `handoff_open = true`.

روابط: [تصنيف الدعم والتصعيد](./WHATSAPP_SUPPORT_ESCALATION_AR.md) · [قواعد المحادثة](./WHATSAPP_CONVERSATION_POLICY_AR.md) · [خريطة التدفقات](./WHATSAPP_FLOW_MAP_AR.md) · [الأمان والخصوصية](./WHATSAPP_SECURITY_PRIVACY_AR.md).

---

## English

### The principle

The bot must know when to stop and bring a human in. Fast access to a human after the bot reaches its limit raises trust, so handoff is explicit, fast, and always offered. The logic lives in `auto_client_acquisition/whatsapp_client_os/human_handoff.py` via `should_handoff`.

### Handoff triggers (`HandoffReason`)

| Trigger | When it fires |
|---|---|
| `angry` | Anger or sharp dissatisfaction (غاضب، زعلان، angry, furious) |
| `pricing_commitment` | A request for a final price or a price commitment |
| `legal_contract` | Contract, agreement, legal obligation, NDA, SLA |
| `sensitive_data` | Bank details, national id, IBAN, card (national id, iban) |
| `data_deletion` | A data-deletion request (احذف بياناتي, delete my data) |
| `dissatisfied` | Explicit dissatisfaction (غير راضٍ, not satisfied) |
| `low_confidence` | Low classification confidence (passed in from the brain) |
| `loop_limit` | A loop of ≥ 3 turns without resolution (`_LOOP_LIMIT = 3`) |
| `explicit_request` | An explicit request for a person (أبغى شخص, كلموني, human, call me) |

> `low_confidence` and `loop_limit` are not text patterns; they are passed in from the brain: the first on an unknown intent with confidence < 0.4, the second when the turn counter reaches three.

### The client handoff message

Arabic (`client_handoff_message("ar")`): "أحتاج أُدخل أحد من الفريق عشان نرد عليك بدقة. جهّزت لهم ملخص المحادثة والنقطة المطلوبة."

English (`client_handoff_message("en")`): "I'll bring a teammate in so we answer you precisely. I've prepared a summary of the conversation and the point you need."

### The internal handoff brief (`build_handoff_brief`)

A brief for the founder/team; its text is already PII-redacted. The fields:

| Field | Content |
|---|---|
| `session_id` | The session id |
| `company` | The company name (if present) |
| `reasons` | The list of handoff triggers |
| `last_message_redacted` | The last message after redaction |
| `suggested_response_ar` | A suggested Arabic reply (optional) |
| `risk` | `high` if the reason is anger/legal/sensitive-data/deletion, else `medium` |
| `next_action` | `call_or_approve_proposal_range` |

The decision attached to a handoff is `ESCALATE`, and the session is marked `handoff_open = true`.

Links: [Support triage + escalation](./WHATSAPP_SUPPORT_ESCALATION_AR.md) · [Conversation policy](./WHATSAPP_CONVERSATION_POLICY_AR.md) · [Flow map](./WHATSAPP_FLOW_MAP_AR.md) · [Security + privacy](./WHATSAPP_SECURITY_PRIVACY_AR.md).

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
