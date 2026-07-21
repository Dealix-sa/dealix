"""Company-to-Client Communication Hub.

Approval-first communication management. NEVER auto-sends. No send() method
exists. All outbound paths call SendGate.assert_blocked() as defense-in-depth.
"""

from __future__ import annotations

import json
import logging
import threading
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any, Literal

from intelligence.bilingual import BilingualRenderer, BilingualText, LanguageCode
from intelligence.ops_adapters import get_price_book
from intelligence.send_gate import SendGate


class SendStatus(str, Enum):
    DRAFT = "draft"
    PENDING_APPROVAL = "pending_approval"
    APPROVED = "approved"
    SENT_EXTERNALLY = "sent_externally"  # log-only; set by human
    REJECTED = "rejected"


@dataclass
class ContactLogEntry:
    entry_id: str
    contact_id: str
    company_name: str
    contact_name: str
    channel: Literal["email", "whatsapp", "linkedin", "call", "meeting", "sms"]
    direction: Literal["outbound_draft", "inbound", "internal_note"]
    subject: BilingualText
    body: BilingualText
    status: SendStatus
    created_at: str
    approved_at: str | None
    approved_by: str | None
    rejection_reason: str | None
    policy_snapshot: dict[str, Any]
    tags: list[str]

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "entry_id": self.entry_id,
            "contact_id": self.contact_id,
            "company_name": self.company_name,
            "contact_name": self.contact_name,
            "channel": self.channel,
            "direction": self.direction,
            "subject": BilingualRenderer.filter_text(self.subject, lang),
            "body": BilingualRenderer.filter_text(self.body, lang),
            "status": self.status.value,
            "created_at": self.created_at,
            "approved_at": self.approved_at,
            "approved_by": self.approved_by,
            "rejection_reason": self.rejection_reason,
            "policy_snapshot": self.policy_snapshot,
            "tags": self.tags,
        }


@dataclass
class SequenceStep:
    step_number: int
    channel: str
    delay_days: int
    subject: BilingualText
    body: BilingualText
    status: SendStatus = field(default=SendStatus.DRAFT)

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "step_number": self.step_number,
            "channel": self.channel,
            "delay_days": self.delay_days,
            "subject": BilingualRenderer.filter_text(self.subject, lang),
            "body": BilingualRenderer.filter_text(self.body, lang),
            "status": self.status.value,
        }


@dataclass
class CommunicationSequence:
    sequence_id: str
    name: str
    contact_id: str
    company_name: str
    steps: list[SequenceStep]
    current_step: int = 0
    status: Literal["active", "paused", "completed"] = "active"

    def to_dict(self, lang: LanguageCode = "both") -> dict[str, Any]:
        return {
            "sequence_id": self.sequence_id,
            "name": self.name,
            "contact_id": self.contact_id,
            "company_name": self.company_name,
            "steps": [s.to_dict(lang) for s in self.steps],
            "current_step": self.current_step,
            "status": self.status,
        }


