# دليل قطاع — شركات اللوجستيك — Logistics Companies Playbook

> دليل تشغيلي داخلي (شحن، توصيل أخير، نقل، تخزين، مناولة). كل الرسائل **مسودات** ترسَل يدوياً. لا إرسال آلي، لا قوائم مشتراة، لا ضمانات.
> Internal operating playbook (freight, last-mile, transport, warehousing, fulfillment). Every message is a DRAFT sent manually. No auto-send, no purchased lists, no guarantees.
>
> المرجع: [README القطاعات](README.md) · [حزم RevOps](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) · [الكتالوج](../../autonomous_growth/product_catalog.py)

---

## 1. الألم الرئيسي / Core pain

**عربي:** شركة اللوجستيك تتعامل مع حسابات شحن B2B وعروض أسعار ومناقصات متكررة، لكن خط الفرص ثقيل ومبعثر: طلبات عروض أسعار قديمة بلا متابعة، حسابات شحن كبيرة بلا مراجعة دورية، ومناقصات تُكتشف متأخرة. فريق المبيعات يلاحق الجديد ويهمل توسيع الحسابات القائمة. النتيجة: حجم شحن متكرر قابل للنمو يُترك بلا تفعيل.

**English:** A logistics company handles recurring B2B shipping accounts, quotes, and tenders, but the pipeline is heavy and scattered: aging quote requests with no follow-up, large shipping accounts without periodic review, and tenders spotted late. Sales chases new business while existing-account expansion is neglected. Result: recurring, growable shipping volume left unactivated.

---

## 2. صاحب القرار / Decision maker

- **الأساسي:** مدير المبيعات التجارية / مدير تطوير الأعمال. — Commercial sales / business development director.
- **المؤثّر:** مدير الحسابات الرئيسية (Key Accounts). — Key accounts manager.
- **مهم:** من يملك بيانات الـ CRM/التسعير. — Whoever owns CRM/pricing data.

---

## 3. مؤشرات أن العميل مناسب / Good-fit signals

- قاعدة حسابات شحن B2B متكررة + عروض أسعار. — Recurring B2B shipping accounts plus quotes.
- خط مناقصات/عقود يحتاج تتبّعاً وأولوية. — Tender/contract pipeline needing tracking and priority.
- يشكو من «حسابات كبيرة ما نراجعها بانتظام». — "Big accounts we don't review regularly."
- بيانات موجودة لكن ثقيلة وغير مرتّبة. — Data exists but heavy and unorganized.

---

## 4. مؤشرات أنه غير مناسب / Disqualifiers

- يطلب scraping لشركات أو قوائم مشتراة — نرفض. — Wants company scraping or purchased lists — declined.
- يريد ضمان حجم شحن أو عقود. — Wants guaranteed volume or contracts.
- لا حسابات B2B ولا خط عروض أسعار. — No B2B accounts, no quote pipeline.
- يبحث عن نظام تتبّع شحنات تشغيلي (TMS) — ليس نطاقنا. — Wants an operational shipment-tracking system (TMS) — not our scope.

---

## 5. أول منتج نبيعه / First product to sell

**Lead Intelligence Sprint — 9,500 ريال** (حتى 500 صف حساب، dedupe، scoring، Top 50، حتى 20 مسودة).
المصدر: [DEALIX_REVOPS_PACKAGES_AR.md](../commercial/DEALIX_REVOPS_PACKAGES_AR.md) · [العرض](../commercial/OFFER_LEAD_INTELLIGENCE_SPRINT_AR.md).

- **لماذا:** البيانات أثقل وحسابات B2B أكبر قيمة؛ dedupe وscoring وTop 50 على الحسابات وطلبات عروض الأسعار يُخرج قيمة مباشرة (أي حساب يستحق المراجعة/التوسعة أولاً).
- **بديل أخف للبداية:** Revenue Intelligence Sprint (499) كاختبار على قائمة حسابات أصغر — [الكتالوج](../../autonomous_growth/product_catalog.py).
- **مدخل مجاني:** Free Diagnostic (0).

> لا تُسعّر خارج هذه الأرقام. لا تقفز لـ Pilot (22,000) قبل حدث إثبات.

---

## 6. زاوية الرسالة / Message angle

**عربي:** «نمِّ الحسابات القائمة قبل مطاردة الجديد». الرسالة: أكبر فرصة غالباً في حساباتكم الحالية وطلبات عروض الأسعار المعلّقة، لا في ليدز جديدة باردة. نرتّب القاعدة الثقيلة ونحدد Top 50 — لا نعد بحجم شحن.

**English:** "Grow existing accounts before chasing new ones." The angle: the biggest opportunity usually sits in current accounts and aging quote requests, not cold new leads. We organize the heavy base and surface a Top 50 — not a shipping-volume promise.

---

## 7. اعتراضات متوقعة / Expected objections (+ safe responses)

