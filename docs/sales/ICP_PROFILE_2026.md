# ملف العميل المثالي 2026 — ICP Profile 2026

> مرجع متقاطع: [`docs/company/ICP.md`](../company/ICP.md) — الملف الأصلي للنمط العام. هذا الملف يوسّع الأصل بمصفوفة تقييم كمية وأسئلة اكتشاف موزّعة وأحداث مشغّلة محددة لعام 2026.
> Cross-reference: [`docs/company/ICP.md`](../company/ICP.md) — original profile for the general pattern. This file extends it with a quantitative scoring matrix, categorised discovery questions, and 2026-specific trigger events.

---

## القسم الأول — تعريف العميل المثالي / Section 1: ICP Definition

### أولاً: العميل المستهدف الأساسي — Primary ICP

**وصف موجز:**
شركة B2B سعودية في مرحلة نمو، مُسجَّلة في ضريبة القيمة المضافة، لديها بيانات تشغيلية فعلية لكنها غير مُستثمَرة، وتواجه ضغطاً تنظيمياً أو تشغيلياً يُنبّه المؤسس للتحرك.

A Saudi B2B company in a growth phase, VAT-registered, holding real but underutilised operational data, facing regulatory or operational pressure that has put the founder on alert.

---

**المعايير الديموغرافية:**

| المعيار | النطاق المستهدف |
|---|---|
| حجم الشركة (موظفون) | 25 - 200 موظف |
| الإيرادات السنوية | 5 مليون - 200 مليون ريال |
| الحالة التنظيمية | مُسجَّلة في الضريبة، ملزمة بـ ZATCA المرحلة الثانية |
| نوع العمل | B2B حصراً — تقديم خدمات أو منتجات لشركات أخرى |

---

**القطاعات بترتيب الأولوية:**

| الترتيب | القطاع | سبب الأولوية |
|---|---|---|
| 1 | تقنية / SaaS | ألم بيانات عالٍ، سرعة قرار، تفهّم تقني |
| 2 | لوجستيات وسلاسل توريد | بيانات حركة غنية، ضغط ZATCA على الفواتير |
| 3 | تقنية رعاية صحية | حساسية PDPL عالية، تقارير تنظيمية متكررة |
| 4 | الخدمات المالية | رقابة صارمة، حاجة للأدلة في كل قرار |
| 5 | تصنيع | بيانات تشغيلية كثيفة، إهدار مرئي |

---

**الأولوية الجغرافية:**

| الترتيب | المدينة | المبرر |
|---|---|---|
| 1 | الرياض | كثافة شركات B2B، كثافة المحافظ الاستثمارية |
| 2 | جدة | تجمع لوجستيات وخدمات، قاعدة تجارية راسخة |
| 3 | الدمام | قاعدة صناعية وتقنية، نموّ مستمر |

---

**المؤشرات العملية (علامات الملاءمة):**

- الشركة مُسجَّلة في ضريبة القيمة المضافة وملزمة بامتثال ZATCA المرحلة الثانية
- تمتلك CRM أو نظام ERP لكن بيانات جودته أقل من 70% (completeness/accuracy)
- تعرّضت لرفض فاتورة من هيئة الزكاة خلال الـ 12 شهرًا الماضية
- التقارير للمؤسس أو الإدارة تُصنع يدوياً كل أسبوع أو شهر
- لا توجد سياسة مكتوبة لاستخدام الذكاء الاصطناعي داخل الشركة
- صاحب قرار واضح (مؤسس أو مدير تنفيذي) يمكن الوصول إليه مباشرة

---

### ثانياً: من نتجنّب — Anti-ICP

الدخول في أي من هذه الفئات يستوجب التوقف أو إعادة التوجيه — ليس التفاوض:

| الفئة | السبب |
|---|---|
| شركات ما قبل الإيراد (pre-revenue) | لا قدرة مالية حقيقية على الاشتراك أو السبرنت |
| شركات B2C للمستهلكين | نموذج مختلف جذرياً — قيمة Dealix في B2B |
| شركات تطلب أتمتة التواصل البارد | يُخالف المادة الأولى من الدستور التشغيلي — لا نفاوض |
| شركات تطلب ضمانات إيراد | يُخالف مبدأ الأدلة المُثبتة — لا نفاوض |
| شركات بلا مالك بيانات واضح | الارتباط التشغيلي لن يعمل — لا نبدأ بدون اسم owner |
| شركات ترفض الحوكمة والموافقات | Dealix مبني على APPROVAL_FIRST — التعارض جوهري |

---

## القسم الثاني — مصفوفة درجة التأهيل / Section 2: Qualification Score Matrix

