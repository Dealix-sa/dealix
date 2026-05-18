# Dealix — سجل الوكلاء · Agent Roster

**الحالة / Status:** DRAFT — architecture
**المالك / Owner:** Sami (founder)
**آخر تحديث / Last updated:** 2026-05-18
**وثائق مرافقة / Companion docs:** `AUTONOMOUS_OPS_ARCHITECTURE.md` · `ORCHESTRATION_AND_AUTONOMY_LADDER.md` · `SALES_AUTONOMY_SYSTEM.md` · `../launch/MACHINE_ORCHESTRATION_MAP.md` · `../COMMERCIAL_WIRING_MAP.md`

---

## الغرض · Purpose

هذه الوثيقة هي السجل الكامل لكل وكيل في هرم العمليات الذاتية: الطبقة الأولى (منسّق تنفيذي واحد)، الطبقة الثانية (سبعة وكلاء أدوار)، والطبقة الثالثة (وكلاء المهام التسعة، ووكلاء النمو الخمسة، ووظائف ARQ الخمس). لكل وكيل بطاقة هوية على نمط `AgentCard`، ومالك مفتاح إيقاف (`kill_switch_owner`)، ومستوى استقلالية (`AutonomyLevel`)، ووحدة حقيقية مُسنِدة، وأنواع أفعال الموافقة التي يصفّها في `ApprovalStore`.

This document is the full registry of every agent in the autonomous-operations pyramid: Tier 1 (one Executive Orchestrator), Tier 2 (seven role agents), and Tier 3 (nine task agents, five growth agents, five ARQ jobs). Each agent carries an `AgentCard`-style identity block, a `kill_switch_owner`, an `AutonomyLevel`, a real backing module, and the `action_type`s it queues into `ApprovalStore`.

**تجميد تجاري نشط (Commercial Freeze):** هذه الوثيقة تصمّم السجل ولا تأذن ببناء كود منتج جديد.
This document designs the roster; it does not authorize new product code.

---

## كيف تُقرأ بطاقة الوكيل · How to read an agent card

كل بطاقة تطابق حقول الـ`AgentCard` المجمَّدة في `auto_client_acquisition/agent_os/`: `agent_id`, `name`, `owner`, `purpose`, `autonomy_level`, `status`, `allowed_tools`, `kill_switch_owner`, `notes`, `created_at`, `killed_reason`. الحالة `status` من `AgentStatus` StrEnum: `PROPOSED` · `ACTIVE` · `SUSPENDED` · `KILLED`. كل وكيل في هذا السجل بحالة `PROPOSED` لأن التجميد التجاري نشط — لا تسجيل `register_agent()` فعلي قبل رفع التجميد.

Every card matches the frozen `AgentCard` fields in `auto_client_acquisition/agent_os/`. All agents listed here are `PROPOSED`; no live `register_agent()` call happens before the freeze lifts.

- **حدود النطاق · Scope boundary** — ما يجوز للوكيل لمسه وما لا يجوز. أي فعل خارجي خارج النطاق ممنوع بالحدود الأربعة (`check_tool_boundary`, `check_data_boundary`).
- **أنواع الموافقة · Approval action_types** — من الأنواع الأحد عشر القانونية في `approval_center`. `—` تعني أن مخرجات الوكيل داخلية بالكامل (لا فعل خارجي).

---

## الطبقة الأولى — المنسّق التنفيذي · Tier 1 — Executive Orchestrator

### `executive_orchestrator`

| الحقل · Field | القيمة · Value |
|---|---|
| `agent_id` | `executive_orchestrator` |
| `name` | المنسّق التنفيذي · Executive Orchestrator |
| `owner` | Sami (founder) |
| `purpose` | يضع الأولويات اليومية، يفوّض إلى وكلاء الأدوار، يركّب طابور قرارات المؤسس · sets daily priorities, delegates to role agents, composes the founder decision queue |
| `autonomy_level` | `L3_RECOMMEND` |
| `status` | `PROPOSED` |
| `allowed_tools` | `build_role_brief`, قراءة `RoleBrief` من الأدوار السبعة, `/api/v1/founder/beast-command-center` |
| `kill_switch_owner` | Sami (founder) |

