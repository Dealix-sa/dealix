<!-- Owner: Founder/CEO | Date: 2026-05-18 | Arabic primary | Workstream F — CEO Commercial Activation Plan -->
<!-- Operating/financial artifact only — no product code, no new dashboard. Respects docs/ops/COMMERCIAL_FREEZE.md -->
<!-- Canonical offer/price source: docs/COMMERCIAL_WIRING_MAP.md — this file references, never restates as new numbers -->

# النموذج المالي واقتصاديات الوحدة — Financial Model & Unit Economics

> **هذه وثيقة تشغيلية، وليست وعداً.** كل الأرقام أدناه نطاقات تخطيطية (محافظ / أساسي / طموح)
> مبنية على معايير صناعية مُستشهَد بها وعلى أسعار العروض الرسمية. لا توجد نتيجة مضمونة.
>
> **This is an operating document, not a promise.** Every figure below is a planning band
> (conservative / base / stretch) built on cited industry benchmarks and the canonical
> offer prices. No outcome is guaranteed.

الأسعار الرسمية الوحيدة هي تلك المُنفَّذة في الكود ومُوثَّقة في
[`docs/COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) — السجل
`auto_client_acquisition/service_catalog/registry.py`. إذا تعارض أي رقم هنا مع تلك
الوثيقة، فالوثيقة الرسمية هي الصحيحة.

The only authoritative prices are those enforced in code and documented in
[`docs/COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) (registry:
`auto_client_acquisition/service_catalog/registry.py`). If any number here conflicts with
that document, the wiring map wins.

---

## 1. اقتصاديات سلّم العروض — Offer-Ladder Economics

نقلاً عن [`docs/COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) §1 — السجل الرسمي
للعروض السبعة. لا تُخترع أرقام جديدة.

Canonical from [`docs/COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md) §1 — the
7-offer registry. No new numbers invented.

| `service_id` | العرض / Offer | السعر (SAR) | الإيقاع / Cadence | دور في السلّم / Ladder role |
|---|---|---|---|---|
| `free_mini_diagnostic` | التشخيص المجاني / Free Mini Diagnostic | 0 | one_time | اكتشاف — يقيس النية / discovery — qualifies intent |
| `revenue_proof_sprint_499` | سبرنت إثبات الإيرادات / Revenue Proof Sprint | 499 | one_time | أول إيراد مدفوع / first paid — the wedge |
| `data_to_revenue_pack_1500` | حزمة من البيانات إلى الإيراد / Data-to-Revenue Pack | 1,500 | one_time | توسعة / expansion (مُجمَّد — frozen, rung 2) |
| `growth_ops_monthly_2999` | عمليات النمو الشهرية / Growth Ops Monthly | 2,999 | per_month | أول تحويل إلى اشتراك / first retainer |
| `support_os_addon_1500` | إضافة دعم العمليات / Support OS Add-on | 1,500 | per_month | إضافة على الاشتراك / retainer add-on |
| `executive_command_center_7500` | غرفة قيادة الإدارة / Executive Command Center | 7,500 | per_month | اشتراك تنفيذي / executive retainer |
| `agency_partner_os` | منصة شركاء الوكالات / Agency Partner OS | custom | — | قناة / channel (5,000 SAR per closed referral) |

**ملاحظة التجميد — Freeze note.** بموجب [`docs/ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md)
الرُتب 2–5 (Data-to-Revenue Pack، Growth Ops، Support OS، Command Center، Partner OS) **لا تُباع
ولا تُبنى** حتى تسليم أول Pilot مدفوع واعتماد Proof Pack بمستوى L3+. النموذج المالي للأيام الـ90
الأولى يقوم على الرُتب 0–1 فقط؛ الرُتب الأعلى تظهر كـ *مسار تحويل* محتمل بعد الخروج من التجميد.

Per [`docs/ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md), rungs 2–5 are neither sold
nor built until the first paid pilot is delivered and its Proof Pack is customer-approved at
L3+. The first-90-days financial model rests on **rungs 0–1 only**; higher rungs appear as a
potential *conversion path* that unlocks after freeze exit.

