#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from app.leadership.dx3 import run_dx3

payload = run_dx3()
out = Path('apps/web/lib/dx3-snapshot.ts')
out.parent.mkdir(parents=True, exist_ok=True)
out.write_text('export const dx3Snapshot = ' + json.dumps(payload, ensure_ascii=False, indent=2) + ' as const;\n', encoding='utf-8')
print('DX3_SNAPSHOT_READY=1')