**تعليمات الاستخدام:** أعطِ كل معيار درجة من 0 إلى 10 بناءً على وصف النطاقات أدناه. اجمع الدرجات للوصول إلى الشريحة المقابلة. الدرجة القصوى: 100.

**Usage instructions:** Score each criterion 0 to 10 based on the band descriptions below. Sum scores to reach the corresponding tier. Maximum score: 100.

---

### معايير التقييم العشرة — Ten Scoring Criteria

**1. نطاق الإيرادات السنوية — Annual Revenue Bracket**

| الدرجة | النطاق |
|---|---|
| 9 - 10 | 50M - 200M ريال |
| 7 - 8 | 15M - 49M ريال |
| 5 - 6 | 5M - 14M ريال |
| 2 - 4 | 1M - 4.9M ريال |
| 0 - 1 | أقل من 1M ريال أو غير معروفة |

---

**2. عدد الموظفين — Employee Count**

| الدرجة | النطاق |
|---|---|
| 9 - 10 | 50 - 200 موظف |
| 7 - 8 | 25 - 49 موظف |
| 5 - 6 | 201 - 500 موظف |
| 2 - 4 | 10 - 24 موظف |
| 0 - 1 | أقل من 10 أو أكثر من 500 |

---

**3. إلحاحية امتثال ZATCA — ZATCA Compliance Urgency**

| الدرجة | المؤشر |
|---|---|
| 9 - 10 | رفض فاتورة حالي أو تحقيق قائم |
| 7 - 8 | إشعار امتثال مستلم خلال 6 أشهر |
| 5 - 6 | ملزم بالمرحلة الثانية ولا يزال يُكمّل |
| 2 - 4 | مُسجَّل لكن لا ضغط فعلي الآن |
| 0 - 1 | غير مُسجَّل أو غير ملزم |

---

**4. الانكشاف على نظام PDPL — PDPL Exposure**

| الدرجة | المؤشر |
|---|---|
| 9 - 10 | يتعامل مع بيانات صحية أو مالية أو سجلات موظفين واسعة |
| 7 - 8 | يجمع بيانات عملاء ولم يُنجز تقييم أثر PDPL |
| 5 - 6 | يُدرك PDPL لكن السياسات غير مكتملة |
| 2 - 4 | انكشاف منخفض، بيانات B2B فقط |
| 0 - 1 | لا بيانات شخصية ذات أثر |

---

**5. نضج البيانات — Data Maturity**

| الدرجة | المؤشر |
|---|---|
| 9 - 10 | CRM/ERP نشط، بيانات موجودة، جودة 50-70% (مشكلة قابلة للحل) |
| 7 - 8 | بيانات في جداول، يمكن تصديرها، التكرارات معروفة |
| 5 - 6 | بيانات مبعثرة لكن يمكن جمعها |
| 2 - 4 | بيانات شحيحة أو غير موثّقة |
| 0 - 1 | لا توجد بيانات رقمية قابلة للعمل |

---

**6. توفر الميزانية — Budget Availability**

| الدرجة | المؤشر |
|---|---|
| 9 - 10 | ميزانية تقنية/تشغيل واضحة ومخصصة، صاحب قرار مالي متاح |
| 7 - 8 | ميزانية موجودة لكن تحتاج موافقة |
| 5 - 6 | يُشير إلى ميزانية محدودة لكن يرى القيمة |
| 2 - 4 | "ميزانية ضيقة" أو لم يُذكر رقم |
| 0 - 1 | رفض صريح للحديث عن الميزانية |

---

**7. إمكانية الوصول لصاحب القرار — Decision-Maker Access**

| الدرجة | المؤشر |
|---|---|
| 9 - 10 | التواصل المباشر مع المؤسس أو CEO أو CFO |
| 7 - 8 | تواصل مع مدير عمليات ذو صلاحية |
| 5 - 6 | تواصل مع فريق تقني / مدير قسم |
| 2 - 4 | التواصل عبر وسيط، صاحب القرار غير متاح |
| 0 - 1 | لا وصول لصاحب القرار |

---

**8. ملاءمة القطاع — Sector Fit**

| الدرجة | المؤشر |
|---|---|
| 9 - 10 | تقنية SaaS أو لوجستيات (الأولوية 1 و2) |
| 7 - 8 | رعاية صحية أو خدمات مالية (الأولوية 3 و4) |
| 5 - 6 | تصنيع أو خدمات مهنية (الأولوية 5) |
| 2 - 4 | قطاع غير مُختبَر لكن B2B |
| 0 - 1 | B2C أو قطاع خارج نطاق النموذج |

---

**9. الأولوية الجغرافية — Geographic Priority**

| الدرجة | المؤشر |
|---|---|
| 9 - 10 | الرياض |
| 7 - 8 | جدة |
| 5 - 6 | الدمام والمنطقة الشرقية |
| 2 - 4 | مناطق سعودية أخرى |
| 0 - 1 | خارج المملكة (MENA — مرحلة لاحقة) |

