# DAILY AGENT SECURITY REVIEW
# المراجعة الأمنية اليومية للوكلاء

> يُعبَّأ يومياً (17:00). مرجع: `docs/security/PROMPT_INJECTION_DEFENSE_MAX_AR.md`

---

## التاريخ — Date: [YYYY-MM-DD]

---

## فحص الحالة الأمنية — Security Status Check

### Input Sanitization
- [ ] تم تفعيل Input Sanitization لكل الوكلاء النشطة اليوم
- [ ] لا مدخلات خارجية مرّت بدون تنظيف

### Sandboxing
- [ ] بيانات العملاء المُعالَجة اليوم مرّت بـ Sandboxing
- [ ] لا بيانات عميل في prompts مباشرة

### External Communications
- [ ] كل رسالة خارجية أُرسلت اليوم لها موافقة المؤسس
- [ ] لا إرسال مباشر من أي وكيل

### Permission Boundaries
- [ ] لا وكيل تجاوز صلاحياته المُعرَّفة اليوم
- [ ] سجلات النشاط مكتملة لكل وكيل

---

## الحوادث الأمنية اليوم — Security Incidents Today

*(يُعبَّأ فقط عند وجود حوادث)*

| الوكيل | نوع الحادثة | الوصف | الإجراء | الحالة |
|--------|-----------|-------|---------|--------|
| — | — | — | — | مُغلَق / مفتوح |

---

## نتيجة المراجعة — Review Outcome

**حالة الأمان اليوم:**
- [ ] كل الفحوص اجتازت — لا إجراء مطلوب
- [ ] تحذير بسيط — مراجعة في الأسبوع القادم
- [ ] حادثة تحتاج إجراء فوري → تفاصيل أدناه

**ملاحظات:**
—

---

## الوثائق المرتبطة

- [`reports/security/AGENT_AUDIT_LOG_REVIEW.md`](./AGENT_AUDIT_LOG_REVIEW.md)
- [`reports/agents/AGENT_DAILY_ACTIVITY_REVIEW.md`](../agents/AGENT_DAILY_ACTIVITY_REVIEW.md)
- [`docs/security/PROMPT_INJECTION_DEFENSE_MAX_AR.md`](../../docs/security/PROMPT_INJECTION_DEFENSE_MAX_AR.md)

---

*للاستخدام الداخلي فقط — Internal use only*
