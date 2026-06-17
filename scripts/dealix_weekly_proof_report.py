import argparse,re,json
from pathlib import Path
parser=argparse.ArgumentParser(); parser.add_argument('--client',required=True); args=parser.parse_args()
slug=re.sub(r'[^\w\u0600-\u06FF-]+','_',args.client).strip('_')
out=Path('out/proof_reports'); out.mkdir(parents=True, exist_ok=True)
invoice_lines=Path('data/revenue/invoices.jsonl').read_text(encoding='utf-8').splitlines() if Path('data/revenue/invoices.jsonl').exists() else []
accept_lines=Path('data/revenue/client_acceptance.jsonl').read_text(encoding='utf-8').splitlines() if Path('data/revenue/client_acceptance.jsonl').exists() else []
inv=[json.loads(x) for x in invoice_lines if x.strip() and args.client in x]
acc=[json.loads(x) for x in accept_lines if x.strip() and args.client in x]
path=out/f'{slug}_weekly_proof_report.md'
path.write_text(f"""# Weekly Proof Report — {args.client}\n\n## Summary\n- Invoices logged: {len(inv)}\n- Accepted milestones: {len(acc)}\n\n## Delivered this week\n- Workflow review.\n- Next action plan.\n- Proof notes.\n\n## Client decisions needed\n- Approve retainer continuation or define next pilot workflow.\n""",encoding='utf-8')
print(f'Wrote {path}')
