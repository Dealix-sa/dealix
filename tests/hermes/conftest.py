"""Per-test isolation for the global state inside ``dealix.hermes``.

The control plane holds in-memory singletons (kill switch, approval
center, outcome registry, audit log, metrics, alert log). Resetting
them between tests guarantees that hermes tests behave the same in
isolation and as part of the wider project test suite.
"""

from __future__ import annotations

import pytest


@pytest.fixture(autouse=True)
def _reset_hermes_global_state():
    from dealix.hermes.assets.asset_store import ASSET_STORE
    from dealix.hermes.control_plane.approval_gate import CENTER as APPROVAL_CENTER
    from dealix.hermes.control_plane.audit_gate import LOG as AUDIT_LOG
    from dealix.hermes.control_plane.kill_switch import SWITCH as KILL_SWITCH
    from dealix.hermes.control_plane.outcome_gate import REGISTRY as OUTCOME_REGISTRY
    from dealix.hermes.control_plane.runtime_modes import STATE as RUNTIME_STATE
    from dealix.hermes.control_plane.runtime_modes import RuntimeMode
    from dealix.hermes.identity.revocation import REVOCATION_LIST
    from dealix.hermes.observability.alerts import ALERT_LOG
    from dealix.hermes.observability.metrics import METRICS_REGISTRY

    snapshot_assets = dict(ASSET_STORE)
    snapshot_metrics = {n: (m.value, list(m.samples)) for n, m in METRICS_REGISTRY.items()}

    yield

    # Wipe runtime / governance state created during the test.
    KILL_SWITCH._entries.clear()
    APPROVAL_CENTER._tickets.clear()
    OUTCOME_REGISTRY._by_request.clear()
    AUDIT_LOG._records.clear()
    ALERT_LOG.clear()
    REVOCATION_LIST.clear()
    RUNTIME_STATE.current = RuntimeMode.DRAFT_ONLY

    # Restore registries that were pre-seeded at import time.
    ASSET_STORE.clear()
    ASSET_STORE.update(snapshot_assets)
    for name, (value, samples) in snapshot_metrics.items():
        m = METRICS_REGISTRY[name]
        m.value = value
        m.samples = samples
