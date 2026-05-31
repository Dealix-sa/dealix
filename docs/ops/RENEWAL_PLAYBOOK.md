# دليل تشغيل التجديد — Renewal Operations Playbook

> مرجع متقاطع: [`docs/07_proof_os/PROOF_PACK_STANDARD.md`](../07_proof_os/PROOF_PACK_STANDARD.md) — معيار حزمة الإثبات المطلوبة في كل تجديد.
> [`docs/05_governance_os/APPROVAL_POLICY.md`](../05_governance_os/APPROVAL_POLICY.md) — سياسة الموافقات، تُطبَّق على عروض التجديد.
> [`docs/03_commercial_mvp/RETAINER_PATH.md`](../03_commercial_mvp/RETAINER_PATH.md) — منطق مسار العقود الشهرية.

---

## القسم الأول — فلسفة التجديد / Section 1: Renewal Philosophy

### بالعربية

التجديد في Dealix ليس مبيعات — هو امتداد طبيعي لأدلة قائمة. قبل أي محادثة تجديد، يجب أن تكون حزمة الإثبات (Proof Pack) جاهزة ومراجَعة. لا نطلب تجديدًا بدون بيانات، ولا نستخدم الإقناع كبديل عن الأثر الموثَّق.

كل محادثة تجديد تبدأ بجملة واحدة: "إليك ما أنجزناه معًا." ثم نتوقف لنسمع.

إذا كانت درجة الصحة (Health Score) أقل من 65 — لا نطرح التجديد حتى نُصلح المشكلة. إذا كانت فوق 75 — التجديد هو الخيار الأقل جهدًا للعميل، لأن البديل هو إعادة بناء ما بنيناه معًا.

لا وعود بنتائج مضمونة في أي محادثة تجديد. الكلام المسموح: "هذا ما حدث، هذا ما نُقدّره للمرحلة القادمة، هذا ما نُوصي به."

### In English

Renewal at Dealix is not a sales event — it is the natural extension of existing evidence. Before any renewal conversation, the Proof Pack must be ready and reviewed. We do not ask for renewal without data, and we do not use persuasion as a substitute for documented impact.

Every renewal conversation begins with one sentence: "Here is what we have achieved together." Then we pause and listen.

If the Health Score is below 65 — do not raise renewal until the underlying problem is resolved. If above 75 — renewal is the path of least effort for the client, because the alternative is rebuilding what we built together.

No guaranteed outcome promises in any renewal conversation. Permitted language: "This is what happened, this is what we estimate for the next period, this is what we recommend."

---

## القسم الثاني — تقويم التجديد (90 يوماً) / Section 2: Renewal Timeline (90-Day Calendar)

### نظرة عامة على المحطات

| اليوم | المحطة | الإجراء | المسؤول |
|---|---|---|---|
| يوم -90 | فحص الصحة | احسب Health Score. إذا < 65: أطلق إجراء التعافي فوراً | المؤسس |
| يوم -60 | مراجعة حزمة الإثبات | اجمع بيانات الأثر، حدّد الأصول المنتجة، حدّد فرص الترقية | المؤسس |
| يوم -45 | بدء محادثة التجديد | افتح المحادثة بالأدلة — لا طلب تجديد مباشر بعد | المؤسس |
| يوم -30 | إرسال العرض | أرسل عرض التجديد (صيانة أو ترقية) عبر APPROVAL_FIRST | المؤسس |
| يوم -14 | موعد القرار | ذكّر بموعد القرار مرة واحدة فقط — لا ضغط متكرر | المؤسس |
| يوم -7 | التوقيع أو التصعيد | إذا لم يُوقَّع: تصعيد وفق بروتوكول أدناه | المؤسس |
| يوم 0 | تاريخ التجديد | تجديد ساري أو إغلاق نظيف مع خطة انتقال | المؤسس |

---

### اليوم -90: فحص الصحة — Day -90: Health Check

**ما يُقاس:**

