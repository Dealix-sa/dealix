"""v7 Phase 8 hardening — no real secret may leak into the repo.

Three perimeter assertions:

  1. ``redact_log_entry`` (security_privacy.log_redaction) replaces a
     Stripe-shaped key built via concatenation with the redaction
     marker. Construct test secrets via concatenation so gitleaks
     never sees a literal ``sk_live_*`` substring in this source.
  2. ``redact_log_entry`` redacts an Anthropic-shaped key
     (``"sk-ant-" + ...``).
  3. A repo-wide grep for the literal prefixes (Stripe, GitHub PAT,
     Google API key) returns ZERO matches outside the explicit
     allowlist below. Each allowlist entry has a comment explaining
     why the prefix legitimately appears in that file.
"""
from __future__ import annotations

import re
from pathlib import Path

from auto_client_acquisition.security_privacy.log_redaction import (
    redact_log_entry,
)


REPO_ROOT = Path(__file__).resolve().parents[1]


def test_redact_log_entry_redacts_stripe_shaped_key():
    """Stripe live-secret-key shape — built via concatenation so gitleaks
    cannot flag this test source as containing the literal prefix."""
    # Build the test value by concatenation so the literal prefix
    # never appears as a contiguous substring in this source file.
    fake_secret = "sk_" + "live" + "_" + "abcdefghijklmnopqrstuvwxyz12345"
    log_line = f"event=invoice_charge attempt key={fake_secret} status=blocked"
    redacted = redact_log_entry(log_line)
    assert isinstance(redacted, str)
    assert fake_secret not in redacted, (
        f"Stripe-shaped key leaked through redaction: {redacted!r}"
    )
    assert "[REDACTED_SECRET]" in redacted


def test_redact_log_entry_redacts_anthropic_shaped_key():
    """Anthropic API key shape — also built via concatenation."""
    fake_anthropic = "sk-" + "ant-" + ("a" * 35)
    log_line = f"event=llm_call provider=anthropic key={fake_anthropic}"
    redacted = redact_log_entry(log_line)
    assert isinstance(redacted, str)
    assert fake_anthropic not in redacted
    assert "[REDACTED_SECRET]" in redacted


def test_redact_log_entry_redacts_inside_dict_log_entry():
    """Dict-shaped log entries (structlog) must also redact."""
    fake_secret = "sk_" + "live" + "_" + "ZYXWVUTSRQPONMLK987654321"
    entry = {
        "event": "moyasar_attempt",
        "metadata": {"key": fake_secret, "status": "rejected"},
    }
    out = redact_log_entry(entry)
    assert isinstance(out, dict)
    flat = repr(out)
    assert fake_secret not in flat, f"secret leaked into dict redaction: {flat}"


