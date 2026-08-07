#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from app.leadership.iv4 import run_iv4, verify_payload

payload = run_iv4()
errors = verify_payload(payload)
print('IV4_READY=' + ('0' if errors else '1'))
for key in sorted(payload['summary']):
    print(str(key).upper() + '=' + str(payload['summary'][key]))
raise SystemExit(1 if errors else 0)
