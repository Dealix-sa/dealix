from __future__ import annotations

from dealix.commercial_ops.railway_production import (
    check_repo_railway_config,
    probe_get,
)


def test_repo_railway_config_ok() -> None:
    repo = check_repo_railway_config()
    assert repo["ok"] is True


def test_probe_healthz_shape() -> None:
    # offline — invalid host should not raise
    blob = probe_get("http://127.0.0.1:1", "/healthz", timeout_sec=0.5)
    assert blob["probed"] is True
    assert blob.get("ok") is False
