import json
from pathlib import Path
m=json.loads(Path('data/preview/launch_week_metrics.json').read_text(encoding='utf-8'))
print('# Launch Week Command Center')
for k,v in m.items():
    print(f'- {k}: {v}')
if m.get('incidents',0)>0:
    print('Next action: pause external scale and resolve incidents')
elif m.get('pilots_won',0)<1:
    print('Next action: focus founder-led outreach and discovery')
else:
    print('Next action: deliver proof reports and push retainer conversion')
