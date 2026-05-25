"""Message drafting — copywriter outputs land here."""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import UTC, datetime

from pydantic import BaseModel, ConfigDict, Field


def _now() -> str:
    return datetime.now(UTC).isoformat()


def _mid() -> str:
    return f"msg_{uuid.uuid4().hex[:16]}"


class Message(BaseModel):
    model_config = ConfigDict(extra="forbid")

    message_id: str = Field(default_factory=_mid)
    campaign_id: str
    channel: str
    locale: str = "en"
    body: str
    approval_id: str | None = None
    created_at: str = Field(default_factory=_now)


@dataclass
class MessageStore:
    _messages: dict[str, Message] = field(default_factory=dict)

    def draft(self, message: Message) -> Message:
        self._messages[message.message_id] = message
        return message

    def approve(self, message_id: str, approval_id: str) -> Message:
        m = self._messages[message_id]
        updated = m.model_copy(update={"approval_id": approval_id})
        self._messages[message_id] = updated
        return updated

    def list(self) -> list[Message]:
        return list(self._messages.values())
