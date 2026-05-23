"""Tests for the Market Attack & Scaling internal endpoints.

Covers all five admin-gated read-only endpoints exposed by
`api/routers/market_attack_internal.py`. The router reads from the
in-repo bootstrap CSVs as a fallback when `$PRIVATE_OPS` is not set,
so these tests run deterministically in CI without any external state.
"""
from __future__ import annotations

import pytest
from fastapi.testclient import TestClient

from api.main import create_app


ADMIN_KEY = "test_admin_market_attack"

ENDPOINTS = (
    "/api/v1/internal/market-attack/summary",
    "/api/v1/internal/campaigns/summary",
    "/api/v1/internal/partners/pipeline",
    "/api/v1/internal/sales-assets/summary",
    "/api/v1/internal/authority/queue",
)


@pytest.fixture(scope="module")
def client() -> TestClient:
    return TestClient(create_app())


@pytest.fixture(autouse=True)
def _set_admin_key(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setenv("ADMIN_API_KEYS", ADMIN_KEY)
    # Force the router to use the bootstrap fallback (no live private ops).
    monkeypatch.delenv("PRIVATE_OPS", raising=False)


def _auth_headers() -> dict[str, str]:
    return {"X-Admin-API-Key": ADMIN_KEY}


@pytest.mark.parametrize("path", ENDPOINTS)
def test_endpoints_require_admin_key(client: TestClient, path: str) -> None:
    resp = client.get(path)
    # Without ADMIN_API_KEYS configured this would 200; with a key set it
    # must reject anonymous callers.
    assert resp.status_code in (401, 403)


def test_market_attack_summary_shape(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/internal/market-attack/summary", headers=_auth_headers()
    )
    assert resp.status_code == 200
    body = resp.json()
    for key in (
        "source",
        "generatedAt",
        "beachhead",
        "p0Count",
        "p1Count",
        "openObjections",
        "highFrequencyObjections",
        "activeT0AndT1Accounts",
    ):
        assert key in body, f"missing key: {key}"
    assert body["source"] in ("api", "fallback")
    # The seeded fallback has at least one P0 sector (construction, score 38).
    assert body["p0Count"] >= 1
    assert body["beachhead"] is not None
    assert body["beachhead"]["priority"] == "P0"


def test_campaigns_summary_shape(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/internal/campaigns/summary", headers=_auth_headers()
    )
    assert resp.status_code == 200
    body = resp.json()
    for key in (
        "source",
        "generatedAt",
        "campaignsByStatus",
        "queueByStatus",
        "assetsPendingApproval",
        "results",
    ):
        assert key in body, f"missing key: {key}"
    assert isinstance(body["campaignsByStatus"], dict)
    assert isinstance(body["queueByStatus"], dict)
    for k in (
        "impressions",
        "clicks",
        "replies",
        "positiveReplies",
        "samples",
        "proposals",
        "payments",
    ):
        assert k in body["results"]
        assert isinstance(body["results"][k], int)


def test_partners_pipeline_shape(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/internal/partners/pipeline", headers=_auth_headers()
    )
    assert resp.status_code == 200
    body = resp.json()
    for key in (
        "source",
        "generatedAt",
        "byType",
        "byStatus",
        "highReferralPartners",
        "whiteLabelCandidates",
    ):
        assert key in body
    # Bootstrap seed contains agency / erp_crm / cybersecurity_grc.
    assert "agency" in body["byType"]
    assert "erp_crm" in body["byType"]


def test_sales_assets_summary_shape(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/internal/sales-assets/summary", headers=_auth_headers()
    )
    assert resp.status_code == 200
    body = resp.json()
    for key in (
        "source",
        "generatedAt",
        "total",
        "byType",
        "byApprovalStatus",
        "championAssets",
    ):
        assert key in body
    assert body["total"] >= 1
    assert body["championAssets"] >= 0
    # Bootstrap seed has at least the one_pager + proposal types.
    assert "one_pager" in body["byType"]


def test_authority_queue_shape(client: TestClient) -> None:
    resp = client.get(
        "/api/v1/internal/authority/queue", headers=_auth_headers()
    )
    assert resp.status_code == 200
    body = resp.json()
    for key in (
        "source",
        "generatedAt",
        "postsPending",
        "postsApproved",
        "insightsValidated",
        "reportIdeas",
    ):
        assert key in body
    assert body["postsPending"] + body["postsApproved"] >= 0
    assert body["reportIdeas"] >= 0


def test_no_endpoint_returns_5xx(client: TestClient) -> None:
    """The router must never crash on missing inputs; the fallback path
    is the contract."""
    for path in ENDPOINTS:
        resp = client.get(path, headers=_auth_headers())
        assert resp.status_code < 500, (
            f"{path} returned {resp.status_code}: {resp.text[:200]}"
        )


def test_runtime_path_marks_source_api(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    """When PRIVATE_OPS points at a real ops tree with all CSVs, the
    response is marked `source=api` (not fallback)."""
    # Seed every CSV the router reads, with a minimal valid row.
    (tmp_path / "market_attack").mkdir()
    (tmp_path / "campaigns").mkdir()
    (tmp_path / "partners").mkdir()
    (tmp_path / "sales_assets").mkdir()
    (tmp_path / "authority").mkdir()

    (tmp_path / "market_attack" / "beachhead_sector_scorecard.csv").write_text(
        "sector,saudi_relevance,buyer_clarity,pain_urgency,high_ticket_potential,"
        "proof_fit,delivery_fit,competition_gap,channel_access,trust_risk,"
        "total_score,priority,next_action\n"
        "live_sector,5,5,5,5,5,5,5,5,5,45,P0,run\n",
        encoding="utf-8",
    )
    (tmp_path / "market_attack" / "strategic_accounts.csv").write_text(
        "account_id,company,sector,website,city,buyer_title,why_strategic,"
        "trigger_event,estimated_value,relationship_path,proof_needed,"
        "trust_risk,priority,next_action,status\n"
        "acct-x,Co,live_sector,,Riyadh,COO,why,trig,1,path,proof,low,T0,act,new\n",
        encoding="utf-8",
    )
    (tmp_path / "market_attack" / "objection_library.csv").write_text(
        "objection_id,sector,stage,objection,frequency,response_angle,"
        "asset_needed,owner,status,next_action\n"
        "obj-x,live_sector,cold,obj,5,resp,one_pager,founder,open,act\n",
        encoding="utf-8",
    )
    (tmp_path / "campaigns" / "campaign_registry.csv").write_text(
        "campaign_id,name,sector,offer,channel,goal,approval_class,owner,"
        "status,start_date,end_date,next_action\n"
        "c1,n,live_sector,o,ch,goal,founder_only,founder,live,,,act\n",
        encoding="utf-8",
    )
    (tmp_path / "campaigns" / "campaign_queue.csv").write_text(
        "queue_id,campaign_id,channel,target_segment,message_or_asset,"
        "approval_status,send_status,next_action\n"
        "q1,c1,ch,seg,a1,approved,approved,act\n",
        encoding="utf-8",
    )
    (tmp_path / "campaigns" / "campaign_assets.csv").write_text(
        "asset_id,campaign_id,type,title,status,approval_status,proof_status,"
        "risk_level,next_action\n"
        "a1,c1,one_pager,title,draft,approved,n_a,low,act\n",
        encoding="utf-8",
    )
    (tmp_path / "campaigns" / "campaign_results.csv").write_text(
        "date,campaign_id,channel,impressions,clicks,replies,positive_replies,"
        "samples,proposals,payments,learning,next_action\n"
        "2026-01-01,c1,ch,10,5,2,1,1,1,1,learn,act\n",
        encoding="utf-8",
    )
    (tmp_path / "partners" / "partner_pipeline.csv").write_text(
        "partner_id,company,type,website,relationship_path,offer_fit,"
        "referral_potential,white_label_potential,trust_risk,status,next_action\n"
        "p1,Co,agency,,path,fit,high,yes,low,active,act\n",
        encoding="utf-8",
    )
    (tmp_path / "sales_assets" / "sales_asset_registry.csv").write_text(
        "asset_id,type,sector,offer,title,status,approval_status,proof_status,"
        "risk_level,file_path,next_action\n"
        "sa-x,one_pager,live_sector,o,title,champion,approved,evidence_attached,"
        "low,path/x.md,act\n",
        encoding="utf-8",
    )
    (tmp_path / "authority" / "founder_posts.csv").write_text(
        "post_id,theme,sector,draft,approval_status,proof_status,risk_level,next_action\n"
        "post-x,theme,live_sector,draft,approved,evidence_attached,low,act\n",
        encoding="utf-8",
    )
    (tmp_path / "authority" / "sector_insights.csv").write_text(
        "insight_id,sector,insight,evidence,source,status,approved_for_public,next_action\n"
        "ins-x,live_sector,insight,ev,internal_ledger,validated,yes,act\n",
        encoding="utf-8",
    )
    (tmp_path / "authority" / "report_ideas.csv").write_text(
        "report_id,sector,title,hypothesis,data_needed,approval_status,next_action\n"
        "rep-x,live_sector,title,hyp,data,pending,act\n",
        encoding="utf-8",
    )

    monkeypatch.setenv("PRIVATE_OPS", str(tmp_path))

    for path in ENDPOINTS:
        resp = client.get(path, headers=_auth_headers())
        assert resp.status_code == 200, f"{path}: {resp.text[:200]}"
        assert resp.json()["source"] == "api", (
            f"{path} should report source=api when PRIVATE_OPS is populated"
        )

    # Verify the champion asset count is picked up from runtime data.
    sa = client.get(
        "/api/v1/internal/sales-assets/summary", headers=_auth_headers()
    ).json()
    assert sa["championAssets"] == 1

    # Verify high-frequency objection count is picked up.
    ma = client.get(
        "/api/v1/internal/market-attack/summary", headers=_auth_headers()
    ).json()
    assert ma["highFrequencyObjections"] == 1
    assert ma["activeT0AndT1Accounts"] == 1


def test_safe_int_handles_non_numeric_payload(
    client: TestClient, monkeypatch: pytest.MonkeyPatch, tmp_path
) -> None:
    """A non-numeric value in campaign_results.csv must not crash the
    endpoint — `_safe_int` falls back to 0."""
    (tmp_path / "campaigns").mkdir()
    (tmp_path / "campaigns" / "campaign_results.csv").write_text(
        "date,campaign_id,channel,impressions,clicks,replies,positive_replies,"
        "samples,proposals,payments,learning,next_action\n"
        "2026-01-01,c1,ch,not_a_number,,,,,,,,\n",
        encoding="utf-8",
    )
    monkeypatch.setenv("PRIVATE_OPS", str(tmp_path))
    resp = client.get(
        "/api/v1/internal/campaigns/summary", headers=_auth_headers()
    )
    assert resp.status_code == 200
    assert resp.json()["results"]["impressions"] == 0
