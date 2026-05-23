#!/usr/bin/env python3
"""Sovereign readiness worker — runs ``scripts/generate_sovereign_readiness.py``."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def main() -> int:
    script = Path(__file__).with_name("generate_sovereign_readiness.py")
    rc = subprocess.run([sys.executable, str(script)], check=False).returncode
    status = "ok" if rc == 0 else "failed"
    subprocess.run(
        [
            sys.executable,
            str(Path(__file__).with_name("update_worker_state.py")),
            "--worker", "sovereign_readiness",
            "--status", status,
        ],
        check=False,
    )
    return rc


if __name__ == "__main__":
    sys.exit(main())
