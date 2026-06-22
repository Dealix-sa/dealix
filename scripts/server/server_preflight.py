#!/usr/bin/env python3
"""
Server preflight checks before deploy or daily run.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[2]
VENV_PYTHON = REPO_ROOT / ".venv" / "Scripts" / "python.exe"
if VENV_PYTHON.exists():
    PYTHON = str(VENV_PYTHON)
else:
    VENV_PYTHON = REPO_ROOT / ".venv" / "bin" / "python3"
    PYTHON = str(VENV_PYTHON) if VENV_PYTHON.exists() else sys.executable

REQUIRED_ENV = [
    ("APP_SECRET_KEY", "cryptographic signing"),
    ("DATABASE_URL", "PostgreSQL connection"),
]

OPTIONAL_BUT_RECOMMENDED = [
    ("REDIS_URL", "cache / queue"),
    ("MOYASAR_SECRET_KEY", "payments sandbox/live"),
    ("HUBSPOT_ACCESS_TOKEN", "CRM sync"),
]


def check_env() -> tuple[list[str], list[str]]:
    missing: list[str] = []
    present: list[str] = []
    for key, purpose in REQUIRED_ENV:
        value = os.getenv(key, "").strip()
        if not value:
            missing.append(f"{key} ({purpose})")
        else:
            present.append(f"{key} ({purpose})")
    for key, purpose in OPTIONAL_BUT_RECOMMENDED:
        value = os.getenv(key, "").strip()
        if value:
            present.append(f"{key} ({purpose}, optional)")
        else:
            present.append(f"{key} ({purpose}, optional) — not set")
    return missing, present


def check_alembic() -> tuple[bool, str]:
    try:
        result = subprocess.run(
            [PYTHON, "scripts/check_alembic_single_head.py"],
            cwd=REPO_ROOT,
            capture_output=True,
            text=True,
            timeout=60,
        )
        return result.returncode == 0, (result.stdout + result.stderr).strip()
    except Exception as exc:
        return False, str(exc)


def main() -> int:
    print("Dealix Server Preflight")
    print("=" * 60)

    missing, present = check_env()
    print("\nEnvironment variables:")
    for item in present:
        print(f"  ✅ {item}")
    for item in missing:
        print(f"  ❌ MISSING {item}")

    print("\nAlembic migration heads:")
    ok, detail = check_alembic()
    print(f"  {'✅' if ok else '❌'} {detail}")

    print("\nNo-auto-send gate:")
    result = subprocess.run(
        [PYTHON, "scripts/verify_no_auto_external_send.py"],
        cwd=REPO_ROOT,
        capture_output=True,
        text=True,
        timeout=60,
    )
    print(f"  {'✅' if result.returncode == 0 else '❌'} {result.stdout.splitlines()[-2] if result.stdout else 'check failed'}")

    overall = ok and not missing
    print("\n" + "=" * 60)
    print(f"PREFLIGHT: {'PASS' if overall else 'FAIL'}")

    out_dir = REPO_ROOT / "reports" / "server"
    out_dir.mkdir(parents=True, exist_ok=True)
    with open(out_dir / "server_preflight.md", "w", encoding="utf-8") as f:
        f.write("# Server Preflight\n\n")
        f.write(f"**Status:** {'PASS' if overall else 'FAIL'}\n\n")
        f.write("## Environment\n")
        for item in present:
            f.write(f"- [x] {item}\n")
        for item in missing:
            f.write(f"- [ ] MISSING {item}\n")
        f.write(f"\n## Alembic\n- {'[x]' if ok else '[ ]'} {detail}\n")

    return 0 if overall else 1


if __name__ == "__main__":
    sys.exit(main())
