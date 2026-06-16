"""Storage backends for outbound data: Postgres (preferred) and CSV (fallback)."""

from __future__ import annotations

import csv
import json
import os
import uuid
from abc import ABC, abstractmethod
from collections.abc import Sequence
from datetime import datetime
from pathlib import Path
from typing import Any

from app.outbound.models import (
    Channel,
    DealPipeline,
    MessageStatus,
    OutboundContact,
    OutboundEvent,
    OutboundMessage,
    PipelineStage,
    SuppressionEntry,
)


class OutboundStorage(ABC):
    """Abstract storage for outbound entities."""

    @abstractmethod
    def save_contact(self, contact: OutboundContact) -> OutboundContact:
        ...

    @abstractmethod
    def get_contact(self, contact_id: str) -> OutboundContact | None:
        ...

    @abstractmethod
    def save_message(self, message: OutboundMessage) -> OutboundMessage:
        ...

    @abstractmethod
    def get_message(self, message_id: str) -> OutboundMessage | None:
        ...

    @abstractmethod
    def save_event(self, event: OutboundEvent) -> OutboundEvent:
        ...

    @abstractmethod
    def add_suppression(self, entry: SuppressionEntry) -> SuppressionEntry:
        ...

    @abstractmethod
    def is_suppressed(self, channel: Channel, value: str) -> bool:
        ...

    @abstractmethod
    def save_pipeline(self, deal: DealPipeline) -> DealPipeline:
        ...

    @abstractmethod
    def list_messages(
        self,
        status: MessageStatus | None = None,
        channel: Channel | None = None,
        limit: int = 1000,
    ) -> Sequence[OutboundMessage]:
        ...


