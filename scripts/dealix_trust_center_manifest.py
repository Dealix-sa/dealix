import json
from pathlib import Path
controls=json.loads(Path('data/trust/trust_controls.json').read_text(encoding='utf-8'))
out=Path('out/trust/trust_center_manifest.md'); out.parent.mkdir(parents=True, exist_ok=True)
lines=['# Trust Center Manifest']+[f'- {k}: {v}' for k,v in controls.items()]
out.write_text('\n'.join(lines), encoding='utf-8')
print(out.read_text(encoding='utf-8'))
