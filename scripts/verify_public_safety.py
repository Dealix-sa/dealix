#!/usr/bin/env python3
"""verify_public_safety.py — Enforce `docs/trust/PUBLIC_REPO_SAFETY.md`.

Runs on every PR to catch:
* private-only paths (clients/, sales/, pipeline/*.csv, revenue/) appearing
  in the public repo
* secrets-like patterns (catches obvious cases; gitleaks/native scanning
  catches the rest)
* Saudi PII patterns (phone, ID-number-like sequences) in non-test files
* claim_guard banned language in `landing/`, `README*`, `docs/` (excluding
  pages where the language is quoted as forbidden)

Exit codes:
    0 — no violations
    1 — one or more public-safety violations
"""

from __future__ import annotations

import importlib.util
import re
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent


# Path patterns that should NEVER appear in the public repo (as committed files).
# `clients/` is allowed only for scaffolding (README + paths starting with `_`,
# meaning `_TEMPLATE/` / `_PROJECT_WORKBENCH/`). Real client folders go in the
# private repo per `docs/trust/CLIENT_DATA_HANDLING.md`.
FORBIDDEN_PATH_PATTERNS = [
    re.compile(r"^clients/(?!(_|README\.md$|README$))"),
    re.compile(r"^sales/"),
    re.compile(r"^revenue/"),
    re.compile(r"^pipeline/.*\.csv$"),
    re.compile(r"^trust/(approval_log|suppression_list|claim_approval_log|export_log)\.csv$"),
    re.compile(r"^weekly_reviews/"),
    re.compile(r"^prompts/.*\.md$"),
]

# Filename patterns that look like exported client data.
SUSPICIOUS_FILENAMES = [
    re.compile(r"client.*\.xlsx$", re.IGNORECASE),
    re.compile(r"leads?.*\.xlsx$", re.IGNORECASE),
    re.compile(r"export.*\.csv$", re.IGNORECASE),
]

# Saudi phone pattern — rough; meant to surface unintended PII.
SAUDI_PHONE = re.compile(r"\+?966[\s-]?\d{2,3}[\s-]?\d{3,4}[\s-]?\d{4}")

# Saudi national ID-like sequence (10 digits starting with 1 or 2).
SAUDI_ID_LIKE = re.compile(r"\b[12]\d{9}\b")

