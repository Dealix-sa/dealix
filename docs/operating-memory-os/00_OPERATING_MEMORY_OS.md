# نظام الذاكرة التشغيلية | Operating Memory OS

> **AR:** طبقة الذاكرة التشغيلية هي السجل الموحّد الذي تتذكّر فيه Dealix قراراتها وعملاءها وسوقها وإيراداتها بصيغة منظمة وقابلة للتدقيق. الهدف أن لا تُتخذ أي قرار مرتين من الصفر، وأن يبقى كل سجل مرجعًا موثّقًا يوافق عليه المؤسس يدويًا.
>
> **EN:** The Operating Memory layer is the unified, auditable ledger where Dealix remembers its decisions, clients, market, and revenue in a structured form. The goal: no decision is taken twice from scratch, and every record stays a documented reference that the founder approves manually.

## المبادئ الحاكمة | Governing Principles

- **AI prepares, Founder approves, Manual action only, No external sending.**
- الذاكرة تُولَّد كمسودّات منظمة؛ لا تُعتمد سجلات إلا بموافقة المؤسس. / Memory is generated as structured drafts; records are committed only on founder approval.
- لا إرسال خارجي تلقائي (بريد/واتساب/لينكدإن) ولا كشط بيانات. / No automated external sending (email/WhatsApp/LinkedIn) and no scraping.
- لا أسرار ولا مفاتيح API داخل السجلات. / No secrets or API keys inside records.

## مكوّنات الطبقة | Layer Components

| المكوّن Component | المسار Path | الدور Role |
|---|---|---|
| المخططات Schemas | `config/operating_memory_schemas.json` | تعريف بنية كل نوع سجل / Defines each record type |
| المُحقِّق Validator | `scripts/operating_memory_validate.py` | فحص السجلات مقابل المخططات / Validates records vs schemas |
| ذاكرة القرار Decision | `02_DECISION_MEMORY.md` | تسجيل واسترجاع القرارات / Record & recall decisions |
| ذاكرة العميل Client | `03_CLIENT_MEMORY.md` | سجل سياق العميل / Client context record |
| ذاكرة السوق Market | `04_MARKET_MEMORY.md` | إشارات وفرضيات السوق / Market signals & hypotheses |
| ذاكرة الإيراد Revenue | `05_REVENUE_MEMORY.md` | حركة الأنبوب والإيراد / Pipeline & revenue movement |

## أنواع السجلات | Record Types

- **Decision Memory** — قرار، سياقه، البدائل، الأساس، الحالة.
- **Client Memory** — هوية العميل، احتياجه، حالة العلاقة، آخر تفاعل.
- **Market Memory** — قطاع، إشارة، فرضية، مستوى الثقة.
- **Revenue Memory** — مرحلة الصفقة، القيمة، الاحتمالية، التحقق.

## دورة الحياة | Lifecycle

1. **Generate** — يولّد الذكاء مسودة سجل وفق المخطط. / AI drafts a record per schema.
2. **Validate** — يُشغَّل `operating_memory_validate.py`. / Run the validator.
3. **Review** — يراجع المؤسس المحتوى. / Founder reviews.
4. **Commit** — يُعتمد السجل ويُختم بالطابع الزمني. / Record committed with timestamp.
5. **Recall** — يُستدعى عند أي قرار لاحق. / Recalled for any later decision.

## حدود الأمان | Safety Boundaries

- كل فعل خارجي يبقى يدويًا وبموافقة المؤسس. / Every external action stays manual and founder-approved.
- لا حركة فعلية (إرسال/تقديم نماذج/إطلاق إعلانات) تنشأ عن سجل ذاكرة. / No live action arises from a memory record.
- لا ادعاءات غير مثبتة ولا عائد مضمون ولا جذب وهمي. / No unproven claims, no guaranteed ROI, no fake traction.

## مراجع | References

- التقرير الإثباتي / Evidence report: `99_OPERATING_MEMORY_REPORT.md`
- حدود الأتمتة / Automation boundaries: `../automation-boundaries-os/00_AUTOMATION_BOUNDARIES_OS.md`
