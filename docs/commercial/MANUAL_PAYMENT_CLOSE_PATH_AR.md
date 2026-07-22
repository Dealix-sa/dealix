# مسار الإغلاق والدفع اليدوي — Dealix

## الهدف

إغلاق أول Revenue Proof Sprint أو Diagnostic بطريقة واضحة، يدوية، خاضعة للموافقة، وقابلة للتدقيق؛ بدون تشغيل دفع حي تلقائي وبدون اعتبار الطلب أو النية إيرادًا.

هذا المسار يستخدم الموجود في الريبو ولا ينشئ tracker جديدًا:

- `dealix/config/phase_0_1_active_deal.yaml`
- `scripts/phase_0_1_close_helper.py`
- `docs/commercial/operations/evidence_events_tracker.csv`
- `dealix/commercial_ops/first_paid_tracker.py`
- `docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md`

## القاعدة التجارية

```text
REQUEST ≠ INVOICE ≠ REVENUE
```

- طلب البدء التجريبي ليس فاتورة.
- إرسال تعليمات الدفع أو الفاتورة لا يعني استلام الدفع.
- الإيراد لا يسجل إلا بعد دليل `payment_received` حقيقي.
- الإغلاق لا يكتمل إلا بعد `proof_pack_delivered` لنفس الشركة وبعد مزامنة KPI/CRM المطلوبة.

## حالات الإغلاق

```text
not_started
payment_instruction_drafted
payment_instruction_approved
invoice_sent
payment_pending
payment_received
proof_pack_delivered
closed_won
closed_lost
```

`closed_won` حالة اختيارية للتوثيق النهائي وليست شرطًا للاعتراف بالدفع. إذا سُجلت، يجب أن تأتي بعد `payment_received` و`proof_pack_delivered` لنفس الشركة؛ وإلا يفشل verifier.

الحالات الخارجية أو الحساسة تحتاج موافقة بشرية. لا يرسل هذا النظام فاتورة أو تعليمات دفع أو رسالة للعميل تلقائيًا.

## التسلسل التنفيذي

### 1. تثبيت الصفقة النشطة

عبّئ محليًا أو في فرع خاص خاضع للمراجعة:

- `active_deal.company`
- `active_deal.contact`
- `active_deal.offer_id`
- `active_deal.source_channel`
- `payment.amount_sar`
- `payment.method`

لا تضع IBAN أو أرقام بطاقات أو API keys أو أسرار دفع في الريبو.

### 2. اعتماد النطاق

قبل الدفع يجب وجود:

- Discovery مكتمل بالقدر المطلوب؛
- عرض واحد واضح؛
- نطاق مكتوب أو opt-in؛
- موافقة المؤسس على السعر والنطاق وتعليمات الدفع؛
- مصدر ومالك وموافقة على بيانات العميل.

### 3. تسجيل تعليمات الدفع/الفاتورة

بعد الإرسال اليدوي المعتمد فقط:

```bash
python scripts/phase_0_1_close_helper.py --event invoice_sent --notes "approved manual instruction sent"
```

يجب أن يحمل صف evidence اسم شركة حقيقية. الصفوف ذات الشركة الفارغة أو seed/internal placeholders لا تثبت إيرادًا.

### 4. تسجيل الدفع

بعد تحقق بنكي/مزود دفع مستقل فقط:

```bash
python scripts/phase_0_1_close_helper.py \
  --event payment_received \
  --amount-sar 499 \
  --notes "payment confirmed outside repository; reference retained in approved secure system"
```

لا تضع مرجع التحويل الكامل أو بيانات الحساب في `notes`. احتفظ بالدليل الحساس في نظام مالي معتمد، وسجل في الريبو إشارة غير حساسة فقط.

### 5. التسليم وProof Pack

ابدأ التنفيذ بعد النطاق والدفع، ثم سلّم Proof Pack فعليًا. بعد التسليم لنفس الشركة:

```bash
python scripts/phase_0_1_close_helper.py \
  --event proof_pack_delivered \
  --notes "proof pack delivered; internal path recorded without customer secrets"
```

### 6. فحص DoD

```bash
python scripts/phase_0_1_close_helper.py --event scope_requested --check-dod
python scripts/verify_first_paid_diagnostic_tracker.py --json
python scripts/commercial/verify_manual_close_path.py --json
```

لا تستخدم `scope_requested` مع `--check-dod` لإضافة حدث؛ وضع الفحص لا يكتب صفًا.

## قواعد same-company evidence

- `invoice_sent` لشركة A و`payment_received` لشركة B لا يصنعان close.
- `payment_received` لشركة A و`proof_pack_delivered` لشركة B لا يصنعان close.
- `proof_pack_delivered` بلا دفع سابق لنفس الشركة فشل حوكمة.
- `closed_won` قبل الدفع وProof لنفس الشركة فشل حوكمة.
- الصفوف الفارغة أو الداخلية أو أمثلة seed لا تعتبر عملاء مدفوعين.

## بيانات ممنوع تخزينها في الريبو

- IBAN كامل أو رقم حساب.
- أرقام بطاقات أو CVV.
- مفاتيح Moyasar/Stripe أو webhook secrets.
- صور إيصالات فيها بيانات شخصية.
- بيانات هوية أو ملفات عميل غير لازمة.
- أرقام تحويل كاملة إذا كانت حساسة.

## Definition of Done

- [ ] طلب البدء موصوف كـTEST/request وليس فاتورة.
- [ ] السعر والنطاق معتمدان بشريًا.
- [ ] `invoice_sent` مسجل لشركة حقيقية.
- [ ] `payment_received` مسجل بعد تحقق مستقل لنفس الشركة.
- [ ] Proof Pack سلّم فعليًا لنفس الشركة.
- [ ] `proof_pack_delivered` مسجل.
- [ ] أي `closed_won` مسجل بعد الدفع وProof لنفس الشركة.
- [ ] KPI/CRM متزامن.
- [ ] لا أسرار أو بيانات دفع حساسة في GitHub.
- [ ] verifier يمر.

## حدود الأتمتة

مسموح تلقائيًا:

- التحقق من الملفات والتسلسل.
- إعداد draft تعليمات أو رسالة.
- إنشاء Proof/DoD report داخلي.
- اكتشاف نقص evidence.

يحتاج موافقة صريحة:

- إرسال تعليمات الدفع أو فاتورة.
- التواصل باسم Dealix أو العميل.
- تسجيل أن الدفع مؤكد.
- إرسال Proof Pack خارجيًا.
- تفعيل بوابة دفع حية.
