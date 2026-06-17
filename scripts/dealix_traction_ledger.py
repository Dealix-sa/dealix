import argparse, json, datetime
from pathlib import Path
p=Path('data/traction/traction_events.jsonl'); p.parent.mkdir(parents=True, exist_ok=True)
parser=argparse.ArgumentParser()
parser.add_argument('--event-type', default='lead')
parser.add_argument('--account', default='Unknown Account')
parser.add_argument('--value-sar', type=float, default=0)
parser.add_argument('--note', default='')
a=parser.parse_args()
row={'ts':datetime.datetime.utcnow().isoformat()+'Z','event_type':a.event_type,'account':a.account,'value_sar':a.value_sar,'note':a.note}
with p.open('a',encoding='utf-8') as f: f.write(json.dumps(row,ensure_ascii=False)+'\n')
print(f"Logged traction event: {a.event_type} / {a.account} / SAR {a.value_sar}")
