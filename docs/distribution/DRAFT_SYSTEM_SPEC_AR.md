# Draft System Spec — مواصفة نظام المسودات — Draft System Spec

> Purpose — الغرض: تحدّد هذه الوثيقة حالات المسودة، أنواعها، والقاعدة الأساسية: كل مسودة تبدأ بحالة `pending_approval` وتحمل حقلَي `governance_decision` و`evidence_level`. لا مسودة تخرج من النظام بحالة «جاهزة للإرسال» تلقائيًا.
>
> This document defines draft states, draft types, and the core rule: every draft starts at `status=pending_approval` and carries both a `governance_decision` and an `evidence_level`. No draft leaves the system "ready to send" automatically.

Cross-link — روابط: [PRODUCT_DISTRIBUTION_OS_AR.md](./PRODUCT_DISTRIBUTION_OS_AR.md) · [DRAFT_APPROVAL_RUNBOOK_AR.md](./DRAFT_APPROVAL_RUNBOOK_AR.md) · [DRAFT_QUALITY_POLICY_AR.md](./DRAFT_QUALITY_POLICY_AR.md) · [CHANNEL_POLICY_AR.md](./CHANNEL_POLICY_AR.md) · [../05_governance_os/GOVERNANCE_DECISION_TYPES.md](../05_governance_os/GOVERNANCE_DECISION_TYPES.md).

---

## 1. القاعدة الأساسية — The core rule

كل مسودة، عند توليدها، تحمل ثلاثة حقول إلزامية:

Every draft, on generation, carries three mandatory fields:

- `status` — يبدأ دائمًا `pending_approval`.
- `governance_decision` — قرار الحوكمة المرفق (راجع جدول القرارات).
- `evidence_level` — مستوى الأدلة L0–L5.

مسودة بلا هذه الحقول الثلاثة تُعتبَر غير صالحة ولا تظهر في قائمة المراجعة. A draft missing any of the three is invalid and does not appear in the review queue.

تُخزَّن المسودات في `data/revenue_execution/drafts.jsonl` (قابل للتجاوز عبر `DEALIX_REVX_DRAFTS_PATH`)، وتُعرَض في `reports/distribution/DRAFT_QUEUE_REVIEW.md`.

Drafts are stored in `data/revenue_execution/drafts.jsonl` and surfaced in `reports/distribution/DRAFT_QUEUE_REVIEW.md`.

---

## 2. حالات المسودة — Draft states

| الحالة — State | المعنى — Meaning |
|---|---|
| `generated` | وُلِّدت آليًا، قبل الفحص |
| `pending_approval` | بانتظار قرار المؤسس (الحالة الافتتاحية الفعلية لكل مسودة) |
| `approved` | اعتمدها المؤسس |
| `rejected` | رفضها المؤسس |
| `needs_edit` | تحتاج تعديلًا قبل الاعتماد |
| `copied_manually` | نسخها المؤسس وأرسلها يدويًا |
| `sent_via_integration` | أُرسِلت عبر تكامل خارجي مُعتمَد لاحقًا (خارج نطاق الإصدار الأول) |
| `replied` | وصل ردّ من الجهة |
| `archived` | أُغلِقت/أُرشِفت |

> ملاحظة الإصدار الأول — v1 note: الحالة `sent_via_integration` معرّفة في المخطط للمستقبل، لكن **لا يوجد إرسال آلي في الإصدار الأول**. المسار العملي هو `approved → copied_manually`. لا ينقل النظام مسودة إلى `sent_via_integration` من تلقائه.

### مسار الحالات المسموح — Allowed state transitions

```text
generated → pending_approval
pending_approval → approved | rejected | needs_edit
needs_edit → pending_approval
approved → copied_manually
copied_manually → replied | archived
replied → archived
```

الانتقال إلى `copied_manually` فعل بشري حصري؛ لا يُنفّذه النظام. The transition to `copied_manually` is an exclusively human act; the system does not perform it.

---

## 3. أنواع المسودة — Draft types

