#!/usr/bin/env python3
"""Verify the Market Production OS: schemas parse, seeds validate, gates hold.

Prints ``DEALIX_MARKET_PRODUCTION_OS_VERDICT=PASS|FAIL`` and exits non-zero on
failure so it can gate CI. No network, no sending, no charging.

Usage:
    python3 scripts/verify_market_production_os.py
"""

from __future__ import annotations

import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.marketing_factory import market_production_os as mpo  # noqa: E402


def main() -> int:
    failures: list[str] = []

    # 1. Draft production target sums correctly.
    if mpo.draft_mix_total() != mpo.DRAFTS_PER_DAY:
        failures.append(f"draft mix sums to {mpo.draft_mix_total()}, expected {mpo.DRAFTS_PER_DAY}")

    # 2. Sending ramp never lets week 0 exceed the warm-up cap.
    if mpo.sending_ramp_cap(0) > 20:
        failures.append("week 0 sending cap exceeds 20")
    if mpo.sending_ramp_cap(4, {"bounce_rate": 0.05}) != 0:
        failures.append("unhealthy domain not paused")

    # 3. All seed datasets validate against their schemas.
    results = mpo.validate_all()
    for errors in results.values():
        failures.extend(errors)

    summary = mpo.summary()
    print(json.dumps(summary, ensure_ascii=False, indent=2))

    verdict = "PASS" if not failures else "FAIL"
    if failures:
        print("\nFailures:")
        for f in failures:
            print(f"  - {f}")
    print(f"\nDEALIX_MARKET_PRODUCTION_OS_VERDICT={verdict}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
