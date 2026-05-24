# Dealix — Comprehensive Holistic Build-Out Plan
# الخطة الشاملة الكاملة لبناء Dealix من الـA إلى الـZ

> Status: **FINAL — ready for execution (6-month compressed timeline, AI-first parallel mode)**
> Horizon: **180 days** (gates at Day 7 / 14 / 30 / 60 / 120 / 180)
> Execution mode: **All 12 AI tiers start Day 1 in parallel** · Trust Plane Postgres migration Day 1 · Hyperpay/Tap integrated parallel with Moyasar from Day 1 · Revenue + Compliance + Operations + Frontend tracks run in parallel against the same gates.
> Scope: **8 tracks × 12 AI tiers × full PDPL/NCA/ZATCA compliance × executive → ops cadence**
> Repo: `/home/user/dealix` · Branch: `claude/upbeat-rubin-bFV43`
> Production: `https://api.dealix.me` (Railway, deployed, Moyasar-blocked) · Landing: `https://voxc2.github.io/dealix/`

---

## 0. Context — لماذا هذه الخطة موجودة

Dealix is a Saudi-native B2B Revenue Engine positioned as a "sovereign, policy-governed Growth & Execution OS for Saudi enterprises." The repo is enterprise-scale (171 routers, 175+ OS modules, 524 test files, 110+ doc subdirs, 180+ landing pages, Next.js 15 frontend) and **technically launched** on Railway — but commercially **pre-revenue**, with Moyasar account activation as the single blocking gate.

This plan does **one thing**: close every gap (commercial + technical + AI + compliance + operational) between what Dealix claims and what Dealix is in production — and turn a launched-but-pre-revenue platform into a 1.5M SAR ARR Saudi enterprise AI company within 12 months, on the way to Series A.

It is **holistic, not partial**. Every layer — executive, commercial, technical, AI (12 tiers), compliance, operations, frontend, data — is named, scoped, sequenced, and gated. Every claim in `dealix/registers/no_overclaim.yaml` moves to **Production** by Day 365. Every AI tier is fully implemented. Every PDPL/NCA/ZATCA control is mapped and verified.

**Operating principles inherited (binding):**
1. **AI explores, analyzes, recommends. Deterministic workflows execute. Humans approve critical moves.** (constitution.md preamble)
2. **No agent makes an external commitment alone** (Article II).
3. **Every critical output is a validated `DecisionOutput` with A/R/S classifications and evidence** (Articles III–V).
4. **Trust Plane is non-bypassable.** Policy → Approval → Audit on every NextAction.
5. **The 8 hard gates** (NO_LIVE_SEND, NO_LIVE_CHARGE, NO_COLD_WHATSAPP, NO_LINKEDIN_AUTO, NO_SCRAPING, NO_FAKE_PROOF, NO_FAKE_REVENUE, NO_BLAST) are enforced in code, not policy.
6. **The 11 non-negotiables / doctrine_lock** (`docs/transformation/01_doctrine_lock.md`) are tested in CI.
7. **No-overclaim register is the source of truth.** CI blocks PRs that claim more than evidence supports.
8. **Bilingual-first (Arabic primary, RTL).** Translation is not localization.

---

## 1. Current-State Snapshot — أين نحن الآن

**Deployed (verified 2026-04-24):**
- `GET /healthz`, `/health`, `/docs`, `/api/v1/pricing/plans`, `/api/v1/public/demo-request`, `/api/v1/public/partner-application` — all **200 ✅**
- `POST /api/v1/checkout` — **502 🔴 `account_inactive_error`** (Moyasar)
- Railway: service `web`, Postgres auto-linked, env vars set (APP_SECRET_KEY, MOYASAR_*, CALENDLY_*, POSTHOG_*, HUBSPOT_*)
- Landing: 180+ static pages live on GitHub Pages with `window.DEALIX_API_BASE='https://api.dealix.me'`
- CI: gitleaks + bandit + trufflehog + detect-secrets all green
- Tests: 524 files / 3,854+ functions

**Inventory (high level):**
- **Backend:** 171 FastAPI routers across 11 domains (sales, customers, agents, compliance, analytics, webhooks, governance, trust, operations, data, platform)
- **Agent ecosystem:** 175+ modules under `auto_client_acquisition/` (76 `_os` directories), 15+ production Phase 8/9 agents under `auto_client_acquisition/agents/` and `autonomous_growth/agents/`
- **LLM stack:** 6 providers (Claude / Gemini / Groq / DeepSeek / GLM / OpenAI) with `core/llm/router.py::ModelRouter` + fallback chain + per-provider usage tracking + async thread-safe
- **Memory/RAG:** OpenAI `text-embedding-3-small` (1536d) via `core/memory/embedding_service.py` + `RevenueMemory` facade with Postgres-backed embedding records
- **Trust Plane:** `dealix/trust/{policy,approval,audit,tool_verification}.py` — all **Pilot / in-memory**, Postgres backend planned
- **Frontend:** Next.js 15 + TypeScript + Tailwind + shadcn/ui + next-intl, RTL-primary, routes `/[locale]/dashboard|pipeline|agents|approvals|clients|analytics|ops/founder|cloud|...`
- **Masters/Registers:** 7 master docs + 4 registers (no_overclaim, compliance_saudi, technology_radar, 90_day_execution)
- **Scripts:** 331 operational scripts (founder daily/weekly, CTO weekly, CEO one-session, official launch verify, etc.)
- **Pricing & checkout:** 6-tier ladder wired (Free Diagnostic / 499 SAR Sprint / 1,500 SAR Data Pack / 2,999–7,500 SAR/mo Retainer / Enterprise PMO), Moyasar gateway code verified functional

**`no_overclaim.yaml` snapshot (49 claims):**
- **Production (16):** multi-LLM routing, bilingual AR+EN, secret hygiene, Phase 8 intake/ICP/pain/qualification/pipeline, sectors (12), content (bilingual), LinkedIn-disabled-by-design, Docker production, CI security, observability structlog, service catalog (7 offerings), platform reference contracts
- **Pilot (5):** `policy_evaluator`, `approval_center`, `audit_log`, `tool_verification`, `phase8_crm` (all in-memory or token-blocked)
- **Partial (5):** `decision_output_contract`, `classifications_enforced`, `phase8_booking`, `pdpl_readiness`, `not_agent_executor`
- **Planned (2 named + many implicit):** `observability_otel`, `nca_alignment`

**AI layer gaps confirmed:**
- ❌ No LLM response caching
- ❌ No streaming outputs
- ❌ No per-customer cost quotas (per-agent budget only)
- ❌ No Jinja2 prompt templating / versioning / A/B testing
- ❌ No prompt-injection guardrail (test file exists, runtime guardrail does not)
- ❌ No PII redaction at LLM boundary (middleware scaffolded, not wired with Presidio/AraBERT)
- ❌ Langfuse not confirmed live (OTel scaffolded; gen_ai.* semantic conventions not emitted)
- ❌ No RLHF/DPO/fine-tuning loop
- ❌ No active learning from friction log
- ❌ Saudi dialect prompt library only ~8.7KB for 15+ agents
- ❌ No multi-modal (Gemini for docs, Whisper for voice)

**Blocked from revenue:**
- Moyasar account verification (KYC: CR, NID, IBAN, address)
- Sentry DSN not set
- UptimeRobot not configured
- First LinkedIn DM not sent

---

## 2. North-Star Metrics — ما الذي سنقيسه (6-month compressed)

| # | Metric | Day 7 | Day 14 | Day 30 | Day 60 | Day 120 | Day 180 |
|---|---|---|---|---|---|---|---|
| 1 | Paying customers | revenue path live | 1 | 5 | **10** (Series A trigger) | 30 | **60+** |
| 2 | ARR (SAR) | 0 | 7,500 | 50,000 | **250,000** | 750,000 | **1,500,000** |
| 3 | MRR retention | n/a | n/a | ≥ 90% | ≥ 95% | ≥ 95% | ≥ 95% |
| 4 | NPS (post-Proof-Pack) | n/a | captured | ≥ 30 | ≥ 40 | ≥ 50 | ≥ 60 |
| 5 | `no_overclaim` claims at Production | 16 | 18 | 22 | 27 | 35 | **49 (100%)** |
| 6 | AI tiers fully implemented (of 12) | 0 (all started in parallel) | 2 | 5 | 9 | 11 | **12** |
| 7 | LLM cost / customer / month (SAR) | tracked | tracked | < 80 | < 60 | < 50 | < 40 |
| 8 | Agent invocation p95 latency | < 12s | < 12s | < 10s | < 8s | < 6s | < 5s |
| 9 | Eval-harness mean score (/10) | baseline | baseline | > 7.5 | > 8.0 | > 8.5 | > 9.0 |
| 10 | PDPL DSAR response time | n/a | n/a | < 30 days | < 14 days | < 7 days | < 72h |
| 11 | Uptime SLO (rolling 30d) | 99.0% | 99.0% | 99.5% | 99.9% | 99.95% | 99.95% |
| 12 | Test count | 3,854 | 3,900 | 4,200 | 4,500 | 5,000 | 5,500+ |
| 13 | Payment processor coverage | Moyasar resubmit + Hyperpay scaffolded | Hyperpay live | Both live | Both + Tap | Multi-PSP load-balanced | Multi-PSP load-balanced |

---

## 3. The Plan Structure — كيف تُقرأ هذه الوثيقة

This plan is a **hybrid matrix**: 8 vertical tracks × 5 time-phased gates. Each track has its own depth; each gate synthesizes the tracks into a shippable state. Then:

