import json
from pathlib import Path
open_tasks=0
if Path('data/founder/founder_tasks.json').exists():
    tasks=json.loads(Path('data/founder/founder_tasks.json').read_text(encoding='utf-8'))
    open_tasks=sum(1 for t in tasks if t.get('status')=='open')
logs=0
if Path('data/founder/execution_log.jsonl').exists():
    logs=len([l for l in Path('data/founder/execution_log.jsonl').read_text(encoding='utf-8').splitlines() if l.strip()])
artifacts=len(list(Path('out/founder/daily_artifacts').glob('*.md'))) if Path('out/founder/daily_artifacts').exists() else 0
brief=Path('out/founder/daily_command_brief.md').exists()
print('# Dealix Founder Autopilot Dashboard')
print(f'Open founder tasks: {open_tasks}')
print(f'Execution log entries: {logs}')
print(f'Daily artifacts: {artifacts}')
print(f'Command brief ready: {brief}')
print('Next action: review command brief, execute top revenue task, then log outcome.')
