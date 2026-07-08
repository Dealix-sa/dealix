# Dealix Autonomous Company OS — Execution Spine

## Mission

Build Dealix as a safe, draft-only, approval-first Saudi B2B Company Operating System.

Dealix must serve Dealix first, then become a managed service for pilot clients, then evolve into SaaS.

This execution spine turns the uploaded master plan into concrete operating layers across GitHub, Slack, Airtable/Sheets, Google Contacts, daily reports, approval queues, proof logs, and self-improvement loops.

## Non-negotiable safety rules

- No live outbound by default.
- No cold WhatsApp campaigns.
- No mass LinkedIn automation.
- No auto-posting content.
- No payment capture without explicit approval.
- No production mutation without explicit approval.
- No secret printing or hardcoded credentials.
- No fake proof, fake clients, fake ROI, or guaranteed revenue claims.
- No government-access claims.
- All external actions must be draft-only, approval-first, and audit-logged.

## Core architecture

```txt
Company Brain
→ Data & Intelligence Layer
→ Opportunity Graph
→ Agent Team
→ Strategy Execution Engine
→ Action Queue
→ Approval Center
→ Proof Ledger
→ Revenue Path Engine
→ Self-Improvement Engine
→ Daily / Weekly Reports
→ Safe connector workflows
```

## Autonomy levels

| Level | Name | Allowed |
|---|---|---|
| L0 | Observe | Read only |
| L1 | Analyze | Summarize, classify, prioritize |
| L2 | Draft | Create drafts, proposals, content, reports |
| L3 | Internal Execute | Write internal queues, reports, proof logs |
| L4 | Repo Execute | Branches, draft PRs, tests, safe patches |
| L5 | External Execute | Send, publish, merge, charge, production change — blocked unless explicitly approved |

## Execution order

### P0 — Production Trust

Goal: stabilize trust before growth.

Required work:

- Verify Railway config does not fight Dockerfile/start script.
- Keep `/healthz` as canonical health endpoint.
- Keep CI, production smoke, OpenSSF, TestSprite, and no-secret checks visible.
- Do not deploy or mutate production directly from autonomous flows.

### P1 — Company OS Foundation

Required modules:

```txt
dealix/company_os/
  company_brain.py
  client_profile.py
  offer_memory.py
  persona_memory.py
  objection_memory.py
  restrictions.py
  daily_planner.py
  report_generator.py

dealix/opportunity_graph/
  company.py
  contact.py
  signal.py
  opportunity.py
  source.py
  scoring.py
  entity_resolution.py
  graph_store.py

dealix/execution/
  action_queue.py
  approval_center.py
  autonomy_levels.py
  execution_policy.py
  audit_log.py

dealix/proof/
  proof_ledger.py
  roi_tracker.py
  weekly_proof_pack.py
  evidence_linker.py
```

### P2 — Autonomous Growth & Strategy Execution

Required modules:

```txt
dealix/strategy_execution/
  strategy_registry.py
  execution_planner.py
  orchestrator.py
  action_queue.py
  safety_gate.py
  proof_logger.py
  learning_loop.py
  model_router.py
  growth_engine.py
  viral_loops.py
```

Required strategies:

```txt
technical_trust.yaml
revenue_sprint.yaml
saudi_market_access.yaml
foreign_company_targeting.yaml
local_b2b_growth.yaml
b2g_readiness.yaml
content_factory.yaml
proof_pack.yaml
founder_daily_ops.yaml
partner_growth.yaml
referral_loop.yaml
seo_market_reports.yaml
```

### P3 — Self-Improvement Layer

Required modules:

```txt
dealix/self_improvement/
  event_collector.py
  root_cause_analyzer.py
  learning_memory.py
  experiment_engine.py
  playbook_optimizer.py
  negotiation_reviewer.py
  data_quality_reviewer.py
  technical_repair_planner.py
  commercial_repair_planner.py
  improvement_queue.py
  autonomy_governor.py
  self_improvement_reporter.py
```

Daily self-improvement must detect:

- no reply
- rejected draft
- rejected proposal
- poor target quality
- duplicate or bad data
- repeated objection
- missed follow-up
- CI failure
- production health issue
- support recurrence
- unclear offer
- weak CTA
- risky claim

## Connector operating board

### GitHub

Use GitHub as the source of truth for implementation:

- Master execution issues
- Safe branches
- Draft PRs
- CI / smoke / security failures
- Verification logs
- Production trust blockers

### Slack

Use Slack as an internal command center only:

- Daily internal brief
- Approval reminder
- Proof Pack summary
- Connector status
- No client-facing outbound automation

### Airtable / Sheets

Use as the operating board with these tables:

- Strategy Backlog
- Action Queue
- Approval Queue
- Opportunity Graph
- Proof Ledger
- Self Improvement
- Contacts Radar

### Google Contacts

Use only for known/warm contacts. Do not infer consent from existence in Contacts. If no Dealix contacts exist, create a Contacts Radar backlog item rather than sending outreach.

## Daily command output

Every daily run must produce:

```txt
reports/company_os/daily/YYYY-MM-DD.md
reports/company_os/drafts/YYYY-MM-DD.json
reports/company_os/approvals/YYYY-MM-DD.json
reports/company_os/proof/YYYY-MM-DD.json
reports/self_improvement/daily/YYYY-MM-DD.md
reports/autonomous_growth/content/YYYY-MM-DD_content_queue.md
```

## Verification commands

Prefer these commands when available:

```bash
python scripts/commercial/run_company_os_daily.py --client dealix --mode draft-only --limit 50
python scripts/commercial/run_autonomous_growth_daily.py --autonomy-level 3 --mode draft-only --limit 50
python scripts/commercial/run_self_improvement_daily.py --client dealix --mode draft-only
python scripts/commercial/run_weekly_proof_pack.py --client dealix --mode draft-only
python scripts/commercial/verify_company_os_foundation.py
python scripts/commercial/verify_autonomous_growth.py
python scripts/commercial/verify_self_improvement.py
```

## 14-day internal proof target

Do not fake these numbers. Track templates only until evidence exists.

- 500 companies observed
- 100 qualified companies
- 50 draft messages
- 20 founder approvals
- 10 manual or approved sends
- 5 replies
- 2 meetings
- 1 paid offer or pilot
- 1 proof pack
- 20 learning events
- 5 internal improvements

## First commercial offers

Use this offer ladder:

1. Saudi Opportunity Snapshot
2. Revenue Proof Sprint
3. Revenue Command Pilot
4. Saudi Market Access Sprint
5. Revenue Command Room Retainer
6. AI Company OS Setup
7. B2G Readiness Sprint
8. Partner / Distributor Desk

## Definition of Done

This spine is implemented only when:

- Daily Company OS runner generates report, drafts, approvals, and proof log.
- Autonomous Growth runner generates action queue, approval queue, proof log, and content queue.
- Self-Improvement runner generates failures, improvements, and experiments.
- Verification scripts pass or document blockers honestly.
- No live outbound is enabled.
- No production mutation is enabled.
- No fake proof or guaranteed claims exist.
- A draft PR summarizes safety guarantees and remaining blockers.
