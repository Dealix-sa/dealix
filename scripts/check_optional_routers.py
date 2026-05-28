#!/usr/bin/env python3
"""Fail if any optional router failed to import at app startup.

Background: api/main.py imports value_os, data_os, agent_os defensively
(try/except wrapping the import) so a single broken router doesn't crash
the entire app. The failure is logged but boot continues.

For CI / doctor / dev — we want fast feedback when an optional router
silently fails. This script imports api.main (triggering the same
defensive imports) and then inspects `_OPTIONAL_ROUTER_ERRORS`.

Usage:
    python scripts/check_optional_routers.py        # exit 0 if all OK
    DEALIX_STRICT_OPTIONAL_ROUTERS=1 python ...     # would have already failed at boot

Exit codes:
    0 — all optional routers imported cleanly
    1 — one or more optional routers failed; traceback printed
"""

from __future__ import annotations

import sys
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO))


def main() -> int:
    try:
        from api.main import _OPTIONAL_ROUTER_ERRORS
    except Exception as exc:
        print(f"FATAL: could not import api.main itself: {type(exc).__name__}: {exc}")
        return 2

    if not _OPTIONAL_ROUTER_ERRORS:
        print("OK: all optional routers (value_os, data_os, agent_os) imported cleanly")
        return 0

    print(
        f"FAIL: {len(_OPTIONAL_ROUTER_ERRORS)} optional router(s) failed to import:\n"
    )
    for name, err in _OPTIONAL_ROUTER_ERRORS.items():
        print(f"── {name} ──")
        # err is already a formatted traceback; print first 20 lines max
        for line in err.splitlines()[:20]:
            print(f"  {line}")
        print()
    print(
        "Fix the underlying import error or document the router as deprecated.\n"
        "To fail boot in dev: export DEALIX_STRICT_OPTIONAL_ROUTERS=1"
    )
    return 1


if __name__ == "__main__":
    sys.exit(main())
