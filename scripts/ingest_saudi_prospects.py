#!/usr/bin/env python3
"""Ingest the curated Saudi B2B target frame.

Three modes, all doctrine-safe (company-level public data, no PII, no scraping):

    # default — validate + ICP-rank, print the top accounts (no server needed)
    python scripts/ingest_saudi_prospects.py

    # also seed the founder lead-inbox so prospects show in /api/v1/founder/leads
    python scripts/ingest_saudi_prospects.py --seed-inbox

    # push to the running API batch endpoint (Tier-1 owned/public source)
    python scripts/ingest_saudi_prospects.py --post-batch http://localhost:8000

The dataset is `data/leads/saudi_b2b_prospects.csv` (override:
DEALIX_LEAD_DATASET_PATH). Provenance: data/leads/SOURCES.md.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

from auto_client_acquisition.commercial_orchestrator.pipeline import (  # noqa: E402
    DEFAULT_ICP,
    dataset_path,
    load_prospects,
    _to_signals,
)
from auto_client_acquisition.icp_scorer import score_lead  # noqa: E402


def _rank(prospects: list[dict]) -> list[dict]:
    scored = []
    for p in prospects:
        if not (p.get("company_name") or "").strip():
            continue
        s = score_lead(_to_signals(p), DEFAULT_ICP)
        scored.append({**p, "icp_score": s["score"], "icp_band": s["band"]})
    scored.sort(key=lambda r: r["icp_score"], reverse=True)
    return scored


def _seed_inbox(ranked: list[dict]) -> int:
    from auto_client_acquisition import lead_inbox
    n = 0
    for r in ranked:
        lead_inbox.append({
            "company": r["company_name"],
            "name_ar": r.get("name_ar", ""),
            "sector": r.get("sector", ""),
            "city": r.get("city", ""),
            "source": "curated_public_frame",
            "source_url": r.get("source_url", ""),
            "consent_status": r.get("consent_status", "required_before_contact"),
            "icp_score": r["icp_score"],
            "icp_band": r["icp_band"],
        })
        n += 1
    return n


def _post_batch(ranked: list[dict], base_url: str) -> dict:
    import httpx
    items = [{
        "company": r["company_name"],
        "sector": r.get("sector", ""),
        "city": r.get("city", ""),
        "website": r.get("website", ""),
        "source_url": r.get("source_url", ""),
    } for r in ranked]
    payload = {"tier1_source": "public", "items": items}
    url = base_url.rstrip("/") + "/api/v1/leads/batch"
    resp = httpx.post(url, json=payload, timeout=30)
    return {"status_code": resp.status_code,
            "body": resp.json() if resp.headers.get("content-type", "").startswith("application/json") else resp.text}


def main(argv: list[str] | None = None) -> int:
    ap = argparse.ArgumentParser(description="Ingest Saudi B2B target frame")
    ap.add_argument("--seed-inbox", action="store_true",
                    help="append prospects to the founder lead-inbox (var/)")
    ap.add_argument("--post-batch", metavar="BASE_URL", default="",
                    help="POST prospects to a running API at BASE_URL")
    ap.add_argument("--top", type=int, default=15, help="how many to print")
    args = ap.parse_args(argv)

    path = dataset_path()
    prospects = load_prospects()
    if not prospects:
        print(f"[ingest] no dataset at {path}", file=sys.stderr)
        return 1

    ranked = _rank(prospects)
    valid = len(ranked)
    skipped = len(prospects) - valid
    print(f"[ingest] dataset: {path}")
    print(f"[ingest] {valid} valid prospects, {skipped} skipped (missing company name)")
    bands: dict[str, int] = {}
    for r in ranked:
        bands[r["icp_band"]] = bands.get(r["icp_band"], 0) + 1
    print(f"[ingest] ICP bands: {json.dumps(bands)}")
    print(f"\nTop {min(args.top, valid)} accounts by ICP fit:")
    for r in ranked[: args.top]:
        print(f"  {r['icp_score']:>3} {r['icp_band']:<5} "
              f"{r['company_name']:<38.38} {r.get('sector',''):<22} {r.get('city','')}")

    if args.seed_inbox:
        n = _seed_inbox(ranked)
        print(f"\n[ingest] seeded {n} prospects into the founder lead-inbox")

    if args.post_batch:
        try:
            out = _post_batch(ranked, args.post_batch)
            print(f"\n[ingest] POST /api/v1/leads/batch → {out['status_code']}")
        except Exception as exc:  # pragma: no cover - network dependent
            print(f"\n[ingest] batch post failed: {exc}", file=sys.stderr)
            return 2

    print("\n[ingest] reminder: every contact is consent_status=required_before_contact; "
          "no outreach until the founder confirms the recipient and approves the draft.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
