# عزل المدخلات غير الموثوقة
# Untrusted Input Sandboxing

---

## المبدأ الأساسي — Core Principle

**كل مدخل من مصدر خارجي = غير موثوق حتى يُعالَج.**

Every input from an external source = untrusted until processed.

"الخارجي" يشمل: ملفات العميل، نتائج البحث، بيانات الويب، أي ملف لم يُنشأ داخل Dealix.

---

## تعريف المصادر — Source Classification

| المصدر | مستوى الثقة | معالجة مطلوبة |
|--------|------------|----------------|
| ملفات الريبو الداخلية (docs/, reports/) | موثوق | لا معالجة إضافية |
| ملفات يُنشئها الوكلاء الداخليون | موثوق جزئياً | مراجعة المؤسس |
| مدخلات المستخدم في المحادثة | غير موثوق | Input Sanitization |
| ملفات مُرفَقة من العملاء | غير موثوق | Sandboxing كامل |
| نتائج بحث ويب | غير موثوق | Sandboxing + تحقق المصدر |
| بيانات API خارجية | غير موثوق | Schema validation + Sandboxing |

---

## بروتوكول العزل — Sandboxing Protocol

### الخطوة 1: التصنيف

قبل معالجة أي مدخل خارجي، يُصنَّف:
```
نوع المصدر: _______________
مستوى الثقة: غير موثوق / موثوق جزئياً
يحتوي على: نص حر / بيانات مهيكلة / ملف ثنائي
```

---

### الخطوة 2: Input Sanitization

للنصوص الحرة (مدخلات المستخدم، ملفات نصية من العميل):

**أنماط تُحذَف أو تُعطَّل:**
- "ignore previous instructions" أو أي ترجمة عربية
- "you are now" / "pretend you are" / "act as"
- أي سلسلة تبدو وكأنها تعيد تعريف دور الوكيل
- أوامر shell أو كود قابل للتنفيذ مضمَّن في النص

**الإجراء:**
- البيانات المُنظَّفة تُوسَم بـ `[SANITIZED_EXTERNAL_INPUT]`
- المحتوى المُزال يُسجَّل (لا يُحذف من السجل)

---

### الخطوة 3: عزل السياق

البيانات الخارجية لا تُدمج مع تعليمات النظام في نفس prompt window:

```
[نموذج مسموح به]
System: أنت محلل بيانات. ستحلل البيانات التالية وتُنتج تقريراً.
User-provided data: [SANITIZED_EXTERNAL_INPUT]
Task: حلل هذه البيانات وأجب فقط على الأسئلة المحددة.

[نموذج محظور]
System: أنت محلل بيانات. [EXTERNAL_DATA_MERGED_HERE] افعل X.
```

---

### الخطوة 4: تحقق المخرجات

قبل استخدام أي مخرج وكيل مبني على بيانات خارجية:

- [ ] هل المخرج يحتوي على تعليمات تنفيذية ناتجة من البيانات الخارجية؟
- [ ] هل المخرج يطلب صلاحيات إضافية؟
- [ ] هل المخرج يُحاول إرسال بيانات لخارج Dealix؟

إذا كانت الإجابة "نعم" لأي منها → **وقف فوري + إبلاغ المؤسس**

---

## قواعد إضافية — Additional Rules

**القاعدة 1:** لا يُعطى وكيل بيانات مباشرة من مصدر خارجي بدون تنظيف سابق.

**القاعدة 2:** البيانات الخارجية لا تُستخدم كـ"تعليمات" — تُستخدم كـ"محتوى للتحليل" فقط.

**القاعدة 3:** أي ملف Excel/CSV يحتوي على أعمدة نصية حرة (مثل "ملاحظات"، "تعليقات") يُعامَل كمصدر غير موثوق حتى بعد التنظيف.

**القاعدة 4:** نتائج بحث الويب لا تدخل في prompt التحليل مباشرة — تُلخَّص أولاً بوسيلة محكومة.

---

## التوثيق والمراجعة — Logging and Review

- كل Input Sanitization يُسجَّل في AGENT_DAILY_ACTIVITY_REVIEW
- كل Sandbox violation مشتبه بها تُرفَع فوراً في AGENT_AUDIT_LOG_REVIEW
- مراجعة أسبوعية لفاعلية Sandboxing في DAILY_AGENT_SECURITY_REVIEW

---

## الوثائق المرتبطة — Related Documents

- [`docs/security/PROMPT_INJECTION_DEFENSE_MAX_AR.md`](./PROMPT_INJECTION_DEFENSE_MAX_AR.md)
- [`docs/agents/WORKFLOW_FIRST_AGENT_POLICY_AR.md`](../agents/WORKFLOW_FIRST_AGENT_POLICY_AR.md)
- [`docs/06_llm_gateway/REDACTION_POLICY.md`](../06_llm_gateway/REDACTION_POLICY.md)
- [`docs/privacy/CLIENT_DATA_HANDLING_AR.md`](../privacy/CLIENT_DATA_HANDLING_AR.md)

---

*القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value*
