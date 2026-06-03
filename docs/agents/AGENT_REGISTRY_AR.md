# سجل الوكلاء — Agent Registry
# Agent Registry — Dealix Governed AI Agents

---

## المبدأ — Principle

كل وكيل في Dealix مُسجَّل هنا. لا يعمل وكيل غير مُسجَّل. كل وكيل له دور واحد، صلاحيات محددة، ومالك مسؤول.

Every agent in Dealix is registered here. No unregistered agent operates. Each agent has one role, defined permissions, and a responsible owner.

مرجع الصلاحيات الكامل: [`docs/agents/AGENT_PERMISSION_MATRIX_AR.md`](./AGENT_PERMISSION_MATRIX_AR.md)

---

## وكلاء النظام الأساسيون — Core System Agents

| الوكيل | الغرض | المدخلات | المخرجات | مستوى الصلاحية | المالك |
|--------|-------|---------|---------|----------------|--------|
| **dealix-pm** | إدارة المشروع: تتبع التقدم، إنتاج ملخصات الحالة | ملفات التقدم، سجلات الأنشطة | ملخصات حالة، قوائم إجراءات | Advise | المؤسس |
| **dealix-engineer** | الدعم التقني: مراجعة الكود، التحقق من الجودة، تشخيص الأخطاء | ملفات الكود، سجلات الأخطاء | تقارير مراجعة، اقتراحات إصلاح | Advise | المؤسس |
| **dealix-content** | إنتاج المحتوى: مسودات المستندات، القوالب، الرسائل | الموضوع، الجمهور، الإرشادات | مسودات محتوى (تحتاج موافقة) | Advise | المؤسس |
| **dealix-delivery** | دعم التسليم: تتبع حالة Sprints، تحديث لوائح التسليم | بيانات Pipeline، قوائم التحقق | تقارير حالة، تنبيهات اختناق | Act with Approval | المؤسس |
| **dealix-sales** | دعم المبيعات: إعداد مسودات المقترحات، تحليل قائمة الحسابات | بيانات الحساب، النطاق المُدخَل | مسودات مقترحات، ملاحظات Call Brief | Advise | المؤسس |

---

## وكلاء العمليات التجارية — Commercial Operations Agents

| الوكيل | الغرض | المدخلات | المخرجات | مستوى الصلاحية | المالك |
|--------|-------|---------|---------|----------------|--------|
| **Data Intelligence Agent** | تحليل بيانات العملاء لإنتاج Account Pack | ملفات بيانات العميل (معالجة مسبقاً) | تقرير Account Intelligence، Need Fit Score | Observe + Advise | المؤسس |
| **Outreach Draft Agent** | صياغة مسودات رسائل التواصل | بيانات الحساب، القطاع، السياق | مسودات رسائل (تحتاج موافقة المؤسس قبل أي إرسال) | Advise فقط | المؤسس |
| **Proposal Draft Agent** | إعداد مسودات Mini Proposal | بيانات الحساب، النطاق المقترح، السعر | مسودة Mini Proposal (تحتاج موافقة المؤسس) | Advise فقط | المؤسس |
| **Delivery Review Agent** | مراجعة جودة مخرجات Sprint قبل تسليمها للعميل | ملفات المخرجات، معيار الجودة | تقرير مراجعة، قائمة ملاحظات | Observe + Advise | المؤسس |
| **Security Audit Agent** | مراجعة أنشطة الوكلاء بحثاً عن أي انتهاك للصلاحيات | سجلات الأنشطة اليومية | تقرير أمني، تنبيهات انتهاك | Observe فقط | المؤسس |

---

## قواعد التسجيل — Registration Rules

1. **تسجيل مطلوب قبل التشغيل:** أي وكيل جديد يُضاف لهذا الجدول ويحصل على موافقة المؤسس قبل أي استخدام.
2. **دور واحد فقط:** كل وكيل مُقيَّد بالغرض المحدد في الجدول. لا يُفوَّض بمهام خارج دوره.
3. **مستوى الصلاحية لا يُتجاوز:** وكيل بمستوى Advise لا يُنفَّذ إجراؤه بدون موافقة المؤسس.
4. **المالك مسؤول:** المالك يراجع نشاط الوكيل يومياً في `reports/agents/AGENT_DAILY_ACTIVITY_REVIEW.md`.

---

## مستويات الصلاحية — Permission Levels Summary

| المستوى | الوصف | الإجراء المطلوب |
|---------|-------|----------------|
| **Observe** | قراءة فقط، لا كتابة، لا اقتراح | لا شيء — مراقبة فقط |
| **Advise** | يقترح، يكتب مسودات، لا ينفذ | موافقة المؤسس قبل أي إجراء |
| **Act with Approval** | ينفذ بعد موافقة صريحة، يسجل كل خطوة | موافقة مكتوبة + تسجيل في السجل |
| **Act Autonomously** | محظور في الإنتاج | بيئات اختبار معزولة فقط |

التفاصيل الكاملة: [`docs/agents/AGENT_PERMISSION_MATRIX_AR.md`](./AGENT_PERMISSION_MATRIX_AR.md)

---

## حالة الوكلاء — Agent Status

| الوكيل | الحالة | تاريخ آخر مراجعة | ملاحظات |
|--------|--------|-------------------|---------|
| dealix-pm | نشط | — | راجع `.claude/agents/dealix-pm.md` |
| dealix-engineer | نشط | — | راجع `.claude/agents/dealix-engineer.md` |
| dealix-content | نشط | — | راجع `.claude/agents/dealix-content.md` |
| dealix-delivery | نشط | — | راجع `.claude/agents/dealix-delivery.md` |
| dealix-sales | نشط | — | راجع `.claude/agents/dealix-sales.md` |
| Data Intelligence Agent | قيد الإعداد | — | يتطلب schema validation |
| Outreach Draft Agent | قيد الإعداد | — | محظور الإرسال المباشر |
| Proposal Draft Agent | قيد الإعداد | — | يتطلب موافقة المؤسس |
| Delivery Review Agent | قيد الإعداد | — | — |
| Security Audit Agent | قيد الإعداد | — | Observe فقط |

---

## الوثائق المرتبطة — Related Documents

- [`docs/agents/AGENT_PERMISSION_MATRIX_AR.md`](./AGENT_PERMISSION_MATRIX_AR.md)
- [`docs/agents/WORKFLOW_FIRST_AGENT_POLICY_AR.md`](./WORKFLOW_FIRST_AGENT_POLICY_AR.md)
- [`reports/agents/AGENT_DAILY_ACTIVITY_REVIEW.md`](../../reports/agents/AGENT_DAILY_ACTIVITY_REVIEW.md)
- [`reports/agents/AGENT_PERMISSION_AUDIT.md`](../../reports/agents/AGENT_PERMISSION_AUDIT.md)
- [`dealix/masters/constitution.md`](../../dealix/masters/constitution.md)

---

*القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value*
