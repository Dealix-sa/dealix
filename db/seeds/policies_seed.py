"""Hermes policy seeds.

Default policies that the control plane enforces. Each policy has an
``id``, human ``description``, ``severity`` and a ``default_action`` the
runtime applies when the policy fails.
"""

from __future__ import annotations

from typing import Any

POLICIES: list[dict[str, Any]] = [
    {
        "id": "external_action_policy",
        "description": (
            "Any side-effecting action that leaves Dealix infrastructure "
            "requires an approval ticket and a registered tool."
        ),
        "severity": "high",
        "default_action": "require_approval",
    },
    {
        "id": "sensitive_data_policy",
        "description": (
            "Personally identifiable information must not leave Dealix "
            "boundaries without founder approval and a SourcePassport."
        ),
        "severity": "critical",
        "default_action": "block",
    },
    {
        "id": "pricing_policy",
        "description": (
            "Quoted prices must fall inside the registered min/max band "
            "for the offer. Out-of-band quotes require founder approval."
        ),
        "severity": "high",
        "default_action": "require_approval",
    },
    {
        "id": "mcp_policy",
        "description": (
            "Only reviewed and approved MCP servers may be invoked. "
            "Pending servers must remain in review-only mode."
        ),
        "severity": "high",
        "default_action": "block",
    },
    {
        "id": "partner_claim_policy",
        "description": (
            "Partner-attributed revenue must reconcile with a verified "
            "revenue event before any payout is calculated."
        ),
        "severity": "medium",
        "default_action": "require_approval",
    },
    {
        "id": "revenue_verification_policy",
        "description": (
            "Revenue may only graduate to verified status when an "
            "invoice or client confirmation is attached."
        ),
        "severity": "high",
        "default_action": "require_verification",
    },
]


__all__ = ["POLICIES"]
