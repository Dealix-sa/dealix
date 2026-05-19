# Dealix — Master Launch & Commercialization Plan — خطة التدشين والتسويق التجاري الأم
<!-- PHASE 12 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> **قاعدة ذهبية:** بِع قبل أن تبني. التجميد يمنع بناء منتج جديد، لا يمنع
> التخطيط الكامل ولا البيع بقوة. كل مكينة تنتقل من اليدوي إلى الآلي فقط بعد
> أن تكرّر نسختها اليدوية بإثبات موثّق. لا ترقية على الإحساس — على بوابة معلنة.

> **تنبيه — لا ضمانات.** كل الأرقام والمسارات في هذا المستند **أهداف تشغيلية لا
> ضمانات تجارية**. أي رقم لم يتحقق = `insufficient_data`. الدرجتان 0–1 من سلم
> العروض مُسلّمتان عبر منتج مُتحقَّق منه؛ الدرجات 3–5 **بقيادة المؤسس / شبه-مؤتمتة**
> اليوم. هذا المستند هو **العمود الفقري** — يربط ولا يُعيد التسعير ولا الـSOP.

---

## 0) السياق — لماذا هذه الخطة · Context

Dealix **مُدشَّن تقنياً**: المنصة حيّة على `api.dealix.me`، صفحة الهبوط حيّة،
117 موجِّه API، 3,881 اختباراً، 9 وحدات تشغيل (OS modules)، سلّم عروض من 6 درجات،
خطة 90 يوماً، وحزمة بيع/محتوى كاملة. ثلاث حقائق حاسمة تُبنى الخطة حولها:

1. **تجميد تجاري نشِط** (بدأ 2026-05-16). العقيدة: *المنصة جاهزة؛ القيد لم يعد
   الكود بل البيع بقيادة المؤسس — كل ساعة بناءٍ بدل البيع لها قيمة متوقّعة سالبة.*
   المسموح: بيع بقيادة المؤسس، أصول بيع، إنهاء تسليم الدرجتين 0–1، إغلاق أول Pilot
   مدفوع. انظر [`docs/ops/COMMERCIAL_FREEZE.md`](ops/COMMERCIAL_FREEZE.md)
   و[`docs/sales-kit/CONDITIONAL_BUILD_TRIGGERS.md`](sales-kit/CONDITIONAL_BUILD_TRIGGERS.md).
2. **قيد إيراد واحد:** تفعيل حساب الدفع Moyasar — إجراء يدوي للمؤسس. لا كود ولا
   وكيل يستطيع إنجازه. حتى يكتمل، **لا يمكن تحصيل 0 ريال**.
3. **تضارب سردي:** أصول قديمة (عرض المستثمر، `docs/ops/launch_content_queue.md`)
   تبيع *«مندوب AI يرد في 45 ثانية ويحجز تلقائياً»* بـ*«1 ريال»*؛ العقيدة الحالية
   تبيع *«رادار عمليات محكوم، مسودات وموافقة أولاً، لا إرسال تلقائي»* بـ499 ريال.
   الادعاءات القديمة تخالف `dealix/registers/no_overclaim.yaml`.

**التوفيق التنفيذي.** الطموح والتجميد ليسا في تعارض لو رُتِّبا بشكل صحيح. هذه الخطة
تُسلّم **وجهة الـfull-ops كاملة** كمخطط متدرّج مُبوَّب: بِع أولاً، أثبِت الطلب، ثم
أتمِت — كل مكينة تُفعَّل فقط بعد أن تكرّر نسختها اليدوية بإثبات.

> Dealix is technically launched; the binding constraint is founder-led selling,
> not code. This plan delivers the full-ops destination as a gated, sequenced
> blueprint: sell first, prove demand, then automate — manual mode before
> automated mode, on a stated trigger, never on vibes.

---

## 1) العقيدة الاستراتيجية — 7 مبادئ تشغيل · Strategic Doctrine

