# Dealix Full Ops — المخطط المعماري الشامل / Architecture Blueprint

> **حالة الوثيقة:** مخطط (Phase 0). لا كود بعد. كل مرحلة بناء لاحقة تُفتح بموافقة صريحة.
> **Status:** Blueprint (Phase 0). No code yet. Each build phase opens on explicit approval.

---

## 0. الملخص التنفيذي / Executive Summary

**بالعربية —** Dealix يملك أصلاً 72 وحدة OS، 141 موجّه API (~794 endpoint)، واجهة `/ops` كاملة،
مركز موافقات، منسّق leads، وخمسة sub-agents. **المشكلة ليست نقص بناء — المشكلة أن هذه القطع غير
موحّدة تحت عقل واحد ذاتي التشغيل.** هذا المخطط يصمم **Full Ops**: طبقة تنسيق واحدة (OpsConductor)
تدير هرماً من الوكلاء التنفيذيين فوق الوحدات الموجودة، مع **مقياس استقلالية (Autonomy Dial L0–L5)**
يضبط لكل نوع فعل كم يتصرف النظام ذاتياً وأين تبقى لمسة بشرية.

**English —** Dealix already has 72 OS modules, 141 API routers (~794 endpoints), a full `/ops`
console, an approval center, a lead orchestrator, and five sub-agents. **The gap is not missing
code — it is that these parts are not unified under one self-operating brain.** This blueprint
designs **Full Ops**: a single coordination layer (`OpsConductor`) running an agent hierarchy on
top of the existing modules, governed by an **Autonomy Dial (L0–L5)** set per action class.

### القرار الجوهري / The core decision

You chose **true full autonomy**. This blueprint delivers it — with one engineering-honest
refinement:

- **9 of the 11 non-negotiables are quality/legality guards, not autonomy brakes.** They stay
  fully enforced at every autonomy level (no scraping, no fake claims, no PII in logs, source
  passport, agent identity, proof pack, capital asset). Autonomy does not need to touch them.
- **Only 2 rules actually gate autonomy:** `no external action without approval` and
  `no_cold_whatsapp` / `no_live_charge`. The blueprint converts *these two* from hard blocks into
  **policy-graded autonomy thresholds** — so the system can run at L5 where you set it to.
- **Recommended default:** L5 (full autonomy) for everything **except** financial charges and
  cold first-contact, which default to **L4 (supervised autonomy with a veto window)** — the
  system still executes itself with zero founder work, but a wrong charge or wrong cold message
  can be caught inside a short window. **At L4 the founder does ~0 daily work; it is still
  "fully self-operating."** You may dial those two to L5; §5 documents exactly what that costs.

> **تحذير هندسي / Engineering warning.** الخصم المالي التلقائي (L5) والإرسال البارد التلقائي (L5)
> بلا أي نافذة تحقق يعرّضان حساب Moyasar للتجميد ويخلقان مسؤولية PDPL. المعمارية تدعمهما، والقرار لك.

---

## 1. النطاق والمبادئ / Scope & Principles

**Scope** — the four axes you selected, as one system:

| Axis | المحور | يُبنى فوق |
|------|--------|-----------|
| A | محرك المبيعات / Sales Engine | `leadops_spine`, `sales_os`, `value_os`, `crm_v10`, `approval_center` |
| B | الماكينة الداخلية / Internal Machine | `delivery_factory`, `proof_os`, `capital_os`, `data_os`, `diagnostic_engine` |
| C | هرم الوكلاء / Agent Hierarchy | `orchestrator/`, `core/agents`, `core/queue`, `agent_os`, `command_os` |
| D | لوحة Full Ops / Ops Console | `frontend/.../ops/*`, `approval_center`, `business_metrics_board` |

**Principles**

1. **Wrap, don't rewrite.** Every capability below maps to an existing module. New code is
   *coordination + the autonomy layer + console glue*, not new business logic.
2. **One brain, many hands.** A single `OpsConductor` plans; tier-1 directors own domains;
   tier-2 executors do bounded tasks; tier-3 = existing OS functions.
3. **Autonomy is a setting, not a rewrite.** Every action class reads its level from one config.
4. **Everything is logged.** Every autonomous action writes to an audit ledger — this is what
   keeps CI meaningful and makes L5 auditable after the fact.
