#!/usr/bin/env python3
"""Single pass/fail gate for the Founder/CEO Hypergrowth Operating Layer.

Final stdout line: HYPERGROWTH_LAYER_VERDICT=OK or HYPERGROWTH_LAYER_VERDICT=FAIL.
Exit code: 0 on OK, 1 on FAIL. PRIVATE_OPS being disabled is a WARNING, not a
failure, so this verifier stays green in CI without runtime data.
"""
from __future__ import annotations

import argparse
import ast
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

DOCS_P0 = [
    "docs/founder/INDEX.md",
    "docs/founder/CEO_OPERATING_SYSTEM.md",
    "docs/founder/CEO_DAILY_BRIEF_SYSTEM.md",
    "docs/founder/CEO_WEEKLY_REVIEW.md",
    "docs/founder/DECISION_LOG_SYSTEM.md",
    "docs/founder/STRATEGIC_ASSUMPTIONS_REGISTER.md",
    "docs/founder/FOUNDER_LEVERAGE_DASHBOARD.md",
    "docs/founder/FOUNDER_TIME_AUDIT.md",
    "docs/founder/DELEGATION_DECISION_TREE.md",
    "docs/founder/CEO_ATTENTION_BUDGET.md",
    "docs/founder/DO_NOT_SAY.md",
    "docs/finance/INDEX.md",
    "docs/finance/CAPITAL_ALLOCATION_SYSTEM.md",
    "docs/finance/ROI_PRIORITY_MATRIX.md",
    "docs/finance/FOUNDER_HOUR_ROI.md",
    "docs/finance/HIRE_VS_AUTOMATE_VS_PARTNER.md",
    "docs/metrics/INDEX.md",
    "docs/metrics/HYPERGROWTH_METRICS_SYSTEM.md",
    "docs/people/INDEX.md",
    "docs/people/DELEGATION_SYSTEM.md",
    "docs/people/FOUNDER_BOTTLENECK_REMOVAL.md",
    "docs/people/HIRING_TRIGGER_SYSTEM.md",
    "docs/strategy/DEALIX_GOAL_TREE.md",
    "docs/strategy/NORTH_STAR_METRIC.md",
    "docs/strategy/KPI_DEFINITION_DICTIONARY.md",
    "docs/revenue/REVENUE_LEADERSHIP_SYSTEM.md",
    "docs/revenue/PIPELINE_REVIEW_RHYTHM.md",
    "docs/revenue/DEAL_DESK_SYSTEM.md",
    "docs/revenue/PRICING_COUNCIL.md",
    "docs/revenue/WIN_LOSS_REVIEW.md",
    "docs/revenue/CLOSE_PLAN_TEMPLATE.md",
]

DOCS_P1 = [
    "docs/strategy/BEACHHEAD_SECTOR_SCORECARD.md",
    "docs/strategy/STRATEGIC_ACCOUNT_LIST.md",
    "docs/revenue/PAYMENT_CAPTURE_OS.md",
    "docs/revenue/REVENUE_FACTORY_LIVE_DATA.md",
    "docs/enterprise/ENTERPRISE_SALES_MOTION.md",
    "docs/enterprise/PROCUREMENT_READINESS.md",
    "docs/enterprise/STAKEHOLDER_MAP.md",
    "docs/enterprise/SECURITY_REVIEW_PACKET.md",
    "docs/enterprise/ENTERPRISE_PROPOSAL_FLOW.md",
    "docs/enterprise/MULTI_THREADING_SYSTEM.md",
]

ALL_DOCS = DOCS_P0 + DOCS_P1

INDEX_DIRS = [
    "docs/founder",
    "docs/finance",
    "docs/metrics",
    "docs/people",
]

SCRIPTS = [
    "scripts/founder_ceo_daily_brief.py",
    "scripts/founder_leverage_dashboard.py",
    "scripts/capital_allocation_snapshot.py",
    "scripts/founder_decision_log_append.py",
    "scripts/strategic_assumptions_check.py",
    "scripts/beachhead_sector_scorecard.py",
    "scripts/enterprise_motion_health.py",
    "scripts/verify_founder_ceo_hypergrowth_layer.py",
]

API_ROUTERS = [
    "api/routers/founder_ceo_os.py",
    "api/routers/founder_leverage.py",
    "api/routers/founder_capital_allocation.py",
]

FRONTEND_PAGES = [
    "frontend/src/app/[locale]/ceo-os/page.tsx",
    "frontend/src/app/[locale]/founder-leverage/page.tsx",
    "frontend/src/app/[locale]/capital-allocation/page.tsx",
    "frontend/src/app/[locale]/strategy/page.tsx",
    "frontend/src/app/[locale]/deal-desk/page.tsx",
    "frontend/src/app/[locale]/enterprise-sales/page.tsx",
    "frontend/src/app/[locale]/metrics/page.tsx",
]