class CommunicationHub:
    """Approval-first communication management."""

    LOG_PATH = Path("data/comms/contact_log.json")
    SEQUENCE_PATH = Path("data/comms/sequences.json")
    _log_lock = threading.Lock()
    _seq_lock = threading.Lock()

    def __init__(self) -> None:
        self.LOG_PATH.parent.mkdir(parents=True, exist_ok=True)
        self._ensure_files()

    def _ensure_files(self) -> None:
        for path in (self.LOG_PATH, self.SEQUENCE_PATH):
            if not path.exists():
                path.write_text("[]", encoding="utf-8")

    def _read_json(self, path: Path) -> list[dict[str, Any]]:
        try:
            return json.loads(path.read_text(encoding="utf-8"))
        except Exception:
            return []

    def _write_json(self, path: Path, data: list[dict[str, Any]]) -> None:
        path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")

    def _bt_to_dict(self, text: BilingualText) -> dict[str, Any]:
        return {"en": text.en, "ar": text.ar, "ar_available": text.ar_available}

    def _dict_to_bt(self, raw: dict[str, Any]) -> BilingualText:
        return BilingualText(
            en=raw.get("en"),
            ar=raw.get("ar"),
            ar_available=raw.get("ar_available", True),
        )

    def _entry_to_dict(self, entry: ContactLogEntry) -> dict[str, Any]:
        data = asdict(entry)
        data["subject"] = self._bt_to_dict(entry.subject)
        data["body"] = self._bt_to_dict(entry.body)
        data["status"] = entry.status.value
        return data

    def _entry_from_dict(self, raw: dict[str, Any]) -> ContactLogEntry:
        return ContactLogEntry(
            entry_id=raw["entry_id"],
            contact_id=raw["contact_id"],
            company_name=raw["company_name"],
            contact_name=raw["contact_name"],
            channel=raw["channel"],
            direction=raw["direction"],
            subject=self._dict_to_bt(raw["subject"]),
            body=self._dict_to_bt(raw["body"]),
            status=SendStatus(raw.get("status", "draft")),
            created_at=raw["created_at"],
            approved_at=raw.get("approved_at"),
            approved_by=raw.get("approved_by"),
            rejection_reason=raw.get("rejection_reason"),
            policy_snapshot=raw.get("policy_snapshot", {}),
            tags=raw.get("tags", []),
        )

    def _policy_snapshot(self, body: BilingualText) -> dict[str, Any]:
        body_text = " ".join(filter(None, [body.en, body.ar]))
        flagged_prices = self._validate_no_prices_outside_catalog(body_text)
        return {
            "send_gate": "blocked",
            "price_validation": "pass" if not flagged_prices else "flagged",
            "flagged_price_mentions": flagged_prices,
            "review_required": True,
        }

    def _validate_no_prices_outside_catalog(self, content: str) -> list[str]:
        flagged: list[str] = []
        price_book = get_price_book()
        allowed_amounts = {
            str(int(v))
            for tiers in price_book.values()
            for v in tiers.values()
        }
        # Simple heuristic: look for SAR/ر.س/ريال followed by number
        import re
        matches = re.findall(r"(?:SAR|ر\.س|ريال)\s*([\d,]+)", content)
        for m in matches:
            amount = m.replace(",", "")
            if amount not in allowed_amounts:
                flagged.append(amount)
        return flagged

    def create_draft(
        self,
        contact_id: str,
        company_name: str,
        contact_name: str,
        channel: Literal["email", "whatsapp", "linkedin", "call", "meeting", "sms"],
        subject_en: str,
        subject_ar: str,
        body_en: str,
        body_ar: str,
        tags: list[str] | None = None,
    ) -> ContactLogEntry:
        SendGate.assert_blocked("create_draft_guard")
        subject = BilingualRenderer.bt(subject_en, subject_ar)
        body = BilingualRenderer.bt(body_en, body_ar)
        entry = ContactLogEntry(
            entry_id=f"msg-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            contact_id=contact_id,
            company_name=company_name,
            contact_name=contact_name,
            channel=channel,
            direction="outbound_draft",
            subject=subject,
            body=body,
            status=SendStatus.DRAFT,
            created_at=datetime.now(timezone.utc).isoformat(),
            approved_at=None,
            approved_by=None,
            rejection_reason=None,
            policy_snapshot=self._policy_snapshot(body),
            tags=tags or [],
        )
        data = self._read_json(self.LOG_PATH)
        data.append(self._entry_to_dict(entry))
        with self._log_lock:
            self._write_json(self.LOG_PATH, data)
        SendGate.audit_log("draft_created", actor="system", draft_id=entry.entry_id)
        return entry

    def _update_entry(
        self,
        entry_id: str,
        updater: Any,
    ) -> ContactLogEntry | None:
        data = self._read_json(self.LOG_PATH)
        for i, raw in enumerate(data):
            if raw.get("entry_id") == entry_id:
                entry = self._entry_from_dict(raw)
                updater(entry)
                data[i] = self._entry_to_dict(entry)
                with self._log_lock:
                    self._write_json(self.LOG_PATH, data)
                return entry
        return None

    def submit_for_approval(self, entry_id: str, actor: str) -> ContactLogEntry | None:
        def _set_pending(entry: ContactLogEntry) -> None:
            if entry.status != SendStatus.DRAFT:
                raise ValueError("Only drafts can be submitted for approval")
            entry.status = SendStatus.PENDING_APPROVAL
        result = self._update_entry(entry_id, _set_pending)
        if result:
            SendGate.audit_log("submitted_for_approval", actor=actor, draft_id=entry_id)
        return result

    def approve_draft(self, entry_id: str, approved_by: str) -> ContactLogEntry | None:
        def _set_approved(entry: ContactLogEntry) -> None:
            if entry.status not in (SendStatus.DRAFT, SendStatus.PENDING_APPROVAL):
                raise ValueError("Only draft or pending entries can be approved")
            entry.status = SendStatus.APPROVED
            entry.approved_at = datetime.now(timezone.utc).isoformat()
            entry.approved_by = approved_by
        result = self._update_entry(entry_id, _set_approved)
        if result:
            SendGate.audit_log("draft_approved", actor=approved_by, draft_id=entry_id)
        return result

    def reject_draft(self, entry_id: str, reason: str) -> ContactLogEntry | None:
        def _set_rejected(entry: ContactLogEntry) -> None:
            if entry.status not in (SendStatus.DRAFT, SendStatus.PENDING_APPROVAL):
                raise ValueError("Only draft or pending entries can be rejected")
            entry.status = SendStatus.REJECTED
            entry.rejection_reason = reason
        result = self._update_entry(entry_id, _set_rejected)
        if result:
            SendGate.audit_log("draft_rejected", actor="reviewer", draft_id=entry_id, metadata={"reason": reason})
        return result

    def mark_sent_externally(self, entry_id: str, actor: str) -> ContactLogEntry | None:
        def _set_sent(entry: ContactLogEntry) -> None:
            if entry.status != SendStatus.APPROVED:
                raise ValueError("Only approved entries can be marked as sent externally")
            entry.status = SendStatus.SENT_EXTERNALLY
        result = self._update_entry(entry_id, _set_sent)
        if result:
            SendGate.audit_log("marked_sent_externally", actor=actor, draft_id=entry_id)
        return result

    def log_inbound(
        self,
        contact_id: str,
        company_name: str,
        contact_name: str,
        channel: Literal["email", "whatsapp", "linkedin", "call", "meeting", "sms"],
        body_en: str,
        body_ar: str,
        tags: list[str] | None = None,
    ) -> ContactLogEntry:
        body = BilingualRenderer.bt(body_en, body_ar)
        entry = ContactLogEntry(
            entry_id=f"inbound-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            contact_id=contact_id,
            company_name=company_name,
            contact_name=contact_name,
            channel=channel,
            direction="inbound",
            subject=BilingualRenderer.bt("Inbound message", "رسالة واردة"),
            body=body,
            status=SendStatus.SENT_EXTERNALLY,
            created_at=datetime.now(timezone.utc).isoformat(),
            approved_at=None,
            approved_by=None,
            rejection_reason=None,
            policy_snapshot={"send_gate": "n/a", "review_required": False},
            tags=tags or [],
        )
        data = self._read_json(self.LOG_PATH)
        data.append(self._entry_to_dict(entry))
        with self._log_lock:
            self._write_json(self.LOG_PATH, data)
        return entry

    def get_contact_history(self, contact_id: str, lang: LanguageCode = "both") -> dict[str, Any]:
        entries = [self._entry_from_dict(raw) for raw in self._read_json(self.LOG_PATH) if raw.get("contact_id") == contact_id]
        return BilingualRenderer.wrap(
            {
                "contact_id": contact_id,
                "count": len(entries),
                "entries": [e.to_dict(lang) for e in sorted(entries, key=lambda x: x.created_at, reverse=True)],
            },
            lang,
        )

    def get_pending_approvals(self, lang: LanguageCode = "both") -> dict[str, Any]:
        entries = [
            self._entry_from_dict(raw)
            for raw in self._read_json(self.LOG_PATH)
            if raw.get("status") in (SendStatus.DRAFT.value, SendStatus.PENDING_APPROVAL.value)
        ]
        return BilingualRenderer.wrap(
            {
                "count": len(entries),
                "entries": [e.to_dict(lang) for e in entries],
            },
            lang,
        )

    def create_sequence(
        self,
        name: str,
        contact_id: str,
        company_name: str,
        steps: list[dict[str, Any]],
    ) -> CommunicationSequence:
        sequence = CommunicationSequence(
            sequence_id=f"seq-{datetime.now(timezone.utc).strftime('%Y%m%d%H%M%S')}",
            name=name,
            contact_id=contact_id,
            company_name=company_name,
            steps=[
                SequenceStep(
                    step_number=i + 1,
                    channel=s.get("channel", "email"),
                    delay_days=s.get("delay_days", 0),
                    subject=BilingualRenderer.bt(s["subject_en"], s["subject_ar"]),
                    body=BilingualRenderer.bt(s["body_en"], s["body_ar"]),
                )
                for i, s in enumerate(steps)
            ],
        )
        data = self._read_json(self.SEQUENCE_PATH)
        data.append({
            "sequence_id": sequence.sequence_id,
            "name": sequence.name,
            "contact_id": sequence.contact_id,
            "company_name": sequence.company_name,
            "steps": [self._step_to_dict(s) for s in sequence.steps],
            "current_step": sequence.current_step,
            "status": sequence.status,
        })
        with self._seq_lock:
            self._write_json(self.SEQUENCE_PATH, data)
        return sequence

    def _step_to_dict(self, step: SequenceStep) -> dict[str, Any]:
        data = asdict(step)
        data["subject"] = self._bt_to_dict(step.subject)
        data["body"] = self._bt_to_dict(step.body)
        data["status"] = step.status.value
        return data

    def _step_from_dict(self, raw: dict[str, Any]) -> SequenceStep:
        return SequenceStep(
            step_number=raw["step_number"],
            channel=raw["channel"],
            delay_days=raw["delay_days"],
            subject=self._dict_to_bt(raw["subject"]),
            body=self._dict_to_bt(raw["body"]),
            status=SendStatus(raw.get("status", "draft")),
        )

    def _load_sequence(self, sequence_id: str) -> CommunicationSequence | None:
        for raw in self._read_json(self.SEQUENCE_PATH):
            if raw.get("sequence_id") == sequence_id:
                return CommunicationSequence(
                    sequence_id=raw["sequence_id"],
                    name=raw["name"],
                    contact_id=raw["contact_id"],
                    company_name=raw["company_name"],
                    steps=[self._step_from_dict(s) for s in raw.get("steps", [])],
                    current_step=raw.get("current_step", 0),
                    status=raw.get("status", "active"),
                )
        return None

    def _save_sequence(self, sequence: CommunicationSequence) -> None:
        data = self._read_json(self.SEQUENCE_PATH)
        for i, raw in enumerate(data):
            if raw.get("sequence_id") == sequence.sequence_id:
                data[i] = {
                    "sequence_id": sequence.sequence_id,
                    "name": sequence.name,
                    "contact_id": sequence.contact_id,
                    "company_name": sequence.company_name,
                    "steps": [self._step_to_dict(s) for s in sequence.steps],
                    "current_step": sequence.current_step,
                    "status": sequence.status,
                }
                break
        with self._seq_lock:
            self._write_json(self.SEQUENCE_PATH, data)

    def advance_sequence(self, sequence_id: str, actor: str) -> dict[str, Any]:
        SendGate.assert_blocked("sequence_advance_guard")
        sequence = self._load_sequence(sequence_id)
        if not sequence:
            raise ValueError(f"Sequence {sequence_id} not found")
        if sequence.current_step >= len(sequence.steps):
            sequence.status = "completed"
            self._save_sequence(sequence)
            return BilingualRenderer.wrap({"sequence": sequence.to_dict(), "next_step": None}, "both")

        step = sequence.steps[sequence.current_step]
        step.status = SendStatus.PENDING_APPROVAL
        self._save_sequence(sequence)
        SendGate.audit_log("sequence_step_advanced", actor=actor, draft_id=sequence_id)
        return BilingualRenderer.wrap(
            {
                "sequence": sequence.to_dict(),
                "next_step": step.to_dict(),
                "note": "This step is a draft. Approve it before any external dispatch.",
            },
            "both",
        )

    def search_communications(self, query: str, limit: int = 20) -> dict[str, Any]:
        q = query.lower()
        entries = [self._entry_from_dict(raw) for raw in self._read_json(self.LOG_PATH)]
        results = [
            e for e in entries
            if q in (e.company_name or "").lower()
            or q in (e.contact_name or "").lower()
            or q in (e.body.en or "").lower()
            or q in (e.body.ar or "").lower()
        ]
        return BilingualRenderer.wrap(
            {
                "query": query,
                "count": len(results),
                "entries": [e.to_dict("both") for e in results[:limit]],
            },
            "both",
        )

    def stats(self) -> dict[str, Any]:
        entries = [self._entry_from_dict(raw) for raw in self._read_json(self.LOG_PATH)]
        status_counts: dict[str, int] = {}
        for e in entries:
            status_counts[e.status.value] = status_counts.get(e.status.value, 0) + 1
        return {
            "total_entries": len(entries),
            "status_counts": status_counts,
        }
