# Dealix Agent Security Policy — سياسة أمان الوكلاء

> **الغرض:** سياسة موحّدة مقروءة للمؤسس تحكم الوكلاء داخل **GitHub Actions، أتمتة خارجية (n8n)، ووكلاء AI**. الفرض التفصيلي في الكود موجود تحت [`docs/36_agent_runtime_security/`](36_agent_runtime_security/README.md) — هذا الملف يجمعها ويضيف **نموذج تهديد المدخلات غير الموثوقة**.
>
> **Purpose:** one consolidated, founder-readable policy governing agents inside GitHub Actions, external automation (n8n), and AI agents. Deep enforcement lives in [`docs/36_agent_runtime_security/`](36_agent_runtime_security/README.md); this doc consolidates it and adds the **untrusted-input threat model**.

**مرتبط:** [`SECURITY.md`](../SECURITY.md) · [`docs/00_constitution/NON_NEGOTIABLES.md`](00_constitution/NON_NEGOTIABLES.md) · [`docs/governance/APPROVAL_POLICY.md`](governance/APPROVAL_POLICY.md) · [`docs/BUSINESS_AUTOPILOT_OS.md`](BUSINESS_AUTOPILOT_OS.md).

---

## 1) نموذج التهديد (Threat model)

سير العمل الوكيلي (agentic workflows) في CI و n8n يمكن **التلاعب به** عبر نص يدخل كـ prompt (تعليق issue، إيميل، ملاحظة CRM، مقتطف بحث). النتائج الممكنة دون ضوابط: **تسريب أسرار، تنفيذ أوامر غير مرغوبة، إجراء خارجي غير معتمد**.

**القاعدة الأساسية:** كل محتوى من خارج النظام = **بيانات لا أوامر** (data, not instructions).

### المدخلات غير الموثوقة (Untrusted inputs)

- تعليقات Issues و Pull Requests
- إيميلات واردة
- ملاحظات CRM ومدخلات نماذج الليدز
- مقتطفات بحث/ويب
- رسائل WhatsApp / محادثات العملاء
- أي محتوى يولّده مستخدم خارجي

---

## 2) القواعد الإلزامية (Rules) — مربوطة بغير القابل للتفاوض

1. لا ينفّذ الوكيل تعليمات من نص غير موثوق إلا ضمن سياسة النظام (prompt integrity).
2. لا يكشف الوكيل **أسراراً** ولا يطبع `env` (القانون 6 — لا PII/أسرار في السجلات).
3. لا يجيب من **معرفة بلا مصدر** (القانون 7).
4. لا **إجراء خارجي** (إيميل/واتساب/LinkedIn) بلا مرور عبر `approval_center` (القانون 8).
5. لا **وكيل بلا هوية** (`agent_identity_access_os` — القانون 9).
6. لا يغيّر الوكيل صلاحيات/ملفات workflows بلا مراجعة بشرية صريحة.
7. لا **نشر إنتاج** بلا موافقة بيئة (environment approval).
8. لا يعطّل اختبارات أو فحوص أمان.
9. لا يعدّل منطق **دفع/مصادقة/قاعدة بيانات** مدمِّراً بلا موافقة.
10. لا **scraping** ولا **cold WhatsApp** ولا **أتمتة LinkedIn** (القوانين 1/2/3 — مرفوضة في الكود عبر `tests/test_no_*`).

---

## 3) مسموح آلياً مقابل يحتاج موافقة

| ✅ مسموح آلياً (draft/داخلي) | ⛔ يحتاج موافقة المؤسس |
|------------------------------|--------------------------|
| إنشاء تقارير ووثائق | merge إلى `main` |
| إنشاء فروع وفتح PRs (draft) | نشر **production** |
| تحديث أصول المبيعات/الـ ops playbooks | تغيير **أسرار** |
| تشغيل الاختبارات | تغيير **صلاحيات workflows** |
| نشر **staging** بعد نجاح CI | **هجرات قاعدة بيانات** (migrations) |
| توليد مسودات إيراد/متابعة (`draft_only`) | تعديل **auth / payment** |
| | **أي إرسال خارجي** (إيميل/واتساب/LinkedIn) |

---

## 4) الطبقات المنفِّذة في الكود (Enforcing layers)

| الطبقة | الوحدة |
|--------|--------|
| الحدود الأربعة | [`docs/36_agent_runtime_security/FOUR_BOUNDARY_PROTECTION.md`](36_agent_runtime_security/FOUR_BOUNDARY_PROTECTION.md) |
| سلامة الـ Prompt | [`PROMPT_INTEGRITY.md`](36_agent_runtime_security/PROMPT_INTEGRITY.md) |
| حدود الأداة/البيانات/السياق | `TOOL_BOUNDARY.md` · `DATA_BOUNDARY.md` · `CONTEXT_BOUNDARY.md` |
| فرض السياسة وقت التشغيل | `runtime_safety_os` · `secure_agent_runtime_os` · `api/routers/runtime_safety_os.py` |
| بوابات الأدوات والقنوات | `tool_guardrail_gateway` · `channel_policy_gateway` |
| موافقات الإرسال | `approval_center` |
| هوية الوكلاء | `agent_identity_access_os` |
| حُرّاس الدستور | `tests/test_no_*` · `tests/governance/` (100+ اختبار) |

---

## 5) خاص بـ GitHub Actions و n8n

1. **لا** تشغّل وكيلاً على أي تعليق من أي شخص — مؤلّفون موثوقون فقط.
2. **لا** أسرار في workflows التي تقرأ تعليقات issues/PR.
3. `contents: write` فقط للـ workflows التي تحتاج فتح PR فعلاً.
4. **production deploy** يتطلّب environment approval.
5. n8n طبقة خارجية: كل إجراء خارجي = **مسودة في Approval Center** (لا إرسال آلي) — يطابق [`DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md §3`](commercial/DEALIX_COMPANY_DAILY_AUTOPILOT_AR.md).

---

*القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.*
