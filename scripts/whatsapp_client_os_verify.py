#!/usr/bin/env python3
"""WhatsApp Client OS — launch/verify gate.

Runs offline checks and prints ``DEALIX_WHATSAPP_CLIENT_OS_VERDICT=PASS|FAIL``.
Exercises the doctrine guardrails (secrets/unsafe blocked), the readiness scan,
the catalog-tied recommendation, the permission ladder, the JSON Schemas and a
full conversation flow. Run from repo root:

    python3 scripts/whatsapp_client_os_verify.py
"""

from __future__ import annotations

import json
import sys
import tempfile
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))


def _check(label: str, ok: bool, detail: str = "") -> tuple[str, bool, str]:
    return (label, bool(ok), detail)


def main() -> int:
    import os

    os.environ["DEALIX_WHATSAPP_OS_DIR"] = tempfile.mkdtemp()

    from auto_client_acquisition.service_catalog.registry import SERVICE_IDS
    from auto_client_acquisition.whatsapp_client_os import permission_levels as pl
    from auto_client_acquisition.whatsapp_client_os import templates
    from auto_client_acquisition.whatsapp_client_os.assessment import AXIS_ORDER, axis_spec
    from auto_client_acquisition.whatsapp_client_os.engine import handle_inbound, new_session
    from auto_client_acquisition.whatsapp_client_os.metrics import compute_metrics
    from auto_client_acquisition.whatsapp_client_os.whatsapp_policy_guard import (
        scan_for_secrets,
        scan_for_unsafe_request,
    )

    results: list[tuple[str, bool, str]] = []

    # 1) Doctrine — secrets blocked
    s = scan_for_secrets("api_key = sk-abcdefghijklmnopqrstuvwxyz12345")
    results.append(_check("secrets_in_chat_blocked", s.found, ",".join(s.kinds)))

    # 2) Doctrine — unsafe blocked
    u = scan_for_unsafe_request("أرسل واتساب بارد لكل الأرقام")
    results.append(_check("cold_whatsapp_blocked", u.blocked, ",".join(u.reasons)))

    # 3) Readiness scan — 10 axes
    results.append(_check("ten_axes", len(AXIS_ORDER) == 10, str(len(AXIS_ORDER))))

    # 4) Permission ladder — 6 levels, L5 cannot complete in WhatsApp
    results.append(_check("six_permission_levels", len(pl.all_specs()) == 6))
    results.append(_check("l5_needs_human", pl.escalate_needed("L5")))

    # 5) Templates render
    results.append(
        _check("templates_render", all(templates.get_template(k) for k in templates.TEMPLATE_KEYS))
    )

    # 6) JSON Schemas exist
    schema_dir = _REPO_ROOT / "dealix" / "contracts" / "schemas"
    schema_files = [
        "whatsapp_session.schema.json",
        "whatsapp_intake.schema.json",
        "whatsapp_action_card.schema.json",
        "client_permission.schema.json",
        "client_onboarding_assessment.schema.json",
    ]
    missing = [f for f in schema_files if not (schema_dir / f).exists()]
    results.append(_check("json_schemas_present", not missing, ",".join(missing)))

    # 7) Full flow → recommendation tied to catalog
    sess = new_session(client_handle="966500000000", company_name="تحقّق")
    r = handle_inbound(sess, button_id="menu:not_sure")
    sess = r.session
    for ax in AXIS_ORDER:
        opt = axis_spec(ax)["options"][0]["id"]
        r = handle_inbound(sess, button_id=f"asmt:{ax}:{opt}")
        sess = r.session
    rec_ok = (
        r.assessment is not None
        and r.assessment.recommended_offer in SERVICE_IDS
        and bool(r.cards and r.cards[0].catalog_ref)
    )
    results.append(
        _check(
            "recommendation_tied_to_catalog",
            rec_ok,
            r.assessment.recommended_offer if r.assessment else "",
        )
    )

    # 8) Secrets inbound never advances state + escalates
    before = sess.stage
    r2 = handle_inbound(sess, text="my key sk-abcdefghijklmnopqrstuvwxyz0000")
    results.append(
        _check(
            "secrets_inbound_safe",
            r2.blocked and r2.session.stage == before and r2.handoff is not None,
        )
    )

    # 9) Metrics compute
    m = compute_metrics()
    results.append(
        _check(
            "metrics_compute", "new_sessions" in m, json.dumps({"new_sessions": m["new_sessions"]})
        )
    )

    # Print summary
    all_ok = all(ok for _, ok, _ in results)
    print("== WhatsApp Client OS verify ==")
    for label, ok, detail in results:
        mark = "PASS" if ok else "FAIL"
        line = f"[{mark}] {label}"
        if detail:
            line += f"  ({detail})"
        print(line)
    verdict = "PASS" if all_ok else "FAIL"
    print(f"DEALIX_WHATSAPP_CLIENT_OS_VERDICT={verdict}")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
