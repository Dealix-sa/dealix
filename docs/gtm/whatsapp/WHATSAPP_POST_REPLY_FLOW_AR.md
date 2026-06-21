# WhatsApp Post-Reply Flow — مسار واتساب بعد الرد (بموافقة فقط) — Consent-gated WhatsApp flow

> طبقة **Market Production OS**. هذه وثيقة **رابطة**: تصف ما يحدث **بعد** رد إيجابي على بريد معتمَد، وتربط وحدات واتساب القائمة دون تكرارها. المبدأ الحاكم: **لا واتساب بارد إطلاقًا، لا أتمتة، الإرسال الفعلي معطّل افتراضيًا**. المصدر البرمجي الموثوق هو الكود لا هذه الوثيقة.

---

## 1) المبدأ الحاكم — لا واتساب بارد (AR)

واتساب في دِيلكس قناة **بعد الرد / بموافقة فقط**. لا تبدأ محادثة واتساب إلا بعد أن **يرد** العميل المحتمل إيجابيًا على بريد اعتمده المؤسس، ثم **يطلب** هو متابعة عبر واتساب أو يوافق عليها صراحةً. هذا يُكافئ بوابة opt-in في [`auto_client_acquisition/whatsapp_decision_bot/policy.py`](../../../auto_client_acquisition/whatsapp_decision_bot/policy.py) حيث `can_ever_live_send()` يعيد `False` دائمًا لهذه الطبقة، ويُحجب أي نمط «رسالة جماعية / قائمة مشتراة / cold whatsapp».

- **لا واتساب بارد.** لا تُرسَل رسالة افتتاحية لرقم لم يُبادِر أو لم يوافق.
- **لا أتمتة إرسال، ولا أتمتة LinkedIn.** البوت يبني بطاقات ومسودات؛ الإرسال قرار بشري.
- **العلَم معطّل افتراضيًا.** الإرسال الفعلي محكوم بـ `WHATSAPP_ALLOW_LIVE_SEND` (الافتراضي **false**) — انظر [`docs/WHATSAPP_PRODUCTION_CUTOVER.md`](../../WHATSAPP_PRODUCTION_CUTOVER.md).
- **سجل opt-in قبل أي قالب.** فحوص القابلية للتواصل (Compliance OS) تسبق أي إرسال جلسة أو قالب — انظر [`docs/WHATSAPP_OPERATOR_FLOW.md`](../../WHATSAPP_OPERATOR_FLOW.md).

## 1) Governing Principle — No Cold WhatsApp (EN)

WhatsApp at Dealix is a **post-reply / consent-only** channel. A WhatsApp conversation begins only after a prospect **replies** positively to a founder-approved email and then **asks for**, or explicitly consents to, a WhatsApp follow-up. This mirrors the opt-in gate in [`whatsapp_decision_bot/policy.py`](../../../auto_client_acquisition/whatsapp_decision_bot/policy.py), where `can_ever_live_send()` always returns `False` for this layer and any "broadcast / purchased list / cold whatsapp" pattern is blocked.

- **No cold WhatsApp.** No opening message to a number that did not initiate or consent.
- **No send automation, no LinkedIn automation.** The bot builds cards and drafts; sending is a human decision.
- **Flag off by default.** Live send is gated by `WHATSAPP_ALLOW_LIVE_SEND` (default **false**) — see [`docs/WHATSAPP_PRODUCTION_CUTOVER.md`](../../WHATSAPP_PRODUCTION_CUTOVER.md).
- **Opt-in ledger before any template.** Contactability checks (Compliance OS) precede any session or template send — see [`docs/WHATSAPP_OPERATOR_FLOW.md`](../../WHATSAPP_OPERATOR_FLOW.md).

---

## 2) شرط البدء — متى يجوز فتح واتساب أصلًا (AR)

الباب الوحيد إلى واتساب هو **رد إيجابي مُصنَّف**. حين يُصنِّف معالِج الردود ردًا بأنه `positive` (راجع `route_reply` و`REPLY_CLASSES` في [`auto_client_acquisition/gtm_os/records.py`](../../../auto_client_acquisition/gtm_os/records.py))، يكون الإجراء المقترح `route_to_discovery` بنص ثنائي: «حوّل إلى مكالمة/واتساب **بعد الموافقة**». لا يدخل أي رد آخر هذا المسار: `price_question` يحصل على بطاقة عرض، `send_more_info` يحصل على حزمة إثبات، و`unsubscribe`/`angry`/`bounce` تُكبَح فورًا.

