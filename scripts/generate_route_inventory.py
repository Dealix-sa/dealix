#!/usr/bin/env python3
"""Regenerate the golden route inventory.

Run this only when a route change is intentional, then include the resulting
diff to ``tests/golden/route_inventory.json`` in the pull request body as an
explicit added/removed list.

    python3 scripts/generate_route_inventory.py           # write
    python3 scripts/generate_route_inventory.py --check   # verify only
"""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

# Importing api.main boots the app factory, which refuses to start on
# placeholder secrets when APP_ENV=production. Pin a test environment so this
# tool never depends on real credentials.
os.environ.setdefault("APP_ENV", "test")
os.environ.setdefault("ENVIRONMENT", "test")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:///./dealix_local_test.db")
os.environ.setdefault("APP_SECRET_KEY", "local-test-secret-change-me")
os.environ.setdefault("JWT_SECRET_KEY", "local-jwt-secret-change-me")
os.environ.setdefault("OUTBOUND_MODE", "draft_only")

from tests.support.route_inventory import (
    build_inventory,
    diff_inventories,
    load_golden,
    write_golden,
)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit non-zero if the golden file is stale; do not write.",
    )
    args = parser.parse_args()

    from api.main import app

    current = build_inventory(app)

    if args.check:
        golden = load_golden()
        added, removed = diff_inventories(golden, current)
        if added or removed:
            print("ROUTE_INVENTORY=STALE")
            for item in added:
                print(f"  + {item}")
            for item in removed:
                print(f"  - {item}")
            return 1
        print("ROUTE_INVENTORY=CURRENT")
        return 0

    write_golden(current)
    print(
        f"Wrote {current['route_count']} paths / "
        f"{current['path_method_count']} path+method pairs "
        f"({current['shadowed_count']} shadowed)."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
