"""
Section 52 — Identity & Access.

Eight identity kinds, mapped to sovereignty tiers, with explicit permissions.
The most consequential rule: `enable_tool`, `launch_api`, `launch_marketplace`
and `approve_external_action` belong to Sami only (or an identity that Sami
has explicitly delegated to, via `Identity.delegated_by`).
"""

from __future__ import annotations

from collections.abc import Iterable
from dataclasses import dataclass, field
from datetime import UTC, datetime
from enum import StrEnum

from dealix.control_plane.sovereignty import SovereigntyTier


class IdentityKind(StrEnum):
    SAMI = "sami"
    INTERNAL_OPERATOR = "internal_operator"
    CUSTOMER_ADMIN = "customer_admin"
    CUSTOMER_USER = "customer_user"
    PARTNER_ADMIN = "partner_admin"
    AGENT = "agent"
    TOOL = "tool"
    API_CLIENT = "api_client"

    @property
    def tier(self) -> SovereigntyTier:
        return {
            IdentityKind.SAMI: SovereigntyTier.SAMI,
            IdentityKind.INTERNAL_OPERATOR: SovereigntyTier.INTERNAL,
            IdentityKind.CUSTOMER_ADMIN: SovereigntyTier.CUSTOMER,
            IdentityKind.CUSTOMER_USER: SovereigntyTier.CUSTOMER,
            IdentityKind.PARTNER_ADMIN: SovereigntyTier.PARTNER,
            IdentityKind.AGENT: SovereigntyTier.AGENT,
            IdentityKind.TOOL: SovereigntyTier.TOOL,
            IdentityKind.API_CLIENT: SovereigntyTier.PARTNER,
        }[self]


class Permission(StrEnum):
    READ_SIGNAL = "read_signal"
    CREATE_OPPORTUNITY = "create_opportunity"
    DRAFT_MESSAGE = "draft_message"
    CREATE_PROPOSAL = "create_proposal"
    REQUEST_APPROVAL = "request_approval"
    APPROVE_EXTERNAL_ACTION = "approve_external_action"
    REGISTER_TOOL = "register_tool"
    ENABLE_TOOL = "enable_tool"
    EXPORT_DATA = "export_data"
    EXPORT_SENSITIVE_DATA = "export_sensitive_data"
    LAUNCH_API = "launch_api"
    LAUNCH_MARKETPLACE = "launch_marketplace"


SOVEREIGN_ONLY: frozenset[Permission] = frozenset(
    {
        Permission.APPROVE_EXTERNAL_ACTION,
        Permission.ENABLE_TOOL,
        Permission.LAUNCH_API,
        Permission.LAUNCH_MARKETPLACE,
        Permission.EXPORT_SENSITIVE_DATA,
    }
)


_DEFAULT_PERMISSIONS: dict[IdentityKind, frozenset[Permission]] = {
    IdentityKind.SAMI: frozenset(Permission),
    IdentityKind.INTERNAL_OPERATOR: frozenset(
        {
            Permission.READ_SIGNAL,
            Permission.CREATE_OPPORTUNITY,
            Permission.DRAFT_MESSAGE,
            Permission.CREATE_PROPOSAL,
            Permission.REQUEST_APPROVAL,
            Permission.REGISTER_TOOL,
            Permission.EXPORT_DATA,
        }
    ),
    IdentityKind.CUSTOMER_ADMIN: frozenset(
        {
            Permission.READ_SIGNAL,
            Permission.CREATE_OPPORTUNITY,
            Permission.DRAFT_MESSAGE,
            Permission.CREATE_PROPOSAL,
            Permission.REQUEST_APPROVAL,
            Permission.EXPORT_DATA,
        }
    ),
    IdentityKind.CUSTOMER_USER: frozenset(
        {Permission.READ_SIGNAL, Permission.DRAFT_MESSAGE, Permission.REQUEST_APPROVAL}
    ),
    IdentityKind.PARTNER_ADMIN: frozenset(
        {
            Permission.READ_SIGNAL,
            Permission.CREATE_OPPORTUNITY,
            Permission.DRAFT_MESSAGE,
            Permission.CREATE_PROPOSAL,
            Permission.REQUEST_APPROVAL,
        }
    ),
    IdentityKind.AGENT: frozenset(
        {
            Permission.READ_SIGNAL,
            Permission.CREATE_OPPORTUNITY,
            Permission.DRAFT_MESSAGE,
            Permission.CREATE_PROPOSAL,
            Permission.REQUEST_APPROVAL,
        }
    ),
    IdentityKind.TOOL: frozenset({Permission.READ_SIGNAL}),
    IdentityKind.API_CLIENT: frozenset(
        {Permission.READ_SIGNAL, Permission.DRAFT_MESSAGE, Permission.REQUEST_APPROVAL}
    ),
}


@dataclass(frozen=True)
class Identity:
    identity_id: str
    kind: IdentityKind
    display_name: str
    tenant_id: str | None = None
    workspace_id: str | None = None
    delegated_by: str | None = None
    granted_permissions: frozenset[Permission] = field(default_factory=frozenset)
    created_at: datetime = field(default_factory=lambda: datetime.now(UTC))

    @property
    def tier(self) -> SovereigntyTier:
        return self.kind.tier

    @property
    def permissions(self) -> frozenset[Permission]:
        base = _DEFAULT_PERMISSIONS[self.kind]
        return base | self.granted_permissions

    def has(self, permission: Permission) -> bool:
        if permission in SOVEREIGN_ONLY:
            if self.kind is IdentityKind.SAMI:
                return True
            return permission in self.granted_permissions and self.delegated_by is not None
        return permission in self.permissions

    def require(self, permission: Permission) -> None:
        if not self.has(permission):
            raise PermissionError(
                f"Identity {self.identity_id} ({self.kind.value}) lacks "
                f"permission {permission.value}"
            )


class IdentityRegistry:
    """In-memory identity registry; production swaps backing store."""

    def __init__(self) -> None:
        self._identities: dict[str, Identity] = {}

    def register(self, identity: Identity) -> Identity:
        if identity.identity_id in self._identities:
            raise ValueError(f"identity already exists: {identity.identity_id}")
        self._identities[identity.identity_id] = identity
        return identity

    def upsert(self, identity: Identity) -> Identity:
        self._identities[identity.identity_id] = identity
        return identity

    def get(self, identity_id: str) -> Identity:
        try:
            return self._identities[identity_id]
        except KeyError as exc:
            raise KeyError(f"unknown identity: {identity_id}") from exc

    def by_kind(self, kind: IdentityKind) -> list[Identity]:
        return [i for i in self._identities.values() if i.kind == kind]

    def all(self) -> list[Identity]:
        return list(self._identities.values())

    def delegate(
        self,
        *,
        sami_id: str,
        delegate_id: str,
        permissions: Iterable[Permission],
    ) -> Identity:
        sami = self.get(sami_id)
        if sami.kind is not IdentityKind.SAMI:
            raise PermissionError("only Sami may delegate sovereign permissions")
        target = self.get(delegate_id)
        new_perms = frozenset(target.granted_permissions) | frozenset(permissions)
        delegated = Identity(
            identity_id=target.identity_id,
            kind=target.kind,
            display_name=target.display_name,
            tenant_id=target.tenant_id,
            workspace_id=target.workspace_id,
            delegated_by=sami.identity_id,
            granted_permissions=new_perms,
            created_at=target.created_at,
        )
        self._identities[target.identity_id] = delegated
        return delegated