- **المهمة · Mission** — تحويل حالة العمل اليومية إلى قائمة قرارات مرتّبة للمؤسس؛ لا ينفّذ شيئًا بنفسه.
- **حدود النطاق · Scope boundary** — *يجوز:* قراءة موجزات الأدوار، ترتيب الأولويات، تركيب طابور القرار. *لا يجوز:* إرسال أي فعل خارجي، تجاوز `ApprovalStore`، تعديل سقف الاستقلالية.
- **المدخلات · Inputs** — سبعة `RoleBrief` من Tier 2، حالة `RuntimeState`، طابور الموافقات المعلّقة.
- **المخرجات · Outputs** — طابور قرارات المؤسس (founder decision queue)، أولويات اليوم، إحالات للأدوار.
- **الوحدة المُسنِدة · Backing module** — `auto_client_acquisition/role_command_os/` (`RoleName.CEO`, `build_role_brief`) · `/api/v1/founder/beast-command-center`.
- **أفعال الموافقة · Approval action_types** — `—` (مخرجاته داخلية: قائمة قرارات؛ القرارات الفردية تصفّ من الأدوار).

---

## الطبقة الثانية — وكلاء الأدوار السبعة · Tier 2 — The Seven Role Agents

كل وكيل دور يصدر `RoleBrief` عبر `build_role_brief(role)` ويحمل الحقول: `role`, `summary_ar/en`, `top_decisions`, `risks`, `approvals_needed`, `evidence_pointers`, `next_action_ar/en`, `blocked_actions`, `guardrails`. القرارات داخل الموجز من نوع `RoleDecision` (`title`, `rationale`, `risk_level`, `approval_required`, `proof_event`).

### `role_ceo`

| الحقل · Field | القيمة · Value |
|---|---|
| `agent_id` | `role_ceo` · `name` المدير التنفيذي · CEO role agent |
| `autonomy_level` | `L3_RECOMMEND` · `status` `PROPOSED` |
| `kill_switch_owner` | Sami (founder) |

- **المهمة · Mission** — يصدر موجز CEO: الصحة العامة، المخاطر العابرة للأدوار، القرار التالي.
- **حدود النطاق · Scope boundary** — *يجوز:* قراءة كل وحدات OS، إصدار `RoleBrief`. *لا يجوز:* تنفيذ أفعال خارجية أو تحصيل.
- **المدخلات · Inputs** — مخرجات الأدوار الستة الأخرى، `governance_os`, `proof_os`.
- **المخرجات · Outputs** — `RoleBrief(role=CEO)`، قرارات `RoleDecision` عابرة للأدوار.
- **الوحدة المُسنِدة · Backing module** — `role_command_os/` — `RoleBrief`, `RoleDecision`.
- **أفعال الموافقة · Approval action_types** — `—` (داخلي؛ يحيل الأفعال للأدوار المختصة).

### `role_sales`

| الحقل · Field | القيمة · Value |
|---|---|
| `agent_id` | `role_sales` · `autonomy_level` `L3_RECOMMEND` · `status` `PROPOSED` · `kill_switch_owner` Sami (founder) |

- **المهمة · Mission** — يشرف على قمع المبيعات من الاستقبال حتى تجهيز الحجز؛ يصدر موجز SALES.
- **حدود النطاق · Scope boundary** — *يجوز:* قراءة الـleads وحالاتها، توصية الترتيب، صفّ المسودات. *لا يجوز:* إرسال بريد/LinkedIn/مكالمة بلا موافقة.
- **المدخلات · Inputs** — مخرجات وكلاء المهام التسعة، `sales_os`, `client_os`.
- **المخرجات · Outputs** — `RoleBrief(role=SALES)`، طابور لمسات مُسوَّدة.
- **الوحدة المُسنِدة · Backing module** — `role_command_os/`؛ يشرف على `auto_client_acquisition/agents/`.
- **أفعال الموافقة · Approval action_types** — `draft_email`, `draft_linkedin_manual`, `call_script`, `follow_up_task`, `prepare_diagnostic`.

### `role_growth`

