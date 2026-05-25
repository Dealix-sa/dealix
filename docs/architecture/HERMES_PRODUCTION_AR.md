# Hermes — Dealix Production Architecture (Sovereign Value Control Plane)

> **Hermes** هو الـ control plane السيادي داخل Dealix. مهمته الوحيدة: تحويل
> الإشارات إلى تنفيذ محوكَم، نتائج قابلة للقياس، أصول قابلة لإعادة الاستخدام،
> ودخل حقيقي مُتحقَّق — تحت قاعدة واحدة: **لا فعل حساس بلا موافقة، لا دخل
> بلا تحقق، لا نتيجة بلا أصل، ولا توسع بلا بيانات.**

النسخة: `dealix/hermes/__init__.py` — `1.0.0`.

---

## 1) الطبقات الأربع

```
Dealix Platform
├── Control Plane         (dealix/hermes/control_plane)
│   ├── runtime           ← orchestrator واحد لكل request
│   ├── authorization     ← هل actor مسموح له؟
│   ├── policy_enforcement← policies-as-code (block/hold/pass)
│   ├── sovereignty_gate  ← S0..S5 classification
│   ├── trust_gate        ← overclaim / PII / injection / pricing band
│   ├── approval_gate     ← default-deny + TTL
│   ├── audit_gate        ← كل stage يكتب AuditEvent
│   └── kill_switch       ← agent / tool / workflow / mcp / workspace
│
├── Execution Plane       (dealix/hermes/execution)
│   ├── agent_runtime     ← AgentCard + model_fn injection
│   ├── workflow_runtime  ← WorkflowSpec → steps deterministic
│   ├── tool_gateway      ← لا tool يُستدعى مباشرة
│   ├── output_validator  ← schema-light validation
│   ├── task_queue        ← in-memory (يستبدل بـ Postgres لاحقًا)
│   └── run_state         ← live status للـ UI
│
├── Intelligence Plane    (dealix/hermes/intelligence_plane)
│   ├── signal_graph      ← signal → opportunity
│   ├── outcome_graph     ← execution → outcome (CTRL-OPS-001)
│   ├── revenue_graph     ← deal → verified revenue
│   ├── attribution_graph ← multi-touch (weights ∈ [0..1])
│   ├── asset_graph       ← templates / playbooks / evidence packs
│   ├── learning_engine   ← expand / kill / investigate
│   └── recommendations   ← Best Next Action
│
└── Product Plane         (dealix/product_plane)
    ├── sovereign_console ← founder cockpit (actions, risks, money)
    ├── internal_workspace
    ├── growth_workspace  ← Section 52 dashboard projections
    ├── trust_workspace   ← controls / kill / audit
    ├── customer_workspace
    └── partner_workspace
```

ودوائر داعمة بنفس المستوى:

```
dealix/hermes/products       ← Offer Registry + Readiness Gate
dealix/hermes/money          ← Revenue Events / Verification / Quality
dealix/hermes/growth         ← Campaigns / ICP / Funnel / Experiments
dealix/hermes/trust          ← AI Risk Controls library
dealix/hermes/security       ← Prompt injection / DLP / Sandbox / Red Team
dealix/hermes/partners       ← Fit scorer / Revenue share
dealix/hermes/workflows      ← Revenue Hunter / AI Trust Kit / Partner Pitch …
```

---

## 2) Runtime Flow الموحَّد

كل request يدخل عبر `HermesRuntime.run(context, intent, draft=None, signals=None, …)`
ويمر بـ pipeline ثابت:

```
ContextPacket
    → authorization_gate      (deny on miss)
    → policy_enforcement      (block / hold)
    → sovereignty_gate        (S5 → block, S2+ → hold)
    → kill_switch             (target killed → deny)
    → [execution plane تنتج draft]
    → trust_gate              (overclaim / PII / pricing / urls)
    → approval_gate           (open ticket if HOLD)
    → audit_gate              (every stage)
    → HermesResponse (Section 58 shape)
    → outcome_logger          (CTRL-OPS-001: required)
    → asset_builder           (إذا النتيجة قابلة لإعادة الاستخدام)
```

شكل الرد الموحّد (Section 58):

