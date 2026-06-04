#!/usr/bin/env python3
"""Run the eval rubrics over a sample of generated drafts and report pass rates."""
from __future__ import annotations
import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from v5.lib import BANNED_PHRASES, out_dir  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
RUBRICS = ROOT / "config" / "ai_eval_rubrics.json"


def eval_draft(d: dict) -> dict:
    text = f"{d.get('subject','')} {d.get('body','')} {d.get('cta','')}".lower()
    compliance = {
        "opt_out": bool(d.get("opt_out")),
        "no_unverified_claims": not any(b in text for b in BANNED_PHRASES),
        "no_banned_tactics": "scrap" not in text and "auto-send" not in text,
    }
    quality = {
        "clarity": d.get("quality_score", 0) >= 3,
        "relevance": bool(d.get("pain_angle")),
        "cta": bool(d.get("cta")),
    }
    return {"compliance_pass": all(compliance.values()), "quality_pass": all(quality.values())}


def main() -> int:
    if not RUBRICS.exists():
        print("ai_eval_rubrics.json missing", file=sys.stderr)
        return 1
    d = out_dir()
    q = d / "draft_queue.jsonl"
    if not q.exists():
        print("no draft_queue — run the draft factory first", file=sys.stderr)
        return 1
    drafts = [json.loads(l) for l in q.read_text(encoding="utf-8").splitlines() if l.strip()]
    sample = drafts[:50]
    results = [eval_draft(x) for x in sample]
    comp_rate = sum(r["compliance_pass"] for r in results) / max(1, len(results))
    qual_rate = sum(r["quality_pass"] for r in results) / max(1, len(results))
    out = {
        "sampled": len(sample),
        "compliance_pass_rate": round(comp_rate, 3),
        "quality_pass_rate": round(qual_rate, 3),
        "compliance_gate": comp_rate == 1.0,
    }
    (d / "ai_eval_report.json").write_text(json.dumps(out, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(out, indent=2))
    # Compliance must be 100%.
    return 0 if out["compliance_gate"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
