# H1 — Reply Handling OS — معالجة الردود وتوجيهها

> طبقة **Market Production OS**. هذه وثيقة **رابطة**: تشرح كيف يُصنَّف كل رد ويُوجَّه إلى الإجراء الصحيح، وتربط الوحدات القائمة ولا تكرّرها. المصدر البرمجي الموثوق هو الكود لا هذه الوثيقة.

## 1. المبدأ الحاكم — كل رد يُوجَّه، لا يُرسَل تلقائيًا (AR)

كل رد وارد على إرسال **معتمَد** يُصنَّف ثم يُوجَّه إلى إجراء. التصنيف والتوجيه في `auto_client_acquisition/gtm_os/records.py` (`Reply`, `route_reply`, ثابت `REPLY_CLASSES`)، ويُغذّيه المصنّف `auto_client_acquisition/email/reply_classifier.py`. كل سجل `Reply` خالٍ من PII (عبر `prospect_ref` و`draft_ref`) ويولد بـ `governance_decision = "approval_required"`: التوجيه اقتراح للمؤسس، لا فعل تلقائي. الردود الإيجابية لا تتحول إلى مكالمة/واتساب إلا **بعد موافقة وموافقة المستلم (consent)**.

## 1. Governing Principle — Every Reply Is Routed, Never Auto-Sent (EN)

Every inbound reply to an **approved** send is classified, then routed to an action. Classification and routing live in `auto_client_acquisition/gtm_os/records.py` (`Reply`, `route_reply`, the `REPLY_CLASSES` constant), fed by the classifier in `auto_client_acquisition/email/reply_classifier.py`. Every `Reply` record is PII-free (via `prospect_ref` and `draft_ref`) and is born with `governance_decision = "approval_required"`: routing is a suggestion for the founder, not an automatic act. Positive replies move to a call/WhatsApp only **after approval and recipient consent**.

## 2. أصناف الردود وجدول التوجيه (AR)

عشرة أصناف في `REPLY_CLASSES`. دالة `route_reply(classification)` تُرجِع الإجراء المقترح وعلَم الكبح:

| الصنف (`classification`) | الإجراء (`suggested_action`) | كبح فوري؟ | الخطوة التالية |
|---|---|---|---|
| `positive` | `route_to_discovery` | لا | حوّل إلى مكالمة/واتساب **بعد الموافقة والموافقة** |
| `interested_later` | `nurture` | لا | ضعه في التنشئة |
| `price_question` | `send_offer_card` | لا | أرسل بطاقة العرض |
| `send_more_info` | `send_proof_pack` | لا | أرسل حزمة الإثبات |
| `wrong_person` | `ask_referral` | لا | اطلب تحويلًا للشخص الصحيح |
| `not_interested` | `close_polite` | لا | أغلق بأدب |
| `unsubscribe` | `suppress_now` | **نعم** | كبح فوري |
| `angry` | `apologize_and_suppress` | **نعم** | اعتذار + كبح |
| `auto_reply` | `hold` | لا | انتظر/تجاهل |
| `bounce` | `suppress_now` | **نعم** | كبح (ارتداد) |

أي صنف غير معروف → `manual_review` (مراجعة يدوية، بلا كبح).

## 2. Reply Classes and Routing Table (EN)

Ten classes in `REPLY_CLASSES`. `route_reply(classification)` returns the suggested action and the suppression flag:

| Class (`classification`) | Action (`suggested_action`) | Suppress now? | Next step |
|---|---|---|---|
| `positive` | `route_to_discovery` | No | Route to call/WhatsApp **after approval + consent** |
| `interested_later` | `nurture` | No | Move to nurture |
| `price_question` | `send_offer_card` | No | Send the offer card |
| `send_more_info` | `send_proof_pack` | No | Send the proof pack |
| `wrong_person` | `ask_referral` | No | Ask for a referral |
| `not_interested` | `close_polite` | No | Close politely |
| `unsubscribe` | `suppress_now` | **Yes** | Suppress immediately |
| `angry` | `apologize_and_suppress` | **Yes** | Apologize + suppress |
| `auto_reply` | `hold` | No | Hold / ignore |
| `bounce` | `suppress_now` | **Yes** | Suppress (bounce) |

Any unknown class → `manual_review` (human review, no suppression).

## 3. الكبح الفوري قطعي (AR)

ثلاثة أصناف ترفع `requires_suppression = true`: `unsubscribe`, `angry`, `bounce`. كل منها يُنشئ `SuppressionEntry` فورًا و`permanent = true`، فلا يُتواصَل مع المستلم مجددًا. الكبح يسري في موضعين: البوابة تحجب أي مسودة لمستلم مكبوح بـ `suppression_hit`، والمخطِّط يستبعده بنفس الكود (انظر [SENDING_RAMP_OS_AR.md](SENDING_RAMP_OS_AR.md) و[DELIVERABILITY_AND_COMPLIANCE_AR.md](DELIVERABILITY_AND_COMPLIANCE_AR.md)). أسباب الكبح في `records.SUPPRESSION_REASONS`.

## 3. Immediate Suppression Is Absolute (EN)

