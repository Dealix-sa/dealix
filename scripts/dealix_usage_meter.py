import argparse, json, time, uuid
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--tenant-id',required=True); p.add_argument('--event-type',required=True); p.add_argument('--quantity',type=float,default=1)
a=p.parse_args()
allowed={'lead_created','agent_run','offer_created','proof_item_added','report_generated'}
if a.event_type not in allowed: raise SystemExit('invalid event type')
Path('data/billing').mkdir(parents=True,exist_ok=True)
e={'id':'usage_'+uuid.uuid4().hex[:10],'tenant_id':a.tenant_id,'event_type':a.event_type,'quantity':a.quantity,'created_at':time.strftime('%Y-%m-%dT%H:%M:%SZ')}
with open('data/billing/usage_events.jsonl','a',encoding='utf-8') as f: f.write(json.dumps(e,ensure_ascii=False)+'\n')
print(f'Logged usage {e["event_type"]} x{e["quantity"]} for {e["tenant_id"]}')
