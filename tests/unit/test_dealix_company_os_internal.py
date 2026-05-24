"""Tests for the Dealix Company OS Founder Console internal API.

Covers:
  - api.internal.policy_adapter — forbidden_claims, contains_forbidden_claim,
    audit_record, and the pyyaml-less fallback parser.
  - api.internal.runtime_reader — workspace_root, read_csv, read_markdown
    against a per-test temp workspace.
  - api.internal.auth — require_internal_key behavior.
  - api.routers.internal.founder_console — get_snapshot for each registered
    page slug, plus queue_for_approval happy path and forbidden-claim block.
"""
from __future__ import annotations

import csv
import os
from pathlib import Path
from typing import Iterator

import pytest
from fastapi import FastAPI, HTTPException
from fastapi.testclient import TestClient


# ── Workspace fixture ────────────────────────────────────────────────────────
@pytest.fixture()
def workspace(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Iterator[Path]:
    monkeypatch.setenv("DEALIX_PRIVATE_OPS", str(tmp_path))
    monkeypatch.setenv("DEALIX_INTERNAL_KEY", "test-key")
    yield tmp_path


# ── policy_adapter ───────────────────────────────────────────────────────────
def test_forbidden_claims_loaded_from_policy_yaml() -> None:
    from api.internal.policy_adapter import forbidden_claims

    claims = forbidden_claims()
    lowered = [c.lower() for c in claims]
    assert "guaranteed revenue" in lowered
    assert "guaranteed sales" in lowered
    assert "100% conversion" in lowered


@pytest.mark.parametrize(
    "text, expected_any",
    [
        ("we promise guaranteed revenue this quarter", True),
        ("we guaranteed sales for the pilot", True),
        ("we have 100% conversion on the new offer", True),
        ("we never make hard claims about outcomes", False),
        ("just a clean status update", False),
        ("", False),
    ],
)
def test_contains_forbidden_claim_finds_hits(text: str, expected_any: bool) -> None:
    from api.internal.policy_adapter import contains_forbidden_claim

    hits = contains_forbidden_claim(text)
    assert (len(hits) > 0) is expected_any


def test_audit_record_shape() -> None:
    from api.internal.policy_adapter import audit_record

    record = audit_record("founder", "act-1", "queue draft", "queued")
    assert set(record.keys()) >= {"actor", "action_id", "reason", "decision", "recorded_at"}
    assert record["actor"] == "founder"
    assert record["decision"] == "queued"
    assert "T" in record["recorded_at"]


def test_fallback_yaml_parser_extracts_forbidden_claims(tmp_path: Path) -> None:
    from api.internal import policy_adapter as pa

    sample = tmp_path / "policy.yaml"
    sample.write_text(
        'forbidden_claims:\n  - "guaranteed revenue"\n  - "guaranteed sales"\n',
        encoding="utf-8",
    )
    parsed = pa._fallback_parse(sample)
    assert parsed == {"forbidden_claims": ["guaranteed revenue", "guaranteed sales"]}


# ── runtime_reader ───────────────────────────────────────────────────────────
def test_workspace_root_reads_env(monkeypatch: pytest.MonkeyPatch, tmp_path: Path) -> None:
    from api.internal.runtime_reader import workspace_root

    monkeypatch.setenv("DEALIX_PRIVATE_OPS", str(tmp_path))
    assert workspace_root() == tmp_path


def test_read_csv_missing_file_returns_stub(workspace: Path) -> None:
    from api.internal.runtime_reader import read_csv

    payload = read_csv("does/not/exist.csv")
    assert payload["source"] == "missing_workspace_file"
    assert payload["data"]["rows"] == []


def test_read_csv_returns_rows_with_freshness(workspace: Path) -> None:
    from api.internal.runtime_reader import read_csv

    rel = "trust/trust_flags.csv"
    path = workspace / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as fh:
        writer = csv.writer(fh)
        writer.writerow(["flagged_at", "flag", "subject", "severity"])
        writer.writerow(["2026-05-24", "missing_evidence", "proof-9", "medium"])

    payload = read_csv(rel)
    assert payload["source"].endswith(rel)
    assert payload["data"]["rows"][0]["flag"] == "missing_evidence"
    assert payload["freshness_iso"]


def test_read_markdown_missing_file_returns_stub(workspace: Path) -> None:
    from api.internal.runtime_reader import read_markdown

    payload = read_markdown("missing.md")
    assert payload["source"] == "missing_workspace_file"
    assert payload["data"]["markdown"] == ""


def test_read_markdown_returns_text(workspace: Path) -> None:
    from api.internal.runtime_reader import read_markdown

    rel = "founder/ceo_daily_brief.md"
    path = workspace / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("# Brief\n", encoding="utf-8")
    payload = read_markdown(rel)
    assert "Brief" in payload["data"]["markdown"]


# ── auth ─────────────────────────────────────────────────────────────────────
def test_require_internal_key_raises_when_unconfigured(monkeypatch: pytest.MonkeyPatch) -> None:
    from api.internal.auth import require_internal_key

    monkeypatch.delenv("DEALIX_INTERNAL_KEY", raising=False)
    with pytest.raises(HTTPException) as exc:
        require_internal_key("anything")
    assert exc.value.status_code == 503


def test_require_internal_key_rejects_wrong_key(workspace: Path) -> None:
    from api.internal.auth import require_internal_key

    with pytest.raises(HTTPException) as exc:
        require_internal_key("not-the-key")
    assert exc.value.status_code == 401


def test_require_internal_key_accepts_match(workspace: Path) -> None:
    from api.internal.auth import require_internal_key

    assert require_internal_key("test-key") == "test-key"


# ── founder_console router ───────────────────────────────────────────────────
@pytest.fixture()
def client(workspace: Path) -> TestClient:
    from api.routers.internal.founder_console import router

    app = FastAPI()
    app.include_router(router)
    return TestClient(app)


def test_snapshot_unknown_slug_returns_404(client: TestClient) -> None:
    res = client.get(
        "/internal/founder-console/does-not-exist",
        headers={"x-internal-key": "test-key"},
    )
    assert res.status_code == 404


def test_snapshot_rejects_missing_key(client: TestClient) -> None:
    res = client.get("/internal/founder-console/ceo")
    assert res.status_code == 401


def test_snapshot_rejects_wrong_key(client: TestClient) -> None:
    res = client.get(
        "/internal/founder-console/ceo",
        headers={"x-internal-key": "wrong"},
    )
    assert res.status_code == 401


def test_every_registered_slug_returns_200(client: TestClient) -> None:
    from api.routers.internal.founder_console import PAGE_SOURCES

    assert PAGE_SOURCES, "PAGE_SOURCES must not be empty"
    for slug in PAGE_SOURCES:
        res = client.get(
            f"/internal/founder-console/{slug}",
            headers={"x-internal-key": "test-key"},
        )
        assert res.status_code == 200, f"slug {slug} returned {res.status_code}"
        body = res.json()
        assert body["source"] == "api / private_ops_csv"
        assert "freshness_iso" in body
        assert body["data"]["slug"] == slug


def test_queue_approval_rejects_forbidden_claim(client: TestClient) -> None:
    res = client.post(
        "/internal/founder-console/approvals/queue",
        headers={"x-internal-key": "test-key"},
        json={"action_id": "send-deck", "reason": "we will deliver guaranteed revenue"},
    )
    assert res.status_code == 400
    body = res.json()
    assert body["detail"]["error"] == "forbidden_claim"
    assert any("guaranteed" in m.lower() for m in body["detail"]["matches"])


def test_queue_approval_happy_path_writes_csv(client: TestClient, workspace: Path) -> None:
    res = client.post(
        "/internal/founder-console/approvals/queue",
        headers={"x-internal-key": "test-key"},
        json={
            "action_id": "draft-outreach",
            "reason": "queue ERP/CRM beachhead draft for founder review",
            "payload": {"sector": "erp_crm"},
        },
    )
    assert res.status_code == 200
    body = res.json()
    assert body["queued"] is True
    assert body["id"].startswith("apt-")
    assert body["audit"]["decision"] == "queued"

    queue_path = workspace / "approvals" / "approval_queue.csv"
    assert queue_path.exists()
    with queue_path.open("r", encoding="utf-8") as fh:
        rows = list(csv.DictReader(fh))
    assert len(rows) == 1
    row = rows[0]
    assert row["action_id"] == "draft-outreach"
    assert row["decision"] == "pending"
    assert row["external_action_allowed"] == "false"