- **§4** — The 8 tracks (Executive · Commercial · Platform/Trust · Execution/Workflows · AI Decision Plane · Compliance · Operations · Frontend/UX)
- **§5** — Time-phased milestones (Day 7 / 14 / 30 / 60 / 120 / 180) with explicit PASS gates
- **§6** — The 12 AI tiers fully detailed (Tier 1 → Tier 12)
- **§7** — Risk register (top 15) with mitigations
- **§8** — Decision gates (A → G) with PASS criteria + owner + evidence
- **§9** — Verification scripts per track
- **§10** — `no_overclaim.yaml` reconciliation table (every claim's path to Production)
- **§11** — Critical path dependencies
- **§12** — Appendix: critical files + cadence calendar

---

# §4. The 8 Tracks — التراكات الثمانية

---

## TRACK 1 — EXECUTIVE / المسار التنفيذي

**Mission:** Codify vision, OKRs, governance, fundraising trigger, and risk ownership so the company can scale beyond the founder.

**Why now:** Dealix is currently a founder-only company. Series A trigger fires at customer #10 (Day 90). Without OKRs, board cadence, and a hiring plan, scaling stalls at customer #5.

**12 Deliverables:**
1. **Annual OKRs register** — `dealix/registers/okrs_2026.yaml` (new) mirroring the schema of `dealix/registers/no_overclaim.yaml`. 4 company OKRs × 3 KRs each, quarterly review.
2. **Board charter + cadence calendar** — monthly observers, quarterly formal. Pack auto-generated via `auto_client_acquisition/board_ready_os/` + `auto_client_acquisition/board_decision_os/`.
3. **Series A trigger document** — "10 paying customers + 250K ARR + 12mo runway = data room opens." Source: `docs/business/INVESTOR_ONE_PAGER.md` (extend).
4. **Cap table model** — founders + option pool (15%) + Series A scenarios (10M / 15M / 20M SAR @ 50M-80M post). Spreadsheet + `dealix/registers/cap_table.yaml`.
5. **Executive decision passport register** — reuse `auto_client_acquisition/decision_passport/` for board-level decisions.
6. **Hiring plan v1** — sequenced against ARR gates: CTO co-founder (250K ARR / Day 90) → Head of Trust & Compliance (500K ARR / Day 150) → first SE (750K ARR / Day 180) → first AE (1M ARR / Day 240). New: `dealix/registers/hiring_plan.yaml`.
7. **Founder operating contract** — explicit time allocation: 50% sales, 25% product/AI, 15% trust/compliance, 10% capital. Reviewed weekly.
8. **CEO monthly review script** — new `scripts/ceo_monthly_review.py` aggregating ARR, funnel, NPS, compliance posture, costs from existing telemetry.
9. **Comp philosophy + first 10 hires comp bands** — KSA market data; equity + cash split.
10. **"What Dealix refuses" canonical doc** — maintain `docs/00_constitution/WHAT_DEALIX_REFUSES.md` (or create if absent). Refusal claims fed into Trust Plane.
11. **Investor narrative pack** — 4-pillar story: PDPL/ZATCA compliance moat · 6 OS tracks · Saudi-native bilingual · Founder-led GTM proof.
12. **Conflict-of-interest + ethics register** — founder personal-name no-fly list (PII), customer non-compete clauses.

**Files touched:**
- New: `dealix/registers/okrs_2026.yaml`, `board_cadence.yaml`, `hiring_plan.yaml`, `cap_table.yaml`
- Modify: `docs/00_constitution/DEALIX_CONSTITUTION.md`, `dealix/masters/constitution.md`
- Reuse: `auto_client_acquisition/board_decision_os/`, `board_ready_os/`, `executive_command_center/`, `founder_command_summary/`

**Sequencing:**
- Day 0–7: vision lock, OKRs Q2-2026, Series A trigger doc
- Day 14: cap table model
- Day 30: board cadence operational (first observer review)
- Day 90: first formal board meeting (Series A trigger fires)

**Success criteria:**
- Every track in this plan has a named owner + KPI in `okrs_2026.yaml`
- Founder weekly cadence ran 12 consecutive weeks with zero misses
- Board observer pack auto-generated from `executive_pack_v2/`
- Series A data room reaches "open" state by Day 90 if customer #10 closes

---

## TRACK 2 — COMMERCIAL / المسار التجاري

**Mission:** Go from 0 → 1 → 10 → 30 paying customers. Unblock Moyasar. Activate partner channel. Productize the 7-Day Revenue Intelligence Sprint at scale.

**Why now:** This is the only track that produces revenue. Everything else exists to enable it. Moyasar block is the single highest-impact open issue.

**15 Deliverables:**
1. **Multi-PSP revenue path (Day 1–14, blocking gate)** — Moyasar and Hyperpay run **in parallel from Day 1** (decision: hedge against PSP stall). Revenue is uncoupled from any single processor.
   - **Day 1–3:** Re-submit Moyasar KYC + scaffold Hyperpay integration spec in `dealix/payments/hyperpay.py` (new, mirrors `dealix/payments/moyasar.py` interface)
   - **Day 4–7:** Hyperpay sandbox integration + webhook → `POST /api/v1/webhooks/hyperpay` (new route)
   - **Day 8–14:** Hyperpay live keys + 1 SAR live charge end-to-end. **Hyperpay = primary by Day 14** unless Moyasar activates first.
   - **Day 14+:** Whichever activates first becomes primary; the other stays as fallback. Tap added as third option by Day 60.
   - **PSP router:** new `dealix/payments/psp_router.py` selects processor per (region, amount, customer preference). Webhook handlers normalize to common event schema.
2. **Customer #1 close (by Day 30)** — pick 1 of the 5 Day-1 leads from `docs/ops/pipeline_tracker.csv`:
   - عبدالله العسيري · Lucidya · CEO (surname affinity, primary target)
   - Ahmad Al-Zaini · Foodics · CEO ($170M Series C)
   - Nawaf Hariri · Salla · CEO (70K+ merchants)
   - Hisham Al-Falih · Lean Technologies · CEO (API-first B2B)
   - Ibrahim Manna · BRKZ · Founder ($30M debt contech)
   Run Free Diagnostic → 499 SAR Sprint → Proof Pack → close on 2,999 SAR/mo Retainer.
3. **First LinkedIn DM** — founder-personal channel, manual send (`NO_LINKEDIN_AUTO`); script in `docs/ops/launch_content_queue.md`. Update `docs/ops/pipeline_tracker.csv` row 1.
4. **3 WhatsApp templates** — A/B/C variants per persona (VP Sales / CEO / Distribution). Send-ready under `NO_COLD_WHATSAPP` doctrine: only after consent OR inbound trigger. Stored in `auto_client_acquisition/sales_os/templates/`.
5. **7-Day Revenue Intelligence Sprint** — productize as day-by-day deliverable contract:
   - D1 Source Passport · D2 DQ Score · D3 Account Scoring · D4 Draft Pack · D5 Governance Review · D6 Proof Pack · D7 Capital Asset + Retainer Eligibility
   - Reuse `auto_client_acquisition/delivery_os/`, `delivery_factory/`, `docs/27_delivery_playbooks/`, `docs/delivery/PROOF_PACK_TEMPLATE.md`
6. **Decision Passport + Proof Pack as packaged deliverables** — auto-built per customer via `auto_client_acquisition/decision_passport/builder.py` + `auto_client_acquisition/proof_ledger/pack_assembly.py` + HMAC-signed via `proof_ledger/hmac_signing.py`
7. **Pricing page revision** — `frontend/src/app/[locale]/services/`, `offer/`, `pricing/` aligned to 6-tier model + ZATCA VAT 15% display + Moyasar checkout
8. **Partner program v1** — 5-track model from `docs/business/AGENCY_PARTNER_REVENUE_MODEL.md`:
   - Referral (10% MRR/12mo) · Reseller (1K + 25% MRR) · Implementation (2.5K + 15% MRR/6mo) · White-Label · Pay-per-Result
   - Attribution in `auto_client_acquisition/partnership_os/` + `ecosystem_os/`
   - Day-1 partner queue: 2 marketing agencies + 5 SaaS founders (seed CSV at `docs/commercial/operations/targeting/agency_accounts_seed.csv`)
9. **Calendly deep-link integration** — close `phase8_booking` Partial. End-to-end test in `auto_client_acquisition/agents/booking.py` + webhook at `POST /api/v1/webhooks/calendly`.
10. **Vertical playbooks finalized** — 4 active verticals:
    - Real Estate (8 active companies, P50 7.4% reply, 3.2× demo lift)
    - Clinics (6 active, P50 13.8% reply, 40% no-show reduction)
    - Logistics (6 active, P50 6.8% reply, <60s response)
    - Hospitality (10 active, P50 12.4% reply, +30% MICE revenue)
    Reuse `auto_client_acquisition/vertical_playbooks/`, `vertical_os/`, `revenue_graph/sector_playbooks.py`
11. **Pipeline dashboard wired to live data** — `auto_client_acquisition/revenue_pipeline/`, `revenue_os/`. Frontend at `/[locale]/pipeline`.
12. **Customer health + churn register** — per-customer score via `auto_client_acquisition/customer_success/`, `customer_success_scores/`. Surfaced in `/[locale]/clients`.
13. **NPS + Voice-of-Customer loop** — captured at Proof-Pack delivery and at month 3. Fed into `auto_client_acquisition/friction_log/` aggregator.
14. **Case study engine** — activates post-customer-#3 via `auto_client_acquisition/case_study_engine/`. Bilingual outputs (AR+EN) auto-drafted, founder-approved before publish.
15. **1.5M SAR ARR customer-mix model** — target by Day 365:
    - 10× Executive Command Center @ 7,500 SAR/mo = 900,000 SAR/yr
    - 30× Growth OS @ 2,999 SAR/mo = 1,079,640 SAR/yr
    - 50× one-shot 499 SAR Sprint = 24,950 SAR
    - 10× Data Pack @ 1,500 SAR = 15,000 SAR
    - Total ≈ **2.02M SAR/yr** (35% buffer over 1.5M target)

**Files touched:**
- `dealix/payments/moyasar.py`, new `dealix/payments/hyperpay.py`, new `dealix/payments/tap.py`, new `dealix/payments/psp_router.py`
- `dealix/payments/{checkout_intent,orchestrator,renewal_scheduler,refund_state_machine,reconciliation}.py`
- `api/routers/{pricing,payment_ops,customer_webhooks,checkout}.py` + new `api/routers/hyperpay_webhooks.py`, `tap_webhooks.py`
- `auto_client_acquisition/service_catalog/registry.py` (already Production — keep stable)
- `frontend/src/app/[locale]/{offer,services,pricing,partners,clients,pipeline}/`
- `docs/ops/pipeline_tracker.csv`, `docs/ops/launch_content_queue.md`

**Sequencing (6-month compressed):**
- Day 1–3: Moyasar resubmission + Hyperpay integration scaffolded
- Day 4: First DM sent (Lucidya · Abdullah)
- Day 7: Live charge via Hyperpay or Moyasar — **whichever activates first** (Gate A)
- Day 14: Customer #1 closed (Gate B compressed from Day 30)
- Day 30: 5 customers
- Day 60: **10 customers · 250K ARR · Series A trigger** (Gate D compressed from Day 90)
- Day 120: 30 customers
- Day 180: **1.5M SAR ARR · Series A closed (Gate G compressed from Day 365)**

**Success criteria:**
- Live Moyasar charge succeeds end-to-end
- First Proof Pack delivered + NPS captured
- Cohort funnel measured: 100 outbound → 30 demos → 10 diagnostics → 3 paying
- Partner program produces ≥ 3 referred customers by Day 180

---

## TRACK 3 — PLATFORM / TRUST PLANE / منصة الثقة

**Mission:** Move Trust Plane from in-memory Pilot to Postgres-backed Production. Add OPA/Rego, per-tenant policies, OpenTelemetry gen_ai semantics, Sentry, UptimeRobot, BOPLA redaction. Close every Pilot/Partial claim in `no_overclaim.yaml`.

**Why now:** The Trust Plane is the defensible moat. Without Postgres persistence, audit log loses data on restart — unacceptable for PDPL S3 data. Without OPA, per-tenant policies cannot scale. Without OTel, observability claims are unsupported.

**14 Deliverables:**
1. **Postgres-backed audit log** — replace in-memory sink in `dealix/trust/audit.py`. Schema modeled on `dealix/contracts/audit_log.py::AuditEvent`. New migration in `migrations/versions/` (follow naming `20260601_xxx_audit_log_pg.py`). Closes `audit_log` Pilot.
2. **Postgres-backed approval store** — replace in-memory in `dealix/trust/approval.py`. Reuse existing reference implementation at `auto_client_acquisition/approval_center/approval_store.py`. Closes `approval_center` Pilot.
3. **Postgres-backed tool verification ledger** — `dealix/trust/tool_verification.py` → DB-backed. Schema: `(call_id, agent_id, trace_id, tool_name, intended_action, actual_action, inputs_hash, outputs_hash, side_effects, status, ts)`. Closes `tool_verification` Pilot.
4. **Unified event store** — reuse `auto_client_acquisition/proof_ledger/pg_event_store.py` (already exists!) as the substrate for policy/approval/audit/verification events. Single source of truth.
5. **OPA/Rego policy engine** — keep `dealix/trust/policy.py` as facade; add Rego policy files under new `dealix/trust/policies/*.rego`; deploy OPA sidecar via Docker; HTTP call from policy facade. Closes `policy_evaluator` Pilot.
6. **Per-tenant policy resolution** — tenant-keyed policy bundle loaded by `policy.py`. Reuse `auto_client_acquisition/platform_v10/tenant_contract.py`. Enables enterprise sales (Tier-1 must answer "can I have my own approval matrix?" with yes).
7. **OpenTelemetry SDK** — instrument `api/main.py`, `api/middleware/`, every LLM call in `core/llm/router.py`. Use `dealix/observability/otel.py` as base. Emit `gen_ai.request.model`, `gen_ai.system`, `gen_ai.usage.input_tokens`, `gen_ai.usage.output_tokens`, `gen_ai.usage.cached_tokens` on every LLM span. Closes `observability_otel` Planned.
8. **Sentry DSN configured** — `dealix/observability/sentry.py` already wired (file exists); set `SENTRY_DSN` env var; smoke test by triggering `/api/v1/_test_sentry` (new endpoint, dev-only).
9. **UptimeRobot monitors** — 5-minute interval on `/healthz`, `/health`, `/docs`, `/api/v1/pricing/plans`. SMS + email alerts to founder.
10. **DecisionOutput contract on every agent** — enforce `dealix/contracts/decision.py` return type in:
    - All `auto_client_acquisition/agents/*.py` (intake, icp_matcher, pain_extractor, qualification, booking, crm, proposal, outreach, followup, prospector, rules_router)
    - All `autonomous_growth/agents/*.py` (sector_intel, content, distribution, enrichment, competitor, market_research)
    CI gate: grep + AST check fails PR if any agent class missing `-> DecisionOutput` annotation. Closes `decision_output_contract` Partial.
11. **Classification enforcement in pipeline wrappers** — every step in `auto_client_acquisition/pipeline.py` reads `dealix/classifications/ACTION_CLASSIFICATIONS` for the NextAction's action_type before execution. Refuse if absent. Closes `classifications_enforced` Partial.
12. **Tool guardrail gateway live** — route every LLM tool call through `auto_client_acquisition/tool_guardrail_gateway/` (already scaffolded: `tool_guardrails.py`, `input_guardrails.py`, `output_guardrails.py`, `cost_budget.py`). Closes `not_agent_executor` Partial.
13. **Connector facade enforcement** — no agent talks to HubSpot/Calendly/Moyasar/SMTP directly. All sensitive tools routed through `auto_client_acquisition/connectors/` + `dealix/connectors/`. CI test asserts.
14. **Trust Pack assembly** — nightly cron at 03:00 KSA assembles per-tenant compliance + audit + decision + evidence + tool-verification into single HMAC-signed pack. Reuse `auto_client_acquisition/proof_ledger/pack_assembly.py`, `hmac_signing.py`, `auto_client_acquisition/{responsible_ai_os,trust_os}/trust_pack.py`.

**Files touched:**
- `dealix/trust/{audit,approval,policy,tool_verification}.py` (rewrite to use Postgres event store)
- `api/main.py`, `api/middleware/http_stack.py` (OTel instrumentation)
- `core/llm/router.py` (LLM span emission)
- 5+ new migrations: `migrations/versions/20260601_*.py`
- New: `dealix/trust/policies/*.rego`, `docker-compose.opa.yml`, `temporal/` (Track 4 prereq)

**Sequencing:**
- Day 7: Sentry + UptimeRobot live (Gate A)
- Day 30: DecisionOutput on every agent + classification enforcement (Gate B)
- Day 60: Postgres audit/approval/tool-verification (Gate C)
- Day 90: OPA/Rego + per-tenant policies + OTel gen_ai semantics (Gate D)
- Day 180: Trust Pack nightly cron, full coverage

**Success criteria:**
- All 5 Pilot claims (policy_evaluator, approval_center, audit_log, tool_verification, classification-enforcement-in-pipeline) → Production
- No in-memory Trust Plane components remain
- Every LLM call emits `gen_ai.*` OTel attributes
- Trust Pack generated for every active tenant nightly

---

## TRACK 4 — EXECUTION / WORKFLOWS / مستوى التنفيذ الدائم

**Mission:** Replace ad-hoc async Python orchestration with durable, replayable workflows. Temporal MVP. Workflow runs ledger. Safe-send gateway as the universal egress chokepoint.

**Why now:** Phase 8 pipeline runs in-process; if a worker dies mid-pipeline, state is lost. For enterprise customers, "we lost your lead" is fatal. Temporal gives replay-from-history and durable timers.

**10 Deliverables:**
1. **Temporal MVP** — self-hosted Temporal server via Docker (or Temporal Cloud for prod). Worker registry in `auto_client_acquisition/orchestrator/runtime.py` (file exists; `durable_workflow.py` is the placeholder).
2. **Phase 8 pipeline → Temporal workflow** — `auto_client_acquisition/pipeline.py` migrated: intake → ICP → pain → qualification → booking become activities. Workflow ID = lead's `dedup_hash`.
3. **Approval gate as Temporal signal** — A1+ actions block on signal from `dealix/trust/approval.py`. Workflow sleeps until signal received or TTL expires.
4. **Workflow runs ledger** — persisted via existing migration `migrations/versions/20260515_102_workflow_runs.py`. Surfaced in `/[locale]/ops/war-room`.
5. **Replay capability** — any workflow replayable from event history. Critical for debugging customer-reported issues.
6. **Channel policy gateway at workflow activity boundary** — `auto_client_acquisition/channel_policy_gateway/` enforces NO_LIVE_SEND, NO_COLD_WHATSAPP, NO_LINKEDIN_AUTO at the moment of send. Every outbound activity calls this gateway first.
7. **Safe-send gateway** — `auto_client_acquisition/safe_send_gateway/action_policy.py` is the universal egress chokepoint. Every workflow that sends external messages must call this. Combines: classification check + policy decision + approval check + rate limit + doctrine_lock check.
8. **Refund + reconciliation state machine** — durable via `dealix/payments/{orchestrator,refund_state_machine,reconciliation}.py` (already exist). Wire to Temporal so refunds survive process crash.
9. **Renewal scheduler as Temporal cron** — `dealix/payments/renewal_scheduler.py`. Customers on monthly retainer get auto-invoice 7 days before period end.
10. **Workflow control registry as policy source** — `auto_client_acquisition/governance_os/workflow_control_registry.py` + `governance_workflow_inventory.yaml`. Single source of truth for "what workflows exist, what classifications, what approvals."

**Files touched:**
- `auto_client_acquisition/orchestrator/{runtime,durable_workflow,queue,tools}.py`
- `auto_client_acquisition/pipeline.py`
- `auto_client_acquisition/safe_send_gateway/action_policy.py`
- New: `temporal/workflows/`, `temporal/activities/`, `docker-compose.temporal.yml`, `scripts/temporal_health.py`

**Sequencing:**
- Day 60: Temporal MVP local + docker-compose
- Day 90: Phase 8 pipeline migrated (Gate D)
- Day 180: Full workflow coverage (payments, renewals, outreach, follow-ups)

**Success criteria:**
- Pipeline runs are replayable from event history
- Approval rejection cleanly aborts workflow with full audit trail
- Zero outbound sends bypass safe_send_gateway (CI test asserts)
- Temporal `workflow_runs` ledger entries match audit log entries 1:1

---

## TRACK 5 — AI / DECISION PLANE / مستوى الذكاء الاصطناعي

**Mission:** Implement all 12 AI tiers fully. Move from "agents exist" to "agents are typed, evaluated, governed, observed, self-improving, cost-controlled, bilingual-rich, multi-modal."

**Why now:** Dealix's commercial wedge is "Saudi-native AI with governance." If the AI layer is shallower than competitors, the moat collapses. The 12 tiers in §6 close the gap between "scaffolded" and "Tier-1 enterprise-grade."

**Top-level deliverables (12, expanded in §6):**
1. LLM router hardening — caching · streaming · per-customer quotas · latency tracking · provider rate limits
2. Agent maturity — Pydantic I/O everywhere · `DecisionOutput` on every agent · auto-built Evidence Pack
3. RAG production — pgvector required · semantic + episodic + working memory · per-tenant isolation · knowledge graph
4. Eval harness — LLM-as-judge · regression suites · golden sets · CI gate · bilingual rubrics
5. Guardrails — PII redaction (Presidio + AraBERT) · prompt injection detection · refusal handling · off-topic
6. Bilingual depth — Khaleeji Arabic for all 15+ agents · dialect-aware routing · Arabic QA & style validators
7. Tool-use loop — auto-emission to verification ledger · structured tool registry · native Anthropic tool use
8. Agentic orchestration — LangGraph for branching · Temporal for durability · replay
9. Cost controls — per-tenant budgets · per-day quotas · provider rate limits · cost anomaly alerting
10. Self-improvement — friction log → prompt A/B → eval feedback → versioned prompt update
11. Observability — Langfuse live · OTel gen_ai.* · trace UI · cost dashboard · eval dashboard
12. Multi-modal — Gemini for document understanding · Whisper/Gemini-audio for sales calls

**Files touched:** see full inventory in §6.

**Sequencing (AI-first parallel mode, decision locked):** **All 12 tiers begin Day 1** and run in parallel. Engineering effort distributed across tiers per available capacity. Verification gates:
- **Day 14:** Tier 1 (caching + streaming) + Tier 2 (DecisionOutput everywhere) **must PASS**
- **Day 30:** + Tier 3 (pgvector RAG) + Tier 4 (eval harness in CI) + Tier 5 (guardrails) **must PASS**
- **Day 60:** + Tier 6 (bilingual depth) + Tier 7 (tool-use loop with ledger auto-emit) + Tier 11 (Langfuse + OTel live) **must PASS**
- **Day 120:** + Tier 8 (LangGraph + Temporal) + Tier 9 (cost controls) **must PASS**
- **Day 180:** + Tier 10 (self-improvement loop) + Tier 12 (multi-modal docs + voice) **must PASS** — all 12 tiers verified.

Each tier has an explicit owner; AI Lead (founder or first CTO hire) tracks tier-level burn-down weekly. Tier work happens in parallel with Tracks 2 (revenue), 3 (Trust Plane), 6 (compliance) — they are not sequenced.

---

## TRACK 6 — COMPLIANCE / PDPL + NCA + ZATCA

**Mission:** Move PDPL from "designed for" (Partial) to operationally proven (Production). Complete NCA control mapping (Planned → Production). Automate ZATCA Phase 2 certificate lifecycle.

**Why now:** Compliance is the moat. PDPL violation is catastrophic (regulatory + reputational). NCA mapping is required for enterprise sales. ZATCA cert expiry can break invoicing.

**16 Deliverables:**
1. **ROPA (Record of Processing Activities)** — populated via `auto_client_acquisition/compliance_os/ropa.py` (file exists). Output: `dealix/registers/ropa.yaml` (new). Required by PDPL Art. 7.
2. **Lawful basis register** — per processing activity. Reuse `auto_client_acquisition/governance_os/lawful_basis.py` (file exists). PDPL Art. 5 maps every operation to legitimate basis.
3. **Consent ledger** — per-data-subject capture, expiry, withdrawal via `auto_client_acquisition/compliance_os/consent_ledger.py` + `consent_signature.py`. PDPL Art. 6.
4. **DSAR (Data Subject Access Request) endpoints** — `/api/v1/privacy/data-subject-request`, `/api/v1/privacy/my-data` (new). Operations: access · rectification · erasure · portability. Reuse `auto_client_acquisition/compliance_os/data_subject_requests.py` (file exists). Wire to new `api/routers/dsar.py`. PDPL Art. 18/21.
5. **Retention enforcement in DB** — cron per table reads retention schedule from `dealix/registers/compliance_saudi.yaml`, executes deletion or anonymization. Reuse `auto_client_acquisition/proof_ledger/retention.py`.
6. **72-hour breach response runbook** — new `docs/25_compliance_trust/BREACH_RUNBOOK.md` with: detection → triage → containment → SDAIA 72h notification → customer notification → root cause → remediation → post-incident review. On-call rotation. Quarterly drill. Closes `pdpl_readiness` Partial.
7. **DPO appointment + register** — name, contact, escalation path, training cert. New `dealix/registers/dpo_appointment.yaml`. Triggered when: public entity onboarded OR core processing scaled OR S3 data at scale.
8. **SDAIA registration** — formal filing to Saudi Data & AI Authority. Required if Dealix becomes data controller for public-entity data.
9. **DPIA (Data Protection Impact Assessments)** — per high-risk processing: ICP scoring, pain extraction, sector intel, multi-modal document understanding. Template at new `docs/25_compliance_trust/DPIA_TEMPLATE.md`.
10. **NCA ECC 2-2024 control-by-control mapping** — complete table in `dealix/registers/compliance_saudi.yaml` for all 114 controls. Closes `nca_alignment` Planned.
11. **NCA DCC-1:2022 + CCC 2:2024 mappings** — Data Cybersecurity Controls + Cloud Cybersecurity Controls. Required for enterprise + government sales.
12. **ZATCA Phase 2 cert rotation** — automated 12-month renewal cron in `integrations/zatca.py`. Alert 30 days before expiry. Verify in proposal/invoice flow.
13. **Vendor risk register (sub-processors)** — reuse `auto_client_acquisition/compliance_os/vendor_registry.py`. Track: OpenAI, Anthropic, Google, Groq, DeepSeek, GLM, HubSpot, Calendly, Railway, Moyasar.
14. **Cross-border data transfer register** — PDPL Art. 29. Document which providers see Saudi data and what mitigations apply (no S3 data sent to non-KSA LLMs by default).
15. **PII redaction middleware live in production** — reuse `api/middleware/bopla_redaction.py` (file exists). Extend with Presidio (English) + AraBERT NER (Arabic) for: names, NIDs, IBANs, KSA phone formats, addresses, dates of birth.
16. **Compliance dashboard per tenant** — via `auto_client_acquisition/compliance_os/` + `trust_os/compliance_report.py`. Surfaced in `/[locale]/ops/evidence` + `/[locale]/customer-portal/compliance`.

**Files touched:**
- `dealix/registers/compliance_saudi.yaml` (expand to full NCA mapping)
- New: `dealix/registers/{ropa,dpo_appointment,vendor_registry,cross_border_transfers}.yaml`
- `auto_client_acquisition/compliance_os/*` (fill in scaffolded implementations)
- `api/routers/{compliance_product,compliance_status}.py` + new `api/routers/dsar.py`
- `api/middleware/bopla_redaction.py` (extend with Presidio + AraBERT)
- `integrations/zatca.py` (cert rotation cron)
- New: `docs/25_compliance_trust/{BREACH_RUNBOOK,DPIA_TEMPLATE,DPO_CHARTER}.md`

**Sequencing:**
- Day 30: Breach runbook published + on-call rotation defined
- Day 45: DPO appointed
- Day 60: DSAR endpoints live + ROPA + lawful basis populated
- Day 90: Retention enforced + full NCA mapping (Gate D)
- Day 120: SDAIA submission filed
- Day 180: ZATCA cert rotation automated (Gate F)

**Success criteria:**
- `pdpl_readiness` → Production
- `nca_alignment` → Production
- DSAR endpoints respond within 30 days (target 72h by Day 365)
- Breach drill executed quarterly with timer met
- ZATCA cert never expires unexpectedly

---

## TRACK 7 — OPERATIONS / العمليات اليومية والأسبوعية

**Mission:** Daily/weekly/monthly/quarterly cadence runs without founder firefighting. Observability + incident response + 331-script ecosystem cleaned up.

**Why now:** Founder time is the bottleneck. Every script that exists must run on a schedule with a named owner, or it doesn't exist.

**12 Deliverables:**
1. **Founder daily brief automated** — `scripts/dealix_founder_daily_brief.py` (exists) runs at 07:00 KSA via cron, delivers to email + WhatsApp (founder personal).
2. **CTO weekly tech watch** — `scripts/daily_tech_watch.sh` (exists) runs Mondays 08:00 KSA. Output: platform KPI snapshot + commercial registry status + dependency drift.
3. **CEO monthly review** — new `scripts/ceo_monthly_review.py` aggregates ARR, funnel, NPS, compliance posture, costs from existing telemetry. Runs 1st of month.
4. **Board quarterly pack** — `scripts/dealix_board_pack.py` (verify or build) auto-generates from `auto_client_acquisition/board_ready_os/` + `executive_pack_v2/`. Runs first Sunday of quarter.
5. **Incident runbook adoption** — `dealix/masters/incident_rollback_runbook.md` (exists) → run quarterly drill. Document outcome in `dealix/registers/incident_drills.yaml` (new).
6. **Release readiness checklist gate** — `dealix/masters/release_readiness_checklist.md` (exists) enforced via CI. Every release tag must pass.
7. **Bottleneck radar live** — `auto_client_acquisition/bottleneck_radar/`, `scripts/dealix_bottleneck_radar.py`. Surfaces top-3 blockers daily.
8. **On-call rotation v1** — founder solo Day 0 → +1 (CTO co-founder) Day 90 → +2 Day 180. PagerDuty or simple SMS escalation via UptimeRobot.
9. **Cost dashboards** — LLM (per provider, per tenant, per agent) + infra (Railway, Postgres, Redis) + Moyasar fees + outbound (HubSpot/Calendly). Via `dealix/observability/cost_tracker.py` + `api/routers/cost_tracking.py`. Surface in `/[locale]/ops/founder`.
10. **Runbook catalog** — every script in `/scripts` (331 currently) has purpose + owner + frequency documented. Dedupe to canonical 30–50. New `docs/ops/SCRIPT_CATALOG.md`.
11. **War Room operational** — `frontend/src/app/[locale]/ops/war-room/`. Surfaces: live pipeline · approvals queue · safe-send queue · cost burn · uptime · friction-log digest.
12. **Customer onboarding wizard hardened** — `scripts/dealix_customer_onboarding_wizard.py` (verify). End-to-end: contract signed → portal account → kickoff scheduled → Source Passport drafted.

**Files touched:**
- `scripts/*` (inventory + dedupe; output `docs/ops/SCRIPT_CATALOG.md`)
- New: `scripts/ceo_monthly_review.py`
- `dealix/masters/release_readiness_checklist.md` (extend with CI enforcement)
- `frontend/src/app/[locale]/ops/`
- `.github/workflows/` (add scheduled workflows for daily/weekly/monthly/quarterly scripts)

**Sequencing:**
- Day 1: founder daily brief live
- Day 7: CTO weekly tech watch live + UptimeRobot configured
- Day 30: CEO monthly review live + incident runbook drilled
- Day 60: cost dashboards live
- Day 90: quarterly board pack auto-generated
- Day 180: on-call rotation v2 with CTO

**Success criteria:**
- Zero missed cadence in any 90-day window
- Incident drill completed quarterly
- Cost dashboard < 5% drift from actual billing
- Script catalog has <50 canonical scripts (down from 331)

---

## TRACK 8 — FRONTEND / UX / واجهة المستخدم

**Mission:** Customer-facing surfaces + founder cockpit + war room + executive room, all RTL-first, bilingual, accessible (WCAG 2.1 AA), performant.

**Why now:** Frontend is the trust-builder for first impression. A clunky Arabic UX kills enterprise sales in KSA.

**12 Deliverables:**
1. **Pricing page locked to 6-tier model** — `frontend/src/app/[locale]/services/`, `offer/`. Moyasar checkout button live + VAT 15% transparent.
2. **Customer portal hardened** — `frontend/src/app/[locale]/customer-portal/`. Sections: Proof Pack viewer · invoices · compliance · approvals.
3. **Founder cockpit (90-min daily)** — `frontend/src/app/[locale]/dashboard/`, `business-now/`, `ops/founder/`. Wires to `business_now` snapshot + war-room today-pack.
4. **Approvals UI live** — `frontend/src/app/[locale]/approvals/`. Reads from Postgres approval store (Track 3 dependency). Approver actions logged in audit.
5. **Diagnostic intake flow** — `frontend/src/app/[locale]/dealix-diagnostic/`. Public, no-auth, with Calendly deep-link on completion.
6. **Proof Pack viewer** — `frontend/src/app/[locale]/proof-pack/`. Renders 10-section memo + evidence appendix with source citations.
7. **Trust Check public page** — `frontend/src/app/[locale]/trust-check/`. Shows: PDPL posture, ZATCA cert state, NCA mapping summary, sub-processor list. Enterprise sales asset.
8. **Risk score view** — `frontend/src/app/[locale]/risk-score/`. Customer-facing risk dashboard.
9. **Partner portal** — `frontend/src/app/[locale]/partners/`. Application form + tracker + commission view + co-branded assets.
10. **Pipeline view** — `frontend/src/app/[locale]/pipeline/`. Kanban over live data with policy + approval state per card.
11. **Landing parity** — reconcile 180+ static HTML pages in `landing/` (GitHub Pages) with Next.js routes. Decide canonical: Next.js for app, static for SEO-anchored marketing.
12. **Accessibility audit** — WCAG 2.1 AA. Arabic screen reader (Narrator/JAWS Arabic), keyboard nav, color contrast. Lighthouse score ≥ 95 on all flagship pages. Use `lighthouserc.js` (exists) + new `.pa11yrc.json` checks.

**Files touched:**
- All `frontend/src/app/[locale]/*` directories listed above
- `frontend/messages/{ar,en}.json` (i18n strings)
- `frontend/src/i18n/`
- `lighthouserc.js`, `.pa11yrc.json` (extend)

**Sequencing:**
- Day 30: Pricing + portal + dashboard live
- Day 60: Approvals UI + Diagnostic flow
- Day 90: Proof Pack viewer + Trust Check page
- Day 180: Accessibility audit pass (WCAG 2.1 AA)

**Success criteria:**
- All flagship surfaces RTL-correct (manual + automated test)
- Lighthouse ≥ 95 on `/`, `/ar`, `/ar/pricing`, `/ar/dealix-diagnostic`
- Customer can self-serve: diagnostic → checkout → Proof Pack delivery without founder touch
- WCAG 2.1 AA verified by external audit

---

# §5. Time-Phased Milestones — البوابات الزمنية (6-month compressed)

Every gate must PASS before proceeding to the next. **All 8 tracks and all 12 AI tiers run in parallel from Day 1**; gates synthesize the cross-track state.

---

## DAY 7 — "Revenue path live (multi-PSP), Trust Plane migration started, all 12 AI tiers scaffolded"

**Gates:**
- G7.1 — **First live charge succeeds** via Moyasar OR Hyperpay (whichever activates first — both running in parallel)
- G7.2 — **Sentry capturing errors** in production (`/api/v1/_test_sentry` triggers a Sentry issue)
- G7.3 — **UptimeRobot green** on `/healthz`, `/health`, `/docs`, `/api/v1/pricing/plans`
- G7.4 — **First LinkedIn DM sent** (Lucidya · Abdullah, founder-personal, manual; `pipeline_tracker.csv` row 1 updated with `sent_at`)
- G7.5 — **Founder daily brief running** for 7 consecutive days
- G7.6 — **Trust Plane Postgres migrations merged** (audit log + approval store + tool verification ledger schemas live; in-memory sinks replaced with writes-through to Postgres)
- G7.7 — **All 12 AI tiers scaffolded** — each tier has an owner, file paths, and Day-14 milestone declared in `dealix/registers/ai_tier_burndown.yaml` (new)
- G7.8 — **Hyperpay sandbox integration complete** + `dealix/payments/psp_router.py` skeleton merged

**Evidence:** Payment ID (Moyasar or Hyperpay), Sentry issue URL, UptimeRobot dashboard, LinkedIn screenshot, founder brief email log, migration files merged, `ai_tier_burndown.yaml` committed.

---

## DAY 14 — "Customer #1, AI Tier 1-2 PASS, Hyperpay live"

**Gates:**
- G14.1 — **Customer #1 signed, paid, Proof Pack delivered** (contract PDF + payment ID + Proof Pack URL + NPS captured) — **compressed from Day 30**
- G14.2 — **Hyperpay live** + 1 SAR live charge verified (revenue uncoupled from any one PSP)
- G14.3 — **Tier 1 PASS:** LLM caching (Redis) live with >30% hit rate · streaming outputs (SSE) live
- G14.4 — **Tier 2 PASS:** DecisionOutput emitted by 100% of Phase 8 agents (closes `decision_output_contract` Partial) · Action classifications enforced in pipeline wrappers (closes `classifications_enforced` Partial)
- G14.5 — **Breach runbook published** with named owner + on-call schedule
- G14.6 — **Postgres-backed audit log + approval store + tool verification ledger** running with live customer data (closes 3 Pilot claims early — compressed from Day 60)
- G14.7 — **DPO appointed** (compressed from Day 45)

**Evidence:** Customer #1 contract; Hyperpay payment ID; cache-hit metrics; CI green on DecisionOutput grep + classification enforcement tests; breach runbook commit SHA; Postgres event store carrying live trust events; DPO appointment YAML.

---

## DAY 30 — "5 customers, AI Tier 3-5 PASS, OTel + Langfuse live"

**Gates:**
- G30.1 — **5 paying customers**
- G30.2 — **Tier 3 PASS:** pgvector RAG production · 3 memory tiers (semantic + episodic + working) · per-tenant RLS verified · knowledge graph 100+ nodes
- G30.3 — **Tier 4 PASS:** Eval harness running on every PR (LLM-as-judge + golden sets) · CI gate fails on regression > 5% · 50+ golden cases per agent
- G30.4 — **Tier 5 PASS:** PII redaction (Presidio + AraBERT) on every LLM call · prompt injection detection live · refusal handling structured · off-topic detection live
- G30.5 — **OTel baseline + Langfuse live** — every HTTP request + LLM call emits `gen_ai.*` semantic conventions, traces visible in Langfuse dashboard (closes `observability_otel` Planned)
- G30.6 — **DSAR endpoints live** at `/api/v1/privacy/data-subject-request`
- G30.7 — **ROPA + lawful basis register populated**
- G30.8 — **Per-tenant cost quotas enforced**
- G30.9 — **First A/B prompt variant promoted** by eval winner (self-improvement loop functional)

**Evidence:** Customer roster · pgvector schema + RLS test · eval CI logs · guardrail decision logs · Langfuse trace URL · DSAR drill executed · `ropa.yaml` populated · quota enforcement test · `prompt_versions.yaml` entry.

---

## DAY 60 — "Series A trigger: 10 customers, 250K ARR, AI Tier 6-7 + 11 PASS, OPA + Temporal"

**Gates:**
- G60.1 — **10 paying customers · 250K ARR · 12mo runway** → Series A data room opens (compressed from Day 90)
- G60.2 — **Tier 6 PASS:** Khaleeji Arabic prompt library covering all 15+ agents (saudi_dialect.py expanded 10×+) · dialect-aware routing · Arabic QA + style validators
- G60.3 — **Tier 7 PASS:** Tool-use loop with native Anthropic tool-use API · auto-emission to verification ledger on every call · structured tool registry · fallback chain tested
- G60.4 — **Tier 11 PASS:** Langfuse capturing every LLM call · OTel gen_ai.* end-to-end trace_id flow (FastAPI → workflow → LLM → tool → DB → audit) · cost dashboard live · eval dashboard live · Sentry + PagerDuty integration
- G60.5 — **OPA/Rego policy engine** handling all policy decisions with per-tenant policies (closes `policy_evaluator` Pilot)
- G60.6 — **Temporal MVP** running Phase 8 pipeline durably with replay verified
- G60.7 — **Retention enforced in DB** (PDPL Art. 30) · full NCA ECC 2-2024 control mapping complete (closes `nca_alignment` Planned)
- G60.8 — **First CTO co-founder hire** signed and onboarded
- G60.9 — **Tap PSP integration live** (third PSP for redundancy)

**Evidence:** Cap table model + Series A data room URL · OPA decision logs with trace IDs · Temporal replay test · Khaleeji Arabic eval results · tool ledger sample (24h) · `compliance_saudi.yaml` NCA-mapped diff · CTO offer letter · Tap payment ID.

---

## DAY 120 — "30 customers, AI Tier 8-9 PASS, enterprise-ready, SDAIA filed"

**Gates:**
- G120.1 — **30 paying customers · 750K ARR**
- G120.2 — **Tier 8 PASS:** LangGraph branching live for qualification → booking/nurture · Temporal saga pattern for cross-service workflows (CRM + Calendly + email + audit with compensation) · trace_id propagation end-to-end
- G120.3 — **Tier 9 PASS:** Per-tenant monthly budgets enforced · per-day quotas per agent · provider rate-limit backoff · cost anomaly alerting (3-sigma) · cost dashboard < 5% drift
- G120.4 — **Knowledge graph for accounts** scaled to 1K+ nodes with relationship inference
- G120.5 — **SDAIA registration submitted**
- G120.6 — **ZATCA Phase 2 cert rotation automated** (12-month cron + 30-day expiry alerts)
- G120.7 — **First non-founder AE hired and ramped** (3 demos/week solo)
- G120.8 — **Accessibility audit pass** (WCAG 2.1 AA verified externally)
- G120.9 — **A/B prompt testing framework** with statistical-significance gates

**Evidence:** Customer roster + ARR statement · LangGraph workflow diagram · per-tenant quota enforcement test · cost dashboard screenshot · knowledge graph node count · SDAIA submission receipt · ZATCA cron logs · AE ramp KPI · external a11y audit report · A/B winner ledger.

---

## DAY 180 — "Scale-ready: 1.5M SAR ARR, Series A closed, all 12 AI tiers, all claims Production"

**Gates:**
- G180.1 — **1.5M SAR ARR achieved** (or 80%+ on track with binding LOIs) — compressed from Day 365
- G180.2 — **Series A closed** (or strategic alternative confirmed: revenue-financing via 1.5M ARR)
- G180.3 — **All `no_overclaim.yaml` claims at Production** (zero Pilot, Partial, or Planned) — ~50 claims total including new ones added during execution
- G180.4 — **Tier 10 PASS:** Self-improvement loop complete — friction log → prompt A/B → eval feedback → versioned prompt update · Jinja2 templates with versioning live · all hardcoded prompts migrated
- G180.5 — **Tier 12 PASS:** Multi-modal — Gemini for document understanding (contracts, RFPs, ZATCA invoices) · Whisper/Gemini-audio for sales calls · post-call summary agent · multi-modal evidence in Evidence Packs
- G180.6 — **All 12 AI tiers fully implemented + verified** by eval suite + manual audit + Tier-by-tier verification scripts green
- G180.7 — **Regional expansion plan** (UAE / Bahrain / Qatar) ready for execution
- G180.8 — **60+ paying customers · 30+ references with NPS > 50 average**
- G180.9 — **Compliance moat proven** — at least 1 enterprise customer citing PDPL/ZATCA-native as decisive reason
- G180.10 — **First quarterly board meeting** completed (compressed cadence: monthly boards Day 60–180)

**Evidence:** ARR statement · Series A term sheet or revenue-financing agreement · `no_overclaim.yaml` 100% Production diff · all 12 tier-verification scripts green · multi-modal eval results · expansion plan doc · reference roster + NPS scores · customer testimonial · board pack PDFs (3 monthly meetings minimum).

---

# §6. The 12 AI Tiers — طبقات الذكاء الاصطناعي بالكامل

---

## Tier 1 — LLM Router Hardening

**Anchor:** `core/llm/router.py`, `auto_client_acquisition/llm_gateway_v10/{budget_policy,cache_policy,fallback_policy,routing_policy,token_estimator}.py`

**Deliverables:**
1. **Redis-backed response cache** — key = `sha256(provider | model | normalized_prompt | params)`. TTL by task: intake 5 min, sector intel 24h, market research 12h. Cache-hit flag on `LLMResponse`.
2. **Streaming outputs** — SSE endpoint at `/api/v1/agents/{id}/stream`. Backend agents remain non-streaming.
3. **Per-customer quotas** — `budget_policy.py` reads tenant budget from `dealix/registers/customer_budgets.yaml`. Over-budget → fallback to cheaper model (DeepSeek/Groq) or 429.
4. **Latency tracking** — p50/p95/p99 per provider per model. Exposed in `api/routers/cost_tracking.py` + `/[locale]/ops/founder` dashboard.
5. **Provider rate-limit backoff** — exponential with jitter; surface 429 status as `LLMRetryable` exception; auto-fallback to next provider in chain.
6. **Cost ledger** — `cost_tracker.py` extended with `(cache_hit, latency_ms, retry_count, fallback_count)` per call.

**Verification:** `tests/unit/test_model_router.py` extended with cache, streaming, quota, rate-limit-backoff cases. New `scripts/llm_router_health.py` runs daily.

**Done when:** Cache hit > 30% · streaming SSE round-trip < 200ms first byte · per-customer over-budget triggers fallback · latency dashboards live.

---

## Tier 2 — Agent Maturity

**Anchor:** `core/agents/base.py`, all `auto_client_acquisition/agents/*.py`, `autonomous_growth/agents/*.py`

**Deliverables:**
1. **Pydantic v2 I/O on every agent** — input and output schemas declared as Pydantic models, not dataclasses.
2. **`DecisionOutput` return on every agent** — `dealix/contracts/decision.py::DecisionOutput` with `evidence`, `policy_decision`, `classification`, `confidence`, `trace_id`. CI gate fails PR if any agent class missing return annotation.
3. **Evidence Pack auto-built per agent call** — reuse `dealix/contracts/evidence_pack.py`. Every Tier-A/B decision ships with source citations.
4. **Verification ledger emission** — `BaseAgent` enforces emission to `dealix/trust/tool_verification.py` after every tool call (intent + actual + diff). Closes `tool_verification` Pilot.
5. **Standardized error taxonomy** — `AgentError`, `BudgetExceeded`, `PolicyDenied`, `ApprovalPending`, `EvidenceMissing` — all surfaced consistently.

**Files (15+ agent files):**
- `auto_client_acquisition/agents/{intake,icp_matcher,pain_extractor,qualification,booking,crm,proposal,outreach,followup,prospector,rules_router}.py`
- `autonomous_growth/agents/{sector_intel,content,distribution,enrichment,competitor,market_research}.py`

**Verification:** Static AST check in CI — `scripts/audit_agent_contracts.py` (new) greps for missing DecisionOutput annotation.

**Done when:** 100% agents emit DecisionOutput · 100% Tier-A/B decisions carry Evidence Pack · every tool call logged in verification ledger.

---

## Tier 3 — RAG Production

**Anchor:** `core/memory/revenue_memory.py`, `core/memory/embedding_service.py`

**Deliverables:**
1. **pgvector extension enabled** in Railway Postgres + migration committed.
2. **Three memory tiers:**
   - **Semantic** (long-term facts about accounts, contacts, sectors) — pgvector-backed
   - **Episodic** (per-customer conversation/decision history) — pgvector-backed with recency boost
   - **Working** (per-session scratchpad) — Redis-backed, TTL 30 min
3. **Knowledge graph for accounts** — nodes: company, person, signal, decision, evidence. Edges: derived, observed, contradicted. Postgres-backed initially; Neo4j evaluated at Day 365.
4. **Embedding caching by content hash** — avoid re-embedding identical content.
5. **Hybrid retrieval** — vector similarity + BM25 keyword + recency decay + tenant filter (RLS).
6. **Per-tenant memory isolation** — enforced via `auto_client_acquisition/platform_v10/rls_contract.py`.

**Files:**
- `core/memory/{revenue_memory,embedding_service}.py`
- `auto_client_acquisition/platform_v10/rls_contract.py`
- New migration: `migrations/versions/20260701_pgvector_enable.py`

**Verification:** `scripts/check_embeddings_readiness.py` (exists) — extend to verify pgvector + 3-tier query latency. RAG eval suite in `evals/rag_recall.yaml` (new).

**Done when:** pgvector live · 3 memory tiers queryable · knowledge graph 100+ nodes · RLS verified across tenants · hybrid retrieval recall@10 > 0.85 on golden set.

---

## Tier 4 — Eval Harness

**Anchor:** `evals/*.yaml`, `evals/{personal_operator_cases,revenue_os_cases}.jsonl`

**Deliverables:**
1. **LLM-as-judge harness** — Claude (Opus) scores agent outputs on per-task rubrics. Rubric in YAML per eval suite.
2. **Regression suites in CI** — every PR runs eval on golden dataset; CI fails if mean score drops > 5% on any suite.
3. **Golden dataset expansion** — 50 cases per agent minimum (currently <20). Bilingual: 25 AR + 25 EN.
4. **Bilingual eval** — Arabic + English with localized rubrics (Khaleeji tone, MSA correctness, RTL formatting). Reuse `evals/arabic_quality_eval.yaml`.
5. **Eval dashboard** — surfaced in `/[locale]/ops/eval`. Per-agent score history, drift alerts, winning prompt variant.
6. **Eval-driven prompt promotion** — top-scoring variant wins; promoted to production via versioned template.

**Files:**
- `evals/*.yaml` (expand to cover all 15+ agents)
- New: `scripts/eval_run.py`, `scripts/eval_dashboard.py`
- `.github/workflows/eval-regression.yml` (new)

**Verification:** `scripts/eval_run.py --suite all` exits non-zero if regression detected.

**Done when:** 15+ eval suites running on every PR · 50+ golden cases per agent · CI regression gate active · dashboard live.

---

## Tier 5 — Guardrails

**Anchor:** `auto_client_acquisition/tool_guardrail_gateway/{input_guardrails,output_guardrails,tool_guardrails,cost_budget}.py`, `api/middleware/bopla_redaction.py`

**Deliverables:**
1. **PII redaction** — Presidio (English) + custom AraBERT-based NER (Arabic) for: full names, NIDs/Iqama (10 digits), IBANs (SA + 22), KSA phone formats (+966 / 05), addresses, DOBs.
2. **Prompt injection detection** — heuristics (jailbreak patterns) + small classifier on every user-supplied text. Test file exists at `tests/test_v7_prompt_injection_resistance.py` — wire runtime guardrail.
3. **Refusal handling** — when policy denies, surface structured refusal with reason code (`REFUSAL_FORBIDDEN_CLAIM`, `REFUSAL_NO_LAWFUL_BASIS`, etc.) instead of LLM-generated apology.
4. **Off-topic detection** — intent classifier; route off-topic to canonical "we don't do that" response.
5. **Output guardrails** — block forbidden claims via `auto_client_acquisition/saudi_layer/forbidden_claims.py`. Examples: "100% guarantee", "shariah-certified" (without cert), revenue numbers above evidence level.
6. **All guardrail decisions logged** with trace IDs in audit log.

**Files:**
- `auto_client_acquisition/tool_guardrail_gateway/*` (fill in scaffolded implementations)
- `api/middleware/bopla_redaction.py` (extend)
- `auto_client_acquisition/saudi_layer/forbidden_claims.py`

**Verification:** `tests/test_v7_prompt_injection_resistance.py` extended; new `tests/test_guardrails_pii.py`, `tests/test_guardrails_forbidden_claims.py`.

**Done when:** Zero PII in LLM logs (sampled audit) · prompt injection corpus 95%+ caught · forbidden claims blocked · refusals structured.

---

## Tier 6 — Bilingual Depth

**Anchor:** `core/prompts/saudi_dialect.py` (current 8.7KB → target 100KB+), `auto_client_acquisition/saudi_layer/*`

**Deliverables:**
1. **Khaleeji Arabic prompt library** — coverage for all 15+ agents. Tone, phrasing, idioms, formal/informal registers, sector-specific terms.
2. **Dialect-aware routing** — detect Khaleeji vs MSA; route accordingly (Khaleeji → GLM for casual, Claude for formal).
3. **RTL/LTR-aware formatting** — mixed-content responses (Arabic body with English brand names) properly bidi-tagged.
4. **Saudi sector taxonomy localized** — `auto_client_acquisition/saudi_layer/saudi_sector_taxonomy.py` extended to 12+ sectors with Arabic + English labels + ISIC codes.
5. **Arabic QA + style validator** — every Arabic LLM output runs through `auto_client_acquisition/saudi_layer/arabic_qa.py` + `arabic_style.py` (files exist) before delivery.
6. **City/region normalizer** — `auto_client_acquisition/saudi_layer/city_region_normalizer.py` handles spelling variants (الرياض / ar-Riyadh / Riyadh).

**Files:**
- `core/prompts/saudi_dialect.py` (expand 10×+)
- `auto_client_acquisition/saudi_layer/{arabic_qa,arabic_style,saudi_sector_taxonomy,city_region_normalizer,forbidden_claims}.py`

**Verification:** `evals/arabic_quality_eval.yaml` extended with Khaleeji rubric. Native-speaker spot-check quarterly.

**Done when:** All 15+ agents have agent-specific Arabic prompt section · Arabic QA pass rate > 95% · Khaleeji vs MSA routing measurable · style validator catches > 90% of issues.

---

## Tier 7 — Tool-Use Loop

**Anchor:** `core/agents/tools.py`, `dealix/trust/tool_verification.py`

**Deliverables:**
1. **Structured tool registry** — every tool declared with `(name, description, input_schema, classification (A/R/S), connector_binding)`.
2. **Native Anthropic tool-use API** — integrate in `core/llm/anthropic_client.py`. Replace string-parsing of tool calls.
3. **Auto-emission to verification ledger** on every tool call (intent + actual result + diff + side effects).
4. **Tool result schema validation** before consumption by agent.
5. **Tool failure fallback** — `fallback_policy.py` defines per-tool fallback chain (e.g., HubSpot fail → email fallback → manual queue).

**Files:**
- `core/agents/tools.py`, `core/agents/base.py`
- `core/llm/anthropic_client.py` (extend with native tool use)
- `dealix/trust/tool_verification.py` (DB-backed in Tier 3)
- `auto_client_acquisition/llm_gateway_v10/fallback_policy.py`

**Verification:** `tests/unit/test_tool_registry.py` (new). Audit query: every tool call in last 24h has corresponding verification ledger entry.

**Done when:** 100% tool calls logged to ledger · zero string-parsing of tool calls · fallback chain tested.

---

## Tier 8 — Agentic Orchestration

**Anchor:** `auto_client_acquisition/orchestrator/*`, future `temporal/`

**Deliverables:**
1. **LangGraph for branching decision flows** — e.g., qualification → either booking OR nurture branch.
2. **Temporal for durability + replay** (Track 4).
3. **Workflow trace IDs propagated** to all LLM calls — single trace_id flows from FastAPI request → workflow → activity → LLM call → tool call → DB write → audit entry. Linked in OTel.
4. **Saga pattern** for cross-service workflows — e.g., CRM upsert + Calendly book + email send + audit, with compensation if any step fails.

**Files:**
- `auto_client_acquisition/orchestrator/{runtime,durable_workflow,queue,tools}.py`
- New: `temporal/workflows/`, `temporal/activities/`

**Verification:** End-to-end trace visible in Langfuse covering 1 customer journey from intake → proof pack.

**Done when:** Pipeline runs durable + replayable · LangGraph branching live for qualification → booking/nurture · saga compensation tested.

---

## Tier 9 — Cost Controls

**Anchor:** `auto_client_acquisition/llm_gateway_v10/budget_policy.py`, `dealix/observability/cost_tracker.py`

**Deliverables:**
1. **Per-tenant monthly budget** — over-budget → throttle to cheaper model (DeepSeek/Groq) or 429.
2. **Per-day quotas per agent type** — e.g., outreach max 50 invocations/day per tenant.
3. **Provider rate-limit awareness** — backoff with jitter; surface 429 from provider as `LLMRetryable`.
4. **Cost dashboard** — by tenant / agent / provider in `api/routers/cost_tracking.py` + `/[locale]/ops/founder`.
5. **Cost anomaly alerting** — 3-sigma over 7-day rolling baseline → Sentry alert + Slack webhook.

**Files:**
- `auto_client_acquisition/llm_gateway_v10/budget_policy.py`
- `dealix/observability/cost_tracker.py`
- `api/routers/cost_tracking.py`
- New `dealix/registers/customer_budgets.yaml`

**Verification:** `scripts/cost_anomaly_check.py` (new) runs hourly.

**Done when:** Over-budget triggers fallback (verified test) · cost dashboard < 5% drift from actual · anomaly alerts fire on synthetic spike.

---

## Tier 10 — Self-Improvement Loop

**Anchor:** `auto_client_acquisition/friction_log/*`, `auto_client_acquisition/learning_flywheel/*`, `auto_client_acquisition/self_evolving_os/*`

**Deliverables:**
1. **Friction events captured** during agent runs — low confidence, user override, policy rejection, eval-score drop, customer complaint.
2. **Friction aggregator** — `auto_client_acquisition/friction_log/aggregator.py` (file exists) produces signals weekly.
3. **Prompt A/B variant generator** — strong model (Claude) analyzes friction signals + suggests prompt variants.
4. **Eval harness scores variants** → winner promoted via versioning (Tier 4 dependency).
5. **Prompt versioning system** — replace string formatting with Jinja2 templates under version control in `core/prompts/templates/`.
6. **Migration of all hardcoded prompts** in `core/prompts/` to versioned templates.
7. **Self-evolving outputs require founder review** before deploy (A1 constraint — never auto-promote externally-facing copy).

**Files:**
- `auto_client_acquisition/friction_log/{aggregator,signal_generator}.py`
- `auto_client_acquisition/learning_flywheel/*`
- `auto_client_acquisition/self_evolving_os/*`
- `core/prompts/templates/*.jinja2` (new)
- New `dealix/registers/prompt_versions.yaml`

**Verification:** `scripts/prompt_ab_run.py --week` produces A/B reports; promoted variants logged in `prompt_versions.yaml`.

**Done when:** Weekly A/B test runs · winning variant promoted (founder-approved) · prompt versions tracked · friction → variant → eval → promote loop closed.

---

## Tier 11 — Observability

**Anchor:** `dealix/observability/{otel,cost_tracker,sentry}.py`

**Deliverables:**
1. **Langfuse live** — capturing every LLM call. Dashboard URL committed in ops doc.
2. **OTel gen_ai.* semantic conventions** — every LLM call emits standard attributes per OpenTelemetry GenAI spec.
3. **Trace UI** — Jaeger or Honeycomb or Langfuse trace view. Recommend Langfuse for AI-first.
4. **Cost dashboard** (Tier 9).
5. **Eval dashboard** (Tier 4).
6. **Single trace ID** flows from FastAPI request → workflow → LLM call → tool call → DB write → audit entry.
7. **Sentry for errors** + PagerDuty integration for critical alerts.

**Files:**
- `dealix/observability/{otel,cost_tracker,sentry}.py`
- `api/main.py` (init OTel)
- `api/middleware/http_stack.py` (request_id propagation)
- `core/llm/router.py` (LLM span emission)

**Verification:** Sample trace from any API call to audit entry must show single trace_id across all spans. `scripts/langfuse_smoke.py` (new) verifies trace ingestion.

**Done when:** Langfuse dashboard receiving traces · OTel gen_ai.* emitted · single trace_id end-to-end · Sentry capturing prod errors.

---

## Tier 12 — Multi-Modal

**Anchor:** `core/llm/gemini_client.py`, new `core/llm/voice_client.py`

**Deliverables:**
1. **Gemini for document understanding** — contracts, RFPs, ZATCA invoices, regulatory PDFs. Upload → Gemini parse → DecisionOutput with extracted entities.
2. **Document ingestion pipeline** — `auto_client_acquisition/document_intake/` (new). Per-document type schema. Evidence cited by page + clause.
3. **Whisper or Gemini-audio for sales calls** — transcription + speaker diarization.
4. **Post-call summary agent** — transcribe → extract pain → update memory → next-action recommendation. New agent class `PostCallSummaryAgent`.
5. **Multi-modal evidence in Evidence Packs** — image of contract page citing the clause; audio snippet of customer stating pain.

**Files:**
- `core/llm/gemini_client.py` (extend with vision + document modes)
- New `core/llm/voice_client.py`
- New `auto_client_acquisition/document_intake/`
- New agent `auto_client_acquisition/agents/post_call_summary.py`

**Verification:** `evals/multimodal_doc_eval.yaml` (new) covers contract/RFP/invoice parsing accuracy.

**Done when:** Customer can upload contract → Gemini extracts clauses → Decision Passport cites clauses · sales call transcribed → pain extracted → memory updated.

---

# §7. Risk Register — سجل المخاطر

| # | Risk | Likelihood | Impact | Mitigation | Owner |
|---|---|---|---|---|---|
| R1 | Moyasar account verification stalls > 30 days | M | Critical | Parallel Hyperpay + Tap integration; manual invoicing bridge | Founder |
| R2 | LLM provider price spike or outage | M | High | 6-provider router mitigates; weekly provider-health drill | CTO |
| R3 | PDPL violation (data leak, missing DSAR, expired consent) | L | Catastrophic | Full Track 6; quarterly drills; DPO Day 45 | DPO |
| R4 | Founder key-person risk | H | Critical | Documentation discipline; CTO co-founder hire Day 90; bus-factor scripts | Founder |
| R5 | Series A market closes before Day 90 trigger | M | High | Bridge from KSA angels; revenue-financing via 1.5M ARR | Founder |
| R6 | Cold-channel temptation (LinkedIn auto, WhatsApp blast) | M | Critical | Hard gates in code; CI tests; channel_policy_gateway enforced | Trust |
| R7 | Prompt injection / jailbreak in customer agent | M | High | Tier 5 guardrails; output sanitization; refusal handling | AI Lead |
| R8 | Cost runaway from LLM calls | M | High | Tier 9 quotas + anomaly alerting + cheap-model fallback | CTO |
| R9 | Hallucination causes false claim in customer Proof Pack | M | High | Evidence Pack requires source citations; LLM-as-judge eval; forbidden_claims filter; human approval on A1+ | AI Lead |
| R10 | Postgres scale ceiling | L | Medium | Track 3 RLS by tenant; pgvector partition; read replicas Day 365 | CTO |
| R11 | Talent acquisition delay (KSA senior AI/SE) | H | Medium | Remote-friendly offers; contractor bridge; KAUST/KFUPM pipeline | Founder |
| R12 | Saudi compliance regime shift (PDPL amendments, NCA updates) | M | Medium | Subscribe to SDAIA bulletins; `compliance_saudi.yaml` reviewed quarterly | DPO |
| R13 | Competitor (US tool localized) enters first | M | Medium | Compliance moat hard to copy fast; double-down on PDPL/ZATCA-native messaging | Marketing |
| R14 | Customer concentration (single account > 30% ARR) | M | Medium | Diversify across 7 verticals; cap any single customer at 25% ARR | Sales |
| R15 | Tech debt from 175+ `_os` modules (orphans, duplicates) | H | Medium | Quarterly module audit + dedupe (e.g., 4 different "company_brain" modules); explicit deprecation register | CTO |

---

# §8. Decision Gates — بوابات القرار

| Gate | Day | PASS criteria | Evidence | Owner |
|---|---|---|---|---|
| **A — Revenue Path Live (multi-PSP)** | 7 | First live charge via Moyasar OR Hyperpay · Sentry capturing · UptimeRobot green · First DM sent · Founder brief x7 · Trust Plane Postgres migrations merged · All 12 AI tiers scaffolded with owners | Payment ID, Sentry URL, UptimeRobot screenshot, LinkedIn screenshot, migration files, `ai_tier_burndown.yaml` | Founder |
| **B — First Customer + AI Tier 1-2 PASS** | 14 | Customer #1 signed/paid/Proof-Pack-delivered · Hyperpay live · Tier 1 (cache + streaming) PASS · Tier 2 (DecisionOutput everywhere + classifications) PASS · Postgres trust plane carrying live data · DPO appointed · Breach runbook published | Contract PDF, payment ID, Proof Pack URL, CI green, DPO YAML, breach runbook | Founder + CTO |
| **C — AI Tier 3-5 + Observability** | 30 | 5 customers · Tier 3 (pgvector RAG + 3 memory tiers + KG 100+ nodes) PASS · Tier 4 (eval harness in CI) PASS · Tier 5 (PII + prompt-injection + refusal guardrails) PASS · OTel + Langfuse live · DSAR endpoints · ROPA · Per-tenant quotas · First A/B variant promoted | Customer roster, tier verification scripts, Langfuse URL, eval CI logs, DSAR drill, `prompt_versions.yaml` | CTO / AI Lead |
| **D — Series A Trigger + AI Tier 6-7+11** | 60 | 10 customers · 250K ARR · 12mo runway · Data room opens · Tier 6 (Khaleeji Arabic depth) PASS · Tier 7 (tool-use loop) PASS · Tier 11 (full observability) PASS · OPA/Rego per-tenant · Temporal MVP · Retention + NCA mapping complete · CTO hire signed · Tap live | ARR statement, cap table, OPA logs, Temporal replay test, Arabic eval results, tool ledger sample, NCA-mapped register, CTO offer letter | Founder + CTO |
| **E — AI Tier 8-9 + Enterprise-Ready** | 120 | 30 customers · 750K ARR · Tier 8 (LangGraph + Temporal saga) PASS · Tier 9 (per-tenant cost controls + anomaly alerting) PASS · Knowledge graph 1K+ nodes · SDAIA submitted · ZATCA cert rotation cron · First AE hired/ramped · A/B framework with significance gates · WCAG 2.1 AA passed | Customer roster, LangGraph diagram, cost dashboard, KG node count, SDAIA receipt, AE ramp KPI, external a11y report | AI Lead + DPO |
| **F — Scale-Ready (all 12 tiers + Series A close)** | 180 | 1.5M SAR ARR · Series A closed (or alt) · ALL `no_overclaim` claims Production · Tier 10 (self-improvement loop) PASS · Tier 12 (multi-modal docs + voice) PASS · All 12 tiers verified · Expansion plan (UAE/BH/QA) ready · 60+ customers · 30+ NPS-50 references · Compliance-moat citation from 1+ enterprise customer | ARR statement, term sheet, register full diff, all 12 tier verification scripts green, multi-modal eval, expansion plan, reference roster, testimonial | Founder + Board |

---

# §9. Verification Approach — كيف نتحقق

**Per track, the verification scripts to run** (most already exist in `scripts/`):

| Track | Scripts (existing + new) |
|---|---|
| T1 Executive | `scripts/dealix_first3_board.py`, `scripts/dealix_founder_daily_brief.py`, new `scripts/ceo_monthly_review.py`, new `scripts/dealix_board_pack.py` |
| T2 Commercial | `scripts/dealix_daily_lead_prep.py`, `scripts/dealix_pilot_brief.py`, `scripts/dealix_demo_outcome.py`, `scripts/dealix_invoice.py`, `scripts/dealix_payment_confirmation_stub.py`, `scripts/dealix_e2e_customer_simulation.sh` |
| T3 Platform | `scripts/dealix_capability_verify.sh`, `scripts/beast_level_verify.sh`, `scripts/audit_orphan_endpoints.py`, `scripts/check_alembic_single_head.py`, `scripts/db_index_audit.py`, `scripts/check_embeddings_readiness.py` |
| T4 Execution | `scripts/check_dlq_size.py`, new `scripts/temporal_health.py` |
| T5 AI | `scripts/dealix_ai_ops_diagnostic.py`, new `scripts/eval_run.py`, new `scripts/langfuse_smoke.py`, new `scripts/audit_agent_contracts.py`, new `scripts/prompt_ab_run.py`, new `scripts/cost_anomaly_check.py`, new `scripts/llm_router_health.py` |
| T6 Compliance | `scripts/commercial_value_map_status.py`, new `scripts/dsar_drill.py`, new `scripts/breach_drill.py`, new `scripts/zatca_cert_rotation.py`, new `scripts/pdpl_artifact_check.py` |
| T7 Operations | `scripts/daily_operate.sh`, `scripts/daily_sanity.sh`, `scripts/business_readiness_verify.sh`, `scripts/company_ready_verify.sh`, `scripts/dealix_local_stack_verify.sh`, `scripts/founder_one_command.sh`, `scripts/founder_cadence.sh` |
| T8 Frontend | `lighthouserc.js` (exists), `.pa11yrc.json` (exists, extend), new `scripts/a11y_audit.sh` |

**End-to-end customer simulation:** `scripts/dealix_e2e_customer_simulation.sh` (exists) runs intake → diagnostic → ICP → pain → qualification → booking → proposal → payment → proof pack → audit loop with full policy + approval + guardrail enforcement.

**Automated KPI gates** (computed every CI run):
- Test count ≥ 3,854 (baseline) and rising
- Coverage ≥ 70% on `dealix/` + `core/`
- All 49 `no_overclaim` claims: target Production count 49 by Day 365
- LLM cost / customer / month < 50 SAR (Day 180), < 40 SAR (Day 365)
- Latency p95 < 8s (Day 90), < 5s (Day 365)
- Eval mean score > 8.0 (Day 90), > 9.0 (Day 365)

**Operating cadence locked:**
- **Daily 07:00 KSA:** founder brief (`scripts/dealix_founder_daily_brief.py`)
- **Monday 08:00:** CTO weekly tech watch + sales pipeline review
- **1st of month:** CEO monthly review with full track health
- **Quarterly (first Sunday):** board pack + incident drill + compliance drill

---

# §10. Register Reconciliation — مسار كل ادعاء إلى Production

| Current Status | Count | Claims | Target Day | Tracks |
|---|---|---|---|---|
| **Production** | 16 | multi_llm_routing, bilingual_ar_en, secret_hygiene, phase8_intake/icp/pain/pipeline, phase9_sectors/content/linkedin, docker_production, ci_security, observability_structlog, canonical_service_catalog, platform_reference_contracts, not_cursor_not_chatbot | maintain | All |
| **Partial → Production** | 5 | decision_output_contract, classifications_enforced, phase8_booking, pdpl_readiness, not_agent_executor | 14, 14, 14, 60, 30 | T3, T3, T2, T6, T3 |
| **Pilot → Production** | 5 | policy_evaluator, approval_center, audit_log, tool_verification, phase8_crm | 60, 14, 14, 14, 14 | T3, T3, T3, T3/T5, T2 |
| **Planned → Production** | 2 | observability_otel, nca_alignment | 30, 60 | T3, T6 |
| **New claims to add** | 15+ | langfuse_live (30), temporal_durable (60), opa_rego_policy (60), pgvector_rag (30), prompt_versioning (30), ab_testing (120), pii_redaction (30), prompt_injection_guardrail (30), multi_modal_docs (180), multi_modal_voice (180), self_improvement_loop (180), eval_harness_ci (30), cost_anomaly_alerting (120), knowledge_graph (60→1K nodes by 120), dsar_endpoints (30) | added when shipped | T5, T6, T4 |

**Net target by Day 180:** ~50 claims tracked · 100% Production · zero Pilot/Partial/Planned. (Compressed from Day 365 baseline plan.)

---

# §11. Critical-Path Dependencies — السلاسل الحرجة (6-month compressed)

**Day 1–7 critical chain (revenue + foundation, sequential):**
1. Moyasar resubmission + Hyperpay integration in parallel
2. Sentry DSN set
3. UptimeRobot configured
4. First DM sent
5. Postgres migrations for trust plane merged
6. AI tier burndown register created with owners
7. First live charge via Hyperpay or Moyasar

**Day 1–14 parallel chain (Customer #1 + AI Tier 1-2):**
1. Customer #1 demo booked (Day 4) → diagnostic delivered (Day 7) → Sprint started (Day 8) → Proof Pack delivered (Day 12) → contract signed + paid (Day 14)
2. **In parallel:** LLM cache (Redis) + streaming SSE shipped → DecisionOutput on every agent → classification enforcement in pipeline → Postgres trust plane carrying live events → DPO appointed → breach runbook published

**Day 1–60 AI critical chain (all 12 tiers in parallel; verification gates at Day 14/30/60):**
1. **Tier 1** (caching + streaming) — Day 14 PASS
2. **Tier 2** (DecisionOutput + classifications) — Day 14 PASS
3. **Tier 3** (pgvector RAG + 3 memory tiers + KG) — Day 30 PASS
4. **Tier 4** (eval harness + CI gate) — Day 30 PASS
5. **Tier 5** (guardrails: PII + injection + refusal) — Day 30 PASS
6. **Tier 11** (Langfuse + OTel gen_ai.*) — Day 30 PASS (early — needed for observing all other tiers)
7. **Tier 6** (Khaleeji Arabic depth) — Day 60 PASS
8. **Tier 7** (tool-use loop with ledger) — Day 60 PASS

**Day 60–180 AI critical chain (Tiers 8-10, 12):**
9. **Tier 8** (LangGraph + Temporal saga) — Day 120 PASS
10. **Tier 9** (per-tenant cost + anomaly alerting) — Day 120 PASS
11. **Tier 10** (self-improvement loop + Jinja2 versioning + A/B) — Day 180 PASS
12. **Tier 12** (multi-modal docs + voice) — Day 180 PASS

**Day 1–60 compliance chain (compressed from 120):**
1. Breach runbook + DPO appointed (Day 14)
2. ROPA + lawful basis populated (Day 30)
3. DSAR endpoints live (Day 30)
4. Retention enforced in DB (Day 60)
5. NCA control mapping complete (Day 60)

**Day 60–180 compliance chain:**
6. SDAIA submission (Day 120)
7. ZATCA cert rotation cron (Day 120)
8. Cross-border transfer register + vendor risk register finalized (Day 60)

**Day 1–180 commercial chain:**
- Day 7: revenue path live · Day 14: customer #1 · Day 30: 5 customers · Day 60: 10 customers + Series A trigger · Day 120: 30 customers + AE hired · Day 180: 60+ customers + 1.5M SAR ARR + Series A closed

**Cross-track dependency rules:**
- Tier 11 (observability) must be live by Day 30 so all other tier-verification has trace data
- Postgres trust plane (Track 3) must be live by Day 14 so OPA per-tenant work (Day 60) has data substrate
- Multi-PSP (Track 2) must be live by Day 14 so revenue is uncoupled from any one processor stall
- DPO appointed by Day 14 so all PDPL artifacts have signing owner
- CTO co-founder by Day 60 so AE hire (Day 120) and Series A close (Day 180) have engineering bandwidth

---

# §12. Appendix

## 12.1 — Critical files index (absolute paths)

**Registers (single source of truth):**
- `/home/user/dealix/dealix/registers/no_overclaim.yaml` — 49 claims
- `/home/user/dealix/dealix/registers/compliance_saudi.yaml` — PDPL/NCA/ZATCA controls
- `/home/user/dealix/dealix/registers/technology_radar.yaml` — Adopt/Trial/Hold
- `/home/user/dealix/dealix/registers/90_day_execution.yaml` — week-by-week
- New: `okrs_2026.yaml`, `board_cadence.yaml`, `hiring_plan.yaml`, `cap_table.yaml`, `ropa.yaml`, `dpo_appointment.yaml`, `vendor_registry.yaml`, `cross_border_transfers.yaml`, `customer_budgets.yaml`, `prompt_versions.yaml`, `incident_drills.yaml`

**Masters (binding specs):**
- `/home/user/dealix/dealix/masters/constitution.md`
- `/home/user/dealix/dealix/masters/trust_fabric_spec.md`
- `/home/user/dealix/dealix/masters/execution_fabric_spec.md`
- `/home/user/dealix/dealix/masters/evidence_pack_spec.md`
- `/home/user/dealix/dealix/masters/incident_rollback_runbook.md`
- `/home/user/dealix/dealix/masters/release_readiness_checklist.md`
- `/home/user/dealix/dealix/masters/repo_operating_pack.md`

**Trust Plane (Track 3 hot path):**
- `/home/user/dealix/dealix/trust/{policy,approval,audit,tool_verification}.py`
- `/home/user/dealix/dealix/contracts/{decision,evidence_pack,audit_log}.py`
- `/home/user/dealix/dealix/classifications/__init__.py`

**LLM Stack (Track 5 hot path):**
- `/home/user/dealix/core/llm/{router,anthropic_client,gemini_client,glm_client,openai_compat,base}.py`
- `/home/user/dealix/core/agents/{base,multi_agent,tools}.py`
- `/home/user/dealix/core/memory/{revenue_memory,embedding_service}.py`
- `/home/user/dealix/core/prompts/{karpathy_prompts,sales_scripts,saudi_dialect}.py`
- `/home/user/dealix/auto_client_acquisition/llm_gateway_v10/{budget_policy,cache_policy,fallback_policy,routing_policy,token_estimator}.py`

**Agents (15+ files, all need DecisionOutput):**
- `/home/user/dealix/auto_client_acquisition/agents/{intake,icp_matcher,pain_extractor,qualification,booking,crm,proposal,outreach,followup,prospector,rules_router}.py`
- `/home/user/dealix/autonomous_growth/agents/{sector_intel,content,distribution,enrichment,competitor,market_research}.py`

**Execution (Track 4):**
- `/home/user/dealix/auto_client_acquisition/orchestrator/{runtime,durable_workflow,queue,tools}.py`
- `/home/user/dealix/auto_client_acquisition/pipeline.py`
- `/home/user/dealix/auto_client_acquisition/{safe_send_gateway,channel_policy_gateway}/`

**Compliance (Track 6):**
- `/home/user/dealix/auto_client_acquisition/compliance_os/{ropa,consent_ledger,consent_signature,data_subject_requests,vendor_registry}.py`
- `/home/user/dealix/auto_client_acquisition/governance_os/{lawful_basis,workflow_control_registry}.py`
- `/home/user/dealix/api/middleware/bopla_redaction.py`
- `/home/user/dealix/integrations/{pdpl,zatca}.py`
- `/home/user/dealix/api/routers/{compliance_product,compliance_status,pdpl,pdpl_dsar}.py` + new `dsar.py`

**Payments (Track 2):**
- `/home/user/dealix/dealix/payments/{moyasar,checkout_intent,orchestrator,renewal_scheduler,refund_state_machine,reconciliation}.py`
- `/home/user/dealix/api/routers/{pricing,payment_ops,customer_webhooks,checkout}.py`

**Frontend (Track 8):**
- `/home/user/dealix/frontend/src/app/[locale]/{dashboard,pipeline,agents,approvals,clients,analytics,offer,services,pricing,partners,customer-portal,dealix-diagnostic,proof-pack,trust-check,risk-score,business-now,ops/founder,ops/war-room,ops/marketing,ops/sales,ops/evidence,ops/approvals}/`
- `/home/user/dealix/frontend/messages/{ar,en}.json`

## 12.2 — Cadence calendar

| Cadence | Day/Time (KSA) | Script | Owner | Output |
|---|---|---|---|---|
| Daily | 07:00 | `dealix_founder_daily_brief.py` | Founder | Brief email + WhatsApp |
| Daily | 08:00 | `daily_operate.sh` | Founder | Operate checklist run |
| Daily | 23:00 | `daily_sanity.sh` | CI | Sanity check |
| Daily | 03:00 | Trust Pack cron (Track 3) | System | Per-tenant trust pack |
| Weekly Mon 08:00 | | `daily_tech_watch.sh` + CTO weekly anchor | CTO | Platform KPI snapshot |
| Weekly Sun 07:00 | | `founder_weekly_loop.sh` | Founder | Weekly gates |
| Monthly 1st 09:00 | | `ceo_monthly_review.py` (new) | CEO | ARR + funnel + NPS report |
| Monthly | | DPO compliance review | DPO | PDPL register update |
| **Monthly first Sun (compressed cadence)** | | `dealix_board_pack.py` | Board chair | Board pack PDF — runs monthly Day 60–180 (compressed from quarterly) then quarterly post-Series A |
| Monthly (alongside board) | | Incident drill | On-call | Drill report |
| Monthly (alongside board) | | Compliance drill (DSAR + breach) | DPO | Drill report |
| **AI tier burndown** | Weekly | `scripts/ai_tier_burndown.py` (new) | AI Lead | Per-tier % complete, blockers, ETA per gate (Day 14 / 30 / 60 / 120 / 180) |

## 12.3 — Plan-of-Plans summary table

| Layer | What gets done | Track | First gate |
|---|---|---|---|
| Executive | OKRs, board, cap table, Series A trigger, hiring | T1 | Day 7 |
| Commercial | Moyasar unblock, customer #1, partner program, vertical playbooks, customer-mix model | T2 | Day 7 / 30 / 90 |
| Trust Plane | Postgres-backed policy/approval/audit/ledger, OPA, OTel, per-tenant policies | T3 | Day 60 |
| Execution | Temporal, durable workflows, safe-send gateway, refund/renewal state machines | T4 | Day 90 |
| AI (12 tiers) | Caching, streaming, RAG, eval, guardrails, bilingual depth, tool-use, orchestration, cost, self-improvement, observability, multi-modal | T5 | Day 30 / 90 / 180 / 365 |
| Compliance | PDPL full suite (ROPA + DSAR + retention + breach + DPO + SDAIA), NCA mapping, ZATCA rotation | T6 | Day 60 / 90 / 180 |
| Operations | Daily/weekly/monthly cadence, cost dashboards, script catalog, war room, incident drills | T7 | Day 1 / 30 / 90 |
| Frontend | Customer portal, founder cockpit, approvals UI, proof-pack viewer, trust-check page, WCAG 2.1 AA | T8 | Day 30 / 60 / 180 |

---

## Final word — كلمة نهائية

This plan is **complete and holistic, not partial**. It names every file, every track, every gate, every AI tier, every PDPL/NCA/ZATCA control, every script, every owner, every PASS criterion.

**Execution mode (locked by founder decision):**
1. **AI-first parallel execution** — all 12 AI tiers begin Day 1 with named owners and a weekly burndown ledger (`dealix/registers/ai_tier_burndown.yaml`). No tier waits for another; verification gates synthesize the cross-tier state at Day 14 / 30 / 60 / 120 / 180.
2. **6-month compressed timeline** — every gate originally scoped at Day 365 is brought forward to Day 180. Customer #1 by Day 14 (not Day 30). Series A trigger by Day 60 (not Day 90). 1.5M SAR ARR by Day 180 (not Day 365).
3. **Multi-PSP from Day 1** — Moyasar resubmission + Hyperpay integration run in parallel. Revenue is uncoupled from any single processor's KYC timeline. Tap added as third PSP by Day 60.

**The plan is bound by:**
- The Constitution (`dealix/masters/constitution.md`) — agents do not execute, humans approve
- The 8 hard gates — coded, not policed
- The 11 non-negotiables / doctrine_lock — tested in CI
- The no_overclaim register — every claim earns its evidence

**Three single-points-of-failure to mitigate from Day 1:**
1. **Moyasar account** → Hyperpay parallel integration (Day 1–14) + Tap as third processor (Day 60). PSP router (`dealix/payments/psp_router.py`) normalizes the routing layer.
2. **Founder bandwidth** → documentation discipline + CTO co-founder hire by Day 60 (compressed from Day 90). Weekly AI tier burndown forces blockers to surface.
3. **AI tier coordination at parallel scale** → `dealix/registers/ai_tier_burndown.yaml` is the single source of truth. Weekly review by AI Lead. Tier 11 (Langfuse + OTel) ships first (Day 30) so the other tiers have trace data to verify against.

Everything else — the 175+ OS modules, the 171 routers, the 12 AI tiers, the 4 registers, the 524 tests, the 110+ doc directories — is **scaffolding to execute this plan**. The plan does not add scaffolding; it makes the scaffolding **load-bearing**.
