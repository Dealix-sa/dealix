# WhatsApp Action & Approval Cards — بطاقات الإجراء والاعتماد

## البطاقات

الأمور المهمة تظهر كبطاقات منظَّمة لا كنص طويل. كل بطاقة (`ActionCard`) تحمل عنوانًا ونصًّا ثنائيي اللغة، ومجموعة خيارات صريحة، ومستوى أدلة (`evidence_level`)، ومستوى مخاطر، وقرار حوكمة مشتقًّا من حارس الإخراج. **لا بطاقة تنفّذ إرسالًا خارجيًا مباشرًا ولا خصمًا ماليًا.** المصدر: `auto_client_acquisition/whatsapp_client_os/action_cards.py`.

### أنواع البطاقات التسعة (`ActionCardKind`)

| النوع | الغرض | قرار الحوكمة النموذجي |
|---|---|---|
| `recommendation` | التوصية بأفضل بداية بعد الفحص | `ALLOW` |
| `approval` | مراجعة مسودة قبل الإرسال اليدوي | `REQUIRE_APPROVAL` (أو `BLOCK` إن سقطت في الحارس) |
| `permission` | توجيه أي تكامل إلى البوابة الآمنة | `REQUIRE_APPROVAL` |
| `proposal` | عرض مرتبط بالكتالوج | `ALLOW` (يمر عبر الحارس) |
| `proof_pack` | حزمة إثبات للعرض في البوابة | `ALLOW` |
| `payment_handoff` | الدفع عبر رابط آمن خارج واتساب | `REQUIRE_APPROVAL` |
| `onboarding` | خطوات بدء التشغيل | `ALLOW` |
| `support_escalation` | تصنيف الدعم والتصعيد | `ALLOW` أو `ESCALATE` (للبشري) |
| `renewal` | التجديد/الترقية حسب القيمة الملاحظة | `ALLOW` (يمر عبر الحارس) |

### بطاقة التوصية (Recommendation Card)

تعرض جاهزية الإيرادات، نضج المتابعة، المخاطر، وسبب التوصية. الخيارات الأربعة:

- `start` — ابدأ
- `send_proposal` — أرسل العرض
- `book_call` — احجز مكالمة
- `explain` — اشرح أكثر

### بطاقة الاعتماد (Approval Card)

تعرض المسودة للمراجعة وتؤكد «إرسال آلي: لا». السلوك مشروط بحارس الإخراج (`guard_outbound`):

- **إذا اجتازت المسودة الحارس** — القرار `REQUIRE_APPROVAL` والمخاطر `low`، والخيارات: `approve` (اعتماد — إرسال يدوي)، `edit` (تعديل)، `reject` (رفض)، `shorten` (اختصرها)، `formal` (اجعلها رسمية أكثر).
- **إذا سقطت المسودة في الحارس** — القرار `BLOCK` والمخاطر `high`، **ويُحجَب خيار الاعتماد**، فلا يبقى إلا `edit` و`reject`.

> **بطاقات الاعتماد لا تُرسل مباشرة أبدًا.** الاعتماد يدوي، والإرسال يقع خارج هذه الطبقة بعد المراجعة. والمسودة المحظورة تُحرَم من خيار الاعتماد بالكامل.

روابط: [مكتبة القوالب](./WHATSAPP_TEMPLATE_LIBRARY_AR.md) · [الصلاحيات والبوابة الآمنة](./WHATSAPP_PERMISSION_ONBOARDING_AR.md) · [خريطة التدفقات](./WHATSAPP_FLOW_MAP_AR.md) · سجل الخدمات `auto_client_acquisition/service_catalog/`.

---

## English

### The cards

Important things appear as structured cards, not long text. Each `ActionCard` carries a bilingual title and body, an explicit set of options, an evidence level (`evidence_level`), a risk band, and a `governance_decision` derived from the outbound guard. **No card performs a live external send or a live charge.** Source: `auto_client_acquisition/whatsapp_client_os/action_cards.py`.

### The nine card kinds (`ActionCardKind`)

| Kind | Purpose | Typical governance decision |
|---|---|---|
| `recommendation` | Recommend the best start after a scan | `ALLOW` |
| `approval` | Review a draft before manual send | `REQUIRE_APPROVAL` (or `BLOCK` if guard trips) |
| `permission` | Route any integration to the Secure Portal | `REQUIRE_APPROVAL` |
| `proposal` | A catalog-tied proposal | `ALLOW` (passes the guard) |
| `proof_pack` | Proof pack for viewing in the portal | `ALLOW` |
| `payment_handoff` | Payment via a secure link outside WhatsApp | `REQUIRE_APPROVAL` |
| `onboarding` | Onboarding steps | `ALLOW` |
| `support_escalation` | Support triage and escalation | `ALLOW` or `ESCALATE` (to a human) |
| `renewal` | Renewal/upgrade based on observed value | `ALLOW` (passes the guard) |

### Recommendation Card

Shows revenue readiness, follow-up maturity, risk, and the reason for the recommendation. The four options:

- `start` — Start
- `send_proposal` — Send proposal
- `book_call` — Book a call
- `explain` — Explain more

### Approval Card

Shows the draft for review and confirms "Auto-send: no". Behavior is conditioned by the outbound guard (`guard_outbound`):

- **If the draft passes the guard** — decision `REQUIRE_APPROVAL`, risk `low`, options: `approve` (Approve — manual send), `edit`, `reject`, `shorten`, `formal` (More formal).
- **If the draft trips the guard** — decision `BLOCK`, risk `high`, **the approve option is withheld**, leaving only `edit` and `reject`.

> **Approval cards never live-send.** Approval is manual, and the send happens outside this layer after review. A blocked draft is denied the approve option entirely.

Links: [Template library](./WHATSAPP_TEMPLATE_LIBRARY_AR.md) · [Permissions + Secure Portal](./WHATSAPP_PERMISSION_ONBOARDING_AR.md) · [Flow map](./WHATSAPP_FLOW_MAP_AR.md) · catalog `auto_client_acquisition/service_catalog/`.

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
