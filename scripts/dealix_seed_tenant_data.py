import argparse, json, uuid
from pathlib import Path
parser=argparse.ArgumentParser()
parser.add_argument('--tenant', required=True)
args=parser.parse_args()
out=Path('data/tenants'); out.mkdir(parents=True, exist_ok=True)
tenant_id='tenant_'+uuid.uuid4().hex[:10]
manifest={'tenant_id':tenant_id,'tenant':args.tenant,'workspace':'Revenue Ops Workspace','status':'seeded'}
path=out/f'{tenant_id}.json'
path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding='utf-8')
print(f'Wrote {path}')
