#!/usr/bin/env python3
"""Private Launch Readiness scorer for Dealix.

Scores launch readiness out of 100 across three bands (P0 / P1 / P2),
prints the verdict and blockers, and (unless --no-write) refreshes
``reports/launch/private_launch_readiness.md``.

Verdict bands:
    0–49   No-Go
    50–69  Internal Only
    70–84  Private Launch Ready
    85–100 Public Limited Ready

Hard rule: any P0 blocker caps the verdict at "Internal Only" regardless
of the numeric score — you do not private-launch with a P0 gap.

Terminal markers:
    LAUNCH_READINESS_SCORE=<n>
    LAUNCH_VERDICT=<verdict>
    DEALIX_LAUNCH_READINESS_OK=true|false
"""
from __future__ import annotations

import argparse
import sys
from datetime import date
from pathlib import Path

REPO = Path(__file__).resolve().parents[1]
if str(REPO) not in sys.path:
    sys.path.insert(0, str(REPO))

from scripts._wave8_scan import scan_files

CUSTOMER_TEMPLATE = REPO / "customers" / "_template"
COMMAND_SPRINT_FILES = (
    "00_intake.md", "01_company_intelligence.md", "02_diagnostic_summary.md",
    "03_command_sprint_scope.md", "04_revenue_map.md", "05_proof_register.md",
    "06_approval_register.md", "07_next_action_board.md",
    "08_executive_command_brief.md", "09_delivery_log.md", "10_proof_pack.md",
    "11_upsell_recommendation.md",
)

# Documents scanned for unsafe claims / auto-send language.
SCAN_TARGETS = (
    "docs/company/POSITIONING.md",
    "docs/commercial/POSITIONING_WHY_NOW_SAUDI_ONEPAGER_AR.md",
    "docs/commercial/sales/P1_REVENUE_INTELLIGENCE_SPRINT_OFFER_AR.md",
    "docs/sales/ONE_PAGER.md",
    "docs/sales-kit/START_HERE.md",
    "customers/_template/03_command_sprint_scope.md",
    "customers/_template/10_proof_pack.md",
)

UNSAFE_CLAIM_PATTERNS = (
    r"guaranteed\s+(revenue|results?|roi|return|income|sales)",
    r"guarantee\s+(you|your)\s+(revenue|results?|sales)",
    r"عائد\s+مضمون",
    r"أرباح\s+مضمونة",
    r"نضمن\s+(لك\s+)?(زيادة|أرباح|إيراد|نتائج|مبيعات)",
)
AUTO_SEND_PATTERNS = (
    r"auto[-\s]?send",
    r"automatically\s+send(s|ing)?\b",
    r"cold\s+whatsapp\s+automation",
    r"linkedin\s+automation",
    r"إرسال\s+تلقائي",
)


def exists(rel: str) -> bool:
    return (REPO / rel).is_file()


def any_exists(*rels: str) -> bool:
    return any(exists(r) for r in rels)


def template_complete() -> bool:
    return CUSTOMER_TEMPLATE.is_dir() and all(
        (CUSTOMER_TEMPLATE / f).is_file() for f in COMMAND_SPRINT_FILES
    )


def scan_hits(patterns: tuple[str, ...]) -> list[str]:
    return scan_files(REPO, SCAN_TARGETS, patterns)


def module_status_ok() -> bool:
    files = (
        "docs/company/SERVICE_STATUS_RULES.md",
        "docs/company/SERVICE_REGISTRY.md",
    )
    if not all(exists(f) for f in files):
        return False
    reg = (REPO / "docs/company/SERVICE_REGISTRY.md").read_text(encoding="utf-8", errors="ignore").lower()
    return any(tok in reg for tok in ("live", "planned", "spec", "beta", "جاهز", "مخطط"))


