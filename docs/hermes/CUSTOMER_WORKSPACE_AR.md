# Customer Workspace — مساحة العميل

> المرجع: §32 من المواصفة الأصلية.

---

## ما هذه المساحة؟

Customer Workspace هي **السطح الوحيد** الذي يراه العميل من Dealix. لا يصل العميل إلى Internal، ولا إلى Sovereign، ولا إلى Trust، ولا إلى أي بيانات تخص عملاء آخرين. ما يرى هو **ما تمّ إنجازه له، بأدلة، وبتقرير قيمة شهري**.

الفلسفة: العميل لا يحتاج CRM. يحتاج إجابة لسؤال "ماذا حصلت من Dealix هذا الشهر، وما القادم؟"

---

## الـ 8 صفحات الظاهرة للعميل

| # | الصفحة | الغرض |
|---|---|---|
| 1 | **Home / Pulse** | لقطة شهرية: ما أُنجز، ما القيمة، ما القادم |
| 2 | **Opportunities** | الفرص التي تمّ تأهيلها لصالح العميل (مع تفاصيل سياق فقط) |
| 3 | **Deliveries** | تسليمات نشطة (Diagnostic, Sprint, Retainer Item) + حالتها |
| 4 | **Evidence** | حِزَم الأدلة الخاصة بهذا العميل (راجع [EVIDENCE_PACK_AR.md](EVIDENCE_PACK_AR.md)) |
| 5 | **Value Report** | تقرير القيمة الشهري (القالب أدناه) |
| 6 | **Recommendations** | توصيات Dealix القادمة (مع تصنيف Estimated / Observed) |
| 7 | **Documents** | عقود، مقترحات، تقارير منتهية، فواتير |
| 8 | **Support** | قناة تواصل مُهيكلة (طلبات، استفسارات، تصعيد) |

---

## الـ 6 أشياء المُخفاة عن العميل

1. **البيانات الخام** التي بُنيت عليها التحليلات — يرى الخلاصة لا المصدر.
2. **الاستراتيجية الداخلية** لـ Dealix (روadmaps، تسعير، اقتصاديات الوحدة).
3. **عملاء آخرون** — لا يعرف من غيره يستخدم Dealix.
4. **الـ Agents الداخلية** — يرى نتيجة الوكيل لا اسمه ولا تكلفته.
5. **Tool Registry** — يرى أن "تحليلًا تمّ" لا "تمّ باستخدام أداة X".
6. **Sovereign / Trust / Partner workspaces** — وجودها معلوم على المستوى العام فقط، لا تفاصيل.

---

## قاعدة الشفافية المتوازنة

العميل يرى **القيمة + الدليل + الحدود**:
- القيمة: ما تمّ إنجازه.
- الدليل: على ماذا اعتمدنا (مصادر، منهجية، استثناءات).
- الحدود: ما لم نفعله ولماذا.

هذا هو الفرق بين تقرير شفّاف وتقرير دعائي. القاعدة المتسقة مع كامل المنظومة: **القيمة التقديرية ليست قيمة مُتحقَّقة** (راجع `docs/08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md`).

---

## قالب Customer Value Report الشهري

كل شهر، Dealix تُولّد لكل عميل تقرير قيمة موحّد بـ 8 حقول:

```markdown
# Customer Value Report — {customer_name} — {month}

## 1. ماذا أنجزنا
{قائمة المُسلَّمات الفعلية: تشخيص، تقرير، عرض، حملة …}

## 2. كم فرصة
{عدد الفرص المُؤهَّلة، بأي قطاع، بأي حجم تقديري}

## 3. كم رسالة
{عدد الرسائل الخارجية المعتمدة، عبر أي قناة، نسبة الرد}

## 4. كم عرضًا
{عدد المقترحات المُرسَلة، حجمها التقديري الإجمالي}

## 5. كم نتيجة
{عدد الصفقات/الاتفاقيات/الأحداث المُغلقة}

## 6. ما القيمة
{Estimated value + Observed value + Verified value — كل واحد منفصل}

## 7. الخطة القادمة
{ما سننفّذه الشهر القادم بناءً على الأدلة + الموافقات المطلوبة}

## 8. التوصية
{توصية واحدة محورية: مواصلة / توسيع / تعديل / إيقاف نشاط محدد}

---
**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
```

---

## قواعد إنتاج Value Report

- يُولَّد آليًا من الأحداث (Event Model)، ثم يُراجَع بشريًا قبل الإرسال.
- يمرّ ببوابة جودة "any external message" (راجع [QUALITY_GATES_AR.md](QUALITY_GATES_AR.md)).
- لا يحتوي على ادعاءات غير مدعومة بدليل.
- ينتهي دائمًا بتذييل **القيمة التقديرية ≠ القيمة المُتحقَّقة**.
- يُؤرشَف في Documents تلقائيًا بعد الإرسال.

---

## ما لا يستطيع العميل فعله

- لا يستطيع تشغيل وكيل بنفسه.
- لا يستطيع طلب رسائل خارجية تخرج باسمه دون موافقة Dealix الداخلية + موافقته الخطية.
- لا يستطيع تصدير بيانات عملاء آخرين أو أصول مشتركة دون عقد صريح.
- لا يستطيع تجاوز Quality Gates عبر "أرسل الآن".

---

## English Summary

- The Customer Workspace is the only Dealix surface a customer ever sees; it shows eight pages focused on value delivered, evidence, and what comes next.
- Six things are intentionally hidden: raw data, internal strategy, other customers, agent internals, tool registry, and sibling workspaces.
- A monthly Customer Value Report follows a fixed eight-field template (delivered / opportunities / messages / proposals / outcomes / value / next plan / recommendation) and always closes with the Estimated-vs-Verified disclosure.
- Reports are auto-generated from the event log, human-reviewed, and gated through the "external message" quality gate before sending.
- Customers cannot run agents themselves, cannot bypass quality gates, and cannot access cross-customer data.
