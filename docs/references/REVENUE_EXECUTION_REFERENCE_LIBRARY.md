# Revenue Execution — Reference Library — مكتبة المراجع

> **REFERENCE ONLY — مرجع فقط.** هذه المستودعات للاطلاع والتعلّم من الأنماط الهندسية فقط. **لا تُضاف كاعتماديات (dependencies)، ولا يُدخَل أي إطار جديد إلا عند وجود فجوة محدّدة موثَّقة.** Dealix يبني على ما هو قائم؛ لا frameworks جديدة بلا مبرّر.
>
> **REFERENCE ONLY.** These repositories are for studying engineering patterns. **Do not add them as dependencies, and introduce no new framework unless a specific, documented gap exists.** Dealix builds on what already exists; no new frameworks without justification.

روابط / Related: [../distribution/REVENUE_EXECUTION_OS_AR.md](../distribution/REVENUE_EXECUTION_OS_AR.md) · [../commercial/CODE_MAP_OS_TO_MODULES_AR.md](../commercial/CODE_MAP_OS_TO_MODULES_AR.md)

---

## كيف تُستخدَم هذه القائمة / How to use this list

- **للاطلاع والمقارنة المعمارية** عند تصميم مرحلة من نظام تنفيذ الإيراد. / For architectural comparison when designing a stage of the Revenue Execution OS.
- **ليست قائمة تثبيت.** قبل أي تبنٍّ، يجب توثيق الفجوة التي يسدّها المرجع ولماذا لا يكفي الموجود. / Not an install list. Before any adoption, document the gap and why existing code is insufficient.
- **تظل الحوكمة سيدة:** أي نمط مستعار يخضع لقواعد [../distribution/REVENUE_EXECUTION_OS_AR.md](../distribution/REVENUE_EXECUTION_OS_AR.md) الـ11 (لا إرسال آلي، لا scraping، لا PII، موافقة المؤسس...). / Governance still rules: any borrowed pattern obeys the 11 non-negotiables.

---

## CRM — إدارة علاقات العملاء (أنماط دورة حياة وكيانات)

| المستودع / Repo | لماذا كمرجع / Why as reference |
|---|---|
| `twentyhq/twenty` | نموذج كيانات CRM حديث وواجهات دورة حياة العميل. / Modern CRM entity model and lifecycle UI patterns. |
| `espocrm/espocrm` | تنظيم العلاقات والمراحل والصلاحيات. / Relationship, stage, and permission organization. |
| `salesagility/SuiteCRM` | أنماط ناضجة لإدارة الفرص والقمع. / Mature opportunity and pipeline patterns. |

> الاستخدام: مقارنة مع كيانات `prospect` / `proposal` / `win_loss` فقط — لا استبدال للمخططات القائمة. / Use: compare against existing entities only — no schema replacement.

## Automation — الأتمتة (أنماط تنسيق سير العمل تحت حوكمة)

| المستودع / Repo | لماذا كمرجع / Why as reference |
|---|---|
| `n8n-io/n8n` | أنماط عقد سير العمل والمشغّلات. / Workflow-node and trigger patterns. |
| `activepieces/activepieces` | تنظيم خطوات وموافقات سير العمل. / Step and approval organization. |
| `automatisch/automatisch` | تكاملات سير عمل مفتوحة كمرجع تصميم. / Open workflow integrations as a design reference. |

> الاستخدام: مرجع لتصميم [../distribution/FOLLOWUP_ENGINE_AR.md](../distribution/FOLLOWUP_ENGINE_AR.md) — **مع إبقاء كل إرسال خارجي يدوياً وبموافقة**. / Use: reference for the follow-up engine — keeping all external send manual and approved.

## Testing / Security — الاختبار والأمن (أنماط جودة وفحص)

| المستودع / Repo | لماذا كمرجع / Why as reference |
|---|---|
| `microsoft/playwright` | أنماط اختبار سير المستخدم end-to-end. / End-to-end user-flow testing patterns. |
| `schemathesis/schemathesis` | فحص اتساق العقود/المخططات (API schemas). / API schema/contract consistency checks. |
| `semgrep/semgrep` | قواعد فحص ثابت للأمن وجودة الكود. / Static analysis for security and code quality. |
| `github/codeql-action` | تحليل كود ضمن CI. / Code analysis within CI. |
| `ossf/scorecard-action` | تقييم نضج أمن المستودع. / Repository security-posture scoring. |

> الاستخدام: مرجع لانضباط الجودة في [../distribution/DRAFT_QUALITY_POLICY_AR.md](../distribution/DRAFT_QUALITY_POLICY_AR.md) ومؤشرات الحوكمة — **لا نشر إنتاجي ولا أسرار**. / Use: reference for quality discipline and governance signals — no production deploy, no secrets.

## Agent Orchestration — تنسيق الوكلاء (أنماط حالة وتدفّق)

| المستودع / Repo | لماذا كمرجع / Why as reference |
|---|---|
| `langchain-ai/langgraph` | أنماط آلة الحالة وتدفّق الوكلاء متعدّد الخطوات. / State-machine and multi-step agent-flow patterns. |

> الاستخدام: مرجع لتصميم انتقالات الحالات (مسودة → موافقة → إرسال) — **مع بقاء بوابة الموافقة البشرية إلزامية**. / Use: reference for state transitions (draft → approval → send) — human approval gate stays mandatory.

---

## الحدود / Boundaries

1. **مرجع فقط؛ لا اعتماديات جديدة.** / Reference only; no new dependencies.
2. **لا إطار جديد إلا بفجوة موثَّقة** ومراجعة هندسية. / No new framework without a documented gap and engineering review.
3. **كل نمط مستعار يخضع للـ11 بنداً** غير القابلة للتفاوض. / Every borrowed pattern obeys the 11 non-negotiables.
4. **لا أسماء مزوّدين/نماذج في واجهة العميل.** / No vendor/model names in customer-facing surfaces.

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
