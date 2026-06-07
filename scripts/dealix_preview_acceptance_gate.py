import argparse,json,datetime
from pathlib import Path
ap=argparse.ArgumentParser()
ap.add_argument('--client', required=True)
ap.add_argument('--deliverable', required=True)
ap.add_argument('--status', choices=['accepted','accepted_with_notes','needs_revision','rejected'], required=True)
ap.add_argument('--notes', default='')
args=ap.parse_args()
Path('data/revenue').mkdir(parents=True, exist_ok=True)
item={'ts':datetime.datetime.utcnow().isoformat()+'Z','client':args.client,'deliverable':args.deliverable,'status':args.status,'notes':args.notes}
with Path('data/revenue/client_acceptance.jsonl').open('a',encoding='utf-8') as f: f.write(json.dumps(item,ensure_ascii=False)+'\n')
print(f"Acceptance logged: {args.client} / {args.deliverable} / {args.status}")
