# Data OS — Consent, quality, retention and deletion system — نظام البيانات

## Purpose — الغرض

Data OS is the discipline layer for every piece of data Dealix holds. It records where data came from, whether consent exists, how fresh and accurate it is, how long it is kept, and when it must be deleted. It is PDPL-aware — designed around Saudi Personal Data Protection Law principles — so consent, quality, retention, and deletion are tracked as first-class controls rather than afterthoughts. AI analyzes records and recommends quality flags and retention actions; deterministic workflows enforce retention windows and execute approved deletions; the human approves any deletion or any use of data for a new purpose. The system keeps personal identifiers out of operational logs and provides the consent records that Proof OS and Client OS depend on before any named customer reference is published. Data without a recorded source and basis is treated as unusable.

نظام البيانات هو طبقة الانضباط لكل بيان تحتفظ به Dealix. يسجّل مصدر البيان، ووجود الموافقة من عدمه، ومدى حداثته ودقّته، ومدّة الاحتفاظ به، ومتى يجب حذفه. النظام مُدرك لنظام حماية البيانات الشخصية (مصمَّم حول مبادئ نظام حماية البيانات الشخصية السعودي) بحيث تُتتبَّع الموافقة والجودة والاحتفاظ والحذف كضوابط أساسية لا كأفكار لاحقة. يحلّل الذكاء الاصطناعي السجلات ويوصي بإشارات الجودة وإجراءات الاحتفاظ؛ وتفرض المسارات الحتمية نوافذ الاحتفاظ وتنفّذ الحذف المعتمد؛ ويعتمد الإنسان أي حذف أو أي استخدام للبيانات لغرض جديد. يبقي النظام المعرّفات الشخصية خارج السجلات التشغيلية، ويوفّر سجلات الموافقة التي يعتمد عليها نظام الإثبات ونظام العميل قبل نشر أي إشارة لعميل مُسمّى. البيان بلا مصدر وأساس مسجّل يُعامَل كغير قابل للاستخدام.

## Status — الحالة

Data OS | BETA | Consent, quality, retention, deletion controls

نظام البيانات | BETA | ضوابط الموافقة والجودة والاحتفاظ والحذف

## Inputs — المدخلات

- Public company context from Market Intelligence OS (no scraping) — السياق العام للشركات من نظام استخبارات السوق (بلا كشط)
- Consent declarations captured at point of collection — إقرارات الموافقة المُلتقَطة عند الجمع
- Retention and deletion policy from Governance OS — سياسة الاحتفاظ والحذف من نظام الحوكمة

## Outputs — المخرجات

- Consent records for named-customer references — سجلات الموافقة لإشارات العملاء المُسمّين
- Quality flags: freshness, accuracy, source completeness — إشارات الجودة: الحداثة، الدقّة، اكتمال المصدر
- Retention windows and approved deletion actions — نوافذ الاحتفاظ وإجراءات الحذف المعتمدة

## Guardrails — الضوابط

- No PII in logs (6): operational logs use anonymized labels — لا بيانات شخصية في السجلات
- No scraping (1): only sourced, consented data enters the system — لا كشط للبيانات
- No fake or un-sourced claims (4): unsourced data is flagged unusable — لا ادعاءات مزيّفة أو بلا مصدر
- No external action without approval (8): deletions and new-purpose uses are human-approved — لا إجراء خارجي بلا اعتماد

## Cross-links — روابط

- [`../00_platform_truth/MODULE_STATUS_MAP.md`](../00_platform_truth/MODULE_STATUS_MAP.md)
- [`MARKET_INTELLIGENCE_OS.md`](./MARKET_INTELLIGENCE_OS.md) · [`PROOF_OS.md`](./PROOF_OS.md) · [`CLIENT_OS.md`](./CLIENT_OS.md) · [`GOVERNANCE_OS.md`](./GOVERNANCE_OS.md)

---

Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
