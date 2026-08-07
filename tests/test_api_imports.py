"""Enterprise control plane import smoke tests."""

from __future__ import annotations


def test_api_imports_without_errors() -> None:
    from api.main import app

    assert app is not None


def _collect_paths(routes: object, parent_prefix: str = "") -> set[str]:
    paths: set[str] = set()
    for route in routes:  # type: ignore[union-attr]
        if type(route).__name__ == "_IncludedRouter":
            ctx = route.include_context
            prefix = (getattr(ctx, "prefix", "") or "") if ctx is not None else ""
            full_prefix = parent_prefix + prefix
            orig = route.original_router
            for r in orig.routes:
                p = getattr(r, "path", "")
                if p:
                    paths.add(full_prefix + p)
            paths.update(_collect_paths(orig.routes, full_prefix))
        elif hasattr(route, "path") and route.path:
            paths.add(parent_prefix + route.path)
    return paths


def test_systems_26_35_routers_registered() -> None:
    from api.main import app

    # Walk _IncludedRouter stubs (no .path on stubs; prefix lives in include_context).
    registered_paths = _collect_paths(app.routes)
    required_paths = {
        "/api/v1/control-plane/health",
        "/api/v1/agent-mesh/health",
        "/api/v1/assurance-contracts/health",
        "/api/v1/sandbox/health",
        "/api/v1/org-graph/health",
        "/api/v1/runtime-safety/health",
        "/api/v1/simulation/health",
        "/api/v1/human-ai/health",
        "/api/v1/value-engine/health",
        "/api/v1/self-evolving/health",
    }
    assert required_paths.issubset(registered_paths)
