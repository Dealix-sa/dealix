#!/usr/bin/env python3
"""Report on optional router imports — warn by default, fail only with --strict.

Background: api/main.py imports value_os, data_os, agent_os defensively
so a single broken router doesn't crash the entire app. The failure is
logged but boot continues.

This script imports api.main (triggering the same defensive imports)
and then inspects `_OPTIONAL_ROUTER_ERRORS`.

Usage:
    python scripts/check_optional_routers.py            # always exits 0
                                                          (prints warning if any failed)
    python scripts/check_optional_routers.py --strict   # exits 1 on any failure
    DEALIX_STRICT_OPTIONAL_ROUTERS=1 python ...         # same as --strict

Exit codes:
    0 — default: always 0 (informational). Strict: all imported cleanly.
    1 — strict mode only: one or more routers failed.
    2 — could not import api.main at all (deeper problem).
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    strict = "--strict" in argv or os.getenv(
        "DEALIX_STRICT_OPTIONAL_ROUTERS", ""
    ).lower() in ("1", "true", "yes")

    try:
        from api.main import _OPTIONAL_ROUTER_ERRORS
    except Exception as exc:
        print(f"FATAL: could not import api.main itself: {type(exc).__name__}: {exc}")
        return 2

    if not _OPTIONAL_ROUTER_ERRORS:
        print("OK: all optional routers (value_os, data_os, agent_os) imported cleanly")
        return 0

    print(
        f"WARN: {len(_OPTIONAL_ROUTER_ERRORS)} optional router(s) failed to import:\n"
    )
    for name, err in _OPTIONAL_ROUTER_ERRORS.items():
        print(f"── {name} ──")
        for line in err.splitlines()[:20]:
            print(f"  {line}")
        print()
    print(
        "Optional routers are defensive imports — app boots without them.\n"
        "To gate CI on these: pass --strict or set DEALIX_STRICT_OPTIONAL_ROUTERS=1."
    )
    return 1 if strict else 0


if __name__ == "__main__":
    sys.exit(main())
