"""Verify the full Dealix Execution & Market Launch Command System.

Runs structural checks on:
  - Launch docs
  - Daily brief / weekly review / revenue forecast scripts
  - Machine registry (delegates to verify_machine_registry.py)
  - Risk docs + risk register CSV bootstrap template (if present)
  - Acquisition playbooks
  - Launch readiness verifier (delegates to verify_launch_readiness.py)
  - Learning docs
  - Makefile commands
  - Launch frontend page (if apps/web exists)
  - No guaranteed-claim language in execution docs

Exit:
  0 — PASS.
  1 — FAIL.
"""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


REPO = Path(__file__).resolve().parent.parent


FORBIDDEN_PHRASES = [
    r"\bguaranteed\s+(revenue|sales|results|meetings|roi)\b",
    r"\b(garant(eed|ie)|ضمان|نضمن|مضمون(ة)?)\s+(دخل|إيراد|أرباح|مبيعات|نتائج|اجتماع)",
]


DOCS = {
    "docs/launch": [
        "LAUNCH_COMMAND_CENTER.md",
        "MARKET_ENTRY_READINESS_GATE.md",
        "LAUNCH_SCORECARD.md",
        "LAUNCH_CAMPAIGN_SYSTEM.md",
        "LAUNCH_OPERATING_RHYTHM.md",
        "GO_TO_MARKET_MASTER_PLAN.md",
        "SAUDI_B2B_LAUNCH_PLAYBOOK.md",
        "LAUNCH_ASSET_CHECKLIST.md",
    ],
    "docs/founder": [
        "CEO_DAILY_BRIEF_SYSTEM.md",
        "CEO_DECISION_PROTOCOL.md",
        "FOUNDER_OPERATING_RHYTHM.md",
    ],
    "docs/growth": [
        "WEEKLY_GROWTH_WAR_ROOM.md",
        "GROWTH_REVIEW_PROTOCOL.md",
        "KILL_FIX_SCALE_DECISION_SYSTEM.md",
    ],
    "docs/ops": [
        "MACHINE_OWNERSHIP_MATRIX.md",
        "MACHINE_HEALTH_STANDARD.md",
        "MACHINE_FAILURE_PLAYBOOK.md",
    ],
    "docs/risk": [
        "DEALIX_RISK_REGISTER.md",
        "MARKET_ENTRY_RISK_MODEL.md",
        "AI_AGENT_RISK_MODEL.md",
        "REVENUE_RISK_MODEL.md",
        "OPERATING_RISK_MODEL.md",
    ],
    "docs/finance": [
        "REVENUE_FORECASTING_SYSTEM.md",
        "PIPELINE_WEIGHTING_MODEL.md",
        "CASH_COMMAND_CENTER.md",
    ],
    "docs/playbooks": [
        "ERP_CRM_ACQUISITION_PLAYBOOK.md",
        "CYBERSECURITY_ACQUISITION_PLAYBOOK.md",
        "B2B_AGENCY_ACQUISITION_PLAYBOOK.md",
        "LOGISTICS_INDUSTRIAL_ACQUISITION_PLAYBOOK.md",
        "CONSULTING_DIGITAL_TRANSFORMATION_PLAYBOOK.md",
        "SAAS_SOFTWARE_ACQUISITION_PLAYBOOK.md",
        "ENTERPRISE_SERVICES_ACQUISITION_PLAYBOOK.md",
        "PARTNER_REFERRAL_PLAYBOOK.md",
        "ABM_STRATEGIC_ACCOUNT_PLAYBOOK.md",
    ],
    "docs/learning": [
        "DEALIX_LEARNING_MEMORY.md",
        "MARKET_LEARNING_LOG.md",
        "MESSAGE_LEARNING_LOG.md",
        "OFFER_LEARNING_LOG.md",
        "SECTOR_LEARNING_LOG.md",
    ],
}


SCRIPTS = [
    "generate_ceo_daily_brief.py",
    "generate_weekly_growth_review.py",
    "generate_revenue_forecast.py",
    "verify_machine_registry.py",
    "verify_launch_readiness.py",
    "verify_execution_launch_layer.py",
]


REQUIRED_MAKE_TARGETS = [
    "ceo-daily-brief",
    "weekly-growth-review",
    "revenue-forecast",
    "machine-registry",
    "launch-readiness",
    "execution-launch-layer",
]


def _exists(p: Path) -> bool:
    return p.exists()


