import argparse
import json
import time
import uuid
from pathlib import Path

p=argparse.ArgumentParser(); p.add_argument('--tenant-id',required=True); p.add_argument('--action',required=True); p.add_argument('--resource-type',default='system'); p.add_argument('--resource-id',default='')
a=p.parse_args(); Path('data/audit').mkdir(parents=True,exist_ok=True)
e={'id':'audit_'+uuid.uuid4().hex[:10],'tenant_id':a.tenant_id,'action':a.action,'resource_type':a.resource_type,'resource_id':a.resource_id,'created_at':time.strftime('%Y-%m-%dT%H:%M:%SZ')}
with open('data/audit/audit_events.jsonl','a',encoding='utf-8') as f: f.write(json.dumps(e,ensure_ascii=False)+'\n')
print(f'Logged audit event {e["id"]}: {a.action}')
