#!/usr/bin/env python3
"""Bootstrap Dealix commercial launch ledgers.

This script creates local templates only. It never performs external actions or charges customers.
"""

from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
FILES = {
    "data/commercial/lead_pipeline.csv": "company_name,sector,city,website,source_url,contact_channel,pain_hypothesis,recommended_offer,stage,next_action,owner_decision,notes\n",
    "data/commercial/deal_pipeline.csv": "company_name,offer,amount_sar,stage,probability,next_step,owner,close_target,notes\n",
    "data/commercial/proposal_log.csv": "company_name,offer,amount_sar,status,created_at,next_step,notes\n",
    "data/commercial/proof_ledger.csv": "client,proof_item,before,after,evidence,next_iteration\n",
}


def main() -> int:
    for relative_path, content in FILES.items():
        path = ROOT / relative_path
        path.parent.mkdir(parents=True, exist_ok=True)
        if not path.exists():
            path.write_text(content, encoding="utf-8")
            print(f"created {relative_path}")
        else:
            print(f"exists {relative_path}")
    print("COMMERCIAL_BOOTSTRAP_READY")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