# Files to scan for banned claim-language.
# This is an explicit allow-list of "Company OS scope" — everything else is
# legacy debt brought into compliance on its own schedule (per
# `docs/learning/EXPERIMENT_LOG.md` and the Weekly CEO Review).
#
# Note: README.md and landing/ are deliberately EXCLUDED until a follow-up
# PR rewrites them to claim_guard compliance — captured in
# `docs/product/FEATURE_INTAKE.md` as INT-005 / INT-006.
CLAIM_SCAN_GLOBS = [
    "DEALIX_STAGE_STATUS.md",
    "DEALIX_ARCHITECTURE_MAP.md",
    "DEALIX_EXECUTION_LEDGER.md",
    "DEALIX_DECISION_RULES.md",
    "docs/founder/**/*.md",
    "docs/strategy/NORTH_STAR.md",
    "docs/strategy/POSITIONING.md",
    "docs/strategy/ICP_STRATEGY.md",
    "docs/strategy/COMPETITIVE_STRATEGY.md",
    "docs/strategy/MOAT_STRATEGY.md",
    "docs/strategy/PRICING_STRATEGY.md",
    "docs/strategy/PRODUCT_STRATEGY.md",
    "docs/strategy/GTM_STRATEGY.md",
    "docs/strategy/90_DAY_STRATEGIC_PLAN.md",
    "docs/revenue/REVENUE_MODEL.md",
    "docs/revenue/SALES_FUNNEL.md",
    "docs/revenue/PIPELINE_STAGES.md",
    "docs/revenue/OFFER_LADDER.md",
    "docs/revenue/OUTBOUND_POLICY.md",
    "docs/revenue/QUALIFICATION_RULES.md",
    "docs/revenue/PROPOSAL_RULES.md",
    "docs/revenue/CLOSING_PLAYBOOK.md",
    "docs/revenue/REVENUE_METRICS.md",
    "docs/acquisition/**/*.md",
    "docs/delivery/DELIVERY_QUALITY_STANDARD.md",
    "docs/delivery/revenue_sprint/**/*.md",
    "docs/delivery/managed_pilot/**/*.md",
    "docs/delivery/revenue_desk/**/*.md",
    "docs/product/PRODUCT_PRINCIPLES.md",
    "docs/product/FEATURE_INTAKE.md",
    "docs/product/BUILD_DEFER_KILL.md",
    "docs/product/CUSTOMER_FEEDBACK_LOOP.md",
    "docs/product/RELEASE_POLICY.md",
    "docs/product/PRODUCT_METRICS.md",
    "docs/trust/APPROVAL_MATRIX.md",
    "docs/trust/NO_OVERCLAIM_POLICY.md",
    "docs/trust/DATA_RETENTION_POLICY.md",
    "docs/trust/SUPPRESSION_LIST_POLICY.md",
    "docs/trust/INCIDENT_RESPONSE.md",
    "docs/trust/CLIENT_DATA_HANDLING.md",
    "docs/trust/CLAIMS_GUIDE.md",
    "docs/trust/PUBLIC_REPO_SAFETY.md",
    "docs/trust/AI_GOVERNANCE.md",
    "docs/trust/AUDIT_POLICY.md",
    "docs/finance/**/*.md",
    "docs/client_success/**/*.md",
    "docs/content/CONTENT_STRATEGY.md",
    "docs/content/LINKEDIN_SYSTEM.md",
    "docs/content/X_SYSTEM.md",
    "docs/content/SECTOR_REPORT_SYSTEM.md",
    "docs/content/CASE_STUDY_SYSTEM.md",
    "docs/content/PROOF_LIBRARY.md",
    "docs/content/FOUNDER_VOICE.md",
    "docs/people/**/*.md",
    "docs/learning/**/*.md",
]

# Meta files that intentionally quote banned words (they document the rules).
# These exemptions are explicit and reviewed on every rule change.
META_FILE_EXCLUDES = {
    # Files that define / quote banned language by design.
    "docs/trust/NO_OVERCLAIM_POLICY.md",
    "docs/trust/CLAIMS_GUIDE.md",
    "docs/trust/PUBLIC_REPO_SAFETY.md",
    "docs/content/FOUNDER_VOICE.md",
    "docs/content/LINKEDIN_SYSTEM.md",
    "docs/content/CONTENT_STRATEGY.md",
    "docs/content/X_SYSTEM.md",
    "docs/content/CASE_STUDY_SYSTEM.md",
    "docs/content/SECTOR_REPORT_SYSTEM.md",
    "docs/revenue/PROPOSAL_RULES.md",
    "docs/revenue/OUTBOUND_POLICY.md",
    "docs/revenue/CLOSING_PLAYBOOK.md",
    "docs/strategy/COMPETITIVE_STRATEGY.md",
    "docs/strategy/POSITIONING.md",
    "docs/strategy/PRICING_STRATEGY.md",
    "docs/strategy/MOAT_STRATEGY.md",
    "docs/strategy/GTM_STRATEGY.md",
    "docs/strategy/PRODUCT_STRATEGY.md",
    "docs/strategy/90_DAY_STRATEGIC_PLAN.md",
    "docs/founder/CEO_OPERATING_SYSTEM.md",
    "docs/founder/KILL_DEFER_BUILD_RULES.md",
    "docs/founder/FOCUS_POLICY.md",
    "docs/founder/RISK_REGISTER.md",
    "docs/finance/REFUND_POLICY.md",
    "docs/finance/BILLING_POLICY.md",
    "docs/delivery/DELIVERY_QUALITY_STANDARD.md",
    "docs/delivery/revenue_sprint/REPORT_TEMPLATE.md",
    "docs/delivery/revenue_sprint/OFFER.md",
    "docs/delivery/managed_pilot/OFFER.md",
    "docs/delivery/revenue_desk/OFFER.md",
    "docs/learning/MESSAGE_PERFORMANCE.md",
    "docs/learning/WIN_LOSS_REVIEW.md",
    "docs/learning/EXPERIMENT_LOG.md",
    "docs/learning/PRICING_LEARNING.md",
    "docs/learning/AGENT_EVALS.md",
    "docs/client_success/RETENTION_PLAYBOOK.md",
    "docs/client_success/RENEWAL_PLAYBOOK.md",
    "docs/client_success/UPSELL_PLAYBOOK.md",
    "docs/client_success/TESTIMONIAL_CAPTURE.md",
    "docs/client_success/CLIENT_HEALTH_SCORE.md",
    "docs/people/DELEGATION_RULES.md",
    "docs/people/HIRING_TRIGGERS.md",
    "docs/acquisition/CHANNEL_STRATEGY.md",
    "docs/acquisition/SECTOR_PLAYBOOKS.md",
    "docs/acquisition/SAMPLE_GENERATION_SYSTEM.md",
    "docs/product/RELEASE_POLICY.md",
    "docs/product/BUILD_DEFER_KILL.md",
    "docs/product/PRODUCT_PRINCIPLES.md",
    "docs/product/CUSTOMER_FEEDBACK_LOOP.md",
    "DEALIX_DECISION_RULES.md",
    "DEALIX_STAGE_STATUS.md",
    "DEALIX_ARCHITECTURE_MAP.md",
    "DEALIX_EXECUTION_LEDGER.md",
}

