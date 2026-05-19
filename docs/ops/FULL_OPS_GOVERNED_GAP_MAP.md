# Dealix — Governed Full Ops — Gap Map

> Version 1 — 2026-05-18 — Audit of the existing system before building.
> Scope: a **governed** self-running Full Ops system — automated end-to-end
> **up to a human approval gate**. Aligned with the 11 non-negotiables and
> [`../strategy/DEALIX_COMMERCIAL_PROOF_MODE_AR.md`](../strategy/DEALIX_COMMERCIAL_PROOF_MODE_AR.md).

This document is the single source of truth for what the Full Ops system
**already has**, what is **broken**, and what is **missing** — so we build
only the gaps, in governed form, and reuse everything that exists.

هذه الوثيقة جرد للنظام الحالي قبل البناء: الموجود · المكسور · الناقص.

---

## 1. What already exists (do NOT rebuild)

### Agents & orchestration

- **11 sales agents** wired into `AcquisitionPipeline`
  (`auto_client_acquisition/pipeline.py`): Intake · ICPMatcher · PainExtractor ·
  Qualification · Proposal · Booking · FollowUp · Outreach · CRM ·
  RulesRouter · Prospector.
- **Real `Orchestrator` + `TaskQueue`** (`auto_client_acquisition/orchestrator/`)
  with autonomy modes (MANUAL → SUGGEST → DRAFT_APPROVE → SAFE_AUTOPILOT →
  FULL_AUTOPILOT) and a `requires_approval()` policy gate.
- **`ApprovalStore`** (`auto_client_acquisition/approval_center/`) with
  founder auto-approve rules + safety policy.
- Flagship workflow `DAILY_GROWTH_RUN` (8 steps, discover → … → report).

### OS modules

- **Production-grade (6):** `data_os` · `governance_os` · `sales_os` ·
  `value_os` · `client_os` · `adoption_os` — all have tests.
- **Stub / partial (3):** `proof_os` · `capital_os` · (`friction_log` partial).

### Backend

- `api/routers/revenue_ops_autopilot.py` + `api/routers/full_ops.py` —
  real, draft-first, approval-guarded; `GET /api/v1/full-ops/daily-command-center`
  aggregates 5 OS queues + hard gates + revenue truth.
- **Proof ledger** — file (JSONL) + Postgres backends, PII-redacted on write.
- **Evidence pack** — bundled per high-stakes decision.
- **Approval Center API** — pending / create / approve / reject / edit /
  bulk-approve / expire-sweep.
- **Hard gates** enforced: `no_live_send`, `no_live_charge`, `no_scraping`,
  `no_cold_outreach`, `no_linkedin_automation`, `no_fake_proof`,
  `approval_required_for_external_actions`.
- Integrations real: HubSpot · WhatsApp (live-send gated) · email.

### Frontend

- Feature-rich ops cockpit: `/[locale]/ops/founder` · `/ops/war-room` ·
  `/ops/marketing` · `/ops/sales` · `/ops/evidence` · `/business-now`.
- Data-rich components in `frontend/src/components/gtm/`.

---

## 2. What is BROKEN (fix before anything else)

| # | Issue | Impact | Fix |
|---|---|---|---|
| B1 | `frontend/src/lib/opsAdmin.ts` is gitignored and missing — `npm run build` fails (`Can't resolve '@/lib/opsAdmin'`) in ~12 components | **Entire frontend will not build** | Reconstruct the module (spec in §5) and force-add it (`git add -f`); fix the `.gitignore` `lib/` rule so real lib files are not blocked |

---

## 3. What is MISSING (build, in governed form)

### Backend spine

