<!-- LAYER: empire/doctrine | Owner: Founder | Bilingual AR+EN | draft_only -->
<!-- Part of the Dealix Operating Standard — see INDEX.md -->

# منظمة وكلاء ديلكس — Dealix Agent Organization

> **AR:** هرم محكوم من 25 دوراً وكيلاً يدير دورة تنفيذية يومية. كل عمل يُنجَز آلياً، لكن كل مخرج خارجي **مسودة فقط** تمر على بوابة موافقة المؤسس.
> **EN:** A governed pyramid of 25 agent roles running a daily executive cycle. All work is done automatically, but every externally-visible output is **draft-only** and routed through the founder approval gate.

المصدر التقني / Source modules: `auto_client_acquisition/agent_org/org_chart.py` · `auto_client_acquisition/agent_org/orchestrator.py` · `api/routers/agent_org.py`

---

## 1. الغرض ومبدأ الاستقلالية المحكومة / Purpose & the Governed-Autonomy Principle

**AR:** منظمة الوكلاء تُشغّل عمليات ديلكس اليومية — الإيراد، التسليم، العملاء، النمو، الحوكمة، والذكاء — كهيكل واحد متماسك. المبدأ الحاكم هو **الاستقلالية المحكومة**: المحرّك يُنجز كل العمل آلياً، لكنه لا يملك صلاحية إرسال أي شيء للخارج. كل مخرج خارجي يعود كمسودة بحالة `pending_approval` وينتظر موافقة المؤسس بنقرة واحدة. هذا يقابل النموذج غير المحكوم — «الذكاء الاصطناعي يفعل كل شيء» — الذي يرسل ويَعِد ويُسعّر بلا رقابة بشرية. بوابة الموافقة **غير قابلة للتفاوض** لأنها الفرق بين أداة تُسرّع المؤسس وأداة تتصرف نيابة عنه دون إذن.

**EN:** The Agent Organization runs Dealix's daily operations — revenue, delivery, customer, growth, governance, and intelligence — as one coherent structure. The governing principle is **governed autonomy**: the engine does all the work automatically, but holds no authority to send anything externally. Every external output returns as a draft with status `pending_approval`, awaiting the founder's one-click approval. This contrasts with the ungoverned "AI does everything" model that sends, promises, and prices with no human in the loop. The approval gate is **non-negotiable** because it is the line between a tool that accelerates the founder and a tool that acts on the founder's behalf without permission.

سقف الاستقلالية / Autonomy ceiling: لا دور يتجاوز **L2 (مسودة)** لأي مخرج خارجي. المستويان L4/L5 (تنفيذ آلي) **محجوزان وممنوعان** — لا كود يُفعّلهما. / No role exceeds **L2 (draft)** for any external output. L4/L5 (auto-execute) are **reserved and forbidden** — no code activates them.

---

## 2. الهيكل التنظيمي / The Org Chart

**AR:** الهرم ثلاث طبقات: رئيس أركان واحد (الطبقة 0)، ستة مدراء (الطبقة 1)، وثمانية عشر وكيلاً تنفيذياً (الطبقة 2 — ثلاثة تحت كل مدير). الأسماء والمهام أدناه منقولة حرفياً من `org_chart.py`.

**EN:** A three-tier pyramid: one Chief of Staff (tier 0), six Directors (tier 1), and eighteen Operators (tier 2 — three under each director). Names and missions below are taken verbatim from `org_chart.py`.

### الطبقة 0 — رئيس الأركان / Tier 0 — Chief of Staff

| المعرّف / id | الاسم AR | Name EN | يرفع إلى / Reports to | المهمة / Mission | الاستقلالية / Autonomy |
|---|---|---|---|---|---|
| `chief_of_staff` | رئيس الأركان | Chief of Staff | — | يدير الدورة التنفيذية اليومية، يجمّع موجز المؤسس، ويرفع التصعيدات. / Runs the daily executive cycle, assembles the founder brief, raises escalations. | L3 (داخلي فقط / internal only) |

### الطبقة 1 — المدراء / Tier 1 — Directors

