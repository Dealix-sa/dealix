#!/usr/bin/env python3
"""Print founder north-star metrics (product / commercial / compliance + agent queue P0)."""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from dealix.commercial_ops.founder_agent_tasks import build_queue_status  # noqa: E402
from dealix.commercial_ops.paths import REPO_ROOT  # noqa: E402
from dealix.commercial_ops.railway_production import analyze_railway_production  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402

ensure_stdout_utf8()

METRICS_YAML = REPO_ROOT / "dealix" / "config" / "founder_north_star_metrics.yaml"
EVIDENCE_CSV = REPO_ROOT / "docs" / "commercial" / "operations" / "evidence_events_tracker.csv"


def _load_config() -> dict:
    if not METRICS_YAML.is_file():
        return {}
    return yaml.safe_load(METRICS_YAML.read_text(encoding="utf-8")) or {}


def _count_evidence(event_name: str) -> int:
    if not EVIDENCE_CSV.is_file():
        return 0
    import csv

    count = 0
    with EVIDENCE_CSV.open(encoding="utf-8", newline="") as fh:
        for row in csv.DictReader(fh):
            ev = (row.get("event") or row.get("event_type") or "").strip()
            if ev == event_name:
                count += 1
    return count


def build_status(*, api_base: str, skip_live: bool) -> dict:
    cfg = _load_config()
    product: dict = {"railway_repo": analyze_railway_production(api_base=False)["verdict"] == "PASS"}
    if skip_live:
        product["healthz"] = {"ok": None, "note": "skipped"}
    else:
        live = analyze_railway_production(api_base=api_base).get("live_healthz", {})
        product["healthz"] = {"ok": live.get("ok"), "status": live.get("status", live.get("error"))}

    queue = build_queue_status()
    commercial = {
        "proof_pack_delivered_events": _count_evidence("proof_pack_delivered"),
        "agent_queue_pending_p0": queue.get("pending_p0_count", 0),
        "agent_queue_pending_total": queue.get("pending_total", 0),
    }

    verdict = "PASS" if product.get("railway_repo") else "FAIL"
    if queue.get("pending_p0_count", 0) > 8:
        verdict = "WARN"

    return {
        "product": product,
        "commercial": commercial,
        "agent_queue": queue,
        "weekly_one_metric": (cfg.get("weekly_one_metric") or {}).get("ar"),
        "day_90_targets": cfg.get("day_90_targets"),
        "verdict": verdict,
    }


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--api-base", default=os.getenv("DEALIX_API_BASE", "https://api.dealix.me"))
    p.add_argument("--skip-live", action="store_true")
    p.add_argument("--json", action="store_true")
    args = p.parse_args()

    blob = build_status(api_base=args.api_base, skip_live=args.skip_live)
    if args.json:
        print(json.dumps(blob, ensure_ascii=False, indent=2))
    else:
        print("== Founder North Star Status ==")
        hz = blob["product"].get("healthz", {})
        print(f"  healthz: {hz.get('status', hz.get('note', '?'))}")
        print(f"  railway_repo: {'ok' if blob['product'].get('railway_repo') else 'FAIL'}")
        print(f"  proof_pack events: {blob['commercial']['proof_pack_delivered_events']}")
        print(f"  agent P0 pending: {blob['commercial']['agent_queue_pending_p0']}")
        print(f"  weekly focus: {blob.get('weekly_one_metric')}")

    print(f"FOUNDER_NORTH_STAR_VERDICT={blob['verdict']}")
    return 0 if blob["verdict"] != "FAIL" else 1


if __name__ == "__main__":
    raise SystemExit(main())
