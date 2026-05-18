#!/usr/bin/env python3
"""First paid Diagnostic -> Proof Pack governed path (DoD + tracker)."""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.first_paid_tracker import analyze_first_paid_diagnostic  # noqa: E402
from dealix.commercial_ops.paths import REPO_ROOT  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()

DOD = REPO_ROOT / "docs/commercial/operations/FIRST_PAID_DIAGNOSTIC_DOD_AR.md"
PAYMENT_SOP = REPO_ROOT / "docs/ops/MANUAL_PAYMENT_SOP.md"
PROOF_TEMPLATE = REPO_ROOT / "docs/delivery/PROOF_PACK_TEMPLATE.md"


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--company", help="Generate client pack draft (no send)")
    p.add_argument("--lead-id", help="War Room lead id")
    args = p.parse_args()

    blob = analyze_first_paid_diagnostic()
    print("== first_paid_proof_pack_path ==")
    print(f"  verdict: {blob['verdict']}")
    print(f"  payment_received (real): {blob['payment_received_real']}")
    print(f"  proof_pack_delivered (real): {blob['proof_pack_delivered_real']}")
    print("")
    print("== checklist ==")
    print(f"  - DoD: {DOD.relative_to(REPO_ROOT)}")
    print(f"  - SOP: {PAYMENT_SOP.relative_to(REPO_ROOT)}")
    print(f"  - Proof template: {PROOF_TEMPLATE.relative_to(REPO_ROOT)}")
    print("  - evidence: invoice_sent -> payment_received -> proof_pack_delivered")
    print("  - KPI: dealix/transformation/kpi_founder_commercial_import.yaml")

    if args.company or args.lead_id:
        from dealix.commercial_ops.client_pack import build_client_pack

        pack = build_client_pack(
            company=args.company,
            lead_id=args.lead_id,
            write_disk=True,
        )
        print(f"  client_pack: {pack.get('output_dir', pack)}")

    print(f"\nFIRST_PAID_PROOF_PACK_PATH_VERDICT={blob['verdict']}")
    if not blob["first_close_ready"]:
        print("FOUNDER_ACTION: close one real Diagnostic per DoD before scale motions")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
