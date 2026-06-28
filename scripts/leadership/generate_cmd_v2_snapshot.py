#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.leadership.cmd_v2 import run_cmd_v2

payload = run_cmd_v2()
out = Path('apps/web/lib/cmd-v2-snapshot.ts')
out.parent.mkdir(parents=True, exist_ok=True)
content = 'export const cmdV2Snapshot = ' + json.dumps(payload, ensure_ascii=False, indent=2) + ' as const;\n'
out.write_text(content, encoding='utf-8')
print('CMD_V2_SNAPSHOT_READY=1')
print('SNAPSHOT=apps/web/lib/cmd-v2-snapshot.ts')