| البُعد | وزنه في الدرجة |
|---|---|
| درجة الاستخدام الفعلي للمخرجات | 30% |
| تواصل العميل وإشراكه | 20% |
| جودة البيانات المُدخَلة | 20% |
| عدد الأصول الرأسمالية المُودَعة | 15% |
| درجة إثبات آخر مشروع (Proof Score) | 15% |

**قرار الاستجابة:**

- **Health Score ≥ 75:** كل شيء على المسار — استمر في التقويم
- **Health Score 65 - 74:** راقب عن كثب، ابدأ محادثة استباقية مع العميل
- **Health Score < 65:** أطلق بروتوكول التعافي فوراً — لا تُرجئ

---

### اليوم -60: مراجعة حزمة الإثبات — Day -60: Proof Pack Review

**قائمة التحقق قبل التجديد:**

- [ ] حزمة الإثبات لآخر دورة كاملة موجودة ومكتملة (14 قسماً)
- [ ] درجة الإثبات (Proof Score) ≥ 70
- [ ] مقاييس الأثر الموثّقة: توفير الوقت، جودة البيانات، مخرجات القرار
- [ ] قائمة الأصول الرأسمالية المُودَعة خلال فترة العقد
- [ ] أي حوادث مُغلَقة أو مشاكل مُحلَّة موثّقة
- [ ] تحديد فرصة الترقية إذا Health Score > 75

**قرار فرصة الترقية:**

إذا أنتج العميل 3 أصول رأسمالية أو أكثر، أو تجاوز معدل استخدام المخرجات 80% — أضف سيناريو الترقية إلى العرض.

---

## القسم الثالث — دليل الاستجابة حسب الشريحة / Section 3: Renewal Tiers Response Playbook

---

### الشريحة الأساسية — Essential: 2,999 ريال/شهر

#### سكريبت التجديد القياسي

**بالعربية:**

"خلال الفترة الماضية أنجزنا معًا [X من المخرجات الموثّقة]: درجة جودة بياناتك ارتفعت من [A] إلى [B]، وأنتجنا [N] مسودة معتمدة، وأودعنا [M] أصلاً قابلاً لإعادة الاستخدام. بناءً على هذه الأدلة، نوصي بتجديد العقد للمرحلة القادمة. هل لديك أسئلة حول أي من هذه الأرقام قبل المضي قدماً؟"

**In English:**

"Over the past period we have achieved together [X documented outputs]: your data quality score improved from [A] to [B], we produced [N] approved drafts, and deposited [M] reusable capital assets. Based on this evidence, we recommend renewing for the next period. Do you have any questions about any of these figures before we proceed?"

---

#### ترقية إلى Professional (إذا Health Score > 75)

**بالعربية:**

"درجة الصحة التشغيلية لديكم [X/100]. هذا يُشير إلى أن فريقك يستخدم المخرجات بفاعلية عالية. الشريحة التالية (3,999 ريال/شهر) تُضيف [وصف ما تُضيفه الشريحة المهنية — راجع OFFER_ARCHITECTURE.md]. التقدير: القيمة الإضافية المحتملة تفوق الفارق في التكلفة. هذا رأي مبني على الأدلة، لا ضمان."

**In English:**

"Your operational health score is [X/100]. This indicates your team is using outputs at high effectiveness. The next tier (3,999 SAR/month) adds [describe Professional tier additions — see OFFER_ARCHITECTURE.md]. Estimate: the potential additional value exceeds the cost difference. This is an evidence-based recommendation, not a guarantee."

---

#### استجابة الخطر (Health Score < 55)

**بالعربية:**

"نلاحظ أن درجة الصحة التشغيلية لدورة هذا العقد [X/100] — وهي أقل من المستهدف. قبل أن نطرح خيارات التجديد، نريد أن نفهم معك: ما العائق الرئيسي؟ هل هو استخدام المخرجات، أم جودة البيانات، أم الوقت من فريقك؟ بناءً على إجابتك نحدد الخطوة الصحيحة — وقد تكون التجديد بشكل مختلف، أو مشروعًا تعافٍ قصيراً قبل التجديد."

