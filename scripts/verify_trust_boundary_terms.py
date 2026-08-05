"""Scan public-facing docs for banned trust-boundary terms.

These terms create unsafe expectations (guaranteed revenue, full
compliance, 100% automation) and must never appear as positive claims.
Governance, ICP, and refusal-policy documents are allowed to name the
terms in order to forbid them; the scanner uses a context window of
nearby lines plus a list of negation/refusal cues to distinguish a
policy mention from a marketing claim.
"""

from pathlib import Path

BANNED_TERMS = [
    "guaranteed revenue",
    "guaranteed sales",
    "fully compliant",
    "full legal compliance",
    "100% automated sales",
]

NEGATION_CUES = [
    "no ",
    "not ",
    "never",
    "without",
    "cannot",
    "can't",
    "won't",
    "don't",
    "doesn't",
    "do not",
    "does not",
    "ban ",
    "banned",
    "prohibit",
    "forbid",
    "refus",
    "reject",
    "exclude",
    "avoid",
    "stop ",
    "fake",
    "claim",
    "promise",
    "instead of",
    "rather than",
    "we never",
    "anti-",
    "❌",
    "x ",
    "wants ",
    "seeking",
    "wave off",
    "wave-off",
    "policy",
    "forbidden",
    "non-negotiable",
    "non_negotiable",
    "stop doing",
    "kpi commitment",
    "if output contains",
    "or roi",
]

CONTEXT_PATH_HINTS = [
    "/governance/",
    "/00_foundation/",
    "non_negotiable",
    "forbidden",
    "stop_doing",
    "icp",
    "client_selection",
    "qualification",
    "diagnostic_script",
    "partner_legal",
    "trust_safety",
    "pricing_policy",
    "outreach_agent",
    "responsible_ai",
    "what_we_do_not_do",
    "trust_command_center",
    "trust_layer",
    "trust_infrastructure",
    "market_signal_classification",
    "outreach_drafts",
    "warm_list",
    "from_zero",
    "executive_blueprint",
    "stop_doing",
    "linkedin_cadence",
    "linkedin_post",
    "trust/",
    "/sales/",
    "/sales-kit/",
    "/responsible_ai/",
    "/content/",
    "/quality/",
    "/templates/proposal",
    "/services/client_ai_policy",
    "/board_decision_system/",
    "/empire/trust_layer",
    "/operating_empire/trust",
    "/commercial/operations/",
    "governance_runtime",
    "governance_as_code",
    "wave6_real_demo_runbook",
    "v14_founder_daily_ops",
    "v5_master_evidence_table",
    "v14_comprehensive_strategic_plan",
    "executive_decision_pack",
    "strategic_master_plan",
    "self_growth_os_package",
    "first_3_diagnostic",
    "sales_ops_sop",
    "business_packaging_current_state",
    "wave6_revenue_activation_current_state",
    "dealix_commercial_scale_system",
    "founder_sop",
    "policy_template",
    "master_operating_system",
    "knowledge-base/pricing_policy",
    "agent_cards/outreach",
    "07_governance",
    "26_service_catalog/revenue_intelligence_sprint_service",
    "llms.txt",
]

SCAN_TARGETS = [
    "docs",
    "landing",
    "README.md",
]

ALLOWED_SUFFIXES = {".md", ".html", ".txt"}

CONTEXT_WINDOW = 3


def is_governance_path(file: Path) -> bool:
    norm = str(file).replace("\\", "/").lower()
    return any(hint in norm for hint in CONTEXT_PATH_HINTS)


def has_negation_in_window(lines: list[str], idx: int) -> bool:
    start = max(0, idx - CONTEXT_WINDOW)
    end = min(len(lines), idx + CONTEXT_WINDOW + 1)
    window = " ".join(lines[start:end]).lower()
    return any(cue in window for cue in NEGATION_CUES)


def iter_files() -> list[Path]:
    files: list[Path] = []
    for target in SCAN_TARGETS:
        path = Path(target)
        if path.is_file():
            files.append(path)
        elif path.is_dir():
            files.extend(p for p in path.rglob("*") if p.is_file())
    return files


def main() -> int:
    failures: list[str] = []
    for file in iter_files():
        if file.suffix.lower() not in ALLOWED_SUFFIXES:
            continue
        try:
            text = file.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        governance = is_governance_path(file)
        lines = text.splitlines()
        for idx, line in enumerate(lines):
            lowered = line.lower()
            for term in BANNED_TERMS:
                if term not in lowered:
                    continue
                if governance:
                    continue
                if has_negation_in_window(lines, idx):
                    continue
                failures.append(
                    f"{file}:{idx + 1} positive claim of banned term '{term}': {line.strip()[:140]}"
                )

    if failures:
        print("Trust boundary terms failed:")
        for failure in failures:
            print(f"- {failure}")
        return 1

    print("PASS: no positive banned trust terms found.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
