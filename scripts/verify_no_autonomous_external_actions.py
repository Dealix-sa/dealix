"""Verify Revenue Sprint Kit content makes no autonomous-action claims.

Step 17 of the Revenue Sprint Kit specification: before any DM, proposal,
or report is used externally, its text is checked against a small list
of forbidden claims that would either overstate what Dealix delivers or
imply unsupervised external action.

This script scans the public kit content (and the local copies of the
private kit templates, when present) for those forbidden claim phrases.
The `NO_OVERCLAIM_POLICY.md` file is allowed to list the phrases — it
is the policy document that defines them.

Run locally via `make kit` and in CI via the Revenue Sprint Kit workflow.
"""

from __future__ import annotations

import re
from pathlib import Path


SCAN_PATHS = [
    "docs/offers/revenue_sprint",
    "docs/delivery/revenue_sprint",
    "docs/trust/NO_OVERCLAIM_POLICY.md",
]

# The policy doc defines the forbidden claim list, so it is exempt.
POLICY_DOC = "docs/trust/NO_OVERCLAIM_POLICY.md"

FORBIDDEN_CLAIMS = [
    re.compile(r"\bguaranteed\s+revenue\b", re.IGNORECASE),
    re.compile(r"\bguaranteed\s+sales\b", re.IGNORECASE),
    re.compile(r"\bguaranteed\s+meetings\b", re.IGNORECASE),
    re.compile(r"\bguaranteed\s+replies\b", re.IGNORECASE),
    re.compile(r"\bfully\s+compliant\b", re.IGNORECASE),
    re.compile(r"\b100\s*%\s*automated\s+sales\b", re.IGNORECASE),
    re.compile(r"\bno[-\s]?risk\b", re.IGNORECASE),
    re.compile(r"\brisk[-\s]?free\b", re.IGNORECASE),
    re.compile(r"\bwill\s+close\s+(?:your\s+)?deals\b", re.IGNORECASE),
    re.compile(r"\breplace\s+your\s+sales\s+team\b", re.IGNORECASE),
]

# A line that *negates* a forbidden claim ("not guaranteed sales",
# "no guaranteed meetings", "Out of Scope: Guaranteed revenue", "does
# not guarantee", "without guaranteed") is fine — it is reinforcing
# the trust boundary, not promising the claim.
NEGATION_CONTEXTS = [
    re.compile(r"\bnot\b", re.IGNORECASE),
    re.compile(r"\bno\b", re.IGNORECASE),
    re.compile(r"\bnever\b", re.IGNORECASE),
    re.compile(r"\bwithout\b", re.IGNORECASE),
    re.compile(r"\bdoes\s+not\b", re.IGNORECASE),
    re.compile(r"\bcannot\b", re.IGNORECASE),
    re.compile(r"\bout\s+of\s+scope\b", re.IGNORECASE),
    re.compile(r"\bforbidden\b", re.IGNORECASE),
]


def line_is_negated(line: str) -> bool:
    for pattern in NEGATION_CONTEXTS:
        if pattern.search(line):
            return True
    return False


def iter_files() -> list[Path]:
    files: list[Path] = []
    for entry in SCAN_PATHS:
        path = Path(entry)
        if not path.exists():
            continue
        if path.is_file():
            files.append(path)
            continue
        for child in path.rglob("*.md"):
            if child.is_file():
                files.append(child)
    return files


def scan_file(path: Path) -> list[str]:
    findings: list[str] = []
    if str(path) == POLICY_DOC:
        return findings
    try:
        text = path.read_text(encoding="utf-8", errors="ignore")
    except OSError:
        return findings
    lines = text.splitlines()
    for lineno, line in enumerate(lines, start=1):
        for pattern in FORBIDDEN_CLAIMS:
            if not pattern.search(line):
                continue
            if line_is_negated(line):
                continue
            # Look back up to 6 lines for a negating section heading or
            # introductory sentence ("Out Of Scope", "What It Is Not",
            # "Forbidden Claims", "Dealix does not …"). This keeps
            # policy and scope sections from being flagged while still
            # catching unintended positive claims.
            window_start = max(0, lineno - 1 - 6)
            window = lines[window_start : lineno - 1]
            if any(line_is_negated(prev) for prev in window):
                continue
            findings.append(f"{path}:{lineno}: {line.strip()}")
            break
    return findings


def main() -> int:
    all_findings: list[str] = []
    for path in iter_files():
        all_findings.extend(scan_file(path))

    if all_findings:
        print("Revenue Sprint Kit content guard FAILED:")
        for finding in all_findings:
            print("-", finding)
        print(
            "\nForbidden claims (see docs/trust/NO_OVERCLAIM_POLICY.md):\n"
            "- guaranteed revenue / sales / meetings / replies\n"
            "- fully compliant\n"
            "- 100% automated sales\n"
            "- no-risk / risk-free\n"
            "- will close your deals / replace your sales team\n"
            "Rephrase using the allowed framing in NO_OVERCLAIM_POLICY.md."
        )
        return 1

    print("PASS: no forbidden claims in Revenue Sprint Kit content.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
