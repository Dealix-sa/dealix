#!/usr/bin/env python3
"""Commercial Launch Readiness check.

Verifies the commercial-launch OS is internally consistent and SAFE to run as
a review-only draft factory. This does NOT certify readiness for external
sending — that requires the out-of-repo steps in
docs/commercial-launch/21_EXTERNAL_GO_LIVE_REQUIREMENTS.md.

Exit 0 = ready (draft-only). Exit 1 = blocked.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import commercial_launch_core as core  # noqa: E402


def run_readiness(date_str: str | None = None) -> dict:
    date_str = date_str or core.today_str()
    checks: list[dict] = []

    def check(name: str, ok: bool, detail: str = "") -> None:
        checks.append({"name": name, "ok": bool(ok), "detail": detail})

    # 1. Configs load
    try:
        configs = core.load_all_configs()
        check("configs_load", True, f"{len(configs)} config files")
    except Exception as exc:
        check("configs_load", False, str(exc))
        configs = {}

    if configs:
        # 2. Five verticals
        verts = configs["verticals"]["verticals"]
        check("five_verticals", len(verts) >= 5, f"{len(verts)} verticals")
        # 3. Offer ladder complete
        stages = {o["stage"] for o in configs["offers"]["ladder"]}
        expected = {"entry_diagnostic", "paid_pilot", "department_os",
                    "monthly_retainer", "enterprise_custom_os"}
        check("offer_ladder", expected.issubset(stages), f"stages={sorted(stages)}")
        # 4. Global safety flags correct
        flags = configs["launch"]["global_safety_flags"]
        check("safety_flags", (flags["send_allowed"] is False
                               and flags["external_send_blocked"] is True
                               and flags["requires_founder_approval"] is True
                               and flags["no_auto_send"] is True), str(flags))
        # 5. No forbidden status allowed
        allowed = set(configs["launch"]["allowed_statuses"])
        check("no_forbidden_status", not (allowed & core.FORBIDDEN_STATUSES),
              f"allowed={sorted(allowed)}")
        # 6. Distribution >= 400
        dist_total = sum(configs["distribution"]["distribution"].values())
        check("distribution_target", dist_total >= 400, f"sum={dist_total}")
        # 7. Channels all draft-only / no auto-send
        ch_ok = all(c.get("draft_only") and not c.get("auto_send_allowed")
                    for c in configs["channels"]["channels"].values())
        check("channels_draft_only", ch_ok, "")

    # 8. Required commercial-launch docs present
    docs_dir = core.REPO_ROOT / "docs" / "commercial-launch"
    required_docs = [
        "00_OFFICIAL_COMMERCIAL_LAUNCH_OS.md",
        "02_OFFER_LADDER_SAR.md",
        "06_CHANNEL_POLICY.md",
        "07_COMPLIANCE_AND_SAFETY_GATES.md",
        "21_EXTERNAL_GO_LIVE_REQUIREMENTS.md",
        "99_FINAL_COMMERCIAL_LAUNCH_READINESS_REPORT.md",
    ]
    missing = [d for d in required_docs if not (docs_dir / d).exists()]
    check("core_docs_present", not missing, f"missing={missing}")

    # 9. Five vertical playbooks present
    vdir = docs_dir / "verticals"
    vfiles = sorted(vdir.glob("*.md")) if vdir.exists() else []
    check("vertical_playbooks", len(vfiles) >= 5, f"{len(vfiles)} playbooks")

    # 10. Workflow exists and is artifact-only (no secrets, no commit)
    wf = core.REPO_ROOT / ".github" / "workflows" / "commercial-draft-factory.yml"
    if wf.exists():
        wf_text = wf.read_text(encoding="utf-8")
        # No actual secret usage (${{ secrets.* }}) and no commit/push of outputs.
        wf_ok = ("secrets." not in wf_text) and ("git push" not in wf_text.lower()) \
            and ("git commit" not in wf_text.lower())
        check("workflow_artifact_only", wf_ok, "no secret usage / no git push/commit")
    else:
        check("workflow_artifact_only", False, "workflow missing")

    passed = all(c["ok"] for c in checks)
    report = {
        "ready_draft_only": passed,
        "date": date_str,
        "checks": checks,
        "note": ("Draft-only readiness. External sending requires the out-of-repo "
                 "steps in 21_EXTERNAL_GO_LIVE_REQUIREMENTS.md and is NOT certified here."),
    }
    out = core.output_dir_for(date_str)
    out.mkdir(parents=True, exist_ok=True)
    with (out / "readiness_report.json").open("w", encoding="utf-8") as fh:
        json.dump(report, fh, ensure_ascii=False, indent=2)
    return report


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Commercial launch readiness.")
    parser.add_argument("--date", default=None)
    args = parser.parse_args(argv)
    report = run_readiness(args.date)
    print(f"Readiness (draft-only): {report['ready_draft_only']}")
    for c in report["checks"]:
        mark = "OK " if c["ok"] else "FAIL"
        print(f"  [{mark}] {c['name']} {c['detail']}")
    return 0 if report["ready_draft_only"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
