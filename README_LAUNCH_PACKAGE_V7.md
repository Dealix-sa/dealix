# Dealix Launch Package V7 — AI Agent Operations & Internal Automation Layer

V7 builds on V1–V6 and adds the internal agent operating layer: governed agents, task queues, prompt contracts, evaluation, approval gates, runbooks, audit logs, and human-in-the-loop automation.

## Core principle
Dealix agents do not send messages, change client data, or publish externally without an approval gate. Agents prepare, score, draft, summarize, and recommend; humans approve actions that affect clients, prospects, money, or public communication.

## Quick start
```bash
python scripts/dealix_v7_readiness_check.py
python scripts/dealix_agent_task_queue.py --seed
python scripts/dealix_agent_router.py --role crm_research_agent --task "Research شركة تدريب الرياض and produce next actions"
python scripts/dealix_agent_evaluator.py
python scripts/dealix_agent_control_tower.py
```

## What V7 adds
- Agent governance and role boundaries
- Agent task queue and routing
- Prompt contracts and output schemas
- Human approval gates
- Evaluation and QA harness
- Audit ledger and incident playbooks
- Internal automation pages for the website/admin area