**In English:**

"We observe that the operational health score for this contract period is [X/100] — below target. Before presenting renewal options, we want to understand: what is the primary obstacle? Is it output utilisation, data quality, or team availability? Based on your answer we determine the right next step — which may be renewal in a different form, or a short recovery engagement before renewal."

---

#### بروتوكول منع الإلغاء

- لا أكثر من تدخلين (اتصالات أو رسائل) خلال أي 30 يوماً للمطالبة بالتجديد
- التدخل الأول: مراجعة الأدلة (لا طلب تجديد مباشر)
- التدخل الثاني: عرض مكتوب مع حزمة الإثبات كاملة
- إذا لم تُغلَق الصفقة بعد التدخلين: انتقل لإغلاق نظيف مع خطة انتقال

**الإغلاق النظيف يعني:** توثيق أسباب عدم التجديد، تسليم ملف البيانات الكامل للعميل، تسجيل الدرس في سجل الأصول.

---

### الشريحة المهنية — Professional: 3,999 ريال/شهر

#### سكريبت التجديد القياسي

**بالعربية:**

"في هذه الدورة: [X من المخرجات]. درجة الصحة [Y/100]. الأصول الرأسمالية المُودَعة: [Z]. نوصي بتجديد الشريحة المهنية للمرحلة القادمة. لاحظنا أن [وصف مجال نموّ محدد] يُمثّل فرصة موثّقة — هل تريد أن نُدرجه في نطاق الدورة القادمة؟"

**In English:**

"This cycle: [X outputs]. Health score [Y/100]. Capital assets deposited: [Z]. We recommend renewing the Professional tier for the next period. We have observed that [describe specific growth area] represents a documented opportunity — would you like to include it in the next cycle's scope?"

---

#### ترقية إلى Enterprise (إذا Health Score > 75)

**بالعربية:**

"بناءً على الحجم التشغيلي لعملياتكم ودرجة الصحة المرتفعة، نرى أن الشريحة المؤسسية (4,999 ريال/شهر) تُناسب مرحلة النضج التي وصلتموها. الفارق: [وصف ما تضيفه الشريحة المؤسسية]. القيمة التقديرية للإضافة تفوق فارق التكلفة — هذا تقدير قائم على النمط، لا ضمان."

**In English:**

"Based on your operational volume and strong health score, we see the Enterprise tier (4,999 SAR/month) as suited to the maturity stage you have reached. The difference: [describe Enterprise additions]. The estimated incremental value exceeds the cost delta — this is a pattern-based estimate, not a guarantee."

---

#### استجابة الخطر (Health Score < 55)

**بالعربية:**

"درجة الصحة [X/100] تستوجب محادثة صريحة قبل التجديد. نقترح جلسة مراجعة تشغيلية مدتها 45 دقيقة لتشخيص العائق الفعلي. بناءً على تشخيص المشكلة نُحدد: هل التجديد بالوضع الحالي يُنتج قيمة، أم نحتاج لتعديل النطاق أو الأولويات."

**In English:**

"A health score of [X/100] warrants an honest conversation before renewal. We propose a 45-minute operational review session to diagnose the actual obstacle. Based on the diagnosis we determine: does renewal as-is produce value, or do we need to adjust scope or priorities."

---

#### بروتوكول منع الإلغاء

- التدخل الأول: جلسة مراجعة تشغيلية (تشخيصية، لا بيعية)
- التدخل الثاني: عرض تجديد مُعدَّل بناءً على نتائج الجلسة
- لا تدخل ثالث — إذا لم تُغلَق: أغلق نظيفاً

---

### الشريحة المؤسسية — Enterprise: 4,999 ريال/شهر

#### سكريبت التجديد القياسي

**بالعربية:**

"مراجعة الدورة الكاملة: [قائمة المخرجات الموثّقة]. درجة الصحة: [X/100]. الأصول الرأسمالية: [Z أصلاً]. الأثر الموثّق في حزمة الإثبات يُغطي [الأبعاد التشغيلية الرئيسية]. نوصي بتجديد الشريحة المؤسسية. هل هناك أولويات استراتيجية جديدة للدورة القادمة نُدرجها في نطاق العمل؟"

