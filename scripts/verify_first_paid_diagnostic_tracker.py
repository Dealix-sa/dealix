#!/usr/bin/env python3
"""First paid Diagnostic — evidence CSV verdict."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--json", action="store_true")
    args = p.parse_args()
    blob = analyze_first_paid_diagnostic()
    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print("== first_paid_diagnostic_tracker ==")
        print(f"  verdict: {blob.get('verdict')}")
        print(f"  note: {blob.get('note_ar')}")
        print(f"  pipeline: data/founder_commercial/first_paid_pipeline.yaml")
        print(f"  DoD: docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md")
    print(f"FIRST_PAID_DIAGNOSTIC_VERDICT={blob.get('verdict')}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
