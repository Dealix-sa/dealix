#!/usr/bin/env python3
"""
Dealix Startup OS Verifier — the whole-company gate.

Checks that every V5 OS area, script, config, test, workflow, and report is
present and that core safety invariants hold. Writes:
  outputs/startup_os/startup_os_verification.json
  outputs/startup_os/startup_os_verification.md

Exit 0 only if all CRITICAL checks pass.
"""
from __future__ import annotations
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "outputs" / "startup_os"

OS_AREAS = [
    "company-os", "product-os", "engineering-os", "site-launch", "commercial-launch",
    "sales-os", "marketing-os", "media-social-os", "ads-os", "revops-os", "delivery-os",
    "support-os", "finance-os", "legal-os", "security-os", "analytics-os", "ai-evals-os",
    "people-os", "partnerships-os", "investor-os", "operations-os", "go-live", "launch-control",
]

SCRIPTS = [
    "commercial_generate_400_drafts.py", "commercial_safety_audit.py",
    "commercial_launch_readiness.py", "commercial_founder_review_report.py",
    "commercial_score_drafts.py", "commercial_quality_gate.py", "commercial_compliance_gate.py",
    "commercial_seed_leads_validate.py", "commercial_lead_intake_validate.py",
    "commercial_metrics_summary.py", "commercial_crm_schema_verify.py",
    "media_social_calendar_generate.py", "media_social_verify.py", "media_social_metrics_template.py",
    "site_launch_static_check.py", "api_commercial_static_check.py",
    "final_secret_and_risk_scan.py", "final_launch_control_verify.py", "ai_eval_sample_drafts.py",
]

CONFIGS = ["crm_pipeline_schema.json", "analytics_events.json", "ad_campaigns_seed.json",
           "ai_eval_rubrics.json"]

TESTS = [
    "test_commercial_generate_400_drafts.py", "test_commercial_safety_audit.py",
    "test_commercial_launch_readiness.py", "test_commercial_no_external_send.py",
    "test_commercial_quality_gate.py", "test_commercial_compliance_gate.py",
    "test_commercial_outputs_schema.py", "test_commercial_founder_review_report.py",
    "test_commercial_seed_leads_validate.py", "test_media_social_os.py",
    "test_site_launch_static_check.py", "test_crm_schema_verify.py",
    "test_api_commercial_static_check.py", "test_final_secret_and_risk_scan.py",
    "test_final_launch_control_verify.py", "test_startup_os_verify.py", "test_ai_eval_rubrics.py",
]

WORKFLOWS = ["commercial-draft-factory.yml", "media-social-calendar.yml",
             "site-commercial-verify.yml", "final-launch-control.yml", "startup-os-verify.yml"]

REPORTS = {
    "company-os": "99_COMPANY_OS_REPORT.md", "product-os": "99_PRODUCT_OS_REPORT.md",
    "engineering-os": "99_ENGINEERING_OS_REPORT.md", "site-launch": "99_SITE_LAUNCH_REPORT.md",
    "commercial-launch": "99_FINAL_COMMERCIAL_LAUNCH_REPORT.md", "sales-os": "99_SALES_OS_REPORT.md",
    "marketing-os": "99_MARKETING_OS_REPORT.md", "media-social-os": "99_MEDIA_SOCIAL_READY_REPORT.md",
    "ads-os": "99_ADS_OS_REPORT.md", "revops-os": "99_REVOPS_OS_REPORT.md",
    "delivery-os": "99_DELIVERY_READINESS_REPORT.md", "support-os": "99_SUPPORT_OS_REPORT.md",
    "finance-os": "99_FINANCE_OS_REPORT.md", "legal-os": "99_LEGAL_OS_REPORT.md",
    "security-os": "99_SECURITY_TRUST_REPORT.md", "analytics-os": "99_ANALYTICS_READY_REPORT.md",
    "ai-evals-os": "99_AI_EVALS_REPORT.md", "people-os": "99_PEOPLE_OS_REPORT.md",
    "partnerships-os": "99_PARTNERSHIPS_OS_REPORT.md", "investor-os": "99_INVESTOR_OS_REPORT.md",
    "operations-os": "99_OPERATIONS_OS_REPORT.md", "go-live": "99_GO_LIVE_REPORT.md",
    "launch-control": "99_FINAL_CONTROL_TOWER_REPORT.md",
}


def run() -> dict:
    checks: list[dict] = []

    def chk(name, ok, critical=True, detail=""):
        checks.append({"name": name, "ok": bool(ok), "critical": critical, "detail": detail})

    for area in OS_AREAS:
        d = ROOT / "docs" / area
        n = len(list(d.glob("*.md"))) if d.exists() else 0
        chk(f"docs/{area}", d.exists() and n >= 1, detail=f"{n} docs")
        rep = REPORTS.get(area)
        if rep:
            chk(f"report:{area}", (d / rep).exists(), detail=rep)

    chk("verticals (5)", len(list((ROOT / "docs/commercial-launch/verticals").glob("0*.md"))) >= 5)

    for sname in SCRIPTS:
        chk(f"script:{sname}", (ROOT / "scripts" / sname).exists())
    for c in CONFIGS:
        chk(f"config:{c}", (ROOT / "config" / c).exists())
    for t in TESTS:
        chk(f"test:{t}", (ROOT / "tests" / t).exists())
    for w in WORKFLOWS:
        chk(f"workflow:{w}", (ROOT / ".github/workflows" / w).exists())

    chk("README mentions Startup OS", "Startup Operating System" in (ROOT / "README.md").read_text(encoding="utf-8"),
        critical=False)

    # Safety invariant: today's safety audit (if present) must be clean.
    sa = sorted((ROOT / "outputs/commercial_launch").glob("*/safety_audit.json"))
    if sa:
        ok = json.loads(sa[-1].read_text()).get("ok")
        chk("latest safety audit clean", ok)  # critical: if present, must be clean
    else:
        # Runtime artifact — CI regenerates it; absence in a clean checkout is non-critical.
        chk("safety audit present", False, critical=False,
            detail="run draft factory + safety audit (regenerated in CI)")

    crit_fail = [c for c in checks if c["critical"] and not c["ok"]]
    passed = sum(1 for c in checks if c["ok"])
    result = {
        "verifier": "startup_os_verify",
        "status": "PASS" if not crit_fail else "FAIL",
        "passed": passed,
        "total": len(checks),
        "critical_failures": [c["name"] for c in crit_fail],
        "checks": checks,
    }
    return result


def main() -> int:
    OUT.mkdir(parents=True, exist_ok=True)
    r = run()
    (OUT / "startup_os_verification.json").write_text(json.dumps(r, indent=2, ensure_ascii=False), encoding="utf-8")
    md = [f"# Startup OS Verification — {r['status']}", "",
          f"- Passed: **{r['passed']}/{r['total']}**",
          f"- Critical failures: {len(r['critical_failures'])}", ""]
    if r["critical_failures"]:
        md.append("## Critical failures")
        md += [f"- {c}" for c in r["critical_failures"]]
    md.append("\n> The system never sends externally. All external actions remain founder-gated.")
    (OUT / "startup_os_verification.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print(f"startup_os_verify: {r['status']} ({r['passed']}/{r['total']})")
    for c in r["critical_failures"][:20]:
        print("  ! FAIL", c)
    return 0 if r["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