# ─────────────────────────────────────────────────────────────────────────
# Repo-wide allowlist for legitimate prefix references.
# ─────────────────────────────────────────────────────────────────────────
# Each entry is a path (relative to REPO_ROOT) where the literal token
# ``sk_live_`` / ``ghp_`` / ``AIza`` legitimately appears in:
#   - rejection logic ("if key.startswith('sk_live_'): refuse")
#   - regex patterns themselves (the secret scanner's source of truth)
#   - placeholder examples in deployment docs
#   - role-brief / runbook copy that names the prefix to ban it
#   - test fixtures that intentionally feed the scanner a fake match
#   - launch-verify shell scripts that grep for these patterns
# Reading the file should make the rationale obvious. New entries
# require a one-line comment.
_PREFIX_ALLOWLIST: dict[str, str] = {
    # ── repo-level config files that name the prefix to ban it ──
    ".gitleaks.toml":
        "gitleaks regex rules — the patterns are the secret-scan policy",
    # ── core safety code (the prefix is the policy) ──
    "auto_client_acquisition/finance_os/guardrails.py":
        "live-charge guardrail uses startswith('sk_live_') to refuse",
    "auto_client_acquisition/security_privacy/secret_scan_policy.py":
        "regex patterns themselves — the secret scanner's source of truth",
    "auto_client_acquisition/security_privacy/__init__.py":
        "module docstring names the prefixes the scanner looks for",
    "auto_client_acquisition/role_command_os/role_briefs.py":
        "founder/sales role briefs reference the prefix in policy copy",
    "auto_client_acquisition/personal_operator/memory.py":
        "memory layer regex used to scrub Google API key prefix",
    "auto_client_acquisition/reliability_os/health_matrix.py":
        "health-matrix names sk_live_ in its 'no live charge' assertion",
    # ── scripts ──
    "scripts/dealix_invoice.py":
        "invoice CLI rejects sk_live_* unless --allow-live is set",
    "scripts/github_setup.sh":
        "setup script grep pattern for accidental token paste",
    "scripts/ops/deploy_bundle_v2.sh":
        "deploy bundle env-template comments name the placeholder prefix",
    "scripts/v7_launch_verify.sh":
        "launch verify shell script greps repo for these prefixes",
    "scripts/v10_master_verify.sh":
        "v10 master verifier shell script greps repo for these prefixes",
    "scripts/v11_customer_closure_verify.sh":
        "v11 master verifier shell script greps repo for these prefixes",
    "scripts/v12_full_ops_verify.sh":
        "v12 master verifier shell script greps repo for these prefixes",
    "scripts/beast_level_verify.sh":
        "v12.5 beast master verifier shell script greps repo for these prefixes",
    # ── deployment / placeholder docs ──
    "docs/contributing/DEPLOYMENT.md":
        "deployment doc placeholder values use the prefix names",
    "docs/operations/DEALIX_COMPANY_OPERATIONAL_STATE.md":
        "operational-state doc references the prefix in policy copy",
    # ── docs/* (operational + sales-kit + master-evidence narratives) ──
    "docs/MASTER_CLOSURE_EVIDENCE_TABLE.md":
        "evidence table cell names the prefix as a forbidden token",
    "docs/MOYASAR_E2E_GUIDE.md":
        "Moyasar e2e guide describes test vs live key prefix difference",
    "docs/SAMI_ACTION_ITEMS.md":
        "founder action item names the prefix in policy copy",
    "docs/SECURITY_INCIDENT_PAT_EXPOSURE.md":
        "incident report names the prefix as part of the IOC list",
    "docs/PR125_FINAL_STABILIZATION_REPORT.md":
        "stabilization report cites the prefix in evidence narrative",
    "docs/POST_MERGE_VERIFICATION.md":
        "merge verification checklist names the prefix",
    "docs/FIRST_3_DIAGNOSTIC_SCRIPT.md":
        "diagnostic script doc names the prefix in placeholder text",
    "docs/V5_FOUNDER_RUNBOOK.md":
        "founder runbook names the prefix in policy/safety copy",
    "docs/V5_MASTER_EVIDENCE_TABLE.md":
        "v5 master evidence table names the forbidden prefix",
    "docs/V5_OS_SCOPE.md":
        "v5 OS scope doc names the prefix in policy copy",
    "docs/V5_PHASE_E_CHECKLIST.md":
        "v5 phase E checklist names the prefix in test rows",
    "docs/phase-e/06_MANUAL_PAYMENT_FALLBACK.md":
        "v11 phase E payment fallback doc names sk_live_ in policy copy",
    "docs/knowledge-base/payment_policy_ar_en.md":
        "v12 KB payment policy doc names sk_live_ in policy copy",
    "docs/14_DAY_FIRST_REVENUE_PLAYBOOK.md":
        "RX founder playbook references sk_live_ rejection rule in policy copy",
    "docs/BEAST_LEVEL_ARCHITECTURE.md":
        "v12.5 beast architecture references sk_live_ in policy copy",
    "docs/V5_RELEASE_NOTES.md":
        "v5 release notes name the prefix in safety summary",
    "docs/V5_SYSTEM_OVERVIEW.md":
        "v5 system overview names the prefix in policy diagram",
    "docs/V6_MASTER_EVIDENCE_TABLE.md":
        "v6 master evidence table names the prefix in evidence cells",
    "docs/V6_OBSERVABILITY_AND_INCIDENT_RUNBOOK.md":
        "observability runbook references prefix for incident IOC",
    "docs/V6_OPERATING_REALITY_REPORT.md":
        "v6 reality report cites the prefix in posture narrative",
    "docs/launch/DEALIX_LAUNCH_NOW_BUNDLE.md":
        "launch bundle copy names the prefix in env-var template",
    "docs/ops/COMPANY_CONTROL_CENTER.md":
        "ops control center checklist names the prefix",
    "docs/ops/FIRST_REVENUE_ATTEMPT.md":
        "first-revenue attempt SOP references the prefix",
    "docs/ops/MANUAL_PAYMENT_SOP.md":
        "manual payment SOP names the prefix in policy copy",
    "docs/ops/TODAY.md":
        "daily TODO names the prefix in checklist text",
    "docs/ops/daily_scorecard.md":
        "daily scorecard names the prefix in safety row",
    "docs/ops/moyasar_live_test.sh":
        "Moyasar test shell script names the prefix in placeholder env",
    "docs/sales-kit/dealix_1_riyal_test.sh":
        "sales-kit 1-riyal test shell script names the prefix in env",
    # ── core safety / observability code (regex patterns = the policy) ──
    "api/routers/founder_launch_status.py":
        "launch-status reporter detects Moyasar mode via startswith('sk_live_')",
    "auto_client_acquisition/agent_observability/redaction.py":
        "log-redaction regex patterns for sk_live_/ghp_/AIza secret shapes",
    "auto_client_acquisition/observability_adapters/redaction.py":
        "observability adapter redaction regex names the secret prefixes",
    # ── scripts: secret scanners + env generators + verifiers ──
    "scripts/apply_founder_closure_env.py":
        "env-apply guard regex rejects 'sk_live_CHANGE' placeholder tokens",
    "scripts/dealix_integration_plan_quality_check.py":
        "integration quality check regex matches live API key shape",
    "scripts/dealix_master_full_execution_verify.sh":
        "master verifier shell script greps repo for these prefixes",
    "scripts/first_setup.sh":
        "first-setup script names the prefix in env-template guidance",
    "scripts/generate_production_env.sh":
        "prod env generator writes 'sk_live_xxxxx' placeholder template",
    "scripts/integration_upgrade_verify.sh":
        "integration upgrade verifier greps repo for these prefixes",
    "scripts/moyasar_live_cutover.py":
        "live cutover CLI prompts/validates the sk_live_ key prefix",
    "scripts/preflight_check.py":
        "preflight check names sk_live_ in env-template placeholder text",
    "scripts/reconcile_moyasar.py":
        "reconcile CLI docstring names the sk_live_ key env placeholder",
    "scripts/security_smoke.py":
        "security smoke test regex matches sk_live_/ghp_ secret shapes",
    "scripts/ultimate_upgrade_verify.sh":
        "ultimate upgrade verifier greps repo for these prefixes",
    "scripts/validate_railway_generated_env.py":
        "env validator regex rejects 'sk_live_CHANGE' placeholder tokens",
    "scripts/verify_founder_operating_system.py":
        "verifier uses 'sk_live_REAL' as a fixture to assert rejection",
    "scripts/verify_moyasar_e2e.py":
        "moyasar e2e verifier names sk_test_*/sk_live_* in its check label",
    "scripts/wave6_revenue_activation_verify.sh":
        "wave6 verifier shell script greps repo for these prefixes",
    "scripts/wave7_5_service_truth_verify.sh":
        "wave7.5 verifier shell script greps repo for these prefixes",
    "scripts/wave8_customer_data_boundary_check.sh":
        "wave8 boundary checker greps repo for these prefixes",
    "scripts/wave8_customer_ready_verify.sh":
        "wave8 customer-ready verifier greps repo for these prefixes",
    "scripts/wave11_first3_paid_pilots_verify.sh":
        "wave11 verifier shell script greps repo for these prefixes",
    "scripts/wave12_saudi_revenue_command_center_verify.sh":
        "wave12 verifier shell script greps repo for these prefixes",
    # ── deployment / env-template / policy docs ──
    "docs/LLM_PROVIDERS_SETUP.md":
        "LLM providers setup doc names AIza/sk-ant key prefixes in env table",
    "docs/MOYASAR_LIVE_CUTOVER.md":
        "live cutover doc names sk_live_ in the key-swap procedure",
    "docs/RAILWAY_DEPLOY_CHECKLIST.md":
        "deploy checklist names sk_live_ in the production env step",
    "docs/WAVE11_FIRST3_PAID_PILOTS_EVIDENCE_TABLE.md":
        "evidence table cell names the prefix as a forbidden token",
    "docs/infra/CONFIGURATION_DRIFT_POLICY_AR.md":
        "Arabic config-drift policy names the prefix in env-contract copy",
    "docs/integrations/PAYMENT_MOYASAR_LIVE.md":
        "Moyasar live payment integration doc names sk_live_ in policy copy",
    "docs/ops/ENVIRONMENT_CONTRACT.md":
        "environment contract doc names sk_live_ in the env-var table",
    "docs/ops/GO_LIVE_CHECKLIST_AR.md":
        "Arabic go-live checklist names sk_live_ in the production step",
    "docs/ops/GO_LIVE_INDEX.md":
        "go-live index references sk_live_ in the cutover checklist",
    "docs/ops/MOYASAR_KYC_CHECKLIST.md":
        "Moyasar KYC checklist names sk_live_ in the key-issuance step",
    "docs/ops/PRODUCTION_ENV_TEMPLATE.md":
        "production env template names sk_live_ placeholder for MOYASAR key",
    "docs/ops/RAILWAY_COMMERCIAL_SOFT_LAUNCH_AR.md":
        "Arabic soft-launch runbook names sk_live_ in env-cutover copy",
    "docs/sales-kit/CUSTOMER_1_GO_LIVE_RUNBOOK.md":
        "customer-1 go-live runbook names sk_live_ in the env-config step",
    # ── security policy / key-rotation docs ──
    "docs/security/KEY_ROTATION.md":
        "key-rotation policy names sk_live_ in the rotation matrix table",
    "docs/security/SECRETS_HANDLING_POLICY.md":
        "secrets-handling policy names the prefixes as protected tokens",
    "docs/security/TOOL_USE_SECURITY_POLICY.md":
        "tool-use security policy names the secret prefixes in scan copy",
    "docs/security/UNTRUSTED_INPUT_POLICY.md":
        "untrusted-input policy names the secret prefixes in redaction copy",
    # ── trivy / container scanner config ──
    ".trivyignore.yaml":
        "trivy ignore file explicitly notes sk_live_xxxxx as placeholder token (not a real secret)",
    # ── CI / docs referencing the quarantine entry ──
    "docs/CI_QUARANTINE.md":
        "CI quarantine doc quotes the sk_live_/ghp_/AIza prefix in the quarantine reason text",
    # ── secret scanner scripts (patterns are the policy) ──
    "scripts/check_no_secrets.py":
        "secret-scan script defines AIza/sk_live_ regex patterns as the detection policy",
    "scripts/ops/security_smoke_ci.py":
        "CI security smoke test defines sk_live_/ghp_ regex patterns to detect real secrets",
    "scripts/verify_secret_patterns.py":
        "secret-pattern verifier defines sk_live_/ghp_/AIza regex patterns as detection policy",
    "scripts/dealix_startup_release_gate.py":
        "startup release gate checks Moyasar key startswith('sk_live_') to detect live keys — policy guard, not a real secret",
}


