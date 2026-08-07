import argparse
import datetime
import json
from pathlib import Path

p=argparse.ArgumentParser(); p.add_argument('--partner',required=True); p.add_argument('--lead',required=True); p.add_argument('--value',type=float,default=0); a=p.parse_args()
path=Path('partners/partner_leads.json'); path.parent.mkdir(parents=True,exist_ok=True)
data=json.loads(path.read_text(encoding='utf-8')) if path.exists() and path.read_text(encoding='utf-8').strip() else []
item={'created_at':datetime.datetime.utcnow().isoformat()+'Z','partner':a.partner,'lead':a.lead,'value_sar':a.value,'status':'introduced'}
data.append(item); path.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print('Added partner referral:', item)
