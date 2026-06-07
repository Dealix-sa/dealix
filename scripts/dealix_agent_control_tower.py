import json
from pathlib import Path
q=json.loads(Path('data/agents/task_queue.json').read_text(encoding='utf-8') or '[]') if Path('data/agents/task_queue.json').exists() else []
runs=[]
if Path('data/agents/agent_runs.jsonl').exists():
    for line in Path('data/agents/agent_runs.jsonl').read_text(encoding='utf-8').splitlines():
        if line.strip(): runs.append(json.loads(line))
approvals=[]
if Path('data/agents/approvals.jsonl').exists():
    for line in Path('data/agents/approvals.jsonl').read_text(encoding='utf-8').splitlines():
        if line.strip(): approvals.append(json.loads(line))
print('Dealix Agent Control Tower')
print('Queued tasks:', len([x for x in q if x.get('status')=='queued']))
print('Agent runs:', len(runs))
print('Need approval:', len([x for x in runs if x.get('approval_required')]))
print('Approvals logged:', len(approvals))
print('Next action: review out/agents outputs, approve/reject, then log CRM interaction manually.')