| # | المبدأ | Principle |
|---|--------|-----------|
| 1 | **بِع قبل أن تبني.** خلال التجميد، الهندسة = تحقّق/إصلاح فقط. أي أتمتة جديدة = الأفق 4، مُبوَّبة. | Sell before you build. |
| 2 | **سرد واحد.** رادار عمليات محكوم · موافقة أولاً · مسودات لا إرسال تلقائي · دخول 499 ريال. كل ادعاء «45 ثانية / 1 ريال / حجز تلقائي» مهجور. | One narrative. |
| 3 | **الإثبات هو المنتج.** كل ارتباط ينتهي بـProof Pack من 14 قسماً + أصل واحد قابل لإعادة الاستخدام في Capital Ledger. لا إثبات → لا upsell ولا case study. | Proof is the product. |
| 4 | **انزل منخفضاً، توسّع عالياً.** تشخيص مجاني → Sprint بـ499 ريال يُثبّت؛ الدرجات 3–5 تُوسِّع. NRR هو نجم الشمال. | Land low, expand high. |
| 5 | **المال محكوم.** لا شحنة حيّة، خصم، استرداد، أو دفعة بلا موافقة بشرية مُسجَّلة. كل ريال يمرّ عبر سجل. | Money is governed. |
| 6 | **احترم الـ11 غير قابلة للتفاوض** — مفروضة في الكود (`safe_send_gateway/doctrine.py`). | Honor the 11 non-negotiables. |
| 7 | **بوّب كل تصعيد.** كل أفق وكل «مكينة» تُفتح فقط على محفّز معلن وقابل للقياس. | Gate every escalation. |

---

## 2) المكاين التسع — معمارية الـFull-Ops · The 9 Machines

وجهة «الـfull-ops المؤتمتة بالكامل» = 9 مكاين. لكلٍّ **وضع يدوي (الآن، آمن للتجميد)**
و**وضع آلي (الأفق 4، مُبوَّب)**. الجدول هو الخريطة الأم؛ الأفق يُرتِّب التفعيل.

| # | المكينة · Machine | الوضع اليدوي الآن — Manual mode (freeze-safe) | الوضع الآلي — Automated mode (Horizon 4, gated) | الوكيل المالك |
|---|-------------------|-----------------------------------------------|--------------------------------------------------|----------------|
| 1 | **المبيعات · Sales** | المؤسس يُغلق؛ الوكيل يُؤهّل ويُحضِّر العروض/التواصل للموافقة | تسجيل نقاط آلي، تصيير عروض آلي، طابور مسودات متسلسل | `dealix-sales` |
| 2 | **التسويق/السلطة · Marketing** | المؤسس ينشر؛ الوكيل يُحضِّر إيقاع LinkedIn ومحتوى case مجهول | محرك محتوى مجدوَل من السجلات، تقارير معايير | `dealix-content` |
| 3 | **التسليم · Delivery** | الوكيل يُشغّل خطوات Sprint السبعة؛ المؤسس يوافق على الإرسال | خط تسليم مُقولَب، تجميع Proof Pack آلي | `dealix-delivery` |
| 4 | **الإثبات · Proof** | تجميع Proof Pack لكل ارتباط، مراجعة يدوية | التقاط أحداث إثبات آلي → توليد حزمة → مصنع case | `proof_ledger` / `proof_os` |
| 5 | **المال/RevOps** | فاتورة Moyasar يدوية، ZATCA يدوي، قيود سجل | فاتورة آلية عند `paid`، تسوية فوترة، متابعة تحصيل | `capital_os` + `payment_ops` |
| 6 | **الشركاء/Affiliate** | مكالمات شركاء بقيادة المؤسس؛ تتبّع إحالة يدوي | بوابة شركاء، سجل affiliate، عمولة-بعد-الدفع آلية | `partnership_os` |
| 7 | **الحوكمة · Governance** | طابور موافقات يدوي، فحوص doctrine في الكود | مركز موافقات بـTTL، حفظ سجل تدقيق، محرك سياسات | `governance_os` |
| 8 | **الذكاء/المعايير · Intelligence** | مراجعة أسبوعية يدوية، تجميع مقاييس يدوي | محرك معايير بتجميع آلي، تقارير «State of…» | `intelligence_os` |
| 9 | **التنظيم/التوظيف · Org** | المؤسس منفرد؛ الوكلاء هم الفريق | أول تعيين تسليم عند MRR ≈ 50–100 ألف دولار، ثم RevOps | `dealix-pm` |

**القائد · Conductor:** `dealix-pm` يُنسّق المكاين التسع جميعاً — يملك خطة الـ90 يوماً،
الإيقاع الأسبوعي، بوابات القرار، ومراجعة سجل الاحتكاك.

