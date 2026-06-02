#!/usr/bin/env python3
"""Distribution Day — one command to run the full approval-first cycle.

Runs (in order): generate drafts → review queue → follow-up queue → proposal
drafts → quality gate → metrics. Captures each step's output into
``reports/distribution/DISTRIBUTION_DAY.md`` and prints a single verdict.

No external sends are performed — the output is a review surface only.
"""

from __future__ import annotations

import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from auto_client_acquisition.distribution_os.store import reports_dir, write_text  # noqa: E402

STEPS: list[list[str]] = [
    [sys.executable, "scripts/generate_distribution_drafts.py"],
    [sys.executable, "scripts/review_draft_queue.py"],
    [sys.executable, "scripts/generate_followup_queue.py"],
    [sys.executable, "scripts/generate_proposal_draft.py"],
    [sys.executable, "scripts/check_draft_quality.py"],
    [sys.executable, "scripts/distribution_metrics.py"],
]


def _run(cmd: list[str]) -> tuple[str, int]:
    try:
        out = subprocess.run(cmd, cwd=ROOT, capture_output=True, text=True, timeout=300)
        return (out.stdout + out.stderr), out.returncode
    except subprocess.SubprocessError as exc:  # pragma: no cover - defensive
        return (str(exc), 1)


def main() -> int:
    lines: list[str] = [
        "# Distribution Day — يوم التصريف",
        "",
        f"Generated (UTC): {datetime.now(UTC).isoformat()}",
        "",
        "> approval-first — لا إرسال خارجي. هذه نتيجة تشغيل المسودات والمتابعات والعروض والمقاييس.",
        "",
    ]
    failed = False
    for cmd in STEPS:
        label = " ".join(c.replace(sys.executable, "python3") for c in cmd)
        out, code = _run(cmd)
        if code != 0:
            failed = True
        lines += [
            f"## `$ {label}`",
            "",
            f"exit code: `{code}`",
            "",
            "```text",
            out.strip()[-4000:],
            "```",
            "",
        ]

    verdict = "FAIL" if failed else "PASS"
    lines += ["## Verdict", "", f"**{verdict}**", ""]
    report = write_text(reports_dir() / "DISTRIBUTION_DAY.md", "\n".join(lines))

    print(f"wrote: {report.relative_to(ROOT)}")
    print(f"DEALIX_DISTRIBUTION_DAY={verdict}")
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
