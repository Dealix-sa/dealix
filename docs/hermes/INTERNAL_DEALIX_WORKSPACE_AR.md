# Internal Dealix Workspace — مساحة الفريق الداخلي

> المرجع: §31 من المواصفة الأصلية.

---

## ما هذه المساحة؟

Internal Workspace هي مكان عمل فريق Dealix اليومي. كل ما يخص تشغيل الشركة — من استقبال الإشارات إلى تسليم القيمة — يحدث هنا، تحت إشراف Hermes ومع الالتزام بحدود الـ workspaces.

هذه المساحة **تخدم** Sovereign، لكنها لا تراها. ترى نتائج القرارات السيادية لا منطقها. ترى الموافقات الصادرة لا الموافقات المُعلَّقة. ترى المنتجات النشطة لا قائمة Kill المرشحة.

---

## الـ 11 صفحة الداخلية

| # | الصفحة | الغرض | KPIs أساسية |
|---|---|---|---|
| 1 | **Inbox** | كل الإشارات الواردة المُصنَّفة | عدد إشارات/يوم، زمن تصنيف، نسبة تأهيل |
| 2 | **Opportunities** | الفرص المُؤهَّلة قيد المعالجة | عدد فرص نشطة، قيمة مُقدَّرة، أعمار الفرص |
| 3 | **Pipeline** | خط أنابيب المبيعات (Diagnostic → Sprint → Retainer) | conversion بين المراحل، WIP لكل مرحلة |
| 4 | **Delivery** | تسليم الـ Diagnostics و Sprints الجارية | عدد تسليمات/أسبوع، Time-to-Proof، رضا |
| 5 | **Agents** | حالة الوكلاء الجارية (ما هم، ماذا يفعلون، تكلفتهم) | uptime، cost/run، failure rate |
| 6 | **Tools** | الأدوات المتاحة + الحدود اليومية | استخدام/أداة، quota، انتهاكات |
| 7 | **Evidence** | حِزَم الأدلة قيد البناء أو المسلَّمة (راجع [EVIDENCE_PACK_AR.md](EVIDENCE_PACK_AR.md)) | عدد حزم/أسبوع، اكتمالها، استخدامها في إغلاق |
| 8 | **Quality** | بوابات الجودة وحالاتها (راجع [QUALITY_GATES_AR.md](QUALITY_GATES_AR.md)) | نسبة عبور، أسباب الرفض الشائعة |
| 9 | **Content** | المحتوى المُنتَج (تقارير، مقالات، قوالب) | إنتاج/أسبوع، إعادة استخدام، مصادر الإلهام |
| 10 | **Customers** | قائمة العملاء النشطين + حالة الـ retainer | NRR، صحة العميل، توقعات upsell |
| 11 | **Internal Ops** | شؤون داخلية (HR، مالية تشغيلية، Vendors) | OKRs الفريق، نفقات تشغيل |

---

## ما يُخفى داخل Internal

- Sovereign decisions قيد المراجعة.
- Personal Wealth العائد للمؤسس.
- Kill Switch (يظهر فقط آثاره: "تم إيقاف الأداة X").
- قائمة المرشحين للـ Scale/Kill قبل الإعلان.
- Trust policies التفصيلية القابلة للتعديل (تُقرأ كـ read-only فقط).
- Capital Allocation الكامل (يظهر فقط الميزانية المخصصة للفريق).

---

## الإيقاع اليومي الداخلي (من يفتح ماذا متى)

| الوقت | الدور | الصفحات المفتوحة | الغرض |
|---|---|---|---|
| 08:30 | Lead Operations | Inbox + Opportunities | فرز الوارد، توزيع المهام |
| 09:00 | Delivery Lead | Delivery + Quality | متابعة تسليمات اليوم، إغلاق ما هو جاهز |
| 09:30 | Agents Owner | Agents + Tools | فحص صحة الوكلاء، حلّ failures |
| 10:00 | Sales | Pipeline + Opportunities | تحديث الـ pipeline، تجهيز مكالمات |
| 11:30 | Content/Evidence | Evidence + Content | بناء حزم الأدلة، نشر المحتوى المعتمد |
| 14:00 | Customer Success | Customers | متابعة retainers، Value Reports القادمة |
| 16:00 | Lead Operations | Internal Ops | إغلاق اليوم، تجهيز تقرير لـ Sovereign |
| 16:30 | الكل | Quality (read-only) | فحص بوابات اليوم، تسجيل دروس |

> التفاصيل الكاملة للإيقاع موجودة في [DAILY_OPERATING_RHYTHM_AR.md](DAILY_OPERATING_RHYTHM_AR.md).

---

## قواعد التشغيل الداخلية

1. **لا رسالة خارجية تخرج دون مرور Quality Gate** (راجع [QUALITY_GATES_AR.md](QUALITY_GATES_AR.md)).
2. **لا أداة جديدة تُستخدم دون قيدها في Tool Registry** (يخضع لـ Sovereign).
3. **لا وكيل يعمل خارج صلاحياته L0–L6**.
4. **لا عميل يُضاف يدويًا** — كل عميل يأتي عبر signal → opportunity → decision موثَّق.
5. **كل failure يُسجَّل** في Quality حتى لو حُلّ فورًا — للتعلم لا للعقاب.

---

## التقرير اليومي إلى Sovereign

في نهاية اليوم، Internal Workspace تُولّد تقريرًا موحَّدًا لـ Sovereign Command Page يحتوي على:

- ما تمّ إنجازه (بأرقام).
- ما تعطّل (وكلاء فشلوا، بوابات رُفض فيها شيء).
- ما يحتاج قرار سيادي غدًا.
- مرشحون جدد للـ Scale/Kill.
- تنبيهات Trust جديدة.

التقرير يُولَّد تلقائيًا من الأحداث، لا يُكتب يدويًا، لأن كل ما يحدث يُسجَّل أصلًا (راجع [HERMES_EVENT_MODEL_AR.md](HERMES_EVENT_MODEL_AR.md)).

---

## English Summary

- The Internal Workspace is where the Dealix team runs daily company operations across 11 pages: Inbox, Opportunities, Pipeline, Delivery, Agents, Tools, Evidence, Quality, Content, Customers, and Internal Ops.
- It deliberately hides Sovereign-only items: pending strategic decisions, personal wealth, kill switch state, scale/kill candidate lists, and capital allocation details.
- Each page has clear KPIs; the team follows a documented daily rhythm with named owners opening specific pages at specific times.
- A daily auto-generated report flows from Internal to the Sovereign Command Page — produced from the event log, not written manually.
- Five operating rules govern the workspace: no external message without a Quality Gate, no untracked tools, no out-of-permission agents, no manual customer adds, every failure logged.
