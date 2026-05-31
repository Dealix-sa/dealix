"""
Downstream validation — before letting agent A's output reach agent B,
check that the trust level + sanitization status are compatible with
agent B's risk band.
"""

from __future__ import annotations

from dataclasses import dataclass

from dealix.hermes.provenance.ledger import ProvenanceObject
from dealix.hermes.provenance.trust_level import TrustLevel


@dataclass
class DownstreamValidation:
    allowed: bool
    reason: str
    must_sanitize: bool = False


def validate_for_downstream(
    obj: ProvenanceObject,
    *,
    downstream_agent_id: str,
    downstream_risk_band: str,
    will_be_used_as_instruction: bool,
) -> DownstreamValidation:
    """Hard rule: untrusted/quarantined data is NEVER allowed to act as instructions."""
    tl = obj.source_metadata.trust_level
    if tl == TrustLevel.QUARANTINED:
        return DownstreamValidation(
            False, f"object {obj.object_id} is quarantined", must_sanitize=False
        )
    if will_be_used_as_instruction and tl in (TrustLevel.UNTRUSTED, TrustLevel.VERIFIED):
        return DownstreamValidation(
            False,
            (
                f"object {obj.object_id} (trust={tl.value}) cannot be used as "
                f"instructions for agent {downstream_agent_id}"
            ),
            must_sanitize=False,
        )
    if tl == TrustLevel.UNTRUSTED and not obj.sanitized:
        return DownstreamValidation(
            True,
            "untrusted data allowed downstream only after sanitization",
            must_sanitize=True,
        )
    if downstream_risk_band in ("high", "critical") and not obj.sanitized:
        return DownstreamValidation(
            True,
            f"downstream agent risk band {downstream_risk_band} requires sanitization",
            must_sanitize=True,
        )
    return DownstreamValidation(True, "ok")
