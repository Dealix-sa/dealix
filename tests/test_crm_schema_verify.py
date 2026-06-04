"""CRM schema verifier passes: schema, stages, no send fields, seed leads."""

from __future__ import annotations

from tests._lc_util import REPO_ROOT, load_script


def test_crm_schema_verify_passes():
    mod = load_script("commercial_crm_schema_verify")
    result = mod.run()
    failed = [c for c in result["checks"] if c["critical"] and not c["passed"]]
    assert result["pass"] is True, f"critical failures: {failed}"


def test_no_send_fields_in_active_schema():
    mod = load_script("commercial_crm_schema_verify")
    result = mod.run()
    names = {c["name"]: c for c in result["checks"]}
    assert names["no_send_fields_in_active_schema"]["passed"] is True
    assert names["seed_leads_no_forbidden_fields"]["passed"] is True
