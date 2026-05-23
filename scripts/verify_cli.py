"""Verify the dealix_cli module exposes the priority commands."""

import importlib
import sys
from pathlib import Path

sys.path.insert(0, str(Path.cwd()))

REQUIRED_COMMANDS = ["daily", "weekly", "dashboard", "verify", "close_day"]

failures = []

cli_dir = Path("dealix_cli")
if not cli_dir.exists():
    failures.append("Missing module: dealix_cli/")
else:
    for name in ["__init__.py", "__main__.py", "commands.py"]:
        if not (cli_dir / name).exists():
            failures.append(f"Missing file: dealix_cli/{name}")

if not failures:
    try:
        commands = importlib.import_module("dealix_cli.commands")
    except Exception as exc:
        failures.append(f"Cannot import dealix_cli.commands: {exc}")
        commands = None

    if commands is not None:
        for cmd in REQUIRED_COMMANDS:
            if not hasattr(commands, cmd):
                failures.append(f"Missing command: dealix_cli.commands.{cmd}")

if failures:
    print("CLI verification failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: dealix_cli exposes priority commands.")
