# WhatsApp Security & Privacy — أمان وخصوصية واتساب

## معالجة البيانات الشخصية (PII)

نظام عميل واتساب لا يحتفظ ببيانات شخصية خام. الضوابط مفروضة في الكود ومحمية باختبار عقيدة.

- **معرّف واتساب كتجزئة فقط:** يُخزَّن معرّف العميل عبر `hash_wa_id` كـ SHA-256 مقطوعة بصيغة `wa_<16hex>` على حقل `wa_id_hash`. لا يُخزَّن رقم الهاتف الخام أبدًا، والتجزئة غير قابلة للعكس.
- **تنقيح نص الرسائل:** كل نص يمر عبر `sanitize_notes` قبل الحفظ، ويُخزَّن في `text_redacted` على `MessageEvent`. الوارد والصادر كلاهما مُنقَّح.
- **لا أسرار في السجلات:** يكتشف `looks_like_secret`/`secret_guard` المادة السرّية ولا تُخزَّن ولا تُردَّد. يحظر `guard_outbound` أي تسريب سرّ في النص الصادر.
- **لا دفع داخل واتساب:** الدفع عبر رابط آمن، والمفاتيح عبر البوابة الآمنة فقط. انظر [منح الصلاحيات](./WHATSAPP_PERMISSION_ONBOARDING_AR.md).

## حارس العقيدة

الاختبار `tests/test_no_secrets_in_whatsapp.py` يحرس العقيدة، على غرار حُرّاس `tests/test_no_*` القانونيين. يتحقق من أن النظام:

- يكتشف المادة السرّية ويوجّه التكاملات إلى البوابة الآمنة.
- لا يردّد ولا يخزّن سرًّا ملصوقًا (السرّ الخام لا يظهر في أي رسالة محفوظة).
- لا يصدر بطاقة أو ردًّا يطلب مفتاحًا في النص (بطاقة الصلاحيات تنصّ على «البوابة الآمنة» و«لا ترسل أي مفتاح» وتعرض `open_portal`).

## البنود غير القابلة للتفاوض كما تنطبق هنا

مشتقّة من عقيدة الوحدة، و`hard_gates` في سجل الخدمات، و[NON_NEGOTIABLES](../00_constitution/NON_NEGOTIABLES.md):

1. لا إرسال خارجي مباشر (`no_live_send`) — الطبقة معاينة/مسودة/اعتماد فقط.
2. لا خصم مالي مباشر (`no_live_charge`) — الدفع عبر رابط آمن خارج واتساب.
3. لا واتساب بارد (`no_cold_whatsapp`) — مرفوض عبر `BLOCKED_UNSAFE`.
4. لا أتمتة LinkedIn (`no_linkedin_auto`).
5. لا سحب بيانات (`no_scraping`).
6. لا قوائم مشتراة ولا رسائل جماعية (`no_blast`) — البديل: متابعة جهات العميل بموافقته.
7. لا إثبات مزيّف (`no_fake_proof`) — حِزم الإثبات مرتبطة بأدلة، والقيمة تقديرية لا مُتحقَّقة.
8. لا أرقام إيراد مزيّفة (`no_fake_revenue`) — لا التزام بأرقام؛ «تقديري» و«فرص مُثبتة بأدلة».
9. لا أسرار في النص — المفاتيح عبر البوابة الآمنة فقط، ولا تظهر في السجلات.
10. لا بيانات شخصية خام — تجزئة المعرّف وتنقيح النص قبل الحفظ.
11. كل مخرج يحمل قرار حوكمة (`governance_decision`) ويمر عبر حارس الإخراج.

روابط: [منح الصلاحيات والبوابة الآمنة](./WHATSAPP_PERMISSION_ONBOARDING_AR.md) · [التحويل إلى إنسان](./WHATSAPP_HUMAN_HANDOFF_AR.md) · [قواعد المحادثة](./WHATSAPP_CONVERSATION_POLICY_AR.md) · [البنود غير القابلة للتفاوض](../00_constitution/NON_NEGOTIABLES.md).

---

## English

### PII handling

The WhatsApp Client OS retains no raw PII. The controls are enforced in code and protected by a doctrine test.

- **WhatsApp id as a hash only** — the client id is stored via `hash_wa_id` as a truncated SHA-256 in the form `wa_<16hex>` on the `wa_id_hash` field. The raw phone number is never stored, and the hash is non-reversible.
- **Message text redaction** — every text passes `sanitize_notes` before persistence and is stored in `text_redacted` on `MessageEvent`. Both inbound and outbound are redacted.
- **No secrets in logs** — `looks_like_secret`/`secret_guard` detect secret material; it is neither stored nor echoed. `guard_outbound` blocks any secret leak in outbound text.
- **No payment inside WhatsApp** — payment is via a secure link, keys via the Secure Portal only. See [Permission onboarding](./WHATSAPP_PERMISSION_ONBOARDING_AR.md).

### The doctrine guard

The test `tests/test_no_secrets_in_whatsapp.py` guards the doctrine, mirroring the canonical `tests/test_no_*` guards. It verifies that the system:

- detects secret material and routes integrations to the Secure Portal;
- never echoes or persists a pasted secret (the raw secret appears in no stored message);
- never emits a card or reply asking for a key in text (the permission card states "secure portal" and "never send a key" and offers `open_portal`).

### The 11 non-negotiables as they apply here

Derived from the module doctrine, the catalog `hard_gates`, and [NON_NEGOTIABLES](../00_constitution/NON_NEGOTIABLES.md):

1. No live external send (`no_live_send`) — the layer is preview/draft/approval only.
2. No live charge (`no_live_charge`) — payment is via a secure link outside WhatsApp.
3. No cold WhatsApp (`no_cold_whatsapp`) — refused via `BLOCKED_UNSAFE`.
4. No LinkedIn automation (`no_linkedin_auto`).
5. No scraping (`no_scraping`).
6. No purchased lists or blasts (`no_blast`) — the alternative is follow-up on the client's contacts with approval.
7. No fake proof (`no_fake_proof`) — proof packs are evidence-tied; value is estimated, not verified.
8. No fake revenue (`no_fake_revenue`) — no number is promised; "estimated" and "evidenced opportunities".
9. No secrets in text — keys via the Secure Portal only, never in logs.
10. No raw PII — id hashing and text redaction before persistence.
11. Every output carries a `governance_decision` and passes the outbound guard.

Links: [Permission onboarding + Secure Portal](./WHATSAPP_PERMISSION_ONBOARDING_AR.md) · [Human handoff](./WHATSAPP_HUMAN_HANDOFF_AR.md) · [Conversation policy](./WHATSAPP_CONVERSATION_POLICY_AR.md) · [Non-negotiables](../00_constitution/NON_NEGOTIABLES.md).

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
