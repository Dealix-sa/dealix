#!/usr/bin/env python3
"""Score drafts and emit needs_research / rejected splits + quality/compliance reports."""
from __future__ import annotations

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5.lib import out_dir  # noqa: E402


def load_drafts(d: Path) -> list[dict]:
    queue = d / "draft_queue.jsonl"
    return [json.loads(l) for l in queue.read_text(encoding="utf-8").splitlines() if l.strip()]


def main() -> int:
    d = out_dir()
    drafts = load_drafts(d)
    needs_research = [x for x in drafts if x.get("research_required")]
    rejected = [x for x in drafts if x.get("compliance_score", 5) < 4 or x.get("quality_score", 5) < 2]
    for x in rejected:
        x["status"] = "rejected"
        x["rejection_reason"] = x.get("rejection_reason") or "below quality/compliance threshold"

    (d / "needs_research.jsonl").write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in needs_research), encoding="utf-8")
    (d / "rejected_drafts.jsonl").write_text(
        "\n".join(json.dumps(x, ensure_ascii=False) for x in rejected), encoding="utf-8")

    quality = {
        "total": len(drafts),
        "avg_quality": round(sum(x["quality_score"] for x in drafts) / max(1, len(drafts)), 2),
        "avg_fit": round(sum(x["fit_score"] for x in drafts) / max(1, len(drafts)), 2),
        "needs_research": len(needs_research),
    }
    compliance = {
        "total": len(drafts),
        "avg_compliance": round(sum(x["compliance_score"] for x in drafts) / max(1, len(drafts)), 2),
        "rejected": len(rejected),
        "all_have_opt_out": all(x.get("opt_out") for x in drafts),
    }
    (d / "quality_report.json").write_text(json.dumps(quality, indent=2, ensure_ascii=False), encoding="utf-8")
    (d / "compliance_report.json").write_text(json.dumps(compliance, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({"quality": quality, "compliance": compliance}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
