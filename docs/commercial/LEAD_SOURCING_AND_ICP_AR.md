# جمع العملاء المحتملين وتقييم المطابقة (Lead Sourcing & ICP)

## جمع العملاء المحتملين

### مصادر مسموحة فقط

```
client_provided     ملفات CSV/JSON من العميل
public_website      صفحات تواصل عامة مسموحة
public_directory    أدلة عامة مسموحة
partner             عبر شريك
referral            إحالة
inbound_form        نموذج وارد
```

### القواعد

- **`source_url` إلزامي.** أي حساب بلا مصدر يُعلَّم `unverified` و**يُمنع
  الإرسال إليه** (`is_send_ready=false`). لا نخترع بيانات أبداً.
- المصدر غير المسموح ⇒ `rejected`.
- العميل المستبعَد (`opted_out` / `email_opt_out`) ⇒ غير قابل للتواصل.

### حالة التحقق والتواصل

```
verification_status: unverified | verified | rejected
contactability_status: unknown | contactable | blocked | opted_out
```

## تقييم المطابقة (ICP Scoring)

درجة من 0 إلى 100 شفّافة وقابلة للتدقيق، مبنية على إشارات موزونة:

| الإشارة | الوزن الافتراضي |
|---------|------------------|
| مطابقة القطاع | 22 |
| الموقع | 12 |
| إشارة الألم | 20 |
| إمكانية التواصل | 16 |
| وجود المصدر | 14 |
| مطابقة الحركة | 10 |
| إشارة الإلحاح | 6 |

ثم خصم حسب المخاطر: `high=-18، medium=-6، low=0`.

الطبقات: `A ≥ 70`، `B ≥ 50`، `C ≥ 30`، `D < 30`.

كل نتيجة ترجع مع `breakdown` و`rationale` لتبرير الدرجة في غرفة القيادة.
القواعد قابلة للتهيئة عبر `data/commercial/icp_rules.sample.json`.

## اختيار القناة

`email`, `whatsapp`, `linkedin_manual`, `phone`, `partner_referral`,
`website_form`

- واتساب يتطلب opt-in.
- LinkedIn يدوي.
- الهاتف مهام يدوية.
- البريد مباشر فقط بعد الموافقة ووجود إلغاء الاشتراك.
