"""Final launch control verify reaches GO after the pipeline has run."""

from __future__ import annotations

import api_commercial_static_check as apic
import commercial_generate_400_drafts as gen
import commercial_safety_audit as audit
import final_launch_control_verify as control
import final_secret_and_risk_scan as scan
import media_social_calendar_generate as cal
import site_launch_static_check as site
from _commercial_common import COMMERCIAL_OUTPUTS, OUTPUTS_DIR, write_json
from _launch_util import SEED

DAY = "2099-06-01"


def _run_pipeline():
    # Generate the artifacts the control tower reads.
    result = gen.generate(target=400, day=DAY, seed_path=SEED)
    gen.write_outputs(result, COMMERCIAL_OUTPUTS / DAY)
    write_json(COMMERCIAL_OUTPUTS / DAY / "safety_audit.json", audit.run(DAY))
    cal_out = OUTPUTS_DIR / "media_social" / DAY
    write_json(cal_out / "content_calendar.json", cal.generate(DAY))
    write_json(OUTPUTS_DIR / "site_launch" / DAY / "site_launch_report.json", site.run(DAY))
    write_json(OUTPUTS_DIR / "api" / DAY / "api_commercial_qa.json", apic.run(DAY))
    write_json(control.CONTROL_OUTPUTS / "secret_risk_scan.json", scan.run(DAY))


def test_control_tower_reaches_go():
    _run_pipeline()
    report = control.run(DAY)
    failed = [c for c in report["checks"] if c["critical"] and not c["passed"]]
    assert report["decision"] == "GO", failed
    assert report["passed"] is True


def test_go_and_nogo_scopes_present():
    report = control.run(DAY)
    assert "400 review-only drafts" in report["go_scope"]
    assert "automated email sending" in report["no_go_scope"]