class CSVOutboundStorage(OutboundStorage):
    """Simple CSV-backed storage for local dev and quick starts."""

    def __init__(self, base_dir: str | Path = "data/outbound") -> None:
        self.base_dir = Path(base_dir)
        self.base_dir.mkdir(parents=True, exist_ok=True)
        self._contacts_path = self.base_dir / "contacts.csv"
        self._messages_path = self.base_dir / "messages.csv"
        self._events_path = self.base_dir / "events.csv"
        self._suppression_path = self.base_dir / "suppression_list.csv"
        self._pipeline_path = self.base_dir / "deals_pipeline.csv"
        self._ensure_headers()

    def _ensure_headers(self) -> None:
        files_headers = {
            self._contacts_path: [
                "id", "company_name", "contact_name", "email", "phone", "whatsapp",
                "sector", "city", "website", "source_url", "verification_status",
                "confidence", "pain_hypothesis", "dealix_angle", "email_opt_out",
                "whatsapp_opt_in", "whatsapp_opt_out", "consent_source", "consent_timestamp",
                "created_at",
            ],
            self._messages_path: [
                "id", "contact_id", "channel", "status", "subject", "body", "template_name",
                "provider_message_id", "error_message", "approved_by", "approved_at",
                "queued_at", "sent_at", "replied_at", "created_at",
            ],
            self._events_path: ["id", "message_id", "event_type", "payload", "created_at"],
            self._suppression_path: ["id", "channel", "value", "reason", "created_at"],
            self._pipeline_path: [
                "id", "contact_id", "stage", "value_sar", "next_action", "next_action_at",
                "owner", "created_at",
            ],
        }
        for path, headers in files_headers.items():
            if not path.exists():
                with path.open("w", newline="", encoding="utf-8") as f:
                    writer = csv.writer(f)
                    writer.writerow(headers)

    def _read_rows(self, path: Path) -> list[dict[str, str]]:
        if not path.exists():
            return []
        with path.open("r", encoding="utf-8", newline="") as f:
            return list(csv.DictReader(f))

    def _write_rows(self, path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
        with path.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            writer.writerows(rows)

    def _to_iso(self, dt: datetime | None) -> str:
        return dt.isoformat() if dt else ""

    def _parse_iso(self, value: str) -> datetime | None:
        return datetime.fromisoformat(value) if value else None

    def save_contact(self, contact: OutboundContact) -> OutboundContact:
        rows = self._read_rows(self._contacts_path)
        rows = [r for r in rows if r["id"] != contact.id]
        rows.append({
            "id": contact.id,
            "company_name": contact.company_name,
            "contact_name": contact.contact_name or "",
            "email": contact.email or "",
            "phone": contact.phone or "",
            "whatsapp": contact.whatsapp or "",
            "sector": contact.sector or "",
            "city": contact.city or "",
            "website": contact.website or "",
            "source_url": contact.source_url,
            "verification_status": contact.verification_status,
            "confidence": contact.confidence,
            "pain_hypothesis": contact.pain_hypothesis or "",
            "dealix_angle": contact.dealix_angle or "",
            "email_opt_out": str(contact.email_opt_out),
            "whatsapp_opt_in": str(contact.whatsapp_opt_in),
            "whatsapp_opt_out": str(contact.whatsapp_opt_out),
            "consent_source": contact.consent_source or "",
            "consent_timestamp": self._to_iso(contact.consent_timestamp),
            "created_at": self._to_iso(contact.created_at),
        })
        self._write_rows(self._contacts_path, rows, rows[0].keys())
        return contact

    def get_contact(self, contact_id: str) -> OutboundContact | None:
        for row in self._read_rows(self._contacts_path):
            if row["id"] == contact_id:
                return OutboundContact(
                    id=row["id"],
                    company_name=row["company_name"],
                    contact_name=row["contact_name"] or None,
                    email=row["email"] or None,
                    phone=row["phone"] or None,
                    whatsapp=row["whatsapp"] or None,
                    sector=row["sector"] or None,
                    city=row["city"] or None,
                    website=row["website"] or None,
                    source_url=row["source_url"],
                    verification_status=row["verification_status"],
                    confidence=row["confidence"],
                    pain_hypothesis=row["pain_hypothesis"] or None,
                    dealix_angle=row["dealix_angle"] or None,
                    email_opt_out=row["email_opt_out"].lower() == "true",
                    whatsapp_opt_in=row["whatsapp_opt_in"].lower() == "true",
                    whatsapp_opt_out=row["whatsapp_opt_out"].lower() == "true",
                    consent_source=row["consent_source"] or None,
                    consent_timestamp=self._parse_iso(row["consent_timestamp"]),
                    created_at=self._parse_iso(row["created_at"]) or datetime.utcnow(),
                )
        return None

    def save_message(self, message: OutboundMessage) -> OutboundMessage:
        rows = self._read_rows(self._messages_path)
        rows = [r for r in rows if r["id"] != message.id]
        rows.append({
            "id": message.id,
            "contact_id": message.contact_id,
            "channel": message.channel,
            "status": message.status,
            "subject": message.subject or "",
            "body": message.body,
            "template_name": message.template_name or "",
            "provider_message_id": message.provider_message_id or "",
            "error_message": message.error_message or "",
            "approved_by": message.approved_by or "",
            "approved_at": self._to_iso(message.approved_at),
            "queued_at": self._to_iso(message.queued_at),
            "sent_at": self._to_iso(message.sent_at),
            "replied_at": self._to_iso(message.replied_at),
            "created_at": self._to_iso(message.created_at),
        })
        self._write_rows(self._messages_path, rows, rows[0].keys())
        return message

    def get_message(self, message_id: str) -> OutboundMessage | None:
        for row in self._read_rows(self._messages_path):
            if row["id"] == message_id:
                return OutboundMessage(
                    id=row["id"],
                    contact_id=row["contact_id"],
                    channel=row["channel"],
                    status=row["status"],
                    subject=row["subject"] or None,
                    body=row["body"],
                    template_name=row["template_name"] or None,
                    provider_message_id=row["provider_message_id"] or None,
                    error_message=row["error_message"] or None,
                    approved_by=row["approved_by"] or None,
                    approved_at=self._parse_iso(row["approved_at"]),
                    queued_at=self._parse_iso(row["queued_at"]),
                    sent_at=self._parse_iso(row["sent_at"]),
                    replied_at=self._parse_iso(row["replied_at"]),
                    created_at=self._parse_iso(row["created_at"]) or datetime.utcnow(),
                )
        return None

    def save_event(self, event: OutboundEvent) -> OutboundEvent:
        rows = self._read_rows(self._events_path)
        rows.append({
            "id": event.id,
            "message_id": event.message_id,
            "event_type": event.event_type,
            "payload": json.dumps(event.payload, ensure_ascii=False),
            "created_at": self._to_iso(event.created_at),
        })
        self._write_rows(self._events_path, rows, ["id", "message_id", "event_type", "payload", "created_at"])
        return event

    def add_suppression(self, entry: SuppressionEntry) -> SuppressionEntry:
        rows = self._read_rows(self._suppression_path)
        rows = [r for r in rows if not (r["channel"] == entry.channel and r["value"] == entry.value)]
        rows.append({
            "id": entry.id,
            "channel": entry.channel,
            "value": entry.value,
            "reason": entry.reason,
            "created_at": self._to_iso(entry.created_at),
        })
        self._write_rows(self._suppression_path, rows, ["id", "channel", "value", "reason", "created_at"])
        return entry

    def is_suppressed(self, channel: Channel, value: str) -> bool:
        for row in self._read_rows(self._suppression_path):
            if row["channel"] == channel and row["value"] == value:
                return True
        return False

    def save_pipeline(self, deal: DealPipeline) -> DealPipeline:
        rows = self._read_rows(self._pipeline_path)
        rows = [r for r in rows if r["id"] != deal.id]
        rows.append({
            "id": deal.id,
            "contact_id": deal.contact_id,
            "stage": deal.stage,
            "value_sar": str(deal.value_sar),
            "next_action": deal.next_action or "",
            "next_action_at": self._to_iso(deal.next_action_at),
            "owner": deal.owner,
            "created_at": self._to_iso(deal.created_at),
        })
        self._write_rows(self._pipeline_path, rows, rows[0].keys())
        return deal

    def list_messages(
        self,
        status: MessageStatus | None = None,
        channel: Channel | None = None,
        limit: int = 1000,
    ) -> Sequence[OutboundMessage]:
        results = []
        for row in self._read_rows(self._messages_path):
            msg = self.get_message(row["id"])
            if msg is None:
                continue
            if status and msg.status != status:
                continue
            if channel and msg.channel != channel:
                continue
            results.append(msg)
            if len(results) >= limit:
                break
        return results


class PostgresOutboundStorage(OutboundStorage):
    """Postgres-backed storage using SQLAlchemy models.

    This is a thin wrapper so the outbound runner stays storage-agnostic.
    """

    def __init__(self, session_factory: Any) -> None:
        self.session_factory = session_factory

    def save_contact(self, contact: OutboundContact) -> OutboundContact:
        # Not implemented in this scaffold; CSV is the default quick-start path.
        raise NotImplementedError("Postgres storage requires SQLAlchemy wiring")

    def get_contact(self, contact_id: str) -> OutboundContact | None:
        raise NotImplementedError("Postgres storage requires SQLAlchemy wiring")

    def save_message(self, message: OutboundMessage) -> OutboundMessage:
        raise NotImplementedError("Postgres storage requires SQLAlchemy wiring")

    def get_message(self, message_id: str) -> OutboundMessage | None:
        raise NotImplementedError("Postgres storage requires SQLAlchemy wiring")

    def save_event(self, event: OutboundEvent) -> OutboundEvent:
        raise NotImplementedError("Postgres storage requires SQLAlchemy wiring")

    def add_suppression(self, entry: SuppressionEntry) -> SuppressionEntry:
        raise NotImplementedError("Postgres storage requires SQLAlchemy wiring")

    def is_suppressed(self, channel: Channel, value: str) -> bool:
        raise NotImplementedError("Postgres storage requires SQLAlchemy wiring")

    def save_pipeline(self, deal: DealPipeline) -> DealPipeline:
        raise NotImplementedError("Postgres storage requires SQLAlchemy wiring")

    def list_messages(
        self,
        status: MessageStatus | None = None,
        channel: Channel | None = None,
        limit: int = 1000,
    ) -> Sequence[OutboundMessage]:
        raise NotImplementedError("Postgres storage requires SQLAlchemy wiring")


def get_default_storage() -> OutboundStorage:
    """Return the best available storage backend."""
    if os.getenv("DATABASE_URL") and os.getenv("OUTBOUND_USE_POSTGRES") == "1":
        # Postgres path is intentionally simple here; CSV is the default quick-start.
        return PostgresOutboundStorage(None)
    return CSVOutboundStorage()
