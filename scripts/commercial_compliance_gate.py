#!/usr/bin/env python3
"""Compliance gate CLI — reports compliance rejections for the current batch."""

from __future__ import annotations

import json

import commercial_launch_lib as lib


def main(argv: list[str] | None = None) -> int:
    config = lib.load_all_config()
    drafts = lib.generate_drafts(target=400, config=config)
    rejected = [d for d in drafts if d["status"] == "rejected_compliance"]
    high_risk = [d for d in drafts if d["risk_level"] == "high"]
    print(
        json.dumps(
            {
                "min_compliance_score": config["compliance"]["min_compliance_score"],
                "total": len(drafts),
                "rejected_compliance": len(rejected),
                "high_risk": len(high_risk),
                "banned_phrases_enforced": len(config["compliance"]["banned_phrases"]),
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
