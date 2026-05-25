"""
Authorization Gate — التحقق أن actor عنده صلاحية لتنفيذ intent على هذا الـ
workspace/customer/partner. لا يتعامل مع المخاطر — مهمته شيء واحد فقط: هل
هذا الكائن مسموح له يطلب هذا الفعل؟
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Protocol

from ..contracts import Actor, ActorKind, ContextPacket, GateResult


@dataclass(frozen=True)
class Permission:
    actor_kind: ActorKind
    intent_prefix: str  # eg "external.proposal."  matches any intent that startswith
    scope: str = "*"  # "*" | "own_customer" | "own_partner" | workspace_id


class PermissionRegistry(Protocol):
    def permissions_for(self, actor: Actor) -> list[Permission]: ...


class DefaultPermissionRegistry:
    """
    افتراضات معقولة. تُستبدل لاحقًا بـ Postgres-backed registry.

    - Founder      → كل شيء.
    - Internal     → draft + execute داخلي، draft خارجي (لا execute).
    - Agent        → draft فقط، أي tool يمر عبر tool_gateway.
    - Customer     → فقط داخل workspace العميل نفسه.
    - Partner      → فقط داخل workspace الشريك.
    - System       → workflows مجدولة فقط.
    - Public       → tools عامة فقط (lead capture, diagnostic).
    """

    def permissions_for(self, actor: Actor) -> list[Permission]:
        k = actor.kind
        if k == ActorKind.FOUNDER:
            return [Permission(k, "")]
        if k == ActorKind.INTERNAL_USER:
            return [
                Permission(k, "internal."),
                Permission(k, "draft."),
                Permission(k, "external.", scope="draft_only"),
            ]
        if k == ActorKind.AGENT:
            return [Permission(k, "draft."), Permission(k, "internal.read.")]
        if k == ActorKind.CUSTOMER:
            return [Permission(k, "customer.", scope="own_customer")]
        if k == ActorKind.PARTNER:
            return [Permission(k, "partner.", scope="own_partner")]
        if k == ActorKind.SYSTEM:
            return [Permission(k, "system.")]
        if k == ActorKind.PUBLIC:
            return [
                Permission(k, "public.diagnostic."),
                Permission(k, "public.lead.capture"),
            ]
        return []


class AuthorizationGate:
    STAGE = "gate.authorization"

    def __init__(self, registry: PermissionRegistry | None = None) -> None:
        self._registry = registry or DefaultPermissionRegistry()

    def check(self, context: ContextPacket, intent: str) -> GateResult:
        actor = context.actor
        if actor is None:
            return GateResult(
                stage=self.STAGE,
                passed=False,
                reason="missing actor",
            )

        perms = self._registry.permissions_for(actor)
        for p in perms:
            if intent.startswith(p.intent_prefix) or p.intent_prefix == "":
                if not self._scope_ok(context, actor, p.scope):
                    continue
                return GateResult(
                    stage=self.STAGE,
                    passed=True,
                    metadata={"matched_prefix": p.intent_prefix, "scope": p.scope},
                )
        return GateResult(
            stage=self.STAGE,
            passed=False,
            reason=f"{actor.kind.value} not authorized for `{intent}`",
        )

    @staticmethod
    def _scope_ok(context: ContextPacket, actor: Actor, scope: str) -> bool:
        if scope in {"*", "draft_only"}:
            return True
        if scope == "own_customer":
            return (
                actor.customer_id is not None
                and context.customer_id == actor.customer_id
            )
        if scope == "own_partner":
            return (
                actor.partner_id is not None
                and context.partner_id == actor.partner_id
            )
        return False


__all__ = [
    "AuthorizationGate",
    "DefaultPermissionRegistry",
    "Permission",
    "PermissionRegistry",
]
