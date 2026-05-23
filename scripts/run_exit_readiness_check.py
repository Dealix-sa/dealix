#!/usr/bin/env python3
"""Exit Readiness OS monthly gate check script.

Loads VentureGateChecklist state and computes governance runtime maturity.
Writes a founder brief markdown file.

Usage:
  python scripts/run_exit_readiness_check.py [--dry-run]
"""
from __future__ import annotations

import argparse
import json
import os
import sys
from datetime import date, datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))


_STATE_PATH = ROOT / "var" / "exit_readiness_state.json"

_DEFAULT_GATE_STATE: dict[str, bool] = {
    "paid_clients_5plus": False,
    "retainers_2plus": False,
    "repeatable_delivery": False,
    "product_module_clear": False,
    "playbook_maturity_80plus": False,
    "owner_exists": False,
    "healthy_margin": False,
    "proof_library_exists": False,
    "core_os_dependency_clear": False,
}


def _load_gate_state() -> dict[str, bool]:
    if _STATE_PATH.exists():
        try:
            raw = json.loads(_STATE_PATH.read_text(encoding="utf-8"))
            merged = dict(_DEFAULT_GATE_STATE)
            for k in _DEFAULT_GATE_STATE:
                if k in raw and isinstance(raw[k], bool):
                    merged[k] = raw[k]
            return merged
        except Exception:
            pass
    return dict(_DEFAULT_GATE_STATE)


def run(dry_run: bool) -> None:
    today = date.today().isoformat()
    output_dir = ROOT / "data" / "founder_briefs"
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"EXIT_READINESS_{today}.md"

    if dry_run:
        try:
            from auto_client_acquisition.endgame_os import (
                VentureGateChecklist,
                GOVERNANCE_RUNTIME_COMPONENTS,
                governance_runtime_maturity_score,
                venture_gate_passes,
            )
        except Exception as exc:
            print(f"[Exit Readiness] Import error: {exc}", file=sys.stderr)
            sys.exit(1)

        gate_state = _load_gate_state()
        checklist = VentureGateChecklist(**gate_state)
        gates_passed = sum(1 for v in gate_state.values() if v)
        gates_total = len(gate_state)
        gate_pct = gates_passed / gates_total if gates_total else 0

        # Detect implemented governance components from actual module/file presence
        import importlib.util as _ilu
        _GOV_COMPONENT_MODULES: dict[str, str] = {
            "policy_engine": "auto_client_acquisition.governance_os",
            "pii_detection": "auto_client_acquisition.saudi_layer",
            "audit_log": "api.middleware",
            "approval_engine": "auto_client_acquisition.governance_os.approval_policy",
            "allowed_use_checker": "auto_client_acquisition.governance_os",
            "claim_safety_checker": "auto_client_acquisition.governance_os",
            "channel_risk_checker": "auto_client_acquisition.governance_os.channel_policy",
            "ai_run_ledger": "auto_client_acquisition.friction_log",
            "risk_index": "auto_client_acquisition.governance_os",
            "escalation_rules": "auto_client_acquisition.governance_os.approval_matrix",
        }
        implemented = frozenset(
            c for c, m in _GOV_COMPONENT_MODULES.items()
            if _ilu.find_spec(m) is not None
        )
        gov_score = governance_runtime_maturity_score(implemented)
        gov_max = len(GOVERNANCE_RUNTIME_COMPONENTS)

        # Venture gate pass status
        can_exit = venture_gate_passes(checklist)

        print(
            f"[Exit Readiness] Gates: {gates_passed}/{gates_total} "
            f"({gate_pct:.0%}) | Gov runtime: {gov_score}/100 | "
            f"Exit gate: {'PASS' if can_exit else 'FAIL'}"
        )

        brief = f"""# Exit Readiness OS — Monthly Gate Check
## {today}

**Generated**: {datetime.now(timezone.utc).isoformat()}
**Mode**: dry-run (local modules)

---

## Venture Gate Checklist ({gates_passed}/{gates_total} passed)

| Gate | Status |
|------|--------|
"""
        for gate, passed in gate_state.items():
            status = "PASS" if passed else "fail"
            brief += f"| {gate} | {status} |\n"

        brief += f"""
**Venture Gate Decision**: {"EXIT READY" if can_exit else "NOT READY — address failing gates first"}

---

## Governance Runtime Maturity

- **Score**: {gov_score} / 100
- **Components**: {', '.join(sorted(GOVERNANCE_RUNTIME_COMPONENTS)[:5])}{"..." if len(GOVERNANCE_RUNTIME_COMPONENTS) > 5 else ""}

---

## Next Steps

"""
        failing = [k for k, v in gate_state.items() if not v]
        if failing:
            brief += "Address the following gates before Series A / exit preparation:\n\n"
            for f in failing:
                brief += f"- [ ] {f}\n"
        else:
            brief += "All gates passed. Review with legal counsel before initiating exit process.\n"

        state_source = "var/exit_readiness_state.json" if _STATE_PATH.exists() else "default (all False)"
        brief += f"\n_State loaded from: {state_source}_\n"
        brief += "\n---\n_is_estimate=True. All readiness scores are estimates. Require founder and legal review._\n"
        output_path.write_text(brief, encoding="utf-8")
        print(f"[Exit Readiness] Brief written → {output_path}")
        return

    # Live mode
    import urllib.request
    api_base = os.environ.get("DEALIX_API_BASE", "https://api.dealix.me")
    admin_key = os.environ.get("DEALIX_ADMIN_API_KEY", "")
    api_key = os.environ.get("DEALIX_API_KEY", "")

    def _get(path: str) -> dict:
        url = f"{api_base}{path}"
        req = urllib.request.Request(
            url,
            headers={"X-API-Key": api_key, "X-Admin-API-Key": admin_key},
        )
        with urllib.request.urlopen(req, timeout=30) as r:
            return json.loads(r.read())

    try:
        result = _get("/api/v1/exit-readiness/exit-readiness-summary")
    except Exception as exc:
        print(f"[Exit Readiness] API call failed: {exc}", file=sys.stderr)
        sys.exit(1)

    brief = f"""# Exit Readiness OS — Monthly Gate Check
## {today}

**Generated**: {datetime.now(timezone.utc).isoformat()}
**Mode**: live

---

## Summary
"""
    for k, v in result.items():
        if k not in ("is_estimate", "governance_decision"):
            brief += f"- **{k}**: {v}\n"

    brief += "\n---\n_is_estimate=True. All readiness scores are estimates. Require founder and legal review._\n"
    output_path.write_text(brief, encoding="utf-8")
    print(f"[Exit Readiness] Brief written → {output_path}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run Exit Readiness OS monthly gate check")
    parser.add_argument("--dry-run", action="store_true", help="Use local modules; no HTTP calls")
    args = parser.parse_args()
    run(dry_run=args.dry_run)