| الحقل · Field | القيمة · Value |
|---|---|
| `agent_id` | `role_growth` · `autonomy_level` `L3_RECOMMEND` · `status` `PROPOSED` · `kill_switch_owner` Sami (founder) |

- **المهمة · Mission** — يقود أعلى القمع؛ يصدر موجز GROWTH ويشغّل `GrowthOrchestrator`.
- **حدود النطاق · Scope boundary** — *يجوز:* تشغيل حملات قطاعية، صياغة محتوى، صفّ مسودات التوزيع. *لا يجوز:* نشر أو توزيع بلا موافقة، scraping.
- **المدخلات · Inputs** — `SectorIntelAgent`, `MarketResearchAgent`, `CompetitorMonitorAgent`، إشارات السوق المُوافَق على مصدرها.
- **المخرجات · Outputs** — `RoleBrief(role=GROWTH)`، مسودات محتوى وتوزيع.
- **الوحدة المُسنِدة · Backing module** — `role_command_os/` · `autonomous_growth/orchestrator.py` — `GrowthOrchestrator.run_sector_campaign()`.
- **أفعال الموافقة · Approval action_types** — `draft_linkedin_manual`, `draft_email`.

### `role_partnership`

| الحقل · Field | القيمة · Value |
|---|---|
| `agent_id` | `role_partnership` · `autonomy_level` `L3_RECOMMEND` · `status` `PROPOSED` · `kill_switch_owner` Sami (founder) |

- **المهمة · Mission** — يصدر موجز PARTNERSHIP: فرص الشركاء، التعريفات، حالة قناة `agency_partner_os`.
- **حدود النطاق · Scope boundary** — *يجوز:* تجهيز مسودات تعريف بالشركاء. *لا يجوز:* إرسال تعريف بلا موافقة.
- **المدخلات · Inputs** — سجل الشركاء، `client_os`, `value_os`.
- **المخرجات · Outputs** — `RoleBrief(role=PARTNERSHIP)`، مسودات تعريف.
- **الوحدة المُسنِدة · Backing module** — `role_command_os/`.
- **أفعال الموافقة · Approval action_types** — `partner_intro`.

### `role_customer_success`

| الحقل · Field | القيمة · Value |
|---|---|
| `agent_id` | `role_customer_success` (`RoleName.CUSTOMER_SUCCESS` = `"cs"`) · `autonomy_level` `L3_RECOMMEND` · `status` `PROPOSED` · `kill_switch_owner` Sami (founder) |

- **المهمة · Mission** — يصدر موجز CS: صحة العملاء النشطين، التسليمات، طلبات الإثبات.
- **حدود النطاق · Scope boundary** — *يجوز:* صياغة ردود دعم وطلبات إثبات كمسودات، تجهيز مهام تسليم. *لا يجوز:* إرسال رد للعميل بلا موافقة.
- **المدخلات · Inputs** — `adoption_os`, `client_os`, `proof_os`، حالة التسليم.
- **المخرجات · Outputs** — `RoleBrief(role=CS)`، مسودات ردود ومهام تسليم.
- **الوحدة المُسنِدة · Backing module** — `role_command_os/`.
- **أفعال الموافقة · Approval action_types** — `support_reply_draft`, `delivery_task`, `proof_request`, `follow_up_task`.

### `role_finance`

| الحقل · Field | القيمة · Value |
|---|---|
| `agent_id` | `role_finance` · `autonomy_level` `L3_RECOMMEND` · `status` `PROPOSED` · `kill_switch_owner` Sami (founder) |

- **المهمة · Mission** — يصدر موجز FINANCE: الإيراد المتحقّق، التذكيرات بالدفع، حالة التجديدات.
- **حدود النطاق · Scope boundary** — *يجوز:* صياغة تذكيرات دفع كمسودات. *لا يجوز:* تحصيل أو شحن (`no_live_charge`)، إرسال تذكير بلا موافقة.
- **المدخلات · Inputs** — `capital_os`, `value_os`، سجل الفواتير، عرض `revenue_proof_sprint_499` (499 SAR).
- **المخرجات · Outputs** — `RoleBrief(role=FINANCE)`، مسودات تذكير بالدفع.
- **الوحدة المُسنِدة · Backing module** — `role_command_os/`.
- **أفعال الموافقة · Approval action_types** — `payment_reminder`.