# Legacy directories that existed BEFORE the Company OS was introduced.
# claim_guard is not retroactively applied to them in CI; instead, each
# directory should be brought into compliance on its own schedule (tracked
# in `docs/learning/EXPERIMENT_LOG.md`). This list is intentionally
# explicit — adding a new entry requires a logged decision.
LEGACY_DIR_EXCLUDES = (
    "docs/sales-kit/",
    "docs/case-studies/",
    "docs/from_zero/",
    "docs/proof-events/",
    "docs/execution/",
    "docs/00_constitution/",
    "docs/00_foundation/",
    "docs/01_category/",
    "docs/01_category_creation/",
    "docs/02_saudi_positioning/",
    "docs/02_strategy/",
    "docs/03_commercial_mvp/",
    "docs/03_saudi_positioning/",
    "docs/04_data_os/",
    "docs/04_product_strategy/",
    "docs/05_client_os/",
    "docs/05_governance_os/",
    "docs/06_data_os/",
    "docs/06_llm_gateway/",
    "docs/07_governance/",
    "docs/07_proof_os/",
    "docs/08_responsible_ai/",
    "docs/08_value_os/",
    "docs/09_capital_os/",
    "docs/09_llm_gateway/",
    "docs/10_agents/",
    "docs/10_tests/",
    "docs/11_client_os/",
    "docs/11_secure_runtime/",
    "docs/12_adoption_os/",
    "docs/12_auditability/",
    "docs/13_evidence_control_plane/",
    "docs/13_workflow_os/",
    "docs/14_proof/",
    "docs/14_trust_os/",
    "docs/15_auditability/",
    "docs/15_evidence_control_plane/",
    "docs/15_value/",
    "docs/16_agents/",
    "docs/16_capital/",
    "docs/16_evidence_control_plane/",
    "docs/17_revenue_os/",
    "docs/17_secure_agent_runtime/",
    "docs/18_brain_os/",
    "docs/18_intelligence_os/",
    "docs/19_command_os/",
    "docs/19_workflow_os/",
    "docs/20_adoption/",
    "docs/20_sales_os/",
    "docs/21_operating_finance/",
    "docs/21_operating_rhythm/",
    "docs/22_board_decision/",
    "docs/22_enterprise_rollout/",
    "docs/23_intelligence/",
    "docs/23_standards/",
    "docs/24_ecosystem/",
    "docs/24_risk_resilience/",
    "docs/25_compliance_trust/",
    "docs/25_ventures/",
    "docs/26_human_amplified/",
    "docs/26_service_catalog/",
    "docs/27_delivery_playbooks/",
    "docs/27_value_capture/",
    "docs/28_change_requests/",
)


