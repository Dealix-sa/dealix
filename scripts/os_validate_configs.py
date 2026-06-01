#!/usr/bin/env python3
"""CLI: validate all Dealix OS config files.

Exit 0 if all files are valid, exit 1 if any fail.
"""
from __future__ import annotations

import sys
from pathlib import Path

# Ensure repo root is importable from any working directory
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from os_runtime.validators import validate_configs, validate_all


def main() -> int:
    results = validate_configs()
    all_ok = True
    for filename, status in results.items():
        tag = "OK" if status == "OK" else "FAIL"
        print(f"[{tag}] {filename}: {status}")
        if status != "OK":
            all_ok = False

    if all_ok:
        print("\nAll OS config files are valid.")
        return 0
    else:
        print("\nOne or more OS config files failed validation.")
        return 1


if __name__ == "__main__":
    sys.exit(main())