### `role_compliance`

| الحقل · Field | القيمة · Value |
|---|---|
| `agent_id` | `role_compliance` · `autonomy_level` `L1_ANALYZE` · `status` `PROPOSED` · `kill_switch_owner` Sami (founder) |

- **المهمة · Mission** — يصدر موجز COMPLIANCE: التزام القائمة غير القابلة للتفاوض، الموافقات على البيانات، الانحرافات.
- **حدود النطاق · Scope boundary** — *يجوز:* قراءة سجلات التدقيق، رفع المخاطر. *لا يجوز:* تنفيذ أو موافقة على أي فعل — يحلّل ويحذّر فقط.
- **المدخلات · Inputs** — `governance_os`, `agent_identity_access_os`، سجلات الحدود الأربعة، `SourcePassport`.
- **المخرجات · Outputs** — `RoleBrief(role=COMPLIANCE)`، تنبيهات انحراف، قائمة `blocked_actions`.
- **الوحدة المُسنِدة · Backing module** — `role_command_os/` · `governance_os`.
- **أفعال الموافقة · Approval action_types** — `—` (تحليلي بحت؛ يحظر ولا يصفّ).

---

## الطبقة الثالثة — وكلاء المهام · Tier 3 — Task Agents

### أصناف `auto_client_acquisition/agents/` (×9) · Acquisition task agents

سقف استقلالية هذه الطبقة هو `L3_RECOMMEND`؛ لا وكيل مهمة يبلغ L4 أو L5. `kill_switch_owner` لجميعها: Sami (founder). الحالة `PROPOSED`.

| `agent_id` · الصنف · Class | المهمة · Mission | الحدود · Scope (يجوز / لا يجوز · may / may NOT) | المدخلات · Inputs | المخرجات · Outputs | `AutonomyLevel` | `action_type`s للموافقة |
|---|---|---|---|---|---|---|
| `IntakeAgent` | استقبال الـlead والتحقق من المصدر · receive lead, verify source | يجوز: قراءة الـlead، ختم `SourcePassport` / لا يجوز: قبول lead بلا موافقة مصدر (`no_scraping`, `no_unconsented_data`) | lead خام مع مصدر · raw lead + source | lead موثّق المصدر · source-stamped lead | `L1_ANALYZE` | `—` (داخلي) · `prepare_diagnostic` عند تجهيز تشخيص |
| `ICPMatcherAgent` | تهديف ملاءمة الـICP · score ICP fit | يجوز: حساب `icp_score` / لا يجوز: رفض lead خارجيًا أو إخطاره | lead موثّق · `sales_os` معايير ICP | درجة `icp_score` · ICP score | `L1_ANALYZE` | `—` (داخلي) |
| `PainExtractorAgent` | استخراج الألم من إشارات موثّقة · extract declared pain | يجوز: قراءة إشارات مُوافَق عليها / لا يجوز: استنتاج ألم من بيانات بلا موافقة | إشارات الـlead الموثّقة · consented signals | ملف ألم · pain profile | `L1_ANALYZE` | `—` (داخلي) |
| `QualificationAgent` | إصدار توصية تأهيل · issue qualification verdict | يجوز: استدعاء `sales_os.qualify`، التوصية / لا يجوز: تأهيل نهائي بلا مراجعة | درجة ICP + ملف الألم · ICP score + pain profile | توصية تأهيل · qualification verdict | `L3_RECOMMEND` | `prepare_diagnostic` |
| `ProposalAgent` | صياغة هيكل مقترح · draft proposal skeleton | يجوز: بناء هيكل مقترح 499 SAR / لا يجوز: إرسال المقترح أو تسعيره خارج السجل (`no_hidden_pricing`) | lead مؤهّل · qualified lead · `revenue_proof_sprint_499` | هيكل مقترح · proposal skeleton | `L2_DRAFT` | `upsell_recommendation` (للترقية · for upgrade) |
| `OutreachAgent` | صياغة لمسات التواصل · draft outreach touches | يجوز: صياغة مسودات بريد / LinkedIn يدوية / لا يجوز: إرسال، WhatsApp بارد، DM جماعي (`no_live_send`, `no_cold_whatsapp`) | lead + سياق المقترح · lead + proposal context | مسودات بريد / LinkedIn · email / LinkedIn drafts | `L2_DRAFT` | `draft_email`, `draft_linkedin_manual` |
| `FollowUpAgent` | جدولة مهام المتابعة · schedule follow-up tasks | يجوز: تجهيز مهمة متابعة كمسودة / لا يجوز: إرسال متابعة تلقائيًا | حالة الـlead · lead state | مهمة متابعة مُسوَّدة · drafted follow-up task | `L2_DRAFT` | `follow_up_task` |
| `BookingAgent` | تجهيز نص المكالمة وفتحات الحجز · prepare call script + slots | يجوز: تجهيز فتحات ونص مكالمة / لا يجوز: حجز demo تلقائيًا (`no_live_send`) | تقويم المؤسس + الـlead · founder calendar + lead | فتحات + نص + تأكيد مُسوَّد · slots + script + drafted confirmation | `L3_RECOMMEND` | `call_script`, `follow_up_task` |
| `CRMAgent` | تحديث سجلات CRM داخليًا · update CRM records internally | يجوز: كتابة حالة الـlead في `client_os` / لا يجوز: أي فعل خارجي أو إخطار | أحداث القمع · funnel events | سجل CRM محدّث · updated CRM record | `L4_AUTO_WITH_AUDIT` (داخلي مدقَّق فقط · internal audited only) | `—` (داخلي) |

