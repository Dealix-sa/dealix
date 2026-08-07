import argparse
import re
from pathlib import Path

parser=argparse.ArgumentParser(); parser.add_argument('--client',required=True); parser.add_argument('--monthly-price',default='4500'); args=parser.parse_args()
slug=re.sub(r'[^\w\u0600-\u06FF-]+','_',args.client).strip('_')
out=Path('out/retainer_plans'); out.mkdir(parents=True,exist_ok=True)
path=out/f'{slug}_retainer_plan.md'
path.write_text(f"""# Retainer Conversion Plan — {args.client}\n\nSuggested monthly price: SAR {args.monthly_price}\n\n## Narrative\nThe pilot identified and improved one workflow. The retainer keeps the workflow alive weekly and expands to the next bottleneck.\n\n## Monthly scope\n- Weekly pipeline review.\n- Follow-up system maintenance.\n- KPI report.\n- One improvement sprint per month.\n""",encoding='utf-8')
print(f'Wrote {path}')