def check_docs() -> list[str]:
    errs: list[str] = []
    for d, files in DOCS.items():
        base = REPO / d
        if not base.exists():
            errs.append(f"missing docs dir: {d}")
            continue
        for f in files:
            if not (base / f).exists():
                errs.append(f"missing doc: {d}/{f}")
    return errs


def check_scripts() -> list[str]:
    errs: list[str] = []
    for s in SCRIPTS:
        p = REPO / "scripts" / s
        if not p.exists():
            errs.append(f"missing script: scripts/{s}")
    return errs


def check_registry() -> list[str]:
    p = REPO / "registries" / "machine_registry.yaml"
    if not p.exists():
        return ["missing registries/machine_registry.yaml"]
    try:
        r = subprocess.run(
            [sys.executable, str(REPO / "scripts" / "verify_machine_registry.py")],
            capture_output=True, text=True, cwd=str(REPO),
        )
        if r.returncode != 0:
            return [f"machine_registry verification failed: {r.stdout.strip()} | {r.stderr.strip()}"]
    except Exception as exc:  # noqa: BLE001
        return [f"machine_registry verifier crashed: {exc!r}"]
    return []


def check_launch_readiness() -> list[str]:
    try:
        r = subprocess.run(
            [sys.executable, str(REPO / "scripts" / "verify_launch_readiness.py")],
            capture_output=True, text=True, cwd=str(REPO),
        )
        # launch_readiness is informative; we only fail if required-public checks fail.
        if r.returncode == 2:
            return [f"launch_readiness usage error: {r.stderr.strip()}"]
        if r.returncode == 1 and "decision=HOLD" in r.stdout:
            # PASS for the layer means files are present; HOLD on private/env is OK here.
            # But required public failures = failure.
            return [f"launch_readiness reports HOLD: {r.stdout.strip()}"]
    except Exception as exc:  # noqa: BLE001
        return [f"launch_readiness verifier crashed: {exc!r}"]
    return []


def check_makefile() -> list[str]:
    mf = REPO / "Makefile"
    if not mf.exists():
        return ["Makefile missing"]
    text = mf.read_text(encoding="utf-8", errors="ignore")
    missing = [t for t in REQUIRED_MAKE_TARGETS if not re.search(rf"^{re.escape(t)}:", text, re.M)]
    return [f"Makefile missing target: {t}" for t in missing]


def check_frontend() -> list[str]:
    web = REPO / "apps" / "web"
    if not web.exists():
        return []  # apps/web optional
    if not (web / "app" / "launch" / "page.tsx").exists():
        return ["missing apps/web/app/launch/page.tsx"]
    return []


def check_workflow() -> list[str]:
    wf = REPO / ".github" / "workflows" / "dealix-execution-launch-layer.yml"
    if not wf.exists():
        return ["missing workflow: .github/workflows/dealix-execution-launch-layer.yml"]
    return []


def check_no_guaranteed_claims() -> list[str]:
    """Scan execution docs for forbidden 'guaranteed' / 'مضمون' marketing language.

    We allow these words in negation contexts (e.g., 'No guaranteed revenue claims') —
    only flag when used as an active promise.
    """
    errs: list[str] = []
    targets: list[Path] = []
    for d in DOCS:
        targets.extend((REPO / d).glob("*.md"))
    for path in targets:
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for pattern in FORBIDDEN_PHRASES:
            for match in re.finditer(pattern, text, flags=re.IGNORECASE):
                # context window
                start = max(0, match.start() - 40)
                end = min(len(text), match.end() + 40)
                ctx = text[start:end].lower()
                if any(neg in ctx for neg in ["no ", "لا ", "بدون", "without", "never", "ممنوع"]):
                    continue
                errs.append(f"{path.relative_to(REPO)}: forbidden phrase '{match.group(0)}'")
    return errs


def main(argv: list[str] | None = None) -> int:
    errs: list[str] = []
    errs.extend(check_docs())
    errs.extend(check_scripts())
    errs.extend(check_registry())
    errs.extend(check_makefile())
    errs.extend(check_frontend())
    errs.extend(check_workflow())
    errs.extend(check_launch_readiness())
    errs.extend(check_no_guaranteed_claims())

    if errs:
        sys.stdout.write("[fail] execution-launch-layer verification:\n")
        for e in errs:
            sys.stdout.write(f"  - {e}\n")
        return 1
    sys.stdout.write("[pass] Dealix Execution & Market Launch Command System verified.\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