| المعرّف / id | الاسم AR | Name EN | يرفع إلى / Reports to | المهمة / Mission | الاستقلالية / Autonomy |
|---|---|---|---|---|---|
| `revenue_director` | مدير الإيراد | Revenue Director | `chief_of_staff` | يملك سلّم العروض الخمسة وخط الأنابيب من الحساب المؤهل حتى الإغلاق. / Owns the 5-rung offer ladder and the pipeline from qualified account to close. | L3 |
| `delivery_director` | مدير التسليم | Delivery Director | `chief_of_staff` | يملك تنفيذ السبرنت وجودة التسليم وحزمة الإثبات. / Owns sprint execution, delivery quality, and the Proof Pack. | L3 |
| `customer_director` | مدير العملاء | Customer Director | `chief_of_staff` | يملك الاحتفاظ بالعملاء، صحة الحسابات، والتوسّع المحكوم بالإثبات. / Owns retention, account health, and proof-gated expansion. | L3 |
| `growth_director` | مدير النمو | Growth Director | `chief_of_staff` | يملك محتوى ديلكس الخاص، محرّك السلطة، وشبكة الشركاء. / Owns Dealix's own content, the authority engine, and the partner network. | L3 |
| `governance_director` | مدير الحوكمة | Governance Director | `chief_of_staff` | يملك الامتثال، بوابة الموافقات، وحماية الخصوصية (PDPL). / Owns compliance, the approval gate, and PDPL privacy protection. | L3 |
| `intelligence_director` | مدير الذكاء | Intelligence Director | `chief_of_staff` | يملك جودة البيانات، التسجيل، رصد السوق، وسجل الاحتكاك. / Owns data quality, scoring, market radar, and the friction log. | L3 |

### الطبقة 2 — الوكلاء التنفيذيون / Tier 2 — Operators

| المعرّف / id | الاسم AR | Name EN | يرفع إلى / Reports to | المهمة / Mission | الاستقلالية / Autonomy | مخرج خارجي / External |
|---|---|---|---|---|---|---|
| `lead_scout` | كشّاف العملاء المحتملين | Lead Scout | `revenue_director` | يجهّز قائمة حسابات مؤهلة بمعيار ICP — دافئة أولاً، بلا scraping. / Prepares an ICP-qualified account list — warm-first, no scraping. | L1 | لا / no |
| `proposal_drafter` | كاتب العروض | Proposal Drafter | `revenue_director` | يكتب مسودات عروض من سلّم العروض — نطاق محدود، بلا وعود نتائج. / Drafts proposals from the offer ladder — bounded scope, no outcome promises. | L2 | نعم / yes |
| `outreach_drafter` | كاتب التواصل | Outreach Drafter | `revenue_director` | يكتب مسودات تواصل دافئ — كل مسودة تذهب لقائمة الموافقة، لا إرسال آلي. / Drafts warm outreach — every draft goes to the approval queue, never auto-sent. | L2 | نعم / yes |
| `sprint_planner` | مخطّط السبرنت | Sprint Planner | `delivery_director` | يحوّل المشروع المباع إلى خطة سبرنت سبعة أيام بحدود واضحة. / Turns a sold engagement into a bounded 7-day sprint plan. | L1 | لا / no |
| `data_quality_agent` | وكيل جودة البيانات | Data Quality Agent | `delivery_director` | يفحص بيانات العميل ويصدر درجة جودة قبل أي تحليل. / Inspects customer data and issues a quality score before any analysis. | L1 | لا / no |
| `proof_assembler` | مجمّع حزمة الإثبات | Proof Assembler | `delivery_director` | يجمّع حزمة الإثبات بأربعة عشر قسماً لكل تسليم. / Assembles the 14-section Proof Pack for every delivery. | L2 | نعم / yes |
| `followup_sequencer` | مرتّب المتابعات | Follow-up Sequencer | `customer_director` | يولّد مسودات متابعة D+3 / D+7 / D+14 — كلها للموافقة. / Generates D+3 / D+7 / D+14 follow-up drafts — all approval-gated. | L2 | نعم / yes |
| `health_monitor` | مراقب صحة الحسابات | Account Health Monitor | `customer_director` | يراقب إشارات صحة كل حساب ويصنّفها. / Monitors each account's health signals and buckets them. | L1 | لا / no |
| `expansion_agent` | وكيل التوسّع | Expansion Agent | `customer_director` | يقترح العرض التالي — محكوم بالإثبات، لا توسّع بلا إثبات موثّق. / Recommends the next-best offer — proof-gated, no upsell without recorded proof. | L3 | لا / no |
| `content_writer` | كاتب المحتوى | Content Writer | `growth_director` | يكتب محتوى ديلكس الخاص — لا تواصل بارد، نشر ذاتي فقط. / Writes Dealix's own content — no cold outreach, own-channel publishing only. | L2 | نعم / yes |
| `partner_scout` | كشّاف الشركاء | Partner Scout | `growth_director` | يجهّز قائمة شركاء وكالات محتملين لحركة الإسفين. / Prepares a candidate agency-partner list for the wedge motion. | L1 | لا / no |
| `distribution_planner` | مخطّط النشر | Distribution Planner | `growth_director` | يجدول نشر المحتوى المعتمد عبر قنوات ديلكس بأفضل توقيت. / Schedules approved content across Dealix channels at the best times. | L2 | نعم / yes |
| `compliance_reviewer` | مراجع الامتثال | Compliance Reviewer | `governance_director` | يفحص كل مخرج خارجي بحثاً عن وعود مضمونة أو لغة ممنوعة. / Scans every external output for guaranteed-outcome or forbidden language. | L1 | لا / no |
| `approval_router` | موجّه الموافقات | Approval Router | `governance_director` | يوجّه كل مخرج خارجي إلى قائمة موافقة المؤسس بنقرة واحدة. / Routes every external output to the founder's one-click approval queue. | L1 | لا / no |
| `pdpl_auditor` | مدقّق الخصوصية | PDPL Auditor | `governance_director` | يدقّق التعامل مع البيانات الشخصية وفق نظام حماية البيانات. / Audits personal-data handling against PDPL. | L1 | لا / no |
| `market_radar` | رادار السوق | Market Radar | `intelligence_director` | يرصد إشارات السوق والقطاعات ذات الصلة بالعملاء. / Scans market and sector signals relevant to customers. | L1 | لا / no |
| `metrics_analyst` | محلّل المؤشرات | Metrics Analyst | `intelligence_director` | يحلّل مؤشرات الإيراد والتسليم والاحتفاظ للموجز اليومي. / Analyzes revenue, delivery, and retention metrics for the daily brief. | L1 | لا / no |
| `friction_logger` | مسجّل الاحتكاك | Friction Logger | `intelligence_director` | يسجّل كل احتكاك تشغيلي ليُحوَّل لقرار تحسين. / Logs every operational friction so it becomes an improvement decision. | L1 | لا / no |

