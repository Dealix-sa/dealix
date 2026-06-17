# معمارية طابور العمّال

> النسخة الإنجليزية القانونية: [`WORKER_QUEUE_ARCHITECTURE.md`](./WORKER_QUEUE_ARCHITECTURE.md).

## مرجع الدوكترين
- الالتزامات: #1 (الموافقة قبل الفعل الخارجي)، #4 (لا تشغيل إنتاجي بدون مسار رجوع).
- القرارات المثبّتة: سكربتات التحقق على لوحة التحكم تكون مانعة للإصدار.

## الغرض

تشغيل عمّال المصنع بشكل موثوق على السيرفر. تحديد أي عبء عمل ينتمي لـ cron، أيها لطابور غير متزامن، وأيها لمحرك سير عمل قابل للاستمرار.

## الوضع الحالي

- ARQ + Redis شغّال: `core/queue/worker.py` (10 وظائف متزامنة، 5 دقائق timeout، 3 إعادات محاولة).
- المهام: `core/queue/tasks.py` (`run_agent_job`).
- مهام مجدولة: `core/queue/weekly_self_improvement.py`، `core/queue/cs_handoff_task.py`.
- التشغيل اليومي: GitHub Actions (`daily-revenue-machine.yml`، `founder_commercial_daily.yml`، `daily_digest.yml`، `daily_snapshot.yml`، `founder_autonomous_ops_weekly.yml`، `founder_strongest_ops_daily.yml`).
- لقطات محلية: `make v5-status`، `make v5-digest`، `make v5-snapshot`.

## المراحل

### المرحلة 1 — Cron / Actions (الآن)
للتقارير المجدولة، التصنيف الحتمي، اللقطات اليومية، التجميعات الداخلية بدون أثر خارجي.

### المرحلة 2 — ARQ على Redis (الآن، للحمل المتغيّر)
لإثراء العملاء بالموازاة، توليد drafts التواصل، تصنيف الردود، توليد العينات، استدعاءات LLM داخلية مع retry.

### المرحلة 3 — سير عمل قابل للاستمرار (مستقبل)
لدورة العرض، تحصيل الدفع، التسليم، إعادة محاولات الموافقة عبر إعادات النشر. مرشّحات: Temporal، LangGraph. RFC مستقبلي.

## طوابير منطقية

`lead_discovery`, `enrichment`, `scoring`, `outreach_draft`, `approval_surfacing`, `followup`, `reply_route`, `sample_factory`, `proposal_factory`, `payment_capture`, `delivery`, `retention`, `content`, `cs_handoff`.

## قواعد جوهرية

- كل وظيفة إما idempotent أو آمنة لإعادة التشغيل.
- الآثار الخارجية ما تبدأها وظيفة بمفردها أبدًا — تمر عبر طابور الموافقة.
- الوظائف اللي فشلت بعد لمسة خارج النظام لازم تنتج حدث في `event_store` مع `causation_id`.
- فشل عامل ثلاث مرات على نفس الوظيفة = تنبيه. تراكم طابور فوق العتبة = تنبيه. عدم وجود Action يومية = تنبيه.

## الربط بالتشغيل

- `core/queue/worker.py`, `tasks.py`, `weekly_self_improvement.py`, `cs_handoff_task.py`.
- `auto_client_acquisition/revenue_memory/event_store.py` (لمعرّفات السببية).
- `db/models.py::AuditLogRecord`, `BackgroundJobRecord`.

## روابط ذات صلة

- [`./REVENUE_FACTORY_RUNTIME_AR.md`](./REVENUE_FACTORY_RUNTIME_AR.md)
- [`../engineering/OBSERVABILITY_SLO_SYSTEM_AR.md`](../engineering/OBSERVABILITY_SLO_SYSTEM_AR.md)
- [`../control_plane/APPROVAL_CENTER_V2_AR.md`](../control_plane/APPROVAL_CENTER_V2_AR.md)
- `docs/SLO.md`

## بنود مفتوحة

- سجل مفاتيح Idempotency رسمي لكل طابور منطقي: غير موجود (انضباط على مستوى المهمة اليوم).
- المرحلة 3 ما هي التزام حالي.
- تنبيهات عمر الطابور: السقوف موثقة، لكن خط الأنابيب للتنبيه ما زال مفتوحًا.
