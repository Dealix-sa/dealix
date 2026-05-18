#!/usr/bin/env python3
"""Write executive_day JSON + markdown brief."""

from __future__ import annotations

import argparse
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.founder_rise_bundle import (  # noqa: E402
    build_executive_day_bundle,
    write_executive_day_artifacts,
)
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--api-base", default=os.getenv("DEALIX_API_BASE", "https://api.dealix.me"))
    p.add_argument("--skip-live", action="store_true")
    args = p.parse_args()

    bundle = build_executive_day_bundle(api_base=args.api_base, skip_live=args.skip_live)
    paths = write_executive_day_artifacts(bundle)
    print(f"wrote: {paths['markdown']}")
    print(f"wrote: {paths['json']}")
    print(f"FOUNDER_EXECUTIVE_DAY_VERDICT={bundle['verdict']}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
