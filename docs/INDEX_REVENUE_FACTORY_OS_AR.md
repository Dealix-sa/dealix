# فهرس مجموعة نظام مصنع الإيرادات

> النسخة الإنجليزية القانونية: [`INDEX_REVENUE_FACTORY_OS.md`](./INDEX_REVENUE_FACTORY_OS.md)

هذا هو spine مجموعة وثائق نظام مصنع الإيرادات: 25 وثيقة EN قانونية + 25 مرافقة AR + هذا الفهرس. كل صف يربط مواصفة التشغيل بالتشغيل الأساسي (موديولات، routers، migrations، scripts، GitHub Actions، Makefile targets) ليصبح التوثيق **قابلًا للتشغيل**، مو مجردًا.

## الدوكترين

كل وثيقة في هذه المجموعة مرتبطة بالـ 5 التزامات غير القابلة للمساس في [`docs/transformation/01_doctrine_lock.md`](./transformation/01_doctrine_lock.md):

1. ما يصير فعل خارجي عالي المخاطر بدون موافقة.
2. ما يصير ادعاء قيمة بدون دليل مصدر.
3. ما يصير وصول تشغيلي عبر المستأجرين.
4. ما يصير تشغيل إنتاجي بدون مسار رجوع.
5. ما يصير ادعاء يتجاوز مستوى الدليل المتاح.

## كيف تستخدم المجموعة

- **نقطة بداية تنفيذية**: [`founder/REVENUE_WAR_ROOM_OS_AR.md`](./founder/REVENUE_WAR_ROOM_OS_AR.md) و[`control_plane/SALES_COCKPIT_SYSTEM_AR.md`](./control_plane/SALES_COCKPIT_SYSTEM_AR.md).
- **نقطة بداية هندسية**: [`runtime/REVENUE_FACTORY_RUNTIME_AR.md`](./runtime/REVENUE_FACTORY_RUNTIME_AR.md)، [`runtime/WORKER_QUEUE_ARCHITECTURE_AR.md`](./runtime/WORKER_QUEUE_ARCHITECTURE_AR.md)، [`data/GROWTH_DATABASE_MODEL_AR.md`](./data/GROWTH_DATABASE_MODEL_AR.md).
- **نقطة بداية ثقة/امتثال**: [`control_plane/APPROVAL_CENTER_V2_AR.md`](./control_plane/APPROVAL_CENTER_V2_AR.md)، [`trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM_AR.md`](./trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM_AR.md)، [`evals/AI_EVAL_RED_TEAM_SYSTEM_AR.md`](./evals/AI_EVAL_RED_TEAM_SYSTEM_AR.md).
- **نقطة بداية تجارية**: [`distribution/DEALIX_DISTRIBUTION_OS_AR.md`](./distribution/DEALIX_DISTRIBUTION_OS_AR.md)، [`distribution/EXPERIMENT_ENGINE_AR.md`](./distribution/EXPERIMENT_ENGINE_AR.md)، [`finance/PRICING_YIELD_MANAGEMENT_AR.md`](./finance/PRICING_YIELD_MANAGEMENT_AR.md).

## الفهرس

### الطبقة A — الأساس

| # | الوثيقة (AR) | المرجع الإنجليزي |
|---|--------------|------------------|
| 1 | [مصنع الإيرادات](./runtime/REVENUE_FACTORY_RUNTIME_AR.md) | [EN](./runtime/REVENUE_FACTORY_RUNTIME.md) |
| 2 | [نموذج قاعدة بيانات النمو](./data/GROWTH_DATABASE_MODEL_AR.md) | [EN](./data/GROWTH_DATABASE_MODEL.md) |
| 3 | [معمارية طابور العمّال](./runtime/WORKER_QUEUE_ARCHITECTURE_AR.md) | [EN](./runtime/WORKER_QUEUE_ARCHITECTURE.md) |
| 4 | [مركز الموافقات v2](./control_plane/APPROVAL_CENTER_V2_AR.md) | [EN](./control_plane/APPROVAL_CENTER_V2.md) |
| 5 | [الموافقة والإيقاف والأساس النظامي](./trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM_AR.md) | [EN](./trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM.md) |

### الطبقة B — التجاري

