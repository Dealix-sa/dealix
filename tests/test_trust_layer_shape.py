"""Trust-layer payload shape validation — /version and /api/v1/meta."""

from __future__ import annotations

import json

from dealix.commercial_ops import railway_production as rp


def _probe(body: object, *, ok: bool = True, status: int = 200) -> dict:
    return {
        "probed": True,
        "url": "https://api.dealix.me/x",
        "status": status,
        "ok": ok,
        "snippet": body if isinstance(body, str) else json.dumps(body),
    }


# ── validate_version_payload ─────────────────────────────────────────────


def test_version_payload_valid_when_all_fields_present() -> None:
    body = {"service": "dealix-api", "status": "ok", "version": "3.0.0", "git_sha": "abc123"}
    result = rp.validate_version_payload(_probe(body))
    assert result["valid"] is True
    assert result["missing"] == []


def test_version_payload_invalid_when_not_json() -> None:
    result = rp.validate_version_payload(_probe("<html>nginx</html>"))
    assert result["valid"] is False
    assert result["reason"] == "not_json"


def test_version_payload_invalid_when_object_root_is_list() -> None:
    result = rp.validate_version_payload(_probe([1, 2, 3]))
    assert result["valid"] is False
    assert result["reason"] == "not_object"


def test_version_payload_reports_each_missing_field() -> None:
    body = {"service": "dealix-api", "status": "ok"}  # missing version + git_sha
    result = rp.validate_version_payload(_probe(body))
    assert result["valid"] is False
    assert result["reason"] == "missing_fields"
    assert set(result["missing"]) == {"version", "git_sha"}


def test_version_payload_invalid_when_status_not_ok() -> None:
    body = {"service": "dealix-api", "status": "degraded", "version": "3.0.0", "git_sha": "abc"}
    result = rp.validate_version_payload(_probe(body))
    assert result["valid"] is False
    assert result["reason"] == "status_not_ok"


def test_version_payload_invalid_when_probe_not_ok() -> None:
    result = rp.validate_version_payload(_probe({}, ok=False, status=502))
    assert result["valid"] is False
    assert result["reason"] == "probe_not_ok"


# ── validate_meta_payload ────────────────────────────────────────────────


def test_meta_payload_valid_when_surfaces_populated() -> None:
    body = {
        "service": "Dealix",
        "version": "3.0.0",
        "surfaces": {"frontend": ["/ar"]},
        "canonical_links": {"healthz": "/healthz"},
    }
    result = rp.validate_meta_payload(_probe(body))
    assert result["valid"] is True


def test_meta_payload_invalid_when_surfaces_empty_dict() -> None:
    body = {
        "service": "Dealix",
        "version": "3.0.0",
        "surfaces": {},
        "canonical_links": {"healthz": "/healthz"},
    }
    result = rp.validate_meta_payload(_probe(body))
    assert result["valid"] is False
    assert result["reason"] == "empty_surfaces"


def test_meta_payload_invalid_when_canonical_links_missing() -> None:
    body = {"service": "Dealix", "version": "3.0.0", "surfaces": {"x": 1}}
    result = rp.validate_meta_payload(_probe(body))
    assert result["valid"] is False
    assert result["reason"] == "missing_fields"
    assert "canonical_links" in result["missing"]


def test_meta_payload_invalid_when_not_json() -> None:
    result = rp.validate_meta_payload(_probe("plain text"))
    assert result["valid"] is False
    assert result["reason"] == "not_json"


# ── probe_trust_layer integration ────────────────────────────────────────


def _ok_version_body(sha: str = "deadbee") -> dict:
    return {"service": "dealix-api", "status": "ok", "version": "3.0.0", "git_sha": sha}


def _ok_meta_body() -> dict:
    return {
        "service": "Dealix",
        "version": "3.0.0",
        "surfaces": {"frontend_public_routes": ["/ar"]},
        "canonical_links": {"healthz": "/healthz"},
    }


def _ok_healthz_body() -> dict:
    return {"status": "ok", "version": "3.0.0"}


