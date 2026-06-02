# Revenue Execution Reference Library — مكتبة مراجع تنفيذ الإيراد — Reference Library

> Purpose — الغرض: هذه قائمة مشاريع مفتوحة المصدر **للمرجع فقط** — لدراسة الأنماط، لا للاعتماد عليها. **ليست اعتماديات (NOT dependencies).** لا يُضاف أي مشروع منها إلى شجرة اعتماديات نظام تنفيذ الإيراد دون قرار صريح موثّق. الغرض الوحيد: استلهام أنماط التصميم والحوكمة والاختبار.
>
> This is a list of open-source projects for reference only — to study patterns, not to depend on. NOT dependencies. No project here is added to the Revenue Execution OS dependency tree without an explicit, documented decision. The sole purpose is to learn design, governance, and testing patterns.

Cross-link — روابط: [../distribution/README.md](../distribution/README.md) · [../distribution/EXTERNAL_AUTOMATION_BLUEPRINT_AR.md](../distribution/EXTERNAL_AUTOMATION_BLUEPRINT_AR.md) · [../v10/REFERENCE_LIBRARY_70.yaml](../v10/REFERENCE_LIBRARY_70.yaml) · [../v10/DEPENDENCY_DECISION_RECORD.md](../v10/DEPENDENCY_DECISION_RECORD.md).

---

## 1. كيف تُقرأ هذه القائمة — How to read this list

| العمود — Column | المعنى — Meaning |
|---|---|
| المشروع — Project | الاسم والمستودع (org/repo) |
| النمط المُستلهَم — Pattern studied | ما ندرسه منه |
| الحالة — Status | **reference only — NOT a dependency** لكل الصفوف |

> قاعدة صارمة — Hard rule: كل صف هنا حالته «reference only». تحويل أي منها إلى اعتمادية فعلية يتطلّب قرار اعتمادية موثّقًا (راجع [../v10/DEPENDENCY_DECISION_RECORD.md](../v10/DEPENDENCY_DECISION_RECORD.md)). الإدراج هنا لا يعني الاستخدام.

---

## 2. CRM — أنظمة إدارة العلاقات (مرجع فقط)

| المشروع — Project | المستودع — Repo | النمط المُستلهَم — Pattern studied | الحالة — Status |
|---|---|---|---|
| Twenty | `twentyhq/twenty` | نموذج كائنات CRM، واجهة الصفقات | reference only — NOT a dependency |
| EspoCRM | `espocrm/espocrm` | نموذج العلاقات والأذونات | reference only — NOT a dependency |
| SuiteCRM | `salesagility/SuiteCRM` | تدفّقات المبيعات الناضجة | reference only — NOT a dependency |

نستلهم بنية الكائنات والحالات، لا الكود. نموذج الصفقة لدينا أصلي (راجع [../distribution/DRAFT_SYSTEM_SPEC_AR.md](../distribution/DRAFT_SYSTEM_SPEC_AR.md)).

We study object/state structure, not code. Our deal model is native.

---

## 3. Automation — الأتمتة (مرجع فقط)

| المشروع — Project | المستودع — Repo | النمط المُستلهَم — Pattern studied | الحالة — Status |
|---|---|---|---|
| n8n | `n8n-io/n8n` | تدفّقات حتمية، عُقَد التذكير/المزامنة | reference only — NOT a dependency |
| Activepieces | `activepieces/activepieces` | بنية التدفّق المرئي | reference only — NOT a dependency |
| Automatisch | `automatisch/automatisch` | أتمتة بسيطة مستضافة ذاتيًا | reference only — NOT a dependency |

سياسة n8n الفعلية (المسموح الحتمي مقابل الممنوع) في [../distribution/EXTERNAL_AUTOMATION_BLUEPRINT_AR.md](../distribution/EXTERNAL_AUTOMATION_BLUEPRINT_AR.md). حتى لو استُخدِم n8n، فالحدود تبقى: لا إرسال خارجي، لا قرار LLM بالإرسال.

Even if n8n is used, the boundaries hold: no external send, no LLM-decides-to-send.

---

## 4. Testing & Security — الاختبار والأمن (مرجع فقط)

| المشروع — Project | المستودع — Repo | النمط المُستلهَم — Pattern studied | الحالة — Status |
|---|---|---|---|
| Playwright | `microsoft/playwright` | اختبار تدفّقات المراجعة | reference only — NOT a dependency |
| Schemathesis | `schemathesis/schemathesis` | اختبار المخططات مقابل الـAPI | reference only — NOT a dependency |
| Semgrep | `semgrep/semgrep` | فحص أنماط الكود الخطرة | reference only — NOT a dependency |
| CodeQL | `github/codeql` | تحليل أمني ثابت | reference only — NOT a dependency |
| Scorecard | `ossf/scorecard` | تقييم سلامة سلسلة التوريد | reference only — NOT a dependency |

ندرس منها كيفية اختبار حواجز الحوكمة (مثل التأكّد أن لا endpoint يرسل خارجيًا)، لا لإضافتها كاعتماديات إنتاج.

We study how to test governance gates (e.g., asserting no endpoint sends externally), not to add them as production dependencies.

---

## 5. Orchestration — التنسيق (مرجع فقط)

| المشروع — Project | المستودع — Repo | النمط المُستلهَم — Pattern studied | الحالة — Status |
|---|---|---|---|
| LangGraph | `langchain-ai/langgraph` | بنية الحالات والعُقَد لتدفّق الوكلاء | reference only — NOT a dependency |

نستلهم نمط «الحالة الصريحة» لخط الأنابيب العشاري، مع الإبقاء على قاعدة: لا عقدة تتخذ إجراءً خارجيًا دون موافقة (راجع [../distribution/PRODUCT_DISTRIBUTION_OS_AR.md](../distribution/PRODUCT_DISTRIBUTION_OS_AR.md)).

We borrow the explicit-state pattern for the ten-stage pipeline, keeping the rule: no node takes an external action without approval.

---

## 6. لماذا «مرجع فقط» — Why "reference only"

- **سلسلة التوريد** — كل اعتمادية سطح هجوم؛ نقلّلها عمدًا.
- **الحوكمة** — أداة خارجية قد تحمل قدرة تخالف القواعد الـ11 (مثل إرسال آلي)؛ الإدراج المرجعي يدرس النمط دون استيراد الخطر.
- **الأصالة** — المنطق الأساسي (المسودات، الحوكمة، الإثبات) أصلي في `auto_client_acquisition/revenue_execution_os/`.

Supply-chain minimization, governance safety, and native ownership of core logic.

كل ترقية من «مرجع» إلى «اعتمادية» تمرّ بقرار موثّق (راجع [../v10/DEPENDENCY_DECISION_RECORD.md](../v10/DEPENDENCY_DECISION_RECORD.md)) وبموافقة المؤسس.

Every promotion from "reference" to "dependency" passes a documented decision and founder approval.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة — Estimated value is not Verified value.
