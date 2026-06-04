# نظام ذكاء السوق | Market Intelligence OS

## الغرض | Purpose

**عربي:** نظام «ذكاء السوق» إطار لجمع وتنظيم إشارات السوق اعتمادًا على **البحث والإدخال اليدوي فقط**، دون أي تجريف للويب. يحوّل الملاحظات المتفرقة إلى معرفة منظّمة تدعم القرار. الذكاء الاصطناعي يجهّز الموجزات، والمؤسّس يعتمدها، وكل إجراء خارجي يدوي.

**English:** The Market Intelligence OS is a framework for collecting and organizing market signals using **manual research and input only — NO web scraping**. It turns scattered observations into structured, decision-supporting knowledge. AI prepares briefs, the founder approves, and every external action is manual.

---

## المصادر المسموحة | Allowed Sources

- البحث اليدوي والقراءة العامة.
- المحادثات مع العملاء والشركاء.
- الملاحظات الميدانية الموثّقة.
- المصادر العامة المتاحة (بقراءة يدوية، لا تجريف).

> ممنوع: تجريف المواقع، جمع البيانات الآلي، أو أي إرسال خارجي تلقائي.

---

## المكوّنات | Components

| المكوّن Component | الملف File |
|---|---|
| خريطة إشارات القطاعات | `01_VERTICAL_SIGNAL_MAP.md` |
| تتبّع المنافسين | `02_COMPETITOR_TRACKING.md` |
| مكتبة آلام العملاء | `03_CUSTOMER_PAIN_LIBRARY.md` |
| ملاحظات اتجاهات القطاع | `04_SECTOR_TREND_NOTES.md` |
| سجل أعمال البحث | `05_MARKET_RESEARCH_BACKLOG.md` |
| تقرير الأدلة | `99_MARKET_INTELLIGENCE_REPORT.md` |

---

## سير العمل | Workflow

1. **رصد يدوي | Manual observe:** تسجيل الإشارة ومصدرها.
2. **تصنيف | Classify:** قطاع، نوع، أهمية.
3. **تجهيز | Prepare:** يصيغ الذكاء الاصطناعي موجزًا.
4. **اعتماد | Approve:** يراجع المؤسّس ويعتمد.
5. **إجراء | Act:** خطوات يدوية فقط.

---

## التكوين الفني | Technical Config

- ملف الإشارات: `config/market_intelligence_signals.json`.
- سكربت الموجز: `scripts/market_intelligence_brief_generate.py`.
- الدور: تجهيز موجزات من إدخال يدوي؛ لا تجريف ولا إرسال.

---

## قواعد السلامة | Safety Guardrails

- لا تجريف ويب، لا جمع بيانات آلي.
- لا إرسال خارجي تلقائي (بريد/واتساب/لينكدإن).
- لا ادعاءات غير مثبتة ولا أرقام مفبركة.
- الذكاء الاصطناعي يجهّز، المؤسّس يعتمد، الإجراء يدوي.
