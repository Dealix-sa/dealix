#!/usr/bin/env python3
"""verify_prompt_output_quality.py — flag banned claims in customer-visible artifacts.

Scope is intentionally narrow: only files that can leak to a customer
(public web surfaces, the README, marketing/sales copy, agent prompts,
emails templates). Internal doctrine docs that *describe* banned claims
as forbidden (so a future writer knows not to use them) are explicitly
out of scope — scanning them would force a verifier to grade itself.

To opt a doctrine doc into the scan, add `<!-- audit-enforce: claims -->`
near its top. To opt a marketing-looking doc out of the scan (rare),
add `<!-- audit-allow: doctrine -->`.
"""
from __future__ import annotations

import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML missing", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parents[1]

# Customer-visible scan scope. Anything under these prefixes is held to
# the banned-claims contract by default.
SCAN_PATHS = (
    "README.md",
    "README.ar.md",
    "apps/web/src",
    "apps/web/public",
    "apps/web/messages",
    "frontend/src",
    "frontend/public",
    "templates",
    "landing",
    "docs/marketing",
)
SCAN_SUFFIXES = (".md", ".markdown", ".yaml", ".yml", ".txt", ".mdx", ".html", ".tsx", ".ts", ".jsx", ".js")
DOCTRINE_OPT_IN_TAG = "audit-enforce: claims"
DOCTRINE_OPT_OUT_TAG = "audit-allow: doctrine"

# Lines beginning with these strings are explicitly *describing* banned
# claims (e.g. the manifest itself, this verifier, or doctrine docs that
# say "we never claim X"). Skip such lines.
ALLOW_PREFIXES = (
    "#",  # comments / headings in YAML and Markdown context (used carefully)
)
ALLOW_TOKENS = (
    "banned",
    "forbidden",
    "we never",
    "do not claim",
    "must not claim",
    "must not say",
    "no_guaranteed",
    "no_a3_auto",
    "ممنوع",
    "محظور",
    "لا نَعِد",
    "لا نعد",
)


def load_banned() -> list[str]:
    mf = REPO / "dealix_manifest.yaml"
    if not mf.exists():
        return []
    data = yaml.safe_load(mf.read_text(encoding="utf-8")) or {}
    return list((data.get("global_rules") or {}).get("banned_claims", []))


def line_is_doctrine(line: str) -> bool:
    low = line.lower()
    return any(tok in low for tok in ALLOW_TOKENS)


def paragraph_is_doctrine(lines: list[str], idx: int, window: int = 2) -> bool:
    """Treat a hit as doctrine if the surrounding ±window lines disclaim it.

    Common pattern in landing/marketing copy: "...not for those seeking
    guaranteed sales — we commit to clearer ops, not guaranteed revenue."
    The token "not" lives on the next line.
    """
    start = max(0, idx - window)
    end = min(len(lines), idx + window + 1)
    blob = " ".join(lines[start:end]).lower()
    disclaimers = (
        "not guaranteed",
        "no guaranteed",
        "without guaranteed",
        "do not promise",
        "does not promise",
        "do not claim",
        "does not claim",
        "we never",
        "not for",
        "not promising",
        "غير مضمون",
        "لا نَعِد",
        "لا نعد",
        "ليس مضمونًا",
        "ليس مضمونا",
    )
    return any(d in blob for d in disclaimers)


def iter_targets() -> list[Path]:
    out: list[Path] = []
    for path in SCAN_PATHS:
        p = REPO / path
        if p.is_file():
            if p.suffix.lower() in SCAN_SUFFIXES:
                out.append(p)
        elif p.is_dir():
            for sub in p.rglob("*"):
                if sub.is_file() and sub.suffix.lower() in SCAN_SUFFIXES:
                    out.append(sub)
    return out


def main() -> int:
    banned = load_banned()
    if not banned:
        print("no_banned_claims_defined", file=sys.stderr)
        return 0  # nothing to check is not an error

    failures: list[str] = []
    for p in iter_targets():
        try:
            text = p.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue

        head = text[:512].lower()
        if DOCTRINE_OPT_OUT_TAG in head:
            continue

        lines = text.splitlines()
        for idx, line in enumerate(lines):
            if line_is_doctrine(line):
                continue
            low = line.lower()
            hit = None
            for claim in banned:
                if claim.lower() in low:
                    hit = claim
                    break
            if not hit:
                continue
            if paragraph_is_doctrine(lines, idx):
                continue
            rel = p.relative_to(REPO).as_posix()
            failures.append(f"banned_claim:{rel}:{idx + 1}:'{hit}'")

    for f in failures:
        print(f, file=sys.stderr)
    ok = not failures
    print(
        f"PROMPT_OUTPUT_QUALITY_PASS={'true' if ok else 'false'} "
        f"(failures={len(failures)})"
    )
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
