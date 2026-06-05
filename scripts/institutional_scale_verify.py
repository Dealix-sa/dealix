#!/usr/bin/env python3
"""Verify the Dealix V10 institutional_scale OS: docs present, marker present, no forbidden claims.

Run: python scripts/institutional_scale_verify.py [--strict]
Writes JSON to outputs/v10_verification/. Exits non-zero on FAIL.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from v10_common import emit
from v10_specs import verify

KEY = "institutional_scale"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--strict", action="store_true", help="Exit 1 unless PASS (default behavior)")
    p.parse_args(argv)
    result, json_out = verify(KEY)
    return emit(result, json_out)


if __name__ == "__main__":
    raise SystemExit(main())