| # | Gap | Why it matters |
|---|---|---|
| M1 | ✅ **BUILT** — `PostgresApprovalStore` persists the approval queue across restarts; `approval_store_backend=postgres` opt-in, in-memory fallback | CRITICAL production blocker — now closed |
| M2 | ✅ **BUILT** — `GovernedScheduler` daemon thread runs `run_governed_day` once per KSA day; env-gated (default off), founder kill switch via `/governed-ops/scheduler/stop` | Self-running loop inside the deployment |
| M3 | ✅ **BUILT** — `run_governed_day()` single observable entrypoint + `scripts/dealix_governed_day.py` CLI + `/api/v1/governed-ops` API | Composable "run the day" operator now exists |
| M4 | ✅ **BUILT** — `governance_log` durable event stream (action_blocked / approval_decision / phase_*) on the append-only event store, queryable via API | Blocked-actions audit log now exists |
| M5 | ✅ **BUILT** — `orchestration_sdk` is the one governed import for agents: queue drafts, advance lifecycle, plan sequencing, log governance, run the day | Agents stay on the governed rails by construction |
| M6 | ✅ **ALREADY COVERED** — `api/routers/value_os.py` exposes `POST /api/v1/value/event/{customer_id}` (tier-disciplined) + monthly report endpoints; the `value_ledger_events` table shipped in migration 012 | No new build — reuse |

### Sales engine

| # | Gap | Why it matters |
|---|---|---|
| M7 | **No persistent sequencing / campaign engine** — FollowUp cadence is in-memory only | Cannot run "N leads × 3-touch sequence" reliably |
| M7 | ✅ **BUILT** — `sequencing_engine` + `follow_up_tasks` table persists the cadence; `due_tasks`/`mark_task` drive a governed release | Reliable multi-touch sequencing |
| M8 | ✅ **BUILT** — canonical `LeadLifecycleStage` + forward-only state machine; `leads.lifecycle_stage` + `lead_stage_transitions` table | Durable pipeline state |
| M9 | ✅ **BUILT** — `bulk_intake.normalize_import` lands raw import rows as `captured` leads (dedup + reject); `draft_approval_bridge` auto-queues every agent draft into the governed approval queue | Import-and-process a list; drafts always governed |

### Frontend cockpit

| # | Gap | Why it matters |
|---|---|---|
| M10 | `/ops/targeting`, `/ops/support`, `/ops/partners` hollow/missing (APIs exist) | Cockpit incomplete |
| M11 | No ops-specific **approval queue UI** + no **kill switch** | Founder cannot review/halt governed automation from one place |
| M12 | No unified `ops.*` i18n namespace | Strings scattered, fragile |

### Agent depth

| # | Gap | Why it matters |
|---|---|---|
| M13 | `proof_os` + `capital_os` are stubs | Proof Pack scoring + capital asset registration are thin |
| M14 | No multi-step approval chains (legal → finance → CEO) | Single boolean gate only |

---

## 4. Recommended build sequence (governed, phased)

- **Phase 0 — Unblock (B1):** reconstruct `opsAdmin.ts`, fix `.gitignore`,
  green `npm run build`.
- **Phase 1 — Backend spine (M1, M3, M4):** Postgres-backed `ApprovalStore`;
  one canonical orchestration entrypoint; durable blocked-actions/event log.
- **Phase 2 — Sales engine (M7, M8, M9):** lead lifecycle state machine +
  persistent sequencing engine + bulk intake — all queue to the approval gate.
- **Phase 3 — Cockpit (M10, M11, M12):** governed ops approval UI + kill
  switch; fill targeting/support/partners; unified `ops.*` namespace.
- **Phase 4 — Depth (M2, M5, M6, M13, M14):** scheduler, agent SDK, value
  ledger API, productionize `proof_os`/`capital_os`, multi-step approvals.

Every phase keeps the rule: **automation stops at the human approval gate**;
no new external-send path is added.

---

## 5. `opsAdmin.ts` reconstruction spec (Phase 0)

`frontend/src/lib/opsAdmin.ts` must export exactly three functions
(verified against all ~12 caller sites):

| Export | Signature | Behaviour |
|---|---|---|
| `getAdminApiKey` | `() => string \| null` | localStorage `dealix_admin_api_key`, fallback `process.env.NEXT_PUBLIC_DEALIX_ADMIN_API_KEY`, else `null` |
| `isOpsConfigured` | `() => boolean` | `true` iff `getAdminApiKey()` is a non-empty string |
| `opsMissingKeyMessage` | `(isAr: boolean) => string` | localized "ops not configured — set admin API key" message |

---

> Estimated outcomes are not guaranteed outcomes / النتائج التقديرية ليست نتائج مضمونة.
