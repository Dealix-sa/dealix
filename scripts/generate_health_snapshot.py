#!/usr/bin/env python3
"""Generate a one-page health snapshot of the Dealix repo.

Captures: branch, last 5 commits, untracked files, modified files,
verifier results (best-effort), and counts of pages/scripts/tests.
Output: reports/health/health-snapshot-YYYY-MM-DD.md
"""

from __future__ import annotations

import datetime as _dt
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "reports" / "health"


def _run(cmd: list[str]) -> str:
    try:
        return subprocess.check_output(cmd, cwd=ROOT, text=True, stderr=subprocess.STDOUT).strip()
    except (subprocess.CalledProcessError, FileNotFoundError) as e:
        return f"(error: {e})"


def _count_files(pattern: str) -> int:
    return len(list(ROOT.glob(pattern)))


def main() -> int:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    date = _dt.date.today().isoformat()

    branch = _run(["git", "branch", "--show-current"])
    last5 = _run(["git", "log", "--oneline", "-5"])
    status = _run(["git", "status", "--short"])

    pages = _count_files("apps/web/app/**/page.tsx")
    api_routes = _count_files("apps/web/app/api/**/route.ts")
    py_scripts = _count_files("scripts/*.py")
    tests = _count_files("tests/**/test_*.py")

    lines = [
        f"# Dealix Health Snapshot — {date}",
        "",
        f"**Branch:** `{branch}`",
        "",
        "## Last 5 commits",
        "",
        "```",
        last5,
        "```",
        "",
        "## Working tree",
        "",
        f"- Untracked / modified lines: {len(status.splitlines()) if status else 0}",
        "",
        "## Surface counts",
        "",
        f"- Web pages: **{pages}**",
        f"- Web API routes: **{api_routes}**",
        f"- Python scripts: **{py_scripts}**",
        f"- Test files: **{tests}**",
        "",
        "## Verifier results (best-effort)",
        "",
    ]

    for label, cmd in [
        ("no secrets", ["python3", "scripts/check_no_secrets.py"]),
        ("ultimate OS", ["python3", "scripts/verify_dealix_ultimate_os.py"]),
        ("daily operator (demo)", ["python3", "scripts/dealix_daily_operator.py", "--mode", "demo"]),
    ]:
        try:
            subprocess.check_output(cmd, cwd=ROOT, stderr=subprocess.STDOUT, timeout=60)
            lines.append(f"- {label}: PASS")
        except subprocess.SubprocessError:
            lines.append(f"- {label}: FAIL")
        except FileNotFoundError:
            lines.append(f"- {label}: MISSING")

    out = OUT_DIR / f"health-snapshot-{date}.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
