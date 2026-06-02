# WhatsApp Template Library — مكتبة قوالب واتساب

## القوالب

الردود الثابتة على واتساب تأتي من ملف `auto_client_acquisition/whatsapp_client_os/templates.yaml` (يُحمَّل عبر `templates.py`, الدالة `t(key, lang)`). كل قالب ثنائي اللغة (عربي/إنجليزي)، قصير، وموجَّه بخيارات. لا نص حر يُولَّد ويُرسَل خارج هذه القوالب أو البطاقات المعتمدة.

| المفتاح | الغرض | متى يظهر |
|---|---|---|
| `welcome` | قائمة الترحيب (١–٦) | أول رسالة أو تحية |
| `scan_intro` | مقدمة فحص الجاهزية | بدء فحص الجاهزية الكامل |
| `recommend_intro` | مقدمة «اقترح علي» (٤ أسئلة) | اختيار الخيار ٦ |
| `view_services_intro` | عرض الخدمات الأساسية | استعراض الخدمات / مراجعة عرض |
| `followup_sources` | مصادر leads للمتابعة | تجهيز متابعة |
| `draft_review_prompt` | تمهيد مراجعة المسودة | مراجعة مسودة |
| `unknown_fallback` | إعادة عرض الخيارات | غموض/ثقة منخفضة |
| `blocked_unsafe` | رفض التواصل البارد والقوائم المشتراة | طلب خارج السياسة |
| `human_handoff` | إشعار التحويل إلى إنسان | تصعيد |

### نقاط محتوى ثابتة

- `view_services_intro` يعرض الخدمات الأربع بأسعارها التقديرية كما في الكتالوج: فحص جاهزية الإيرادات (مجاني)، سبرنت إثبات الإيرادات (٤٩٩ ر.س)، حزمة من البيانات إلى الإيراد (١٥٠٠ ر.س)، عمليات النمو الشهرية (٢٩٩٩ ر.س/شهر).
- `followup_sources` يعرض المصادر [ملف CSV] [HubSpot] [Google Sheet] [أدخل يدوي] ويضيف صراحةً: «الربط يتم عبر البوابة الآمنة، وبدون إرسال آلي».
- `draft_review_prompt` يؤكد: «لا يتم أي إرسال إلا باعتمادك اليدوي».
- `blocked_unsafe` يرفض الرسائل الجماعية الباردة والقوائم المشتراة وسحب الأرقام، ويعرض البديل الآمن: متابعة لجهات اتصال العميل الحالية بموافقته على كل إرسال.

## قواعد النبرة والعلامة

- **راقية وموجزة:** نبرة أعمال سعودية تنفيذية، واضحة وحاسمة، بلا حشو تسويقي.
- **العربية أولًا:** المحتوى بالعربية أساسًا مع نظير إنجليزي مساوٍ في البنية والطول.
- **بلا روبوت كرتوني:** لا شخصية لعوبة، لا رموز تعبيرية، لا اسم نموذج.
- **بلا وعود ١٠×:** لا «نضاعف» ولا «نحوّل أعمالك» ولا أرقام عائد كحقيقة. نستخدم «تقديري» و«فرص مُثبتة بأدلة» ولغة الالتزام بدل «نضمن».
- **خيارات لا فقرات:** كل قالب ينتهي بسؤال أو قائمة خيارات قصيرة.

روابط: [قواعد المحادثة](./WHATSAPP_CONVERSATION_POLICY_AR.md) · [بطاقات الإجراء](./WHATSAPP_APPROVAL_CARDS_AR.md) · [تجربة العميل](./WHATSAPP_CLIENT_EXPERIENCE_AR.md) · [البنود غير القابلة للتفاوض](../00_constitution/NON_NEGOTIABLES.md).

---

## English

### The templates

WhatsApp's fixed replies come from `auto_client_acquisition/whatsapp_client_os/templates.yaml` (loaded via `templates.py`, function `t(key, lang)`). Each template is bilingual (AR/EN), short, and option-driven. No free text is generated and sent outside these templates or approved cards.

| Key | Purpose | When it appears |
|---|---|---|
| `welcome` | Welcome menu (1–6) | First message or greeting |
| `scan_intro` | Readiness scan intro | Starting the full readiness scan |
| `recommend_intro` | "Recommend for me" intro (4 questions) | Selecting option 6 |
| `view_services_intro` | Core services overview | Browsing services / reviewing a proposal |
| `followup_sources` | Lead sources for follow-up | Setting up follow-up |
| `draft_review_prompt` | Draft-review lead-in | Reviewing a draft |
| `unknown_fallback` | Re-offer the options | Ambiguity / low confidence |
| `blocked_unsafe` | Refuse cold outreach + purchased lists | Out-of-policy request |
| `human_handoff` | Human-handoff notice | Escalation |

### Fixed content points

- `view_services_intro` lists the four services with their estimated catalog prices: Free Revenue Readiness, Revenue Proof Sprint (499 SAR), Data-to-Revenue Pack (1500 SAR), Growth Ops Monthly (2999 SAR/mo).
- `followup_sources` shows the sources [CSV] [HubSpot] [Google Sheet] [Manual] and explicitly adds: "integrations go through the secure portal; no auto-send".
- `draft_review_prompt` confirms: "Nothing is sent without your manual approval".
- `blocked_unsafe` refuses cold blasts, purchased lists, and number harvesting, and offers the safe alternative: follow-up on the client's existing contacts, with approval on every send.

### Tone and brand rules

- **Premium and concise** — executive Saudi business tone, clear and decisive, no marketing fluff.
- **Saudi-first** — content is Arabic-first with a parallel English equivalent of matching structure and length.
- **No cartoon robot** — no playful persona, no emojis, no model name.
- **No 10x promises** — no "double", no "transform your business", no ROI numbers as fact. We use "estimated" and "evidenced opportunities", and commitment language instead of "guaranteed".
- **Options, not paragraphs** — every template ends with a question or a short option list.

Links: [Conversation policy](./WHATSAPP_CONVERSATION_POLICY_AR.md) · [Action cards](./WHATSAPP_APPROVAL_CARDS_AR.md) · [Client experience](./WHATSAPP_CLIENT_EXPERIENCE_AR.md) · [Non-negotiables](../00_constitution/NON_NEGOTIABLES.md).

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
