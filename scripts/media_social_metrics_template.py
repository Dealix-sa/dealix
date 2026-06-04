#!/usr/bin/env python3
"""Emit an empty social metrics template (founder fills in; no fabricated numbers)."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "config" / "media_social_metrics_template.json"


def main() -> int:
    template = {
        "version": "v5",
        "note": "Manual inputs only. Leave null until real, measured values exist.",
        "metrics": {m: None for m in ["reach", "engagement", "profile_visits", "inbound_dms",
                                       "follower_growth", "posts_published"]},
    }
    OUT.write_text(json.dumps(template, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Wrote metrics template -> {OUT}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
