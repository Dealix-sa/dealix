# Open-Source Reference Library — مكتبة المراجع مفتوحة المصدر

**الغرض / Purpose:** مكتبة مراجع **للتعلّم المعماري فقط**. هذه المشاريع **ليست تبعيات (dependencies)، وليست submodules**، ولا نشحنها. نقرأها لفهم أنماط بنية CRM، الأتمتة، الأمن، الاختبار، وتنسيق الوكلاء — ثم نبني ما يناسب حوكمة Dealix.

A curated library for **architecture learning only**. None of these are dependencies, submodules, or shipped code. We read them to understand patterns in CRM structure, automation, security, testing, and agent orchestration — then build what fits Dealix governance.

**حدّ صريح / Hard boundary:** هذه المكتبة **لا تتضمّن** أي أداة كشط بيانات، ولا أداة أتمتة لينكدإن، ولا مرسل واتساب جماعي. تواصل Dealix يبقى **مسودة + موافقة + إرسال يدوي** فقط — انظر [PRODUCT_DISTRIBUTION_OS_AR.md](../distribution/PRODUCT_DISTRIBUTION_OS_AR.md).

This library **excludes** any data-scraping tool, any LinkedIn automation tool, and any WhatsApp bulk sender. Dealix outreach stays draft + approval + manual send.

**مرجع ذو صلة / Related:** نماذج CRM المرجعية: [CRM_REFERENCE_MODELS.md](CRM_REFERENCE_MODELS.md) · مصفوفة التكاملات: [../ops/INTEGRATION_ROADMAP_AND_VENDOR_MATRIX_AR.md](../ops/INTEGRATION_ROADMAP_AND_VENDOR_MATRIX_AR.md).

---

## 1) CRM — هيكلة الـ pipeline وبيانات العميل

| Project | لماذا مرجع مفيد / Why a useful reference |
|---------|------------------------------------------|
| `twentyhq/twenty` | CRM حديث TypeScript — مرجع لنمذجة الكائنات (objects) وعلاقات الـ pipeline وواجهة عمليات نظيفة. |
| `espocrm/espocrm` | نموذج كيانات قابل للتخصيص + طبقة صلاحيات — مرجع لتصميم الأدوار والحقول المخصصة. |
| `salesagility/SuiteCRM` | CRM مؤسسي ناضج — مرجع لمراحل المبيعات والـ workflow وحقول الصفقات. |

---

## 2) Automation — تنسيق سير العمل الحتمي

| Project | لماذا مرجع مفيد / Why a useful reference |
|---------|------------------------------------------|
| `n8n-io/n8n` | محرّك workflow عقدي — مرجع لنمذجة الخطوات الحتمية والـ triggers والربط بين الأنظمة. |
| `activepieces/activepieces` | أتمتة مفتوحة قابلة للامتداد — مرجع لبنية الـ pieces/connectors وطبقة الموافقة على الخطوات. |
| `automatisch/automatisch` | بديل مفتوح المصدر — مرجع لنمط الـ flows وإدارة بيانات الاعتماد بأمان. |

> ملاحظة حوكمة: نستلهم **نمط التنسيق** فقط؛ في Dealix لا خطوة ترسل خارجياً دون موافقة بشرية — لا «إرسال تلقائي» مهما سمحت الأداة المرجعية.

---

## 3) Security — الأمن وسلامة سلسلة التوريد

| Project | لماذا مرجع مفيد / Why a useful reference |
|---------|------------------------------------------|
| `semgrep/semgrep` | فحص ثابت قائم على القواعد — مرجع لكتابة قواعد حجب أنماط ممنوعة (مثل بوابة الجودة عندنا). |
| `github/codeql-action` | تحليل دلالي للكود في CI — مرجع لدمج فحص أمني في خط الـ pipeline. |
| `ossf/scorecard-action` | تقييم صحّة سلسلة التوريد — مرجع لمعايير الأمان للمستودعات. |

---

## 4) Testing — الاختبار والمراقبة

| Project | لماذا مرجع مفيد / Why a useful reference |
|---------|------------------------------------------|
| `microsoft/playwright` | اختبار E2E للواجهات — مرجع لاختبار مسارات المستخدم بثبات. |
| `schemathesis/schemathesis` | اختبار API انطلاقاً من OpenAPI/JSON Schema — مرجع للتحقق من العقود (مثل مخططاتنا تحت `schemas/`). |
| `getsentry/sentry-python` | رصد الأخطاء والأداء — مرجع لطبقة المراقبة وإخفاء البيانات الحساسة في السجلات. |

---

## 5) Agent orchestration — تنسيق الوكلاء (مرجع فقط)

| Project | لماذا مرجع مفيد / Why a useful reference |
|---------|------------------------------------------|
| `langchain-ai/langgraph` | رسم بياني لحالات الوكيل — **مرجع فقط** لفهم حلقات القرار/المراجعة. في Dealix: الذكاء يستكشف ويوصي، والبشر يوافقون على الالتزامات الخارجية — لا حلقة وكيل تُحدث إرسالاً خارجياً. |

---

## 6) كيف نستخدم هذه المكتبة

| نريد أن نتعلّم | نقرأ من |
|----------------|---------|
| كيف نهيكل الـ pipeline | CRM (Twenty / EspoCRM / SuiteCRM) — وانظر [CRM_REFERENCE_MODELS.md](CRM_REFERENCE_MODELS.md) |
| كيف ننسّق خطوات حتمية | Automation (n8n / Activepieces / Automatisch) |
| كيف نكتب بوابات حجب | Security (Semgrep / CodeQL / Scorecard) |
| كيف نختبر العقود والواجهات | Testing (Playwright / Schemathesis / Sentry) |
| كيف نفكّر في حلقات الوكلاء | LangGraph (مرجع فقط) |

> قاعدة ثابتة: أي نمط نستعيره يخضع لحوكمة Dealix أولاً — لا إرسال خارجي تلقائي، لا كشط، لا قنوات ممنوعة. المرجع يُلهم البنية، لا يتجاوز السياسة.

---

> القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.

*مكتبة مراجع — ليست تبعيات. آخر تحديث: 2026-06-02.*
