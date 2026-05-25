"""
Provenance ledger — in-memory append-only store of ProvenanceObjects.
"""

from __future__ import annotations

import uuid
from dataclasses import dataclass, field

from dealix.hermes.provenance.source_metadata import SourceMetadata


@dataclass
class ProvenanceObject:
    object_id: str
    object_type: str
    source_metadata: SourceMetadata
    created_by: str
    used_by: list[str] = field(default_factory=list)
    sanitized: bool = False
    policy_notes: list[str] = field(default_factory=list)
    payload_preview: str = ""

    def to_dict(self) -> dict[str, object]:
        return {
            "object_id": self.object_id,
            "object_type": self.object_type,
            "source": self.source_metadata.source,
            "source_trust_level": self.source_metadata.trust_level.value,
            "created_by": self.created_by,
            "used_by": list(self.used_by),
            "sanitized": self.sanitized,
            "policy_notes": list(self.policy_notes),
            "payload_preview": self.payload_preview,
        }


class ProvenanceLedger:
    def __init__(self) -> None:
        self._objects: dict[str, ProvenanceObject] = {}

    def append(
        self,
        object_type: str,
        source_metadata: SourceMetadata,
        created_by: str,
        *,
        payload_preview: str = "",
        sanitized: bool = False,
        policy_notes: list[str] | None = None,
    ) -> ProvenanceObject:
        obj = ProvenanceObject(
            object_id=str(uuid.uuid4()),
            object_type=object_type,
            source_metadata=source_metadata,
            created_by=created_by,
            sanitized=sanitized,
            policy_notes=list(policy_notes or []),
            payload_preview=payload_preview[:200],
        )
        self._objects[obj.object_id] = obj
        return obj

    def record_use(self, object_id: str, consumed_by: str) -> None:
        obj = self.get(object_id)
        if consumed_by not in obj.used_by:
            obj.used_by.append(consumed_by)

    def mark_sanitized(self, object_id: str, note: str) -> None:
        obj = self.get(object_id)
        obj.sanitized = True
        obj.policy_notes.append(note)

    def get(self, object_id: str) -> ProvenanceObject:
        if object_id not in self._objects:
            raise KeyError(f"unknown provenance object_id '{object_id}'")
        return self._objects[object_id]

    def __len__(self) -> int:
        return len(self._objects)

    def __iter__(self):
        return iter(self._objects.values())