---

**10. الإحالة أو التواصل الدافئ — Referral or Warm Intro**

| الدرجة | المؤشر |
|---|---|
| 9 - 10 | إحالة مباشرة من عميل حالي راضٍ |
| 7 - 8 | تواصل دافئ عبر شبكة الثقة (زميل، مجلس إدارة) |
| 5 - 6 | حضر حدثًا وتواصل بشكل طوعي |
| 2 - 4 | تواصل عبر محتوى رقمي (LinkedIn، مقال) |
| 0 - 1 | تواصل بارد من مصدر غير معروف |

---

### شرائح القرار — Decision Tiers

| مجموع الدرجات | الشريحة | الإجراء |
|---|---|---|
| 70 - 100 | الشريحة الأولى — اتبع فوراً | ابدأ بالتشخيص المجاني هذا الأسبوع |
| 50 - 69 | الشريحة الثانية — رعاية ومتابعة | أضف لقائمة المتابعة، تواصل خلال 30 يوماً |
| أقل من 50 | الشريحة الثالثة — ليس الآن | وثّق السبب، أغلق المرحلة بدون استثمار وقت |

> سجّل الدرجة وتاريخها ومبررها في نظام CRM أو سجل الصفقات. قرار التأهيل دائم؛ لكن يمكن إعادة التقييم إذا تغيّرت الظروف.

---

## القسم الثالث — أسئلة الاكتشاف / Section 3: Discovery Questions

> مرجع: [`docs/sales/DISCOVERY_SCRIPT.md`](./DISCOVERY_SCRIPT.md) — سكريبت الاكتشاف الأصلي. الأسئلة أدناه تُوسّعه وتُنظّمه حسب الفئة.

الهدف من أسئلة الاكتشاف: **الفهم، لا الإقناع**. اسمع أكثر مما تتحدث. كل سؤال يُعطيك نقاط تقييم وبيانات لتقرير التشخيص.

The purpose of discovery questions is **understanding, not persuasion**. Listen more than you speak. Each question gives you scoring data and inputs for the diagnostic report.

---

### أ. تحديد الألم — Pain Identification (5 أسئلة)

**السؤال 1 (AR):** ما أكثر عملية تشغيلية تستهلك وقت فريقك أسبوعياً دون أن تُنتج قرارًا واضحًا؟

**Question 1 (EN):** What operational process consumes the most team time each week without producing a clear decision?

---

**السؤال 2 (AR):** هل هناك إيرادات أو فرص تعلمون أنها موجودة لكن لا تملكون الأدوات لمتابعتها بشكل منتظم؟

**Question 2 (EN):** Are there revenues or opportunities you know exist but lack the tools to follow up on consistently?

---

**السؤال 3 (AR):** عندما تُعدّ تقرير الأداء للإدارة — من يصنعه، وكم يأخذ من الوقت، وما نسبة البيانات التي تثق بصحتها؟

**Question 3 (EN):** When you prepare a performance report for leadership — who builds it, how long does it take, and what percentage of the data do you trust to be accurate?

---

**السؤال 4 (AR):** ما أكثر موقف يشعر فيه الفريق بأن العمل اليدوي يُبطّئ القرار الذي كان يجب اتخاذه بالأمس؟

**Question 4 (EN):** What situation most often makes the team feel that manual work is delaying a decision that should have been made yesterday?

---

**السؤال 5 (AR):** إذا استطعت إزالة إجراء واحد يدوي من يومك تمامًا — ما هو؟

**Question 5 (EN):** If you could eliminate one manual task from your workday entirely — what would it be?

---

### ب. تأهيل الميزانية — Budget Qualification (3 أسئلة)

**السؤال 6 (AR):** هل خصّصتم ميزانية هذا العام لمشاريع تحسين العمليات أو التقنية؟ وما حجمها التقريبي؟

**Question 6 (EN):** Have you allocated a budget this year for operations improvement or technology projects? What is its approximate range?

---

**السؤال 7 (AR):** من يملك قرار صرف الميزانية على مشروع من هذا النوع — أنت مباشرة، أم يحتاج موافقة إضافية؟

**Question 7 (EN):** Who owns the spending decision for a project of this type — you directly, or does it require additional approval?

---

**السؤال 8 (AR):** هل سبق أن تعاملتم مع مستشار تقني أو شريك عمليات خلال السنتين الماضيتين؟ ما الذي نجح وما الذي لم ينجح؟

**Question 8 (EN):** Have you worked with a technology consultant or operations partner in the past two years? What worked and what did not?

---

### ج. عملية القرار — Decision Process (3 أسئلة)

