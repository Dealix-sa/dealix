import json
from pathlib import Path
items=json.loads(Path('data/automation/automation_backlog.json').read_text(encoding='utf-8'))
ranked=sorted(items,key=lambda x:(x['priority'], -x.get('weekly_hours_saved',0)))
print('# Automation Backlog')
for i in ranked:
    print(f"- {i['id']} | {i['priority']} | saves {i['weekly_hours_saved']}h/week | {i['title']} | gate={i['safety_gate']}")
