import json
from pathlib import Path

items_path=Path('data/proof/proof_items.json')
items=json.loads(items_path.read_text(encoding='utf-8')) if items_path.exists() else []
print('Proof Vault Index')
print(f'Total proof items: {len(items)}')
print(f'Marketing allowed: {sum(1 for x in items if x.get("marketing_allowed"))}')
print(f'Sensitive items: {sum(1 for x in items if x.get("sensitive"))}')
