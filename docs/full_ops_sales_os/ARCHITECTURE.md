# Full Ops Sales System — المعمارية
<!-- WAVE 18 | Owner: Founder | Date: 2026-05-18 -->
<!-- Arabic primary — العربية أولاً -->

> هذا المستند يصف *كيف* تتصل الوحدات. التفاصيل التنفيذية في الكود؛ هذا
> المستند يبقى المصدر الأعلى — لا يسبقه الكود.

---

## 1. المبدأ — The Principle

`FullOpsOrchestrator` يشغّل دورة المبيعات كاملةً كآلة واحدة. لكل مرحلة:
وحدة تنفّذ، عقد يصف القرار، وحدّ تصنيف يقرّر هل تُنفَّذ ذاتياً أم تنتظر موافقة.

```
                ┌─────────────────────────────────────────┐
                │        FullOpsOrchestrator               │
                │  (control_plane_os.WorkflowRun spine)     │
                └───────────────┬───────────────────────────┘
                                │ لكل مرحلة:
        EventEnvelope ◄─────────┤  1) ينفّذ وحدة المرحلة
        AuditEntry    ◄─────────┤  2) ينتج DecisionOutput
                                │  3) يصنّف الإجراء (A/R/S)
                                ▼
                ┌───────────────────────────────┐
                │  هل الإجراء A0 + R0/R1 + S0/S1؟ │
                └──────┬─────────────────┬───────┘
                   نعم │                 │ لا
                       ▼                 ▼
              تنفيذ ذاتي فوري      ApprovalTicket → approval_center
              + AuditEntry         (المؤسس يوافق بضغطة)
```

---

## 2. الخيط الذهبي — The 12-Stage Golden Chain

| # | المرحلة | الوحدة | فئة الإجراء | الوضع |
|---|---------|--------|-------------|-------|
| 1 | استقبال الإشارة / Lead | `data_os.SourcePassport` + `lead_intake` | `A0` | ذاتي |
| 2 | تخصيب البيانات | `revenue_os.enrichment_waterfall` | `A0` `enrichment_query` | ذاتي |
| 3 | التقييم (ICP/حساب) | `sales_os.icp_score`, `revenue_os.account_scoring`, `command_os` | `A0` `icp_match` | ذاتي |
| 4 | استخراج الألم | محرّك `pain_extract` | `A0` | ذاتي |
| 5 | التأهيل (8 أسئلة) | `sales_os.qualification` | `A0` `qualification_questions` | ذاتي |
| 6 | ترتيب الأولويات | `revenue_pipeline.pipeline` + `stage_policy` | `A0` داخلي | ذاتي |
| 7 | توليد المسودّات | `sales_os.proposal_renderer`, `revenue_os.draft_pack` | `A0` `*_generate_draft` | ذاتي (مسودّة فقط) |
| 8 | **بوابة الموافقة** | `approval_center.ApprovalStore` | `A1/A2` `outreach_send`, `proposal_send`, `followup_send`, `booking_schedule` | **موافقة** |
| 9 | التسليم | `proof_os.assemble` + خطوات الـSprint | إجراءات تسليم مصنّفة | مختلط |
| 10 | الإثبات | `proof_os` ProofPack (score ≥ 70) | `A0` داخلي | ذاتي |
| 11 | التوسّع | `adoption_os.retainer_readiness`, `client_os` إشارات | `A0` تحليل | ذاتي |
| 12 | التعلّم | `friction_log`, `capital_os`, إعادة تقييم `command_os` | `A0` داخلي | ذاتي |

> الإجراءات في `NEVER_AUTO_EXECUTE` (`pricing_offer_commit`, `contract_change`,
> `nda_send`, `payment_terms_change`, `regulator_communication`,
> `sensitive_data_export`, `market_facing_statement`) لا تُنفَّذ ذاتياً أبداً
> ولو طلب المستخدم — تُحجب وتُصعَّد للمؤسس.

---

## 3. حدّ الأتمتة — The Auto-Exec Boundary

القرار يأتي من `dealix/classifications/ACTION_CLASSIFICATIONS` على ثلاثة محاور:

