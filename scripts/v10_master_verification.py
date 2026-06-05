#!/usr/bin/env python3
"""V10 master verification — aggregate all V10 OS checks into one report.

Runs all 11 V10 OS verifications, writes each per-OS JSON plus a master
markdown report to outputs/v10_verification/. Read/score/report only — never
sends anything externally.

Run: python scripts/v10_master_verification.py [--strict]
Exit code is non-zero if any OS fails (always non-zero gate, --strict is a no-op
alias kept for CLI compatibility).
"""

from __future__ import annotations

import argparse
import sys
from datetime import UTC, datetime, timezone
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

from v10_common import REPO, write_json
from v10_specs import verify_all

MASTER_MD = "outputs/v10_verification/V10_MASTER_VERIFICATION.md"


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--strict", action="store_true")
    p.parse_args(argv)

    results = verify_all()
    all_pass = True
    rows = []
    for _key, result, json_out in results:
        write_json(json_out, result.to_dict())
        all_pass = all_pass and result.passed
        present = len(result.required_files) - len(result.missing_files)
        rows.append((result.name, result.verdict, present, len(result.required_files), result))

    now = datetime.now(UTC).strftime("%Y-%m-%d %H:%M UTC")
    lines = [
        "# V10 Master Verification — Institutional Scale & Market Domination OS",
        "",
        f"_Generated: {now}_",
        "",
        f"## Overall: {'PASS' if all_pass else 'FAIL'}",
        "",
        "| OS | Verdict | Files Present | Forbidden Claims | Missing Markers |",
        "|---|---|---|---|---|",
    ]
    for name, verdict, present, total, result in rows:
        lines.append(
            f"| {name} | {verdict} | {present}/{total} | "
            f"{len(result.forbidden_hits)} | {len(result.missing_markers)} |"
        )
    lines += [
        "",
        "## Safety Invariants",
        "",
        "- No external sending (Email/WhatsApp/LinkedIn), no SMTP, no secrets.",
        "- No scraping, no auto-submit, no LinkedIn automation, no live paid ads.",
        "- No fake traction, no guaranteed ROI, no unverified security/compliance claims.",
        "- Every output is a draft/report for founder review.",
        "",
    ]
    if not all_pass:
        lines += ["## Failures", ""]
        for name, _verdict, _present, _total, result in rows:
            if not result.passed:
                for m in result.missing_files:
                    lines.append(f"- {name}: missing_file `{m}`")
                for m in result.missing_markers:
                    lines.append(f"- {name}: missing_marker `{m}`")
                for h in result.forbidden_hits:
                    lines.append(f"- {name}: forbidden_claim `{h}`")
        lines.append("")

    out = REPO / MASTER_MD
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines).rstrip() + "\n", encoding="utf-8")

    print(f"V10_MASTER_VERIFICATION={'PASS' if all_pass else 'FAIL'}")
    print(f"wrote {out.relative_to(REPO)}")
    for name, verdict, present, total, _ in rows:
        print(f"  {name}={verdict} ({present}/{total})")
    return 0 if all_pass else 1


if __name__ == "__main__":
    raise SystemExit(main())
