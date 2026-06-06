#!/usr/bin/env python3
"""Verify the canonical Dealix modules are present and importable.

Checks each module under ``auto_client_acquisition/``: first that the package
directory exists on disk, then whether it imports cleanly. A module that is
present on disk but fails to import is reported as PRESENT (not PASS) so the
verifier surfaces import problems without crashing. Prints a status table and
returns a non-zero exit code when any module is missing from disk.
"""

from __future__ import annotations

import argparse
import importlib
import json
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

CANONICAL_MODULES: list[str] = [
    "data_os",
    "governance_os",
    "proof_os",
    "value_os",
    "capital_os",
    "adoption_os",
    "sales_os",
    "client_os",
    "friction_log",
]

PKG = "auto_client_acquisition"


def _check_module(name: str) -> dict[str, Any]:
    present = (ROOT / PKG / name).is_dir()
    importable = False
    error = ""
    if present:
        try:
            importlib.import_module(f"{PKG}.{name}")
            importable = True
        except Exception as exc:  # pragma: no cover - environment dependent
            error = f"{type(exc).__name__}: {exc}"
    if not present:
        status = "MISSING"
    elif importable:
        status = "PASS"
    else:
        status = "PRESENT"
    return {
        "module": name,
        "present": present,
        "importable": importable,
        "status": status,
        "error": error,
    }


def check_modules() -> dict[str, Any]:
    """Check every canonical module. Returns a structured result."""
    items = [_check_module(name) for name in CANONICAL_MODULES]
    missing = [i["module"] for i in items if not i["present"]]
    verdict = "PASS" if not missing else "FAIL"
    return {"items": items, "missing": missing, "verdict": verdict}


def _print_table(result: dict[str, Any]) -> None:
    print("== Dealix Module Status ==")
    for item in result["items"]:
        suffix = f" ({item['error']})" if item["error"] else ""
        print(f"  [{item['status']}] {item['module']}{suffix}")
    if result["missing"]:
        print(f"Missing on disk: {', '.join(result['missing'])}")
    print(f"Verdict: {result['verdict']}")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="emit JSON")
    args = parser.parse_args(argv)

    result = check_modules()
    if args.json:
        print(json.dumps(result, ensure_ascii=False, indent=2))
    else:
        _print_table(result)
    return 0 if result["verdict"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
