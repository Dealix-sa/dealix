import argparse
import datetime
import json
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--client',required=True)
parser.add_argument('--milestone',required=True)
parser.add_argument('--status',default='accepted')
args=parser.parse_args()
p=Path('data/revenue/client_acceptance.jsonl'); p.parent.mkdir(parents=True,exist_ok=True)
event={'ts':datetime.datetime.utcnow().isoformat()+'Z','client':args.client,'milestone':args.milestone,'status':args.status}
with p.open('a',encoding='utf-8') as f: f.write(json.dumps(event,ensure_ascii=False)+'\n')
print(f"Acceptance logged: {args.client} / {args.milestone} / {args.status}")
