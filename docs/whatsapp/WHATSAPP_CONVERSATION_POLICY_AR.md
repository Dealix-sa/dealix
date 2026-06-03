# WhatsApp Conversation Policy — قواعد المحادثة على واتساب

## القواعد

المحادثة على واتساب محكومة بقواعد ثابتة تحمي العميل وتحفظ الاتساق. لا توجد محادثة مفتوحة بنموذج لغوي؛ كل رد يأتي من قالب أو بطاقة معتمدة.

### ١) رسائل قصيرة وخيارات واضحة

- الردود مختصرة وموجّهة بخيارات (أرقام أو أزرار)، لا فقرات طويلة.
- الأمور المهمة تظهر كبطاقات منظَّمة لا كنص حر. انظر [بطاقات الإجراء](./WHATSAPP_APPROVAL_CARDS_AR.md).

### ٢) دائمًا اعرض "ما أعرف — اقترح علي"

- قائمة الترحيب تتضمن دائمًا الخيار رقم ٦: «ما أعرف — اقترح علي».
- هذا المسار يطرح ٤ أسئلة سريعة (`QUICK_TRIAGE_QUESTIONS`) ثم يعطي أنسب بداية. العميل غير المتأكد لا يُترك بلا طريق.

### ٣) نوايا حتمية فقط

- التصنيف حتمي عبر `intent_router.classify_intent`: أرقام القائمة أولًا، ثم مطابقة كلمات مفتاحية عربية/إنجليزية.
- لا يوجد توجيه بنموذج لغوي مفتوح. النوايا مجموعة محدّدة ومغلقة (`Intent`).
- عند الغموض الشديد (ثقة منخفضة) يظهر رد `unknown_fallback` الذي يعيد عرض الخيارات.

### ٤) لا إرسال بنموذج لغوي مفتوح

- لا يُولَّد نص حر يُرسل للعميل مباشرة. كل رد من القوالب (`templates.yaml`) أو من بطاقة معتمدة.
- لا يصدر أي إرسال خارجي مباشر ولا أي خصم مالي من المحادثة.
- طلبات التواصل البارد والقوائم المشتراة وسحب الأرقام مرفوضة فورًا عبر `BLOCKED_UNSAFE` مع عرض البديل الآمن.

### ٥) كل مخرج يحمل قرار حوكمة

- كل رد من العقل يحمل `governance_decision` بإحدى القيم: `ALLOW` أو `REQUIRE_APPROVAL` أو `ESCALATE` أو `BLOCK`.
- النص الصادر يمر عبر `guard_outbound`: يُحظَر النص الممنوع، ويُحوَّل الالتزام السعري إلى إنسان، وتُمنع تسريبات الأسرار.

### ما لا نقوله أبدًا

- لا التزام بأرقام مبيعات أو نسب تحويل أو عائد كحقيقة — نستخدم «تقديري» أو «فرص مُثبتة بأدلة».
- لا نستخدم «نضمن»؛ نستخدم لغة الالتزام.
- لا نطلب مفتاح API أو سرًّا في نص واتساب أبدًا.

روابط: [قواعد المحادثة → التدفقات](./WHATSAPP_FLOW_MAP_AR.md) · [مكتبة القوالب](./WHATSAPP_TEMPLATE_LIBRARY_AR.md) · [التحويل إلى إنسان](./WHATSAPP_HUMAN_HANDOFF_AR.md) · [البنود غير القابلة للتفاوض](../00_constitution/NON_NEGOTIABLES.md).

---

## English

### The rules

WhatsApp conversation is governed by fixed rules that protect the client and preserve consistency. There is no open LLM chat; every reply comes from a template or an approved card.

### 1) Short messages, clear options

- Replies are concise and option-driven (numbers or buttons), never long paragraphs.
- Important things appear as structured cards, not free text. See [Action cards](./WHATSAPP_APPROVAL_CARDS_AR.md).

### 2) Always offer "Not sure — recommend for me"

- The welcome menu always includes option 6: "Not sure — recommend for me".
- That path asks 4 quick questions (`QUICK_TRIAGE_QUESTIONS`), then gives the best starting point. An unsure client is never left without a route.

### 3) Deterministic intents only

- Classification is deterministic via `intent_router.classify_intent`: menu numbers first, then AR/EN keyword matching.
- No open-LLM routing. Intents are a fixed, closed set (`Intent`).
- On strong ambiguity (low confidence), the `unknown_fallback` reply re-offers the options.

### 4) No open LLM sends

- No free text is generated and sent to a client. Every reply is from templates (`templates.yaml`) or an approved card.
- No live external send or charge originates from the conversation.
- Cold-outreach, purchased lists, and number-harvesting requests are refused immediately via `BLOCKED_UNSAFE`, with the safe alternative offered.

### 5) Every output carries a governance decision

- Every brain reply carries a `governance_decision`: `ALLOW`, `REQUIRE_APPROVAL`, `ESCALATE`, or `BLOCK`.
- Outbound text passes `guard_outbound`: forbidden language is blocked, pricing commitments route to a human, and secret leaks are prevented.

### What we never say

- No sales numbers, conversion rates, or ROI as fact — we use "estimated" or "evidenced opportunities".
- We never say "guaranteed"; we use commitment language.
- We never request an API key or secret in WhatsApp text.

Links: [Flow map](./WHATSAPP_FLOW_MAP_AR.md) · [Template library](./WHATSAPP_TEMPLATE_LIBRARY_AR.md) · [Human handoff](./WHATSAPP_HUMAN_HANDOFF_AR.md) · [Non-negotiables](../00_constitution/NON_NEGOTIABLES.md).

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
