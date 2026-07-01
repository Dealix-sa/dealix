#!/usr/bin/env python3
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from app.leadership.iv4 import run_iv4

payload = run_iv4()
out = Path('apps/web/lib/iv4-snapshot.ts')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text('export const iv4Snapshot = ' + json.dumps(payload, indent=2) + ' as const;\n', encoding='utf-8')
print('IV4_SNAPSHOT_READY=1')
