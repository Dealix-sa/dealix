#!/usr/bin/env python3
from pathlib import Path
import sys
ROOT = Path(__file__).resolve().parents[2]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))
from app.commercial.channel_control_plane import run_channel_control_plane
payload = run_channel_control_plane()
summary = payload['summary']
print('COMMERCIAL_CHANNEL_CONTROL_READY=1')
print(f"ACTIONS={summary['actions']}")
print(f"APPROVAL_CARDS={summary['approval_cards']}")
print(f"LIVE_SENDS={summary['live_sends']}")
print('REPORT_JSON=reports/commercial/channel_control/latest.json')
