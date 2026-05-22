"""Tests for /api/v1/diagnostic/* endpoints."""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import create_app


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(create_app())


def test_diagnostic_status(client: TestClient):
    resp = client.get("/api/v1/diagnostic/status")
    assert resp.status_code == 200
    body = resp.json()
    assert body["module"] == "diagnostic_engine"
    assert body["n_sectors"] >= 5
    g = body["guardrails"]
    assert g["no_llm_calls"] is True
    assert g["no_live_sends"] is True
    assert g["approval_required_on_every_brief"] is True


def test_diagnostic_sectors_list(client: TestClient):
    resp = client.get("/api/v1/diagnostic/sectors")
    assert resp.status_code == 200
    body = resp.json()
    assert "sectors" in body
    assert len(body["sectors"]) >= 5
    assert "b2b_services" in body["sectors"]


def test_diagnostic_generate_valid_payload(client: TestClient):
    resp = client.post(
        "/api/v1/diagnostic/generate",
        json={
            "company": "ACME Saudi Co.",
            "sector": "b2b_services",
            "region": "riyadh",
            "pipeline_state": "WhatsApp incoming, founder responds at night",
        },
    )
    assert resp.status_code == 200
    body = resp.json()
    assert body["company"] == "ACME Saudi Co."
    assert body["recommended_bundle"] == "growth_starter"
    assert body["approval_status"] == "approval_required"
    assert body["markdown_ar_en"]
    assert body["safety_notes"]


def test_diagnostic_generate_empty_company_returns_422(client: TestClient):
    resp = client.post(
        "/api/v1/diagnostic/generate",
        json={"company": "", "sector": "b2b_services"},
    )
    assert resp.status_code == 422


def test_diagnostic_generate_extra_field_returns_422(client: TestClient):
    """DiagnosticRequest sets extra='forbid'; rogue fields must 422."""
    resp = client.post(
        "/api/v1/diagnostic/generate",
        json={
            "company": "ACME",
            "sector": "b2b_services",
            "rogue_field": "should_be_rejected",
        },
    )
    assert resp.status_code == 422


def test_diagnostic_report_markdown_is_bilingual_and_approval_tagged(
    client: TestClient,
):
    resp = client.post(
        "/api/v1/diagnostic/report/markdown",
        json={
            "company": "Acme Saudi Co.",
            "sector": "b2b_services",
            "region": "riyadh",
            "pipeline_state": "founder responds at night",
        },
    )
    assert resp.status_code == 200
    text = resp.text
    assert "Acme Saudi Co." in text
    assert "approval_required" in text
    assert "Recommended bundle" in text
    assert "النتائج التقديرية ليست نتائج مضمونة" in text


def test_diagnostic_report_pdf_or_markdown_fallback(client: TestClient):
    resp = client.post(
        "/api/v1/diagnostic/report/pdf",
        json={"company": "Acme Saudi Co.", "sector": "b2b_services"},
    )
    assert resp.status_code == 200
    if "application/pdf" in resp.headers.get("content-type", ""):
        assert resp.content[:5] == b"%PDF-"
    else:
        assert resp.headers.get("X-PDF-Renderer", "").startswith("unavailable")
        assert "Acme Saudi Co." in resp.text


def test_diagnostic_report_html_is_arabic_first(client: TestClient):
    resp = client.post(
        "/api/v1/diagnostic/report/html",
        json={
            "request": {
                "company": "Acme Saudi Co.",
                "sector": "b2b_services",
                "region": "riyadh",
            }
        },
    )
    assert resp.status_code == 200
    assert "text/html" in resp.headers.get("content-type", "")
    body = resp.text
    assert body.startswith("<!doctype html>")
    assert "dir='rtl'" in body
    assert "Acme Saudi Co." in body
    assert "النتائج التقديرية ليست نتائج مضمونة" in body
    # No audit reference when no commitment id is supplied.
    assert "مرجع التدقيق" not in body


def test_diagnostic_report_html_embeds_audit_link(
    client: TestClient, tmp_path, monkeypatch
):
    monkeypatch.setenv(
        "DEALIX_CAPITAL_LEDGER_PATH", str(tmp_path / "cap.jsonl")
    )
    resp = client.post(
        "/api/v1/diagnostic/report/html",
        json={
            "request": {"company": "Acme Saudi Co.", "sector": "b2b_services"},
            "customer_id": "c1",
            "engagement_id": "e1",
            "written_commitment_id": "commit_42",
        },
    )
    assert resp.status_code == 200
    assert "commit_42" in resp.text
    assert "مرجع التدقيق" in resp.text


def test_diagnostic_report_html_rejects_flat_payload(client: TestClient):
    """The frontend used to send a flat payload (company_handle, sector, ...)
    directly instead of the nested {request: {...}} shape. Confirm that
    extra='forbid' rejects it with 422 so the bug can't regress silently."""
    resp = client.post(
        "/api/v1/diagnostic/report/html",
        json={
            "company_handle": "Acme KSA",
            "sector": "b2b_services",
            "biggest_problem": "no follow-up",
            "offer": "7_day_proof_sprint",
        },
    )
    assert resp.status_code == 422


def test_diagnostic_report_html_pipeline_state_in_output(client: TestClient):
    """pipeline_state (mapped from biggest_problem in the frontend) should
    influence the diagnostic context in the rendered HTML."""
    resp = client.post(
        "/api/v1/diagnostic/report/html",
        json={
            "request": {
                "company": "Pipeline Test Co.",
                "sector": "consulting",
                "region": "ksa",
                "pipeline_state": "no CRM, leads in WhatsApp only",
            }
        },
    )
    assert resp.status_code == 200
    body = resp.text
    assert "Pipeline Test Co." in body
    assert "dir='rtl'" in body
