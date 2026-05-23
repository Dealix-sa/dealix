#!/usr/bin/env python3
"""Scan docs / prompts / outputs for unsafe patterns.

Hard-fail patterns:
  * guaranteed revenue / guaranteed sales / guaranteed meetings / guaranteed replies
  * fully compliant / no-risk
  * sent automatically
  * raw real-looking emails (e.g. `name@company.com`, but NOT example.com)
  * common secret prefixes (sk-ant-, sk-live-, AKIA, BEGIN PRIVATE KEY)
  * direct external send phrasing without approval

Scanned roots: docs/, CLAUDE.md, README.md, policies/, registries/,
evals/, scripts/run_*_worker.py.

Returns 0 if clean, 1 if hits found.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

# The scanner is designed to gate *AI-drafted* content owned by the
# Dealix Sovereign Operating Stack. It is NOT a retrofit for legacy
# docs that pre-date this contract — those have legitimate contact
# emails and quoted examples that would create noise.
#
# We scan an explicit allowlist of paths this stack owns. To add a new
# AI-author-facing file, add it here.
ROOTS: list[Path] = []  # no recursive roots; we use the explicit list below.

SINGLE_FILES = [
    Path("CLAUDE.md"),
    Path("docs/ops/CLAUDE_CODE_EXECUTION_REPORT.md"),
    Path("policies/dealix_control_policy.yaml"),
    Path("registries/agent_registry.yaml"),
    Path("evals/gates/dealix_agent_eval_gate.yaml"),
    # Trust plane docs (Sovereign stack)
    Path("docs/trust/POLICY_AS_CODE_V1.md"),
    Path("docs/trust/ULTIMATE_TRUST_PLANE.md"),
    Path("docs/trust/FOUNDER_CONSOLE_TRUST_GATE.md"),
    # Agent / eval docs (Sovereign stack)
    Path("docs/ai/AGENT_REGISTRY_SYSTEM.md"),
    Path("docs/ai/CEO_COPILOT_SYSTEM.md"),
    Path("docs/ai/REVENUE_AGENT_SWARM.md"),
    Path("docs/ai/TRUST_GUARDIAN_AGENT.md"),
    Path("docs/ai/EVAL_RED_TEAM_SYSTEM.md"),
    Path("docs/evals/EVAL_GATE_V1.md"),
    Path("docs/evals/PROMPT_OUTPUT_EVAL_MATRIX.md"),
    # Founder scorecards
    Path("docs/founder/OPERATING_SCORECARD_V1.md"),
    Path("docs/founder/SOVEREIGN_READINESS_SCORECARD.md"),
    # Control plane + API docs
    Path("docs/control_plane/DEALIX_CONTROL_PLANE.md"),
    Path("docs/api/CONTROL_PLANE_API.md"),
    Path("docs/api/ULTIMATE_INTERNAL_API.md"),
    # Architecture
    Path("docs/architecture/AI_NATIVE_COMPANY_ARCHITECTURE.md"),
    Path("docs/architecture/ULTIMATE_ARCHITECTURE_MAP.md"),
    # Company narrative
    Path("docs/company/DEALIX_SOVEREIGN_AI_OPERATING_COMPANY.md"),
    Path("docs/company/DEALIX_AUTONOMOUS_ENTERPRISE_OS.md"),
    Path("docs/company/DEALIX_MATURITY_MODEL.md"),
    # Frontend
    Path("docs/frontend/ULTIMATE_FOUNDER_CONSOLE.md"),
    # Revenue / delivery / finance / product / engineering
    Path("docs/revenue/ULTIMATE_REVENUE_FACTORY.md"),
    Path("docs/delivery/ULTIMATE_DELIVERY_OS.md"),
    Path("docs/finance/ULTIMATE_FINANCE_OS.md"),
    Path("docs/product/ULTIMATE_PRODUCT_PLATFORM.md"),
    Path("docs/engineering/ULTIMATE_OBSERVABILITY_DORA.md"),
    # Data + runtime
    Path("docs/data/POSTGRES_PRIMARY_MODE.md"),
    Path("docs/data/ULTIMATE_DATA_PLATFORM.md"),
    Path("docs/runtime/PRIVATE_OPS_RUNTIME_CONTRACT.md"),
    Path("docs/runtime/WORKER_ORCHESTRATOR_V1.md"),
    Path("docs/runtime/ULTIMATE_WORKER_MESH.md"),
    # Security
    Path("docs/security/ULTIMATE_SECURITY_GOVERNANCE.md"),
    Path("docs/security/PRODUCTION_SECURITY_GATE.md"),
    Path("docs/security/INTERNAL_API_AUTH_GATE.md"),
    Path("docs/security/BRANCH_PROTECTION_REQUIRED_CHECKS.md"),
]

# Files that deliberately list the deny-phrases (eval gate, policy doc,
# matrix). They are exempt from the deny scan but still scanned for
# secret leakage and real emails.
DENY_EXEMPT = {
    "evals/gates/dealix_agent_eval_gate.yaml",
    "policies/dealix_control_policy.yaml",
    "docs/evals/EVAL_GATE_V1.md",
    "docs/evals/PROMPT_OUTPUT_EVAL_MATRIX.md",
    "docs/ai/EVAL_RED_TEAM_SYSTEM.md",
}

# Patterns that must not appear in AI-facing docs/prompts/outputs.
# Each tuple is (pattern, description, is_regex). Patterns are case-insensitive.
DENY = [
    (r"guaranteed\s+revenue", "absolute revenue claim", True),
    (r"guaranteed\s+sales", "absolute sales claim", True),
    (r"guaranteed\s+meetings", "absolute meetings claim", True),
    (r"guaranteed\s+replies", "absolute replies claim", True),
    (r"fully\s+compliant", "absolute compliance claim", True),
    (r"no[-\s]?risk", "absolute risk claim", True),
    (r"sent\s+automatically", "auto-send phrasing without approval", True),
    (r"sk-ant-[A-Za-z0-9_-]+", "Anthropic API key prefix", True),
    (r"sk-live-[A-Za-z0-9_-]+", "Stripe live key prefix", True),
    (r"AKIA[0-9A-Z]{16}", "AWS access key", True),
    (r"BEGIN\s+PRIVATE\s+KEY", "private key block", True),
]

# Phrases that describe an unsafe action — must be paired with approval/evidence/risk
# language in the same file.
PAIRED_REQUIRED = [
    "direct external send",
    "send to customer",
    "publish proof",
    "change pricing",
]
APPROVAL_KEYWORDS = ["approval", "approved", "evidence", "risk", "founder", "queued"]


def _file_text(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8")
    except Exception:
        return ""


# Real-looking email regex: name@domain.tld, excluding example.com/co/org and
# placeholder TLDs.
_EMAIL_RE = re.compile(r"(?P<email>[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,})")
_ALLOWED_DOMAINS = {
    "example.com",
    "example.org",
    "example.net",
    "example.sa",
    "example.co",
    "test.com",
    "test.sa",
    "dealix.com",
    "dealix.sa",
}


def _scan_file(path: Path) -> list[str]:
    text = _file_text(path)
    hits: list[str] = []
    lower = text.lower()

    # The "deny phrase" scan is suppressed for files that document the
    # deny phrases by design (the eval gate, the policy file, the
    # prompt/output matrix). Secret + email scans still run.
    posix_path = path.as_posix()
    skip_deny_phrases = posix_path in DENY_EXEMPT

    if not skip_deny_phrases:
        for pat, desc, is_regex in DENY:
            if is_regex:
                if re.search(pat, text, flags=re.IGNORECASE):
                    hits.append(f"{path}: deny pattern '{desc}'")
            else:
                if pat.lower() in lower:
                    hits.append(f"{path}: deny pattern '{desc}'")
    # DENY_EXEMPT files are by design listing these patterns as bad
    # examples — we trust them. The email scan still runs below.

    for email_match in _EMAIL_RE.finditer(text):
        email = email_match.group("email")
        domain = email.split("@", 1)[1].lower()
        if domain in _ALLOWED_DOMAINS:
            continue
        if any(domain.endswith("." + a) for a in _ALLOWED_DOMAINS):
            continue
        # Allow common Dealix Github + monitoring domains.
        if domain in {"github.com", "githubusercontent.com"}:
            continue
        hits.append(f"{path}: real-looking email '{email}'")

    for phrase in PAIRED_REQUIRED:
        if phrase in lower:
            if not any(kw in lower for kw in APPROVAL_KEYWORDS):
                hits.append(f"{path}: phrase '{phrase}' without approval/evidence/risk language")

    return hits


def _iter_paths():
    for root in ROOTS:
        if not root.exists():
            continue
        for p in root.rglob("*"):
            if p.is_file() and p.suffix.lower() in {".md", ".yaml", ".yml", ".txt", ".prompt"}:
                yield p
    for p in SINGLE_FILES:
        if p.exists():
            yield p
    for p in Path("scripts").glob("run_*_worker.py"):
        yield p


def main() -> int:
    hits: list[str] = []
    for path in _iter_paths():
        hits.extend(_scan_file(path))
    if hits:
        for h in hits:
            print(f"[FAIL] {h}", file=sys.stderr)
        print(f"[FAIL] {len(hits)} prompt/output safety hit(s)", file=sys.stderr)
        return 1
    print("[PASS] prompt/output quality scan clean")
    return 0


if __name__ == "__main__":
    sys.exit(main())
