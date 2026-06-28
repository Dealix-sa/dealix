import json
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT))
from app.leadership.x5 import run_x5
payload = run_x5()
out = Path('apps/web/lib/x5-snapshot.ts')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text('export const x5Snapshot = ' + json.dumps(payload, indent=2) + ' as const;\n', encoding='utf-8')
print('X5_SNAPSHOT_READY=1')
