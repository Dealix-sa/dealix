#!/usr/bin/env python3
"""Production-certification orchestrator.

Runs every Dealix verifier in sequence (new + pre-existing) and aggregates
their PASS/WARN/FAIL verdicts into:

  - stdout summary (human-readable),
  - ``docs/ops/DEALIX_FINAL_READINESS_REPORT.md``  (regenerated each run),
  - ``docs/ops/DEALIX_MISSING_SYSTEMS.md``         (only entries that FAILed),
  - exit code 1 if any FAIL.

The orchestrator deliberately calls verifier scripts via ``subprocess`` so
each one runs with its own argument parser; we do not import them as
modules to keep state isolation tight.

Pass ``--ci`` to use CI-safe modes (no real secret values required) on
verifiers that support it. Pass ``--skip-live`` to skip any network probe.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


@dataclass
class CheckResult:
    name: str
    cmd: list[str]
    returncode: int
    stdout: str
    verdict: str  # PASS | WARN | FAIL | SKIPPED


# Each entry: (display name, [argv from repo root])
# ``ci_only_extra_args`` is merged when --ci is passed.
CHECKS: list[tuple[str, list[str], list[str]]] = [
    ("production_env",            ["python", "scripts/verify_production_env.py"],            ["--ci"]),
    ("railway_readiness",         ["python", "scripts/verify_railway_readiness.py"],         []),
    ("live_send_safety",          ["python", "scripts/verify_live_send_safety.py"],          []),
    ("railway_production_config", ["python", "scripts/verify_railway_production_config.py"], ["--skip-live"]),
]


def _parse_verdict(text: str, default: str = "PASS") -> str:
    """Pull *_VERDICT=... from the verifier's stdout (last match wins)."""
    m = re.findall(r"^[A-Z_]+VERDICT=(PASS|WARN|FAIL)\b", text, re.MULTILINE)
    if not m:
        return default
    return m[-1]


def _run(name: str, base_cmd: list[str], extra: list[str], ci: bool) -> CheckResult:
    cmd = list(base_cmd)
    if ci:
        cmd.extend(extra)
    try:
        proc = subprocess.run(
            cmd,
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
            timeout=120,
        )
    except FileNotFoundError as exc:
        return CheckResult(name, cmd, 127, f"not_runnable: {exc}", "SKIPPED")
    except subprocess.TimeoutExpired:
        return CheckResult(name, cmd, 124, "timeout (>120s)", "FAIL")

    combined = (proc.stdout or "") + (proc.stderr or "")
    verdict = _parse_verdict(combined, default="PASS" if proc.returncode == 0 else "FAIL")
    if proc.returncode != 0 and verdict == "PASS":
        # Defensive: a non-zero exit must never be reported as PASS.
        verdict = "FAIL"
    return CheckResult(name, cmd, proc.returncode, combined, verdict)


def _write_reports(results: list[CheckResult]) -> tuple[Path, Path]:
    now = datetime.now(timezone.utc).isoformat()
    full = ROOT / "docs" / "ops" / "DEALIX_FINAL_READINESS_REPORT.md"
    missing = ROOT / "docs" / "ops" / "DEALIX_MISSING_SYSTEMS.md"
    full.parent.mkdir(parents=True, exist_ok=True)

    lines: list[str] = []
    lines.append("# Dealix Final Readiness Report")
    lines.append("")
    lines.append(f"Generated: `{now}`")
    lines.append("")
    lines.append("| Check | Verdict | Exit |")
    lines.append("|------|---------|------|")
    for r in results:
        lines.append(f"| `{r.name}` | **{r.verdict}** | {r.returncode} |")
    lines.append("")
    for r in results:
        lines.append(f"## `{r.name}` — {r.verdict}")
        lines.append("")
        lines.append("```")
        lines.append(" ".join(r.cmd))
        lines.append("```")
        lines.append("")
        tail = r.stdout.strip().splitlines()[-80:] or ["(no output)"]
        lines.append("```")
        lines.extend(tail)
        lines.append("```")
        lines.append("")
    full.write_text("\n".join(lines), encoding="utf-8")

    miss_lines = ["# Dealix Missing Systems", "", f"Generated: `{now}`", ""]
    any_fail = False
    for r in results:
        if r.verdict in {"FAIL", "SKIPPED"}:
            any_fail = True
            miss_lines.append(f"## {r.name} — {r.verdict}")
            miss_lines.append("")
            miss_lines.append("```")
            miss_lines.extend(r.stdout.strip().splitlines()[-30:] or ["(no output)"])
            miss_lines.append("```")
            miss_lines.append("")
    if not any_fail:
        miss_lines.append("All systems present. No FAIL or SKIPPED checks.")
    missing.write_text("\n".join(miss_lines), encoding="utf-8")

    return full, missing


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--ci", action="store_true", help="Use CI-safe modes for verifiers")
    p.add_argument(
        "--skip-live",
        action="store_true",
        help=(
            "Skip any live network probes (forces --skip-live on verifiers "
            "that probe Railway). Implied by --ci."
        ),
    )
    args = p.parse_args()
    ci = args.ci
    # --skip-live is currently subsumed by the per-check ci_only_extra_args; we
    # keep the flag for symmetry and future per-check toggles.
    _ = args.skip_live

    print("== verify_everything ==")
    results: list[CheckResult] = []
    for name, base, extra in CHECKS:
        print(f"--> {name} ...")
        r = _run(name, base, extra, ci)
        print(f"    verdict: {r.verdict} (exit {r.returncode})")
        results.append(r)

    full, missing = _write_reports(results)
    print()
    print(f"report: {full.relative_to(ROOT)}")
    print(f"missing: {missing.relative_to(ROOT)}")
    print()
    any_fail = any(r.verdict == "FAIL" for r in results)
    any_skip = any(r.verdict == "SKIPPED" for r in results)
    overall = "FAIL" if any_fail else ("WARN" if any_skip else "PASS")
    print(f"EVERYTHING_VERDICT={overall}")
    return 1 if overall == "FAIL" else 0


if __name__ == "__main__":
    raise SystemExit(main())
