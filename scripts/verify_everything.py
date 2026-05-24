#!/usr/bin/env python3
"""
Dealix Supreme Verifier — verify_everything.py
=================================================

Runs every layer verifier and prints an aggregate PASS/FAIL block.

Usage:
    python scripts/verify_everything.py                  # all 26 layers
    python scripts/verify_everything.py --layer brand    # one layer
    python scripts/verify_everything.py --list           # list layers
    python scripts/verify_everything.py --verbose        # stream child output

Each registered layer verifier must:
  * be invokable as `python <path>` (or `bash <path>` for shell)
  * print `<LAYER_NAME>: PASS|FAIL` as its FINAL line
  * exit 0 on PASS, non-zero on FAIL

The supreme verifier exits 0 only when every layer passes.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
VERIFIERS_DIR = REPO_ROOT / "scripts" / "verifiers"


@dataclass(frozen=True)
class Layer:
    key: str           # CLI alias (e.g. "brand")
    name: str          # display name (e.g. "Brand OS")
    runner: list[str]  # command argv (interpreter resolved at runtime)


def _py(*relpath: str) -> list[str]:
    """Return a python-runner argv pointing at scripts/verifiers/<relpath>."""
    return [sys.executable, str(VERIFIERS_DIR.joinpath(*relpath))]


def _bash(*relpath: str) -> list[str]:
    """Return a bash-runner argv pointing at scripts/<relpath>."""
    bash = shutil.which("bash") or "/bin/bash"
    return [bash, str(REPO_ROOT.joinpath(*relpath))]


LAYERS: list[Layer] = [
    Layer("brand",              "Brand OS",                    _py("verify_brand_system.py")),
    Layer("founder-console",    "Founder Console",             _py("verify_founder_console.py")),
    Layer("company-os",         "CEO Operating System",        _py("verify_company_os.py")),
    Layer("capital-allocation", "Capital Allocation",          _py("verify_capital_allocation.py")),
    Layer("strategy-metrics",   "Strategy Metrics",            _py("verify_strategy_metrics.py")),
    Layer("revenue-factory",    "Revenue Factory",             _py("verify_revenue_factory.py")),
    Layer("launch-layer",       "Launch Layer",                _py("verify_launch_layer.py")),
    Layer("market-attack",      "Market Attack System",        _py("verify_market_attack_system.py")),
    Layer("scale-moat",         "Scale Moat System",           _py("verify_scale_moat_system.py")),
    Layer("founder-mgmt",       "Founder Management System",   _py("verify_company_os.py")),  # shares verifier
    Layer("hypergrowth",        "Hypergrowth CEO Layer",       _py("verify_founder_ceo_hypergrowth_layer.py")),
    Layer("ai-governance",      "AI Governance",               _py("verify_ai_governance.py")),
    Layer("policy-as-code",     "Policy-as-Code",              _py("verify_policy_as_code.py")),
    Layer("agent-registry",     "Agent Registry",              _py("verify_agent_registry.py")),
    Layer("machine-registry",   "Machine Registry",            _py("verify_machine_registry.py")),
    Layer("eval-gate",          "Eval Gate",                   _py("verify_eval_gate.py")),
    Layer("private-ops",        "Private Ops Runtime",         _py("verify_private_ops_runtime.py")),
    Layer("internal-api",       "Internal API",                _py("smoke_internal_api.py")),
    Layer("worker-orch",        "Worker Orchestrator",         _py("verify_worker_orchestrator.py")),
    Layer("customer-success",   "Customer Success",            _py("verify_customer_success.py")),
    Layer("enterprise-sales",   "Enterprise Sales",            _py("verify_enterprise_sales.py")),
    Layer("legal-trust",        "Legal Trust Security",        _py("verify_legal_trust_security.py")),
    Layer("company-memory",     "Company Memory",              _py("verify_company_memory.py")),
    Layer("verifiers",          "Verifiers",                   _py("verify_verifiers.py")),
    Layer("makefile",           "Makefile",                    _py("verify_makefile.py")),
    Layer("github-actions",     "GitHub Actions",              _py("verify_github_actions.py")),
]


def list_layers() -> None:
    print(f"{'KEY':<22} {'NAME':<32} RUNNER")
    print("-" * 80)
    for layer in LAYERS:
        runner = " ".join(Path(p).name if Path(p).is_absolute() else p for p in layer.runner)
        print(f"{layer.key:<22} {layer.name:<32} {runner}")


def run_layer(layer: Layer, verbose: bool) -> tuple[bool, str]:
    """Run a single verifier; return (passed, last-line)."""
    try:
        proc = subprocess.run(
            layer.runner,
            cwd=str(REPO_ROOT),
            capture_output=True,
            text=True,
            timeout=180,
        )
    except FileNotFoundError:
        return False, f"{layer.name}: FAIL (verifier missing)"
    except subprocess.TimeoutExpired:
        return False, f"{layer.name}: FAIL (timeout)"

    stdout = (proc.stdout or "").strip()
    stderr = (proc.stderr or "").strip()

    if verbose:
        if stdout:
            print(stdout)
        if stderr:
            print(stderr, file=sys.stderr)

    last = stdout.splitlines()[-1] if stdout else f"{layer.name}: FAIL (no output)"
    passed = proc.returncode == 0 and last.upper().endswith(": PASS")
    if not passed and not last.upper().endswith(("PASS", "FAIL")):
        last = f"{layer.name}: FAIL ({last[:80] or 'no output'})"
    return passed, last


def main() -> int:
    parser = argparse.ArgumentParser(description="Dealix supreme verifier (26 layers).")
    parser.add_argument("--layer", help="Run one layer by key (see --list).")
    parser.add_argument("--list", action="store_true", help="List registered layers.")
    parser.add_argument("--verbose", action="store_true", help="Stream child stdout/stderr.")
    args = parser.parse_args()

    if args.list:
        list_layers()
        return 0

    layers = LAYERS
    if args.layer:
        layers = [L for L in LAYERS if L.key == args.layer]
        if not layers:
            print(f"Unknown layer: {args.layer!r}. Use --list.", file=sys.stderr)
            return 2

    print("DEALIX EVERYTHING VERIFICATION")
    overall_pass = True
    for layer in layers:
        passed, last = run_layer(layer, verbose=args.verbose)
        # Normalize line so output is always `<Name>: PASS|FAIL`.
        if last.upper().endswith(": PASS"):
            print(f"{layer.name}: PASS")
        else:
            print(f"{layer.name}: FAIL")
            overall_pass = False

    print(f"RESULT: {'PASS' if overall_pass else 'FAIL'}")
    return 0 if overall_pass else 1


if __name__ == "__main__":
    sys.exit(main())