### 1.1 المنطق وراء كل رتبة — Why each rung exists

- **Rung 0 (0 SAR).** ليس خسارة — هو **مؤهِّل**. يفصل النية الجادة عن الفضول، ويُغذّي
  منطق التأهيل في `auto_client_acquisition/sales_os/qualification.py`. تكلفته = ساعات المؤسس فقط.
- **Rung 1 (499 SAR).** الإسفين التجاري. سعر منخفض بما يكفي ليكون قراراً سريعاً للمالك، ومرتفع
  بما يكفي ليُثبت أن العميل **يدفع** — أهم إشارة في أول 90 يوماً. يُنتج Proof Pack حقيقياً.
- **Rung 3 (2,999 SAR/شهر).** أول إيراد متكرر (MRR). يُباع **فقط** بعد أن يُثبت سبرنت مدفوع
  القيمة، **ومتى توفّرت سعة التسليم** (انظر §5).
- **Rungs 4–6.** توسعات لاحقة — خارج نطاق نموذج الأيام الـ90.

---

## 2. نموذج تصاعد الإيراد المتكرر — MRR Ramp Model

المسار: **أول Pilot مدفوع (499، لمرة واحدة)** ← **3 سبرنتات مدفوعة** ← **أول تحويل إلى اشتراك
(Growth Ops 2,999/شهر)**.

Path: **first paid pilot (499, one-time)** → **3 paid sprints** → **first retainer conversion
(Growth Ops, 2,999/mo)**.

ثلاثة مسارات. الفرضيات صريحة حتى يستطيع المؤسس تعديلها بأرقامه الحقيقية. **«الإيراد التراكمي»**
يجمع المبالغ لمرة واحدة + الاشتراكات المُحصَّلة خلال النافذة. «MRR في اليوم 90» هو معدل التشغيل
الخارج من النافذة.

Three paths. Assumptions are explicit so the founder can re-fit them to real numbers.
*Cumulative revenue* sums one-time fees + retainer cash collected within the window. *Day-90
MRR* is the exit run-rate.

### 2.1 المسار المحافظ — Conservative path

الفرضية: التأهيل بطيء؛ سبرنت واحد فقط مدفوع؛ لا تحويل إلى اشتراك خلال 90 يوماً.

| البند / Item | الكمية / Qty | السعر / Price | الإجمالي / Total |
|---|---|---|---|
| Free Diagnostic | 4–6 | 0 | 0 |
| Revenue Proof Sprint | 1 | 499 | 499 |
| Growth Ops retainer | 0 | 2,999/mo | 0 |
| **الإيراد التراكمي / Cumulative (90 days)** | | | **≈ 499 SAR** |
| **MRR في اليوم 90 / Day-90 MRR** | | | **0 SAR** |

النتيجة الحقيقية للمسار المحافظ ليست المال — بل **Proof Pack واحد معتمد L3+** يُنهي التجميد.
The real conservative-path outcome is not cash — it is **one L3+-approved Proof Pack** that
exits the freeze.

### 2.2 المسار الأساسي — Base path *(planning anchor)*

الفرضية: القائمة الدافئة تعمل؛ 3 سبرنتات مدفوعة خلال النافذة؛ أول تحويل إلى اشتراك واحد في
الأسبوع 9–10 يجمع شهرين من النقد قبل اليوم 90.

| البند / Item | الكمية / Qty | السعر / Price | الإجمالي / Total |
|---|---|---|---|
| Free Diagnostic | 10–14 | 0 | 0 |
| Revenue Proof Sprint | 3 | 499 | 1,497 |
| Growth Ops retainer (1 عميل، شهران مُحصَّلان) | 1 × 2 | 2,999/mo | 5,998 |
| **الإيراد التراكمي / Cumulative (90 days)** | | | **≈ 7,495 SAR** |
| **MRR في اليوم 90 / Day-90 MRR** | | | **≈ 2,999 SAR** |