FRONTEND_COMPONENTS = [
    "frontend/src/components/founder-ceo/CeoOsHub.tsx",
    "frontend/src/components/founder-ceo/FounderLeveragePanel.tsx",
    "frontend/src/components/founder-ceo/CapitalAllocationPanel.tsx",
    "frontend/src/components/founder-ceo/StrategyAssumptionsPanel.tsx",
    "frontend/src/components/founder-ceo/DealDeskPanel.tsx",
    "frontend/src/components/founder-ceo/EnterpriseSalesPanel.tsx",
    "frontend/src/components/founder-ceo/HypergrowthMetricsPanel.tsx",
    "frontend/src/components/founder-ceo/CeoOsSection.tsx",
]

BRAND_TOKENS = [
    "frontend/src/lib/brand-tokens.json",
    "frontend/src/lib/brand-tokens.ts",
]

MAKE_TARGETS = [
    "bootstrap-runtime",
    "hyper-verify",
    "hyper-daily-brief",
    "hyper-leverage",
    "hyper-capital",
    "hyper-assumptions",
    "hyper-sectors",
    "hyper-enterprise",
]

WORKFLOW = ".github/workflows/founder_ceo_hypergrowth.yml"

PRIVATE_OPS_EXPORTS = [
    "private_ops_root",
    "is_enabled",
    "resolve_csv",
    "resolve_jsonl",
    "write_jsonl_append",
    "missing_private_ops_note",
    "bootstrap_skeleton",
]

DO_NOT_SAY_PHRASES = [
    r"guaranteed revenue",
    r"guaranteed roi",
    r"we guarantee",
    r"we will pay you back",
    r"auto[- ]send",
    r"automated outreach",
    r"scraped",
    r"we transfer funds on behalf of",
    r"نضمن",
    r"مضمون",
]

EXTERNAL_VERBS = [
    r"\.send\(",
    r"\.publish\(",
    r"\.broadcast\(",
    r"sendOutreach",
    r"broadcastNow",
]

PAYMENT_DISCLAIMER_FRAGMENT = (
    "records intent only"
)


def check(name: str, ok: bool, detail: str = "") -> tuple[str, bool, str]:
    return (name, ok, detail)


def has_h1(p: Path) -> bool:
    try:
        with p.open("r", encoding="utf-8") as fh:
            for line in fh:
                if line.startswith("# "):
                    return True
                if line.strip() and not line.startswith("#"):
                    return False
    except OSError:
        return False
    return False


def has_relative_link(p: Path) -> bool:
    try:
        text = p.read_text(encoding="utf-8")
    except OSError:
        return False
    return bool(re.search(r"\]\((?!https?:)[^)]+\.md[^)]*\)", text))


