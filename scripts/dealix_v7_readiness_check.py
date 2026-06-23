from pathlib import Path

required = [
 'agents/AGENT_OPERATING_SYSTEM_AR.md',
 'agents/HUMAN_APPROVAL_GATE_AR.md',
 'data/agents/agent_registry.json',
 'data/agents/task_queue.json',
 'prompts/contracts/OUTREACH_DRAFT_AGENT.md',
 'scripts/dealix_agent_task_queue.py',
 'scripts/dealix_agent_router.py',
 'scripts/dealix_agent_evaluator.py',
 'scripts/dealix_agent_control_tower.py',
 '.github/workflows/dealix-v7-agent-readiness.yml',
]
missing=[p for p in required if not Path(p).exists()]
if missing:
    print('Missing V7 files:')
    print('\n'.join(missing))
    raise SystemExit(1)
print('OK: Dealix V7 AI agent operations files are present')