### 2.3 المسار الطموح — Stretch path

الفرضية: التأهيل قوي؛ 5 سبرنتات مدفوعة؛ تحويلان إلى اشتراك (أحدهما مبكر)؛ لا تُباع أي اشتراكات
تتجاوز سعة التسليم في §5.

| البند / Item | الكمية / Qty | السعر / Price | الإجمالي / Total |
|---|---|---|---|
| Free Diagnostic | 16–20 | 0 | 0 |
| Revenue Proof Sprint | 5 | 499 | 2,495 |
| Growth Ops retainer (عميلان، 4 أشهر-عميل مُحصَّلة) | 2، 4 شهر-عميل | 2,999/mo | 11,996 |
| **الإيراد التراكمي / Cumulative (90 days)** | | | **≈ 14,491 SAR** |
| **MRR في اليوم 90 / Day-90 MRR** | | | **≈ 5,998 SAR** |

### 2.4 ملخص المسارات — Path summary

| المسار / Path | سبرنتات / Sprints | اشتراكات / Retainers | تراكمي / Cumulative | MRR يوم 90 / Day-90 MRR |
|---|---|---|---|---|
| محافظ / Conservative | 1 | 0 | ≈ 499 SAR | 0 SAR |
| **أساسي / Base** | **3** | **1** | **≈ 7,495 SAR** | **≈ 2,999 SAR** |
| طموح / Stretch | 5 | 2 | ≈ 14,491 SAR | ≈ 5,998 SAR |

> هذه نطاقات تخطيطية، وليست توقعات ملتزَماً بها. يُعاد ضبطها كل أسبوع بأرقام القائمة الدافئة الحقيقية.
> These are planning bands, not committed forecasts. Re-fit weekly against real warm-list data.

---

## 3. المعايير الصناعية الخارجية (2026) — External Benchmarks

تُذكر كـ **معايير صناعية مُستشهَد بها** لتخطيط القمع — وليست وعوداً ولا التزامات أداء.

Stated as **cited industry benchmarks** for funnel planning — not promises, not performance
commitments.

| المعيار / Benchmark | النطاق / Range | الأثر على الخطة / Planning implication |
|---|---|---|
| إغلاق من العرض التوضيحي / Demo-to-close — demo-led B2B SaaS | متوسط 22–30٪، الأفضل ~40٪ / avg 22–30%, top ~40% | كل عرض توضيحي مؤهَّل = ~رُبع إلى ثلث فرصة إغلاق. خطّط لـ3–5 عروض توضيحية لكل سبرنت مدفوع. |
| زائر → عميل محتمل / visitor-to-lead — sales-led inbound | 0.5–1.5٪ فقط / only 0.5–1.5% | الوارد البارد لا يمكنه تشغيل أول 90 يوماً. |

**الاستنتاج — The engine for the first 90 days.** عند تحويل 0.5–1.5٪ فقط، يتطلب الوارد البارد
آلاف الزيارات لإنتاج سبرنت واحد. **القائمة الدافئة — وليس الوارد البارد — هي محرّك الإيراد** في
أول 90 يوماً: علاقات موجودة، ثقة موجودة، تحويل أعلى بكثير، تكلفة اكتساب = وقت المؤسس فقط. هذا
يتوافق مع [`docs/ops/COMMERCIAL_FREEZE.md`](../ops/COMMERCIAL_FREEZE.md) ومع
[`docs/sales-kit/WARM_LIST_WORKFLOW.md`](../sales-kit/WARM_LIST_WORKFLOW.md).

At a 0.5–1.5% conversion, cold inbound needs thousands of visits to yield a single sprint.
**The warm list — not cold inbound — is the revenue engine** for the first 90 days: existing
relationships, existing trust, far higher conversion, and a CAC of founder time only.

