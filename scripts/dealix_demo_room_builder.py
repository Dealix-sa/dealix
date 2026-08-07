import argparse
import datetime
import json
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('--vertical', default='training')
ap.add_argument('--account', required=True)
args=ap.parse_args()
scenarios=json.loads(Path('demos/demo_scenarios.json').read_text(encoding='utf-8')) if Path('demos/demo_scenarios.json').exists() else {}
s=scenarios.get(args.vertical, {'pain':'متابعة غير موحدة','primary_kpi':'qualified conversations'})
leads=[{'name':f'Lead {i+1}','pain':s['pain'],'score':80-i*7,'next_action':'مراجعة المسودة وتحديد موعد diagnostic'} for i in range(3)]
demo={'account':args.account,'vertical':args.vertical,'scenario':s,'demo_leads':leads,'created_at':datetime.datetime.utcnow().isoformat()+'Z'}
out=Path('out/demo_rooms'); out.mkdir(parents=True, exist_ok=True)
fn=out/(args.account.replace(' ','_')+'_demo_room.json')
fn.write_text(json.dumps(demo,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Wrote {fn}')
