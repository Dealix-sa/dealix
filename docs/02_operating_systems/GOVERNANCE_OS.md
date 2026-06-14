# 10 — Governance OS — نظام الحوكمة

**الحالة — Status: `LIVE` (الموافقة-أولًا جوهر المنتج اليوم؛ السجلات الكاملة قيد التشغيل)**

> الحوكمة ليست زينة. هي خندق تنافسي (competitive moat). الذي يضع الموافقة قبل الإجراء يكسب ثقة السوق السعودي.

## الغرض — Purpose

Governance OS هو طبقة الثقة: الحارس الذي يقف بين كل قدرة وكل إجراء خارجي. لا مسودّة تصبح إرسالًا، ولا ادعاء يصبح إثباتًا، إلا بعبور بوّابة. هذه الطبقة **LIVE اليوم** لأن مبدأ «الموافقة أولًا (approval-first)» مفروض في صميم التسليم الحالي.

## القيمة — Value

- يحوّل الحوكمة من مخاطرة إلى ميزة بيع.
- يمنع كل إجراء غير آمن قبل وقوعه، لا بعده.
- يبني سجلًا تدقيقيًا (audit log) قابلًا للعرض على العميل والجهة التنظيمية.

## سياق خارجي — External Context

سياق «التنظيم المرن (soft regulation)» في الخليج يترك مساحة تفسير واسعة. *(سياق خارجي للتأطير.)* الفرصة: دِيليكس **يُشغِّل الحوكمة داخل المنتج** (operationalize) بدل انتظار إلزام تنظيمي — فيصبح المعيار العملي.

## Approval Classes — فئات الموافقة (A0–A5)

| الفئة | الوصف | الموافقة |
|---|---|---|
| **A0** | مسودّة داخلية (internal draft) | تلقائي |
| **A1** | تحليل داخلي (internal analysis) | تلقائي |
| **A2** | مسودّة موجّهة للعميل (customer-facing draft) | **موافقة المؤسس** |
| **A3** | إجراء خارجي (external action) | **موافقة المؤسس** |
| **A4** | قانوني/مالي/أمني (legal/financial/security) | **موافقة المؤسس** |
| **A5** | تدميري (destructive) | **موافقة المؤسس + تأكيد مزدوج** |

**القاعدة:** كل ما هو **A2 فأعلى يحتاج موافقة المؤسس** قبل التنفيذ.

## القدرات — Capabilities

- بوّابات الموافقة (approval gates) وضبط الإجراء الخارجي.
- سياسة لا-سبام، لا تزييف إثبات، لا إرسال تلقائي، لا ادعاءات غير آمنة.
- سجلات تدقيق (audit logs) وموافقة بشرية إلزامية.

## البوابات والقواعد — Gates / Rules

- **لا إرسال تلقائي · لا واتساب جماعي · لا outreach بالجملة.**
- **لا إثبات مزيّف · لا ادعاء إيراد مضمون.**
- **لا إجراء خارجي موجّه للعميل بلا موافقة المؤسس.**
- **كل إجراء A2+ يُسجَّل** قبل وبعد الموافقة.

## الاتصالات — Connections to other OS

- **Agent OS** — كل وكيل يحمل Approval Class: [AGENT_OS.md](AGENT_OS.md)
- **Finance OS** — كل إجراء مالي A4: [FINANCE_OS.md](FINANCE_OS.md)
- **Data OS** — الحذف/التصدير A4: [DATA_OS.md](DATA_OS.md)
- سياسات الحوكمة الفعلية: [../05_governance_os/APPROVAL_POLICY.md](../05_governance_os/APPROVAL_POLICY.md) · [../05_governance_os/RUNTIME_GOVERNANCE.md](../05_governance_os/RUNTIME_GOVERNANCE.md) · [../05_governance_os/CLAIM_SAFETY.md](../05_governance_os/CLAIM_SAFETY.md)
- حدّ الواتساب: [../02_saudi_positioning/WHATSAPP_BOUNDARY.md](../02_saudi_positioning/WHATSAPP_BOUNDARY.md)

---

> Estimated value is not Verified value / القيمة التقديرية ليست قيمة مُتحقَّقة