| # | الوثيقة (AR) | المرجع الإنجليزي |
|---|--------------|------------------|
| 6 | [نظام التصريف](./distribution/DEALIX_DISTRIBUTION_OS_AR.md) | [EN](./distribution/DEALIX_DISTRIBUTION_OS.md) |
| 7 | [قابلية تسليم الإيميل](./distribution/EMAIL_DELIVERABILITY_SYSTEM_AR.md) | [EN](./distribution/EMAIL_DELIVERABILITY_SYSTEM.md) |
| 8 | [قمرة قيادة المبيعات](./control_plane/SALES_COCKPIT_SYSTEM_AR.md) | [EN](./control_plane/SALES_COCKPIT_SYSTEM.md) |
| 9 | [محرك التجارب](./distribution/EXPERIMENT_ENGINE_AR.md) | [EN](./distribution/EXPERIMENT_ENGINE.md) |
| 10 | [غرفة عمليات الإيرادات](./founder/REVENUE_WAR_ROOM_OS_AR.md) | [EN](./founder/REVENUE_WAR_ROOM_OS.md) |
| 11 | [رصة KPI على مستوى المجلس](./founder/BOARD_LEVEL_KPI_STACK_AR.md) | [EN](./founder/BOARD_LEVEL_KPI_STACK.md) |

### الطبقة C — التوابع + الحوكمة

| # | الوثيقة (AR) | المرجع الإنجليزي |
|---|--------------|------------------|
| 12 | [دورة حياة العميل](./client_success/CUSTOMER_LIFECYCLE_OS_AR.md) | [EN](./client_success/CUSTOMER_LIFECYCLE_OS.md) |
| 13 | [نظام الفوترة والمستحقات](./finance/BILLING_RECEIVABLES_OS_AR.md) | [EN](./finance/BILLING_RECEIVABLES_OS.md) |
| 14 | [نظام دعم ونجاح العميل](./client_success/SUPPORT_SUCCESS_OS_AR.md) | [EN](./client_success/SUPPORT_SUCCESS_OS.md) |
| 15 | [إدارة عائد التسعير](./finance/PRICING_YIELD_MANAGEMENT_AR.md) | [EN](./finance/PRICING_YIELD_MANAGEMENT.md) |
| 16 | [اقتصاد الوحدة لـ AI](./finance/AI_UNIT_ECONOMICS_AR.md) | [EN](./finance/AI_UNIT_ECONOMICS.md) |
| 17 | [الرصد و SLO](./engineering/OBSERVABILITY_SLO_SYSTEM_AR.md) | [EN](./engineering/OBSERVABILITY_SLO_SYSTEM.md) |
| 18 | [التقييم و Red Team](./evals/AI_EVAL_RED_TEAM_SYSTEM_AR.md) | [EN](./evals/AI_EVAL_RED_TEAM_SYSTEM.md) |
| 19 | [تصلّب سلسلة التوريد](./security/SUPPLY_CHAIN_HARDENING_ROADMAP_AR.md) | [EN](./security/SUPPLY_CHAIN_HARDENING_ROADMAP.md) |
| 20 | [مواصفة مركز القيادة](./product/COMMAND_CENTER_PRODUCT_SPEC_AR.md) | [EN](./product/COMMAND_CENTER_PRODUCT_SPEC.md) |
| 21 | [ماكينة الحسابات الاستراتيجية](./distribution/ABM_STRATEGIC_ACCOUNT_MACHINE_AR.md) | [EN](./distribution/ABM_STRATEGIC_ACCOUNT_MACHINE.md) |
| 22 | [ماكينة إيرادات الشركاء](./partners/PARTNER_REVENUE_MACHINE_AR.md) | [EN](./partners/PARTNER_REVENUE_MACHINE.md) |
| 23 | [ماكينة الذكاء التنافسي](./intelligence/COMPETITIVE_INTELLIGENCE_MACHINE_AR.md) | [EN](./intelligence/COMPETITIVE_INTELLIGENCE_MACHINE.md) |
| 24 | [حزمة العقود التجارية](./legal/COMMERCIAL_CONTRACT_PACK_AR.md) | [EN](./legal/COMMERCIAL_CONTRACT_PACK.md) |
| 25 | [محرّك المبيعات العربية](./localization/ARABIC_SALES_ENGINE_AR.md) | [EN](./localization/ARABIC_SALES_ENGINE.md) |

## بنود مفتوحة (بصراحة)

- هذه المجموعة **توثيق**، مو وقت تشغيل جديد. توصيل targets الـ Makefile الجديدة، بناء صندوق موافقات موحد، إضفاء الطابع الرسمي على سجل التجارب، وتوجيه الردود end-to-end كلها أعمال متابعة — كل واحد منها مذكور في بنود مفتوحة في الوثيقة ذات الصلة.
- ~12 من الـ 25 وثيقة توسّع مادة موجودة (التسعير، دورة الحياة، الرصد، التقييمات، Red Team، التنافسية، ABM، الشريك، العقود، مركز القيادة، غرفة العمليات، الفوترة). قيمتها = تجميع + ثنائية اللغة + ارتباط بالدوكترين، مو استراتيجية جديدة.
- هذا الفهرس spine لهذه المجموعة الـ 51 وثيقة؛ ما هو بديل لـ `docs/INDEX.md` على مستوى الريبو الذي يفهرس كل الـ 2,222 ملف.
