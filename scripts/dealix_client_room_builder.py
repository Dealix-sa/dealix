import argparse
import re
from pathlib import Path

parser=argparse.ArgumentParser()
parser.add_argument('--client', required=True)
parser.add_argument('--package', default='pilot')
args=parser.parse_args()
slug=re.sub(r'[^\w\u0600-\u06FF-]+','_',args.client).strip('_')
out=Path('out/client_rooms'); out.mkdir(parents=True, exist_ok=True)
path=out/f'{slug}_client_room.md'
path.write_text(f"""# Client Room — {args.client}\n\nPackage: {args.package}\n\n## Scope\n- One workflow.\n- One baseline.\n- One proof report.\n\n## Milestones\n- Intake complete.\n- Workflow map delivered.\n- Templates delivered.\n- Proof report delivered.\n- Retainer decision.\n""",encoding='utf-8')
print(f'Wrote {path}')