---

## 3) الآفاق الخمسة — التنفيذ المتدرّج · The 5 Horizons (0–4)

### الأفق 0 — فكّ قيد الإيراد · Unblock Revenue (الأيام 0–3) · آمن للتجميد

الهدف: إزالة كل قيد غير-بيعي ليبيع المؤسس بنظافة.

| الإجراء | المالك | المُخرَج |
|---------|--------|----------|
| وسم تفعيل Moyasar كمسار حرج #1 | `dealix-pm` → المؤسس | المؤسس يُكمل KYC/تفعيل Moyasar (يدوي، خارج النظام). حتى يكتمل، الإيراد = مُعطَّل. |
| توحيد السرد | `dealix-content` | تحرير الأصول الحيّة للعقيدة الحالية؛ إهجار «45 ثانية / 1 ريال / حجز تلقائي». إعادة فحص مقابل `no_overclaim.yaml`. |
| تقييم بوابة الجاهزية | `dealix-pm` + `dealix-engineer` | تشغيل `scripts/*_verify.sh` وفحوص `readiness/`؛ تقرير جاهزية أخضر/أحمر. |
| التحقق من تسليم الدرجتين 0–1 | `dealix-delivery` | تأكيد أن التشخيص المجاني وSprint الـ499 يُنتج كلٌّ منهما مُخرجاً حقيقياً جاهزاً للعميل من الطرف للطرف. |
| كتابة وثائق الخطة المرافقة | `dealix-content` | هذا المستند + `REVENUE_OPS_AND_MONEY_PLAN.md` + سدّ فجوتي `AFFILIATE_GOVERNANCE.md` و`DISTRIBUTION_DASHBOARD.md`. |

**بوابة الخروج → الأفق 1:** Moyasar مُفعَّل **و** السرد موحَّد **و** تقرير الجاهزية أخضر للدرجتين 0–1.

### الأفق 1 — أول إثبات مدفوع · First Paid Proof (الأيام 4–30) · آمن للتجميد

الهدف: المؤسس يُغلق شخصياً أول 1–3 عملاء دافعين؛ يُنتِج أول Proof Pack وأول case مجهول.

- `dealix-sales`: تأهيل القائمة الدافئة 20–50 عبر `sales_os/qualification.py`؛ تصيير عروض Sprint الـ499؛ صياغة تواصل دافئ **في طابور موافقة المؤسس** (لا إرسال تلقائي أبداً).
- المؤسس: إرسال التواصل الموافَق عليه، إجراء التشخيصات، إغلاق أول Sprint بـ499.
- `dealix-delivery`: تشغيل Sprint ذكاء الإيرادات السبعة أيام؛ تجميع Proof Pack من 14 قسماً؛ تسجيل ≥1 أصل في Capital Ledger.
- `dealix-content`: أول منشور case-style مجهول؛ بدء إيقاع LinkedIn.
- المال: أول فاتورة Moyasar + سجل ZATCA؛ تسجيل في سجلّي capital وproof.
- الأهداف (أهداف لا ضمانات): 3 تشخيصات، 1–3 Sprints مدفوعة، 1 Proof Pack، MRR ≥ 499 ريال.

### الأفق 2 — إيراد قابل للتكرار · Repeatable Revenue (الأيام 31–60) · آمن للتجميد

الهدف: تحويل فوز واحد إلى حركة قابلة للتكرار.

- 3 Sprints متوازية (حدّ التزامن على سعة المؤسس).
- أول upsell: Sprint → Data-to-Revenue Pack أو Managed Revenue Ops.
- أول 1–2 محادثة شريك-وكالة ([`docs/AGENCY_PARTNER_PROGRAM.md`](AGENCY_PARTNER_PROGRAM.md)).
- ملاحظة التسعير: سجّل كل اعتراض؛ لا تخصم — خفّض النطاق.
- الأهداف: 5 pilots إجمالاً، 2 Managed Ops، MRR ~5,998 ريال، 1–2 case study.

### الأفق 3 — التوسّع ومحفّز البناء المشروط · Scale (الأيام 61–90) · آمن للتجميد

الهدف: استقرار الـretainers و**اكتساب حقّ الأتمتة**.

