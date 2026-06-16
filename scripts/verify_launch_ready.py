#!/usr/bin/env python3
"""Dealix launch-readiness verifier — read-only.

Asserts that the "company starts now" spine is wired end-to-end:
  1. curated Saudi target frame present, parses, fully consent-gated
  2. commercial orchestrator generates company-level drafts (no live send)
  3. durable draft queue round-trips (enqueue → list → approve)
  4. founder approval routes are importable + mounted
  5. the 5 service tiers resolve
  6. doctrine: every generated draft carries the "not guaranteed" disclaimer

Exit 0 if every check passes, 1 otherwise. Safe to run anywhere — no network,
no external send, uses a temporary queue so it never touches real state.
"""
from __future__ import annotations

import os
import sys
import tempfile
from pathlib import Path

_REPO_ROOT = Path(__file__).resolve().parent.parent
if str(_REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(_REPO_ROOT))

_results: list[tuple[str, bool, str]] = []


def _check(name: str, fn) -> None:
    try:
        ok, detail = fn()
    except Exception as exc:  # pragma: no cover - defensive
        ok, detail = False, f"{type(exc).__name__}: {str(exc)[:160]}"
    _results.append((name, ok, detail))


def _c_dataset():
    from auto_client_acquisition.commercial_orchestrator import load_prospects
    rows = load_prospects()
    if not rows:
        return False, "dataset empty/missing"
    consented = all((r.get("consent_status") or "") == "required_before_contact" for r in rows)
    named = sum(1 for r in rows if (r.get("company_name") or "").strip())
    return (consented and named > 0,
            f"{named} named companies; all consent-gated={consented}")


def _c_orchestrator():
    # Use a throwaway queue so we never touch var/draft-queue.jsonl.
    tmp = Path(tempfile.gettempdir()) / "dealix_verify_q.jsonl"
    if tmp.exists():
        tmp.unlink()
    os.environ["DEALIX_DRAFT_QUEUE_PATH"] = str(tmp)
    import importlib
    from auto_client_acquisition.commercial_orchestrator import draft_queue, pipeline
    importlib.reload(draft_queue)
    importlib.reload(pipeline)
    res = pipeline.run_acquisition_to_drafts(min_band="warm")
    return res.generated > 0, f"{res.generated} drafts generated, {res.skipped} skipped"


def _c_queue_roundtrip():
    import importlib
    from auto_client_acquisition.commercial_orchestrator import draft_queue
    importlib.reload(draft_queue)
    rec = draft_queue.enqueue({"kind": "outreach", "company_name": "Verify Co",
                               "sector": "logistics", "body_md": "x"})
    did = rec["id"]
    draft_queue.set_status(did, "approved", who="verifier")
    cur = draft_queue.get(did)
    return cur is not None and cur["status"] == "approved", f"draft {did} → approved"


def _c_founder_routes():
    from api.routers import founder
    paths = {r.path for r in founder.router.routes}
    needed = {"/api/v1/founder/approvals",
              "/api/v1/founder/approvals/{draft_id}/approve",
              "/api/v1/founder/approvals/{draft_id}/reject"}
    missing = needed - paths
    return not missing, ("all approval routes mounted" if not missing else f"missing {missing}")


def _c_sprint_executor():
    tmp = Path(tempfile.gettempdir()) / "dealix_verify_sprint.jsonl"
    if tmp.exists():
        tmp.unlink()
    os.environ["DEALIX_SPRINT_STORE_PATH"] = str(tmp)
    import importlib
    from auto_client_acquisition.delivery_factory import sprint_executor, sprint_store
    importlib.reload(sprint_store)
    importlib.reload(sprint_executor)
    from dealix.commercial.sprint_orchestrator import SprintContext
    ctx = SprintContext(
        engagement_id="verify_eng", customer_id="verify", sector="logistics",
        sources=[{"source_type": "crm", "row_count": 50, "consent": "granted",
                  "has_source_passport": True}],
        rows=[{"company": "A", "email": "a@x.com", "amount": 1}],
        pain_summary="x", founder_approved=False,
    )
    sprint_executor.start_sprint(ctx)
    paused = sprint_executor.run_to_completion("verify_eng", auto_approve=False)
    if not paused or paused.get("status") != "awaiting_approval":
        return False, "Day-5 gate did not pause"
    done = sprint_executor.run_to_completion("verify_eng", auto_approve=True)
    ok = bool(done) and done.get("status") == "complete" and done.get("current_day") == 7
    return ok, "7-day sprint pauses at Day-5 gate, completes after approval"


def _c_service_tiers():
    from dealix.payments.payment_link import SERVICE_TIERS
    return len(SERVICE_TIERS) >= 5, f"{len(SERVICE_TIERS)} tiers: {list(SERVICE_TIERS)}"


def _c_doctrine_disclaimer():
    from auto_client_acquisition.commercial_orchestrator import (
        OutreachContext, render_outreach_draft,
    )
    body = render_outreach_draft(OutreachContext(company_name="X", sector="logistics"))["body_md"]
    ok = "not guaranteed" in body and "ليست نتائج مضمونة" in body
    return ok, "bilingual 'estimated ≠ guaranteed' disclaimer present"


def main() -> int:
    _check("target frame (consent-gated)", _c_dataset)
    _check("commercial orchestrator", _c_orchestrator)
    _check("draft queue round-trip", _c_queue_roundtrip)
    _check("founder approval routes", _c_founder_routes)
    _check("7-day sprint executor", _c_sprint_executor)
    _check("service tiers resolve", _c_service_tiers)
    _check("doctrine disclaimer", _c_doctrine_disclaimer)

    print("Dealix launch-readiness\n" + "=" * 48)
    all_ok = True
    for name, ok, detail in _results:
        mark = "PASS" if ok else "FAIL"
        all_ok = all_ok and ok
        print(f"[{mark}] {name:<32} {detail}")
    print("=" * 48)
    print("RESULT:", "READY ✅" if all_ok else "NOT READY ❌")
    return 0 if all_ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