> القناة باردة الواتساب والكشط ممنوعة بموجب اللوائح غير القابلة للتفاوض — المحرّك الدافئ ليس
> اختياراً تكتيكياً فحسب، بل قيد عقائدي. / Cold WhatsApp and scraping are forbidden by the
> non-negotiables — the warm engine is not just a tactic, it is a doctrine constraint.

---

## 4. هدف الزمن-حتى-الإثبات — Time-to-Proof Target

**الهدف: أقل من 48 ساعة داخل أي Pilot** — من بيانات العميل المُستلَمة إلى Proof Pack مُجمَّع جاهز
للمراجعة.

**Target: under 48 hours inside a pilot** — from received customer data to an assembled Proof
Pack ready for review.

- لماذا 48 ساعة: سرعة الإثبات هي الميزة. كلما اقتربت لحظة «أرني القيمة» من لحظة الدفع، ارتفع
  معدّل التحويل إلى اشتراك. / Why 48h: speed-to-proof is the moat — the closer the "show me the
  value" moment is to the payment moment, the higher the retainer conversion.
- المسار: السبرنت من 10 خطوات (`auto_client_acquisition/delivery_factory/delivery_sprint.run_sprint`)
  ← التجميع من 14 قسماً (`auto_client_acquisition/proof_os/proof_pack.assemble`).
- هذا هدف تشغيلي **داخلي**، وليس بنداً تعاقدياً ولا وعداً للعميل. / This is an **internal**
  operating target, not a contractual term or a customer promise.
- يُتتبَّع في [`DELIVERY_LEDGER.md`](DELIVERY_LEDGER.md) لكل Pilot.

---

## 5. تكلفة الاكتساب والسعة والهامش — CAC, Capacity & Margin

### 5.1 تكلفة الاكتساب بقيادة المؤسس — Founder-led CAC

في أول 90 يوماً، **تكلفة الاكتساب النقدية ≈ صفر**؛ التكلفة الحقيقية هي **ساعات المؤسس**. لا
إنفاق إعلاني، لا أدوات مدفوعة للوارد البارد. لذا فإن القيد هو **الوقت**، وليس الميزانية.

In the first 90 days, **cash CAC ≈ 0**; the real cost is **founder hours**. No ad spend, no
paid cold-inbound tooling. The binding constraint is **time**, not budget.

| نشاط / Activity | تقدير ساعات المؤسس / Est. founder hours |
|---|---|
| تواصل القائمة الدافئة + متابعات (لكل سبرنت مغلق) / warm outreach + follow-ups (per closed sprint) | 3–5 |
| مكالمة اكتشاف + عرض توضيحي / discovery call + demo | 1–2 |
| تسليم السبرنت + مراجعة Proof Pack / sprint delivery + Proof Pack review | 3–5 |
| **إجمالي تقريبي لكل سبرنت مدفوع / approx total per paid sprint** | **7–12 ساعة / hours** |

### 5.2 نموذج سعة التسليم — Delivery Capacity Model

انظر [`docs/company/DELIVERY_CAPACITY_MODEL.md`](../company/DELIVERY_CAPACITY_MODEL.md)
و[`docs/company/CAPACITY_MODEL.md`](../company/CAPACITY_MODEL.md) للنموذج الأم. الجدول التالي
يقيّد كم اشتراكاً يمكن **بيعه بأمان**.

See [`docs/company/DELIVERY_CAPACITY_MODEL.md`](../company/DELIVERY_CAPACITY_MODEL.md) and
[`docs/company/CAPACITY_MODEL.md`](../company/CAPACITY_MODEL.md) for the parent model. The
table below bounds how many retainers can be **safely sold**.

