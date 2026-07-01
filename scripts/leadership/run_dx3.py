#!/usr/bin/env python3
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from app.leadership.dx3 import run_dx3, verify_payload

payload = run_dx3()
errors = verify_payload(payload)
print('DX3_READY=' + ('0' if errors else '1'))
for key, value in payload['summary'].items():
    print(f'{key.upper()}={value}')
raise SystemExit(1 if errors else 0)
