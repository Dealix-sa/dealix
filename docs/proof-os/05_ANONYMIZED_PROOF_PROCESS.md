# عملية الإثبات المجهّل | Anonymized Proof Process

## الغرض | Purpose

**عربي:** عملية منهجية لإخفاء هوية العميل وبياناته الحساسة قبل أي مشاركة، مع الحفاظ على صدق النتائج وقابليتها للتحقق. الهدف حماية العميل والامتثال لأنظمة حماية البيانات.

**English:** A systematic process to anonymize client identity and sensitive data before any sharing, while preserving honest, verifiable results. The goal is to protect the client and comply with data-protection regulations.

---

## خطوات الإخفاء | Anonymization Steps

1. **تحديد المعرّفات | Identify identifiers:** الأسماء، الشعارات، الروابط، الأرقام الفريدة.
2. **الاستبدال | Replace:** «عميل في قطاع X»، «مدينة في المنطقة Y».
3. **التعميم | Generalize:** تحويل الأرقام الدقيقة إلى نطاقات.
4. **إزالة البيانات الوصفية | Strip metadata:** من الصور والملفات.
5. **مراجعة مزدوجة | Double review:** فريق ثم مؤسّس.

---

## جدول المعالجة | Handling Table

| نوع البيانات Data Type | الإجراء Action |
|---|---|
| اسم العميل Client name | استبدال بفئة قطاع |
| الشعار/العلامة Logo/Brand | إزالة |
| أرقام دقيقة Exact figures | تحويل إلى نطاق |
| بيانات شخصية PII | إزالة كاملة |
| أسرار/مفاتيح Secrets/Keys | إزالة كاملة |
| روابط داخلية Internal links | إزالة |

---

## قائمة التحقق من الإخفاء | Anonymization Checklist

- [ ] لا اسم عميل أو شعار ظاهر.
- [ ] لا بيانات شخصية (PII).
- [ ] لا أسرار أو مفاتيح API.
- [ ] الأرقام موثّقة ومُعمّمة عند الحاجة.
- [ ] لا بيانات وصفية مخفية في الملفات.
- [ ] مراجعة مزدوجة مكتملة.

---

## الامتثال | Compliance

- متوافق مع مبادئ حماية البيانات الشخصية (PDPL-aware).
- يُسجَّل مستوى الإذن (انظر `04_CLIENT_PERMISSION_RULES.md`).

---

## قواعد السلامة | Safety Guardrails

- الإخفاء افتراضي، والكشف استثناء بموافقة.
- لا إرسال آلي ولا تجريف.
- الذكاء الاصطناعي يجهّز، المؤسّس يعتمد، الإجراء يدوي.
