# Product Distribution OS — نظام تنفيذ الإيراد (Revenue Execution OS)

> Purpose — الغرض: هذه الوثيقة هي المرجع الأساسي لطبقة توزيع المنتج المبنية على الموافقة (approval-first). تشرح الغرض، القواعد الإحدى عشرة غير القابلة للتفاوض، خط الأنابيب من عشر مراحل، وكيف تُعيد هذه الطبقة استخدام طبقات `governance_os` و`data_os` و`proof_os` و`value_os` و`sales_os`. لا يُرسل أي شيء خارجيًا في الإصدار الأول؛ النظام يُجهّز المسودات فقط ليوافق عليها المؤسس ثم ينسخها ويرسلها يدويًا.
>
> This document is the canonical reference for the approval-first product-distribution layer. It states the purpose, the eleven non-negotiables, the ten-stage pipeline, and how this layer reuses `governance_os`, `data_os`, `proof_os`, `value_os`, and `sales_os`. Nothing is sent externally in v1; the system only prepares drafts for the founder to approve, then copy and send manually.

Cross-link — روابط: [README.md](./README.md) · [CHANNEL_POLICY_AR.md](./CHANNEL_POLICY_AR.md) · [DRAFT_SYSTEM_SPEC_AR.md](./DRAFT_SYSTEM_SPEC_AR.md) · [SECTOR_PRIORITIZATION_AR.md](./SECTOR_PRIORITIZATION_AR.md) · [PROOF_PACK_FACTORY_AR.md](./PROOF_PACK_FACTORY_AR.md) · [../00_constitution/NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md) · [../strategic/SAUDI_REVENUE_EXECUTION_OS_RADARS_AR.md](../strategic/SAUDI_REVENUE_EXECUTION_OS_RADARS_AR.md).

---

## 1. ما هي هذه الطبقة — What this layer is

نظام تنفيذ الإيراد هو الطبقة التي تحوّل النشاط التجاري إلى **مسودات مُحوكَمة جاهزة للموافقة**: من نستهدف، ماذا نقول، عبر أي قناة آمنة، مع منع المخاطر، وإنتاج Proof Pack وأصل رأسمالي لكل مشروع. الطبقة لا تتخذ إجراءً خارجيًا؛ هي مصنع مسودات وتسليمات يقرّ بها المؤسس.

The Revenue Execution OS turns commercial activity into **governed, approval-ready drafts**: who to target, what to say, on which safe channel, with risk prevention, producing a Proof Pack and a Capital Asset per project. The layer takes no external action; it is a factory of drafts and handoffs that the founder approves.

**التنفيذ المرجعي — canonical implementation:**

| العنصر — Element | المسار — Path |
|---|---|
| Python module | `auto_client_acquisition/revenue_execution_os/` |
| API prefix | `/api/v1/revenue-execution` (admin-gated via `X-API-Key`) |
| Daily script | `scripts/revenue_execution_day.py` |
| Draft-quality script | `scripts/revenue_execution_draft_quality.py` |
| Metrics script | `scripts/revenue_execution_metrics.py` |
| Make targets | `make distribution-day` · `make draft-quality` · `make revx-verify` |
| Reports | `reports/distribution/*.md` |
| JSONL stores | `data/revenue_execution/*.jsonl` (override via `DEALIX_REVX_*_PATH`) |
| Seed data | `data/distribution/sectors.yaml` · `channel_policy.yaml` · `prospects.example.json` |
| JSON schemas | `schemas/` |

كل استجابة من الـ API تحمل حقل `governance_decision`، ولا يوجد أي endpoint يُرسل شيئًا خارجيًا. Every API response carries a `governance_decision` field, and no endpoint sends anything externally.

---

## 2. القواعد الإحدى عشرة غير القابلة للتفاوض — The 11 non-negotiables

هذه الحدود تُطبَّق على كل مسودة، تسليم، وتقرير في هذه الطبقة. مخالفة أي بند تعني إيقاف الإجراء، لا التفاوض عليه.

These boundaries apply to every draft, handoff, and report in this layer. A violation halts the action; it is not negotiated.