| المورد / Resource | السعة الافتراضية / Assumed capacity | يقيّد / Bounds |
|---|---|---|
| ساعات المؤسس المُسلِّمة / founder delivery hours per week | ~20 ساعة قابلة للتسليم / ~20 deliverable hrs | عدد السبرنتات + الاشتراكات المتزامنة |
| سبرنت مدفوع / paid sprint | 7–12 ساعة لمرة واحدة / one-time | بحد ~2 سبرنت متزامن / ~2 concurrent |
| اشتراك Growth Ops / Growth Ops retainer | ~6–10 ساعات شهرياً مستمرة / ~6–10 hrs/mo ongoing | كل اشتراك يستهلك سعة دائمة |

**قاعدة السعة — Capacity rule.** لا يُباع اشتراك إلا إذا توفّرت سعة تسليم له **قبل** التوقيع.
بيع اشتراك بلا سعة = تسليم متأخر = إخفاق في الإثبات = ضرر للثقة. عند **>5 ساعات لكل سبرنت بعد
العميل الخامس**، توقّف عن بيع سبرنتات جديدة وارفع أتمتة السبرنت إلى أعلى قائمة P0 (قاعدة قرار من
خطة الـ90 يوماً).

Never sell a retainer unless delivery capacity exists for it **before** signing. Selling a
retainer with no capacity = late delivery = a failed proof = trust damage. If founder time
exceeds **5 hours per sprint after customer 5**, stop selling new sprints and push sprint
automation to the top of the P0 list.

### 5.3 الهامش الإجمالي — Gross Margin

انظر [`docs/company/MARGIN_CONTROL.md`](../company/MARGIN_CONTROL.md). في مرحلة المؤسس-الوحيد،
التكلفة المتغيّرة الأساسية هي وقت المؤسس + استدعاءات نماذج اللغة (LLM) لكل سبرنت.

See [`docs/company/MARGIN_CONTROL.md`](../company/MARGIN_CONTROL.md). At the solo-founder stage,
the main variable cost is founder time + per-sprint LLM calls.

- **النقدي / cash:** بلا أجور مدفوعة، يكون الهامش النقدي على السبرنت مرتفعاً (التكلفة المتغيّرة
  النقدية الوحيدة هي رسوم LLM/البنية التحتية، وهي صغيرة مقابل سعر 499).
- **الاقتصادي / economic:** عند تسعير وقت المؤسس، السبرنت **يكسر التعادل تقريباً** — قيمته
  الحقيقية هي **الأصل الرأسمالي** الذي يُنتجه (Proof Pack، رؤية قطاعية) وليس النقد. الاشتراك هو
  حيث ينتقل الهامش الاقتصادي إلى الموجب.
- **القاعدة / rule:** يُحرَس الهامش بقاعدة السعة في §5.2، لا بخصم السعر. لا تُخفَّض الأسعار
  الرسمية لتعويض ضيق السعة.

---

## 6. انضباط الاستبعاد — Disqualification Discipline

التأهيل مُنفَّذ في الكود: `auto_client_acquisition/sales_os/qualification.py`
(`qualify_opportunity`). النموذج المالي يحترم قراراته — لا يُسجَّل عميل في المسار الأساسي إلا إذا
اجتاز التأهيل.

Qualification is enforced in code: `auto_client_acquisition/sales_os/qualification.py`
(`qualify_opportunity`). The financial model respects its verdicts — no lead enters the base
path unless it passes qualification.

| الإشارة / Signal | القرار / Verdict | الأثر المالي / Financial effect |
|---|---|---|
| يريد كشطاً/سبام أو ضمان مبيعات / wants scraping/spam or guaranteed sales | `REJECT` — `non_negotiable_risk` | يُستبعَد — صفر إيراد مُخطَّط. غير قابل للتفاوض. |
| خطورة عميل عالية / high client risk (score ≥ 55) | `REJECT` — `high_client_risk` | يُستبعَد. |
| لا يقبل الحوكمة / governance not accepted | `REFER_OUT` | يُحال للخارج — صفر إيراد مُخطَّط. |
| لا حجم عملاء محتملين / لا مالك / مسار إثبات ضعيف | `DIAGNOSTIC_ONLY` / `REFRAME` | يُؤجَّل أو يُعاد تأطيره — يبدأ من رتبة 0، لا يُحتسَب كسبرنت مُخطَّط. |
| ICP قوي + خطورة منخفضة + مسار إثبات ممكن | `ACCEPT` | يدخل المسار الأساسي كسبرنت مُخطَّط. |

