import argparse,json,datetime
from pathlib import Path
p=argparse.ArgumentParser(); p.add_argument('--vertical',required=True); p.add_argument('--campaign-name',required=True); a=p.parse_args(); Path('data/campaigns').mkdir(parents=True,exist_ok=True)
obj={'name':a.campaign_name,'vertical':a.vertical,'created_at':datetime.datetime.utcnow().isoformat()+'Z','status':'draft','rules':['manual review required','no automated bulk send','document source_url']}
out=Path(f'data/campaigns/{a.campaign_name}.json'); out.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8'); print(f'Wrote {out}')
