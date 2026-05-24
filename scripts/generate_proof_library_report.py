#!/usr/bin/env python3
"""Generate Proof Library report."""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_lib import cli, md_table, read_csv_rows, workspace_root, write_doc  # noqa: E402


def main() -> int:
    cli("Generate Proof Library report").parse_args()
    ws = workspace_root()
    proof = read_csv_rows(ws / "proof" / "proof_library.csv")
    pending = read_csv_rows(ws / "proof" / "proof_approval_queue.csv")
    approved = [r for r in proof if r.get("approved_for_external", "").lower() in ("true", "yes", "1")]
    body = (
        "# Proof Library\n\n"
        f"## Approved for external use ({len(approved)})\n"
        + md_table(["proof_id", "customer", "result"], [[r.get("proof_id",""), r.get("customer",""), r.get("result","")] for r in approved])
        + f"\n## Pending approval ({len(pending)})\n"
        + md_table(["proof_id", "queued_at", "approval_state"], [[r.get("proof_id",""), r.get("queued_at",""), r.get("approval_state","")] for r in pending])
    )
    out = write_doc("docs/proof/PROOF_LIBRARY.md", body, [ws / "proof" / "proof_library.csv"])
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
