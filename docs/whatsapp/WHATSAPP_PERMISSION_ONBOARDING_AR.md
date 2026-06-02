# WhatsApp Permission Onboarding — منح الصلاحيات على واتساب

## سُلّم الصلاحيات L0–L5

الصلاحيات متدرّجة (`PermissionLevel`)، والوصف ثنائي اللغة مأخوذ من `permission_os.PERMISSION_LEVELS`. المبدأ الحاكم: المستوى L2 فأعلى وكل الأسرار تمر عبر البوابة الآمنة، لا عبر نص واتساب.

| المستوى | الوصف (عربي) | Description (English) | البوابة الآمنة؟ |
|---|---|---|---|
| `L0` | محادثة فقط — بدون أي صلاحيات. | Chat only — no permissions. | لا |
| `L1` | رفع ملف أو رابط من العميل. | Client-provided file or link upload. | لا |
| `L2` | قراءة فقط من CRM أو جدول (عبر البوابة الآمنة). | Read-only from CRM or sheet (via secure portal). | نعم |
| `L3` | إنشاء مسودات ومهام داخلية. | Create internal drafts and tasks. | نعم (عند مسّ أنظمة خارجية) |
| `L4` | إرسال بعد موافقة صريحة على كل نوع. | Send after explicit per-type approval. | نعم |
| `L5` | دفع وعقود وبيانات حساسة — لا يتم عبر واتساب. | Payment, contracts, sensitive data — never over WhatsApp. | نعم |

> الإجراءات التي تمسّ أنظمة خارجية أو أسرارًا لا تُمنَح إلا عبر البوابة الآمنة: قراءة CRM، الإرسال بعد الموافقة، الدفع، توقيع العقود، البيانات الحساسة (`requires_secure_portal`). والمستوى L5 لا يُمنَح عبر نص واتساب إطلاقًا.

### القاعدة الصارمة: لا مفتاح API في نص واتساب

عند ذكر تكامل أو مفتاح، يكتشف `secret_guard` ذلك ويوجّه إلى البوابة الآمنة. وإذا لصق العميل مادة سرّية، تُنقَّح ولا تُخزَّن، ويُرشَد إلى البوابة. بطاقة الصلاحيات (`permission_card`) تنصّ صراحةً: «لا ترسل أي مفتاح هنا» وتعرض الخيارات:

- `open_portal` — فتح رابط آمن لإدخال المفتاح
- `manual_steps` — أرسل لي خطوات يدوية
- `csv` — استخدم ملف CSV بدل الربط
- `skip` — تجاوز الآن

## المسار: واتساب ← البوابة ← الخزنة ← التدقيق ← التأكيد

1. **واتساب (WhatsApp):** يُذكَر التكامل؛ يردّ النظام ببطاقة صلاحيات ورابط بوابة آمن. لا سرّ في النص.
2. **البوابة (Portal):** العميل يدخل المفتاح في البوابة الآمنة، خارج واتساب تمامًا.
3. **الخزنة (Vault):** يُخزَّن السرّ في الخزنة المشفّرة؛ لا يظهر في أي سجل.
4. **التدقيق (Audit):** يُسجَّل مرجع تدقيق (`audit_ref`) على سجل الصلاحية (`ClientPermission`)، بقيمة `granted_via = secure_portal`.
5. **التأكيد (Confirmation):** يعود إلى واتساب تأكيد نجاح الربط دون أي مادة سرّية.

روابط: [الأمان والخصوصية](./WHATSAPP_SECURITY_PRIVACY_AR.md) · [بطاقات الإجراء](./WHATSAPP_APPROVAL_CARDS_AR.md) · [خريطة التدفقات](./WHATSAPP_FLOW_MAP_AR.md) · [البنود غير القابلة للتفاوض](../00_constitution/NON_NEGOTIABLES.md).

---

## English

### The L0–L5 ladder

Permissions are graduated (`PermissionLevel`); the bilingual descriptions are taken from `permission_os.PERMISSION_LEVELS`. The governing principle: L2 and above, and all secrets, go through the Secure Portal, not WhatsApp text.

| Level | Description (Arabic) | Description (English) | Secure Portal? |
|---|---|---|---|
| `L0` | محادثة فقط — بدون أي صلاحيات. | Chat only — no permissions. | No |
| `L1` | رفع ملف أو رابط من العميل. | Client-provided file or link upload. | No |
| `L2` | قراءة فقط من CRM أو جدول (عبر البوابة الآمنة). | Read-only from CRM or sheet (via secure portal). | Yes |
| `L3` | إنشاء مسودات ومهام داخلية. | Create internal drafts and tasks. | Yes (when touching external systems) |
| `L4` | إرسال بعد موافقة صريحة على كل نوع. | Send after explicit per-type approval. | Yes |
| `L5` | دفع وعقود وبيانات حساسة — لا يتم عبر واتساب. | Payment, contracts, sensitive data — never over WhatsApp. | Yes |

> Actions that touch external systems or secrets may only be granted via the Secure Portal: read CRM, send-after-approval, payment, sign contract, sensitive data (`requires_secure_portal`). L5 is never granted over WhatsApp text.

### Hard rule: never request an API key in WhatsApp text

When an integration or key is mentioned, `secret_guard` detects it and routes to the Secure Portal. If a client pastes secret material, it is redacted and not stored, and the client is guided to the portal. The permission card (`permission_card`) states explicitly: "never send a key here" and offers:

- `open_portal` — Open secure link
- `manual_steps` — Send manual steps
- `csv` — Use CSV instead
- `skip` — Skip for now

### The path: WhatsApp → Portal → Vault → Audit → Confirmation

1. **WhatsApp** — an integration is mentioned; the system replies with a permission card and a Secure Portal link. No secret in text.
2. **Portal** — the client enters the key in the Secure Portal, entirely outside WhatsApp.
3. **Vault** — the secret is stored in the encrypted vault; it never appears in any log.
4. **Audit** — an audit reference (`audit_ref`) is recorded on the permission record (`ClientPermission`), with `granted_via = secure_portal`.
5. **Confirmation** — a success confirmation returns to WhatsApp with no secret material.

Links: [Security + privacy](./WHATSAPP_SECURITY_PRIVACY_AR.md) · [Action cards](./WHATSAPP_APPROVAL_CARDS_AR.md) · [Flow map](./WHATSAPP_FLOW_MAP_AR.md) · [Non-negotiables](../00_constitution/NON_NEGOTIABLES.md).

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