**In English:**

"Full cycle review: [list documented outputs]. Health score: [X/100]. Capital assets: [Z assets]. Documented impact in the Proof Pack covers [key operational dimensions]. We recommend renewing the Enterprise tier. Are there new strategic priorities for the next cycle to include in the scope?"

---

#### ترقية إلى Custom AI أو مشروع توسع

**بالعربية:**

"في المرحلة القادمة، نرى فرصة موثّقة لبناء [وصف النظام أو القدرة المحددة — Custom AI أو توسع في قطاع آخر]. هذا يتجاوز نطاق الشريحة الحالية ويستحق نقاشاً منفصلاً حول النطاق والميزانية. هل نُدرج ذلك كاستشارة مجانية ضمن جلسة التجديد؟"

**In English:**

"In the next phase, we see a documented opportunity to build [describe specific system or capability — Custom AI or sector expansion]. This exceeds the current tier's scope and warrants a separate scoping and budget discussion. Shall we include it as a complimentary consultation within the renewal session?"

---

#### استجابة الخطر (Health Score < 55)

**بالعربية:**

"عقد المؤسسية يستحق مراجعة تفصيلية قبل أي قرار. نقترح تشكيل فريق مراجعة مشترك (من الجانبين) لمدة أسبوع لتقييم: ما الذي نجح فعلاً، ما الذي لم ينجح، وما الإجراء التصحيحي اللازم. لا تجديد قبل اكتمال هذه المراجعة."

**In English:**

"An Enterprise contract warrants a detailed review before any decision. We propose forming a joint review team (from both sides) for one week to assess: what actually worked, what did not, and what corrective action is required. No renewal before this review is complete."

---

#### بروتوكول منع الإلغاء

- التدخل الأول: مراجعة تشغيلية مشتركة (لا بيعية)
- التدخل الثاني: عرض تجديد مُعدَّل أو مقترح إعادة هيكلة
- لا تدخل ثالث — قرار العميل نهائي بعد التدخلين

---

## القسم الرابع — مقاييس التجديد / Section 4: Renewal Metrics

**جميع الأهداف أدناه مستهدفات تشغيلية تقديرية — ليست ضمانات.**

---

### KPIs الأساسية

| المؤشر | التعريف | الهدف التشغيلي (تقديري) |
|---|---|---|
| صافي الاحتفاظ بالإيرادات (NRR) | (إيرادات نهاية الفترة من العملاء الموجودين ÷ إيرادات بداية الفترة) × 100 | > 105% |
| إجمالي الاحتفاظ بالإيرادات (GRR) | (إيرادات المحتفَظ بها بعد الخسائر ÷ إيرادات بداية الفترة) × 100 | > 90% |
| متوسط وقت إشعار التجديد المبكر | متوسط الأيام من بدء محادثة التجديد حتى التوقيع | 30 - 45 يوماً |
| معدل تحويل الترقية | (عمليات الترقية المُنجَزة ÷ فرص الترقية المُقدَّمة) × 100 | > 35% (تقديري) |
| معدل الاحتفاظ بالعملاء السنوي | (عدد العملاء المُجدِّدين ÷ إجمالي العقود المنتهية) × 100 | > 85% (تقديري) |

---

### تصنيف أسباب الإلغاء — Churn Reason Taxonomy

كل إلغاء يُوثَّق بسبب رئيسي واحد من القائمة أدناه. البيانات تُستخدم لتحسين العرض والتشغيل — لا للمساءلة الفردية.

| الرمز | السبب | التعريف |
|---|---|---|
| PRICE | السعر | العميل يرى الفجوة السعرية أكبر من القيمة الموثّقة |
| VALUE | القيمة | القيمة الموثّقة أقل من التوقعات — Health Score كان منخفضاً |
| COMPETITOR | منافس | العميل انتقل لحل آخر |
| INTERNAL | داخلي | تغيير في هيكل الشركة، ميزانية، أو أولويات استراتيجية |
| DISSOLVED | انحلال | الشركة أُغلقت أو اندمجت |