**السؤال 9 (AR):** كيف تبدو عملية اتخاذ القرار عادةً لمشروع بهذا الحجم — ما الخطوات من الاهتمام الأولي حتى التوقيع؟

**Question 9 (EN):** What does your decision-making process typically look like for a project of this size — from initial interest to signing?

---

**السؤال 10 (AR):** هل هناك أطراف أخرى تحتاج رأيها — مثل الشريك، المدير التقني، أو القانوني — قبل المضي قدماً؟

**Question 10 (EN):** Are there other stakeholders whose input you need — such as a co-founder, CTO, or legal counsel — before moving forward?

---

**السؤال 11 (AR):** ما الذي سيجعل هذا القرار سهلاً لك — وما الذي يجعله صعبًا؟

**Question 11 (EN):** What would make this decision easy for you — and what makes it difficult?

---

### د. إلحاحية ZATCA / PDPL — ZATCA/PDPL Urgency (4 أسئلة)

**السؤال 12 (AR):** هل تلقّيتم أي إشعارات من هيئة الزكاة والضريبة والجمارك بخصوص امتثال الفاتورة الإلكترونية المرحلة الثانية؟ وما وضع الامتثال لديكم الآن؟

**Question 12 (EN):** Have you received any notices from ZATCA regarding Phase 2 e-invoicing compliance? What is your current compliance status?

---

**السؤال 13 (AR):** هل قيّمتم التزاماتكم بموجب نظام حماية البيانات الشخصية (PDPL)؟ وهل عندكم سياسة خصوصية مكتوبة وفعّالة؟

**Question 13 (EN):** Have you assessed your obligations under the Personal Data Protection Law (PDPL)? Do you have a written and active privacy policy?

---

**السؤال 14 (AR):** ما البيانات التي تجمعونها عن عملائكم أو موظفيكم حالياً — وهل تعرفون أين تُخزَّن ومن يصل إليها؟

**Question 14 (EN):** What data do you currently collect about your clients or employees — and do you know where it is stored and who has access?

---

**السؤال 15 (AR):** إذا طُلب منكم تقرير امتثال ZATCA أو PDPL اليوم — كم ستأخذ من الوقت لإعداده، ومن المسؤول عنه؟

**Question 15 (EN):** If you were asked for a ZATCA or PDPL compliance report today — how long would it take to prepare, and who owns that responsibility?

---

## القسم الرابع — أحداث المشغّل / Section 4: Trigger Events

الأحداث المشغّلة هي إشارات خارجية تُشير إلى أن الشركة في حالة ألم فعلي الآن — مما يُقلّل دورة المبيعات ويرفع نسبة التحويل.

Trigger events are external signals indicating a company is in active pain now — reducing the sales cycle and raising conversion rates.

---

| # | الحدث المشغّل | ما يعنيه |
|---|---|---|
| 1 | رفض فاتورة من ZATCA | ضغط امتثال فوري، صاحب القرار في حالة يقظة |
| 2 | إشعار تدقيق ضريبي | حاجة عاجلة لبيانات منظّمة وقابلة للتدقيق |
| 3 | تعيين CFO أو مدير مالي جديد | أجندة جديدة، رغبة في إعادة ترتيب الأولويات |
| 4 | شكوى PDPL مقدَّمة ضد الشركة | ضغط قانوني مباشر، إلحاحية عالية |
| 5 | فقدان عميل رئيسي بسبب مشكلة بيانات | ألم مرئي، الاستعداد للاستثمار مرتفع |
| 6 | تعيين مدير عمليات جديد | فرصة لإعادة هيكلة العمليات بمنظور جديد |
| 7 | إطلاق منافس برقمنة عمليات | ضغط تنافسي يدفع لإغلاق الفجوة |
| 8 | توسع الشركة (فرع جديد أو منتج جديد) | ضغط تشغيلي متزايد على بنية بيانات غير جاهزة |
| 9 | فشل نظام تقارير داخلي | توقّف أو تأخير في قرارات إدارية يدفع للتغيير |
| 10 | إعلان الشركة عن دخول برنامج حكومي (نطاقات، إتاحة، إلخ) | التزامات امتثال جديدة تتطلب بيانات منظّمة |

---

> مرجع متقاطع لمنهجية التسليم: [`docs/03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md`](../03_commercial_mvp/SPRINT_DELIVERY_PLAYBOOK.md)
> مرجع التشخيص: [`docs/03_commercial_mvp/DIAGNOSTIC_DELIVERY_SOP.md`](../03_commercial_mvp/DIAGNOSTIC_DELIVERY_SOP.md)
> مرجع معايير الحوكمة: [`docs/00_foundation/NON_NEGOTIABLES.md`](../00_foundation/NON_NEGOTIABLES.md)

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
