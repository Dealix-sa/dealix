"""Deterministic trust policy for Dealix MCP tools and network endpoints.

This module has no FastMCP dependency so CI and security checks can import it
without starting a server. It deliberately does not perform an HTTP request.
Callers must connect only to one of the returned, validated IP addresses while
preserving the original hostname for TLS certificate validation.
"""

from __future__ import annotations

import hashlib
import ipaddress
import json
import socket
from dataclasses import asdict, dataclass
from typing import Any, Callable, Iterable, Literal
from urllib.parse import urlparse

MANIFEST_SCHEMA_VERSION = "dealix.mcp-tool-manifest.v1"
ALLOWED_TOOL_CAPABILITIES = frozenset({"read", "local_draft"})
ALLOWED_DATA_CLASSES = frozenset({"internal", "personal", "public"})
DENIED_TOOL_CAPABILITIES = frozenset(
    {
        "browser_session",
        "credential_access",
        "external_send",
        "filesystem_write",
        "network_read",
        "network_write",
        "payment",
        "production_mutation",
        "raw_database",
        "shell",
    }
)
_LOOPBACK_BINDINGS = frozenset({"127.0.0.1", "::1", "localhost"})


@dataclass(frozen=True, slots=True)
class ToolPolicy:
    """Least-privilege declaration attached to every Dealix MCP tool."""

    name: str
    capability: Literal["read", "local_draft"]
    data_classes: tuple[str, ...] = ("internal",)
    approval_required: bool = False
    external_side_effects: bool = False


@dataclass(frozen=True, slots=True)
class EndpointDecision:
    allowed: bool
    reason: str
    host: str
    resolved_ips: tuple[str, ...] = ()
    resolution_fingerprint: str | None = None


@dataclass(frozen=True, slots=True)
class BindingDecision:
    allowed: bool
    reason: str
    allowed_hosts: tuple[str, ...] = ()
    allowed_origins: tuple[str, ...] = ()


def validate_tool_policy(policy: ToolPolicy) -> list[str]:
    errors: list[str] = []
    if not policy.name or not policy.name.replace("_", "").isalnum():
        errors.append("tool name must contain only letters, numbers, and underscores")
    if policy.capability not in ALLOWED_TOOL_CAPABILITIES:
        errors.append(f"capability {policy.capability!r} is not allowed")
    if policy.external_side_effects:
        errors.append("external side effects are forbidden in the Dealix MCP server")
    if policy.capability == "local_draft" and not policy.approval_required:
        errors.append("local_draft tools must require approval")
    if not policy.data_classes:
        errors.append("at least one data class is required")
    invalid_data_classes = sorted(set(policy.data_classes) - ALLOWED_DATA_CLASSES)
    if invalid_data_classes:
        errors.append(f"data classes are not allowed: {', '.join(invalid_data_classes)}")
    return errors


def register_tool_policy(registry: dict[str, ToolPolicy], policy: ToolPolicy) -> None:
    """Register one policy and reject duplicates or unsafe declarations."""
    errors = validate_tool_policy(policy)
    if errors:
        raise ValueError(f"unsafe MCP tool policy for {policy.name!r}: {'; '.join(errors)}")
    existing = registry.get(policy.name)
    if existing is not None and existing != policy:
        raise ValueError(f"conflicting MCP tool policy for {policy.name!r}")
    registry[policy.name] = policy


