import argparse, json, time
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--tenant',required=True); p.add_argument('--plan',default='starter_managed')
a=p.parse_args()
base=Path('data/tenants'); base.mkdir(parents=True, exist_ok=True)
tenant_id='tenant_'+str(abs(hash(a.tenant)))[:10]
obj={'id':tenant_id,'name':a.tenant,'plan':a.plan,'status':'active','created_at':time.strftime('%Y-%m-%dT%H:%M:%SZ')}
(base/f'{tenant_id}.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Created tenant {tenant_id}: {a.tenant}')
