# نظام العملاء المحتملين — Dealix Prospect OS

هذا الملف يحدّد **دورة حياة العميل المحتمل**، حالاته، وقواعد التأهيل. الكيان `prospect` يحمل الحقول التالية حرفياً: `id`, `company`, `sector`, `region`, `source`, `decision_maker`, `status`, `pain_hypothesis`, `offer_angle`, `estimated_value_sar`, `confidence`, `preferred_channel`, `last_contact_at`, `next_action`, `next_action_date`, `risk`, `evidence_level`.

This file defines the **prospect lifecycle**, its statuses, and qualification rules. The `prospect` entity carries the fields above verbatim.

روابط / Related: [REVENUE_EXECUTION_OS_AR.md](REVENUE_EXECUTION_OS_AR.md) · [DRAFT_SYSTEM_SPEC_AR.md](DRAFT_SYSTEM_SPEC_AR.md) · [FOLLOWUP_ENGINE_AR.md](FOLLOWUP_ENGINE_AR.md) · [PROPOSAL_FACTORY_AR.md](PROPOSAL_FACTORY_AR.md) · [../commercial/OFFER_LADDER_AR.md](../commercial/OFFER_LADDER_AR.md)

---

## دورة حياة العميل المحتمل / The prospect lifecycle

```text
new → qualified → drafted → contacted → replied → discovery_booked
→ proposal_needed → proposal_sent → payment_handoff → won
                                                    ↘ lost
                                                    ↘ nurture
```

| الحالة / Status | المعنى / Meaning | الإجراء التالي النموذجي / Typical next_action |
|---|---|---|
| `new` | عميل جديد لم يُؤهَّل بعد. / New, not yet qualified. | تأهيل أولي |
| `qualified` | مرّ التأهيل (انظر القواعد أدناه). / Passed qualification. | تحديد زاوية العرض وصياغة مسودة |
| `drafted` | جُهِّزت مسودة تواصل بانتظار الموافقة. / A contact draft is pending approval. | موافقة المؤسس |
| `contacted` | أُرسِل تواصل يدوياً بعد الموافقة. / Manually contacted after approval. | متابعة وفق الإيقاع |
| `replied` | ردّ العميل المحتمل. / Prospect replied. | تأهيل الرد وحجز اكتشاف |
| `discovery_booked` | حُجِزت جلسة اكتشاف. / A discovery session is booked. | إجراء الجلسة وتحديد الحاجة |
| `proposal_needed` | الحاجة واضحة ويُطلَب عرض. / Need is clear; a proposal is required. | صياغة عرض (انظر PROPOSAL_FACTORY) |
| `proposal_sent` | أُرسِل عرض معتمَد. / An approved proposal was sent. | متابعة قرار العرض |
| `payment_handoff` | جاهز للدفع بعد كل الموافقات. / Ready for payment after all approvals. | تسليم للدفع (انظر PAYMENT_HANDOFF) |
| `won` | تحوَّل لعميل. / Converted to a customer. | تسليم (انظر DELIVERY_HANDOFF) |
| `lost` | لم يُغلَق. / Did not close. | تسجيل Win/Loss |
| `nurture` | غير جاهز الآن؛ رعاية لاحقة. / Not ready now; later nurture. | متابعة دورية خفيفة |

> الانتقال بين الحالات يتبع التسلسل؛ لا قفز إلى `proposal_sent` بلا `proposal_needed`، ولا `payment_handoff` بلا عرض معتمَد. / Status moves follow the sequence; no jump to `proposal_sent` without `proposal_needed`, no `payment_handoff` without an approved proposal.

---

## قواعد التأهيل / Qualification rules

ينتقل العميل من `new` إلى `qualified` فقط عند توفر **كل** ما يلي:

A prospect moves from `new` to `qualified` only when **all** of the following hold:

1. **القطاع والمنطقة معروفان** (`sector`, `region`) ويقعان ضمن استهداف Dealix. / Known sector and region within Dealix targeting.
2. **مصدر مسموح** (`source`) — لا scraping، لا قوائم مشتراة؛ علاقة قائمة، إحالة، أو طلب تواصل. / Allowed source — no scraping, no bought lists; existing relationship, referral, or inbound request.
3. **فرضية ألم واضحة** (`pain_hypothesis`) قابلة للاختبار. / A clear, testable pain hypothesis.
4. **زاوية عرض مبدئية** (`offer_angle`) مربوطة بمنتج من [../commercial/PRODUCT_CATALOG_AR.md](../commercial/PRODUCT_CATALOG_AR.md). / An initial offer angle linked to a catalog product.
5. **قيمة تقديرية وثقة** (`estimated_value_sar`, `confidence`) مسجَّلتان كتقدير لا كوعد. / An estimated value and confidence recorded as estimate, not promise.
6. **مخاطر روجِعت** (`risk`) — لا مانع امتثالي (PDPL/مصدر بيانات). / Risk reviewed — no compliance blocker.

> `estimated_value_sar` تقدير داخلي للأولوية، **ليس** سعراً معروضاً ولا قيمة مضمونة. / `estimated_value_sar` is an internal prioritization estimate — not an offered price or a guaranteed value.

---

## القناة المفضّلة والتواصل / Preferred channel and contact

- `preferred_channel` يُحدَّد من سلوك العميل ووفق [DRAFT_SYSTEM_SPEC_AR.md](DRAFT_SYSTEM_SPEC_AR.md): بريد، واتساب warm فقط، LinkedIn، أو هاتف. / Set from prospect behavior, per the draft spec: email, warm-only WhatsApp, LinkedIn, or phone.
- `last_contact_at` و`next_action_date` يقودان [FOLLOWUP_ENGINE_AR.md](FOLLOWUP_ENGINE_AR.md). / These two drive the follow-up engine.
- لا تواصل بارد ولا أتمتة قنوات؛ كل تواصل خارجي يمر بموافقة. / No cold contact, no channel automation; every external contact passes approval.

---

## ربط الدليل والمنتج / Evidence and product linkage

- `evidence_level` (L0–L5، راجع [PROOF_PACK_FACTORY_AR.md](PROOF_PACK_FACTORY_AR.md)) يحدّد جاهزية الترقية درجة في [../commercial/OFFER_LADDER_AR.md](../commercial/OFFER_LADDER_AR.md). / Evidence level gates rung promotion in the offer ladder.
- كل `offer_angle` يربط العميل بمنتج عبر `product_id` لاحقاً في العرض. / Each offer angle ties the prospect to a product via `product_id` at proposal time.

---

## قواعد ملزمة / Binding rules

1. لا PII في السجل التشغيلي للعميل المحتمل؛ تُستخدَم تسميات مجهَّلة عند الحاجة. / No PII in the prospect's operational record; anonymized labels when needed.
2. لا انتقال إلى `payment_handoff` بلا عرض معتمَد وموافقات [PAYMENT_HANDOFF_AR.md](PAYMENT_HANDOFF_AR.md). / No move to payment handoff without an approved proposal and the payment-handoff approvals.
3. لا ادعاء قيمة مضمونة في أي حقل؛ `estimated_value_sar` تقدير فقط. / No guaranteed-value claim in any field.
4. كل زاوية عرض مربوطة بمنتج كتالوج. / Every offer angle links to a catalog product.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