Three classes raise `requires_suppression = true`: `unsubscribe`, `angry`, `bounce`. Each creates a `SuppressionEntry` immediately, with `permanent = true`, so the recipient is never contacted again. Suppression applies in two places: the gate blocks any draft for a suppressed recipient as `suppression_hit`, and the planner excludes them on the same code (see [SENDING_RAMP_OS_AR.md](SENDING_RAMP_OS_AR.md) and [DELIVERABILITY_AND_COMPLIANCE_AR.md](DELIVERABILITY_AND_COMPLIANCE_AR.md)). Suppression reasons live in `records.SUPPRESSION_REASONS`.

## 4. ردود المسار الإيجابي (AR)

- **`positive` → اكتشاف:** الانتقال إلى مكالمة/واتساب يتطلّب موافقة المؤسس **وموافقة المستلم (consent)**؛ لا قناة خارجية بلا opt-in. سجّل الموافقة في `auto_client_acquisition/compliance_os/consent_ledger`.
- **`price_question` → بطاقة العرض:** أرسل بطاقة العرض المطابقة لكتالوج العروض المعتمد. التسعير محكوم في سلّم الدرجات الخمس عبر [../../OFFER_LADDER_AND_PRICING.md](../../OFFER_LADDER_AND_PRICING.md) — لا يُخترَع سعر هنا.
- **`send_more_info` → حزمة الإثبات:** أرسل حزمة إثبات case-safe؛ معايير الإثبات في [../../07_proof_os/PROOF_PACK_STANDARD.md](../../07_proof_os/PROOF_PACK_STANDARD.md). القيمة تُعرَض كتقديرية لا مُتحقَّقة.
- **`wrong_person` → تحويل:** اطلب بأدب اسم/دور الشخص الصحيح؛ لا نخمّن ولا نبحث آليًا.

## 4. Positive-Path Replies (EN)

- **`positive` → discovery:** moving to a call/WhatsApp requires founder approval **and recipient consent**; no external channel without opt-in. Record consent in `auto_client_acquisition/compliance_os/consent_ledger`.
- **`price_question` → offer card:** send the offer card matched to the approved offer catalog. Pricing is governed by the five-rung ladder via [../../OFFER_LADDER_AND_PRICING.md](../../OFFER_LADDER_AND_PRICING.md) — no price is invented here.
- **`send_more_info` → proof pack:** send a case-safe proof pack; proof standards are in [../../07_proof_os/PROOF_PACK_STANDARD.md](../../07_proof_os/PROOF_PACK_STANDARD.md). Value is shown as estimated, not verified.
- **`wrong_person` → referral:** politely ask for the correct person's name/role; we never guess or look up automatically.

## 5. الردود غير الحاسمة (AR)

`interested_later` → تنشئة بزاوية قيمة لاحقة. `not_interested` → إغلاق مؤدب بلا إلحاح. `auto_reply` → انتظار/تجاهل (لا فعل). أي رد غامض → `manual_review` ليقرّر المؤسس. كل خطوة تالية مولَّدة هنا هي **مسودة** تعود إلى قائمة الموافقة قبل أي إرسال خارجي، وتمر بنفس البوابة في [COLD_EMAIL_DRAFT_FACTORY_AR.md](COLD_EMAIL_DRAFT_FACTORY_AR.md).

## 5. Non-Decisive Replies (EN)

`interested_later` → nurture on a later value angle. `not_interested` → polite close, no pushing. `auto_reply` → hold/ignore (no action). Any ambiguous reply → `manual_review` for the founder to decide. Every next step generated here is a **draft** that returns to the approval queue before any external send, passing the same gate in [COLD_EMAIL_DRAFT_FACTORY_AR.md](COLD_EMAIL_DRAFT_FACTORY_AR.md).

## 6. العقود والعينات (AR)

مخطط `reply.schema.json` و`suppression_entry.schema.json` في `dealix/contracts/schemas/`، والعينات في `data/gtm/replies/*.sample.jsonl` و`data/gtm/suppression/*.sample.jsonl`. تُولَّد العينات بـ `scripts/gtm_seed_samples.py`.

## 6. Contracts and Samples (EN)

The `reply.schema.json` and `suppression_entry.schema.json` schemas live in `dealix/contracts/schemas/`, with samples in `data/gtm/replies/*.sample.jsonl` and `data/gtm/suppression/*.sample.jsonl`. Samples are generated by `scripts/gtm_seed_samples.py`.

## روابط مرجعية / Related

- [COLD_EMAIL_DRAFT_FACTORY_AR.md](COLD_EMAIL_DRAFT_FACTORY_AR.md) — مصنع المسودات والبوابة / the draft factory + gate.
- [SENDING_RAMP_OS_AR.md](SENDING_RAMP_OS_AR.md) — المنحنى والكبح في الإرسال / ramp + send-time suppression.
- [DELIVERABILITY_AND_COMPLIANCE_AR.md](DELIVERABILITY_AND_COMPLIANCE_AR.md) — التسليم والامتثال / deliverability + compliance.
- [../signals/SIGNAL_OS_AR.md](../signals/SIGNAL_OS_AR.md) — الإشارات / signals.
- [../../07_proof_os/PROOF_PACK_STANDARD.md](../../07_proof_os/PROOF_PACK_STANDARD.md) — معيار حزمة الإثبات / proof pack standard.

---

**Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة.**
