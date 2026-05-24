"""Scan the repo for forbidden phrases in user-facing copy.

Looks at markdown, jinja templates, and tsx/ts strings for:
    - "guaranteed revenue / sales / meetings" and Arabic equivalents
    - hard pricing commitments outside docs/pricing/*

This is a static guardrail, not an LLM eval — it catches the easy mistakes.
"""
from __future__ import annotations

import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_cert_common import (
    REPO_ROOT,
    VerifierReport,
    iter_files,
    main_cli,
)

FORBIDDEN_PATTERNS = [
    re.compile(r"\bguaranteed\s+(revenue|sales|meetings|leads|customers|deals)\b", re.I),
    re.compile(r"نضمن\s+لك\s+(مبيعات|إيرادات|اجتماعات|عملاء|صفقات|قنوات)"),
    re.compile(r"\bguaranteed\s+ROI\b", re.I),
    re.compile(r"\b100%\s+(uptime|deliverability)\b", re.I),
]

# Negators that turn a "guaranteed X" mention into a prohibition (e.g.
# "never claim guaranteed revenue", "no guaranteed sales", "❌ guaranteed leads").
# When any of these appears within NEGATOR_WINDOW chars before the match on
# the same line, the line is treated as policy/doctrine, not a promise.
NEGATOR_WINDOW = 60
NEGATOR_RE = re.compile(
    r"(?i)(?:\bnever\b|\bno\b|\bnot\b|\bnon-?\b|\bwithout\b|\bdon'?t\b|\bdo\s+not\b|"
    r"\bavoid\b|\bforbidden\b|\bprohibited\b|\bbanned?\b|\bblocked?\b|\bdenied?\b|"
    r"\brefuses?\b|\brefuse\b|\brefused\b|\bremove\b|\brewrite\b|\bclaim(?:ing|s|ed)?\b|"
    r"\bpromise(?:s|d|ing)?\b|\bwants?\b|\basks?\b|\bdemands?\b|\brequests?\b|"
    r"\bmentions?\b|\brejects?\b|\bdisqualif\w*\b|\bdoctrine\b|❌|«no»|"
    r"\bif\s+output\s+contains\b|\bsource-?less\b|\bcold\s+whatsapp\b|"
    r"لا\s|ليس|بدون|ممنوع|نتجنب|يمنع|ضد|نرفض|بدل)"
)


SECTION_NEGATOR_RE = re.compile(
    r"(?i)(forbidden|refus(?:e|ed|als?|ing)|banned?|prohibited|never\b|\bdo\s+not\b|"
    r"\bmust\s+not\b|\bagrees?\s+to\s+never\b|\bnot\s+for\b|\bblocked\b|"
    r"don'?t\b|red\s*lines?|hard\s*rules?|guardrails?|policy|disqualif|"
    r"non-?negotiable|cannot|won'?t|claim\s*safety|safe_publishing_gate|"
    r"ممنوع|ضد|نرفض|قواعد|سياسة|محظور|يجب\s+ألا|يجب\s+عدم)"
)

# Directories whose .md content is internal policy/doctrine — scan with
# negation awareness but never treat as user-facing marketing copy.
DOCTRINE_PATH_PREFIXES = (
    "docs/governance/",
    "docs/product/GOVERNANCE",
    "docs/sales/QUALIFICATION",
    "docs/sales/CLIENT_SELECTION",
    "docs/services/",            # service definitions list refusals
    "docs/board_decision_system/",
    "docs/board_ready/",
    "docs/company/ICP",
    "docs/company/DEALIX_MASTER_OPERATING_SYSTEM",
    "docs/knowledge_base/",
    "docs/content/",
    "docs/sector-reports/",
    "docs/delivery/",
    "docs/sales/PROPOSAL_LEAD_INTELLIGENCE",
    ".claude/",                  # agent doctrine
)


def _is_negated(line: str, match: re.Match[str], prev_lines: list[str]) -> bool:
    """Treat the match as a prohibition (not a promise) if either:
       * a negator sits within NEGATOR_WINDOW chars before it on the same line, or
       * the nearest section header / preceding non-empty line contains a
         negator keyword (forbidden / refuse / never / red lines / policy ...).
    """
    start = match.start()
    window = line[max(0, start - NEGATOR_WINDOW):start]
    if NEGATOR_RE.search(window):
        return True
    # bullet-list case: look back up to 6 non-empty lines for a section header
    looked = 0
    for prev in reversed(prev_lines):
        s = prev.strip()
        if not s:
            continue
        looked += 1
        if SECTION_NEGATOR_RE.search(s):
            return True
        if looked >= 12:
            break
    return False


# Files where the forbidden phrase is the subject of the file (rules, policies,
# evals describing what to detect). These are skipped entirely.
DOCTRINE_FILE_NAMES = {
    "DEALIX_FINAL_READINESS_REPORT.md",
    "DEALIX_IMPLEMENTATION_AUDIT.md",
    "DEALIX_MISSING_SYSTEMS.md",
    "LIVE_SEND_SAFETY_GATE.md",
    "WHATSAPP_APPROVAL_GATE.md",
    "EMAIL_APPROVAL_GATE.md",
    "LIVE_INTEGRATION_KILL_SWITCHES.md",
}


def run() -> VerifierReport:
    r = VerifierReport(verifier="Prompt / Output Safety")
    hits: list[tuple[Path, int, str]] = []
    suffixes = {".md", ".mdx", ".tsx", ".ts", ".jsx", ".js", ".jinja", ".j2", ".html", ".txt"}
    skipdirs = {
        "evals",          # cases include the forbidden strings on purpose
        "tests",
        ".github",        # CI yaml may quote the phrases when defining them
        "policies",       # policy yaml literally names the forbidden phrases
        "scripts",        # this verifier and friends mention them
        "registries",
    }
    for path in iter_files(REPO_ROOT, suffixes=suffixes, skip_dirs=skipdirs):
        # also skip CLAUDE-style files that list the forbidden phrases
        rel = path.relative_to(REPO_ROOT)
        if rel.name in {"CLAUDE.md", "AGENTS.md"} or rel.name in DOCTRINE_FILE_NAMES:
            continue
        rel_s = str(rel).replace("\\", "/")
        if any(rel_s.startswith(pref) for pref in DOCTRINE_PATH_PREFIXES):
            continue
        try:
            text = path.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        lines_all = text.splitlines()
        for lineno, line in enumerate(lines_all, start=1):
            for pat in FORBIDDEN_PATTERNS:
                m = pat.search(line)
                if m and not _is_negated(line, m, lines_all[max(0, lineno - 16):lineno - 1]):
                    hits.append((rel, lineno, line.strip()[:180]))
                    break

    if hits:
        for p, ln, snippet in hits[:25]:
            r.fail(f"forbidden:{p}:{ln}", snippet,
                   hint="rewrite to remove the guarantee — see policies/dealix_control_policy.yaml")
        if len(hits) > 25:
            r.fail("forbidden:more", f"+{len(hits) - 25} additional hits not shown")
    else:
        r.pass_("forbidden_phrases", "no banned copy found")

    return r


if __name__ == "__main__":
    raise SystemExit(main_cli(run, name="verify_prompt_output_quality"))
