"""Deployed SHA comparison — local HEAD vs live /version git_sha."""

from __future__ import annotations

from dealix.commercial_ops import railway_production as rp


def _ok_version_probe(sha: str) -> dict:
    import json

    return {
        "probed": True,
        "url": "https://api.dealix.me/version",
        "status": 200,
        "ok": True,
        "snippet": json.dumps({"service": "dealix-api", "git_sha": sha, "version": "3.0.0"}),
    }


def test_extract_deployed_sha_from_ok_probe() -> None:
    assert rp.extract_deployed_sha(_ok_version_probe("abc1234def5678")) == "abc1234def5678"


def test_extract_deployed_sha_returns_empty_when_unknown() -> None:
    assert rp.extract_deployed_sha(_ok_version_probe("unknown")) == ""


def test_extract_deployed_sha_returns_empty_on_failed_probe() -> None:
    assert rp.extract_deployed_sha({"ok": False, "status": 404}) == ""


def test_extract_deployed_sha_handles_malformed_snippet() -> None:
    assert rp.extract_deployed_sha({"ok": True, "snippet": "not-json"}) == ""


def test_compare_deployed_sha_no_api_base() -> None:
    blob = rp.compare_deployed_sha("")
    assert blob["verdict"] == "NOT_PROBED"
    assert blob["reason"] == "no_api_base"


def test_compare_deployed_sha_match_full(monkeypatch) -> None:
    sha = "a" * 40
    monkeypatch.setattr(rp, "probe_get", lambda *a, **k: _ok_version_probe(sha))
    blob = rp.compare_deployed_sha("https://api.dealix.me", local_sha=sha)
    assert blob["verdict"] == "MATCH"
    assert blob["hint_ar"] == ""


def test_compare_deployed_sha_match_short_vs_full(monkeypatch) -> None:
    """Production sometimes reports a short SHA — comparison must still match."""
    full = "1234567890abcdef" + "0" * 24
    short = full[:7]
    monkeypatch.setattr(rp, "probe_get", lambda *a, **k: _ok_version_probe(short))
    blob = rp.compare_deployed_sha("https://api.dealix.me", local_sha=full)
    assert blob["verdict"] == "MATCH"


def test_compare_deployed_sha_drift_includes_arabic_hint(monkeypatch) -> None:
    deployed = "deadbee" + "f" * 33
    local = "1111111" + "1" * 33
    monkeypatch.setattr(rp, "probe_get", lambda *a, **k: _ok_version_probe(deployed))
    blob = rp.compare_deployed_sha("https://api.dealix.me", local_sha=local)
    assert blob["verdict"] == "DRIFT"
    assert "deadbee" in blob["hint_ar"]
    assert "1111111" in blob["hint_ar"]
    assert "git push" in blob["hint_ar"]


def test_compare_deployed_sha_unknown_when_prod_reports_unknown(monkeypatch) -> None:
    monkeypatch.setattr(rp, "probe_get", lambda *a, **k: _ok_version_probe("unknown"))
    blob = rp.compare_deployed_sha("https://api.dealix.me", local_sha="a" * 40)
    assert blob["verdict"] == "UNKNOWN"
    assert blob["reason"] == "deployed_sha_missing_or_unknown"
    assert "GIT_SHA" in blob["hint_ar"] or "RAILWAY_GIT_COMMIT_SHA" in blob["hint_ar"]


def test_compare_deployed_sha_unknown_when_local_unavailable(monkeypatch) -> None:
    monkeypatch.setattr(rp, "probe_get", lambda *a, **k: _ok_version_probe("a" * 40))
    blob = rp.compare_deployed_sha("https://api.dealix.me", local_sha="")
    assert blob["verdict"] == "UNKNOWN"
    assert blob["reason"] == "local_sha_unavailable"


def test_compare_deployed_sha_not_probed_on_404(monkeypatch) -> None:
    monkeypatch.setattr(
        rp,
        "probe_get",
        lambda *a, **k: {"probed": True, "ok": False, "status": 404, "url": "x"},
    )
    blob = rp.compare_deployed_sha("https://api.dealix.me", local_sha="a" * 40)
    assert blob["verdict"] == "NOT_PROBED"
    assert blob["reason"] == "version_endpoint_unreachable"
    assert "/version" in blob["hint_ar"]


def test_analyze_railway_production_carries_sha_block_when_offline() -> None:
    blob = rp.analyze_railway_production(api_base=False)
    assert "deployed_sha_check" in blob
    assert blob["deployed_sha_check"]["verdict"] == "NOT_PROBED"


def test_read_local_git_sha_returns_40_char_hex_in_repo() -> None:
    sha = rp.read_local_git_sha()
    # In a real git checkout this should be a 40-char hex; in a fresh
    # tarball it may be empty. Either is acceptable — but if present it
    # must be a valid SHA.
    if sha:
        assert len(sha) == 40
        assert all(c in "0123456789abcdef" for c in sha.lower())
