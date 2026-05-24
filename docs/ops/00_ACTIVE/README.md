# docs/ops/00_ACTIVE — Active Operational SOPs (15 ملفات فقط)

**Purpose:** هذه الـ 15 ملف هي **الوحيدة الحية** للعمليات اليومية. أي ملف آخر في `docs/ops/` (103 ملف) = مرجع تاريخي، **لا تفتحه إلا للبحث**.

**Master plan:** [/MASTER_PLAN.md](../../../MASTER_PLAN.md) — يفوز عند أي تعارض.

---

## القائمة الحية (Wave 1 — 2026-05-24)

| # | الملف | الغرض |
|---|---|---|
| 1 | [/DEALIX_COMPANY_OPERATIONAL_STATE.md](../../../DEALIX_COMPANY_OPERATIONAL_STATE.md) | حالة الشركة الحالية (live endpoints + blockers) |
| 2 | [FOUNDER_DAILY_ANCHOR_AR.md](../FOUNDER_DAILY_ANCHOR_AR.md) | مرساة اليوم — أول ما يُقرأ صباحاً |
| 3 | [FOUNDER_SELL_MOTION_AR.md](../FOUNDER_SELL_MOTION_AR.md) | حركة البيع — كيف يقفل المؤسس صفقة |
| 4 | [FOUNDER_WEEKLY_ONE_DECISION_AR.md](../FOUNDER_WEEKLY_ONE_DECISION_AR.md) | القرار الواحد الأسبوعي |
| 5 | [pipeline_tracker.csv](../pipeline_tracker.csv) | الـ CRM الوحيد (50 lead، priority_rank) |
| 6 | [launch_content_queue.md](../launch_content_queue.md) | DMs + LinkedIn posts جاهزة للنسخ |
| 7 | [CUSTOMER_ONBOARDING_DAY_BY_DAY.md](../CUSTOMER_ONBOARDING_DAY_BY_DAY.md) | onboarding يوم-بيوم بعد الدفع |
| 8 | [FIRST_CUSTOMER_DELIVERY_TEMPLATE.md](../FIRST_CUSTOMER_DELIVERY_TEMPLATE.md) | template تسليم Sprint 7-يوم |
| 9 | [CEO_TOP50_TRACKER.csv](../CEO_TOP50_TRACKER.csv) | قائمة موسعة 50 CEO (ركز على pipeline_tracker أولاً) |
| 10 | [COMPANY_CONTROL_CENTER.md](../COMPANY_CONTROL_CENTER.md) | Control Center + Gates G1-G7 |
| 11 | [DEPLOY_RUNBOOK.md](../DEPLOY_RUNBOOK.md) | نشر backend + checks |
| 12 | [BACKUP_RESTORE.md](../BACKUP_RESTORE.md) | نسخ احتياطي Postgres |
| 13 | [DATABASE_STATE.md](../DATABASE_STATE.md) | جدول الحالة الحالية للـ DB |
| 14 | [ENV_UNLOCK_MATRIX.md](../ENV_UNLOCK_MATRIX.md) | env vars مطلوبة من المؤسس |
| 15 | [friction_log_review_weekly.md](../friction_log_review_weekly.md) | SOP أسبوعي لمراجعة friction (جديد) |

---

## القاعدة الذهبية

> **قبل فتح أي ملف آخر في `docs/ops/`، اسأل:** هل هو في هذه القائمة؟
> إذا لا → ابحث في الـ 15 أولاً. غالباً سيكون أحدها يجيب على سؤالك.
> إذا حتى الـ 15 لم يجيبوا → اقرأ المرجع التاريخي، ثم **حدّث الـ 15 ليشمل المعلومة الجديدة** (لا تكرر ملف).

---

## الـ 88 ملف الأخرى في `docs/ops/`

تبقى في مكانها للرجوع التاريخي. ستُؤرشف لـ `docs/_archive/2026_pre_revenue/` في موجات تنظيف لاحقة (10 ملفات/موجة، آخر أربعاء من كل شهر).

**قاعدة موجة التنظيف:** لا يُؤرشف ملف إلا بعد التحقق أن لا ملف من الـ 15 يُشير إليه، ولا commit في آخر 30 يوم لمسه.

---

*Version 1.0 — 2026-05-24 — Per MASTER_PLAN.md Section 10 (Doc Consolidation Plan)*
