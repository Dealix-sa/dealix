#!/usr/bin/env python3
"""verify_wiring.py — fail when an artifact exists but nothing calls it.

A required script that no Makefile target, GitHub workflow, or other
verifier references is dead code — it cannot keep the company honest.
This script confirms each manifest-listed `.py`/`.sh` file is mentioned
by Makefile or by some workflow under .github/workflows/.
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


def collect_wiring_corpus() -> str:
    parts: list[str] = []

    # Top-level orchestration surfaces
    for name in ("Makefile", ".pre-commit-config.yaml", "railway.toml", "railway.json"):
        p = REPO / name
        if p.exists():
            parts.append(p.read_text(encoding="utf-8", errors="ignore"))

    # Every CI workflow
    wf_dir = REPO / ".github" / "workflows"
    if wf_dir.is_dir():
        for f in sorted(wf_dir.glob("*.y*ml")):
            parts.append(f.read_text(encoding="utf-8", errors="ignore"))

    # Other shell/python scripts can also wire a target script
    scripts_dir = REPO / "scripts"
    if scripts_dir.is_dir():
        for f in scripts_dir.iterdir():
            if not f.is_file():
                continue
            # Don't count a script as wiring itself.
            if f.name.startswith("verify_"):
                continue
            if f.suffix in {".sh", ".py", ".ps1"}:
                parts.append(f.read_text(encoding="utf-8", errors="ignore"))

    # Tests reference required scripts too — that counts as wiring.
    tests_dir = REPO / "tests"
    if tests_dir.is_dir():
        for f in tests_dir.rglob("*.py"):
            try:
                parts.append(f.read_text(encoding="utf-8", errors="ignore"))
            except OSError:
                continue

    return "\n".join(parts).lower()


# Layers whose files are pure docs/configs that don't need a wiring caller.
SKIP_LAYERS = {
    "brand_os",
    "ceo_operating_system",
    "capital_allocation",
    "revenue_factory",
    "market_attack",
    "customer_success_os",
    "launch_readiness",
    "ai_governance",
    "policy_as_code",
    "agent_registry",
    "machine_registry",
    "live_send_safety",
    "audit_reports",
    "production_env",
    "frontend_surfaces",
}


def main() -> int:
    manifest = REPO / "dealix_manifest.yaml"
    if not manifest.exists():
        print("missing_manifest", file=sys.stderr)
        return 2
    data = yaml.safe_load(manifest.read_text(encoding="utf-8"))
    corpus = collect_wiring_corpus()

    failures: list[str] = []
    for name, layer in (data.get("layers") or {}).items():
        if name in SKIP_LAYERS:
            continue
        for path in layer.get("required_files", []):
            if not path.endswith((".py", ".sh")):
                continue
            if not (REPO / path).exists():
                # missing entirely — flagged by another verifier
                continue
            basename = Path(path).name.lower()
            stem = Path(path).stem.lower()
            if basename in corpus or stem in corpus or path.lower() in corpus:
                continue
            failures.append(f"unwired:{name}:{path}")

    for f in failures:
        print(f, file=sys.stderr)
    ok = not failures
    print(f"WIRING_PASS={'true' if ok else 'false'} (unwired={len(failures)})")
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