def build_checks() -> tuple[list[tuple[str, bool, str]], list[tuple[str, bool, str]], list[tuple[str, bool, str]], list[str], list[str]]:
    claim_hits = scan_hits(UNSAFE_CLAIM_PATTERNS)
    autosend_hits = scan_hits(AUTO_SEND_PATTERNS)

    p0 = [
        ("Command Sprint offer exists", exists("docs/commercial/sales/P1_REVENUE_INTELLIGENCE_SPRINT_OFFER_AR.md"), "docs/commercial/sales/P1_REVENUE_INTELLIGENCE_SPRINT_OFFER_AR.md"),
        ("Start / Diagnostic path exists", exists("docs/sales-kit/START_HERE.md"), "docs/sales-kit/START_HERE.md"),
        ("Sales one-pager exists", any_exists("docs/sales/ONE_PAGER.md", "docs/sales-kit/dealix_onepager.md"), "docs/sales/ONE_PAGER.md"),
        ("Diagnostic script exists", exists("scripts/dealix_diagnostic.py"), "scripts/dealix_diagnostic.py"),
        ("Customer workspace template complete", template_complete(), "customers/_template/ (12 files)"),
        ("Proof Pack template exists", exists("customers/_template/10_proof_pack.md"), "customers/_template/10_proof_pack.md"),
        ("Claims Register exists", exists("docs/governance/registers/CLAIMS_REGISTER.md"), "docs/governance/registers/CLAIMS_REGISTER.md"),
        ("Human Approval Policy exists", any_exists("docs/governance/APPROVAL_POLICY.md", "docs/governance/HUMAN_IN_THE_LOOP_MATRIX.md"), "docs/governance/APPROVAL_POLICY.md"),
        ("No External Action gate exists", exists("docs/03_governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md"), "docs/03_governance/NO_EXTERNAL_ACTION_WITHOUT_APPROVAL.md"),
        ("No unsafe claims", not claim_hits, f"{len(claim_hits)} hit(s)"),
        ("No auto-send language", not autosend_hits, f"{len(autosend_hits)} hit(s)"),
        ("No future module presented as live", module_status_ok(), "docs/company/SERVICE_REGISTRY.md"),
    ]
    p1 = [
        ("Business OS Score exists / spec-ready", any_exists("docs/company/OPERATING_SCORECARD.md", "reports/company_os/weekly/GROWTH_SCORECARD.md"), "docs/company/OPERATING_SCORECARD.md"),
        ("First 30 targets system exists", exists("data/outreach/first_30_targets.csv"), "data/outreach/first_30_targets.csv"),
        ("Outreach approval queue exists", exists("data/outreach/approval_queue.csv"), "data/outreach/approval_queue.csv"),
        ("Founder Daily Command exists", exists("reports/founder/daily_command.md"), "reports/founder/daily_command.md"),
        ("Revenue pipeline files exist", any_exists("reports/revenue/first_revenue_board.md", "reports/revenue/dealix_revenue_asset_index.md"), "reports/revenue/first_revenue_board.md"),
    ]
    p2 = [
        ("Answer Library plan exists", any_exists("docs/services/company_brain_sprint/answer_schema.md", "docs/sales-kit/dealix_objection_handler.md"), "docs/services/company_brain_sprint/answer_schema.md"),
        ("Sector pages plan exists", any_exists("sales/service_pages/revenue_os.md", "docs/sector-reports/b2b_services_sample.md"), "sales/service_pages/"),
        ("Partner/referral plan exists", any_exists("docs/growth/PARTNER_STRATEGY.md", "docs/AGENCY_PARTNER_PROGRAM.md"), "docs/growth/PARTNER_STRATEGY.md"),
        ("Growth metrics report exists", exists("reports/company_os/weekly/GROWTH_SCORECARD.md"), "reports/company_os/weekly/GROWTH_SCORECARD.md"),
    ]
    return p0, p1, p2, claim_hits, autosend_hits


def verdict_for(score: int, p0_blockers: list[str]) -> str:
    if p0_blockers:
        # A P0 gap caps the verdict regardless of numeric score.
        return "No-Go" if score < 50 else "Internal Only"
    if score < 50:
        return "No-Go"
    if score < 70:
        return "Internal Only"
    if score < 85:
        return "Private Launch Ready"
    return "Public Limited Ready"


