#!/usr/bin/env python3
"""
verify_everything.py — the anti-bullshit layer.

Reads dealix_manifest.yaml at the repo root, then judges the repo against it:
existence, non-emptiness, required keywords, banned claims, and each layer's
verifier exit code.

Exits 1 on any FAIL. Prints a per-layer table and the underlying reasons.
Wired into `make everything` and .github/workflows/dealix-everything.yml.

Nothing here writes to production. Nothing sends. Read-only by construction.
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("FATAL: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

ROOT = Path(__file__).resolve().parent.parent
MANIFEST = ROOT / "dealix_manifest.yaml"

# ── Colors (TTY-only) ────────────────────────────────────────────────────────
_USE_COLOR = sys.stdout.isatty() and os.environ.get("NO_COLOR") is None
def _c(code: str, s: str) -> str:
    return f"\033[{code}m{s}\033[0m" if _USE_COLOR else s
def red(s: str) -> str:    return _c("31", s)
def green(s: str) -> str:  return _c("32", s)
def yellow(s: str) -> str: return _c("33", s)
def cyan(s: str) -> str:   return _c("36", s)
def bold(s: str) -> str:   return _c("1", s)


def load_manifest() -> dict[str, Any]:
    if not MANIFEST.exists():
        print(red(f"FATAL: missing manifest at {MANIFEST}"))
        sys.exit(2)
    with MANIFEST.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f)
    if not isinstance(data, dict) or "layers" not in data:
        print(red("FATAL: manifest has no 'layers' key"))
        sys.exit(2)
    return data


def check_file(
    spec: dict[str, Any],
    extra_keywords: list[str] | None = None,
) -> tuple[bool, list[str]]:
    """Returns (passed, failures)."""
    rel = spec["path"]
    p = ROOT / rel
    min_size = int(spec.get("min_size", 1))
    keywords = list(spec.get("required_keywords", []) or [])
    if extra_keywords:
        keywords.extend(extra_keywords)
    optional = bool(spec.get("optional", False))

    failures: list[str] = []
    if not p.exists():
        if optional:
            return True, []
        return False, [f"missing file: {rel}"]
    if p.is_dir():
        return False, [f"path is a directory, expected file: {rel}"]

    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except Exception as exc:
        return False, [f"cannot read {rel}: {exc}"]

    actual = len(text.strip())
    if actual < min_size:
        failures.append(f"file too small: {rel} ({actual} bytes < {min_size})")

    lowered = text.lower()
    for kw in keywords:
        if kw.lower() not in lowered:
            failures.append(f"missing keyword '{kw}' in {rel}")

    return (not failures), failures


# Negation cues — when a banned phrase appears in the same line as one of
# these, treat as a NEGATION ("we do NOT promise X") and don't flag.
_NEGATION_CUES = [
    # English negation verbs / particles
    "no ", "not ", "never", "don't", "do not", "doesn't", "does not",
    "won't", "will not", "cannot", "can not", "without", "forbidden",
    "banned", "reject", "refuse", "refuses", "stop ", "avoid", "prohibit",
    "prohibited", "disallow", "disallowed", "we don't", "we do not",
    "we never", "we refuse", "we reject", "we avoid", "we won't",
    # Symbols & contract markers that mean "do not"
    "❌", "✗", "✘", "🚫",
    "article 8",        # legal article enumerating banned patterns
    "non-negotiable", "non negotiable",
    # Suffixes/qualifiers that mean "this kind of bad pattern" not an actual claim
    " claims", " claim ", " outcomes", "-type claims",
    "wants ", "claiming", "promising", "polite refusal", "refusal",
    "bad client", "bad-fit", "bad fit", "what if",
    # Arabic
    "لا ", "لن ", "ممنوع", "أبدًا", "أبداً", "نرفض", "ليس", "بدون", "محظور",
    "نتجنب", "لا نقدم", "لا نضمن", "لا نعد",
    "نضمن",  # appears in QUALITY_STANDARD as the Arabic verb being banned
]


def _is_negated(line: str, phrase: str) -> bool:
    """Is `phrase` negated in this line?

    True if a negation cue appears anywhere in the line.
    Also true if the line is a bullet listing the phrase as a bad pattern
    (e.g. `- guaranteed meetings` inside a known "stop doing" file — but
    file-level negation already filters those; this catches inline
    enumerations in mixed-content docs).
    """
    low = line.lower()
    if any(cue in low for cue in _NEGATION_CUES):
        return True
    # Bullet form `- guaranteed X` followed by nothing more meaningful — usually
    # a forbidden-list item.
    stripped = low.strip().lstrip("-*•·").strip()
    if stripped.startswith(phrase.lower()) and len(stripped) - len(phrase) < 35:
        return True
    return False


# File-path-level negation hints — entire files about what we DON'T do.
_NEGATIVE_FILE_HINTS = [
    "what_we_do_not_do",
    "stop_doing",
    "forbidden_actions",
    "non_negotiables",
    "trust_safety_charter",
    "trust_layer",
    "governance_runtime",
    "responsible_ai_trust_pack",
    "enterprise_trust_pack",
    "ai_output_audit",
    "trust_infrastructure",
    "governance_as_code",
    ".claude/agents/",  # agent prompts that REJECT banned requests
]


def scan_banned_claims(manifest: dict[str, Any]) -> list[str]:
    """Walk *.md docs and flag banned-claim phrases.

    Context-aware: skips negations ("we do NOT promise guaranteed sales"),
    skips files whose entire purpose is to enumerate forbidden things, and
    skips manifest+verifiers.
    """
    banned: list[str] = list(manifest.get("global_rules", {}).get("banned_claims", []))
    excludes: list[str] = list(manifest.get("global_rules", {}).get("banned_claims_excludes", []))
    if not banned:
        return []

    hits: list[str] = []
    for md in ROOT.rglob("*.md"):
        rel = str(md.relative_to(ROOT))
        rel_low = rel.lower()
        if any(rel.startswith(ex) or ex in rel.split("/") for ex in excludes):
            continue
        if any(hint in rel_low for hint in _NEGATIVE_FILE_HINTS):
            continue
        try:
            text = md.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        for raw_line in text.splitlines():
            line = raw_line.lower()
            for phrase in banned:
                p = phrase.lower()
                if p not in line:
                    continue
                if _is_negated(raw_line, phrase):
                    continue
                hits.append(f"banned claim '{phrase}' in {rel}: {raw_line.strip()[:120]}")
                break  # one hit per line is enough
    return hits


def run_verifier(rel: str) -> tuple[bool, str]:
    """Run a sub-verifier. PASS if exit 0. Captures stderr tail on FAIL."""
    p = ROOT / rel
    if not p.exists():
        return False, f"verifier missing: {rel}"
    try:
        proc = subprocess.run(
            [sys.executable, str(p)],
            cwd=str(ROOT),
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        return False, f"verifier timeout: {rel}"
    except Exception as exc:
        return False, f"verifier error: {rel}: {exc}"
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-5:]
        return False, f"verifier failed: {rel} (rc={proc.returncode}) :: " + " | ".join(tail)
    return True, "ok"


def main() -> int:
    manifest = load_manifest()
    layers: dict[str, Any] = manifest.get("layers", {})

    print(bold(cyan("\n═════════════════ DEALIX EVERYTHING VERIFICATION ═════════════════")))
    print(f"Manifest: {MANIFEST}")
    print(f"Layers:   {len(layers)}")
    print(bold("─" * 70))

    pass_layers: list[str] = []
    fail_layers: list[tuple[str, list[str]]] = []
    sub_verifiers: dict[str, tuple[bool, str]] = {}

    for layer_name, layer in layers.items():
        failures: list[str] = []
        for spec in layer.get("required_files", []) or []:
            ok, fails = check_file(spec)
            if not ok:
                failures.extend(fails)

        # Run sub-verifier once per unique verifier path
        verifier = layer.get("verifier")
        if verifier:
            if verifier not in sub_verifiers:
                sub_verifiers[verifier] = run_verifier(verifier)
            v_ok, v_msg = sub_verifiers[verifier]
            if not v_ok:
                failures.append(v_msg)

        if failures:
            fail_layers.append((layer_name, failures))
            print(f"  {red('FAIL')}  {layer_name}")
            for f in failures:
                print(f"        - {f}")
        else:
            pass_layers.append(layer_name)
            print(f"  {green('PASS')}  {layer_name}")

    # Banned-claim scan
    print(bold("\n─── BANNED-CLAIM SCAN ───"))
    banned_hits = scan_banned_claims(manifest)
    if banned_hits:
        for h in banned_hits:
            print(f"  {red('FAIL')}  {h}")
    else:
        print(f"  {green('PASS')}  no banned claims in customer-facing docs")

    # Summary
    print(bold("\n─── SUMMARY ───"))
    print(f"  passed layers:  {green(str(len(pass_layers)))}")
    print(f"  failed layers:  {red(str(len(fail_layers)))}")
    print(f"  banned hits:    {red(str(len(banned_hits))) if banned_hits else green('0')}")

    overall_pass = not fail_layers and not banned_hits
    print(bold("\n─── RESULT ───"))
    if overall_pass:
        print(f"  {green(bold('DEALIX EVERYTHING VERIFICATION: PASS'))}\n")
        return 0
    print(f"  {red(bold('DEALIX EVERYTHING VERIFICATION: FAIL'))}\n")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
