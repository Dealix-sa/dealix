from __future__ import annotations

from types import SimpleNamespace

from fastapi import FastAPI
from fastapi.testclient import TestClient

from api.routers.full_ops import router
from api.security.auth_deps import get_current_user
from auto_client_acquisition.full_ops import get_default_queue


def _client(tenant_id: str = "dealix") -> TestClient:
    app = FastAPI()
    app.include_router(router)

    async def _current_user():
        return SimpleNamespace(tenant_id=tenant_id)

    app.dependency_overrides[get_current_user] = _current_user
    return TestClient(app)


def _unauthenticated_client() -> TestClient:
    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_capability_map_and_plan_endpoint_have_no_side_effect() -> None:
    queue = get_default_queue()
    queue.clear()
    client = _client("tenant_plan")
    capability_response = client.get("/api/v1/full-ops/capability-map")
    assert capability_response.status_code == 200
    assert capability_response.json()["count"] == 16

    response = client.post(
        "/api/v1/full-ops/route-workload",
        json={
            "customer_id": "customer_001",
            "title": "حل عبء خدمة العملاء",
            "description": "فرز التذاكر وكتابة الردود وقياس SLA",
            "evidence_ids": ["ev_001"],
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "plan_only"
    assert body["external_side_effect"] is False
    assert body["route"]["primary_domain"] == "customer_support"
    assert queue.list_all(tenant_id="tenant_plan") == []


def test_enqueue_endpoint_only_mutates_internal_tenant_queue() -> None:
    queue = get_default_queue()
    queue.clear()
    client = _client("tenant_queue")
    payload = {
        "customer_id": "customer_002",
        "title": "أتمتة عمليات التقارير الداخلية",
        "description": "تقليل العمل اليدوي وتجهيز تقرير أسبوعي",
        "evidence_ids": ["ev_002"],
    }
    first = client.post("/api/v1/full-ops/workloads", json=payload)
    second = client.post("/api/v1/full-ops/workloads", json=payload)
    assert first.status_code == 200
    assert second.status_code == 200
    assert first.json()["external_side_effect"] is False
    assert second.json()["tenant_queue_depth"] == 1
    assert len(queue.list_all(tenant_id="tenant_queue")) == 1
    queue.clear()


def test_enqueue_preserves_blocked_external_action() -> None:
    queue = get_default_queue()
    queue.clear()
    client = _client("tenant_safe")
    response = client.post(
        "/api/v1/full-ops/workloads",
        json={
            "customer_id": "customer_003",
            "title": "إرسال رسائل للعملاء",
            "description": "حملة مبيعات",
            "external_action_requested": True,
            "requested_channel": "whatsapp",
            "recipient_opted_in": False,
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["work_item"]["status"] == "blocked"
    assert body["work_item"]["action_mode"] == "blocked"
    assert "whatsapp_opt_in_not_proven" in body["work_item"]["risk_flags"]
    queue.clear()


def test_daily_command_center_is_tenant_scoped() -> None:
    queue = get_default_queue()
    queue.clear()
    base = {
        "customer_id": "customer_004",
        "title": "حملة نمو داخلية",
        "description": "تحليل funnel وإعداد تجارب conversion",
        "evidence_ids": ["ev_004"],
    }
    tenant_one = _client("tenant_one")
    tenant_two = _client("tenant_two")
    tenant_one.post("/api/v1/full-ops/workloads", json=base)
    tenant_two.post("/api/v1/full-ops/workloads", json=base)

    one = tenant_one.get("/api/v1/full-ops/daily-command-center")
    two = tenant_two.get("/api/v1/full-ops/daily-command-center")
    assert one.status_code == 200
    assert two.status_code == 200
    assert one.json()["tenant_id"] == "tenant_one"
    assert one.json()["executive_summary"]["total_items"] == 1
    assert two.json()["executive_summary"]["total_items"] == 1
    assert one.json()["revenue_truth"]["status"] == "not_configured"
    queue.clear()


def test_workload_and_command_center_endpoints_require_authentication() -> None:
    client = _unauthenticated_client()
    payload = {
        "title": "خطة تشغيل داخلية",
        "description": "تخطيط عبء بدون أثر خارجي",
    }
    assert client.post("/api/v1/full-ops/route-workload", json=payload).status_code == 401
    assert client.post("/api/v1/full-ops/workloads", json=payload).status_code == 401
    assert client.get("/api/v1/full-ops/daily-command-center").status_code == 401
