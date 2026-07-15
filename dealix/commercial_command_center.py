"""Pure daily command-center projection for the commercial universe.

This module is intentionally read-only. It aggregates tenant-scoped Wave A
records and their approval envelopes into a deterministic snapshot that a
workspace, API, or daily founder brief can render later.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Iterable

from dealix.commercial_universe import (
    ApprovalEnvelope,
    ApprovalStatus,
    CommercialAccount,
    score_account,
)


@dataclass(frozen=True)
class CommandCenterSnapshot:
    tenant_id: str
    account_count: int
    pending_approval_count: int
    blocked_count: int
    department_counts: dict[str, int]
    priority_account_ids: tuple[str, ...]
    priority_actions: tuple[str, ...]

    def __post_init__(self) -> None:
        if self.account_count < 0 or self.pending_approval_count < 0 or self.blocked_count < 0:
            raise ValueError("snapshot counts must be non-negative")
        if self.pending_approval_count + self.blocked_count > self.account_count:
            raise ValueError("approval counts cannot exceed account count")


def build_command_center(
    accounts: Iterable[CommercialAccount],
    envelopes: Iterable[ApprovalEnvelope],
    *,
    tenant_id: str | None = None,
    priority_limit: int = 5,
) -> CommandCenterSnapshot:
    """Aggregate internal opportunities into a deterministic founder brief."""
    account_list = list(accounts)
    envelope_list = list(envelopes)
    if priority_limit < 1:
        raise ValueError("priority_limit must be positive")
    if not account_list:
        raise ValueError("at least one account is required")

    resolved_tenant = tenant_id or account_list[0].tenant_id
    if any(account.tenant_id != resolved_tenant for account in account_list):
        raise ValueError("all accounts must share one tenant")
    if any(envelope.tenant_id != resolved_tenant for envelope in envelope_list):
        raise ValueError("all envelopes must share one tenant")

    by_account = {account.account_id: account for account in account_list}
    if len(by_account) != len(account_list):
        raise ValueError("account_id values must be unique")
    if any(envelope.account_id not in by_account for envelope in envelope_list):
        raise ValueError("every envelope must reference a known account")

    status_by_account = {envelope.account_id: envelope.status for envelope in envelope_list}
    pending = sum(status is ApprovalStatus.REQUIRED for status in status_by_account.values())
    blocked = sum(status is ApprovalStatus.BLOCKED for status in status_by_account.values())
    departments = Counter(account.department.value for account in account_list)

    ranked = sorted(
        (
            account
            for account in account_list
            if status_by_account.get(account.account_id) is ApprovalStatus.REQUIRED
        ),
        key=lambda account: (-score_account(account), -account.urgency, account.account_id),
    )
    priority_accounts = tuple(account.account_id for account in ranked[:priority_limit])
    action_by_account = {envelope.account_id: envelope.action for envelope in envelope_list}
    priority_actions = tuple(action_by_account[account_id] for account_id in priority_accounts)

    return CommandCenterSnapshot(
        tenant_id=resolved_tenant,
        account_count=len(account_list),
        pending_approval_count=pending,
        blocked_count=blocked,
        department_counts=dict(sorted(departments.items())),
        priority_account_ids=priority_accounts,
        priority_actions=priority_actions,
    )


__all__ = ["CommandCenterSnapshot", "build_command_center"]