> ملاحظة · Note: `CRMAgent` هو الوكيل الوحيد في هذا السجل على `L4_AUTO_WITH_AUDIT` لأن عمله داخلي بالكامل ومدقَّق؛ L4 لا يعني أبدًا فعلًا خارجيًا.

### أصناف `autonomous_growth/agents/` (×5) · Growth task agents

تُشغَّل تحت `role_growth` عبر `GrowthOrchestrator.run_sector_campaign()`. `kill_switch_owner`: Sami (founder). الحالة `PROPOSED`.

| `agent_id` · الصنف · Class | المهمة · Mission | الحدود · Scope (يجوز / لا يجوز) | المدخلات · Inputs | المخرجات · Outputs | `AutonomyLevel` | `action_type`s للموافقة |
|---|---|---|---|---|---|---|
| `SectorIntelAgent` | جمع إشارات القطاع المُجمَّعة · gather aggregated sector signals | يجوز: قراءة مصادر مُوافَق عليها / لا يجوز: scraping، نشر مقاييس سرية | تعريف القطاع · sector definition | إشارات قطاعية مُجمَّعة · aggregated sector signals | `L1_ANALYZE` | `—` (داخلي) |
| `MarketResearchAgent` | تحليل السوق والطلب · analyze market & demand | يجوز: تحليل أنماط مُجمَّعة / لا يجوز: ادعاء أرقام كحقيقة (`no_unverified_outcomes`) | إشارات القطاع · sector signals | تحليل سوق · market analysis | `L1_ANALYZE` | `—` (داخلي) |
| `ContentCreatorAgent` | صياغة مسودات محتوى · draft content | يجوز: صياغة مسودات مطابقة للرواية الرسمية / لا يجوز: نشر، استخدام اسم عميل وهمي (`no_fake_proof`) | تحليل السوق · market analysis | مسودات محتوى · content drafts | `L2_DRAFT` | `draft_linkedin_manual`, `draft_email` |
| `DistributionAgent` | تجهيز خطة توزيع كمسودة · prepare distribution plan as draft | يجوز: تجهيز جدول توزيع مقترح / لا يجوز: نشر تلقائي، أتمتة LinkedIn (`no_live_send`) | مسودات المحتوى · content drafts | خطة توزيع مُسوَّدة · drafted distribution plan | `L2_DRAFT` | `draft_linkedin_manual` |
| `CompetitorMonitorAgent` | مراقبة المنافسين من مصادر علنية · monitor competitors from public sources | يجوز: قراءة مصادر علنية / لا يجوز: scraping، جمع بيانات بلا موافقة | تعريف المنافسين · competitor set | تقرير مراقبة · monitoring report | `L1_ANALYZE` | `—` (داخلي) |

