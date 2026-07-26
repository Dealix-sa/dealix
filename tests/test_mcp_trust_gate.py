from __future__ import annotations

import importlib.util
import json
import socket
import sys
import types
from pathlib import Path
from typing import Any

import pytest

_REPO = Path(__file__).resolve().parents[1]
_MODULE_PATH = _REPO / "mcp_server" / "trust_gate.py"
_SPEC = importlib.util.spec_from_file_location("_dealix_mcp_trust_gate", _MODULE_PATH)
assert _SPEC and _SPEC.loader
_MODULE = importlib.util.module_from_spec(_SPEC)
sys.modules[_SPEC.name] = _MODULE
_SPEC.loader.exec_module(_MODULE)

ToolPolicy = _MODULE.ToolPolicy
ToolRateLimiter = _MODULE.ToolRateLimiter
build_tool_manifest = _MODULE.build_tool_manifest
revalidate_mcp_endpoint = _MODULE.revalidate_mcp_endpoint
validate_http_binding = _MODULE.validate_http_binding
validate_mcp_endpoint = _MODULE.validate_mcp_endpoint
REMOTE_WILDCARD_BIND = "0.0.0.0"  # noqa: S104 - deliberate unsafe input for fail-closed tests


def _resolver(*addresses: str):
    def resolve(host: str, port: int, **kwargs: Any) -> list[tuple[Any, ...]]:
        del host, kwargs
        return [
            (
                socket.AF_INET6 if ":" in address else socket.AF_INET,
                socket.SOCK_STREAM,
                6,
                "",
                (address, port),
            )
            for address in addresses
        ]

    return resolve


def test_manifest_is_deterministic_and_denies_external_authority() -> None:
    policies = [
        ToolPolicy(name="read_status", capability="read"),
        ToolPolicy(
            name="draft_intro",
            capability="local_draft",
            approval_required=True,
            timeout_seconds=45,
        ),
    ]

    first = build_tool_manifest(policies)
    second = build_tool_manifest(reversed(policies))

    assert first == second
    assert len(first["sha256"]) == 64
    assert first["external_send"] is False
    assert first["payment"] is False
    assert "shell" in first["denied_capabilities"]
    tools = {item["name"]: item for item in first["tools"]}
    assert tools["draft_intro"]["timeout_seconds"] == 45
    assert tools["draft_intro"]["rate_limit_per_minute"] == 60


def test_manifest_rejects_unsafe_or_duplicate_tools() -> None:
    with pytest.raises(ValueError, match="must require approval"):
        build_tool_manifest([ToolPolicy(name="draft", capability="local_draft")])
    with pytest.raises(ValueError, match="duplicate"):
        build_tool_manifest(
            [
                ToolPolicy(name="read_status", capability="read"),
                ToolPolicy(name="read_status", capability="read"),
            ]
        )
    with pytest.raises(ValueError, match="data classes are not allowed"):
        build_tool_manifest([ToolPolicy(name="read_secret", capability="read", data_classes=("secret",))])
    with pytest.raises(ValueError, match="timeout_seconds"):
        build_tool_manifest([ToolPolicy(name="slow", capability="read", timeout_seconds=0)])
    with pytest.raises(ValueError, match="rate_limit_per_minute"):
        build_tool_manifest([ToolPolicy(name="burst", capability="read", rate_limit_per_minute=0)])


def test_rate_limit_is_enforced_and_recovers_after_window() -> None:
    now = [100.0]
    limiter = ToolRateLimiter(clock=lambda: now[0])
    policy = ToolPolicy(name="read_status", capability="read", rate_limit_per_minute=2)

    limiter.enforce(policy)
    limiter.enforce(policy)
    with pytest.raises(RuntimeError, match="rate limit exceeded"):
        limiter.enforce(policy)

    now[0] += 60.1
    limiter.enforce(policy)


def test_endpoint_blocks_private_resolution_even_when_host_is_allowed() -> None:
    decision = validate_mcp_endpoint(
        "https://mcp.example.com/mcp",
        allowed_hosts={"mcp.example.com"},
        resolver=_resolver("127.0.0.1"),
    )

    assert decision.allowed is False
    assert "not globally routable" in decision.reason