1. **لا أنظمة كَشط (No scraping systems).** لا جمع بيانات آليًا من مصادر دون إذن مالكها.
2. **لا أتمتة واتساب بارد (No cold WhatsApp automation).** لا إرسال جماعي أو آلي لرسائل واتساب لجهات لم تُبدِ اهتمامًا.
3. **لا أتمتة لينكدإن (No LinkedIn automation).** لا أتمتة للتواصل أو القبول أو الرسائل على لينكدإن.
4. **لا ادعاءات مزيّفة أو بلا مصدر (No fake/un-sourced claims).** كل رقم أو حالة لها مصدر موثّق.
5. **لا ضمان لنتائج مبيعات (No guaranteed sales outcomes).** نتحدث عن «فرص مُثبتة بأدلة»، لا عن مبيعات مضمونة.
6. **لا بيانات شخصية في السجلات (No PII in logs).** لا بريد أو هاتف أو هوية وطنية أو أسماء حقيقية في أي log.
7. **لا إجابات معرفية بلا مصدر (No source-less knowledge answers).** كل إجابة معرفية مسنودة بمصدر.
8. **لا إجراء خارجي دون موافقة (No external action without approval).** لا إرسال أو نشر أو دفع دون إقرار المؤسس.
9. **لا وكيل دون هوية (No agent without identity).** كل وكيل يعمل بهوية مُسجَّلة وصلاحيات محدّدة.
10. **لا مشروع دون Proof Pack (No project without Proof Pack).** كل مشروع مدفوع يُنتج حزمة إثبات.
11. **لا مشروع دون أصل رأسمالي (No project without Capital Asset).** كل مشروع يودِع أصلًا قابلًا لإعادة الاستخدام.

> ملاحظة حوكمة — Governance note: البنود 1، 2، 3، 5، 8 تمنع أي «إرسال آلي» نهائيًا في هذه الطبقة. إن طلب أحد بناء كَشط أو إرسال بارد آلي، تُرفض المهمة وتُسجَّل، ولا تُنفَّذ.

---

## 3. خط الأنابيب من عشر مراحل — The 10-stage pipeline

كل مرحلة لها مُدخل، إجراء، مخرج، وحقل `governance_decision`. المراحل تتدفّق لكنها لا تُرسل؛ المخرج دائمًا مسودة أو تسليم بانتظار الموافقة.

Each stage has an input, an action, an output, and a `governance_decision`. Stages flow but never send; the output is always a draft or handoff awaiting approval.

| # | المرحلة — Stage | المُدخل — Input | المخرج — Output | الطبقة المُعاد استخدامها — Reused layer |
|---|---|---|---|---|
| 1 | الاستهداف — Target | قطاع + احتمال (prospect) | جهة مُرتَّبة بنموذج 100 نقطة | `sales_os` (ICP), `data_os` (provenance) |
| 2 | المسودة — Draft | جهة + نوع مسودة | نص ثنائي اللغة `status=pending_approval` | `sales_os`, `governance_os` |
| 3 | الجودة — Quality | دفعة مسودات | درجة جودة + أعلام | `governance_os` (claim/channel safety) |
| 4 | الموافقة — Approval | مسودة بانتظار الإقرار | approved / needs_edit / rejected | `governance_os` (approval matrix) |
| 5 | المتابعة — Follow-up | حالة الجهة | قائمة متابعة مُولَّدة للموافقة | `governance_os` |
| 6 | العرض — Proposal | جهة مؤهَّلة | مسودة عرض على السلّم الخماسي | `sales_os` (proposal sections) |
| 7 | الإثبات — Proof | مشروع مدفوع | Proof Pack بمستوى أدلة | `proof_os` (proof pack + score) |
| 8 | تسليم الدفع — Payment handoff | عرض مُعتمَد | تسليم دفع بانتظار الموافقة | `value_os`, `governance_os` |
| 9 | التهيئة — Onboarding | عميل دافع | رسالة تهيئة + تقرير قيمة أسبوعي | `value_os` (value ledger) |
| 10 | التجديد — Renewal | عميل نشط (يوم 21–30) | مسودة تجديد/ترقية | `value_os`, `sales_os` |

**القاعدة العابرة لكل المراحل:** المرحلة لا تتقدّم تلقائيًا إلى إجراء خارجي. الانتقال من «مسودة» إلى «مُرسَل» يحدث يدويًا بيد المؤسس فقط (راجع [DRAFT_APPROVAL_RUNBOOK_AR.md](./DRAFT_APPROVAL_RUNBOOK_AR.md)).

The cross-stage rule: a stage never auto-advances to an external action. The move from "draft" to "sent" is done manually, by the founder only.

---

## 4. كيف تُعاد استخدام الطبقات — How the OS reuses existing layers

هذه الطبقة لا تُكرّر منطقًا موجودًا؛ تستدعي الطبقات القائمة:

This layer duplicates no existing logic; it calls the layers already built:

- **`governance_os`** — مصدر الحقيقة لقرار `governance_decision`، مصفوفة الموافقة، فحص أمان الادعاء والقناة. كل مسودة تمرّ عليه قبل أن تصير `pending_approval`. راجع [../05_governance_os/GOVERNANCE_OS.md](../05_governance_os/GOVERNANCE_OS.md).
- **`data_os`** — مصدر البيانات وجواز المصدر (Source Passport)؛ لا تُستهدَف جهة بلا مصدر مُعلَن. راجع [../04_data_os/DATA_OS.md](../04_data_os/DATA_OS.md) و[../04_data_os/SOURCE_PASSPORT.md](../04_data_os/SOURCE_PASSPORT.md).
- **`proof_os`** — تجميع Proof Pack ودرجة الإثبات لكل مشروع مدفوع (البند 10). راجع [../07_proof_os/PROOF_OS.md](../07_proof_os/PROOF_OS.md) و[../07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md).
- **`value_os`** — سجل القيمة وتمييز Estimated / Observed / Verified؛ يحكم تقارير القيمة الأسبوعية والتجديد. راجع [../08_value_os/VALUE_OS.md](../08_value_os/VALUE_OS.md) و[../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md](../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md).
- **`sales_os`** — درجة ICP، أقسام العرض، وشجرة القرار التجاري التي تُغذّي العروض والاستهداف. راجع [../09_capital_os/CAPITAL_OS.md](../09_capital_os/CAPITAL_OS.md) لإيداع الأصل الرأسمالي (البند 11).

---

## 5. مستويات الأدلة — Evidence levels (L0–L5)

تُستخدَم لكل مسودة، حالة، وتسليم. القاعدة: لا تسويق عام تحت مستوى L4 مع موافقة صريحة.

Used for every draft, case, and handoff. The rule: no public marketing below L4 plus explicit consent.

| المستوى — Level | المعنى — Meaning |
|---|---|
| L0 | مُخطَّط — planned |
| L1 | مسودة داخلية — internal draft |
| L2 | راجعها العميل — customer reviewed |
| L3 | اعتمدها العميل (إثبات بيع خاص) — customer approved (private sales proof) |
| L4 | مُعتمَد للنشر العام (حالة دراسية) — public approved (case study) |
| L5 | دليل إيراد/توسّع — revenue/expansion evidence |

تفاصيل تطبيق المستويات في المسودات: [DRAFT_SYSTEM_SPEC_AR.md](./DRAFT_SYSTEM_SPEC_AR.md) و[PROOF_PACK_FACTORY_AR.md](./PROOF_PACK_FACTORY_AR.md).

---

## 6. السلّم التجاري الخماسي — The 5-rung commercial ladder

كل عرض يُربَط بدرجة على هذا السلّم؛ لا تُخترَع أسعار خارجه.

Every proposal maps to a rung; no prices are invented outside it.

| الدرجة — Rung | المنتج — Product | السعر — Price |
|---|---|---|
| Rung 0 | Free AI Ops Diagnostic | 0 SAR |
| Rung 1 | 7-Day Revenue Intelligence Sprint | 499 SAR |
| Rung 2 | Data-to-Revenue Pack | 1,500 SAR |
| Rung 3 | Managed Revenue Ops | 2,999–4,999 SAR/mo |
| Rung 4 | Custom AI Service Setup | 5,000–25,000 SAR + 1,000 SAR/mo |
| Enterprise (slow track) | AI Governance Review | 25,000–50,000 SAR |

تفصيل ربط العروض بالسلّم: [PROPOSAL_FACTORY_AR.md](./PROPOSAL_FACTORY_AR.md).

---

## 7. ماذا لا تفعل هذه الطبقة — What this layer will not do

- لا تُرسل بريدًا أو واتساب أو رسالة لينكدإن نيابةً عن أحد دون موافقة صريحة.
- لا تنشئ أنظمة كَشط ولا قوائم باردة آلية.
- لا تَعِد بأرقام مبيعات أو نسب تحويل كحقيقة.
- لا تُسجّل بيانات شخصية.
- لا ترسل رابط دفع دون عرض مُعتمَد وموافقة المؤسس.

This layer will not: send on anyone's behalf without explicit approval; build scraping or cold lists; promise sales numbers as fact; log PII; or send a payment link without an approved proposal and founder approval.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