> **AR:** ستة وكلاء فقط من 25 ينتجون مخرجات خارجية، وكلهم محصورون عند L2 (مسودة). البقية داخلية بحتة.
> **EN:** Only 6 of 25 roles produce external output, and all are capped at L2 (draft). The rest are purely internal.

---

## 3. الدورة التنفيذية اليومية / The Daily Executive Cycle

**AR:** الدالة `run_daily_cycle()` تمشي بالهرم من الأسفل للأعلى بترتيب ثابت:

**EN:** `run_daily_cycle()` walks the pyramid bottom-up in a fixed order:

1. **فحص السلامة / Integrity check** — تشغّل `validate_org()` أولاً؛ أي خلل بنيوي يُسجَّل تصعيداً بصيغة `org-integrity: …`. / Runs `validate_org()` first; any structural problem is recorded as an `org-integrity: …` escalation.
2. **الوكلاء التنفيذيون ينتجون العمل / Operators produce work** — لكل مدير، يعمل وكلاؤه الثلاثة وينتج كلٌّ منهم عناصر عمل (`WorkItem`). / For each director, its three operators run and each produces work items (`WorkItem`).
3. **المدراء يراجعون / Directors review** — كل مدير يصدر عنصر مراجعة واحداً يلخّص مخرجات فريقه وعدد ما ينتظر الموافقة. / Each director emits one review item summarizing its team's outputs and how many await approval.
4. **رئيس الأركان يجمّع الموجز / Chief of Staff assembles the brief** — يحسب حِمل الموافقة الحقيقي (عدد المسودات خلف كل عنصر خارجي)، ويصدر **موجز المؤسس** ثنائي اللغة كآخر عنصر عمل (داخلي). إذا تجاوز حجم المسودات 20 يُضاف تصعيد `approval-load`. / Computes the real approval load (the count of drafts behind each external item), and emits the bilingual **founder brief** as the final (internal) work item. If draft volume exceeds 20 an `approval-load` escalation is added.

### بنية `WorkItem` / The `WorkItem` shape

`id` · `agent_id` · `agent_name_en` · `kind` · `title_ar` · `title_en` · `summary` · `external` (منطقي / bool) · `status` · `autonomy` · `created_at` · `payload`.