- 10 عملاء إجمالاً، 3 retainers، 2 case study منشورة (بموافقة)، أول lead من شريك.
- `dealix-pm` يُقيّم [`CONDITIONAL_BUILD_TRIGGERS.md`](sales-kit/CONDITIONAL_BUILD_TRIGGERS.md): هل تكرّر نفس الـworkflow 3+ مرّات بإثبات؟ هل الطلب حقيقي؟ إن نعم → تجهيز **مقترح رفع تجميد انتقائي** لتوقيع المؤسس.
- الأهداف: MRR 8,997–14,997 ريال؛ قياس معدّل Sprint→retainer.

### الأفق 4 — أتمتة الـFull-Ops · Full-Ops Automation (بعد 90 يوماً) · مُبوَّب — يتطلّب رفع تجميد

ابنِ **فقط** المكاين التي كرّرت نسختها اليدوية 3+ مرّات بإثبات، بهذا الترتيب:

1. **مكينة المال أولاً** — فوترة آلية عند `paid`، أتمتة ZATCA، تسوية فوترة، متابعة تحصيل. (أعلى رافعة، أدنى خطر.)
2. **مكينة الإثبات** — التقاط أحداث إثبات آلي → تجميع Proof Pack → تغذية مصنع الـcase.
3. **مكينة المبيعات** — تسجيل نقاط + تصيير عروض + طابور مسودات (يبقى موافقة-أولاً؛ copilot قبل autopilot).
4. **مكينة التسليم** — خط Sprint مُقولَب.
5. **التسويق/السلطة** — محرك محتوى مجدوَل + محرك معايير.
6. **الشركاء/Affiliate** — بوابة شركاء + سجل affiliate (عمولة فقط بعد `invoice_paid`).
7. **الحوكمة** — حفظ مركز الموافقات، سجل تدقيق إلى Postgres، محرك سياسات. **الذكاء** — تجميع مقاييس آلي + تقرير «State of…».
8. **التنظيم** — أول تعيين تسليم عند MRR ≈ 50–100 ألف دولار مكافئ.

كل تفعيل قرار مُبوَّب منفصل؛ `dealix-engineer` يُفعَّل هنا فقط، بموجب رفع التجميد.

```text
H0 فكّ القيد ──▶ H1 أول إثبات مدفوع ──▶ H2 إيراد متكرّر ──▶ H3 توسّع ──▶ H4 full-ops
   3 أيام            30 يوماً               60 يوماً         90 يوماً     بعد 90 (مُبوَّب)
   آمن للتجميد ───────────────────────────────────────────────▶  رفع تجميد مطلوب
```

---

## 4) نموذج تنسيق الوكلاء · Agent Orchestration Model

| الوكيل | الدور (تشبيه تنفيذي) | التفويض خلال التجميد |
|--------|----------------------|-----------------------|
| `dealix-pm` | رئيس الأركان / COO | يملك خطة الـ90 يوماً، الإيقاع الأسبوعي، كل البوابات، سجل الاحتكاك؛ يقود بقية الوكلاء |
| `dealix-sales` | نائب رئيس المبيعات | تأهيل، تصيير عروض، صياغة تواصل للموافقة؛ لا يُرسِل أبداً |
| `dealix-delivery` | نائب رئيس التسليم | تشغيل Sprint السبعة أيام، تجميع Proof Packs، تسجيل الأصول |
| `dealix-content` | نائب رئيس التسويق | محتوى ثنائي اللغة، السلطة، توحيد السرد، دراسات الحالة |
| `dealix-engineer` | نائب رئيس الهندسة | **تحقّق/إصلاح فقط** خلال التجميد؛ يُفعَّل للأفق 4 |

انطلاق التنفيذ = `dealix-pm` يُشغّل الأفق 0، ثم يقود الأفق 1 فما بعد، مُفوِّضاً
للوكلاء المتخصّصين. كل فعل خارجي (إرسال، شحن، نشر) يتوقّف عند المؤسس للموافقة.

---

## 5) سجل المخاطر وبوابات القرار · Risk Register & Decision Gates

