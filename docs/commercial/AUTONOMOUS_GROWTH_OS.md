# Dealix Autonomous Growth & Strategy Execution OS

> **Mode: draft-only, approval-first.** This system thinks, plans, and prepares
> commercial work autonomously. It never sends an external message and never
> approves its own actions. The founder stays in the loop for every external
> touch and every irreversible decision.

## What it is

A self-contained autonomous layer (`dealix/autonomous_os/`) that runs a daily
cycle to advance Dealix's commercial objectives without daily founder
intervention in the *thinking*, while keeping the founder firmly in control of
the *doing*.

It is intentionally dependency-light (standard library + PyYAML) so it runs in a
minimal cron/CI environment, and it depends on no agent or integration module —
consistent with the `dealix/` kernel contract.

## The daily cycle

`AutonomousOS.run()` performs one full pass:

1. **Tripwire** — assert the environment is draft-only (`SafetyGate.assert_draft_only`).
2. **Load strategies** — from `dealix/autonomous_os/strategies/*.yaml`.
3. **Plan** — expand each active strategy into routed steps.
4. **Dispatch**
   - internal, low-risk → **Action Queue** (draft artifact, safe to prepare now)
   - external / high-risk → **Approval Queue** (founder decides; nothing is sent)
   - forbidden → **blocked** (recorded, never queued)
5. **Recommend** — the Growth Engine proposes prioritised commercial drafts.
6. **Reflect** — the Learning Loop computes transparent per-strategy scores.
7. **Report** — a bilingual-friendly daily report + JSON summary are written to
   a gitignored runtime directory.

## Module map

| File | Responsibility |
|------|----------------|
| `safety_gate.py` | Hard boundary: forbidden actions, external-channel routing, risk ceiling. |
| `strategy_registry.py` | Loads declarative strategy YAML. |
| `execution_planner.py` | Turns a strategy into a routed execution plan. |
| `action_queue.py` | File-backed queue of internal draft artifacts. |
| `approval_queue.py` | Founder-gated queue for external / high-risk actions. |
| `proof_logger.py` | Append-only JSONL audit trail. |
| `learning_loop.py` | Transparent per-strategy scoring over the proof trail. |
| `model_router.py` | Local-first (Ollama) model selection with hosted fallbacks. |
| `growth_engine.py` | Commercial prioritiser mapped to the offer ladder. |
| `integrations.py` | Honest catalogue of external tools + wiring status. |
| `orchestrator.py` | Wires the cycle together. |

## Running it

```bash
# One draft-only cycle (writes to company/runtime/autonomous_os/, gitignored):
python3 scripts/autonomous_os_daily.py

# With a commercial context signal:
python3 scripts/autonomous_os_daily.py \
  --context '{"proof_assets_ready": 3, "warm_leads": 8, "proposals_outstanding": 1}'
```

CI schedule: `.github/workflows/autonomous-os-daily.yml` runs it daily at
05:00 UTC in draft-only mode and uploads the artifacts. It verifies
`scripts/verify_no_auto_external_send.py` before running.

## Strategies shipped

| Strategy | Objective (focus) |
|----------|-------------------|
| `revenue_sprint` | Convert proof + warm relationships into booked Transformation Sprints. |
| `proof_pack` | Assemble review-ready Proof Packs that power proposals and trust. |
| `saudi_market_access` | Compliant, opt-in Saudi B2B target map from public research only. |
| `technical_trust` | Keep commercial claims backed by real, sourced evidence. |
| `content_factory` | Steady cadence of bilingual proof-led content drafts (no auto-post). |

Strategies are data. Edit the YAML to change behaviour — no code change needed.

## Core-stack adapters (real, offline-safe, draft-only)

`dealix/autonomous_os/adapters/` contains real connectors for the priority core
stack. Each is **offline-safe** (degrades to a local fallback, never raises) and
**draft-only** (none can send):

| Adapter | Tool | Role | Offline behaviour |
|---------|------|------|-------------------|
| `ollama_adapter` | Ollama | local-first text generation (the "brain") | deterministic template draft |
| `twenty_adapter` | Twenty CRM | read-only pipeline signals → GrowthContext (the "eyes") | local snapshot / zeros |
| `whatsapp_draft_adapter` | Evolution/WhatsApp | formats review-ready payload drafts (the bound "hands") | always draft-only, **no send method exists** |

`draft_composer.py` uses the model router + Ollama adapter to compose actual
draft text for each queued item; when no model is present it falls back to a
labelled template. The orchestrator pulls commercial context from the CRM
adapter automatically when no explicit context is passed, and surfaces every
adapter's status in the daily report. These adapters use only the standard
library (`urllib`) — no extra install in CI/cron.

## Toolkit orchestration (honest status)

`integrations.py` catalogues the external open-source tools this OS is *designed
to* orchestrate (n8n, Dify, Ollama, CrewAI/LangGraph, Twenty, Firecrawl, Mem0,
Evolution API, and more), each tagged with its real wiring status
(`reference` / `adapter_planned`). **Nothing in that catalogue is wired to send
anything.** When an adapter is built, it must still pass through the Safety Gate
and Approval Queue. Local-first / self-hosted tools are preferred.

## What this OS will never do

- Send WhatsApp, email, SMS, or any external message automatically.
- Perform cold outreach, contact scraping, or LinkedIn automation.
- Issue invoices or charge customers automatically.
- Approve its own external actions.
- Fabricate metrics, testimonials, or guaranteed-ROI claims.

See `SAFETY_GATES.md` and `ACTION_APPROVAL_POLICY.md` in this folder.
