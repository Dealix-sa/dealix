import argparse
import datetime
import json
from pathlib import Path

p=argparse.ArgumentParser(); p.add_argument('--partner',required=True); p.add_argument('--lead',required=True); p.add_argument('--vertical',default='unknown'); a=p.parse_args(); path=Path('data/referrals/referral_partners.json'); path.parent.mkdir(parents=True,exist_ok=True); obj=json.loads(path.read_text(encoding='utf-8')) if path.exists() else {'partners':[]}; obj['partners'].append({'partner':a.partner,'lead':a.lead,'vertical':a.vertical,'created_at':datetime.datetime.utcnow().isoformat()+'Z','status':'new'}); path.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8'); print('Logged referral')
