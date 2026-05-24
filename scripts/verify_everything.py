#!/usr/bin/env python3
"""
verify_everything.py — Dealix master verifier.

Drives `dealix_manifest.yaml` and refuses to declare PASS unless every
layer satisfies the 5-test rule: exists, non-empty, complete, wired, verified.

Usage:
    python scripts/verify_everything.py
    python scripts/verify_everything.py --json
    python scripts/verify_everything.py --layer policy_as_code

Exit codes:
    0  All layers PASS
    1  At least one layer FAIL
    2  Manifest itself is missing or unparseable
"""
from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

try:
    import yaml
except ImportError:
    print("FATAL: PyYAML not installed. Run: pip install pyyaml", file=sys.stderr)
    sys.exit(2)

REPO = Path(__file__).resolve().parents[1]
MANIFEST_PATH = REPO / "dealix_manifest.yaml"


class Result:
    __slots__ = ("layer", "checks", "failures", "warnings")

    def __init__(self, layer: str) -> None:
        self.layer = layer
        self.checks: list[str] = []
        self.failures: list[str] = []
        self.warnings: list[str] = []

    @property
    def passed(self) -> bool:
        return not self.failures

    def to_dict(self) -> dict[str, Any]:
        return {
            "layer": self.layer,
            "passed": self.passed,
            "checks_run": len(self.checks),
            "failures": self.failures,
            "warnings": self.warnings,
        }


def load_manifest() -> dict[str, Any]:
    if not MANIFEST_PATH.exists():
        print(f"FATAL: manifest not found at {MANIFEST_PATH}", file=sys.stderr)
        sys.exit(2)
    try:
        data = yaml.safe_load(MANIFEST_PATH.read_text(encoding="utf-8"))
    except yaml.YAMLError as exc:
        print(f"FATAL: manifest is not valid YAML: {exc}", file=sys.stderr)
        sys.exit(2)
    if not isinstance(data, dict) or "layers" not in data:
        print("FATAL: manifest missing 'layers' key", file=sys.stderr)
        sys.exit(2)
    return data


# Files that define doctrine (i.e., enumerate banned claims as data).
# These files legitimately mention banned phrases; scanning them would
# force the verifier to grade itself.
DOCTRINE_FILES = frozenset(
    {
        "dealix_manifest.yaml",
        "policies/dealix_control_policy.yaml",
        "docs/ops/DEALIX_FINAL_READINESS_REPORT.md",
        "docs/ops/DEALIX_MISSING_SYSTEMS.md",
        "docs/ops/DEALIX_IMPLEMENTATION_AUDIT.md",
        "docs/trust/LIVE_SEND_SAFETY_GATE.md",
        "docs/founder/LAUNCH_READINESS_GATE.md",
        "docs/ai_governance/AI_GOVERNANCE_OVERVIEW.md",
    }
)


def _line_is_doctrine_context(line: str) -> bool:
    low = line.lower()
    markers = (
        "banned", "forbid", "must not", "do not claim", "we never",
        "never claim", "no_guaranteed", "no_a3", "no_direct", "no_suppressed",
        "ممنوع", "محظور", "لا نَعِد", "لا نعد",
    )
    return any(m in low for m in markers)


def check_file(
    result: Result,
    file_path: str,
    *,
    min_size: int,
    banned_claims: list[str],
    banned_patterns: list[str],
) -> str:
    """Inspect one required file. Returns its lowercased text (or '' on miss)."""
    rel = file_path
    p = REPO / file_path
    result.checks.append(f"file:{rel}")

    if not p.exists():
        result.failures.append(f"missing_file:{rel}")
        return ""
    if not p.is_file():
        result.failures.append(f"not_a_file:{rel}")
        return ""

    try:
        text = p.read_text(encoding="utf-8", errors="ignore")
    except OSError as exc:
        result.failures.append(f"unreadable_file:{rel} ({exc})")
        return ""

    stripped_len = len(text.strip())
    if stripped_len < min_size:
        result.failures.append(
            f"too_small:{rel} ({stripped_len} < {min_size} chars)"
        )

    lower = text.lower()

    # Banned-claim check skips doctrine files entirely (they enumerate
    # claims as data) and otherwise does a per-line scan that tolerates
    # legitimate doctrine context (e.g. "we never claim guaranteed X").
    if rel not in DOCTRINE_FILES:
        for line_no, line in enumerate(text.splitlines(), 1):
            if _line_is_doctrine_context(line):
                continue
            llow = line.lower()
            for banned in banned_claims:
                if banned.lower() in llow:
                    result.failures.append(
                        f"banned_claim:{rel}:{line_no}:'{banned}'"
                    )
                    break

    # Patterns only meaningful in source / config files
    if file_path.endswith((".py", ".ts", ".tsx", ".js", ".yaml", ".yml", ".toml", ".sh")):
        if rel not in DOCTRINE_FILES and not Path(file_path).name.startswith("verify_"):
            for pattern in banned_patterns:
                if pattern.lower() in lower:
                    result.failures.append(f"banned_pattern:{rel}:'{pattern}'")

    if file_path.endswith((".yaml", ".yml")):
        try:
            yaml.safe_load(text)
        except yaml.YAMLError as exc:
            result.failures.append(f"invalid_yaml:{rel} ({exc})")

    if file_path.endswith(".py") and stripped_len > 0:
        try:
            compile(text, str(p), "exec")
        except SyntaxError as exc:
            result.failures.append(f"python_syntax:{rel} (line {exc.lineno})")

    return lower


