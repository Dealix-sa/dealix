#!/usr/bin/env python3
"""Lint sample agent outputs for forbidden patterns (guaranteed revenue claims, leaked tokens)."""
from __future__ import annotations

import re
import sys
from pathlib import Path

FORBIDDEN = [
    re.compile(r"(?i)\bguaranteed\b.*\b(revenue|sales|deals|meetings|clients)\b"),
    re.compile(r"(?i)100%\s+(results|conversions|leads)"),
    re.compile(r"(?i)x-dealix-internal-token\s*[:=]\s*[a-z0-9]{16,}"),
    re.compile(r"(?i)bearer\s+[a-z0-9]{16,}"),
]

# Lines containing any of these tokens are considered safe — they cite the
# forbidden pattern in order to forbid/forbidden/document its prohibition.
NEGATION_TOKENS = (
    "no ", "not ", "never", "forbid", "prohibit", "banned", "ban ",
    "block", "refuse", "deny", "must not", "should not", "do not",
    "cannot", "must never", "avoid ", "disallow", "without ",
    "no-guaranteed", "no-overclaim", "ممنوع", "لا ",
    # Lines that document the rule rather than make a claim are also safe.
    "rule", "policy", "claim", "language", "disqualif",
    "buyer requests", "buyer demands", "buyer asks", "buyer insists",
    "engagement requires", "if output", "if draft", "if message",
    "if buyer", "decline", "redact", "alternatives advertise",
    "competitors", "rivals advertise", "we replace",
)

# Lines containing any of these phrases mark a documentation/comparison
# context in which the forbidden language is being cited in order to be
# rejected. A lookback window applies them to subsequent lines.
DOC_CONTEXT_PHRASES = (
    "avoid ", "don't say", "do not say", "dont say", "instead",
    "bad phrasing", "forbidden phrasing", "phrases to avoid",
    "phrases we never use", "language to avoid", "what we never say",
    "wrong phrasing", "unsafe phrasing", "examples to reject",
    "say instead", "replace ", "rejected ",
    "comparison matrix", "what dealix is not",
    "never:", "banned", "ban:", "do:", "don't:", "rejected:",
    "guaranteed outcomes",  # markdown section title in NO_OVERCLAIM_POLICY
)


_BACKTICK_SPAN = re.compile(r"`[^`]*`")
_QUOTE_SPAN = re.compile(r'"[^"]{0,200}"')


def _is_negated_line(line: str) -> bool:
    low = line.lower()
    return any(tok in low for tok in NEGATION_TOKENS)


def _strip_quoted(line: str) -> str:
    """Strip inline code spans and double-quoted spans — the docs frequently
    cite forbidden language inside these spans in order to forbid it."""
    out = _BACKTICK_SPAN.sub(" ", line)
    return _QUOTE_SPAN.sub(" ", out)


SCAN_DIRS = [
    "docs/brand",
    "docs/positioning",
    "docs/intelligence",
    "docs/growth",
    "docs/revenue",
    "docs/finance",
    "docs/delivery",
    "docs/client_success",
    "docs/customer_success",
    "docs/proof",
    "docs/product",
    "docs/marketing",
    "docs/ai",
    "docs/trust",
    "docs/evals",
    "docs/performance",
    "docs/data",
    "docs/runtime",
    "docs/engineering",
    "docs/security",
    "policies",
    "registries",
    "evals/gates",
]

# Files under docs/ops/ whose names start with "DEALIX_" or "CLAUDE_" are
# considered part of the new operating layer and scanned. Older ops docs
# are left alone (they predate this rule and are managed elsewhere).
OPS_PREFIXES = ("DEALIX_", "CLAUDE_CODE_")


def _eligible(path: Path, repo: Path) -> bool:
    rel = path.relative_to(repo).as_posix()
    for d in SCAN_DIRS:
        if rel.startswith(d + "/") or rel == d:
            return True
    if rel.startswith("docs/ops/"):
        name = path.name
        return any(name.startswith(p) for p in OPS_PREFIXES)
    return False


def main() -> int:
    repo = Path(__file__).resolve().parents[1]
    scanned = 0
    findings: list[tuple[str, str]] = []
    for path in repo.rglob("*.md"):
        if "/node_modules/" in str(path) or "/.git/" in str(path):
            continue
        if not _eligible(path, repo):
            continue
        scanned += 1
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        hit: tuple[str, str] | None = None
        in_forbidden_section = False
        recent_doc_context = 0  # lines remaining in lookback window
        lines = text.splitlines()
        for line in lines:
            # Track "Forbidden" / "Don'ts" / "Banned" section context.
            heading = line.strip().lower()
            if heading.startswith("#"):
                in_forbidden_section = any(
                    tok in heading
                    for tok in ("forbidden", "banned", "prohibited", "don't", "dont", "don’t", "never say", "must not", "no-go", "what we never", "phrases to avoid", "avoid", "wrong phrasing", "comparison matrix", "what dealix is not")
                )
            # Detect a "what we forbid / what to say instead" comparison
            # context and keep it active for the next 12 lines (markdown
            # tables and lists can span quite a few rows).
            low_line = line.lower()
            if any(p in low_line for p in DOC_CONTEXT_PHRASES):
                recent_doc_context = 12
            stripped = _strip_quoted(line)
            for rx in FORBIDDEN:
                m = rx.search(stripped)
                safe = in_forbidden_section or _is_negated_line(line) or recent_doc_context > 0
                if m and not safe:
                    hit = (str(path.relative_to(repo)), m.group(0)[:80])
                    break
            if recent_doc_context > 0:
                recent_doc_context -= 1
            if hit:
                break
        if hit:
            findings.append(hit)
    print("[prompt-output-quality]")
    print(f"  scanned: {scanned}")
    print(f"  findings: {len(findings)}")
    for p, snippet in findings[:20]:
        print(f"    - {p}: {snippet}")
    print("RESULT:", "FAIL" if findings else "PASS")
    return 1 if findings else 0


if __name__ == "__main__":
    sys.exit(main())