5. **Reversibility shapes the dial.** Irreversible/high-blast-radius actions (charge, cold
   first-contact) get a lower default level than reversible ones.

---

## 2. جرد الأنظمة الموجودة / Existing System Inventory

Full Ops is an *integration*. Build on these — do not duplicate.

### 2.1 Backend OS modules (72) — grouped

| Group | Modules (selected) |
|-------|--------------------|
| Lead → Revenue | `leadops_spine` (orchestrator, draft_builder, offer_router, compliance_gate), `leadops_reliability`, `sales_os` (icp_score, qualification, proposal), `revenue_pipeline`, `crm_v10`, `value_os` (value_ledger) |
| Delivery → Proof | `delivery_factory`, `diagnostic_engine`, `proof_os`, `proof_architecture_os`, `capital_os` (capital_ledger), `data_os` |
| Governance / Trust | `governance_os` (approval_matrix, draft_gate, policy_check), `trust_os`, `compliance_os` (consent_ledger), `runtime_safety_os`, `auditability_os`, `evidence_control_plane_os`, `compliance_trust_os` (approval_engine) |
| Agents / Orchestration | `agent_os`, `agent_mesh_os`, `agent_governance`, `agent_identity_access_os`, `agentic_operations_os`, `agent_observability`, `orchestrator/`, `command_os`, `execution_os`, `workflow_os` |
| Ops / Intelligence | `full_ops` (work_queue, prioritizer), `control_plane_os`, `business_metrics_board`, `bottleneck_radar`, `reporting_os`, `observability_v10`, `friction_log`, `self_evolving_os`, `unified_operating_graph`, `intelligence_os`, `market_intelligence` |
| Customer / Growth | `client_os`, `customer_brain`, `customer_success`, `adoption_os`, `expansion_engine`, `gtm_os`, `proof_to_market`, `case_study_engine`, `ecosystem_os` |
| Finance / Platform | `finance_os`, `payment_ops`, `llm_gateway_v10`, `platform_v10`, `service_catalog`, `security_privacy` |

### 2.2 Runtime infra that already exists

- **Orchestration:** `auto_client_acquisition/orchestrator/runtime.py` (+ `policies.py`, `queue.py`),
  `leadops_spine/orchestrator.py`, `core/agents/multi_agent.py`.
- **Queue/worker:** `core/queue/tasks.py`, `core/queue/worker.py`, `core/tasks/worker.py`,
  `core/queue/weekly_self_improvement.py`.
- **Work queue:** `auto_client_acquisition/full_ops/{work_queue,work_item,prioritizer}.py`.
- **Approval:** `approval_center/{approval_store,approval_renderer,founder_rules}.py`,
  `compliance_trust_os/approval_engine.py` (7-state `GovernanceDecision`).

### 2.3 Frontend `/ops` console (already shipped)

`frontend/src/app/[locale]/ops/` — `founder`, `war-room`, `approvals`, `sales`, `support`,
`marketing`, `partners`, `targeting`, `evidence`. Components in `components/gtm/` +
`components/approvals/`. Stack: Next 15, shadcn/Radix, Tailwind, axios (`lib/api.ts`),
`next-intl` (ar/en, RTL), Recharts.

### 2.4 Ledgers (write targets)

`value_os/value_ledger`, `capital_os/capital_ledger`, `compliance_os/consent_ledger`,
`control_plane_os/postgres_ledger`, `friction_log` (append-only), `trust_os/ai_control_plane`,
`db.AuditLogRecord`.

### 2.5 Build-time vs run-time agents

- **Build-time agents** = `.claude/agents/` (dealix-pm, -engineer, -delivery, -sales, -content).
  They *construct* Full Ops. Used to execute this blueprint's phases.
- **Run-time agents** = the Python `OpsConductor` hierarchy in §6. They *run the business*.
  Distinct systems — do not conflate.

---

## 3. مقياس الاستقلالية / The Autonomy Dial

The heart of Full Ops. One config governs how autonomously every action executes.

### 3.1 Levels

