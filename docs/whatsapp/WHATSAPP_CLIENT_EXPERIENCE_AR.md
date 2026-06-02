# WhatsApp Client Experience — تجربة العميل على واتساب

## الرسالة الأولى — القائمة (١–٦)

عند أول رسالة يستقبل العميل قائمة ترحيب قصيرة (قالب `welcome`). الأرقام مربوطة حتميًا بالنوايا في `intent_router._MENU`:

| الرقم | الخيار | النية (Intent) |
|---|---|---|
| 1 | فحص جاهزية شركتك | `start_scan` |
| 2 | تجهيز متابعة leads | `build_followup` |
| 3 | فهم أفضل خدمة مناسبة لك | `view_services` |
| 4 | مراجعة عرض أو تقرير | `review_proposal` |
| 5 | طلب دعم | `request_support` |
| 6 | ما أعرف — اقترح علي | `recommend_me` |

> العميل يختار رقمًا أو يكتب طلبه باختصار. الرقم ثقته عالية؛ النص الحر يُصنَّف بالكلمات المفتاحية.

## مسار "اقترح علي" — ٤ أسئلة

الخيار ٦ يشغّل الفرز السريع `QUICK_TRIAGE_QUESTIONS` — أربعة أسئلة قصيرة إجابتها اختيار، ثم توصية ببداية مناسبة عبر `quick_triage`:

1. **هل عندكم استفسارات أو leads شهريًا؟** (نعم / لا / غير متأكد)
2. **أين تأتي الاستفسارات غالبًا؟** (واتساب / إيميل / نموذج / إعلانات / فريق مبيعات / ما أعرف)
3. **ما أكبر مشكلة؟** (المتابعة / التقارير / الحجوزات / العروض / تشتت الفريق / ما أعرف)
4. **ما هدفك الأقرب؟** (زيادة الردود / حجز مواعيد / تقليل ضياع الفرص / تقرير للإدارة / بدء نظام كامل)

النتيجة توصية مرتبطة بسجل الخدمات: التشخيص المجاني، أو سبرنت إثبات الإيرادات (٤٩٩)، أو حزمة من البيانات إلى الإيراد (١٥٠٠)، أو عمليات النمو الشهرية (٢٩٩٩). كل التوصيات تقديرية، لا التزام بأرقام.

## الرحلة: من Lead إلى عميل

| المرحلة | ماذا يحدث | المخرج |
|---|---|---|
| **الدخول (Entry)** | الترحيب والقائمة، أو الفرز السريع لغير المتأكد | اختيار مسار |
| **القرار (Decision)** | فحص الجاهزية (١٠ محاور) ثم بطاقة التوصية فبطاقة العرض | عرض مرتبط بالكتالوج |
| **الأمان (Security)** | جمع الصلاحيات عبر البوابة الآمنة — لا مفاتيح في النص | رابط بوابة آمن (`portal_link_issued`) |
| **التسليم (Delivery)** | بدء التشغيل، أول workflow، مراجعة المسودات، حِزم الإثبات، التقرير الأسبوعي | بطاقات اعتماد + تقارير |
| **التجديد (Renewal)** | بطاقة التجديد/الترقية بناءً على القيمة الملاحظة | قرار تجديد |

- الدفع دائمًا عبر رابط آمن، لا داخل واتساب.
- المسودات لا تُرسل آليًا أبدًا — كل إرسال باعتماد يدوي.
- التحويل إلى إنسان متاح في كل مرحلة عند الحاجة.

روابط: [خريطة التدفقات](./WHATSAPP_FLOW_MAP_AR.md) · [بطاقات الإجراء والاعتماد](./WHATSAPP_APPROVAL_CARDS_AR.md) · [الصلاحيات والبوابة الآمنة](./WHATSAPP_PERMISSION_ONBOARDING_AR.md) · سجل الخدمات `auto_client_acquisition/service_catalog/`.

---

## English

### First message — the menu (1–6)

On the first message the client receives a short welcome menu (template `welcome`). The numbers are deterministically bound to intents in `intent_router._MENU`:

| # | Option | Intent |
|---|---|---|
| 1 | Company readiness scan | `start_scan` |
| 2 | Lead follow-up setup | `build_followup` |
| 3 | Best-fit service | `view_services` |
| 4 | Review a proposal or report | `review_proposal` |
| 5 | Support | `request_support` |
| 6 | Not sure — recommend for me | `recommend_me` |

> The client picks a number or describes the need briefly. A number is high-confidence; free text is keyword-classified.

### The "recommend for me" path — 4 questions

Option 6 runs the quick triage `QUICK_TRIAGE_QUESTIONS` — four short option-based questions, then a starting recommendation via `quick_triage`:

1. **Do you get leads/inquiries monthly?** (Yes / No / Not sure)
2. **Where do inquiries usually come from?** (WhatsApp / Email / Form / Ads / Sales team / Not sure)
3. **What is your biggest problem?** (Follow-up / Reporting / Bookings / Proposals / Team scatter / Not sure)
4. **What is your nearest goal?** (More replies / Book appointments / Fewer lost opportunities / Management report / Start a full system)

The result is a catalog-tied recommendation: Free Mini Diagnostic, Revenue Proof Sprint (499), Data-to-Revenue Pack (1500), or Growth Ops Monthly (2999). All recommendations are estimates; no number is promised.

### The journey: lead to client

| Stage | What happens | Output |
|---|---|---|
| **Entry** | Welcome + menu, or quick triage for the unsure | A chosen path |
| **Decision** | 10-axis readiness scan, then a recommendation card, then a proposal card | A catalog-tied proposal |
| **Security** | Permission collection via the Secure Portal — no keys in text | A secure portal link (`portal_link_issued`) |
| **Delivery** | Onboarding, first workflow, draft review, proof packs, weekly report | Approval cards + reports |
| **Renewal** | Renewal/upgrade card based on observed value | A renewal decision |

- Payment is always via a secure link, never inside WhatsApp.
- Drafts are never auto-sent — every send is manually approved.
- Human handoff is available at every stage when needed.

Links: [Flow map](./WHATSAPP_FLOW_MAP_AR.md) · [Action + approval cards](./WHATSAPP_APPROVAL_CARDS_AR.md) · [Permissions + Secure Portal](./WHATSAPP_PERMISSION_ONBOARDING_AR.md) · catalog `auto_client_acquisition/service_catalog/`.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
