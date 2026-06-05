# سياسة الاحتفاظ بالبيانات — Data Retention Policy — Dealix

> **القاعدة الحاكمة:** بيانات العميل **لا تُستخدم لتدريب النماذج** إطلاقًا (no customer data for model training).
> الاحتفاظ بقدر الحاجة فقط؛ عند الشك → **حذف**.
> هذه وثيقة سياسة **قابلة للإنفاذ**، وتُشغَّل بالكود لا بالنوايا.

الجمهور: المؤسس، التشغيل، DPO. النطاق: كل بيانات تدخل Dealix.
تكامل قائم: [`integrations/pdpl.py`](../../integrations/pdpl.py) (consent · erasure Art. 13 · export Art. 14 · audit Art. 18).

---

## 1. دورة حياة البيانة — Data Lifecycle

```
Intake → Consent → Source tracking → Deduplication → Retention window → Deletion / Export (DSR) → Quality score
```

1. **Intake — الإدخال:** كل بيانة تُسجَّل بفئتها وغرضها (purpose) لحظة الدخول. لا إدخال بلا غرض معلن.
2. **Consent — الموافقة:** للبيانات التي تتطلب موافقة (تسويق/حساسة)، تُلتقط الموافقة وتُربط بالسجل قبل أي معالجة.
3. **Source tracking — تتبّع المصدر:** لكل بيانة `source_ref` يثبت من أين أتت ووفق أي أساس قانوني. لا بيانات يتيمة المصدر.
4. **Deduplication — إزالة التكرار:** الدمج على مفتاح ثابت (account/contact) لمنع تعدّد السجلات وتضخّم الاحتفاظ.
5. **Retention window — نافذة الاحتفاظ:** كل فئة لها مدة محددة (الجدول أدناه)، يفرضها job مجدول.
6. **Deletion / Export — الحذف/التصدير:** عبر طلب صاحب البيانات (Data Subject Request) بـ SLA محدد.
7. **Quality score — درجة الجودة:** كل مجموعة بيانات تُقيَّم (اكتمال · حداثة · صحة المصدر · إثبات الموافقة).

---

## 2. مدد الاحتفاظ حسب الفئة — Retention by Category

| فئة البيانات (Category) | الغرض | مدة الاحتفاظ (Retention) | محفّز الحذف |
|---|---|---|---|
| **بيانات الـ lead/البحث** (lead & research data) | targeting مبني على دليل | 12 شهرًا من آخر تفاعل | خمول > 12 شهرًا → حذف/anonymise |
| **بيانات تسليم العميل** (customer delivery data) | تنفيذ الخدمة المتعاقد عليها | مدة العقد + 7 سنوات (التزام ضريبي) | نهاية العقد + 7 سنوات |
| **بيانات الإثبات** (proof data — proof pack) | إثبات التسليم للعميل | مدة العقد + 24 شهرًا | انقضاء النافذة |
| **البيانات المالية** (financial / payments) | محاسبة + التزام نظامي | 10 سنوات | 10 سنوات من العملية |
| **سجلات التدقيق** (audit logs) | أمن + حوكمة | 24 شهرًا | rolling cron |
| **حمولات webhook / تشغيلية** | موثوقية + تتبّع | 90 يومًا | rolling cron |

البيانات الحساسة (national ID, health, biometric, religious, political): **Dealix لا تجمعها**. إن وصلت سهوًا → حذف خلال 7 أيام مع قيد.

> EN: Lead/research = 12 mo. Delivery = contract + 7 yr. Proof = contract + 24 mo. Financial = 10 yr. When in doubt, delete.

الجدول التشغيلي المفصّل (jobs, schema enforcement): [`../ops/PDPL_RETENTION_POLICY.md`](../ops/PDPL_RETENTION_POLICY.md).

---

## 3. طلبات الحذف/التصدير — Data Subject Requests (DSR)

صاحب البيانات قد يطلب: **وصول / نسخة (export)**، **تصحيح**، **حذف (erasure)**، **تقييد**، **سحب موافقة**.

### سير العمل — Workflow

1. **استلام** عبر قناة موثّقة (`privacy@dealix.sa` أو نموذج الخصوصية).
2. **التحقق من الهوية (identity verification):** لا تُنفَّذ DSR قبل التحقق. لا endpoint عام مجهول.
3. **التنفيذ:** التصدير عبر سكربت read-only → ZIP مشفّر؛ الحذف بـ **dry-run أولًا** ثم تنفيذ (فئة **A5** — راجع [`HUMAN_APPROVAL_POLICY.md`](HUMAN_APPROVAL_POLICY.md)).
4. **التحقق البعدي:** إعادة التصدير بعد الحذف يجب أن تُرجِع نتيجة فارغة.
5. **التسجيل:** كل DSR يُقيَّد (request id · type · decision · response date · evidence).

### SLA

- **30 يومًا** من الاستلام (PDPL Art. 12)، قابلة للتمديد 30 يومًا للطلبات المعقّدة مع إشعار صاحب البيانات.

تفاصيل القناة والسكربت: [`../ops/PDPL_RETENTION_POLICY.md`](../ops/PDPL_RETENTION_POLICY.md) · [`../PDPL_DATA_SUBJECT_REQUEST_SOP.md`](../PDPL_DATA_SUBJECT_REQUEST_SOP.md).

---

## 4. لا تدريب على بيانات العميل — No Model Training

**بيانات العميل (محتوى التسليم، بيانات الأفراد، الإثبات) لا تُغذّى لأي تدريب نماذج، لا fine-tuning، لا embeddings للتدريب.** أي استثناء يتطلب موافقة صريحة موثّقة من العميل (فئة **A4**) — والافتراض دائمًا **لا**.

> EN: Customer data is never used for model training, fine-tuning, or training embeddings. The default is always no.

---

## 5. درجة جودة البيانات — Data Quality Score

كل مجموعة بيانات تُقيَّم على: **الاكتمال** · **الحداثة (recency)** · **صحة المصدر** · **إثبات الموافقة** · **خلوّها من تكرار**. البيانات منخفضة الجودة تُحذف بدل الاحتفاظ بها.

---

## 6. الإنفاذ — Enforcement

- الاحتفاظ يُفرض بـ jobs مجدولة، يراجع DPO سجلّاتها ربع سنويًا.
- أي بيانة بلا مصدر أو بلا غرض = تُحذف.
- أي استخدام لبيانات عميل في تدريب = **حادثة حوكمة** كبرى.
- KPI: **صفر بيانات محتفَظ بها خارج المدة المعتمدة**.

---

## روابط مرجعية — Related

- [`PRIVACY_AND_PDPL_READINESS.md`](PRIVACY_AND_PDPL_READINESS.md)
- [`HUMAN_APPROVAL_POLICY.md`](HUMAN_APPROVAL_POLICY.md)
- [`EXTERNAL_ACTIONS_POLICY.md`](EXTERNAL_ACTIONS_POLICY.md)
- [`../ops/PDPL_RETENTION_POLICY.md`](../ops/PDPL_RETENTION_POLICY.md)
- [`../PDPL_DATA_SUBJECT_REQUEST_SOP.md`](../PDPL_DATA_SUBJECT_REQUEST_SOP.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