## 2) Entry Condition — When WhatsApp May Open at All (EN)

The only door into WhatsApp is a **classified positive reply**. When the reply handler classifies a reply as `positive` (see `route_reply` and `REPLY_CLASSES` in [`gtm_os/records.py`](../../../auto_client_acquisition/gtm_os/records.py)), the suggested action is `route_to_discovery`: "Route to discovery / WhatsApp **after consent**." No other class enters this path: `price_question` gets an offer card, `send_more_info` gets a proof pack, and `unsubscribe`/`angry`/`bounce` are suppressed immediately.

---

## 3) المسار خطوة بخطوة — Step-by-step flow (AR)

| الخطوة — Step | ما يحدث — What happens | البوابة — Gate |
|---|---|---|
| 1) رد إيجابي على البريد | يُصنَّف الرد `positive` → الحالة `replied` على العميل المحتمل | تصنيف داخلي (لا إرسال) |
| 2) سؤال التفضيل | البوت يقترح مسودة: «هل تفضّل متابعة عبر واتساب أم حجز مكالمة؟» | المسودة تحتاج موافقة المؤسس قبل أي إرسال |
| 3) opt-in واتساب | يُسجَّل اختيار العميل في سجل opt-in قبل أي قالب | Compliance OS + opt-in ledger |
| 4) مسح الجاهزية | فحص عام/مُدخَل من المؤسس لإشارات الجاهزية (لا scraping) | بيانات عامة/مُدخَلة فقط |
| 5) بطاقة التوصية | بطاقة تفاعلية (≤ 3 أزرار) عبر [`whatsapp_cards.py`](../../../auto_client_acquisition/personal_operator/whatsapp_cards.py): قبول/تخطي/رسالة | لا HTTP send داخل الريبو |
| 6) العرض + الإثبات | بطاقة عرض من الكتالوج المعتمد + حزمة إثبات بمستوى أدلة | السعر محكوم بالكتالوج — لا يُخترَع |
| 7) الدفع/التهيئة | تسليم الدفع والتهيئة بموافقة صريحة | بوابات الموافقة (أدناه) |

كل انتقال من «مسودة» إلى «إرسال» يمر بموافقة المؤسس. البوت لا يُرسل نيابةً عن العميل دون موافقة صريحة.

## 3) Step-by-step Flow (EN)

| Step | What happens | Gate |
|---|---|---|
| 1) Positive email reply | Reply classified `positive` → prospect status `replied` | Internal classification (no send) |
| 2) Preference question | Bot drafts: "Prefer a WhatsApp follow-up, or to book a call?" | Draft needs founder approval before any send |
| 3) WhatsApp opt-in | Prospect's choice recorded in the opt-in ledger before any template | Compliance OS + opt-in ledger |
| 4) Readiness scan | Public / founder-input readiness signals only (no scraping) | Public/founder-input data only |
| 5) Recommendation card | Interactive card (≤ 3 buttons) via [`whatsapp_cards.py`](../../../auto_client_acquisition/personal_operator/whatsapp_cards.py): accept/skip/draft | No HTTP send in-repo |
| 6) Proposal + proof | Catalog offer card + evidence-leveled proof pack | Price governed by the catalog — never invented |
| 7) Payment / onboarding | Payment + onboarding handoff on explicit consent | Approval gates (below) |

Every "draft → send" transition passes founder approval. The bot never messages on the customer's behalf without explicit consent.

---

## 4) بطاقات الأزرار وحدود واتساب — Buttons + WhatsApp limits (AR)

البطاقات التفاعلية محدودة بـ **3 أزرار رد** لكل رسالة (حد WhatsApp Cloud API). الخطوة الأولى: قبول / تخطي / رسالة؛ الخطوة الثانية بعد «رسالة»: اعتماد / تعديل / إلغاء. كل المعرّفات مستقرّة لكل فرصة/مسودة. التفاصيل والحمولات في [`docs/WHATSAPP_OPERATOR_FLOW.md`](../../WHATSAPP_OPERATOR_FLOW.md) — لا نكرّرها هنا. لا تُخزَّن PII في البطاقة: المستلم مرجع معتم، لا اسم ولا رقم في النص الداخلي.