def build_tool_manifest(
    policies: Iterable[ToolPolicy],
    *,
    server_id: str = "dealix-business-os",
) -> dict[str, Any]:
    """Build a stable manifest whose fingerprint changes on permission drift."""
    ordered = sorted(policies, key=lambda item: item.name)
    if not ordered:
        raise ValueError("MCP manifest cannot be empty")
    names: set[str] = set()
    for policy in ordered:
        errors = validate_tool_policy(policy)
        if errors:
            raise ValueError(f"unsafe MCP tool policy for {policy.name!r}: {'; '.join(errors)}")
        if policy.name in names:
            raise ValueError(f"duplicate MCP tool policy for {policy.name!r}")
        names.add(policy.name)

    unsigned = {
        "schema_version": MANIFEST_SCHEMA_VERSION,
        "server_id": server_id,
        "allowed_capabilities": sorted(ALLOWED_TOOL_CAPABILITIES),
        "denied_capabilities": sorted(DENIED_TOOL_CAPABILITIES),
        "external_send": False,
        "payment": False,
        "production_mutation": False,
        "tools": [asdict(policy) for policy in ordered],
    }
    canonical = json.dumps(unsigned, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    return {**unsigned, "sha256": hashlib.sha256(canonical.encode()).hexdigest()}


def _normalize_allowed_hosts(allowed_hosts: Iterable[str]) -> tuple[str, ...]:
    normalized: list[str] = []
    for raw in allowed_hosts:
        value = raw.strip().lower().rstrip(".")
        if not value:
            continue
        if any(token in value for token in ("*", ":", "/", "@")):
            raise ValueError(f"invalid exact host entry: {raw!r}")
        normalized.append(value)
    return tuple(sorted(set(normalized)))


def _normalize_allowed_origins(allowed_origins: Iterable[str]) -> tuple[str, ...]:
    normalized: list[str] = []
    for raw in allowed_origins:
        value = raw.strip()
        if not value:
            continue
        parsed = urlparse(value)
        if (
            value == "*"
            or parsed.scheme.lower() != "https"
            or not parsed.hostname
            or parsed.username
            or parsed.password
            or parsed.path not in ("", "/")
            or parsed.query
            or parsed.fragment
        ):
            raise ValueError(f"invalid exact HTTPS origin: {raw!r}")
        normalized.append(f"https://{parsed.netloc.lower()}")
    return tuple(sorted(set(normalized)))


def validate_http_binding(
    *,
    transport: str,
    bind_host: str,
    allowed_hosts: Iterable[str] = (),
    allowed_origins: Iterable[str] = (),
    remote_enabled: bool = False,
    trusted_ingress_auth: bool = False,
) -> BindingDecision:
    """Fail closed before FastMCP binds a remotely reachable HTTP socket."""
    if transport == "stdio":
        return BindingDecision(True, "stdio has no network listener")
    if transport not in {"http", "sse"}:
        return BindingDecision(False, f"unsupported transport {transport!r}")

    host = bind_host.strip().lower().strip("[]").rstrip(".")
    if host in _LOOPBACK_BINDINGS:
        return BindingDecision(True, "loopback-only HTTP binding")
    try:
        bind_ip = ipaddress.ip_address(host)
    except ValueError:
        bind_ip = None
    if bind_ip is not None and bind_ip.is_loopback:
        return BindingDecision(True, "loopback-only HTTP binding")

    try:
        normalized_hosts = _normalize_allowed_hosts(allowed_hosts)
        normalized_origins = _normalize_allowed_origins(allowed_origins)
    except ValueError as exc:
        return BindingDecision(False, str(exc))

    if not remote_enabled:
        return BindingDecision(False, "remote MCP HTTP is disabled")
    if not trusted_ingress_auth:
        return BindingDecision(False, "remote MCP HTTP requires an auth-enforcing trusted ingress")
    if not normalized_hosts:
        return BindingDecision(False, "remote MCP HTTP requires exact allowed hosts")
    if not normalized_origins:
        return BindingDecision(False, "remote MCP HTTP requires exact allowed origins")
    return BindingDecision(
        True,
        "remote binding explicitly approved with ingress auth and exact host/origin policy",
        normalized_hosts,
        normalized_origins,
    )


Resolver = Callable[..., list[tuple[Any, ...]]]


def _resolve_public_ips(host: str, port: int, resolver: Resolver) -> tuple[str, ...]:
    records = resolver(host, port, type=socket.SOCK_STREAM)
    addresses: set[str] = set()
    for record in records:
        sockaddr = record[4]
        if not sockaddr:
            continue
        address = str(sockaddr[0]).split("%", maxsplit=1)[0]
        ip = ipaddress.ip_address(address)
        if not ip.is_global:
            raise ValueError(f"resolved address {ip} is not globally routable")
        addresses.add(ip.compressed)
    if not addresses:
        raise ValueError("DNS resolution returned no addresses")
    return tuple(sorted(addresses))


def validate_mcp_endpoint(
    url: str,
    *,
    allowed_hosts: Iterable[str],
    resolver: Resolver = socket.getaddrinfo,
) -> EndpointDecision:
    """Validate an outbound MCP endpoint and return IPs that must be pinned."""
    try:
        normalized_hosts = _normalize_allowed_hosts(allowed_hosts)
        parsed = urlparse(url)
        host = (parsed.hostname or "").lower().rstrip(".")
        port = parsed.port or 443
    except (TypeError, ValueError) as exc:
        return EndpointDecision(False, f"invalid MCP endpoint: {exc}", "")

    if parsed.scheme.lower() != "https":
        return EndpointDecision(False, "outbound MCP endpoints require https", host)
    if not host or parsed.username or parsed.password:
        return EndpointDecision(False, "endpoint host is missing or contains credentials", host)
    if parsed.query or parsed.fragment:
        return EndpointDecision(False, "endpoint query and fragment are forbidden", host)
    if port != 443:
        return EndpointDecision(False, "outbound MCP endpoints require port 443", host)
    if host not in normalized_hosts:
        return EndpointDecision(False, "endpoint host is not in the exact allowlist", host)
    try:
        literal = ipaddress.ip_address(host)
    except ValueError:
        literal = None
    if literal is not None and not literal.is_global:
        return EndpointDecision(False, "endpoint IP is not globally routable", host)

    try:
        addresses = _resolve_public_ips(host, port, resolver)
    except (OSError, ValueError) as exc:
        return EndpointDecision(False, f"unsafe DNS resolution: {exc}", host)
    fingerprint = hashlib.sha256("\n".join(addresses).encode()).hexdigest()
    return EndpointDecision(True, "approved endpoint; pin one validated IP for connect", host, addresses, fingerprint)


def revalidate_mcp_endpoint(
    previous: EndpointDecision,
    *,
    url: str,
    allowed_hosts: Iterable[str],
    resolver: Resolver = socket.getaddrinfo,
) -> EndpointDecision:
    """Detect DNS rebinding/resolution drift immediately before a reconnect."""
    if not previous.allowed or not previous.resolution_fingerprint:
        return EndpointDecision(False, "previous endpoint decision is not approved", previous.host)
    current = validate_mcp_endpoint(url, allowed_hosts=allowed_hosts, resolver=resolver)
    if not current.allowed:
        return current
    if current.resolution_fingerprint != previous.resolution_fingerprint:
        return EndpointDecision(
            False,
            "DNS resolution changed; require a fresh approval before reconnect",
            current.host,
            current.resolved_ips,
            current.resolution_fingerprint,
        )
    return current
