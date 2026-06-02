#!/usr/bin/env python3
"""Proof Pack Factory (Revenue Execution OS) — evidence packs (L1 internal draft).

Builds leakage→quick-win→measurement packs for contacted+ prospects. Public/case
-study use requires L4 + explicit consent (enforced). No invented numbers.

Usage:
    python scripts/generate_proof_pack.py
    python scripts/generate_proof_pack.py --promote proof_xxx --level 4 --consent
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402
from dealix.distribution import proof_packs  # noqa: E402


def main(argv: list[str] | None = None) -> int:
    ensure_stdout_utf8()
    p = argparse.ArgumentParser(description="Generate proof-pack drafts.")
    p.add_argument("--prospects", type=Path, default=None)
    p.add_argument("--promote", metavar="PROOF_ID", default=None)
    p.add_argument("--level", type=int, default=4)
    p.add_argument("--consent", action="store_true", help="Explicit public-use consent (L4+).")
    p.add_argument("--json", action="store_true")
    args = p.parse_args(argv)

    if args.promote:
        rec = proof_packs.promote_to_public(
            args.promote, level=args.level, consent_public=args.consent
        )
        print(
            f"PROMOTED: {args.promote} -> L{args.level} ({rec['status'] if rec else 'NOT FOUND'})"
        )

    summary = proof_packs.run_generation(args.prospects)
    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        print("PROOF_PACK_FACTORY:")
        print(f"  new proof packs        : {summary['new_proof_packs']}")
        print(f"  default evidence level : L{summary['default_evidence_level']}")
        for pid in summary["ids"]:
            print(f"    - {pid}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except Exception as exc:
        print(f"PROOF_PACK_FACTORY: FAIL — {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