```json
{
  "success": true,
  "data": {...},
  "risk": {
    "risk_level": "medium",
    "sovereignty_level": "S2_SAMI_APPROVAL",
    "approval_required": true,
    "reasons": ["..."],
    "controls_triggered": ["external_action_policy"]
  },
  "next_actions": [{"action": "approve_or_reject", "ticket_id": "apr_..."}],
  "events_emitted": ["hermes.request.accepted", "hermes.approval.opened"]
}
```

---

## 3) Sovereignty Model — S0..S5

| Level | المعنى | متى |
|-------|--------|-----|
| `S0_INTERNAL_DRAFT`  | مسودة داخلية، تظهر في الـ UI فقط | الافتراضي لأي خارجي |
| `S1_INTERNAL_AUTO`   | فعل داخلي يمكن أتمتته | actor داخلي موثوق |
| `S2_SAMI_APPROVAL`   | يحتاج قرار المؤسس | كل خارجي / تسعير / mcp غير مراجَع |
| `S3_LEGAL_APPROVAL`  | يحتاج قانوني | عقود / بيانات منظَّمة |
| `S4_BOARD_APPROVAL`  | يحتاج مجلس | acquisition / spinout / equity |
| `S5_BLOCKED`         | مرفوض مطلقًا | bulk unverified send / scraping / credential exfiltrate |

التصنيف في `dealix/hermes/sovereignty.py:classify()` — مجموعات ثابتة:
`FOUNDER_ONLY_ACTIONS`, `LEGAL_ONLY_ACTIONS`, `BOARD_ONLY_ACTIONS`, `BLOCKED_ACTIONS`.

---

## 4) Trust Gate — ما يفحصه

- **Overclaim** عربي + إنجليزي (نضمن لك / the only / guaranteed / 100%).
- **Prompt-injection hints** (ignore previous instructions / تجاهل التعليمات).
- **PII**: Saudi ID (`[12]\d{9}`)، IBAN (`SA\d{22}`)، Credit Card.
- **Pricing band**: 499..250,000 ريال افتراضيًا.
- **URLs**: لا `localhost`/`127.0.0.1` في أي مخرج خارجي.

كل finding له `code`، `severity` (`low|medium|high|critical`)، و detail. أي
`high|critical` → الـ runtime يردّ `success=False` ولا يفتح approval — يطلب
إعادة صياغة المسودة أولًا.

---

## 5) AI Risk Controls (Section 55)

تسعة controls مدمجة في `dealix/hermes/trust/controls.py`:

| ID | Category | Severity |
|----|----------|----------|
| CTRL-GOV-001 | Agent must have owner | HIGH |
| CTRL-GOV-002 | Tool must have owner | HIGH |
| CTRL-GOV-003 | External action requires approval | HIGH |
| CTRL-SEC-001 | Sensitive data cannot leave workspace | CRITICAL |
| CTRL-SEC-002 | MCP server requires review | HIGH |
| CTRL-OPS-001 | Every execution requires outcome | MEDIUM |
| CTRL-OPS-002 | Incident requires remediation | HIGH |
| CTRL-TRANS-001 | External claim requires evidence | HIGH |
| CTRL-COM-001 | Enterprise pricing requires approval | HIGH |

كل control عبارة عن دالة `(ctx) -> ControlVerdict` قابلة للتفسير. الـ Trust
Workspace يعرض الـ failures مباشرة بدون تفسير LLM.

---

## 6) Offer Registry + Readiness Gate

10 offers افتراضية مسجَّلة في `dealix/hermes/products/offer_registry.py`:

```
revenue_hunter_pilot       2,499 – 9,999 ريال
ai_trust_kit               5,000 – 25,000 ريال
agency_white_label_kit     7,500 – 35,000 ريال
founder_os_setup           1,999 – 4,999 ريال
market_radar_report        4,999 – 14,999 ريال
proposal_factory_pack      3,499 – 12,999 ريال
mcp_risk_review            4,500 – 18,000 ريال
evidence_pack_generator    3,500 – 11,500 ريال
customer_value_report      2,999 – 8,999 ريال
executive_pmo_lite         4,999 – 16,999 ريال
```

لا offer يخرج للسوق قبل المرور على `ProductReadinessGate.assess(offer)`:

- `buyer / pain / promise / entry_cta / outcome_metric / proof_hypothesis`
  لازم مُعرَّفة (10 نقاط لكل واحد).
- `deliverables` غير فارغة.
- `price_min_sar > 0` و `price_min_sar <= price_max_sar`.
- `trust_risks` لازم تكون مذكورة بشكل صريح.
- `delivery_checklist` ≥ 2 عناصر.
- `upsell` لازم محدد (no offer without next-step revenue).

النتيجة dict جاهز للـ UI:

```json
{"offer_id":"...", "ready":false, "score":72, "missing":[...], "required_before_launch":[...]}
```

---

## 7) Money — Revenue Verification

أحداث الدخل لا تُعتبر `verified` إلا إذا مرّت بـ `RevenueVerifier`:

```python
VERIFICATION_KINDS = {
    payment_received,            # يتطلب payment_reference
    signed_agreement,            # يتطلب deal_id
    invoice_paid,                # يتطلب payment_reference
    retainer_started / renewed,  # متكرر
    partner_paid_customer,       # شريك
}
```

أي شيء آخر (proposal_sent, likes, views, verbal interest) **لا يُحسب دخلًا**.
الـ `RevenueQualityScorer` يصنف الجودة (recurring / margin / size / partner-influence).

---

## 8) Default Policies (Section 57)

سياسات runtime مسجَّلة في `dealix/hermes/control_plane/policy_enforcement.py`:

| Policy | Block | Reason |
|--------|-------|--------|
| `external_action_policy`        | no | يحوَّل لـ approval |
| `sensitive_data_policy`         | yes | regulated export blocked |
| `pricing_policy`                | no | يحوَّل لـ approval |
| `mcp_policy`                    | yes | unreviewed MCP blocked |
| `partner_claim_policy`          | yes | claim بلا evidence pack |
| `revenue_verification_policy`   | yes | revenue بلا payment/agreement |

---

## 9) Database — Migration Order

التطبيق على Postgres بنفس ترتيب Section 56، تحت `db/migrations/versions/`:

```
20260525_201_hermes_core.py
    hermes_signals, hermes_opportunities, hermes_decisions,
    hermes_executions, hermes_outcomes, hermes_assets, hermes_events

20260525_202_hermes_sovereignty_trust.py
    hermes_agents, hermes_tools, hermes_permissions, hermes_approvals,
    hermes_audit_events, hermes_risks, hermes_incidents, hermes_evidence_packs

20260525_203_hermes_growth_money.py
    hermes_growth_campaigns, hermes_growth_leads, hermes_growth_touches,
    hermes_growth_experiments, hermes_growth_attribution, hermes_revenue_events,
    hermes_deal_rooms, hermes_invoices

20260525_204_hermes_products_partners_customers.py
    hermes_offers, hermes_product_lines, hermes_partners,
    hermes_partner_revenue, hermes_customers, hermes_customer_health,
    hermes_value_reports

20260525_205_hermes_advanced.py
    hermes_mcp_servers, hermes_mcp_reviews, hermes_agent_runs,
    hermes_tool_calls, hermes_traces, hermes_cost_events
```

Seeds مرافقة:

```
db/seeds/agents_seed.py     ← 8 agents (Signal/Opportunity/Hunter/Proposal/Trust/Outcome/Asset/Attribution)
db/seeds/tools_seed.py      ← ~10 tools (lead_lookup, draft_only senders, …)
db/seeds/offers_seed.py     ← يعيد تصدير DEFAULT_OFFERS
db/seeds/policies_seed.py   ← 6 policies
db/seeds/controls_seed.py   ← 9 controls من ControlLibrary
db/seeds/icp_seed.py        ← 5 ICPs سعودية
```

---

## 10) API Surface

router واحد: `api/routers/hermes.py` تحت `/api/v1/hermes`:

| Method | Path | الوصف |
|--------|------|------|
| `POST` | `/run` | يدخل request كاملًا في الـ runtime |
| `GET`  | `/approvals` | قائمة الـ tickets المعلَّقة |
| `POST` | `/approvals/{ticket_id}/decide` | قرار approve/reject |
| `GET`  | `/trace/{request_id}` | audit trail كامل |
| `GET`  | `/offers` | كل العروض |
| `GET`  | `/offers/{offer_id}/readiness` | فحص جاهزية offer |
| `GET`  | `/controls/evaluate` | تقييم controls مع ctx من query |
| `POST` | `/kill-switch/{kind}/{target_id}/trip` | تعطيل |
| `POST` | `/kill-switch/{kind}/{target_id}/restore` | استعادة |
| `GET`  | `/kill-switch/active` | كل التعطيلات النشطة |

