#!/usr/bin/env python3
"""Generate Message Performance Report."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Message Performance Report").parse_args()
    ws = workspace_root()
    rows = read_csv_rows(ws / "growth" / "message_performance.csv")
    rows.sort(key=lambda r: float(r.get("reply_rate", 0) or 0), reverse=True)
    body = (
        "# Message Performance\n\n"
        + md_table(
            ["message_id", "angle", "reply_rate", "convert_rate"],
            [[r.get("message_id",""), r.get("angle",""), r.get("reply_rate",""), r.get("convert_rate","")] for r in rows],
        )
    )
    out = write_doc("docs/intelligence/MESSAGE_PERFORMANCE.md", body, [ws / "growth" / "message_performance.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