| Level | Name | Behaviour |
|-------|------|-----------|
| **L0** | Off | Action disabled. |
| **L1** | Assist | Agent analyses only; human does the action. |
| **L2** | Draft-gate | Agent drafts + queues; human approves each item. *(today's default)* |
| **L3** | Batch-approve | Agent drafts + queues; human approves in batches / by exception. |
| **L4** | Supervised autonomy | Agent **executes automatically**; action is held in a **veto window** (e.g. 15–60 min); auto-proceeds if not vetoed. Founder does 0 work unless something looks wrong. |
| **L5** | Full autonomy | Agent executes immediately; **no gate**; post-hoc audit ledger only. |

### 3.2 Action classes (each gets its own level)

| # | Action class | Reversible? | Recommended default | Max safe |
|---|--------------|-------------|---------------------|----------|
| 1 | Internal compute (score, analyse, research) | yes | **L5** | L5 |
| 2 | Internal artifact (draft, proof pack, report) | yes | **L5** | L5 |
| 3 | Internal state change (stage move, task assign) | yes | **L5** | L5 |
| 4 | Warm external send (existing contact, consent on file) | hard | **L5** | L5 |
| 5 | Cold external first-contact | hard | **L4** (veto window) | L5 (see §5) |
| 6 | Financial charge (invoice send, payment capture) | **very hard** | **L4** (veto window) | L5 (see §5) |
| 7 | Partner / affiliate commitment | hard | **L4** | L5 |
| 8 | Publish content (LinkedIn / X) | hard | **L4** | L5 |

### 3.3 Config (single source of truth)

```yaml
# config/autonomy.yaml  — read by OpsConductor on every action
autonomy:
  internal_compute:        L5
  internal_artifact:       L5
  internal_state:          L5
  warm_external_send:      L5
  cold_first_contact:      L4    # veto_window: 60m   ← dial to L5 per §5
  financial_charge:        L4    # veto_window: 60m   ← dial to L5 per §5
  partner_commitment:      L4
  publish_content:         L4
veto_window_minutes: 60
kill_switch: false               # true => everything drops to L1 instantly
```

> **النتيجة:** عند الإعداد الموصى به، النظام ذاتي التشغيل بالكامل — المؤسس لا ينفّذ شيئاً يومياً.
> الفرق الوحيد عن L5 الكامل: نافذة 60 دقيقة يقدر يلغي فيها خصماً خاطئاً أو رسالة باردة خاطئة.

---

## 4. الهرم — البنية / Agent Hierarchy

```
                         ┌──────────────────────────┐
              schedule →  │   Tier 0 — OpsConductor   │ ← config/autonomy.yaml
                         │  plan · dispatch · collect │
                         │  escalate · update tower   │
                         └─────────────┬──────────────┘
        ┌───────────────┬──────────────┼───────────────┬──────────────┐
   ┌────▼────┐    ┌──────▼─────┐  ┌─────▼─────┐   ┌──────▼─────┐  ┌─────▼────┐
   │ Revenue │    │  Delivery  │  │  Growth   │   │ Governance │  │   Ops    │
   │ Director│    │  Director  │  │ Director  │   │  Director  │  │ Director │
   └────┬────┘    └──────┬─────┘  └─────┬─────┘   └──────┬─────┘  └─────┬────┘
        │ Tier 2 executors (bounded-task agents) ...     │              │
   Lead Scout       Source Passport   Content Writer  Policy Checker  Scorecard
   Lead Scorer      DQ Scorer         Post Scheduler  PII Redactor    Health Monitor
   ICP Qualifier    Account Scorer    Partner Scout   Approval Router Friction Aggregator
   Draft Writer     Proof Assembler   Affiliate Mgr   Truth Verifier  Escalation Handler
   Sequence Runner  Capital Registrar Benchmark Bldr  Audit Logger    Self-Improve Agent
   Follow-up Agent  Sprint Runner
   Closer / Proposer
   Objection Responder
        │
   Tier 3 — existing OS module functions (sales_os.icp_score(), proof_os.assemble(), ...)
```

### 4.1 Tier 0 — OpsConductor

The single brain. Runs on a schedule (§12). Each cycle: read state from the operating graph →
plan the day's work items (`full_ops/prioritizer.py`) → dispatch to directors → collect results →
update the Commercial Control Tower → raise escalations. Built by wrapping
`orchestrator/runtime.py` + `command_os` + `unified_operating_graph`.

### 4.2 Tier 1 — Directors (strategic agents)

One per domain. Each owns a goal, a budget (LLM/time), a set of executors, and a slice of the
autonomy config. Directors plan; they do not call external APIs directly.

| Director | Owns | Backed by |
|----------|------|-----------|
| Revenue | pipeline from lead to paid | `leadops_spine`, `sales_os`, `value_os`, `crm_v10` |
| Delivery | sprint → proof pack → capital asset | `delivery_factory`, `proof_os`, `capital_os`, `diagnostic_engine` |
| Growth | content, distribution, partners, benchmarks | `gtm_os`, `proof_to_market`, `case_study_engine`, `ecosystem_os` |
| Governance | policy, PII, approvals, audit, truth labels | `governance_os`, `trust_os`, `compliance_os`, `auditability_os` |
| Ops | scorecard, health, friction, escalations, self-improvement | `business_metrics_board`, `bottleneck_radar`, `friction_log`, `self_evolving_os` |

### 4.3 Tier 2 — Executors (operational agents)

Bounded-task agents. Each has a strict **contract**:

```
AgentCard:
  id, name, tier, director
  identity_card_ref      # non-negotiable #9 — registered identity
  input_schema           # typed
  output_schema          # typed
  allowed_action_classes # subset of the 8 in §3.2
  autonomy_binding       # reads level from config per action class
  ledger_writes          # which ledgers it must write
  tools                  # tier-3 OS functions it may call
  budget                 # max LLM calls / runtime per cycle
```

### 4.4 Tier 3 — Tools

Existing OS module functions. Agents never reach the DB or external APIs directly — only through
tier-3 functions, which already carry governance hooks.

---

## 5. الحوكمة تحت الأتمتة الكاملة / Governance under Full Autonomy

### 5.1 The 11 non-negotiables, reclassified

| # | Non-negotiable | Under Full Ops |
|---|----------------|----------------|
| 1 | No scraping | **Preserved at all levels** — never an autonomy question |
| 2 | No cold WhatsApp | **Becomes the `cold_first_contact` dial** — see §5.2 |
| 3 | No LinkedIn automation | Becomes `publish_content` + `cold_first_contact` dial |
| 4 | No fake / un-sourced claims | **Preserved at all levels** |
| 5 | No guaranteed sales outcomes | **Preserved at all levels** |
| 6 | No PII in logs | **Preserved at all levels** |
| 7 | No source-less answers | **Preserved at all levels** |
| 8 | No external action without approval | **Becomes the `warm/cold send` + `financial_charge` dials** |
| 9 | No agent without identity | **Preserved + extended** — every tier-2 agent has an identity card |
| 10 | No project without Proof Pack | **Preserved + automated** by Delivery Director |
| 11 | No project without Capital Asset | **Preserved + automated** by Delivery Director |

**Takeaway:** 8 of 11 stay hard-enforced exactly as today. Full autonomy only reinterprets
**#2, #3, #8** — and only for the action classes you dial to L4/L5.

### 5.2 What dialing to L5 actually costs

To run `cold_first_contact` or `financial_charge` at **L5** (no veto window):

1. **Code:** `compliance_trust_os/approval_engine.py` — `governance_decision_for_pii_external()`
   reads `config/autonomy.yaml`; at L5 for that class it returns `ALLOW` + records to the audit
   ledger instead of `REQUIRE_APPROVAL`.
2. **Guards:** `governance_os/draft_gate`, `leadops_spine/compliance_gate` — same: graded by
   config, not hard-coded.
3. **CI tests** — rewrite from "always blocks" to "respects configured level **and** records the
   action". Shape:

   ```python
   # before:  asserts the action is always blocked
   def test_no_cold_whatsapp():
       assert policy_check_draft("cold whatsapp ...").allowed is False

   # after:  asserts the dial is honoured and every autonomous send is audited
   def test_cold_contact_respects_autonomy_dial():
       with autonomy(cold_first_contact="L2"):
           assert policy_check_draft("cold ...").decision == "REQUIRE_APPROVAL"
       with autonomy(cold_first_contact="L5"):
           r = policy_check_draft("cold ...")
           assert r.decision == "ALLOW"
           assert audit_ledger.last().action_class == "cold_first_contact"  # never silent
   ```

   CI stays meaningful and green: it now proves the dial works and **nothing executes silently**.
4. **Kept regardless:** PII redaction, source passport, no-fake-claims, audit logging, the
   `kill_switch`. These are never dialed off.

> **التوصية تبقى:** اترك `financial_charge` و`cold_first_contact` على L4. النظام يبقى ذاتي التشغيل
> 100% (المؤسس لا يعمل شيئاً)، لكن نافذة الـ60 دقيقة تمنع كارثة لا رجعة فيها. ارفعهما إلى L5 فقط بعد
> ما يثبت النظام عبر مئات الأفعال في L4.

### 5.3 Always-on safety (every level, including L5)

Kill switch (one flag → everything to L1) · per-class budgets / rate limits · anomaly detector
(spike in charges or sends → auto-drop to L2 + escalate) · full audit ledger · daily founder
digest of everything executed.

---

## 6. المحور A — محرك المبيعات / Sales Engine

End-to-end pipeline. Each step → owning executor → existing module → autonomy class.

| Step | Executor | Module | Action class |
|------|----------|--------|--------------|
| 1 Intake | Lead Scout | `lead_inbox`, `api/routers/leads` | internal_state |
| 2 Enrich | Lead Scout | `customer_brain`, `data_os` | internal_compute |
| 3 Score (ICP) | Lead Scorer / ICP Qualifier | `sales_os/icp_score`, `intelligence/lead_scorer` | internal_compute |
| 4 Qualify + risk | ICP Qualifier | `sales_os/qualification`, `client_risk_score` | internal_compute |
| 5 Route to offer | Revenue Director | `leadops_spine/offer_router` | internal_state |
| 6 Draft message | Draft Writer | `leadops_spine/draft_builder`, `llm_gateway_v10` | internal_artifact |
| 7 Governance check | Policy Checker | `governance_os/policy_check`, `leadops_spine/compliance_gate` | — |
| 8 **Send** | Sequence Runner | `api/routers/outreach` | warm/cold send ← **dial** |
| 9 Track | Follow-up Agent | `EmailSendLog`, `leadops_reliability` | internal_state |
| 10 Follow-up sequence | Follow-up Agent | `core/queue/tasks` (scheduled) | warm send ← dial |
| 11 Reply / objection | Objection Responder | `objection` components, `sales_os` | internal_artifact + send |
| 12 Proposal | Closer / Proposer | `sales_os/proposal` | internal_artifact |
| 13 Close + invoice | Closer / Proposer | `finance_os`, `payment_ops`, `ZATCAInvoiceRecord` | financial_charge ← **dial** |
| 14 Payment capture | Closer / Proposer | `payment_ops` (Moyasar) | financial_charge ← **dial** |
| 15 → Delivery handoff | Revenue Director | hands to Delivery Director | internal_state |

This is "the strongest sales system": at the recommended config, steps 1–7, 9, 11–12 run at L5
(instant, autonomous); steps 8/10 warm sends at L5; cold sends + 13/14 charges at L4 (60-min
veto). The founder sees a daily digest, not a task list.

---

## 7. المحور B — الماكينة الداخلية / Internal Machine

The 7-day Revenue Intelligence Sprint, automated by the Delivery Director (mirrors the
`dealix-delivery` agent, now run-time):

| Day | Step | Executor | Module | Ledger write |
|-----|------|----------|--------|--------------|
| 1 | Source Passport | Source Passport Agent | `trust_os/source_passport` | consent_ledger |
| 2 | Data Quality score | DQ Scorer | `data_os` | — |
| 3 | Account scoring | Account Scorer | `sales_os`, `value_os` | value_ledger |
| 4 | Draft pack | Draft Writer | `delivery_factory`, `llm_gateway_v10` | — |
| 5 | Governance review | Governance Director | `governance_os`, `trust_os` | audit ledger |
| 6 | Proof Pack assembly | Proof Assembler | `proof_os/assemble` | proof ledger |
| 7 | Capital asset register | Capital Registrar | `capital_os/capital_ledger` | capital_ledger |
| 7 | Retainer eligibility | Delivery Director | `adoption_os` (retainer readiness) | — |

Plus continuous loops: **Governance review loop** (Governance Director re-checks every artifact),
**Friction loop** (`friction_log` aggregates every override/failure), and the **Self-Improvement
loop** (`self_evolving_os` + `weekly_self_improvement.py` — weekly, proposes config/prompt
tweaks; proposals themselves go through an approval dial).

---

## 8. المحور C — تشغيل الهرم / Hierarchy Runtime

- **Conductor loop:** scheduled cycles — morning plan, hourly execution sweeps, evening digest.
- **Scheduler:** `core/queue` (Celery already present) for v1; **Temporal** recommended once
  multi-day workflows (sprints, follow-up sequences) need durable timers. Decision in §13.
- **State:** `unified_operating_graph` as the shared operating picture; Postgres event store
  (`test_pg_event_store` exists) as the event bus between tiers.
- **Identity & budgets:** `agent_identity_access_os` issues identity cards; per-agent budgets
  enforced by `agent_governance`; telemetry to `agent_observability` + `observability_v10`.
- **Escalation:** anything an executor cannot resolve, or any anomaly, → Ops Director →
  founder digest / push.

---

## 9. المحور D — لوحة Full Ops / Ops Console

Extends the existing `/ops` pages — one new unified surface plus widgets.

**New page `/[locale]/ops/full`** — the founder cockpit:

| Panel | Content | Built from |
|-------|---------|-----------|
| Autonomy Dial | 8 sliders (L0–L5) per action class + kill switch | new `AutonomyDial` component (shadcn `slider`) |
| Live Agent Feed | streaming activity of every tier-2 agent | SSE/WebSocket → conductor event bus |
| Veto Queue | L4 actions inside their veto window — one-click veto | extends `components/approvals/ApprovalCenter` |
| Approval Queue | L2/L3 items | existing `ApprovalCenter` |
| Control Tower | daily/weekly/monthly scorecard | `business_metrics_board`, Recharts |
| Pipeline Funnel | lead→paid funnel, live | `OpsSalesPipeline` extended |
| Escalations / Alerts | anomalies, blocked risks, failures | `bottleneck_radar`, `friction_log` |
| Ledger Viewers | value / capital / consent / audit | read-only tables |

**Backend:** new router `api/routers/full_ops.py` — `GET /full-ops/state`,
`POST /full-ops/autonomy` (set dial), `POST /full-ops/veto/{action_id}`,
`POST /full-ops/kill-switch`, `GET /full-ops/feed` (SSE). Reuses axios client + admin API key
pattern in `frontend/src/lib/api.ts`. Bilingual via `next-intl` (new `opsFull` namespace), RTL ready.

---

## 10. البيانات والـ Ledgers / Data & Ledgers

```
 Lead ─▶ LeadRecord ─▶ LeadScoreRecord ─▶ DealRecord ─▶ PaymentRecord/ZATCAInvoiceRecord
   │           │              │               │                 │
   ▼           ▼              ▼               ▼                 ▼
 friction   consent_ledger  value_ledger   audit ledger     value_ledger
  _log     (PDPL basis)    (tier-disc.)  (every L4/L5 act) (client_confirmed)
                                              │
 every autonomous action ─────────────────────┘  +  ai_control_plane (LLM runs)
 every engagement close ─▶ proof ledger (Proof Pack)  +  capital_ledger (asset)
```

Rule: **no autonomous action exists without an audit-ledger row.** That row is what makes L5
safe-to-audit and CI-verifiable.

---

## 11. حزمة التقنية / Tech Stack

| Layer | Choice |
|-------|--------|
| Backend | FastAPI (existing), Python 3.11, the 72 OS modules |
| Orchestration | Conductor on `core/queue` (Celery) for v1 → migrate durable workflows to Temporal |
| Event bus | Postgres event store (existing `pg_event_store`) |
| LLM | `llm_gateway_v10` (model routing, budgets) |
| State graph | `unified_operating_graph` |
| Frontend | Next 15 App Router, shadcn/Radix, Tailwind, Recharts, `next-intl` (ar/en RTL) |
| Live feed | SSE (v1) → WebSocket if needed |
| Observability | `observability_v10`, `agent_observability`, Sentry |
| Config | `config/autonomy.yaml` (hot-reloaded by Conductor) |

---

## 12. خطة البناء على مراحل / Phased Build Plan

Each phase is bounded, ships behind config, and **keeps CI green**. A phase opens only on explicit
approval. Build-time sub-agents in brackets.

| Phase | Deliverable | Exit criterion |
|-------|-------------|----------------|
| **0** | This blueprint | Approved ✅ (you are here) |
| **1 — Autonomy spine** | `config/autonomy.yaml`, autonomy resolver, reclassify approval_engine to read the dial, rewrite the 2 affected CI tests to dial-aware form, audit-ledger row on every action [engineer] | Dial at L2 == today's behaviour; CI green |
| **2 — Conductor + 1 Director** | `OpsConductor` loop + Revenue Director + 3 executors (Lead Scout, Lead Scorer, Draft Writer) over `leadops_spine` [engineer] | Conductor runs a full cycle in dry-run; produces drafts |
| **3 — Sales Engine end-to-end** | remaining Revenue executors, steps 8–15; warm send at L4 [engineer, sales] | A lead flows intake→draft→queued→ (vetoable) send |
| **4 — Full Ops Console** | `/ops/full` page, `full_ops.py` router, autonomy dial UI, veto queue, live feed [engineer, content] | Founder can set dials + veto from UI |
| **5 — Internal Machine** | Delivery Director + 7-day sprint automation, proof pack + capital auto-register [engineer, delivery] | One sprint runs unattended end-to-end |
| **6 — Governance + Ops Directors** | policy/PII/audit executors, scorecard, anomaly detector, escalations, self-improvement loop [engineer] | Anomaly auto-drops dial; digest generates |
| **7 — Growth Director** | content, partner, affiliate, benchmark executors [engineer, content] | Content drafted + scheduled at L4 |
| **8 — Autonomy ramp** | move classes L2→L4→L5 as evidence accumulates; load/anomaly testing | Sustained L4/L5 operation, clean audit |

---

## 13. المخاطر والقرارات المفتوحة / Risks & Open Decisions

| # | Item | Recommendation |
|---|------|----------------|
| R1 | L5 charge/cold-send → Moyasar freeze, PDPL exposure | Stay L4 until hundreds of clean L4 actions; document in TRUST_LAYER |
| R2 | Pricing fork (empire vs `OFFER_LADDER_AND_PRICING.md`) feeds wrong numbers into autonomous proposals | Reconcile pricing **before** Phase 3 |
| R3 | Celery vs Temporal for durable multi-day workflows | Decide at Phase 5; Celery fine for 1–4 |
| R4 | 72 OS modules — overlap/dead code | Phase 1 includes a thin capability audit per director |
| R5 | Cost — autonomous LLM loops can run up spend | Per-agent budgets via `agent_governance` from Phase 2 |
| R6 | CI coverage gate ≥70% | Every phase ships tests; dial-aware tests replace, not delete, the old ones |

**Open decisions for you:** (a) confirm L4 defaults for charge + cold-contact, or override to L5;
(b) confirm reconciling the pricing fork before Phase 3; (c) approve starting Phase 1.

---

## 14. التحقق / Verification (per phase)

- Phase 1: `pytest tests/test_*autonomy* tests/governance/` green; dial at L2 reproduces current
  behaviour byte-for-byte; every action class produces an audit-ledger row.
- Phase 2+: conductor dry-run cycle logged end-to-end; each new executor has a contract test.
- Phase 3/5: a synthetic lead / synthetic sprint runs the full path with the dial at L4 and is
  visible + vetoable in the console.
- All phases: `ci.yml` gates pass (compile, alembic single-head, compliance tests, coverage ≥70%,
  service-readiness, SEO).

---

## روابط ذات صلة / Related

- [docs/empire/CURRENT_DIRECTION.md](../empire/CURRENT_DIRECTION.md) · [TRUST_LAYER.md](../empire/TRUST_LAYER.md) · [OFFER_LADDER.md](../empire/OFFER_LADDER.md)
- [docs/architecture/CORE_OS.md](CORE_OS.md) · [MODULAR_MONOLITH.md](MODULAR_MONOLITH.md) · [EVENT_MODEL.md](EVENT_MODEL.md)
- [docs/00_constitution/NON_NEGOTIABLES.md](../00_constitution/NON_NEGOTIABLES.md) · [DECISION_PRINCIPLES.md](../00_constitution/DECISION_PRINCIPLES.md)
- `auto_client_acquisition/trust_os/trust_pack.py` — the 11 non-negotiables (source of truth)