كل endpoint يُرجِع شكل Section 58 من خلال `HermesResponse.to_dict()`.

---

## 11) Security Defaults

- Draft-only by default — لا فعل خارجي بلا approval.
- No tool call without `ToolGateway` — أي `tool.call()` يمر بـ kill switch + permissions + audit.
- No unreviewed MCP — `mcp_policy` يحجب MCP server بدون sign-off.
- No public API by default — `/api/v1/hermes/*` خلف admin guard.
- No marketplace by default — يتطلب decision gate explicit.
- No sensitive data export — `sensitive_data_policy` يحجبه.
- No autonomous contracts — `S3_LEGAL_APPROVAL` إلزامي.
- No verified revenue without payment/agreement — `RevenueVerifier`.

---

## 12) Deployment Modes

| Mode | الجمهور | الحالة |
|------|---------|--------|
| Internal OS | Founder / فريق Dealix | **Alpha — يجب البدء هنا** |
| Assisted Service | عميل + delivery team | Beta |
| Customer Workspace | عميل يدخل بنفسه | بعد تثبيت TrustWorkspace |
| Partner Workspace | شريك يعيد البيع | بعد PartnerFit ≥ 60 |
| Enterprise Control Plane | شركة كبيرة | لاحقًا — يتطلب tenancy |
| API Platform | dev يبني فوقها | لاحقًا — يتطلب rate limit + auth |
| Marketplace | offers موحدة | آخر مرحلة |

---

## 13) Alpha Success Criteria (Section 66)

- 100 signals captured
- 30 opportunities scored
- 10 proposals drafted
- 5 calls booked
- 3 paid pilots (verified revenue)
- 20 outcomes logged
- 10 assets created
- 1 repeatable offer proven (case study)
- **0 unsafe external actions**

---

## 14) ما لا يجب بناؤه الآن (Section 64)

- Marketplace
- Public API
- Full autonomy
- External send automation
- Complex multi-tenant billing
- Large paid ads
- Too many verticals

ابدأ بـ: Kernel → Sovereignty → Trust → Growth Attribution → Revenue Assurance
→ Revenue Hunter → AI Trust Kit → Agency White-label Kit.

---

## 15) كيف تشغّل Hermes محليًا

```bash
# smoke test
python3 -c "
from dealix.hermes.control_plane import HermesRuntime
from dealix.hermes.contracts import Actor, ActorKind, ContextPacket, OutputKind
from dealix.hermes.control_plane.runtime import DraftBundle

rt = HermesRuntime()
ctx = ContextPacket(
    actor=Actor(actor_id='founder.sami', kind=ActorKind.FOUNDER),
    intent='external.send.email',
    declared_output_kind=OutputKind.MESSAGE,
)
outcome = rt.run(
    context=ctx,
    intent='external.send.email',
    draft=DraftBundle(text='عرض حقيقي خالٍ من الادعاءات.'),
)
print(outcome.response.to_dict())
# success=True, approval_required=True, ticket opened.
"

# tests
pytest tests/hermes/

# migrations
alembic upgrade head
```

---

## 16) الفرق بين Hermes والمنافس

| المنافس | Hermes |
|---------|--------|
| Chatbot | Sovereign Control Plane |
| Automation rules | Trust-Governed Agents |
| CRM plugin | Outcome Graph + Asset Library |
| AI sales assistant | Revenue Assurance + Partner Network |
| Generic governance | Saudi/Arabic-first Playbooks + PDPL-aware |

---

> الخلاصة:
>
> Hermes ليس وكيلًا ذكيًا آخر. هو الـ control plane الذي يحوّل وكلاء Dealix
> إلى منتج تجاري حقيقي تحت قاعدة واحدة: **لا فعل بلا حوكمة، ولا دخل بلا
> تحقق، ولا توسع بلا بيانات.**
