#!/usr/bin/env python3
"""Generate the Dealix Sovereign Readiness scorecard.

This is the highest-level founder gate. It scores the readiness of each
layer of the Sovereign Operating Stack and writes
``<private_ops>/founder/sovereign_readiness.md``.

Readiness is binary per layer: present + verifier passes → 1, else 0.
We then derive a percentage. Honest, no inflation.
"""

from __future__ import annotations

import argparse
import datetime as _dt
import os
import subprocess
import sys
from pathlib import Path


def _root(args) -> Path:
    return Path(args.private_ops or os.environ.get("DEALIX_PRIVATE_OPS", "/opt/dealix-ops-private"))


def _exists(path: str) -> bool:
    return Path(path).exists()


def _run(cmd: list[str]) -> bool:
    try:
        return subprocess.run(cmd, capture_output=True, text=True, timeout=60).returncode == 0
    except Exception:
        return False


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--private-ops", default=None)
    args = p.parse_args()
    root = _root(args)

    layers: list[tuple[str, bool]] = [
        ("Founder Console pages", _exists("apps/web/app/ceo/page.tsx")),
        ("Sovereign page", _exists("apps/web/app/sovereign/page.tsx")),
        ("Control Plane page", _exists("apps/web/app/control-plane/page.tsx")),
        ("Founder Shell", _exists("apps/web/components/founder-shell.tsx")),
        ("Runtime client", _exists("apps/web/lib/dealix-runtime.ts")),
        ("Action client", _exists("apps/web/lib/dealix-actions.ts")),
        ("Internal API auth", _exists("api/internal/auth.py")),
        ("Internal runtime reader", _exists("api/internal/runtime_reader.py")),
        ("Internal policy adapter", _exists("api/internal/policy_adapter.py")),
        ("Internal router", _exists("api/routers/internal/founder_console.py")),
        ("Policy-as-Code", _exists("policies/dealix_control_policy.yaml")),
        ("Agent Registry", _exists("registries/agent_registry.yaml")),
        ("Eval Gate", _exists("evals/gates/dealix_agent_eval_gate.yaml")),
        ("Bootstrap script", _exists("scripts/bootstrap_private_ops_runtime.py")),
        ("Worker state helper", _exists("scripts/update_worker_state.py")),
        ("Operating scorecard script", _exists("scripts/generate_operating_scorecard.py")),
        ("GitHub workflow", _exists(".github/workflows/dealix-sovereign-operating-stack.yml")),
        ("Policy verifier", _run([sys.executable, "scripts/verify_policy_as_code.py"])),
        ("Agent registry verifier", _run([sys.executable, "scripts/verify_agent_registry.py"])),
        ("Eval gate verifier", _run([sys.executable, "scripts/verify_eval_gate.py"])),
        ("Prompt/output safety", _run([sys.executable, "scripts/verify_prompt_output_quality.py"])),
    ]

    score = sum(1 for _, ok in layers if ok)
    total = len(layers)
    pct = round(100 * score / total) if total else 0

    lines = [
        "# Dealix — Sovereign Readiness Scorecard",
        "",
        f"Generated: {_dt.datetime.now(_dt.UTC).isoformat(timespec='seconds')}",
        f"Private runtime: `{root}`",
        "",
        f"**Overall: {score}/{total} ({pct}%)**",
        "",
        "| Layer | Ready |",
        "| --- | :---: |",
    ]
    for name, ok in layers:
        lines.append(f"| {name} | {'PASS' if ok else 'FAIL'} |")

    lines += [
        "",
        "## Notes",
        "- This scorecard runs the local verifiers; it does not perform network calls.",
        "- A 100% score does NOT imply production readiness — that is a separate gate.",
        "- See `docs/security/PRODUCTION_SECURITY_GATE.md`.",
    ]

    out = root / "founder/sovereign_readiness.md"
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print(f"[OK] wrote {out}  ({score}/{total})")
    return 0 if pct >= 60 else 1


if __name__ == "__main__":
    raise SystemExit(main())
