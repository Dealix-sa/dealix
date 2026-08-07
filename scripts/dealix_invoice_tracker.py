import argparse
import datetime
import json
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--client',required=True)
parser.add_argument('--amount',type=float,required=True)
parser.add_argument('--status',default='sent')
parser.add_argument('--currency',default='SAR')
args=parser.parse_args()
p=Path('data/revenue/invoices.jsonl'); p.parent.mkdir(parents=True,exist_ok=True)
event={'ts':datetime.datetime.utcnow().isoformat()+'Z','client':args.client,'amount':args.amount,'currency':args.currency,'status':args.status}
with p.open('a',encoding='utf-8') as f: f.write(json.dumps(event,ensure_ascii=False)+'\n')
print(f"Invoice logged: {args.client} {args.amount} {args.currency} {args.status}")
