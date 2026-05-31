"""
AgentMessage — the wire envelope for cross-agent calls.

This carries the message text plus provenance and intended capability so
the validator can make a single end-to-end decision.
"""

from __future__ import annotations

import time
import uuid
from dataclasses import dataclass, field

from dealix.hermes.provenance.source_metadata import SourceMetadata


@dataclass
class AgentMessage:
    message_id: str
    sender_agent_id: str
    receiver_agent_id: str
    requested_capability: str
    text: str
    source_metadata: SourceMetadata
    created_at: float = field(default_factory=time.time)
    sanitized: bool = False
    sanitization_findings: tuple[str, ...] = field(default_factory=tuple)


def build_agent_message(
    sender_agent_id: str,
    receiver_agent_id: str,
    requested_capability: str,
    text: str,
    source_metadata: SourceMetadata,
) -> AgentMessage:
    return AgentMessage(
        message_id=str(uuid.uuid4()),
        sender_agent_id=sender_agent_id,
        receiver_agent_id=receiver_agent_id,
        requested_capability=requested_capability,
        text=text,
        source_metadata=source_metadata,
    )
