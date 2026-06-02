# Revenue Execution OS — فهرس نظام تنفيذ الإيراد — Index

> Purpose — الغرض: هذا الفهرس هو نقطة الدخول لطبقة توزيع المنتج المبنية على الموافقة. يشرح الحلقة اليومية للمؤسس ويربط بكل وثيقة في هذه الطبقة. القاعدة الحاكمة: النظام يُجهّز المسودات فقط؛ المؤسس يوافق ثم ينسخ ويرسل يدويًا. لا إرسال خارجي في الإصدار الأول.
>
> This index is the entry point for the approval-first product-distribution layer. It explains the founder's daily loop and links to every document in the layer. The governing rule: the system only prepares drafts; the founder approves, then copies and sends manually. No external send in v1.

---

## الحلقة اليومية للمؤسس — The daily founder loop

أربع خطوات، تتكرّر كل يوم عمل. لا خطوة منها تُرسل شيئًا خارجيًا تلقائيًا.

Four steps, repeated each working day. No step sends anything externally on its own.

1. **توليد — Generate.** شغّل `make distribution-day` (يستدعي `scripts/revenue_execution_day.py`). يكتب التقارير إلى `reports/distribution/`.
2. **مراجعة — Review.** افتح التقارير: `DISTRIBUTION_DAY.md`, `DRAFT_QUEUE_REVIEW.md`, `FOLLOWUP_QUEUE.md`, `PROPOSAL_DRAFT_REPORT.md`, `DISTRIBUTION_METRICS.md`, `WIN_LOSS_LEARNING.md`.
3. **قرار — Approve / edit / reject.** لكل مسودة: `approved`، أو `needs_edit`، أو `rejected`. درجة الجودة تأتي من `make draft-quality`.
4. **نسخ يدوي — Copy manually.** انسخ المسودات المعتمدة وأرسلها بنفسك عبر قناتها، ثم علّمها `copied_manually`.

> القاعدة غير القابلة للتفاوض رقم 8: لا إجراء خارجي دون موافقة. النظام لا يَنقُر «إرسال» أبدًا — أنت من يفعل، يدويًا، بعد الموافقة.

---

## الأوامر — Commands

| الأمر — Command | الوظيفة — Function |
|---|---|
| `make distribution-day` | تشغيل اليوم: توليد المسودات والمتابعات والتقارير |
| `make draft-quality` | تقييم جودة دفعة المسودات قبل الموافقة |
| `make revx-verify` | التحقق من سلامة الطبقة (حوكمة، لا إرسال خارجي) |

التقارير تُكتب إلى `reports/distribution/`. مخازن البيانات في `data/revenue_execution/*.jsonl` (قابلة للتجاوز عبر `DEALIX_REVX_*_PATH`).

---

## وثائق الطبقة — Layer documents

| الوثيقة — Document | الموضوع — Topic |
|---|---|
| [PRODUCT_DISTRIBUTION_OS_AR.md](./PRODUCT_DISTRIBUTION_OS_AR.md) | الغرض، القواعد الـ11، خط الأنابيب من 10 مراحل، إعادة استخدام الطبقات |
| [CHANNEL_POLICY_AR.md](./CHANNEL_POLICY_AR.md) | جدول سياسة القنوات: المسموح والممنوع لكل قناة |
| [SECTOR_PRIORITIZATION_AR.md](./SECTOR_PRIORITIZATION_AR.md) | نموذج 100 نقطة + الترتيب الابتدائي + أول عرض لكل قطاع |
| [DRAFT_SYSTEM_SPEC_AR.md](./DRAFT_SYSTEM_SPEC_AR.md) | حالات المسودة وأنواعها وقاعدة `pending_approval` |
| [DRAFT_APPROVAL_RUNBOOK_AR.md](./DRAFT_APPROVAL_RUNBOOK_AR.md) | كتاب تشغيل الموافقة اليومي للمؤسس |
| [DRAFT_QUALITY_POLICY_AR.md](./DRAFT_QUALITY_POLICY_AR.md) | بوابة الجودة وكيف يقيّم `make draft-quality` |
| [FOLLOWUP_ENGINE_AR.md](./FOLLOWUP_ENGINE_AR.md) | إيقاع المتابعة وأنه يولّد قائمة للموافقة فقط |
| [PROPOSAL_FACTORY_AR.md](./PROPOSAL_FACTORY_AR.md) | أقسام العرض + ربط السلّم الخماسي |
| [PROOF_PACK_FACTORY_AR.md](./PROOF_PACK_FACTORY_AR.md) | محتوى حزمة الإثبات + مستويات الأدلة |
| [PAYMENT_HANDOFF_AR.md](./PAYMENT_HANDOFF_AR.md) | حالات تسليم الدفع وقاعدة «لا رابط دفع بلا موافقة» |
| [RENEWAL_ENGINE_AR.md](./RENEWAL_ENGINE_AR.md) | سلّم التجديد ومحفّزاته |
| [WIN_LOSS_LEARNING_AR.md](./WIN_LOSS_LEARNING_AR.md) | ما يُسجَّل لكل نتيجة + أسئلة التعلّم الأسبوعية |
| [DISTRIBUTION_METRICS_AR.md](./DISTRIBUTION_METRICS_AR.md) | قوائم المؤشرات اليومية والأسبوعية |
| [EXTERNAL_AUTOMATION_BLUEPRINT_AR.md](./EXTERNAL_AUTOMATION_BLUEPRINT_AR.md) | سياسة n8n: المسموح الحتمي مقابل الممنوع |
| [../references/REVENUE_EXECUTION_REFERENCE_LIBRARY.md](../references/REVENUE_EXECUTION_REFERENCE_LIBRARY.md) | مكتبة مرجعية فقط — ليست اعتماديات |

---

## روابط ذات صلة — Related links

- الدستور: [../00_constitution/NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md)
- الحوكمة: [../05_governance_os/GOVERNANCE_OS.md](../05_governance_os/GOVERNANCE_OS.md)
- الإثبات: [../07_proof_os/PROOF_PACK_STANDARD.md](../07_proof_os/PROOF_PACK_STANDARD.md)
- السبرنت: [../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md)
- تأكيد الدفع اليدوي: [../wave6/MANUAL_PAYMENT_CONFIRMATION_CHECKLIST.md](../wave6/MANUAL_PAYMENT_CONFIRMATION_CHECKLIST.md)
- الرؤية الاستراتيجية: [../strategic/SAUDI_REVENUE_EXECUTION_OS_RADARS_AR.md](../strategic/SAUDI_REVENUE_EXECUTION_OS_RADARS_AR.md)

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