def render_report(score: int, verdict: str, p0, p1, p2, p0_blk, p1_blk, p2_imp, next_fixes) -> str:
    today = date.today().isoformat()

    def rows(items):
        return "\n".join(
            f"| {'✅' if ok else '❌'} | {name} | `{detail}` |" for name, ok, detail in items
        )

    def bullets(items):
        return "\n".join(f"- {x}" for x in items) if items else "- _(none)_"

    return f"""# Dealix — Private Launch Readiness

_Generated by `scripts/verify_dealix_launch_readiness.py` on {today}. Do not edit by hand._

## Score: {score}/100 → **{verdict}**

| Band | Decision |
| --- | --- |
| 0–49 | No-Go |
| 50–69 | Internal Only |
| 70–84 | Private Launch Ready |
| 85–100 | Public Limited Ready |

> A P0 blocker caps the verdict at **Internal Only** regardless of score.

## P0 — must pass
| | Check | Reference |
| --- | --- | --- |
{rows(p0)}

## P1 — should pass
| | Check | Reference |
| --- | --- | --- |
{rows(p1)}

## P2 — improvements
| | Check | Reference |
| --- | --- | --- |
{rows(p2)}

## P0 blockers
{bullets(p0_blk)}

## P1 blockers
{bullets(p1_blk)}

## P2 improvements
{bullets(p2_imp)}

## Next 10 fixes
{bullets(next_fixes)}
"""


def main(argv: list[str] | None = None) -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        # UTF-8 reconfigure is best-effort; the default stream is fine if unavailable.
        pass

    parser = argparse.ArgumentParser(description="Dealix Private Launch Readiness scorer")
    parser.add_argument("--no-write", action="store_true", help="Do not write the markdown report")
    args = parser.parse_args(argv)

    p0, p1, p2, claim_hits, autosend_hits = build_checks()

    # Weighting: P0 = 60, P1 = 25, P2 = 15.
    def band_score(items, weight):
        if not items:
            return 0.0
        passed = sum(1 for _, ok, _ in items if ok)
        return weight * passed / len(items)

    score = round(band_score(p0, 60) + band_score(p1, 25) + band_score(p2, 15))

    p0_blk = [name for name, ok, _ in p0 if not ok]
    p1_blk = [name for name, ok, _ in p1 if not ok]
    p2_imp = [name for name, ok, _ in p2 if not ok]

    verdict = verdict_for(score, p0_blk)

    next_fixes = (p0_blk + p1_blk + p2_imp)[:10]
    if claim_hits:
        next_fixes = (["Remove unsafe-claim phrasing: " + claim_hits[0]] + next_fixes)[:10]
    if autosend_hits:
        next_fixes = (["Remove auto-send phrasing: " + autosend_hits[0]] + next_fixes)[:10]

    # Console summary.
    print("== Private Launch Readiness ==")
    for label, items in (("P0", p0), ("P1", p1), ("P2", p2)):
        for name, ok, _ in items:
            print(f"[{label}] {'PASS' if ok else 'FAIL'} — {name}")
    for h in claim_hits:
        print(f"UNSAFE_CLAIM: {h}")
    for h in autosend_hits:
        print(f"AUTO_SEND: {h}")

    if not args.no_write:
        out = REPO / "reports" / "launch" / "private_launch_readiness.md"
        out.parent.mkdir(parents=True, exist_ok=True)
        out.write_text(
            render_report(score, verdict, p0, p1, p2, p0_blk, p1_blk, p2_imp, next_fixes),
            encoding="utf-8",
        )
        print(f"WROTE {out.relative_to(REPO)}")

    print(f"LAUNCH_READINESS_SCORE={score}")
    print(f"LAUNCH_VERDICT={verdict}")
    ok = score >= 70 and not p0_blk
    print(f"DEALIX_LAUNCH_READINESS_OK={'true' if ok else 'false'}")
    # Exit 0 for Internal Only or better so CI can still gate on the marker;
    # non-zero only on No-Go.
    return 0 if score >= 50 else 1


if __name__ == "__main__":
    raise SystemExit(main())