| النوع — Type | الاستخدام — Use |
|---|---|
| `outreach_first` | تواصل أول (اليوم 0) |
| `outreach_followup_1` | متابعة أولى (اليوم 2) |
| `outreach_followup_2` | متابعة ثانية (اليوم 4) |
| `breakup` | رسالة إنهاء مهذّبة (اليوم 7) |
| `discovery_invite` | دعوة جلسة استكشاف بعد ردّ |
| `diagnostic_summary` | ملخّص التشخيص المجاني (Rung 0) |
| `proposal` | عرض على السلّم الخماسي |
| `proof_pack_intro` | تقديم حزمة الإثبات |
| `payment_followup` | متابعة دفع (بعد تسليم الدفع بـ24 ساعة) |
| `onboarding_message` | رسالة تهيئة بعد الدفع |
| `renewal_upsell` | تجديد/ترقية (يوم 21–30) |

كل نوع يُربَط بمرحلة في خط الأنابيب العشاري (راجع [PRODUCT_DISTRIBUTION_OS_AR.md](./PRODUCT_DISTRIBUTION_OS_AR.md)) وبإيقاع المتابعة (راجع [FOLLOWUP_ENGINE_AR.md](./FOLLOWUP_ENGINE_AR.md)).

Each type maps to a pipeline stage and to the follow-up cadence.

---

## 4. حقل قرار الحوكمة — The `governance_decision` field

يأتي من `governance_os` ويأخذ إحدى القيم: `ALLOW`, `DRAFT_ONLY`, `REQUIRE_APPROVAL`, `REDACT`, `BLOCK`, `RATE_LIMIT`, `REROUTE`. في هذه الطبقة، القيمة العملية القصوى لأي مسودة خارجية هي `REQUIRE_APPROVAL`؛ لا تصل أبدًا إلى «إرسال تلقائي».

It comes from `governance_os` and takes one of: `ALLOW`, `DRAFT_ONLY`, `REQUIRE_APPROVAL`, `REDACT`, `BLOCK`, `RATE_LIMIT`, `REROUTE`. In this layer, the maximum practical value for any outbound draft is `REQUIRE_APPROVAL`; it never reaches automatic sending.

- مسودة بقناة ممنوعة → `BLOCK` (راجع [CHANNEL_POLICY_AR.md](./CHANNEL_POLICY_AR.md)).
- مسودة تحوي بيانات شخصية في حقل معاينة → `REDACT` (البند 6).
- مسودة بادعاء غير مسنود → `BLOCK` حتى يُضاف مصدر (البند 4، 5).

---

## 5. حقل مستوى الأدلة — The `evidence_level` field

يأخذ L0–L5 (راجع التعريفات في [PRODUCT_DISTRIBUTION_OS_AR.md](./PRODUCT_DISTRIBUTION_OS_AR.md)). القاعدة: لا تُستخدَم مسودة بمحتوى تسويقي عام تحت L4 مع موافقة صريحة. مسودة التواصل الأولى تبدأ عادةً عند L1 (مسودة داخلية) وترتفع مع مراجعة العميل وموافقته.

Takes L0–L5. The rule: no draft with public-marketing content is used below L4 plus explicit consent. A first-outreach draft typically starts at L1 and rises as the customer reviews and approves.

---

## 6. مخطط المسودة (للمرجع) — Draft schema (reference)

المخطط الكامل في `schemas/`. الحقول الإلزامية:

```json
{
  "draft_id": "string",
  "type": "outreach_first | outreach_followup_1 | ... | renewal_upsell",
  "channel": "email | whatsapp | linkedin | phone | proposal | payment",
  "status": "pending_approval",
  "governance_decision": "DRAFT_ONLY | REQUIRE_APPROVAL | REDACT | BLOCK | ...",
  "evidence_level": "L0 | L1 | L2 | L3 | L4 | L5",
  "body_ar": "string",
  "body_en": "string",
  "source_ref": "string (Source Passport id — no PII)"
}
```

لا يحتوي المخطط على بريد أو هاتف أو هوية وطنية؛ يُشار للجهة عبر معرّف مصدر فقط (البند 6). The schema contains no email/phone/national ID; the prospect is referenced by a source id only.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