## 4) Buttons + WhatsApp Limits (EN)

Interactive cards are capped at **3 reply buttons** per message (WhatsApp Cloud API limit). Step one: accept / skip / draft; step two after "draft": approve / edit / cancel. IDs are stable per opportunity/draft. Payloads and details live in [`docs/WHATSAPP_OPERATOR_FLOW.md`](../../WHATSAPP_OPERATOR_FLOW.md) — not duplicated here. No PII in the card: the recipient is an opaque ref, never a name or number in internal copy.

---

## 5) ما هو **معطّل** ولماذا — What is OFF, and why (AR)

- **`WHATSAPP_ALLOW_LIVE_SEND` = false** افتراضيًا؛ لا إرسال فعلي قبل اكتمال opt-in والمراجعة القانونية وتفعيل صريح لبيئة محددة.
- **`can_ever_live_send()` = False** لهذه الطبقة دائمًا — حاجز صلب لا يعتمد على الإعداد.
- لا cold outreach، لا broadcast، لا قوائم مشتراة، لا harvesting أرقام — مفروض في [`policy.py`](../../../auto_client_acquisition/whatsapp_decision_bot/policy.py) و[`whatsapp_safe_send.py`](../../../auto_client_acquisition/whatsapp_safe_send.py).
- خطة الانتقال إلى الإنتاج وrollback في [`docs/WHATSAPP_PRODUCTION_CUTOVER.md`](../../WHATSAPP_PRODUCTION_CUTOVER.md): تعطيل الإرسال = إرجاع العلَم إلى `false`.

## 5) What Is OFF, and Why (EN)

- **`WHATSAPP_ALLOW_LIVE_SEND` = false** by default; no live send before opt-in completion, legal review, and an explicit per-environment enable.
- **`can_ever_live_send()` = False** for this layer, always — a hard guard independent of config.
- No cold outreach, broadcast, purchased lists, or number harvesting — enforced in [`policy.py`](../../../auto_client_acquisition/whatsapp_decision_bot/policy.py) and [`whatsapp_safe_send.py`](../../../auto_client_acquisition/whatsapp_safe_send.py).
- Cutover and rollback live in [`docs/WHATSAPP_PRODUCTION_CUTOVER.md`](../../WHATSAPP_PRODUCTION_CUTOVER.md): disabling send = returning the flag to `false`.

---

## 6) إعادة الاستخدام — لا تكرار — Reuse, not duplication

- **بوت قرار واتساب:** [`auto_client_acquisition/whatsapp_decision_bot/`](../../../auto_client_acquisition/whatsapp_decision_bot/) — السياسة والمعالِج والمعاينة.
- **بطاقات واتساب:** [`auto_client_acquisition/personal_operator/whatsapp_cards.py`](../../../auto_client_acquisition/personal_operator/whatsapp_cards.py) — حمولات أزرار آمنة.
- **الإرسال الآمن:** [`auto_client_acquisition/whatsapp_safe_send.py`](../../../auto_client_acquisition/whatsapp_safe_send.py).
- **تدفّق المشغّل والانتقال:** [`docs/WHATSAPP_OPERATOR_FLOW.md`](../../WHATSAPP_OPERATOR_FLOW.md) و[`docs/WHATSAPP_PRODUCTION_CUTOVER.md`](../../WHATSAPP_PRODUCTION_CUTOVER.md).
- **توجيه الردود ودورة الحالة:** [`../prospects/PROSPECT_OS_AR.md`](../prospects/PROSPECT_OS_AR.md) و[`auto_client_acquisition/gtm_os/records.py`](../../../auto_client_acquisition/gtm_os/records.py).
- **طابور الموافقة:** [`../FOUNDER_APPROVAL_QUEUE_AR.md`](../FOUNDER_APPROVAL_QUEUE_AR.md).

This flow reuses the existing WhatsApp modules; it does not add a new send path.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة. لا واتساب بارد، ولا إرسال بلا موافقة المؤسس.
> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.