### بنية `DailyOrgReport` / The `DailyOrgReport` shape

`cycle_id` · `run_date` · `agents_run` · `items_total` · `items_pending_approval` · `items_internal` · `escalations` · `founder_brief_ar` · `founder_brief_en` · `work_items[]`.

### الفرق بين الحالتين / `internal_done` vs `pending_approval`

**AR:** عند بناء أي عنصر عمل، يُجبر الحارس العقائدي في `_make_item()` الحالة: إذا كان الدور ينتج مخرجاً خارجياً (`produces_external = True`) فالحالة `pending_approval` إلزامياً — لا يستطيع الوكيل أن يعلن عمله الخارجي «منجزاً». أما العمل الداخلي (تحليل، تسجيل، مراجعة) فحالته `internal_done` لأنه لا يغادر النظام ولا يحتاج موافقة.

**EN:** When any work item is built, the doctrine guard in `_make_item()` forces the status: if the role produces external output (`produces_external = True`), the status is mandatorily `pending_approval` — an agent cannot mark its own external work "done." Internal work (analysis, logging, review) gets `internal_done` because it never leaves the system and needs no approval.

---

## 4. واجهة API / The API Surface

المسار الأساسي / Base path: `/api/v1/agent-org`

| الطريقة / Method | المسار / Path | الوصف / Description |
|---|---|---|
| `GET` | `/status` | عدد الأدوار، توزيع الطبقات، والحواجز المُعلَنة (`governed_autonomy`, `no_auto_send`, `no_scraping`, `max_autonomy_for_external: L2_DRAFT`). / Headcount, tier counts, and declared guardrails. |
| `GET` | `/chart` | الهرم الكامل: رئيس ← مدراء ← وكلاء (`org_chart_dict()`). / The full pyramid: chief → directors → operators. |
| `GET` | `/agents` | كل الأدوار الـ25 بتفاصيلها. / All 25 roles with full detail. |
| `GET` | `/agents/{agent_id}` | دور واحد بالمعرّف؛ يرجع 404 لمعرّف غير معروف. / One role by id; returns 404 for an unknown id. |
| `GET` | `/validate` | فحص السلامة البنيوية: `{healthy, problems}`. / Structural integrity check. |
| `POST` | `/daily-cycle/run` | يشغّل دورة تنفيذية واحدة. جسم اختياري: `run_date`, `context`. كل مخرج خارجي يعود `pending_approval`. / Runs one cycle. Optional body: `run_date`, `context`. Every external output returns `pending_approval`. |

> **AR:** نقاط القراءة نقية بلا أثر جانبي؛ نقطة الدورة حتمية بالنسبة لمدخلها. لا نقطة في الواجهة تُرسِل شيئاً للخارج.
> **EN:** Read endpoints are pure and side-effect free; the cycle endpoint is deterministic given its input. No endpoint sends anything externally.

---

## 5. ضمانات الحوكمة / Governance Guarantees

**AR:** الدالة `validate_org()` تفرض ثوابت السلامة التالية (قائمة فارغة = سليم):

**EN:** `validate_org()` enforces these integrity invariants (empty list = healthy):

- رئيس واحد بالضبط في الطبقة 0 ولا يرفع لأحد. / Exactly one chief at tier 0, reporting to no one.
- كل دور غير الرئيس يرفع إلى دور موجود فعلاً. / Every non-chief reports to an existing role.
- الوكلاء يرفعون لمدير، والمدراء يرفعون للرئيس. / Operators report to a director; directors report to the chief.
- لا دورات في سلسلة الرفع. / No cycles in the reporting chain.
- لا دور ينتج مخرجاً خارجياً يتجاوز استقلالية L2. / No role producing external output exceeds L2 autonomy.

**سقف الاستقلالية / Autonomy ceiling:** المخرج الخارجي ممنوع فوق L2 (مسودة)؛ L3 مسموح للأدوار الداخلية فقط (مدراء، رئيس، وكيل التوسّع)؛ L4/L5 محجوزان وممنوعان. / External output is forbidden above L2 (draft); L3 is allowed for internal roles only (directors, chief, expansion agent); L4/L5 are reserved and forbidden.

### الربط بغير القابل للتفاوض الـ11 / Mapped to the 11 Non-Negotiables

