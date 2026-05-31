"""
Red-team playbooks — structured incident-response checklists.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class RedTeamPlaybook:
    name: str
    trigger: str
    steps: tuple[str, ...]


RED_TEAM_PLAYBOOKS: tuple[RedTeamPlaybook, ...] = (
    RedTeamPlaybook(
        name="suspected_prompt_injection",
        trigger="message_sanitizer or indirect_injection_detector findings != []",
        steps=(
            "Quarantine the affected ProvenanceObject (set TrustLevel=QUARANTINED).",
            "Restrict the receiving agent to DRAFT_ONLY for the next 24h.",
            "Open an Approval Center ticket with the sanitized message attached.",
            "Run the standard prompt-injection test vectors against the responsible "
            "tool/route to confirm coverage.",
            "If a downstream action was taken before detection, roll it back and "
            "notify the workspace owner.",
        ),
    ),
    RedTeamPlaybook(
        name="mcp_anomaly",
        trigger="mcp.anomaly_detection severity in ('warn','critical')",
        steps=(
            "Trip the MCP kill switch for the affected server.",
            "Compare current manifest_sha256 against the allowlist entry — if it "
            "drifted, disable the server.",
            "Snapshot the last 100 calls (request + response previews) for review.",
            "Schedule a manifest re-review before re-enabling.",
        ),
    ),
    RedTeamPlaybook(
        name="dlp_secret_leak",
        trigger="data_loss_prevention.findings contains secret_token:* or pii:possible_*",
        steps=(
            "Block the outbound payload at the boundary.",
            "Rotate the leaked credential (if any) within 1 hour.",
            "Trace the lineage via ProvenanceLedger to the originating object_id.",
            "Add a regression test vector to prompt_injection_tests with the offending "
            "shape.",
        ),
    ),
    RedTeamPlaybook(
        name="overclaim_in_marketing",
        trigger="claim_verifier.flagged_phrases != []",
        steps=(
            "Block the asset from publishing.",
            "Route the asset to the approved-claims editor (partners.approved_claims).",
            "Update the offending template with safe alternatives.",
        ),
    ),
)
