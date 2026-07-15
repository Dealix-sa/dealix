from pathlib import Path

BANNED_TERMS = [
    "guaranteed revenue",
    "guaranteed sales",
    "fully compliant",
    "full legal compliance",
    "100% automated sales",
]

POLICY_CONTEXT_MARKERS = [
    "no ",
    "not ",
    "never",
    "without",
    "don't",
    "do not",
    "won't",
    "cannot",
    "can't",
    "must not",
    "should not",
    "shall not",
    "ban",
    "banned",
    "forbid",
    "forbidden",
    "prohibit",
    "prohibited",
    "refuse",
    "refusing",
    "refused",
    "avoid",
    "disallow",
    "disallowed",
    "block",
    "blocked",
    "reject",
    "rejected",
    "deny",
    "denied",
    "stop",
    "halt",
    "anti-",
    "anti ",
    "non-",
    "non ",
    "no-",
    "claim",
    "claims",
    "claiming",
    "claimed",
    "promise",
    "promises",
    "promising",
    "promised",
    "outcome",
    "outcomes",
    "wants",
    "want ",
    "seeking",
    "seek ",
    "unsupported",
    "false",
    "fake",
    "article 8",
    "❌",
    "policy",
    "illegal",
    "language",
    "violation",
    "violates",
    "breach",
    "forbidden_actions",
    "stop_doing",
    "non_negotiables",
    "scope_boundary",
]

EXCLUDED_PATH_FRAGMENTS = [
    "docs/governance/",
    "docs/00_foundation/",
    "docs/00_constitution/",
    "docs/responsible_ai/",
    "docs/trust/",
    "docs/quality/",
    "docs/team/founder_sop",
    "docs/board_decision_system/",
    "docs/from_zero/",
    "docs/sales-kit/",
    "docs/services/client_ai_policy_pack/",
    "docs/product/governance",
    "docs/product/agent_cards/",
    "docs/empire/trust",
    "docs/operating_empire/trust",
    "docs/knowledge-base/pricing_policy",
    "docs/26_service_catalog/",
    "docs/company/stop_doing",
    "docs/company/icp",
    "docs/sales/client_selection_decision",
    "docs/sales/qualification_engine",
    "docs/sales/proposal_system",
    "docs/sales/sales_messages",
    "docs/content/linkedin_cadence_plan",
    "docs/content/linkedin_post_001",
    "docs/growth/trust_page/",
    "docs/07_governance/",
    "docs/14_trust_os/",
    "docs/25_compliance_trust/",
    "docs/templates/proposal_body",
    "docs/v14_founder_daily_ops",
    "docs/strategic_master_plan_2026",
    "docs/wave6_revenue_activation_current_state",
    "docs/dealix_business_packaging_current_state",
    "docs/partner_legal_agreement",
    "docs/first_3_diagnostic_script",
    "docs/executive_decision_pack",
    "docs/v5_master_evidence_table",
    "docs/self_growth_os_package",
    "docs/sales_ops_sop",
    "docs/wave6_real_demo_runbook",
    "docs/v14_comprehensive_strategic_plan",
    "docs/commercial/dealix_commercial_scale_system_ar",
    "docs/commercial/operations/commercial_governance_gates_ar",
    "docs/company/dealix_master_operating_system",
    "docs/company/dealix_unified_executive_blueprint",
    "landing/llms.txt",
]

SCAN_DIRS = ["docs", "landing", "README.md"]


def is_excluded(path: Path) -> bool:
    s = str(path).replace("\\", "/").lower()
    return any(fragment in s for fragment in EXCLUDED_PATH_FRAGMENTS)


failures = []

for item in SCAN_DIRS:
    path = Path(item)
    files = [path] if path.is_file() else list(path.rglob("*"))
    for file in files:
        if not (file.is_file() and file.suffix.lower() in {".md", ".html", ".txt"}):
            continue
        if is_excluded(file):
            continue
        text = file.read_text(encoding="utf-8", errors="ignore")
        for raw_line in text.splitlines():
            line = raw_line.lower()
            for term in BANNED_TERMS:
                if term not in line:
                    continue
                if any(marker in line for marker in POLICY_CONTEXT_MARKERS):
                    continue
                failures.append(f"{file}: affirmative banned claim: {term}: {raw_line.strip()[:160]}")

if failures:
    print("Trust boundary terms failed:")
    for f in failures:
        print("-", f)
    raise SystemExit(1)

print("PASS: no banned trust terms found.")
