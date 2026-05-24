"""Verify policies/dealix_control_policy.yaml is well-formed and intact.

Fails the build if any immutable rule has been removed or weakened.
Run via: make production-certification
"""
from __future__ import annotations

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _dealix_cert_common import (
    VerifierReport,
    load_yaml,
    main_cli,
    must_be_file,
    repo_path,
)

POLICY = "policies/dealix_control_policy.yaml"

REQUIRED_APPROVAL_CLASSES = {"A0", "A1", "A2", "A3"}
REQUIRED_RULE_IDS = {
    "no_a3_auto",
    "no_suppressed_outreach",
    "high_risk_requires_evidence",
    "no_guaranteed_revenue_claims",
    "pricing_commit_requires_approval",
    "public_proof_requires_approval",
    "approved_a2_can_request_execution",
    "a2_without_approval_escalates",
    "a3_always_escalates",
    "production_internal_api_requires_token",
    "no_secret_in_frontend",
    "no_frontend_direct_send",
}
IMMUTABLE = {
    "no_a3_auto",
    "no_suppressed_outreach",
    "no_guaranteed_revenue_claims",
    "a2_without_approval_escalates",
    "a3_always_escalates",
    "production_internal_api_requires_token",
    "no_secret_in_frontend",
    "no_frontend_direct_send",
}


def run() -> VerifierReport:
    r = VerifierReport(verifier="Policy-as-Code")
    if not must_be_file(r, "policy_file", POLICY,
                        hint="create policies/dealix_control_policy.yaml — see master prompt"):
        return r

    data = load_yaml(repo_path(POLICY))

    # approval classes
    classes = data.get("approval_classes") or {}
    missing_cls = REQUIRED_APPROVAL_CLASSES - set(classes.keys())
    if missing_cls:
        r.fail("approval_classes", f"missing: {sorted(missing_cls)}",
               hint="A0/A1/A2/A3 must all be declared")
    else:
        r.pass_("approval_classes", "A0/A1/A2/A3 present")

    # A3 must require approval + escalation, never auto-external
    a3 = classes.get("A3") or {}
    if a3.get("external_action_allowed", True) is True:
        r.fail("A3_external_blocked", "A3.external_action_allowed must be false")
    elif not a3.get("approval_required", False):
        r.fail("A3_requires_approval", "A3.approval_required must be true")
    elif not a3.get("escalate", False):
        r.fail("A3_escalates", "A3.escalate must be true")
    else:
        r.pass_("A3_hardened", "A3 never auto, always escalates")

    # rules
    rules = data.get("rules") or []
    rule_ids = {x.get("id") for x in rules if isinstance(x, dict)}
    missing = REQUIRED_RULE_IDS - rule_ids
    if missing:
        r.fail("rules_present", f"missing rule ids: {sorted(missing)}")
    else:
        r.pass_("rules_present", f"{len(rule_ids)} rules")

    # immutable rules
    immut = set(data.get("immutable_rules") or [])
    missing_immut = IMMUTABLE - immut
    if missing_immut:
        r.fail("immutable_rules", f"missing immutable rule ids: {sorted(missing_immut)}",
               hint="restore them to immutable_rules in the policy file")
    else:
        r.pass_("immutable_rules", f"{len(immut)} ids locked")

    # each immutable id must still appear in rules[]
    not_defined = IMMUTABLE - rule_ids
    if not_defined:
        r.fail("immutable_rules_defined", f"immutable but undefined: {sorted(not_defined)}")
    else:
        r.pass_("immutable_rules_defined", "all immutable rules have a rule body")

    return r


if __name__ == "__main__":
    raise SystemExit(main_cli(run, name="verify_policy_as_code"))
