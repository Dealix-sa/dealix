#!/usr/bin/env python3
"""Verify Verifiers: every layer key in verify_everything.py has an existing
verifier script. Self-referential layer #24."""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from _common import REPO_ROOT, report  # noqa: E402

LAYER = "Verifiers"


def main() -> None:
    supreme = REPO_ROOT / "scripts" / "verify_everything.py"
    if not supreme.exists():
        report(LAYER, False, ["missing: scripts/verify_everything.py"])

    text = supreme.read_text(encoding="utf-8")
    # Match _py("...") calls
    refs = re.findall(r'_py\("([^"]+)"\)', text)
    reasons: list[str] = []
    for r in set(refs):
        if not (REPO_ROOT / "scripts" / "verifiers" / r).exists():
            reasons.append(f"verifier missing: scripts/verifiers/{r}")

    report(LAYER, not reasons, reasons)


if __name__ == "__main__":
    main()