# Filename patterns we ignore entirely:
#   - any file with ``test_`` in its name (test fixtures may construct
#     fake-shaped values via concatenation; gitleaks won't flag them
#     because we always concatenate)
#   - non-source artifacts (caches, htmlcov, etc.)
_SKIP_PARTS = {".git", ".claude", "node_modules", "__pycache__", "htmlcov", ".pytest_cache", ".venv", "venv"}


def _should_skip_file(rel_path: Path) -> bool:
    parts = set(rel_path.parts)
    if parts & _SKIP_PARTS:
        return True
    name = rel_path.name
    # Tests are exempt — they construct via concatenation.
    if name.startswith("test_") or name == "conftest.py":
        return True
    return False


def test_no_secret_prefix_outside_allowlist():
    """Repo-wide grep for the three forbidden literal prefixes.

    Each match outside the allowlist is a regression — either a real
    secret slipped in, or a new file legitimately needs to reference
    the prefix and should be added to ``_PREFIX_ALLOWLIST`` with a
    reason comment.
    """
    pattern = re.compile(r"sk_live_|ghp_|AIza")

    extensions = {".py", ".md", ".sh", ".env", ".ini", ".toml", ".yaml", ".yml"}
    violations: list[str] = []

    for path in REPO_ROOT.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix not in extensions:
            continue
        rel = path.relative_to(REPO_ROOT)
        if _should_skip_file(rel):
            continue
        if str(rel) in _PREFIX_ALLOWLIST:
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if pattern.search(text):
            violations.append(str(rel))

    assert not violations, (
        "Forbidden secret prefix found outside allowlist. Either:\n"
        "  - a real secret leaked (rotate it + remove from history), OR\n"
        "  - a new file legitimately references the prefix in policy/"
        "regex/runbook copy — add it to _PREFIX_ALLOWLIST with a "
        "one-line reason.\n"
        "Files:\n" + "\n".join(sorted(violations))
    )


def test_prefix_allowlist_entries_actually_exist():
    """Catch stale allowlist entries — if a file no longer contains
    the prefix, drop it from the allowlist to keep the perimeter tight."""
    pattern = re.compile(r"sk_live_|ghp_|AIza")
    stale: list[str] = []
    for rel_path in _PREFIX_ALLOWLIST:
        path = REPO_ROOT / rel_path
        if not path.exists():
            stale.append(f"{rel_path}: file no longer present")
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except (OSError, UnicodeDecodeError):
            continue
        if not pattern.search(text):
            stale.append(f"{rel_path}: prefix no longer in file")
    assert not stale, (
        "Stale entries in _PREFIX_ALLOWLIST — remove them:\n"
        + "\n".join(stale)
    )
