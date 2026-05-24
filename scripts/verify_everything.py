"""Master verifier: the Dealix Production Certification gate.

Runs every layer and rolls up a single PASS / FAIL / WARN result.
Used by:
    make production-certification
    .github/workflows/dealix-production-certification.yml
"""
from __future__ import annotations

import importlib.util
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_cert_common import (  # noqa: E402
    VerifierReport,
    print_report,
)

# Order matters: run static gates first so the live-send-safety marker
# is written before verify_production_env reads it.
VERIFIERS = [
    ("verify_policy_as_code", "Policy-as-Code"),
    ("verify_agent_registry", "Agent Registry"),
    ("verify_machine_registry", "Machine Registry"),
    ("verify_eval_gate", "Eval Gate"),
    ("verify_prompt_output_quality", "Prompt / Output Safety"),
    ("verify_live_send_safety", "Live Send Safety"),
    ("verify_railway_readiness", "Railway Readiness"),
    ("verify_production_env", "Production Env"),
    ("verify_ai_company_os", "AI Company OS"),
]


def _import(module_name: str):
    here = Path(__file__).resolve().parent
    path = here / f"{module_name}.py"
    spec = importlib.util.spec_from_file_location(module_name, path)
    if spec is None or spec.loader is None:
        raise ImportError(module_name)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def main() -> int:
    overall = VerifierReport(verifier="Dealix Everything Verification")
    details: list[tuple[str, VerifierReport]] = []
    for mod_name, label in VERIFIERS:
        try:
            mod = _import(mod_name)
            report: VerifierReport = mod.run()
        except Exception as exc:  # pragma: no cover - defensive
            overall.fail(label, f"verifier crashed: {exc.__class__.__name__}: {exc}",
                         hint=f"run: python scripts/{mod_name}.py")
            continue
        details.append((label, report))
        if report.overall == "PASS":
            overall.pass_(label, f"{len(report.results)} checks")
        elif report.overall == "WARN":
            overall.warn(label, f"{sum(1 for r in report.results if r.status == 'WARN')} warnings")
        else:
            fails = [r for r in report.results if r.status == "FAIL"]
            overall.fail(label, f"{len(fails)} failures",
                         hint=f"run: python scripts/{mod_name}.py")

    # full detail dump for CI logs
    print("\n############################################")
    print("# DEALIX PRODUCTION CERTIFICATION — DETAILS")
    print("############################################")
    for _, rep in details:
        print_report(rep)

    print("\n############################################")
    print("# DEALIX PRODUCTION CERTIFICATION — ROLLUP")
    print("############################################")
    print_report(overall)

    if overall.overall == "PASS":
        print("\nRESULT: PRODUCTION-GATED READY")
    elif overall.overall == "WARN":
        print("\nRESULT: PRODUCTION-GATED READY (with warnings)")
    else:
        print("\nRESULT: NOT READY — fix the failures above before deploy")

    # honor STRICT=1 → treat WARN as failure (used by CI)
    strict = os.environ.get("DEALIX_CERT_STRICT", "").lower() in {"1", "true", "yes"}
    if strict and overall.overall != "PASS":
        return 1
    return overall.exit_code()


if __name__ == "__main__":
    raise SystemExit(main())