**التقرير الشهري:** راجع توزيع الإلغاءات بهذه الرموز. نمط PRICE أو VALUE المتكرر يُشير لمشكلة في التسليم أو التسعير — ليس في المبيعات.

---

## القسم الخامس — غير قابل للتفاوض في التجديد / Section 5: Non-Negotiables in Renewal

### القائمة

1. **لا وعود بنتائج مضمونة** — يُحظر تقديم أي ادعاء من نوع "نضمن لك X في الدورة القادمة." المسموح: "قدّرنا X بناءً على النمط الموثّق."

   **No guaranteed outcome promises** — It is prohibited to make any claim of the form "we guarantee you X in the next cycle." Permitted: "we estimate X based on the documented pattern."

2. **لا إعادة تفعيل باردة** — إذا أُغلق عقد وانتهت العلاقة، لا يمكن إعادة التواصل إلا عبر نماذج التواصل المعتمدة. لا رسائل غير رسمية أو WhatsApp خارج السياق الموافَق عليه.

   **No cold re-activation** — If a contract is closed and the relationship ended, re-engagement is only via approved outreach templates. No informal messages or WhatsApp outside the approved context.

3. **جميع عروض التجديد تمر بوابة APPROVAL_FIRST** — العرض يُصنَّف مسودة حتى تُراجَع من المؤسس وتُوثَّق موافقته قبل الإرسال.

   **All renewal proposals pass through the APPROVAL_FIRST gate** — The proposal remains a draft until reviewed by the founder and approval is logged before sending.

4. **حزمة الإثبات مُرفقة في كل عرض تجديد** — لا يُرسَل عرض تجديد بدون حزمة إثبات كاملة ومحدَّثة مرفقة. هذا إلزامي، لا اختياري.

   **Proof Pack must be attached to every renewal proposal** — No renewal proposal is sent without a complete, up-to-date Proof Pack attached. This is mandatory, not optional.

5. **الإغلاق النظيف محترم** — إذا قرر العميل عدم التجديد بعد التدخلين المسموح بهما، يُغلَق الملف بشكل محترم مع تسليم البيانات والأصول للعميل وتوثيق الدرس.

   **Clean closure is respected** — If the client decides not to renew after the permitted two interventions, the file is closed respectfully with data and assets delivered to the client and the lesson documented.

---

## ملحق: نموذج تسجيل التجديد — Renewal Record Template

```text
رقم العقد / Contract ID: ___________
تاريخ التجديد / Renewal Date: ___________
الشريحة / Tier: [ ] Essential 2,999 [ ] Professional 3,999 [ ] Enterprise 4,999
درجة الصحة عند يوم -90 / Health Score at Day -90: ___ / 100
درجة الصحة عند يوم -30 / Health Score at Day -30: ___ / 100
درجة الإثبات / Proof Score: ___ / 100
حزمة الإثبات مرفقة / Proof Pack attached: [ ] نعم / Yes
عرض الترقية مُقدَّم / Upgrade pitch presented: [ ] نعم / Yes [ ] لا / No
نتيجة التجديد / Renewal outcome:
  [ ] تجديد بنفس الشريحة / Renewed same tier
  [ ] ترقية / Upgraded to ___________
  [ ] إلغاء — السبب / Cancelled — reason: ___________
ملاحظات المؤسس / Founder notes: ___________
```

---

> مرجع متقاطع للأدوات التشغيلية:
> - معايير إثبات القيمة: [`docs/08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md`](../08_value_os/ESTIMATED_OBSERVED_VERIFIED_VALUE.md)
> - سياسة القنوات: [`docs/05_governance_os/CHANNEL_POLICY.md`](../05_governance_os/CHANNEL_POLICY.md)
> - معايير جودة البيانات: [`docs/04_data_os/DATA_QUALITY_SCORE.md`](../04_data_os/DATA_QUALITY_SCORE.md)

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
