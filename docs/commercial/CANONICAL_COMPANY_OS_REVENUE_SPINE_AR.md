# Dealix Canonical Company OS — Revenue Spine

## القرار التنفيذي

Dealix يجب أن يعمل من خلال مسار تشغيل يومي واحد فقط. لا توجد أنظمة Company OS متوازية، ولا Approval Queues متعددة، ولا Workflows مجدولة تتنافس على نفس المهمة.

المسار القانوني هو:

```text
Company Brain
→ Real/Warm Target Intake
→ Opportunity Graph
→ Offer Match
→ Internal Action Queue
→ External Approval Queue
→ Evidence Check
→ Revenue State
→ Proof Log
→ Daily Command
```

## الهدف التجاري الأول

إغلاق أول **Revenue Proof Sprint بقيمة 499 ريال** مع عميل حقيقي دافئ أو وارد أو محال أو مستهدف معتمد.

لا يعتبر أي مبلغ إيرادًا إلا بعد وجود حدث حقيقي:

```text
payment_received
```

ولا تعتبر الصفقة مغلقة ومثبتة إلا بعد:

```text
payment_received
+ proof_pack_delivered
+ CRM/KPI synchronization
```

## سلم التحويل التجاري

1. Revenue Proof Sprint — 499 SAR
2. Revenue Command Pilot
3. Revenue Command Room — monthly retainer
4. Saudi Market Access Sprint
5. AI Company OS Setup
6. B2G Readiness Sprint
7. Partner / Distributor Desk

## مخرجات التشغيل اليومي

```text
reports/canonical_company_os/latest.json
reports/canonical_company_os/latest.md
reports/canonical_company_os/YYYY-MM-DD/bundle.json
reports/canonical_company_os/YYYY-MM-DD/opportunity_graph.csv
reports/canonical_company_os/YYYY-MM-DD/action_queue.csv
reports/canonical_company_os/YYYY-MM-DD/approval_queue.csv
reports/canonical_company_os/YYYY-MM-DD/revenue_status.json
reports/canonical_company_os/YYYY-MM-DD/proof_log.json
reports/canonical_company_os/YYYY-MM-DD/daily_command.md
```

## قواعد البيانات والأهداف

- عند وجود `data/self_operating_company_os/targets.json` يستخدم النظام البيانات الحقيقية الموجودة فيه.
- عند غياب الملف يعمل النظام بوضع `safe_seed_only` للتوضيح الداخلي فقط.
- الأمثلة ليست عملاء حقيقيين ولا يجوز إرسال أي رسالة لها.
- لا تستخدم بيانات مرضى أو معلومات شخصية حساسة.

## قواعد الموافقة

مسموح تلقائيًا:

- البحث والتحليل.
- ترتيب الفرص.
- إنشاء مسودات.
- بناء Action Queue وApproval Queue.
- تحديث Proof Log.
- إنشاء تقارير داخلية وPRs واختبارات.

تحتاج موافقة أو صلاحية موصل مباشرة:

- إرسال خارجي.
- نشر.
- تحصيل دفع.
- تعديل أسرار الإنتاج.
- تغيير Production.

## قواعد الأمان

- لا Cold WhatsApp.
- لا Mass LinkedIn automation.
- لا إيراد مختلق.
- لا ادعاء ROI مضمون.
- لا ادعاء وصول حكومي.
- لا طباعة أو تخزين أسرار.
- لا إرسال تلقائي من هذا الـRunner.
- لا تشغيل Production mutation من Workflow اليومي.

## تشغيل محلي

```bash
python scripts/commercial/run_canonical_company_os.py --limit 50
python scripts/verify_first_paid_diagnostic_tracker.py --json
python -m pytest tests/test_canonical_company_os.py -q --no-cov
```

## Definition of Done

- Workflow مجدول واحد فقط للـCompany OS.
- Runner واحد يخرج الأولويات والفرص والإجراءات والموافقات والإثبات وحالة الإيراد.
- لا احتساب إيراد قبل دليل دفع حقيقي.
- لا Closed status قبل التسليم والإثبات والمزامنة.
- أي قدرات تفاوض أو Model Routing أو Owner Value تضاف كوحدات داخل هذا المسار، لا كأنظمة مستقلة.