| الاعتراض | رد آمن (لا ضمانات) |
|---|---|
| «بياناتنا ضخمة ومعقدة» | «الـ Sprint يبدأ بنطاق متفق عليه (حتى 500 صف) ويثبت القيمة قبل التوسع في العقد.» |
| «هل تضمنون حجم شحن؟» | «لا نضمن أرقاماً. نسلّم Top 50 حساباً مرتّباً ومسودات، والإغلاق على فريقكم.» |
| «عندنا CRM/نظام تشغيل» | «لا نستبدله — نرتّب طبقة الفرص فوقه: dedupe وscoring وأولوية مراجعة.» |
| «نخاف على بيانات عملائنا» | «تحت DPA، داخلي فقط، بلا إرسال خارجي ولا scraping.» |

---

## 8. الدليل المطلوب / Proof required (L0–L5)

- **أول لمسة:** PDPL + تموضع (طبقة 1–2) — **L0/L1**، عيّنات فقط.
- **بعد رد إيجابي:** عيّنة Proof Pack + تقرير عيّنة بلا بيانات — **L1**.
- **بعد التسليم:** تسليم Sprint = **L1**؛ موافقة مسودة = **L2**.
- **حالة نجاح:** لا أرقام حجم/عقود منسوبة قبل **L4/L5** بموافقة موقّعة.

---

## 9. أول workflow للتنفيذ / First workflow to run

1. تأهيل + تحديد نطاق البيانات (حتى 500 صف). — Qualify; scope the data (up to 500 rows).
2. اتفاق Lead Intelligence Sprint (9,500) بـ SOW قصير وDPA. — Agree the 9,500 Sprint with a short SOW and DPA.
3. استلام تصدير حسابات/عروض أسعار/مناقصات. — Receive accounts/quotes/tenders export.
4. dedupe + scoring + Top 50 حساباً + إشارات استحقاق المراجعة. — Dedupe, score, Top 50 accounts, review-due signals.
5. توليد حتى 20 **مسودة** تواصل تجاري (لا إرسال). — Up to 20 commercial outreach DRAFTS.
6. تقرير تنفيذي + لوحة pipeline مصغّرة + تسجيل الإثبات. — Executive report, mini pipeline board, proof logged.

---

## 10. رسائل عربية جاهزة / Ready Arabic messages (مسودات فقط)

**أول تواصل:**
«مساء الخير [الاسم]. شركات اللوجستيك غالباً أكبر فرصها داخل حساباتها القائمة وطلبات عروض الأسعار المعلّقة، لا في ليدز جديدة. نرتّب القاعدة (dedupe + scoring) ونحدد Top 50 حساباً يستحق المراجعة أو التوسعة، مع مسودات تواصل — نطاق معتمد 9,500 ريال، مخرجات داخلية فقط. تستحق 15 دقيقة؟»

**متابعة 1:**
«[الاسم]، متابعة سريعة. أقدر أرسل تقرير عيّنة (بدون أي بيانات) يبين شكل الترتيب وTop 50. تناسبك مكالمة قصيرة هالأسبوع؟»

**متابعة 2:**
«[الاسم]، باختصار: نرتّب حساباتكم الثقيلة ونبرز الأعلى أولوية للمراجعة، 9,500 ريال (أو سبرينت اختبار 499 أولاً)، مسودات لموافقتكم بلا إرسال خارجي. أرد متى ما ناسبك.»

**الإغلاق (Breakup):**
«[الاسم]، ما أبي أثقّل عليك. أغلق الموضوع وأبقى متاحاً لو حبيتم ترتيب قاعدة الحسابات لاحقاً. شكراً ووفقكم.»

---

## 11. رسائل إنجليزية جاهزة / Ready English messages (DRAFTS only)

**First touch:**
"Hi [Name]. For logistics companies, the biggest opportunity usually sits inside existing accounts and aging quote requests, not new leads. We organize the base (dedupe + scoring) and surface a Top 50 of accounts due for review or expansion, with outreach drafts — approved scope 9,500 SAR, internal outputs only. Worth 15 minutes?"

**Follow-up 1:**
"[Name], quick nudge. I can share a sample report (no data at all) showing the ranking and Top 50 format. Would a short call this week work?"

**Follow-up 2:**
"[Name], in short: we organize your heavy account base and surface the highest-priority for review — 9,500 SAR (or a 499 test sprint first), drafts for your approval, no external send. Reply whenever suits."

**Breakup:**
"[Name], I won't keep nudging. I'll close this and stay available if organizing the account base becomes useful later. Thanks, and best of luck."

---

## 12. أسئلة discovery / Discovery questions

1. كم حساب شحن B2B نشط لديكم تقريباً؟ — Roughly how many active B2B shipping accounts?
2. كيف تراجعون الحسابات الكبيرة اليوم، وبأي وتيرة؟ — How and how often do you review large accounts?
3. ماذا يحدث لطلب عرض سعر بلا رد؟ — What happens to a quote request with no reply?
4. كيف تكتشفون المناقصات، وهل تُتابَع منهجياً؟ — How are tenders discovered and tracked?
5. ما تقدير التكرار والبيانات القديمة في القاعدة؟ — Estimated duplication and stale data?
6. من سيستخدم Top 50 ولوحة الأولوية؟ — Who will use the Top 50 and priority board?

---

**القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
