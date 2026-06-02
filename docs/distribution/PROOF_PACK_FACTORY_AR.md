# Proof Pack Factory — مصنع حزمة الإثبات — Proof Pack Factory

> Purpose — الغرض: يحدّد هذا المستند محتوى حزمة الإثبات، ربطها بمستويات الأدلة L0–L5، والقاعدة غير القابلة للتفاوض رقم 10: لا مشروع مدفوع دون Proof Pack. الحزمة تُجمَّع من `proof_os`؛ هذه الطبقة تُجهّز مقدّمتها وتسليمها للموافقة.
>
> This document defines the Proof Pack contents, maps them to evidence levels L0–L5, and states non-negotiable #10: no paid project without a Proof Pack. The pack is assembled by `proof_os`; this layer prepares its intro and handoff for approval.

Cross-link — روابط: [PRODUCT_DISTRIBUTION_OS_AR.md](./PRODUCT_DISTRIBUTION_OS_AR.md) · [PROPOSAL_FACTORY_AR.md](./PROPOSAL_FACTORY_AR.md) · [PAYMENT_HANDOFF_AR.md](./PAYMENT_HANDOFF_AR.md) · [../07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md) · [../07_proof_os/PROOF_OS.md](../07_proof_os/PROOF_OS.md) · [../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md](../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md).

---

## 1. القاعدة غير القابلة للتفاوض — The non-negotiable

**البند 10: لا مشروع دون Proof Pack.** كل مشروع مدفوع (Rung 1 وما فوق) يُنتج حزمة إثبات قبل أن يُعَدّ مُسلَّمًا. مشروع بلا Proof Pack لا يُغلَق ولا يُسوَّق.

**Non-negotiable #10: no project without a Proof Pack.** Every paid project (Rung 1 and above) produces a Proof Pack before it is considered delivered. A project without one is neither closed nor marketed.

تُخزَّن حزم الإثبات في `data/revenue_execution/proof_packs.jsonl` (قابل للتجاوز عبر `DEALIX_REVX_PROOF_PACKS_PATH`).

---

## 2. محتوى حزمة الإثبات — Proof Pack contents

الحزمة تتبع المعيار الموحّد في `proof_os` (راجع [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md)). أقسامها الأساسية:

The pack follows the `proof_os` standard. Its core sections:

| # | القسم — Section | المحتوى — Content |
|---|---|---|
| 1 | الاستلام والنطاق — Intake & scope | ما اتُّفِق عليه |
| 2 | جواز المصدر — Source Passport | مالك البيانات، نوع المصدر، الاستخدام المسموح (لا كَشط) |
| 3 | جودة البيانات — Data quality | درجة الجودة قبل/بعد |
| 4 | إزالة التكرار — Dedupe | ما عُولِج |
| 5 | الترتيب/التحليل — Scoring/analysis | المنطق القابل للتفسير |
| 6 | المسودات — Drafts | المخرجات النصّية (لا بيانات شخصية) |
| 7 | قرارات الحوكمة — Governance decisions | سجل القرارات (BLOCK/REDACT/…) |
| 8 | الموافقات — Approvals | إقرارات المؤسس |
| 9 | تعيين القيمة — Value mapping | Estimated/Observed/Verified |
| 10 | الأصل الرأسمالي — Capital asset | الأصل المُودَع (البند 11) |
| 11 | الحدود — Limitations | ما لا تَعِد به الحزمة |
| 12 | المنهجية — Methodology | كيف عُمِل العمل |
| 13 | درجة الإثبات — Proof score | الدرجة الكميّة |
| 14 | التوقيعات — Signatures | الإقرار الختامي |

> كل قسم إلزامي — Every section is required. قسم ناقص يُفشِل تجميع الحزمة (راجع [PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md)).

---

## 3. ربط مستويات الأدلة — Evidence-level mapping

حزمة الإثبات ترفع مستوى الأدلة للمشروع عبر L0–L5:

The Proof Pack lifts the project's evidence level through L0–L5:

| المستوى — Level | المعنى — Meaning | في حزمة الإثبات — In the Proof Pack |
|---|---|---|
| L0 | مُخطَّط — planned | نطاق متّفق عليه، لا تنفيذ بعد |
| L1 | مسودة داخلية — internal draft | مخرجات أولية لم يرها العميل |
| L2 | راجعها العميل — customer reviewed | العميل قرأ الحزمة |
| L3 | اعتمدها العميل — customer approved | إثبات بيع خاص، موقّع |
| L4 | مُعتمَد للنشر — public approved | يصلح لحالة دراسية عامة |
| L5 | دليل إيراد/توسّع — revenue/expansion | تجديد أو توسّع موثّق |

**القاعدة:** لا تسويق عام للحزمة تحت L4 مع موافقة صريحة. الحالة الدراسية العامة لا تُنشَر إلا عند L4 + إذن مكتوب (راجع [../07_proof_os/CASE_SAFE_SUMMARY.md](../07_proof_os/CASE_SAFE_SUMMARY.md)).

The rule: no public marketing of the pack below L4 plus explicit consent. A public case study is published only at L4 plus written permission.

---

## 4. مقدّمة الحزمة (مسودة للموافقة) — Proof pack intro (draft for approval)

هذه الطبقة تُجهّز مسودة من نوع `proof_pack_intro` لتقديم الحزمة للعميل. تبدأ `pending_approval`، تحمل `governance_decision` و`evidence_level`، ولا تُرسَل إلا بعد موافقة المؤسس ونسخه اليدوي (راجع [DRAFT_SYSTEM_SPEC_AR.md](./DRAFT_SYSTEM_SPEC_AR.md)).

This layer prepares a `proof_pack_intro` draft to present the pack. It starts `pending_approval`, carries a `governance_decision` and `evidence_level`, and is sent only after founder approval and manual copy.

---

## 5. القيمة في الحزمة — Value inside the pack

كل رقم قيمة يُصنَّف:

Every value figure is classified:

- **Estimated** — تقدير منهجي (مثل ساعات موفّرة محسوبة منهجيًا).
- **Observed** — ملاحَظ على بيانات المشروع (مثل تكرارات أُزيلت).
- **Verified** — مُتحقَّق بقياس خارجي مستقلّ.

لا يُسوَّق رقم تقديري كأنه متحقَّق؛ هذا جوهر سطر الإخلاء في كل وثيقة (البند 4). راجع [../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md](../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md).

An estimated figure is never marketed as verified; this is the essence of the disclaimer on every doc.

---

## 6. الأصل الرأسمالي المُلازِم — The accompanying Capital Asset

البند 11 يلزم بإيداع أصل رأسمالي قابل لإعادة الاستخدام مع كل مشروع (قاعدة ترتيب، قالب، قاعدة حوكمة، رؤية قطاعية). يُسجَّل في القسم 10 من الحزمة وفي `capital_os` (راجع [../09_capital_os/CAPITAL_OS.md](../09_capital_os/CAPITAL_OS.md)).

Non-negotiable #11 requires depositing a reusable Capital Asset with each project (a scoring rule, template, governance rule, sector insight). It is recorded in pack Section 10 and in `capital_os`.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
