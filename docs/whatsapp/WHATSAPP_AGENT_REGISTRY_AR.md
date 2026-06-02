# WhatsApp Agent Registry — سجل وكلاء واتساب

## الوكلاء العشرة

«الوكلاء» هنا أدوار منطقية داخل خط الأنابيب المحكوم، كلٌّ مربوط بوحدة كود محدّدة. لا وكيل يصدر إرسالًا خارجيًا مباشرًا ولا خصمًا ماليًا، وكلٌّ يلتزم بالبنود غير القابلة للتفاوض. تنسّقهم منطقة العقل `brain.py`.

| الوكيل | الوحدة | مسموح (Allowed) | ممنوع (Forbidden) |
|---|---|---|---|
| الكونسيرج (Concierge) | `intent_router.py` + `brain.py` | تصنيف نية حتمي، عرض القائمة، الردود من القوالب | توجيه بنموذج مفتوح، إرسال نص حر، قبول تواصل بارد |
| تقييم العميل (Client Assessment) | `readiness_scan.py` | فحص ١٠ محاور، فرز سريع ٤ أسئلة، درجات تقديرية | التزام بأرقام، إثبات مزيّف |
| بطاقة الإجراء (Action Card) | `action_cards.py` | بناء بطاقات منظَّمة بخيارات صريحة وقرار حوكمة | إرسال مباشر، خصم مالي، اعتماد مسودة محظورة |
| حارس الصلاحيات (Permission Guard) | `permission_os.py` | تدرّج L0–L5، توجيه التكاملات للبوابة، كشف الأسرار | طلب مفتاح في النص، تخزين سرّ خام، منح L5 عبر واتساب |
| مراجعة المسودة (Draft Review) | `policy_guard.py` + `action_cards.approval_card` | عرض المسودة، حجب الاعتماد عند الحظر، إرسال يدوي فقط | إرسال آلي، تمرير نص ممنوع، وعد سعري بوتي |
| مراجعة العرض (Proposal Review) | `action_cards.proposal_card` + `service_catalog` | عرض مرتبط بالكتالوج بأسعار تقديرية | أسعار/عروض مُختلَقة، تأكيد سعر نهائي |
| حزمة الإثبات (Proof Pack) | `action_cards.proof_pack_card` | عرض إثبات مرتبط بأدلة في البوابة، تنويه «تقديري لا مُتحقَّق» | إثبات مزيّف، أرقام إيراد كحقيقة |
| فرز الدعم (Support Triage) | `support_triage.py` | تصنيف لثماني فئات، تعليم ما يحتاج إنسانًا | حلّ الفوترة/الشكوى العاجلة بلا إنسان |
| التحويل إلى إنسان (Human Handoff) | `human_handoff.py` | كشف المُحفِّزات، بناء موجز مُنقَّح، تصعيد سريع | إخفاء التصعيد، تمرير بيانات شخصية خام في الموجز |
| نبرة العلامة (Brand Voice) | `templates.yaml` + `templates.py` | قوالب راقية موجزة ثنائية اللغة | حشو تسويقي، وعود ١٠×، رموز تعبيرية، اسم نموذج |

> كل المخرجات تمر عبر حارس الإخراج `guard_outbound`، وكل بطاقة/رد يحمل `governance_decision`. حارس العقيدة `tests/test_no_secrets_in_whatsapp.py` يحمي قاعدة الأسرار.

روابط: [نظرة عامة على النظام](./WHATSAPP_CLIENT_OS_AR.md) · [بطاقات الإجراء](./WHATSAPP_APPROVAL_CARDS_AR.md) · [الصلاحيات والبوابة الآمنة](./WHATSAPP_PERMISSION_ONBOARDING_AR.md) · [البنود غير القابلة للتفاوض](../00_constitution/NON_NEGOTIABLES.md) · سجل الخدمات `auto_client_acquisition/service_catalog/`.

---

## English

### The ten agents

"Agents" here are logical roles inside the controlled pipeline, each bound to a specific code module. No agent performs a live external send or charge, and each obeys the non-negotiables. They are orchestrated by the brain `brain.py`.

| Agent | Module | Allowed | Forbidden |
|---|---|---|---|
| Concierge | `intent_router.py` + `brain.py` | Deterministic intent classification, menu display, template replies | Open-model routing, free-text sends, accepting cold outreach |
| Client Assessment | `readiness_scan.py` | 10-axis scan, 4-question quick triage, estimated scores | Promising numbers, fake proof |
| Action Card | `action_cards.py` | Build structured cards with explicit options and a governance decision | Live send, live charge, approving a blocked draft |
| Permission Guard | `permission_os.py` | L0–L5 ladder, route integrations to the portal, detect secrets | Requesting a key in text, storing a raw secret, granting L5 over WhatsApp |
| Draft Review | `policy_guard.py` + `action_cards.approval_card` | Show the draft, withhold approve when blocked, manual send only | Auto-send, passing forbidden text, bot-authored price promises |
| Proposal Review | `action_cards.proposal_card` + `service_catalog` | Catalog-tied proposal at estimated prices | Invented prices/offers, confirming a final price |
| Proof Pack | `action_cards.proof_pack_card` | Show evidence-tied proof in the portal, "estimated not verified" notice | Fake proof, revenue numbers as fact |
| Support Triage | `support_triage.py` | Classify into eight categories, flag what needs a human | Resolving billing/urgent complaint without a human |
| Human Handoff | `human_handoff.py` | Detect triggers, build a redacted brief, fast escalation | Hiding escalation, passing raw PII in the brief |
| Brand Voice | `templates.yaml` + `templates.py` | Premium, concise, bilingual templates | Marketing fluff, 10x promises, emojis, model name |

> All outputs pass the outbound guard `guard_outbound`, and every card/reply carries a `governance_decision`. The doctrine guard `tests/test_no_secrets_in_whatsapp.py` protects the secrets rule.

Links: [System overview](./WHATSAPP_CLIENT_OS_AR.md) · [Action cards](./WHATSAPP_APPROVAL_CARDS_AR.md) · [Permissions + Secure Portal](./WHATSAPP_PERMISSION_ONBOARDING_AR.md) · [Non-negotiables](../00_constitution/NON_NEGOTIABLES.md) · catalog `auto_client_acquisition/service_catalog/`.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