def _fake_probe_get(routes: dict[str, dict]):
    """Return a probe_get replacement that serves canned bodies per path."""

    def _impl(api_base: str, path: str, **_kwargs) -> dict:
        if path not in routes:
            return {"probed": True, "ok": False, "status": 404, "url": api_base + path}
        body = routes[path]
        return _probe(body, ok=True, status=200) | {"url": api_base + path}

    return _impl


def test_probe_trust_layer_ok_when_all_payloads_valid(monkeypatch) -> None:
    monkeypatch.setattr(
        rp,
        "probe_get",
        _fake_probe_get(
            {
                "/healthz": _ok_healthz_body(),
                "/health": _ok_healthz_body(),
                "/version": _ok_version_body(),
                "/api/v1/meta": _ok_meta_body(),
            }
        ),
    )
    blob = rp.probe_trust_layer("https://api.dealix.me")
    assert blob["ok"] is True
    assert blob["version_payload"]["valid"] is True
    assert blob["meta_payload"]["valid"] is True
    assert blob["shape_drift_hint_ar"] == ""


def test_probe_trust_layer_flags_shape_drift_when_version_html(monkeypatch) -> None:
    """A misconfigured CDN that returns HTML on /version must produce a hint."""

    def _impl(api_base: str, path: str, **_kwargs):
        bodies = {
            "/healthz": json.dumps(_ok_healthz_body()),
            "/health": json.dumps(_ok_healthz_body()),
            "/version": "<html><body>nginx</body></html>",  # raw HTML
            "/api/v1/meta": json.dumps(_ok_meta_body()),
        }
        return {
            "probed": True,
            "ok": True,
            "status": 200,
            "url": api_base + path,
            "snippet": bodies.get(path, ""),
        }

    monkeypatch.setattr(rp, "probe_get", _impl)
    blob = rp.probe_trust_layer("https://api.dealix.me")
    assert blob["version_payload"]["valid"] is False
    assert blob["version_payload"]["reason"] == "not_json"
    assert "/version" in blob["shape_drift_hint_ar"]
    assert blob["ok"] is False


def test_probe_trust_layer_flags_missing_git_sha_field(monkeypatch) -> None:
    """A regressed /version that drops git_sha must surface in the hint."""
    body_without_sha = {"service": "dealix-api", "status": "ok", "version": "3.0.0"}

    def _impl(api_base: str, path: str, **_kwargs):
        bodies = {
            "/healthz": json.dumps(_ok_healthz_body()),
            "/health": json.dumps(_ok_healthz_body()),
            "/version": json.dumps(body_without_sha),
            "/api/v1/meta": json.dumps(_ok_meta_body()),
        }
        return {
            "probed": True,
            "ok": True,
            "status": 200,
            "url": api_base + path,
            "snippet": bodies.get(path, ""),
        }

    monkeypatch.setattr(rp, "probe_get", _impl)
    blob = rp.probe_trust_layer("https://api.dealix.me")
    assert blob["version_payload"]["valid"] is False
    assert "git_sha" in blob["version_payload"]["missing"]
    assert "git_sha" in blob["shape_drift_hint_ar"]


def test_analyze_railway_production_warns_on_shape_drift(monkeypatch) -> None:
    """Repo OK but shape drift on /version should produce verdict WARN."""

    def _impl(api_base: str, path: str, **_kwargs):
        bodies = {
            "/healthz": json.dumps(_ok_healthz_body()),
            "/health": json.dumps(_ok_healthz_body()),
            "/version": "<html/>",  # bad shape
            "/api/v1/meta": json.dumps(_ok_meta_body()),
        }
        return {
            "probed": True,
            "ok": True,
            "status": 200,
            "url": api_base + path,
            "snippet": bodies.get(path, ""),
        }

    monkeypatch.setattr(rp, "probe_get", _impl)
    blob = rp.analyze_railway_production(api_base="https://api.dealix.me")
    assert blob["repo"]["ok"]
    assert blob["verdict"] == "WARN"
    assert blob["live_trust_layer"]["shape_drift_hint_ar"]
