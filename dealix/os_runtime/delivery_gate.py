"""
Delivery Gate
=============
Enforces delivery quality gates before each project phase.
No phase proceeds without passing its gate.
"""

GATES: dict[str, list[str]] = {
    "build": [
        "scope_document_signed",
        "acceptance_criteria_defined",
        "sample_data_approved",
    ],
    "integration": [
        "sandbox_access_confirmed",
        "api_intake_completed",
        "no_production_access_yet",
    ],
    "production_api": [
        "founder_approval_granted",
        "sandbox_tested",
        "security_checklist_passed",
        "client_approval_documented",
    ],
    "delivery": [
        "qa_checklist_passed",
        "acceptance_criteria_met",
        "demo_path_verified",
    ],
    "handover": [
        "documentation_complete",
        "handover_document_signed",
        "uat_signoff_received",
    ],
    "scope_change": [
        "change_request_submitted",
        "impact_assessed",
        "client_approved",
    ],
}


def check_gate(gate_name: str, checklist: dict[str, bool]) -> dict:
    """Verify all required items for a gate are checked."""
    required = GATES.get(gate_name)
    if required is None:
        return {"gate": gate_name, "passed": False, "error": f"Unknown gate: {gate_name}"}

    missing = [item for item in required if not checklist.get(item, False)]
    passed = len(missing) == 0

    return {
        "gate": gate_name,
        "passed": passed,
        "required": required,
        "missing": missing,
        "message": "Gate passed." if passed else f"Gate blocked — {len(missing)} item(s) incomplete.",
    }


def list_gates() -> list[str]:
    return list(GATES.keys())


def gate_requirements(gate_name: str) -> list[str]:
    return GATES.get(gate_name, [])
