#!/usr/bin/env python3
from pathlib import Path
import json
import sys
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from app.commercial.channel_control_plane import run_channel_control_plane, verify_channel_control
path = Path('reports/commercial/channel_control/latest.json')
payload = json.loads(path.read_text(encoding='utf-8')) if path.exists() else run_channel_control_plane()
failures = verify_channel_control(payload)
print('COMMERCIAL_CHANNEL_CONTROL_VERIFY=' + ('FAIL' if failures else 'PASS'))
for failure in failures:
    print('FAIL: ' + failure)
raise SystemExit(1 if failures else 0)
