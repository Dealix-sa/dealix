import json, datetime
from pathlib import Path
traction=Path('data/traction/traction_events.jsonl')
events=[]
if traction.exists():
    events=[json.loads(x) for x in traction.read_text(encoding='utf-8').splitlines() if x.strip()]
metrics={
 'ts':datetime.datetime.utcnow().isoformat()+'Z',
 'events':len(events),
 'leads':sum(1 for e in events if e.get('event_type')=='lead'),
 'pilots':sum(1 for e in events if e.get('event_type')=='pilot'),
 'retainers':sum(1 for e in events if e.get('event_type')=='retainer'),
 'revenue_sar':sum(float(e.get('value_sar',0)) for e in events)
}
out=Path('out/board/board_metrics.md'); out.parent.mkdir(parents=True, exist_ok=True)
out.write_text('\n'.join([f"# Board Metrics", f"Events: {metrics['events']}", f"Leads: {metrics['leads']}", f"Pilots: {metrics['pilots']}", f"Retainers: {metrics['retainers']}", f"Revenue SAR: {metrics['revenue_sar']}"]), encoding='utf-8')
print(out.read_text(encoding='utf-8'))
