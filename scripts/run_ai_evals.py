#!/usr/bin/env python3
"""Run AI evals.

In demo mode, no real provider is called; deterministic outputs go through
the same eval gates. Reports go to reports/ai/evals-YYYY-MM-DD.md.
"""
from __future__ import annotations

import argparse
import datetime as _dt
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.ai_eval import check_no_autosend, check_no_banned_claims
from lib.ai_router import route

ROOT = Path(__file__).resolve().parent.parent
EVAL_DIR = ROOT / "business" / "ai" / "evals"
OUT_DIR = ROOT / "reports" / "ai"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--mode", default="demo", choices=["demo", "live"])
    args = parser.parse_args()

    cases: list[dict] = []
    for fp in sorted(EVAL_DIR.glob("*_cases.json")):
        data = json.loads(fp.read_text(encoding="utf-8"))
        for c in data.get("cases", []):
            c["_source"] = fp.name
            cases.append(c)

    OUT_DIR.mkdir(parents=True, exist_ok=True)
    date = _dt.date.today().isoformat()
    lines = [f"# AI evals — {date} (mode={args.mode})", "", f"Cases: **{len(cases)}**", ""]
    pass_count = 0
    fail_count = 0

    for c in cases:
        prompt = json.dumps(c.get("input", ""), ensure_ascii=False)
        resp = route(
            c["task"],
            prompt,
            lang=c.get("lang", "en"),
            use_ai=(args.mode == "live"),
        )
        checks = [
            check_no_banned_claims(resp.output),
            check_no_autosend(resp.output),
        ]
        # safety case-specific
        if c.get("expected_refusal"):
            ok = resp.review_status == "refused"
            checks.append(type("R", (), {"name": "expected_refusal", "passed": ok, "detail": f"review_status={resp.review_status}"})())
        if c.get("expected_refusal") is False:
            ok = resp.review_status != "refused"
            checks.append(type("R", (), {"name": "expected_pass", "passed": ok, "detail": f"review_status={resp.review_status}"})())

        ok_all = all(getattr(ch, "passed", False) for ch in checks)
        if ok_all:
            pass_count += 1
        else:
            fail_count += 1

        lines.append(f"## {c['id']} ({c['task']}, {c.get('lang','en')}) — {'PASS' if ok_all else 'FAIL'}")
        for ch in checks:
            mark = "✓" if getattr(ch, "passed", False) else "✗"
            lines.append(f"- {mark} {getattr(ch, 'name', '?')} {getattr(ch, 'detail', '')}")
        lines.append("")

    lines.insert(3, f"Pass: **{pass_count}** · Fail: **{fail_count}**")
    out = OUT_DIR / f"evals-{date}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out}")
    print(f"pass={pass_count} fail={fail_count}")
    return 0 if fail_count == 0 else 1


if __name__ == "__main__":
    raise SystemExit(main())
