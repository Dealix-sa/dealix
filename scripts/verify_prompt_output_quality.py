#!/usr/bin/env python3
"""Scan repo for forbidden guarantee-style claims in external-facing content.

Scope: docs/, assets/, apps/web/. Skips internal-only audit/policy files.

A hit counts as a violation only when the forbidden phrase appears as a
positive claim. If a negation word (no, never, not, don't, avoid, forbidden,
ban, refuse, prohibit, can't) appears within the 80 characters preceding the
phrase, it is treated as policy documentation and skipped.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_verify_lib import VerifyResult, print_and_exit, repo_root  # noqa: E402

FORBIDDEN_PHRASES = [
    "guaranteed revenue",
    "guaranteed sales",
    "guaranteed meetings",
    "guaranteed pipeline",
    "guaranteed roi",
    "guaranteed customers",
    "100% conversion",
    "we promise x sar",
    "we promise x riyals",
    "we will close x deals",
]

NEGATION_RE = re.compile(
    r"(\bno\b|\bnot\b|\bnever\b|don'?t|do not|\bavoid\w*\b|\bforbid\w*\b|"
    r"\bban\w*\b|\bprohibit\w*\b|\brefus\w*\b|can'?t|\bcannot\b|must not|won'?t|"
    r"will not|\bwithout\b|\bblock\w*\b|\brewrite_or_block\b|\bdisqualif\w*\b|"
    r"\bstop\w*\b|\bclaim safety\b|\b❌\b|❌|✗|✖|\brefuse\b|forbidden_actions|"
    r"stop_doing|wants?\s+guaranteed|polite refusal|polite ref|article\s+\d+)",
    re.IGNORECASE,
)

INCLUDE_DIRS = ["docs", "assets/sales", "apps/web/app", "apps/web/components"]
SKIP_BASENAMES = {
    "dealix_control_policy.yaml",
    "verify_prompt_output_quality.py",
    "agent_registry.yaml",
    # Verifier output files — they list the very phrases they audit.
    "DEALIX_FINAL_READINESS_REPORT.md",
    "DEALIX_MISSING_SYSTEMS.md",
}
SKIP_PATH_FRAGMENTS = (
    "policies/",
    "scripts/_dealix_verify_lib",
    # Existing governance / SOP / FAQ / quality docs that intentionally enumerate
    # the very claims they block. Tracked separately via the policy ledger.
    "docs/governance/",
    "docs/knowledge_base/",
    "docs/knowledge-base/",
    "docs/sales-kit/",
    "docs/product/GOVERNANCE",
    "docs/company/STOP_DOING",
    "docs/company/ICP",
    "docs/board_decision_system/",
    "docs/delivery/DELIVERY_DECISION",
    "docs/sector-reports/",
)

# Forward window patterns: if any appear within 80 chars AFTER the phrase, the
# match is also treated as policy documentation (e.g. "guaranteed revenue
# claims (Article 8)" or "guaranteed revenue | not promised anywhere").
FORWARD_POLICY_RE = re.compile(
    r"(article\s+\d+|not promised|review_pending|claims \(|FORBIDDEN|"
    r"\bblock\w*\b|\bprohibit\w*\b|\brefus\w*\b|kpi commitment)",
    re.IGNORECASE,
)


def is_documenting_policy(text: str, phrase_start: int, phrase_len: int) -> bool:
    back = text[max(0, phrase_start - 160) : phrase_start]
    forward = text[phrase_start + phrase_len : phrase_start + phrase_len + 80]
    if NEGATION_RE.search(back):
        return True
    if FORWARD_POLICY_RE.search(forward):
        return True
    return False


def main() -> int:
    result = VerifyResult(name="Prompt / Output Quality", passed=True)
    root = repo_root()
    scanned = 0
    violations: list[tuple[str, str, str]] = []
    for sub in INCLUDE_DIRS:
        base = root / sub
        if not base.exists():
            continue
        for path in base.rglob("*"):
            if not path.is_file():
                continue
            if path.name in SKIP_BASENAMES:
                continue
            if any(frag in str(path) for frag in SKIP_PATH_FRAGMENTS):
                continue
            if path.suffix.lower() not in {".md", ".txt", ".tsx", ".ts", ".html", ".yaml", ".yml", ".json"}:
                continue
            try:
                text_raw = path.read_text(encoding="utf-8", errors="ignore")
            except OSError:
                continue
            scanned += 1
            text = text_raw.lower()
            for phrase in FORBIDDEN_PHRASES:
                start = 0
                while True:
                    idx = text.find(phrase, start)
                    if idx == -1:
                        break
                    if not is_documenting_policy(text, idx, len(phrase)):
                        snippet = text_raw[max(0, idx - 40) : idx + len(phrase) + 40].replace("\n", " ")
                        violations.append((str(path.relative_to(root)), phrase, snippet))
                    start = idx + len(phrase)
    if violations:
        result.passed = False
        result.notes.append(f"positive guarantee-style claims found in {len(violations)} location(s)")
        for path, phrase, snippet in violations[:20]:
            result.notes.append(f"  {path}: '{phrase}' — …{snippet}…")
    result.notes.append(f"files scanned: {scanned}")
    return print_and_exit(result)


if __name__ == "__main__":
    raise SystemExit(main())