| المخاطرة · Risk | الأثر | التخفيف |
|-----------------|-------|----------|
| Moyasar غير مُفعَّل | الإيراد = 0 | أولوية المؤسس #1؛ `dealix-pm` يحجب الأفق 1 حتى الإنجاز |
| استمرار تضارب السرد | خطر ثقة / مبالغة / قانوني | توحيد السرد في الأفق 0 قبل أي تواصل |
| خرق التجميد (بناء > بيع) | وقت بقيمة متوقّعة سالبة | `dealix-engineer` مُقيَّد؛ البوابات تفرض |
| البناء بلا طلب | رأس مال مهدور | محفّزات بناء مشروط؛ الأفق 4 مُبوَّب |
| سعة المؤسس | انزلاق التسليم | حدّ Sprints المتزامنة؛ أول تعيين عند محفّز MRR |
| عدم امتثال PDPL / CITC | تنظيمي + فقدان ثقة | تسجيل موافقات، DPA، موافقة-أولاً موجودة في الكود؛ أبقِها |

**البوابات:** H0→H1 (Moyasar + سرد + جاهزية خضراء) · H1→H2 (≥1 Proof Pack مدفوع) ·
H2→H3 (≥5 pilots، ≥2 متكرّر) · H3→H4 (محفّزات البناء المشروط مُستوفاة + رفع تجميد صريح من المؤسس).

---

## 6) المقاييس واللوحات · Metrics & Dashboards

- **لوحة التوزيع اليومية** → [`docs/ops/DISTRIBUTION_DASHBOARD.md`](ops/DISTRIBUTION_DASHBOARD.md) (رسائل، ردود، demos، scopes، فواتير، مدفوع، Proof Packs، مخاطر محجوبة).
- **المراجعة التشغيلية الأسبوعية** → [`docs/meetings/WEEKLY_OPERATING_REVIEW.md`](meetings/WEEKLY_OPERATING_REVIEW.md).
- **مقاييس نجم الشمال:** MRR، NRR، زمن-الوصول-للإثبات (هدف <48 ساعة في الـpilots)، معدّل Sprint→retainer، النقد المُحصَّل.
- **قواعد التشخيص:** 7 أيام بلا ردود → غيّر الشريحة/الرسالة · ردود بلا demos → غيّر الـCTA · demos بلا مدفوع → غيّر العرض/السعر/الإثبات.

> Metrics roll up daily into the Distribution Dashboard and weekly into the
> Operating Review. MRR and NRR are the north-star pair; every number not yet
> achieved is reported as `insufficient_data`, never as a guarantee.

---

## 7) الأفق 4 — خطة البناء التكتيكية للأتمتة الكاملة · Horizon 4 Tactical Build Plan

> **قاعدة ذهبية:** «كل شيء أوتوماتيكي» = خط الأنابيب الداخلي يُشغّل نفسه من الطرف
> للطرف (التقاط → إثراء → تسجيل → مسودة → تجميع → جدولة → تقرير → تعلّم). أمّا
> الطرف الخارجي غير القابل للتراجع — إرسال، شحن، نشر، صرف عمولة — فيبقى **طابور
> موافقة دائماً**. هذه أتمتة محكومة، لا autopilot — وهي أصل بيع، لا قيد.

النواة موجودة بالفعل: الـOrchestrator، طابور المهام، محرك السياسات، سجل الوكلاء،
الـagent mesh، 11 وكيلاً، جدولة GitHub Actions، والهجرات 101–108. الأفق 4 =
**ربط وإكمال** ما هو مبنيّ، لا بناء من الصفر. كل بناء فرعي مُبوَّب باستقلال:
يُبنى فقط بعد أن تكرّر نسخته اليدوية 3+ مرّات بإثبات.

> "Everything automated" means the internal pipeline self-runs; the external,
> irreversible seam stays a permanent approval queue. Horizon 4 wires and
> completes the existing orchestrator — it is not greenfield, and each sub-build
> is independently gated on its manual version having repeated with proof.

**الارتفاع الاستراتيجي:** عمل المؤسس كلّه = شاشة واحدة (مركز القيادة) — يوافق على
طابور، يقرأ موجزاً. الوكلاء يفعلون الباقي. الهدف: زمن المؤسس التشغيلي < 30 دقيقة/يوم.

### 7.1 ما هو مبنيّ — لا يُعاد بناؤه · Already wired

