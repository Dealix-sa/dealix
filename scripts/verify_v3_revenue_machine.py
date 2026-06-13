#!/usr/bin/env python3
"""Verify the Dealix V3 — Revenue Machine integration layer is wired (repo check).

Confirms every canonical artifact referenced by dealix/config/v3_revenue_machine.yaml
exists on disk — i.e. the seven Revenue-Machine layers (lead capture → CRM ledger →
offer builder → case studies → KPIs → delivery → security/doctrine) are realised by
real files, not promises. Prints DEALIX_V3_REVENUE_MACHINE_VERDICT=PASS|FAIL.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.v3_revenue_machine import (  # noqa: E402
    build_v3_revenue_machine_snapshot,
    verify_v3_revenue_machine_repo,
)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true", help="emit machine-readable JSON")
    args = p.parse_args()

    repo = verify_v3_revenue_machine_repo()
    snap = build_v3_revenue_machine_snapshot()
    verdict = "PASS" if repo["ok"] else "FAIL"

    if args.json:
        print(
            json.dumps(
                {"verdict": verdict, "repo": repo, "snapshot": snap}, ensure_ascii=False, indent=2
            )
        )
    else:
        print("== verify_v3_revenue_machine ==")
        print(f"  version: {snap.get('version')}")
        for layer in snap.get("layers", []):
            print(f"  layer: {layer['id']} — {layer['artifact_count']} artifacts")
        if repo["ok"]:
            print(
                f"  ok: {repo['layers_checked']} layers, "
                f"{repo['artifacts_checked']} canonical artifacts present"
            )
        for issue in repo.get("issues", []):
            print(f"  FAIL: {issue}")

    print(f"DEALIX_V3_REVENUE_MACHINE_VERDICT={verdict}")
    return 1 if verdict == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
