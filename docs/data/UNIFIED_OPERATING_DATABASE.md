# Unified Operating Database / قاعدة التشغيل الموحدة

## Purpose / الغرض

Create one operating source of truth for revenue, delivery, finance, trust, and productization.

إنشاء مصدر تشغيلي واحد للحقيقة للإيرادات والتسليم والمالية والثقة والمنتجة.

## Core Tables / الجداول الأساسية

### accounts / الحسابات
All discovered companies.

جميع الشركات المكتشفة.

### contacts / جهات الاتصال
Public business contact paths and decision-maker hypotheses.

مسارات الاتصال التجاري العامة وفرضيات صانعي القرار.

### signals / الإشارات
Market, sector, technology, hiring, funding, expansion, compliance, or buyer signals.

إشارات السوق، القطاع، التقنية، التوظيف، التمويل، التوسع، الامتثال، أو المشتري.

### lead_scores / تقييم العملاء
Fit score, priority, reason, and next action.

درجة الملاءمة، الأولوية، السبب، والإجراء التالي.

### suppression_list / قائمة الاستبعاد
Opt-outs, bad-fit, duplicate, risky, or do-not-contact records.

سجلات الانسحاب، عدم الملاءمة، التكرار، المخاطرة، أو عدم الاتصال.

### outreach_queue / طابور التواصل
Messages pending approval, draft, sent, or follow-up.

رسائل بانتظار الموافقة، مسودات، مُرسَلة، أو متابعة.

### conversation_log / سجل المحادثات
Replies, objections, routing, and next action.

الردود، الاعتراضات، التوجيه، والإجراء التالي.

### sample_queue / طابور العينات
Sample tasks triggered by positive replies.

مهام العينات المُحفَّزة بردود إيجابية.

### proposal_queue / طابور العروض
Proposal drafts, approval state, amount, and due date.

مسودات العروض، حالة الموافقة، المبلغ، وتاريخ الاستحقاق.

### payment_capture_queue / طابور تحصيل الدفع
Payment, PO, and written approval follow-ups.

متابعات الدفع، أمر الشراء، والموافقة الكتابية.

### delivery_queue / طابور التسليم
Paid or approved work ready for delivery.

العمل المدفوع أو المعتمد الجاهز للتسليم.

### retention_queue / طابور الاحتفاظ
Feedback, retainer, renewal, proof, referral.

تغذية راجعة، اشتراك شهري، تجديد، إثبات، إحالة.

### proof_library / مكتبة الإثباتات
Approved proof, anonymized proof, case study candidates.

إثبات معتمد، إثبات مجهول الهوية، مرشحون لدراسات الحالة.

### ai_audit_log / سجل تدقيق الذكاء
AI actions, prompts, outputs, approval class, evidence, model.

إجراءات الذكاء، الموجهات، المخرجات، فئة الموافقة، الدليل، النموذج.

### ceo_decision_log / سجل قرارات الرئيس التنفيذي
CEO decisions and outcomes.

قرارات الرئيس التنفيذي ونتائجها.

## Rule / القاعدة

The dashboard reads from this database. Workers write to this database. CEO acts from this database.

لوحة المعلومات تقرأ من هذه القاعدة. العاملون يكتبون إلى هذه القاعدة. الرئيس التنفيذي يتصرف من هذه القاعدة.

## See Also / مراجع

- [`SOVEREIGN_DATA_MODEL.md`](SOVEREIGN_DATA_MODEL.md) — نموذج البيانات السيادي الأساسي / underlying sovereign data model
- [`DATA_READINESS_STANDARD.md`](DATA_READINESS_STANDARD.md) — معيار جاهزية البيانات / data readiness standard
- [`../../schemas/unified_operating_database.schema.json`](../../schemas/unified_operating_database.schema.json) — JSON schema

## Owner / المسؤول

Sami / سامي (CEO)

## Version / الإصدار

v3.0 — 2026-05-23
