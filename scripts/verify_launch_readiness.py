"""Verify Dealix Launch Asset Checklist (docs/launch/LAUNCH_ASSET_CHECKLIST.md).

Two scopes:
  - "public" — repo-only checks (always runnable in CI).
  - "private" — additionally checks <private_ops>/ artefacts when PRIVATE_OPS is set.

Emits machine-readable JSON on stdout + a human checklist on stderr.
Exit code:
  0 — PASS.
  1 — FAIL on required public checks.
  2 — usage error.
"""

from __future__ import annotations

import argparse
import json
import os
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent


def _check(name: str, condition: bool, detail: str = "") -> dict:
    return {"name": name, "ok": bool(condition), "detail": detail}


def public_checks() -> list[dict]:
    out: list[dict] = []
    # 1. Brand assets — docs/brand presence
    brand_dir = REPO / "docs" / "brand"
    out.append(_check("brand_dir_exists", brand_dir.exists(), str(brand_dir)))
    # 2. Brand tokens
    out.append(_check(
        "brand_tokens_doc",
        (brand_dir / "BRAND_TOKENS.md").exists() if brand_dir.exists() else False,
    ))
    # 3. Website / landing
    out.append(_check("apps_web_page", (REPO / "apps" / "web" / "app" / "page.tsx").exists()))
    # 4. Founder Console
    out.append(_check(
        "founder_console_page",
        (REPO / "apps" / "web" / "app" / "agents" / "page.tsx").exists(),
    ))
    # 5. Non-negotiables present
    out.append(_check(
        "non_negotiables_doc",
        (REPO / "docs" / "00_constitution" / "NON_NEGOTIABLES.md").exists(),
    ))
    # 6. Trust risks doc
    out.append(_check(
        "ai_agent_risk_model",
        (REPO / "docs" / "risk" / "AI_AGENT_RISK_MODEL.md").exists(),
    ))
    # 7. Launch docs
    for f in [
        "LAUNCH_COMMAND_CENTER.md",
        "MARKET_ENTRY_READINESS_GATE.md",
        "LAUNCH_SCORECARD.md",
        "LAUNCH_CAMPAIGN_SYSTEM.md",
        "LAUNCH_OPERATING_RHYTHM.md",
        "GO_TO_MARKET_MASTER_PLAN.md",
        "SAUDI_B2B_LAUNCH_PLAYBOOK.md",
        "LAUNCH_ASSET_CHECKLIST.md",
    ]:
        out.append(_check(f"launch_doc_{f}", (REPO / "docs" / "launch" / f).exists()))
    # 8. Founder docs
    for f in [
        "CEO_DAILY_BRIEF_SYSTEM.md",
        "CEO_DECISION_PROTOCOL.md",
        "FOUNDER_OPERATING_RHYTHM.md",
    ]:
        out.append(_check(f"founder_doc_{f}", (REPO / "docs" / "founder" / f).exists()))
    # 9. Growth docs
    for f in [
        "WEEKLY_GROWTH_WAR_ROOM.md",
        "GROWTH_REVIEW_PROTOCOL.md",
        "KILL_FIX_SCALE_DECISION_SYSTEM.md",
    ]:
        out.append(_check(f"growth_doc_{f}", (REPO / "docs" / "growth" / f).exists()))
    # 10. Ops docs
    for f in [
        "MACHINE_OWNERSHIP_MATRIX.md",
        "MACHINE_HEALTH_STANDARD.md",
        "MACHINE_FAILURE_PLAYBOOK.md",
    ]:
        out.append(_check(f"ops_doc_{f}", (REPO / "docs" / "ops" / f).exists()))
    # 11. Risk docs
    for f in [
        "DEALIX_RISK_REGISTER.md",
        "MARKET_ENTRY_RISK_MODEL.md",
        "AI_AGENT_RISK_MODEL.md",
        "REVENUE_RISK_MODEL.md",
        "OPERATING_RISK_MODEL.md",
    ]:
        out.append(_check(f"risk_doc_{f}", (REPO / "docs" / "risk" / f).exists()))
    # 12. Finance docs
    for f in [
        "REVENUE_FORECASTING_SYSTEM.md",
        "PIPELINE_WEIGHTING_MODEL.md",
        "CASH_COMMAND_CENTER.md",
    ]:
        out.append(_check(f"finance_doc_{f}", (REPO / "docs" / "finance" / f).exists()))
    # 13. Playbooks
    for f in [
        "ERP_CRM_ACQUISITION_PLAYBOOK.md",
        "CYBERSECURITY_ACQUISITION_PLAYBOOK.md",
        "B2B_AGENCY_ACQUISITION_PLAYBOOK.md",
        "LOGISTICS_INDUSTRIAL_ACQUISITION_PLAYBOOK.md",
        "CONSULTING_DIGITAL_TRANSFORMATION_PLAYBOOK.md",
        "SAAS_SOFTWARE_ACQUISITION_PLAYBOOK.md",
        "ENTERPRISE_SERVICES_ACQUISITION_PLAYBOOK.md",
        "PARTNER_REFERRAL_PLAYBOOK.md",
        "ABM_STRATEGIC_ACCOUNT_PLAYBOOK.md",
    ]:
        out.append(_check(f"playbook_{f}", (REPO / "docs" / "playbooks" / f).exists()))
    # 14. Learning docs
    for f in [
        "DEALIX_LEARNING_MEMORY.md",
        "MARKET_LEARNING_LOG.md",
        "MESSAGE_LEARNING_LOG.md",
        "OFFER_LEARNING_LOG.md",
        "SECTOR_LEARNING_LOG.md",
    ]:
        out.append(_check(f"learning_doc_{f}", (REPO / "docs" / "learning" / f).exists()))
    # 15. Machine registry
    out.append(_check("machine_registry_yaml", (REPO / "registries" / "machine_registry.yaml").exists()))
    # 16. Scripts
    for s in [
        "generate_ceo_daily_brief.py",
        "generate_weekly_growth_review.py",
        "generate_revenue_forecast.py",
        "verify_machine_registry.py",
        "verify_launch_readiness.py",
        "verify_execution_launch_layer.py",
    ]:
        out.append(_check(f"script_{s}", (REPO / "scripts" / s).exists()))
    # 17. Workflow
    out.append(_check(
        "workflow_execution_launch_layer",
        (REPO / ".github" / "workflows" / "dealix-execution-launch-layer.yml").exists(),
    ))
    # 18. Frontend launch page
    out.append(_check(
        "launch_frontend_page",
        (REPO / "apps" / "web" / "app" / "launch" / "page.tsx").exists(),
    ))
    return out


