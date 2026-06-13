import argparse, json
from pathlib import Path
parser=argparse.ArgumentParser(); parser.add_argument('--account', default='Target Account')
a=parser.parse_args()
proof=json.loads(Path('data/proof/proof_items.json').read_text(encoding='utf-8'))
out=Path('out/proof')/(a.account.replace(' ','_')+'_proof_packet.md'); out.parent.mkdir(parents=True, exist_ok=True)
content = f"# Enterprise Proof Packet — {a.account}\n\n## مكونات الثقة\n- Human approval gates\n- No automated outbound\n- Proof-first claims\n- Data minimization\n\n## Proof items\n" + "\n".join([f"- {x.get('id')}: {x.get('title')}" for x in proof])
out.write_text(content, encoding='utf-8')
print(f'Wrote {out}')