| القدرة | المكان | الحالة |
|--------|--------|--------|
| Orchestrator + workflow DAG | `orchestrator/runtime.py` (`Orchestrator`، `DAILY_GROWTH_RUN`) | مبنيّ |
| طابور المهام + آلة الحالات | `orchestrator/queue.py` | مبنيّ |
| محرك السياسات + بوابات الموافقة + سقوف الميزانية | `orchestrator/policies.py` | مبنيّ |
| سجل الوكلاء + الدورة الحياتية + صلاحيات الأدوات | `agent_os/` | مبنيّ |
| الـAgent mesh + حدود الثقة | `agent_mesh_os/` | مبنيّ |
| 11 وكيلاً قانونياً | `auto_client_acquisition/agents/` | مبنيّ |
| مكينة الإيراد اليومية (cron) | `.github/workflows/daily-revenue-machine.yml` | مبنيّ (يُجهّز طابوراً، لا يُرسل) |
| بوابة الامتثال + تصنيف الردود + موجز المؤسس | `compliance_os/`، `scripts/dealix_morning_digest.py` | مبنيّ |
| المخططات 101–108 (control_events … improvement_proposals) | `migrations/versions/` | الجداول موجودة |

### 7.2 ترتيب البناء — متسلسل حسب التبعية · Build order

العمود الفقري للحوكمة/السلامة يُبنى أولاً — كل مكينة تعتمد عليه.

```text
H4.1 العمود الفقري للحوكمة ─┬─▶ H4.2 المال ─▶ H4.3 الإثبات ───────────────┐
                            ├─▶ H4.4 إكمال المبيعات + daily-run موحّد ──────┤
                            └─▶ H4.5 التسليم ─▶ H4.6 التسويق/المعايير      ▼
                                              ─▶ H4.7 الشركاء/Affiliate
                                              ─▶ H4.8 التطوّر الذاتي ─▶ H4.9 مركز القيادة
```

### 7.3 المكاين التسع — تكتيكياً · The 9 builds

| البناء | الهدف | الوحدات/الملفات الأساسية | البوابة |
|--------|-------|---------------------------|----------|
| **H4.1 العمود الفقري للحوكمة** | كل خطوة آلية متعاقَدة، مُبوَّبة، مُدقَّقة، قابلة للإيقاف | `governance_os/`، `approval_center/`، `assurance_contract_os/`، `runtime_safety_os/`، `control_plane_os/` | لا بوابة — شرط مسبق، يُبنى أولاً |
| **H4.2 المال / RevOps** | تحصيل النقد يُشغّل نفسه؛ المؤسس يوافق على الصرف فقط | `capital_os/`، `integrations/` (Moyasar، ZATCA)، `payment_ops.py`، `proof_ledger/` | ≥3 فواتير يدوياً |
| **H4.3 الإثبات** | الإثبات يلتقط نفسه؛ Proof Pack يُجمَّع عند الإغلاق | `proof_ledger/`، `proof_os/`، `proof_architecture_os/`، `pack_assembly.py` | ≥3 Proof Packs يدوياً |
| **H4.4 إكمال المبيعات + daily-run موحّد** | اكتشاف → تسجيل → عرض → طابور مسودات متسلسل؛ أمر واحد يُشغّل اليوم | `sales_os/`، `agents/`، `orchestrator/runtime.py`، `automation.py` + `daily_run.py` جديد | ≥5 Sprints بِيعت يدوياً |
| **H4.5 التسليم** | Sprint السبعة أيام يعمل كـworkflow؛ كل خطوة مُخرَج جاهز للموافقة | `orchestrator/runtime.py` (`SPRINT_DELIVERY_RUN` جديد) | ≥3 Sprints سُلّمت يدوياً |
| **H4.6 التسويق/السلطة/المعايير** | المحتوى والمعايير تُولَّد من السجلات | `autonomous_growth/agents/content.py`، `intelligence_os/`، `value_os/`، `growth/` | ≥3 case studies منشورة |
| **H4.7 الشركاء/Affiliate** | تتبّع وعمولة تُشغّل نفسها؛ الصرف مُبوَّب بموافقة | `partnership_os/`، سجل affiliate جديد، `client_os/` | ≥3 صفقات شركاء يدوياً |
| **H4.8 التطوّر الذاتي** | النظام يقترح تحسيناته؛ المؤسس يوافق؛ منخفض-الخطر يُطبَّق آلياً | `self_evolving_os/`، جدول `improvement_proposals` (108)، `self_growth_os/` | ≥30 يوماً تشغيل أفق-4 مستقر |
| **H4.9 مركز القيادة** | شاشة واحدة تُشغّل الشركة | `api/routers/command_center.py`، `control_plane_os/`، لوحة أمامية رفيعة | يُبنى مع H4.4 |