def regex_in_text(patterns: list[str], text: str) -> list[str]:
    hits: list[str] = []
    lowered = text.lower()
    for pat in patterns:
        if re.search(pat, lowered, flags=re.IGNORECASE):
            hits.append(pat)
    return hits


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON summary")
    args = parser.parse_args()

    results: list[tuple[str, bool, str]] = []
    warnings: list[str] = []

    # 1. Doc completeness + H1
    for rel in ALL_DOCS:
        p = ROOT / rel
        if not p.exists():
            results.append(check(f"doc:exists:{rel}", False, "missing"))
            continue
        if p.stat().st_size == 0:
            results.append(check(f"doc:nonempty:{rel}", False, "empty"))
            continue
        if not has_h1(p):
            results.append(check(f"doc:h1:{rel}", False, "no h1 header"))
            continue
        results.append(check(f"doc:ok:{rel}", True, ""))

    # 2. Each new doc has at least one relative md link
    for rel in ALL_DOCS:
        p = ROOT / rel
        if not p.exists():
            continue
        if not has_relative_link(p):
            results.append(check(f"doc:crosslink:{rel}", False, "no relative .md link"))

    # 3. INDEX.md exists in each new dir
    for d in INDEX_DIRS:
        p = ROOT / d / "INDEX.md"
        results.append(check(f"index:{d}", p.exists(), "" if p.exists() else "missing"))

    # 4. Scripts exist + AST-parse
    for rel in SCRIPTS:
        p = ROOT / rel
        if not p.exists():
            results.append(check(f"script:exists:{rel}", False, "missing"))
            continue
        try:
            ast.parse(p.read_text(encoding="utf-8"))
            results.append(check(f"script:parse:{rel}", True, ""))
        except SyntaxError as exc:
            results.append(check(f"script:parse:{rel}", False, str(exc)))

    # 5. Private ops helper present + exports correct surface
    helper = ROOT / "dealix/private_ops.py"
    if helper.exists():
        text = helper.read_text(encoding="utf-8")
        missing = [n for n in PRIVATE_OPS_EXPORTS if f"def {n}(" not in text]
        results.append(check(
            "helper:dealix/private_ops.py",
            not missing,
            "" if not missing else f"missing exports: {missing}",
        ))
    else:
        results.append(check("helper:dealix/private_ops.py", False, "missing"))

    # 6. API routers registered in api/main.py
    main_py = ROOT / "api/main.py"
    if main_py.exists():
        main_text = main_py.read_text(encoding="utf-8")
        for rel in API_ROUTERS:
            mod = rel.removeprefix("api/routers/").removesuffix(".py")
            imp_ok = f"import {mod}" in main_text or f"from api.routers import {mod}" in main_text
            inc_ok = f"{mod}_router.router" in main_text or f"{mod}.router" in main_text
            results.append(check(
                f"router:registered:{mod}",
                imp_ok and inc_ok,
                "" if (imp_ok and inc_ok) else f"import={imp_ok} include={inc_ok}",
            ))
    else:
        results.append(check("api/main.py", False, "missing"))

    # 7. Frontend pages + components exist
    for rel in FRONTEND_PAGES + FRONTEND_COMPONENTS + BRAND_TOKENS:
        p = ROOT / rel
        results.append(check(f"frontend:{rel}", p.exists(), "" if p.exists() else "missing"))

    # 8. Makefile contains targets
    makefile = ROOT / "Makefile"
    if makefile.exists():
        mtext = makefile.read_text(encoding="utf-8")
        for target in MAKE_TARGETS:
            pat = re.compile(rf"^{re.escape(target)}:", re.MULTILINE)
            results.append(check(
                f"make:{target}",
                bool(pat.search(mtext)),
                "" if pat.search(mtext) else "target not found",
            ))
    else:
        results.append(check("Makefile", False, "missing"))

    # 9. Workflow exists + workflow_dispatch
    wf = ROOT / WORKFLOW
    if wf.exists():
        wtext = wf.read_text(encoding="utf-8")
        results.append(check(
            "workflow:founder_ceo_hypergrowth.yml",
            "workflow_dispatch" in wtext,
            "" if "workflow_dispatch" in wtext else "no workflow_dispatch trigger",
        ))
    else:
        results.append(check("workflow:founder_ceo_hypergrowth.yml", False, "missing"))

    # 10. Non-negotiables regex check on all new docs
    for rel in ALL_DOCS:
        p = ROOT / rel
        if not p.exists():
            continue
        if rel.endswith("DO_NOT_SAY.md"):
            continue  # the policy file itself quotes the phrases
        text = p.read_text(encoding="utf-8")
        hits = regex_in_text(DO_NOT_SAY_PHRASES, text)
        if hits:
            results.append(check(
                f"doctrine:no_say:{rel}",
                False,
                f"forbidden phrases: {hits}",
            ))

    # 11. External-action grep on founder-ceo frontend components
    for rel in FRONTEND_COMPONENTS:
        p = ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        hits = regex_in_text(EXTERNAL_VERBS, text)
        if hits:
            results.append(check(
                f"frontend:no_external_send:{rel}",
                False,
                f"external action verbs: {hits}",
            ))

    # 12. Payment disclaimer present in finance docs
    for rel in [
        "docs/finance/CAPITAL_ALLOCATION_SYSTEM.md",
        "docs/finance/ROI_PRIORITY_MATRIX.md",
    ]:
        p = ROOT / rel
        if not p.exists():
            continue
        text = p.read_text(encoding="utf-8")
        ok = PAYMENT_DISCLAIMER_FRAGMENT in text
        results.append(check(
            f"doctrine:payment_disclaimer:{rel}",
            ok,
            "" if ok else f"missing fragment '{PAYMENT_DISCLAIMER_FRAGMENT}'",
        ))

    # 13. PRIVATE_OPS status — warning only
    private_ops_root = os.environ.get("DEALIX_OPS_PRIVATE")
    if private_ops_root:
        root_path = Path(private_ops_root).expanduser()
        if not root_path.exists():
            warnings.append(f"PRIVATE_OPS env set but path missing: {private_ops_root}")
    else:
        warnings.append("PRIVATE_OPS=disabled (DEALIX_OPS_PRIVATE not set)")

    # Tally
    failed = [r for r in results if not r[1]]
    summary = {
        "total_checks": len(results),
        "passed": len(results) - len(failed),
        "failed": [{"check": n, "detail": d} for (n, ok, d) in failed if not ok],
        "warnings": warnings,
    }

    if args.json:
        print(json.dumps(summary, ensure_ascii=False, indent=2))
    else:
        for name, ok, detail in results:
            tag = "OK  " if ok else "FAIL"
            line = f"[{tag}] {name}"
            if detail:
                line += f" — {detail}"
            print(line)
        for w in warnings:
            print(f"[WARN] {w}")
        print()
        print(f"Total checks: {summary['total_checks']}  "
              f"Passed: {summary['passed']}  Failed: {len(failed)}")

    verdict = "OK" if not failed else "FAIL"
    print(f"HYPERGROWTH_LAYER_VERDICT={verdict}")
    return 0 if verdict == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
