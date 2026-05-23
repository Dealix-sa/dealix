#!/usr/bin/env python3
"""Dealix Master Verifier — 9-layer orchestrator.

Runs verify_layer1..verify_layer9 in order, aggregates verdicts.
Exit codes: 0=PASS, 1=FAIL, 2=PARTIAL (any layer exit 2, none exit 1).

See docs/ops/MASTER_VERIFICATION_SYSTEM.md.
"""

from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
import time
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"

LAYERS = [
    (1, "repo_structure", SCRIPTS / "verify_layer1_repo_structure.py"),
    (2, "code_health", SCRIPTS / "verify_layer2_code_health.sh"),
    (3, "data_contracts", SCRIPTS / "verify_layer3_data_contracts.py"),
    (4, "prompt_output_quality", SCRIPTS / "verify_layer4_prompt_output_quality.sh"),
    (5, "trust_security", SCRIPTS / "verify_layer5_trust_security.sh"),
    (6, "revenue_runtime", SCRIPTS / "verify_layer6_revenue_runtime.sh"),
    (7, "server_runtime", SCRIPTS / "verify_layer7_server_runtime.sh"),
    (8, "github_governance", SCRIPTS / "verify_layer8_github_governance.py"),
    (9, "business_evidence", SCRIPTS / "verify_layer9_business_evidence.sh"),
]

CODE_VERDICT = {0: "PASS", 1: "FAIL", 2: "PARTIAL"}


def run_layer(script: Path, private_ops: str | None) -> dict:
    if not script.exists():
        return {
            "verdict": "FAIL",
            "exit_code": 1,
            "summary": f"missing: {script.name}",
            "duration_s": 0.0,
        }
    cmd = [str(script)] if script.suffix == ".sh" else [sys.executable, str(script)]
    cmd.append("--json")
    if private_ops:
        cmd += ["--private-ops", private_ops]
    env = os.environ.copy()
    if private_ops:
        env["PRIVATE_OPS"] = private_ops
    start = time.time()
    try:
        res = subprocess.run(  # noqa: S603
            cmd, capture_output=True, text=True, env=env, timeout=900
        )
    except subprocess.TimeoutExpired:
        return {
            "verdict": "FAIL",
            "exit_code": 1,
            "summary": "timeout (>15min)",
            "duration_s": 900.0,
        }
    duration = round(time.time() - start, 2)
    verdict = CODE_VERDICT.get(res.returncode, "FAIL")
    last_stdout = (res.stdout.strip().splitlines() or [""])[-1]
    last_stderr = (res.stderr.strip().splitlines() or [""])[-1]
    summary = ""
    try:
        parsed = json.loads(last_stdout)
        if isinstance(parsed, dict) and parsed.get("summary"):
            summary = str(parsed["summary"])
    except (json.JSONDecodeError, ValueError):
        pass
    if not summary:
        summary = (last_stdout if res.returncode == 0 else last_stderr or last_stdout)[:200]
    return {
        "verdict": verdict,
        "exit_code": res.returncode,
        "summary": summary or "(no output)",
        "duration_s": duration,
    }


def aggregate(layers: list[dict]) -> str:
    if any(layer["exit_code"] == 1 for layer in layers):
        return "FAIL"
    if any(layer["exit_code"] == 2 for layer in layers):
        return "PARTIAL"
    return "PASS"


def fmt_table(rows: list[dict]) -> str:
    icon = {"PASS": "[OK]", "FAIL": "[FAIL]", "PARTIAL": "[WARN]"}
    lines = ["", "=" * 64, " Dealix Master Verification", "=" * 64]
    for r in rows:
        lines.append(
            f" {icon.get(r['verdict'], '[?]'):<7} L{r['layer']} {r['name']:<24} {r['duration_s']:>5}s  {r['summary'][:60]}"
        )
    return "\n".join(lines)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--layers", help="Comma-separated layer numbers e.g. 1,3,5", default="")
    p.add_argument("--private-ops", default=os.environ.get("PRIVATE_OPS"))
    p.add_argument("--json-out", help="Write full report JSON to file")
    p.add_argument("--quiet", action="store_true")
    args = p.parse_args()

    selected = (
        {int(x) for x in args.layers.split(",") if x.strip().isdigit()} if args.layers else None
    )
    rows: list[dict] = []
    for num, name, script in LAYERS:
        if selected is not None and num not in selected:
            continue
        if not args.quiet:
            print(f"--> L{num} {name} ...", file=sys.stderr, flush=True)
        result = run_layer(script, args.private_ops)
        rows.append({"layer": num, "name": name, "script": script.name, **result})

    overall = aggregate(rows)
    warnings = sum(1 for r in rows if r["exit_code"] == 2)
    try:
        git_sha = (
            subprocess.run(
                ["git", "rev-parse", "HEAD"],  # noqa: S607
                capture_output=True,
                text=True,
                cwd=REPO,
            ).stdout.strip()
            or "unknown"
        )
    except Exception:
        git_sha = "unknown"

    report = {
        "overall": overall,
        "warnings": warnings,
        "git_sha": git_sha,
        "private_ops": args.private_ops or None,
        "layers": rows,
    }

    if args.json_out:
        Path(args.json_out).write_text(json.dumps(report, indent=2))
    if not args.quiet:
        print(fmt_table(rows), file=sys.stderr)
        print(f" Overall: {overall}  (warnings={warnings})", file=sys.stderr)
        print("=" * 64, file=sys.stderr)
    print(json.dumps(report, separators=(",", ":")))

    return {"PASS": 0, "FAIL": 1, "PARTIAL": 2}[overall]


if __name__ == "__main__":
    sys.exit(main())