def test_endpoint_returns_public_ips_and_stable_fingerprint() -> None:
    decision = validate_mcp_endpoint(
        "https://mcp.example.com/mcp",
        allowed_hosts={"mcp.example.com"},
        resolver=_resolver("93.184.216.34", "2606:2800:220:1:248:1893:25c8:1946"),
    )

    assert decision.allowed is True
    assert decision.resolved_ips == ("2606:2800:220:1:248:1893:25c8:1946", "93.184.216.34")
    assert len(str(decision.resolution_fingerprint)) == 64


def test_dns_resolution_change_requires_fresh_approval() -> None:
    previous = validate_mcp_endpoint(
        "https://mcp.example.com/mcp",
        allowed_hosts={"mcp.example.com"},
        resolver=_resolver("93.184.216.34"),
    )
    current = revalidate_mcp_endpoint(
        previous,
        url="https://mcp.example.com/mcp",
        allowed_hosts={"mcp.example.com"},
        resolver=_resolver("1.1.1.1"),
    )

    assert current.allowed is False
    assert "fresh approval" in current.reason


def test_remote_http_binding_is_disabled_by_default() -> None:
    decision = validate_http_binding(transport="http", bind_host=REMOTE_WILDCARD_BIND)

    assert decision.allowed is False
    assert decision.reason == "remote MCP HTTP is disabled"


def test_all_loopback_addresses_remain_available_without_remote_authority() -> None:
    decision = validate_http_binding(transport="http", bind_host="127.0.0.2")

    assert decision.allowed is True
    assert decision.reason == "loopback-only HTTP binding"


def test_remote_binding_requires_auth_and_exact_hosts_and_origins() -> None:
    no_auth = validate_http_binding(
        transport="http",
        bind_host=REMOTE_WILDCARD_BIND,
        allowed_hosts={"mcp.dealix.me"},
        allowed_origins={"https://chatgpt.com"},
        remote_enabled=True,
    )
    wildcard = validate_http_binding(
        transport="http",
        bind_host=REMOTE_WILDCARD_BIND,
        allowed_hosts={"*.dealix.me"},
        allowed_origins={"https://chatgpt.com"},
        remote_enabled=True,
        trusted_ingress_auth=True,
    )
    allowed = validate_http_binding(
        transport="http",
        bind_host=REMOTE_WILDCARD_BIND,
        allowed_hosts={"mcp.dealix.me"},
        allowed_origins={"https://chatgpt.com"},
        remote_enabled=True,
        trusted_ingress_auth=True,
    )

    assert no_auth.allowed is False
    assert "auth-enforcing" in no_auth.reason
    assert wildcard.allowed is False
    assert "invalid exact host" in wildcard.reason
    assert allowed.allowed is True
    assert allowed.allowed_hosts == ("mcp.dealix.me",)
    assert allowed.allowed_origins == ("https://chatgpt.com",)


def test_server_source_has_no_ungoverned_tool_decorators() -> None:
    source = (_REPO / "mcp_server" / "dealix_mcp.py").read_text(encoding="utf-8")

    assert "@mcp.tool" not in source
    assert source.count("@governed_tool") >= 21
    assert "allowed_hosts=list(binding.allowed_hosts)" in source
    assert "allowed_origins=list(binding.allowed_origins)" in source


def test_server_import_registers_every_tool_under_policy(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    class FakeFastMCP:
        def __init__(self, **kwargs: Any) -> None:
            self.kwargs = kwargs

        def tool(self, func):
            return func

        def resource(self, *args: Any, **kwargs: Any):
            del args, kwargs
            return lambda func: func

        def prompt(self, func):
            return func

        def run(self, **kwargs: Any) -> None:
            self.run_kwargs = kwargs

    monkeypatch.setitem(sys.modules, "fastmcp", types.SimpleNamespace(FastMCP=FakeFastMCP))
    server_path = _REPO / "mcp_server" / "dealix_mcp.py"
    spec = importlib.util.spec_from_file_location("_dealix_mcp_policy_import", server_path)
    assert spec and spec.loader
    module = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = module
    spec.loader.exec_module(module)

    manifest = json.loads(module.get_mcp_trust_manifest())
    policies = {item["name"]: item for item in manifest["tools"]}
    assert len(policies) == 21
    assert policies["draft_warm_intro"]["capability"] == "local_draft"
    assert policies["draft_warm_intro"]["approval_required"] is True
    assert policies["draft_warm_intro"]["timeout_seconds"] == 45
    assert policies["draft_warm_intro"]["rate_limit_per_minute"] == 10
    assert policies["run_diagnostic_report"]["approval_required"] is True
    assert all(item["external_side_effects"] is False for item in policies.values())
