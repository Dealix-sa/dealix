#!/usr/bin/env python3
"""Generate Offer-Market-Fit Report."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Offer-Market-Fit Report").parse_args()
    ws = workspace_root()
    rows = read_csv_rows(ws / "market_attack" / "offer_market_fit_tests.csv")
    body = (
        "# Offer-Market-Fit Report\n\n"
        + md_table(["test_id", "offer", "result"], [[r.get("test_id",""), r.get("offer",""), r.get("result","")] for r in rows])
    )
    out = write_doc("docs/market_attack/OFFER_MARKET_FIT.md", body, [ws / "market_attack" / "offer_market_fit_tests.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
