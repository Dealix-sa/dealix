"""Lead sourcing for the Commercial Growth OS.

Rules enforced here:
  * Only allowed source types are accepted.
  * Every account must carry a ``source_url`` — accounts without one are
    marked ``unverified`` and are *not send-ready*. We never invent data.
  * Client-provided CSV/JSON and allowed public contact pages are supported.

This module does not crawl the web; it ingests already-collected records
(client uploads or pre-approved public sources) and normalises them.
"""

from __future__ import annotations

import csv
import json
from pathlib import Path
from typing import Any, Iterable, Mapping

from app.commercial.schemas import CommercialAccount

ALLOWED_SOURCE_TYPES = (
    "client_provided",
    "public_website",
    "public_directory",
    "partner",
    "referral",
    "inbound_form",
)


class SourceValidationError(ValueError):
    """Raised when a record cannot be safely sourced."""


def _account_from_record(record: Mapping[str, Any]) -> CommercialAccount:
    return CommercialAccount(
        account_id=str(record.get("account_id") or record.get("id") or _slug(record)),
        company_name=str(record.get("company_name") or record.get("name") or "").strip(),
        sector=str(record.get("sector", "")).strip(),
        city=str(record.get("city", "")).strip(),
        website=str(record.get("website", "")).strip(),
        source_url=str(record.get("source_url", "")).strip(),
        source_type=str(record.get("source_type", "")).strip(),
        public_email=str(record.get("public_email", "")).strip(),
        whatsapp=str(record.get("whatsapp", "")).strip(),
        phone=str(record.get("phone", "")).strip(),
        linkedin_url=str(record.get("linkedin_url", "")).strip(),
        pain_hypothesis=str(record.get("pain_hypothesis", "")).strip(),
        recommended_motion=str(record.get("recommended_motion", "")).strip(),
        recommended_product=str(record.get("recommended_product", "")).strip(),
        owner=str(record.get("owner", "unassigned")).strip() or "unassigned",
        risk_level=str(record.get("risk_level", "medium")).strip() or "medium",
        whatsapp_opt_in=bool(record.get("whatsapp_opt_in", False)),
        email_opt_out=bool(record.get("email_opt_out", False)),
        contactability_status=str(record.get("contactability_status", "unknown")).strip()
        or "unknown",
    )


def _slug(record: Mapping[str, Any]) -> str:
    name = str(record.get("company_name") or record.get("name") or "acct")
    return "acct_" + "".join(c for c in name.lower() if c.isalnum())[:24]


def validate_source(account: CommercialAccount) -> CommercialAccount:
    """Set verification + contactability based on source quality.

    An account with no ``source_url`` stays ``unverified`` (and therefore not
    send-ready). One with an allowed source and a usable channel is marked
    ``verified``/``contactable`` — unless it has already opted out.
    """
    if not account.source_url:
        account.verification_status = "unverified"
        if account.contactability_status == "unknown":
            account.contactability_status = "blocked"
        return account

    if account.source_type and account.source_type not in ALLOWED_SOURCE_TYPES:
        account.verification_status = "rejected"
        account.contactability_status = "blocked"
        return account

    account.verification_status = "verified"
    if account.contactability_status in ("unknown", ""):
        has_channel = any(
            (account.public_email, account.whatsapp, account.phone, account.linkedin_url)
        )
        account.contactability_status = "contactable" if has_channel else "blocked"
    return account


def is_send_ready(account: CommercialAccount) -> bool:
    """An account is send-ready only if verified, sourced, and contactable."""
    return (
        bool(account.source_url)
        and account.verification_status == "verified"
        and account.contactability_status == "contactable"
        and not account.email_opt_out
    )


def load_accounts(records: Iterable[Mapping[str, Any]]) -> list[CommercialAccount]:
    """Build validated accounts from an iterable of raw dict records."""
    accounts: list[CommercialAccount] = []
    for rec in records:
        account = _account_from_record(rec)
        accounts.append(validate_source(account))
    return accounts


def load_accounts_from_json(path: str | Path) -> list[CommercialAccount]:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if isinstance(data, dict):
        data = data.get("accounts", [])
    return load_accounts(data)


def load_accounts_from_csv(path: str | Path) -> list[CommercialAccount]:
    with Path(path).open(encoding="utf-8", newline="") as fh:
        reader = csv.DictReader(fh)
        return load_accounts(list(reader))