| المحور | القيم | قاعدة الأتمتة الذاتية |
|--------|-------|------------------------|
| `ApprovalClass` | A0 / A1 / A2 / A3 | `A0` فقط |
| `ReversibilityClass` | R0 / R1 / R2 / R3 | `R0` أو `R1` فقط |
| `SensitivityClass` | S0 / S1 / S2 / S3 | `S0` أو `S1` فقط |

`auto_exec_allowed(action) == (A0) ∧ (R0∨R1) ∧ (S0∨S1) ∧ (action ∉ NEVER_AUTO_EXECUTE)`

أي نوع إجراء جديد يضيفه أي wave **يجب** أن يُصنَّف في `ACTION_CLASSIFICATIONS`
قبل أن يعمل — لا إجراء بلا تصنيف.

---

## 4. العقود — Contracts (`dealix/contracts/`)

| العقد | الدور في الحلقة |
|-------|------------------|
| `DecisionOutput` | مخرج كل مرحلة: توصية + ثقة + تبرير + أدلة + فئات A/R/S + `next_actions` |
| `EventEnvelope` | CloudEvents 1.0 — تُبثّ عند كل انتقال مرحلة |
| `EvidencePack` | حزمة الأدلة لكل قرار؛ `is_complete` شرط إغلاق Proof Pack |
| `AuditEntry` | سجلّ append-only لكل انتقال؛ لا حركة صامتة |

قاعدة: قرار `A2+` أو `R3` يجب أن يحمل ≥1 عنصر دليل.

---

## 5. طبقة الأجينتس — The Agent Layer

`FullOpsOrchestrator` لا "يفعل" بنفسه — بل يوزّع على هرم أجينتس وقت-التشغيل،
كلٌّ بـ`AgentCard` (هوية + `AutonomyLevel`). التفصيل في
[RUNTIME_AGENT_HIERARCHY.md](RUNTIME_AGENT_HIERARCHY.md). القاعدة الحاكمة:

- أجينتس التنسيق والمراحل الداخلية الآمنة → حتى `L4_AUTO_WITH_AUDIT`.
- أي أجينت يلمس الخارج → سقفه `L2_DRAFT` — يصوغ ولا يرسل أبداً.
- `governance-warden` يقيّم كل إجراء قبل تنفيذه (`agent_governance.evaluate_action`).

---

## 6. الطبقات التقنية — Technical Layers

| الطبقة | الموقع | المحتوى |
|--------|--------|---------|
| الواجهة | `frontend/src/app/[locale]/` | Full Ops Console: لوحة pipeline، تغذية الأجينتس، صندوق الموافقات، اللوحة اليومية |
| الـAPI | `api/routers/full_ops*.py` (جديد) | `prefix=/api/v1/full-ops`؛ كل ردّ يحمل `governance_decision` |
| التنسيق | `auto_client_acquisition/full_ops_os/` (جديد) | `FullOpsOrchestrator`، سجلّ المراحل، الموزّع |
| الوحدات | الوحدات القانونية القائمة | منطق كل مرحلة (نقي، بلا I/O) |
| الحوكمة | `governance_os`, `agent_governance`, `classifications` | تقييم كل إجراء + حدّ الأتمتة |
| العقود والسجلّات | `contracts/`, `*_ledger` | التتبّع والأدلة وسجلّ التدقيق |

> الوحدة الجديدة الوحيدة هي `full_ops_os/` (التنسيق) + موجِّهات `full-ops`.
> كل شيء آخر إعادة استخدام — لا إعادة تسمية، لا وحدة موازية.

---

## 7. مبادئ ثابتة — Invariants

1. لا انتقال مرحلة بلا `EventEnvelope` + `AuditEntry`.
2. لا إجراء بلا تصنيف A/R/S.
3. لا إرسال خارجي إلا عبر `approval_center`.
4. لا أجينت بلا `AgentCard`؛ لا أجينت خارجي فوق `L2`.
5. لا مشروع مغلق بلا Proof Pack (score ≥ 70) وCapital Asset.
6. كل مخرج عميل يحمل `governance_decision` والإخلاء ثنائي اللغة.

---

*Version 1.0 | Architecture is the source of truth | Code never drifts ahead.*