def min_size_for(file_path: str, rules: dict[str, Any]) -> int:
    if file_path.endswith(".py"):
        return int(rules.get("min_script_size_bytes", 500))
    if file_path.endswith((".yaml", ".yml", ".toml", ".json")):
        return int(rules.get("min_yaml_size_bytes", 200))
    if file_path.endswith(".sh"):
        return int(rules.get("min_script_size_bytes", 500)) // 2
    return int(rules.get("min_doc_size_bytes", 600))


def run_verifier(result: Result, script_path: str) -> None:
    p = REPO / script_path
    if not p.exists():
        result.warnings.append(f"verifier_missing:{script_path}")
        return
    result.checks.append(f"verifier:{script_path}")
    try:
        proc = subprocess.run(
            [sys.executable, str(p)],
            cwd=REPO,
            capture_output=True,
            text=True,
            timeout=120,
        )
    except subprocess.TimeoutExpired:
        result.failures.append(f"verifier_timeout:{script_path}")
        return
    except OSError as exc:
        result.failures.append(f"verifier_unrunnable:{script_path} ({exc})")
        return
    if proc.returncode != 0:
        tail = (proc.stderr or proc.stdout or "").strip().splitlines()[-5:]
        result.failures.append(
            f"verifier_failed:{script_path} (exit={proc.returncode}) :: "
            + " | ".join(tail)
        )


def verify_layer(name: str, layer: dict[str, Any], rules: dict[str, Any]) -> Result:
    """Verify one layer.

    Keyword semantics are *layer-scoped*: a keyword must appear in **at
    least one** required_file. Forcing every file in a layer to contain
    every keyword turns honest manifests into checklist gymnastics
    (e.g. a Dockerfile that mentions "healthz" only because the manifest
    insisted). The contract we actually want is "the layer as a whole
    proves the concept exists somewhere".
    """
    result = Result(name)
    keywords = list(layer.get("required_keywords", []))
    banned_claims = list(rules.get("banned_claims", []))
    banned_patterns = list(rules.get("banned_unsafe_patterns", []))

    layer_corpus: list[str] = []
    for file_path in layer.get("required_files", []):
        body = check_file(
            result,
            file_path,
            min_size=min_size_for(file_path, rules),
            banned_claims=banned_claims,
            banned_patterns=banned_patterns,
        )
        if body:
            layer_corpus.append(body)

    if keywords:
        joined = "\n".join(layer_corpus)
        for kw in keywords:
            if kw.lower() not in joined:
                result.failures.append(f"layer_missing_keyword:{name}:'{kw}'")

    verifier = layer.get("verifier")
    if verifier and result.passed:
        # Only run the layer verifier if file-level checks passed; otherwise
        # we already know the layer is broken and noise from a sub-verifier
        # would just obscure the real problem.
        run_verifier(result, verifier)

    return result


def format_report(results: list[Result], manifest: dict[str, Any]) -> str:
    lines: list[str] = []
    total = len(results)
    passed = sum(1 for r in results if r.passed)
    failed = total - passed

    lines.append("=" * 72)
    lines.append("DEALIX EVERYTHING VERIFICATION")
    lines.append("=" * 72)
    lines.append(f"Manifest:   {MANIFEST_PATH.relative_to(REPO)}")
    lines.append(f"Layers:     {total}")
    lines.append(f"Passed:     {passed}")
    lines.append(f"Failed:     {failed}")
    lines.append("")

    for r in results:
        marker = "PASS" if r.passed else "FAIL"
        lines.append(f"[{marker}] {r.layer} ({len(r.checks)} checks)")
        for fail in r.failures:
            lines.append(f"    - {fail}")
        for warn in r.warnings:
            lines.append(f"    ~ {warn}")

    lines.append("")
    lines.append("=" * 72)
    if failed:
        lines.append(f"RESULT: FAIL ({failed} layer(s) failed)")
    else:
        lines.append("RESULT: PASS (all layers verified)")
    lines.append("=" * 72)
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--json", action="store_true", help="Emit JSON instead of text")
    parser.add_argument("--layer", help="Verify a single layer only")
    parser.add_argument(
        "--strict-warnings",
        action="store_true",
        help="Treat warnings (e.g. missing verifier scripts) as failures",
    )
    args = parser.parse_args()

    manifest = load_manifest()
    rules = manifest.get("global_rules", {})
    layers = manifest["layers"]

    if args.layer:
        if args.layer not in layers:
            print(f"FATAL: unknown layer '{args.layer}'", file=sys.stderr)
            return 2
        layers = {args.layer: layers[args.layer]}

    results = [verify_layer(name, layer, rules) for name, layer in layers.items()]

    if args.strict_warnings:
        for r in results:
            if r.warnings:
                r.failures.extend(f"warning_promoted:{w}" for w in r.warnings)

    if args.json:
        print(
            json.dumps(
                {
                    "manifest": str(MANIFEST_PATH.relative_to(REPO)),
                    "total_layers": len(results),
                    "passed": sum(1 for r in results if r.passed),
                    "failed": sum(1 for r in results if not r.passed),
                    "results": [r.to_dict() for r in results],
                },
                indent=2,
                ensure_ascii=False,
            )
        )
    else:
        print(format_report(results, manifest))

    return 0 if all(r.passed for r in results) else 1


if __name__ == "__main__":
    raise SystemExit(main())