### وظائف ARQ في `core/queue/tasks.py` (×5) · Background ARQ jobs

تُستدعى عبر `run_agent_job()`؛ منفّذون في الخلفية، محدودون، تابعون لـ Tier 3. `kill_switch_owner`: Sami (founder). الحالة `PROPOSED`.

| `agent_id` · الوظيفة · Job | المهمة · Mission | الحدود · Scope (يجوز / لا يجوز) | المخرجات · Outputs | `AutonomyLevel` | `action_type`s للموافقة |
|---|---|---|---|---|---|
| `lead_score` | تهديف الـleads دفعةً · batch lead scoring | يجوز: حساب الدرجات داخليًا / لا يجوز: فعل خارجي | درجات leads · lead scores | `L1_ANALYZE` | `—` (داخلي) |
| `proposal_draft` | توليد مسودات مقترحات · generate proposal drafts | يجوز: بناء هياكل مقترحات / لا يجوز: إرسال أو تسعير خارج السجل | مسودات مقترحات · proposal drafts | `L2_DRAFT` | `upsell_recommendation` |
| `outreach_batch` | تجهيز دفعة لمسات كمسودات · prepare a batch of outreach drafts | يجوز: إنتاج مسودات فقط / لا يجوز: إرسال دفعي (`no_live_send`, `no_cold_whatsapp`) | مسودات لمسات · outreach drafts | `L2_DRAFT` | `draft_email`, `draft_linkedin_manual` |
| `embedding_index` | فهرسة المتجهات داخليًا · internal embedding indexing | يجوز: بناء فهرس داخلي مدقَّق / لا يجوز: فعل خارجي | فهرس متجهات · vector index | `L4_AUTO_WITH_AUDIT` (داخلي مدقَّق · internal audited) | `—` (داخلي) |
| `commercial_sprint_report` | توليد تقرير سبرنت تجاري · generate commercial sprint report | يجوز: تجميع تقرير من بيانات موسومة / لا يجوز: ادعاء نتائج غير مُتحقَّقة كحقيقة | تقرير سبرنت · sprint report | `L1_ANALYZE` | `proof_request` (عند طلب إثبات · when requesting proof) |

---

## ملخّص توزيع الاستقلالية · Autonomy Distribution Summary

| `AutonomyLevel` | عدد الوكلاء · Agent count | أمثلة · Examples |
|---|---|---|
| `L1_ANALYZE` | 9 | `role_compliance`, `IntakeAgent`, `ICPMatcherAgent`, `lead_score`, `SectorIntelAgent` |
| `L2_DRAFT` | 6 | `ProposalAgent`, `OutreachAgent`, `FollowUpAgent`, `ContentCreatorAgent`, `proposal_draft`, `outreach_batch` |
| `L3_RECOMMEND` | 11 | `executive_orchestrator`, وكلاء الأدوار الستة, `QualificationAgent`, `BookingAgent` |
| `L4_AUTO_WITH_AUDIT` | 2 | `CRMAgent`, `embedding_index` — **داخلي مدقَّق فقط · internal audited only** |
| `L5_FULLY_AUTONOMOUS` | 0 | **محظور · blocked** (`MAX_AUTONOMY_LEVEL_MVP = L4`) |

لا وكيل في السجل يبلغ L5. الوكيلان على L4 يعملان داخليًا بالكامل ولا يصفّان أي فعل خارجي. تفصيل السلّم في [`ORCHESTRATION_AND_AUTONOMY_LADDER.md`](ORCHESTRATION_AND_AUTONOMY_LADDER.md).

No agent reaches L5. The two L4 agents act fully internally and queue no external action. Full ladder detail in [`ORCHESTRATION_AND_AUTONOMY_LADDER.md`](ORCHESTRATION_AND_AUTONOMY_LADDER.md).

---

> النتائج التقديرية ليست نتائج مضمونة / Estimated outcomes are not guaranteed outcomes.