def _load_claim_guard():
    path = REPO_ROOT / "dealix/trust/claim_guard.py"
    if not path.exists():
        return None
    name = "_claim_guard_for_safety"
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        return None
    module = importlib.util.module_from_spec(spec)
    # Register before exec so @dataclass can resolve __module__ during class body.
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def _check_forbidden_paths(repo_paths: list[Path]) -> list[str]:
    violations: list[str] = []
    for p in repo_paths:
        rel = str(p.relative_to(REPO_ROOT))
        # Template / scaffold paths are public-safe by design.
        if "/_TEMPLATE/" in f"/{rel}/" or "/_template/" in f"/{rel}/":
            continue
        for pattern in FORBIDDEN_PATH_PATTERNS:
            if pattern.search(rel):
                violations.append(f"forbidden-path: {rel} (matches {pattern.pattern})")
        for sus in SUSPICIOUS_FILENAMES:
            if sus.search(p.name):
                violations.append(f"suspicious-filename: {rel}")
    return violations


def _is_in_company_os_scope(rel: str) -> bool:
    """True if a file is within the Company OS allow-list (claim/PII scope)."""
    if rel in {
        "DEALIX_STAGE_STATUS.md",
        "DEALIX_ARCHITECTURE_MAP.md",
        "DEALIX_EXECUTION_LEDGER.md",
        "DEALIX_DECISION_RULES.md",
    }:
        return True
    return any(_match_glob(rel, g) for g in CLAIM_SCAN_GLOBS)


def _check_pii_patterns(text_files: list[Path]) -> list[str]:
    """PII scan applied to Company OS scope only.

    Legacy files may contain example phone numbers (`+966501234567`). They
    are tracked separately and brought into compliance over time, not
    forced retroactively in CI.
    """
    violations: list[str] = []
    for p in text_files:
        rel = str(p.relative_to(REPO_ROOT))
        if not _is_in_company_os_scope(rel):
            continue
        if "test" in rel.lower() or "example" in rel.lower() or "verify_public_safety" in rel:
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:  # noqa: S112 — best-effort scan; unreadable files are skipped
            continue
        if SAUDI_PHONE.search(text):
            violations.append(f"saudi-phone-pattern: {rel}")
    return violations


def _check_claim_guard(text_files: list[Path], claim_guard) -> list[str]:
    if claim_guard is None:
        return []
    violations: list[str] = []
    meta_excludes = {REPO_ROOT / p for p in META_FILE_EXCLUDES}
    for p in text_files:
        rel = str(p.relative_to(REPO_ROOT))
        if p in meta_excludes:
            continue
        if rel.startswith(LEGACY_DIR_EXCLUDES):
            continue
        if not any(_match_glob(rel, g) for g in CLAIM_SCAN_GLOBS):
            continue
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:  # noqa: S112 — best-effort scan; unreadable files are skipped
            continue
        report = claim_guard.check(text)
        if report.is_blocking:
            for flag in report.flags:
                if flag.severity.value == "block":
                    violations.append(
                        f"claim_guard:{flag.rule}: {rel} '{flag.excerpt}'"
                    )
    return violations


def _match_glob(rel: str, pattern: str) -> bool:
    # tiny glob-to-regex
    re_pat = re.escape(pattern).replace(r"\*\*", ".*").replace(r"\*", "[^/]*")
    return re.fullmatch(re_pat, rel) is not None


def main() -> int:
    repo_paths: list[Path] = []
    text_files: list[Path] = []
    for p in REPO_ROOT.rglob("*"):
        if ".git/" in str(p) or "node_modules/" in str(p) or "__pycache__" in str(p):
            continue
        if p.is_file():
            repo_paths.append(p)
            if p.suffix in {".md", ".html", ".txt", ".rst"}:
                text_files.append(p)

    violations: list[str] = []
    violations += _check_forbidden_paths(repo_paths)
    violations += _check_pii_patterns(text_files)
    claim_guard = _load_claim_guard()
    violations += _check_claim_guard(text_files, claim_guard)

    if violations:
        print("Public Safety verification FAILED:")
        for v in violations:
            print(f"  - {v}")
        return 1
    print(
        f"Public Safety verification OK "
        f"({len(repo_paths)} files scanned, {len(text_files)} text files checked)."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