### 7.4 حواجز دائمة — لا تُؤتمَت أبداً · Permanent guardrails

- الإرسال/الشحن/النشر/الصرف الخارجي = **دائماً بموافقة بشرية** — مفروض بـ`assurance_contracts` واختبارات الـ11 غير-قابلة-للتفاوض.
- كل خطوة تُسجَّل في سجل (proof / value_metrics / control_events).
- مفتاح إيقاف لكل وكيل (`runtime_safety`)؛ سقوف ميزانية يومية (`policies.within_budget`).
- لا workflow ذاتي بلا هوية وكيل مُسجَّلة (`agent_os`).

### 7.5 التحقق · Verification

كل الاختبارات القائمة تبقى خضراء — خصوصاً الـ11 غير-قابلة-للتفاوض. اختبار جديد لكل
`WorkflowDefinition`، واختبار فرض `assurance_contracts`، واختبار انتشار مفتاح
الإيقاف. e2e: `/api/v1/daily-run` يُنتج طابور يوم كامل بـ**صفر إرسال تلقائي**.

> Out of scope, deliberately: autopilot external send (permanently forbidden by
> the 11 non-negotiables); multi-tenant SaaS productization (Platform Path,
> post-Horizon-4); stack replacement (reference contracts only).

---

## فهرس مراجع الريبو — Repo Cross-reference Index

| الموضوع | الملف المعتمد |
|---------|----------------|
| المال وRevOps (توسعة الجزء D) | [REVENUE_OPS_AND_MONEY_PLAN.md](REVENUE_OPS_AND_MONEY_PLAN.md) |
| سلم العروض والتسعير (مصدر الأسعار) | [OFFER_LADDER_AND_PRICING.md](OFFER_LADDER_AND_PRICING.md) |
| خطة 90 يوم التنفيذية (مصدر الأهداف) | [90_DAY_BUSINESS_EXECUTION_PLAN.md](90_DAY_BUSINESS_EXECUTION_PLAN.md) |
| التوزيع والتسويق التجاري (فهرس) | [DISTRIBUTION_AND_COMMERCIALIZATION_MASTER.md](DISTRIBUTION_AND_COMMERCIALIZATION_MASTER.md) |
| التجميد التجاري | [ops/COMMERCIAL_FREEZE.md](ops/COMMERCIAL_FREEZE.md) |
| محفّزات البناء المشروط | [sales-kit/CONDITIONAL_BUILD_TRIGGERS.md](sales-kit/CONDITIONAL_BUILD_TRIGGERS.md) |
| حوكمة الـAffiliate | [growth/AFFILIATE_GOVERNANCE.md](growth/AFFILIATE_GOVERNANCE.md) |
| لوحة التوزيع اليومية | [ops/DISTRIBUTION_DASHBOARD.md](ops/DISTRIBUTION_DASHBOARD.md) |
| المراجعة التشغيلية الأسبوعية | [meetings/WEEKLY_OPERATING_REVIEW.md](meetings/WEEKLY_OPERATING_REVIEW.md) |
| برنامج شراكة الوكالات | [AGENCY_PARTNER_PROGRAM.md](AGENCY_PARTNER_PROGRAM.md) |
| ميثاق الثقة والسلامة | [governance/TRUST_SAFETY_CHARTER.md](governance/TRUST_SAFETY_CHARTER.md) |
| غير قابل للتفاوض (الـ11) | [00_foundation/NON_NEGOTIABLES.md](00_foundation/NON_NEGOTIABLES.md) |
| بوابة الموافقات (كود) | `dealix/governance/approvals.py` |
| فرض الـdoctrine (كود) | `auto_client_acquisition/safe_send_gateway/doctrine.py` |

---

*Version 1.1 | Spine doc — canonical Master Launch & Commercialization Plan |
§7 Horizon 4 tactical build plan added 2026-05-18 | Goals not guarantees |
Missing data = insufficient_data | Honors the 11 non-negotiables | Pricing lives
in OFFER_LADDER_AND_PRICING.md — not re-priced here.*
