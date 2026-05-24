#!/usr/bin/env python3
"""
verify_everything.py — Dealix Company OS master verifier.

Pattern follows scripts/v10_master_verify.sh: runs every sub-verifier,
prints per-layer ✅/❌, then a verdict block.

Sub-verifiers (new in this OS surface):
  - verify_policy_as_code
  - verify_agent_registry
  - verify_machine_registry
  - verify_eval_gate
  - verify_brand_system
  - verify_growth_system
  - verify_marketing_system
  - verify_product_distribution
  - verify_market_attack_system
  - verify_scale_moat_system
  - verify_founder_ceo_hypergrowth_layer
  - verify_prompt_output_quality

Existing verifiers (treated as informational unless --include-existing):
  - verify_governance_rules
  - verify_service_readiness_matrix
  - verify_reference_library_70

Hard-rule invariants (always enforced):
  - is_live_charge_allowed() is False
  - WhatsApp live send banned
  - LinkedIn automation banned
  - Scraping banned
  - claim_policy.roi_or_guarantee.allowed is False

Usage:
  python scripts/verify_everything.py [--strict] [--include-existing] [--json]

Exit: 0 PASS / 1 FAIL.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SCRIPTS = ROOT / "scripts"

NEW_VERIFIERS = [
    ("Policy-as-Code",            "verify_policy_as_code.py"),
    ("Agent Registry",            "verify_agent_registry.py"),
    ("Machine Registry",          "verify_machine_registry.py"),
    ("Eval Gate",                 "verify_eval_gate.py"),
    ("Brand System",              "verify_brand_system.py"),
    ("Growth System",             "verify_growth_system.py"),
    ("Marketing System",          "verify_marketing_system.py"),
    ("Product Distribution",      "verify_product_distribution.py"),
    ("Market-Attack System",      "verify_market_attack_system.py"),
    ("Scale/Moat System",         "verify_scale_moat_system.py"),
    ("Founder-CEO Hypergrowth",   "verify_founder_ceo_hypergrowth_layer.py"),
    ("Prompt-Output Quality",     "verify_prompt_output_quality.py"),
]
EXISTING_VERIFIERS = [
    ("Governance Rules",          "verify_governance_rules.py"),
    ("Service Readiness Matrix",  "verify_service_readiness_matrix.py"),
    ("Reference Library 70",      "verify_reference_library_70.py"),
]


def _run(script: str, *, strict: bool) -> tuple[int, str]:
    path = SCRIPTS / script
    if not path.exists():
        return 2, f"{script}: missing"
    args = [sys.executable, str(path)]
    if strict and script in {v for _, v in NEW_VERIFIERS}:
        args.append("--strict")
    try:
        proc = subprocess.run(args, capture_output=True, text=True, timeout=120, check=False)
    except subprocess.TimeoutExpired:
        return 1, f"{script}: timeout"
    head = ""
    for line in (proc.stdout or "").splitlines():
        if "=" in line and line.split("=")[0].isupper():
            head = line.strip()
            break
    if not head:
        head = (proc.stdout or proc.stderr or "").strip().splitlines()[-1:][0] if (proc.stdout or proc.stderr) else "no output"
    return proc.returncode, head


def _hard_rule_invariants() -> tuple[bool, list[str]]:
    """Replicates the v10 hard-rule invariant checks."""
    notes: list[str] = []
    sys.path.insert(0, str(ROOT))
    try:
        from auto_client_acquisition.finance_os import is_live_charge_allowed  # type: ignore
        if is_live_charge_allowed().get("allowed") is not False:
            notes.append("is_live_charge_allowed() != False")
    except Exception as exc:  # noqa: BLE001
        notes.append(f"finance_os import: {exc}")

    try:
        from auto_client_acquisition.agent_governance import (  # type: ignore
            FORBIDDEN_TOOLS, ToolCategory,
        )
        for needed in (ToolCategory.SEND_WHATSAPP_LIVE, ToolCategory.LINKEDIN_AUTOMATION, ToolCategory.SCRAPE_WEB):
            if needed not in FORBIDDEN_TOOLS:
                notes.append(f"{needed} not in FORBIDDEN_TOOLS")
    except Exception as exc:  # noqa: BLE001
        notes.append(f"agent_governance import: {exc}")

    try:
        import yaml  # type: ignore
        claim = yaml.safe_load((ROOT / "dealix" / "config" / "claim_policy.yaml").read_text(encoding="utf-8"))
        if claim["rules"]["roi_or_guarantee"]["allowed"] is not False:
            notes.append("claim_policy.roi_or_guarantee.allowed != False")
    except Exception as exc:  # noqa: BLE001
        notes.append(f"claim_policy read: {exc}")

    return (not notes), notes


def main() -> int:
    p = argparse.ArgumentParser(description="Dealix Company OS master verifier.")
    p.add_argument("--strict", action="store_true", help="Treat warnings as failures in sub-verifiers.")
    p.add_argument("--include-existing", action="store_true", help="Also run existing verifiers (informational).")
    p.add_argument("--json", action="store_true", help="Emit JSON summary at the end.")
    args = p.parse_args()

    print("═══════════════════════════════════════════════════════════════")
    print(" Dealix Company OS — verify_everything")
    print(f" Date: {datetime.now(timezone.utc).strftime('%Y-%m-%dT%H:%M:%SZ')}")
    print("═══════════════════════════════════════════════════════════════")

    results: list[dict[str, object]] = []

    print("\n 1. Company OS layers (new)")
    print("───────────────────────────────────────────────────────────────")
    for label, script in NEW_VERIFIERS:
        rc, head = _run(script, strict=args.strict)
        icon = "✅" if rc == 0 else ("❌" if rc == 1 else "⚠️ ")
        print(f"  {icon}  {label:<28} {head}")
        results.append({"layer": label, "script": script, "code": rc, "head": head})

    if args.include_existing:
        print("\n 2. Existing verifiers (informational)")
        print("───────────────────────────────────────────────────────────────")
        for label, script in EXISTING_VERIFIERS:
            rc, head = _run(script, strict=False)
            icon = "✅" if rc == 0 else ("❌" if rc == 1 else "⚠️ ")
            print(f"  {icon}  {label:<28} {head}")
            results.append({"layer": label, "script": script, "code": rc, "head": head, "informational": True})

    print("\n 3. Hard-rule invariants")
    print("───────────────────────────────────────────────────────────────")
    ok, notes = _hard_rule_invariants()
    if ok:
        print("  ✅  is_live_charge_allowed                    False")
        print("  ✅  SEND_WHATSAPP_LIVE in FORBIDDEN_TOOLS")
        print("  ✅  LINKEDIN_AUTOMATION in FORBIDDEN_TOOLS")
        print("  ✅  SCRAPE_WEB in FORBIDDEN_TOOLS")
        print("  ✅  claim_policy.roi_or_guarantee.allowed     False")
    else:
        for n in notes:
            print(f"  ❌  {n}")

    fails = sum(1 for r in results if r["code"] == 1 and not r.get("informational"))
    warns = sum(1 for r in results if r["code"] == 2 and not r.get("informational"))
    if not ok:
        fails += 1
    verdict = "PASS" if fails == 0 else "FAIL"

    print("\n═══════════════════════════════════════════════════════════════")
    print(" Verdict")
    print("═══════════════════════════════════════════════════════════════")
    print(f"DEALIX_EVERYTHING={verdict.lower()}")
    print(f"FAILED_LAYERS={fails}")
    print(f"WARNED_LAYERS={warns}")
    print(f"TOTAL_LAYERS={len(NEW_VERIFIERS)}")
    print(f"INVARIANTS_OK={'true' if ok else 'false'}")
    print(f"COMMIT={os.environ.get('GITHUB_SHA', 'local')}")

    if args.json:
        print("\n## JSON")
        print(json.dumps(
            {
                "verdict": verdict,
                "results": results,
                "invariants_ok": ok,
                "invariant_notes": notes,
                "ts": datetime.now(timezone.utc).isoformat(),
            },
            ensure_ascii=False,
            indent=2,
        ))

    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
