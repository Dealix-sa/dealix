# Draft Quality Policy — سياسة جودة المسودات — Draft Quality Policy

> Purpose — الغرض: تحدّد هذه الوثيقة بوابة الجودة التي تمرّ بها كل دفعة مسودات، وكيف يقيّمها `make draft-quality`. البوابة تفحص: أمان الادعاء، أمان القناة، حضور مستوى الأدلة، التخصيص، ووضوح دعوة الإجراء. الدرجة أداة فرز للمؤسس، وليست بديلًا عن موافقته.
>
> This document defines the quality gate every draft batch passes and how `make draft-quality` scores it. The gate checks: claim safety, channel safety, evidence-level presence, personalization, and a clear CTA. The score is a triage tool for the founder, not a substitute for approval.

Cross-link — روابط: [DRAFT_SYSTEM_SPEC_AR.md](./DRAFT_SYSTEM_SPEC_AR.md) · [DRAFT_APPROVAL_RUNBOOK_AR.md](./DRAFT_APPROVAL_RUNBOOK_AR.md) · [CHANNEL_POLICY_AR.md](./CHANNEL_POLICY_AR.md) · [../05_governance_os/CLAIM_SAFETY.md](../05_governance_os/CLAIM_SAFETY.md) · [../05_governance_os/GOVERNANCE_OS.md](../05_governance_os/GOVERNANCE_OS.md).

---

## 1. الأداة — The tool

`make draft-quality` يستدعي `scripts/revenue_execution_draft_quality.py`، يقرأ المسودات من `data/revenue_execution/drafts.jsonl`، ويكتب التقرير إلى `reports/distribution/DRAFT_QUEUE_REVIEW.md`. الفحص حتمي (لا قرار LLM يحدّد النجاح/الرفض).

`make draft-quality` invokes `scripts/revenue_execution_draft_quality.py`, reads drafts from `data/revenue_execution/drafts.jsonl`, and writes the report to `reports/distribution/DRAFT_QUEUE_REVIEW.md`. The check is deterministic; no LLM decides pass/fail.

---

## 2. بوابة الجودة — The quality gate (5 checks)

| الفحص — Check | يسأل — Asks | عند الفشل — On fail |
|---|---|---|
| أمان الادعاء — Claim safety | هل يوجد وعد بمبيعات/نسب/ROI كحقيقة، أو رقم بلا مصدر؟ | `BLOCK` (البند 4، 5) |
| أمان القناة — Channel safety | هل القناة مسموحة؟ هل توجد لغة كَشط/واتساب بارد/أتمتة لينكدإن؟ | `BLOCK` (البند 1، 2، 3) |
| حضور مستوى الأدلة — Evidence level present | هل `evidence_level` مضبوط؟ هل المحتوى التسويقي العام ≥ L4؟ | يُعلَّم نقص |
| التخصيص — Personalization | هل الرسالة موجَّهة لهذه الجهة لا قالبًا عامًا؟ | خصم درجة |
| وضوح دعوة الإجراء — Clear CTA | هل توجد دعوة إجراء واحدة واضحة؟ | خصم درجة |

أي فشل في **أمان الادعاء** أو **أمان القناة** يُسقِط المسودة إلى `BLOCK` بصرف النظر عن بقية الدرجة؛ هذان فحصان حاجزان لا تُعوَّضان.

A failure in **claim safety** or **channel safety** drops the draft to `BLOCK` regardless of the rest of the score; these two are blocking checks that cannot be offset.

---

## 3. كيف تُحسَب الدرجة — How the score is computed

درجة من 100، موزّعة على الفحوص. الحاجزان (الادعاء والقناة) شرط مرور؛ الثلاثة الباقية درجات تراكمية.

A score out of 100 across the checks. The two blocking checks are pass/fail gates; the remaining three are cumulative points.

| المكوّن — Component | الوزن — Weight |
|---|---|
| أمان الادعاء — Claim safety | حاجز (pass/fail) |
| أمان القناة — Channel safety | حاجز (pass/fail) |
| حضور مستوى الأدلة — Evidence level present | 30 |
| التخصيص — Personalization | 40 |
| وضوح دعوة الإجراء — Clear CTA | 30 |

- المسودة التي تسقط في أي حاجز → درجة فعّالة `BLOCK` ولا تظهر للاعتماد.
- المسودة التي تمرّ الحاجزين تأخذ درجة 0–100 من الثلاثة الباقية.

A draft failing either gate is effectively `BLOCK` and is not shown for approval; one passing both gates scores 0–100 on the remaining three.

---

## 4. عتبات القرار — Decision thresholds (guidance)

| الدرجة — Score | الإرشاد — Guidance |
|---|---|
| ≥ 85 | جاهزة غالبًا للاعتماد بعد قراءة سريعة |
| 60–84 | راجعها بعناية؛ غالبًا `needs_edit` |
| < 60 | افتراضيًا `needs_edit` أو `rejected` |
| `BLOCK` | لا تُعتمَد؛ أصلِح السبب أو ارفض |

> الدرجة لا تعتمد المسودة — The score does not approve the draft. الموافقة فعل بشري دائمًا (راجع [DRAFT_APPROVAL_RUNBOOK_AR.md](./DRAFT_APPROVAL_RUNBOOK_AR.md)).

---

## 5. أمثلة على ادعاءات مرفوضة — Examples of rejected claims

- «نضمن لك مبيعات» → يُستبدَل بـ«فرص مُثبتة بأدلة» (البند 5).
- «نرفع تحويلك 30٪» كرقم بلا مصدر → `BLOCK` (البند 4).
- «سمعنا من مديرك المالي…» (مرجع مُلفَّق) → `BLOCK` (البند 4).
- أي لغة «إرسال جماعي / blast / cold WhatsApp» → `BLOCK` (البند 2).

Rejected: "we guarantee sales" (replace with "evidenced opportunities"); "we raise conversion 30%" as a source-less number; a fabricated reference; any mass-send / cold language.

---

## 6. مكان الفحص في التدفّق — Where the gate sits in the flow

```text
generated → [draft-quality gate] → pending_approval → founder approval → copied_manually
```

البوابة تسبق الموافقة، لا تستبدلها. تُصفّي الواضح خطؤه قبل أن يصل وقت المؤسس. The gate precedes approval; it does not replace it. It filters the obviously-wrong before it reaches the founder's time.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