**قاعدة النموذج — Model rule.** «لا حجم عملاء محتملين / لا مالك / يريد كشطاً أو عائد استثمار
مضموناً → يُؤجَّل.» العميل المؤجَّل **لا** يُحتسَب في إسقاطات §2. الانضباط في الاستبعاد يحمي
أرقام السعة والهامش من التضخّم بفرص لن تُغلَق أبداً.

A disqualified or deferred lead is **not** counted in the §2 projections. Disqualification
discipline keeps the capacity and margin numbers honest.

---

## 7. ما الذي يُقاس بجانب الإيراد — Measured Alongside Revenue

الإيراد وحده مؤشر متأخّر. يُسجَّل أيضاً في السجلّات تحت [`docs/ledgers/`](./):

Revenue alone is a lagging metric. The following are also recorded to the ledgers under
[`docs/ledgers/`](./):

- **Proof Packs** بمستوى L3+ — [`PROOF_LEDGER.md`](PROOF_LEDGER.md)
- **الأصول الرأسمالية** لكل مشروع (أصل ثقة واحد على الأقل) — [`CAPITAL_LEDGER.md`](CAPITAL_LEDGER.md)
- **القيمة المُتحقَّقة** للعميل — [`VALUE_LEDGER.md`](VALUE_LEDGER.md)
- **سعة التسليم** المُستهلَكة — [`CAPACITY_LEDGER.md`](CAPACITY_LEDGER.md), [`DELIVERY_LEDGER.md`](DELIVERY_LEDGER.md)
- **الزمن-حتى-الإثبات** لكل Pilot (هدف < 48 ساعة، §4)

> مؤشر اليوم 90 الواحد قبل توسيع المبيعات أو المنتج: **Pilot مدفوع واحد مُسلَّم + Proof Pack
> معتمد L3+.** ليس MRR، ليس عدد العملاء المحتملين — ذلك الإثبات الواحد. (شرط الخروج من التجميد.)

---

## 8. ملاحظات وضوابط — Notes & Guards

- كل الأسعار من [`docs/COMMERCIAL_WIRING_MAP.md`](../COMMERCIAL_WIRING_MAP.md). لا تُخترع أرقام.
- لا توجد لغة عائد استثمار مضمون أو إيراد مضمون في أي مكان من هذه الوثيقة — لائحة غير قابلة للتفاوض.
- الرُتب 2–5 مُجمَّدة؛ نموذج الأيام الـ90 يقوم على الرُتب 0–1 فقط.
- يُعاد ضبط هذا النموذج في **المراجعة الأسبوعية للتحسين الذاتي** الموصوفة في
  [`docs/ops/REVENUE_OPERATING_SYSTEM.md`](../ops/REVENUE_OPERATING_SYSTEM.md) §3.
- وثائق ذات صلة: [`docs/company/UNIT_ECONOMICS.md`](../company/UNIT_ECONOMICS.md)،
  [`docs/company/FINANCIAL_MODEL.md`](../company/FINANCIAL_MODEL.md)،
  [`docs/company/MARGIN_CONTROL.md`](../company/MARGIN_CONTROL.md)،
  [`docs/company/SERVICE_ECONOMICS.md`](../company/SERVICE_ECONOMICS.md).

---

> **النتائج التقديرية ليست نتائج مضمونة.** كل مسار في §2 فرضية تخطيطية مبنية على معايير صناعية
> مُستشهَد بها وعلى أسعار رسمية — وليس التزاماً ولا توقّعاً للعميل.
>
> **Estimated outcomes are not guaranteed outcomes.** Every path in §2 is a planning
> hypothesis built on cited industry benchmarks and canonical prices — not a commitment and
> not a customer-facing forecast.
