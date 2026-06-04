#!/usr/bin/env python3
"""Quality gate CLI — reports how the current batch passes/fails quality rules."""

from __future__ import annotations

import json

import commercial_launch_lib as lib


def main(argv: list[str] | None = None) -> int:
    config = lib.load_all_config()
    drafts = lib.generate_drafts(target=400, config=config)
    rejected = [d for d in drafts if d["status"] == "rejected_quality"]
    print(
        json.dumps(
            {
                "min_quality_score": config["quality"]["min_quality_score"],
                "total": len(drafts),
                "rejected_quality": len(rejected),
                "sample_reasons": list({d["rejection_reason"] for d in rejected})[:10],
            },
            ensure_ascii=False,
            indent=2,
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
