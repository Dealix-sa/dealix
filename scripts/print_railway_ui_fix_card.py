#!/usr/bin/env python3
"""Print Arabic Railway UI fix card (matches common dashboard drift)."""

from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.railway_production import (  # noqa: E402
    CANONICAL_PREDEPLOY,
    CANONICAL_START,
    parse_railway_ui_drift_hint,
    parse_railway_ui_predeploy_drift,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

DEFAULT_BAD_START = "./start.sh"
DEFAULT_BAD_PREDEPLOY = 'echo "no migration needed"'


def main() -> int:
    ensure_stdout_utf8()
    ui_start = os.getenv("RAILWAY_UI_START_COMMAND", DEFAULT_BAD_START)
    ui_pre = os.getenv("RAILWAY_UI_PREDEPLOY", DEFAULT_BAD_PREDEPLOY)

    print("== بطاقة إصلاح Railway (api.dealix.me) ==")
    print()
    print("| الإعداد | عندك (خطأ شائع) | المطلوب |")
    print("|---------|-----------------|----------|")
    print(f"| Pre-deploy | `{ui_pre}` | فارغ أو `{CANONICAL_PREDEPLOY}` |")
    print(f"| Start command | `{ui_start}` | فارغ أو `{CANONICAL_START}` |")
    print("| Target port | 8080 | صحيح — التطبيق يقرأ $PORT |")
    print()
    print("بعد التعديل: Redeploy من main ثم:")
    print("  curl -fsS https://api.dealix.me/healthz")
    print()

    start_hint = parse_railway_ui_drift_hint(ui_start)
    pre_hint = parse_railway_ui_predeploy_drift(ui_pre)
    if start_hint or pre_hint:
        print("FOUNDER_RAILWAY_UI_ACTION=REQUIRED")
        if start_hint:
            print(f"  START: {start_hint}")
        if pre_hint:
            print(f"  PREDEPLOY: {pre_hint}")
    else:
        print("FOUNDER_RAILWAY_UI_ACTION=OK")

    print()
    print("== verify_railway_production_config (محاكاة) ==")
    cmd = [
        sys.executable,
        str(ROOT / "scripts/verify_railway_production_config.py"),
        "--skip-live",
        "--ui-start-command",
        ui_start,
        "--ui-predeploy",
        ui_pre,
    ]
    return subprocess.call(cmd)


if __name__ == "__main__":
    raise SystemExit(main())
