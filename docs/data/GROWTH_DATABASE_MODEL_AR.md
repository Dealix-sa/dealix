# نموذج قاعدة بيانات النمو

> النسخة الإنجليزية القانونية: [`GROWTH_DATABASE_MODEL.md`](./GROWTH_DATABASE_MODEL.md). هذه النسخة العربية ترافقها ولا تستبدلها عند الاختلاف.

## مرجع الدوكترين
- الالتزامات: #2 (لا ادعاء قيمة بدون مصدر دليل)، #3 (لا وصول تشغيلي عبر المستأجرين)، #5 (لا ادعاء يتجاوز مستوى الدليل).
- القرارات المثبّتة: الموافقة-أولًا للفعل الخارجي، سكربتات التحقق على لوحة التحكم تكون مانعة للإصدار.

## الغرض

تحديد الطبقات الرسمية للبيانات التي تشغّل مصنع الإيرادات. "خط الأنابيب" (Pipeline) ليس قاعدة البيانات؛ هو فقط الجزء النشط تجاريًا من سوق أكبر يكتشفه Dealix باستمرار.

## الطبقات المفاهيمية

1. سوق شامل (Market Universe) — كل حساب قابل للاكتشاف.
2. قاعدة ذكاء العملاء (Lead Intelligence) — حسابات بحثت ووُضع لها تصنيف.
3. خط الأنابيب (Pipeline) — تفاعل تجاري نشط.
4. طابور التواصل (Outreach Queue) — رسائل معتمدة أو بانتظار الموافقة.
5. سجل المحادثات (Conversation Log) — كل رد وقرار التوجيه الناتج عنه.
6. طابور الفرص (Opportunity) — عينات، عروض، تحصيل دفع.
7. طابور العملاء (Client) — التسليم، الاحتفاظ، الإثبات، الإحالة، التوسع.

السجل الواحد ينتقل بين طبقات، وكل انتقال يُسجّل.

## الجداول الموجودة فعلًا

- قاعدة الذكاء: `LeadRecord` في `db/models.py`.
- التصنيف: `LeadScoreRecord`.
- طوابير التواصل: `OutreachQueueRecord`, `GmailDraftRecord`, `LinkedInDraftRecord`.
- الإيقاف: `SuppressionRecord`.
- سجل التدقيق: `AuditLogRecord`.
- أحداث الإيرادات (إلحاق فقط): `RevenueEventRecord` في `db/models_revenue_events.py`.
- المهام الخلفية: `BackgroundJobRecord`.
- الإيجار/الصلاحيات: `TenantRecord`, `UserRecord`, `RoleRecord`.
- المدفوعات: `db/migrations/versions/20260512_005_payments_table.py`.
- الهجرات: `db/migrations/versions/`.

## القواعد الجوهرية

- "خط الأنابيب" مشتق من قاعدة الذكاء، ما هو مصدر أصلي.
- ما ينكتب سجل تواصل لحساب موجود في `SuppressionRecord`.
- أي فعل خارجي يحمل مرجع `AuditLogRecord`.
- الـ joins عبر المستأجرين ممنوعة في الـ ORM والـ Policy layer.
- مجاري الأحداث (`RevenueEventRecord`) هي مصدر الحقيقة للي حصل فعلًا خارجيًا.

## الربط بالتشغيل القائم

- `db/models.py`, `db/session.py`.
- `auto_client_acquisition/revenue_memory/event_store.py`.
- `auto_client_acquisition/revenue_memory/projections.py`.
- `core/memory/revenue_memory.py`.
- `auto_client_acquisition/lead_inbox.py`.

## روابط ذات صلة

- [`../runtime/REVENUE_FACTORY_RUNTIME_AR.md`](../runtime/REVENUE_FACTORY_RUNTIME_AR.md)
- [`../trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM_AR.md`](../trust/CONSENT_SUPPRESSION_LAWFUL_BASIS_SYSTEM_AR.md)
- [`../control_plane/APPROVAL_CENTER_V2_AR.md`](../control_plane/APPROVAL_CENTER_V2_AR.md)
- `docs/transformation/01_doctrine_lock.md`

## بنود مفتوحة

- جداول مفاهيمية (market_accounts, conversation_log, sample_queue, retention_queue) ما زالت موزّعة في ملفات وموديولات.
- قاموس بيانات رسمي يربط كل عمود بطبقته غير موجود.
- توحيد JSONL في `lead_inbox.py` مع `LeadRecord` في قاعدة البيانات: ما زال مفتوحًا.
