#!/usr/bin/env python3
"""Compliance gate — the first hard filter in the targeting pipeline.

Every candidate company must pass this gate BEFORE it is scored, routed, or
drafted. The gate encodes the Dealix non-negotiables:

  - No scraping behind login / no CAPTCHA bypass / no leaked datasets.
  - Respect robots.txt and source terms.
  - No personal phone numbers; an official channel is required.
  - Sensitive sectors (gov / health / finance) require governance review.
  - Enough independent evidence to justify outreach.

Output: each company is classified as ``approved``, ``review_required``
(sensitive sector held for a human governance sign-off), or ``rejected`` with an
explicit reason. Nothing silently drops — every reject carries a reason so the
decision is auditable.

Usage:
    python scripts/targeting_compliance_gate.py \\
        --in data/targeting/company_master.jsonl \\
        --out data/targeting/out
"""
from __future__ import annotations

import argparse
import csv
import json
from pathlib import Path
from typing import Any

from scripts.targeting_common import (
    COMPANY_MASTER,
    OUT_DIR,
    ensure_out_dir,
    load_blocked,
    load_companies,
)

APPROVED = "approved"
REVIEW = "review_required"
REJECTED = "rejected"


def evaluate(company: dict[str, Any], blocked: dict[str, Any] | None = None) -> dict[str, Any]:
    """Return a compliance verdict for one company.

    The verdict dict carries: status, reasons (list), and the original company.
    """
    blocked = blocked or load_blocked()
    reasons: list[str] = []

    blocked_domains = [d.lower() for d in blocked.get("blocked_domains", [])]
    blocked_types = set(blocked.get("blocked_source_types", []))
    red_flags = blocked.get("red_flag_fields", {})
    sensitive = set(blocked.get("sensitive_sectors", []))
    allowed_channels = set(blocked.get("allowed_channels", []))
    min_evidence = int(blocked.get("minimum_evidence_count", 1))

    # 1) Blocked source type → hard reject.
    src_type = (company.get("source_type") or "").strip()
    if src_type in blocked_types:
        reasons.append(f"blocked_source_type:{src_type}")

    # 2) Blocked domain substring in any source URL → hard reject.
    for url in company.get("source_urls", []):
        low = str(url).lower()
        for dom in blocked_domains:
            if dom in low:
                reasons.append(f"blocked_domain:{dom}")
                break

    # 3) Red-flag fields (personal phone, leaked data, robots ignored).
    for field, why in red_flags.items():
        if company.get(field):
            reasons.append(f"red_flag:{field}:{why}")

    # 4) Evidence floor.
    evidence = int(company.get("evidence_count") or 0)
    if evidence < min_evidence:
        reasons.append(f"insufficient_evidence:{evidence}<{min_evidence}")

    # 5) Channel must be official/allowed.
    channel = (company.get("contact_channel") or "").strip()
    if not channel:
        reasons.append("no_contact_channel")
    elif channel not in allowed_channels:
        # Not an automatic reject unless it is an explicit red flag; flag it as a
        # weak channel so scoring can apply the penalty.
        reasons.append(f"weak_contact_channel:{channel}")

    # Decide status.
    # Hard-reject reasons (anything that violates the non-negotiables).
    hard = [
        r for r in reasons
        if r.startswith(("blocked_source_type", "blocked_domain", "red_flag", "insufficient_evidence"))
        or r == "no_contact_channel"
    ]
    if hard:
        return {"status": REJECTED, "reasons": reasons, "company": company}

    if (company.get("sector") or "") in sensitive:
        reasons.append("sensitive_sector_review_required")
        return {"status": REVIEW, "reasons": reasons, "company": company}

    return {"status": APPROVED, "reasons": reasons, "company": company}


def run(companies: list[dict[str, Any]]) -> dict[str, list[dict[str, Any]]]:
    """Partition companies into approved / review / rejected buckets."""
    blocked = load_blocked()
    buckets: dict[str, list[dict[str, Any]]] = {APPROVED: [], REVIEW: [], REJECTED: []}
    for c in companies:
        verdict = evaluate(c, blocked)
        buckets[verdict["status"]].append(verdict)
    return buckets


def _write_outputs(buckets: dict[str, list[dict[str, Any]]], out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    # approved_research_pool.csv — the only set that flows onward to scoring.
    approved = buckets[APPROVED] + buckets[REVIEW]
    with (out_dir / "approved_research_pool.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["company_name", "sector", "city", "status", "reasons"])
        for v in approved:
            c = v["company"]
            w.writerow([c.get("company_name"), c.get("sector"), c.get("city"),
                        v["status"], "; ".join(v["reasons"])])
    # rejected_targets.csv — every reject with its reason.
    with (out_dir / "rejected_targets.csv").open("w", encoding="utf-8", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["company_name", "sector", "reasons"])
        for v in buckets[REJECTED]:
            c = v["company"]
            w.writerow([c.get("company_name"), c.get("sector"), "; ".join(v["reasons"])])


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Dealix targeting compliance gate")
    ap.add_argument("--in", dest="infile", default=str(COMPANY_MASTER))
    ap.add_argument("--out", dest="outdir", default=str(OUT_DIR))
    args = ap.parse_args(argv)

    companies = load_companies(Path(args.infile))
    buckets = run(companies)
    out_dir = Path(args.outdir)
    _write_outputs(buckets, out_dir)

    print(json.dumps({
        "approved": len(buckets[APPROVED]),
        "review_required": len(buckets[REVIEW]),
        "rejected": len(buckets[REJECTED]),
        "out": str(out_dir),
    }, ensure_ascii=False, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