def private_checks(private_ops: Path) -> list[dict]:
    out: list[dict] = []
    paths = [
        "sales/sample_offer.md",
        "sales/proposal_template.md",
        "sales/sales_script.md",
        "sales/objections.md",
        "launch/target_sector.yaml",
        "sales/lead_sources.csv",
        "distribution/queues.json",
        "distribution/approvals.csv",
        "distribution/suppression.csv",
        "distribution/followups.csv",
        "finance/cash_collected.csv",
        "risk/risk_register.csv",
        "ops/machine_health.csv",
        "trust/open_risks.csv",
    ]
    for rel in paths:
        full = private_ops / rel
        out.append(_check(f"private_{rel}", full.exists(), str(full)))
    return out


def env_checks() -> list[dict]:
    out: list[dict] = []
    out.append(_check("env_INTERNAL_ADMIN_KEY", bool(os.environ.get("INTERNAL_ADMIN_KEY"))))
    out.append(_check(
        "env_MOYASAR_SECRET_KEY",
        (os.environ.get("MOYASAR_SECRET_KEY") or "").startswith(("sk_test_", "sk_live_")),
    ))
    return out


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--private-ops", default=os.environ.get("PRIVATE_OPS") or os.environ.get("DEALIX_PRIVATE_OPS"))
    parser.add_argument("--strict-env", action="store_true", help="Fail on missing env (default: report only).")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args(argv)

    checks = public_checks()
    if args.private_ops:
        p = Path(args.private_ops).expanduser().resolve()
        if p.exists():
            checks.extend(private_checks(p))
    checks.extend(env_checks())

    required_failing = [c for c in checks if not c["ok"] and not c["name"].startswith(("private_", "env_"))]
    if args.strict_env:
        required_failing.extend([c for c in checks if not c["ok"] and c["name"].startswith("env_")])

    score = sum(1 for c in checks if c["ok"]) / max(1, len(checks))
    summary = {
        "total": len(checks),
        "passing": sum(1 for c in checks if c["ok"]),
        "failing": sum(1 for c in checks if not c["ok"]),
        "readiness_score": round(score, 3),
        "required_failing_count": len(required_failing),
        "decision": "PASS" if not required_failing else "HOLD",
        "checks": checks,
    }
    if args.json:
        sys.stdout.write(json.dumps(summary, ensure_ascii=False, indent=2))
        sys.stdout.write("\n")
    else:
        sys.stdout.write(f"[launch readiness] decision={summary['decision']} "
                         f"score={summary['readiness_score']} "
                         f"pass={summary['passing']}/{summary['total']}\n")
        for c in checks:
            mark = "[ok]" if c["ok"] else "[--]"
            sys.stderr.write(f"  {mark} {c['name']} {c.get('detail','')}\n")
    return 0 if not required_failing else 1


if __name__ == "__main__":
    raise SystemExit(main())