انظر [`../00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md).

| # | غير قابل للتفاوض / Non-negotiable | الضمان في المنظمة / Guarantee in the org |
|---|---|---|
| 1 | لا scraping / no scraping | `lead_scout` و`partner_scout` يستخدمان مصادر دافئة وإحالات وinbound فقط. / warm, referral, inbound sourcing only. |
| 2 | لا تواصل بارد آلي / no cold automation | `outreach_drafter` ينتج مسودات فقط؛ لا إرسال آلي. / drafts only, never auto-sent. |
| 3 | لا أتمتة LinkedIn/WhatsApp / no LI/WA automation | لا دور أو نقطة API تُرسل عبر قنوات خارجية. / no role or endpoint sends on external channels. |
| 4 | لا وعود نتائج / no guaranteed outcomes | `compliance_reviewer` يحجب أي لغة ضمان؛ التوصيات «فرص مُثبتة بأدلة». / blocks guarantee language. |
| 5 | لا أرقام مبيعات كحقيقة / no sales numbers as fact | `metrics_analyst` يُصرّح أن الأرقام تقديرات تخطيطية. / figures declared as planning estimates. |
| 6 | لا PII / no PII | `pdpl_auditor` يدقّق الموافقة والاحتفاظ والإلغاء. / audits consent, retention, revoke. |
| 7 | لا إرسال نيابة عن العميل بلا إذن / no send without approval | `approval_router` يوجّه كل مخرج خارجي لبوابة الموافقة. / routes every external output to the gate. |
| 8 | الإثبات قبل التوسّع / proof before expansion | `expansion_agent` محكوم بالإثبات؛ لا توسّع بلا إثبات موثّق. / proof-gated, no upsell without recorded proof. |
| 9 | القيمة التقديرية مفصولة / estimated value separated | `proof_assembler` يفصل القيمة التقديرية عن المُتحقَّقة في كل تسليم. / separates estimated from verified value. |
| 10 | لا تحليل على بيانات رديئة / no analysis on bad data | `data_quality_agent` يصدر درجة جودة قبل أي تحليل. / quality score before analysis. |
| 11 | بوابة موافقة بشرية إلزامية / mandatory human gate | الحارس في `_make_item()` يفرض `pending_approval` على كل مخرج خارجي. / forces `pending_approval` on every external output. |

---

## 6. الربط ببقية النظام / How It Connects to the Rest of the System

**AR:**
- **قائمة الموافقات / Approval queue** — كل مخرج خارجي يمر عبر [`/api/v1/approvals`](../14_trust_os/) للموافقة أو الرفض أو التعديل بنقرة واحدة؛ لا شيء يُرسَل قبل ذلك.
- **محرّك الأتمتة القائم / Existing automation engine** — المنظمة طبقة تنسيق فوق المحرّكات القائمة (`revenue_os.followup_plan`, `revenue_os.expansion_engine`)؛ تُستدعى دفاعياً بحيث لا يكسر أي إعادة هيكلة الدورة.
- **سلّم العروض / Offer ladder** — `revenue_director` و`proposal_drafter` يعملان من سلّم العروض الخمسة في [`OFFER_LADDER.md`](OFFER_LADDER.md)، والسلم الحي للأسعار في [`../COMPANY_SERVICE_LADDER.md`](../COMPANY_SERVICE_LADDER.md).

**EN:**
- **Approval queue** — every external output flows through [`/api/v1/approvals`](../14_trust_os/) for one-click approve / reject / edit; nothing is sent before that.
- **Existing automation engine** — the org is a coordination layer over existing engines (`revenue_os.followup_plan`, `revenue_os.expansion_engine`), called defensively so a downstream refactor cannot break the cycle.
- **Offer ladder** — `revenue_director` and `proposal_drafter` work from the 5-rung ladder in [`OFFER_LADDER.md`](OFFER_LADDER.md); the live pricing source of truth is [`../COMPANY_SERVICE_LADDER.md`](../COMPANY_SERVICE_LADDER.md).

روابط مرجعية / Related docs: [`COMMERCIAL_CONTROL_TOWER.md`](COMMERCIAL_CONTROL_TOWER.md) · [`PROOF_PACK_STANDARD.md`](PROOF_PACK_STANDARD.md) · [`TRUST_LAYER.md`](TRUST_LAYER.md) · [`../00_constitution/NON_NEGOTIABLES.md`](../00_constitution/NON_NEGOTIABLES.md)

---

> **القيمة التقديرية ليست قيمة مُتحقَّقة / Estimated value is not Verified value.**
