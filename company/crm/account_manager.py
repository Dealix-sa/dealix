"""Dealix CRM — Account manager for Saudi B2B prospects."""

from __future__ import annotations

import json
import os
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

_DEFAULT_PATH = Path("company/runtime/crm/accounts.json")
_ACCOUNTS_PATH = Path(os.getenv("DEALIX_CRM_ACCOUNTS_PATH", str(_DEFAULT_PATH)))

VALID_TIERS = frozenset({"HOT", "WARM", "COOL", "COLD"})
VALID_STAGES = frozenset(
    {"prospect", "contacted", "qualified", "proposal_sent", "negotiation", "won", "lost"}
)


@dataclass
class AccountRecord:
    company_name: str
    sector: str
    size: str
    city: str
    pain_hypothesis: str
    score: int = 0
    tier: str = "COLD"
    status: str = "prospect"
    source_url: str = ""
    notes: str = ""
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    created_at: str = field(default_factory=lambda: datetime.now(UTC).isoformat())

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)


class AccountManager:
    """File-based CRM account manager. No external API calls, no sending."""

    def __init__(self, accounts_path: Path | None = None) -> None:
        self._path = accounts_path or _ACCOUNTS_PATH

    def _load(self) -> list[dict[str, Any]]:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        if not self._path.exists():
            return []
        with self._path.open("r", encoding="utf-8") as fh:
            data = json.load(fh)
        return data if isinstance(data, list) else []

    def _save(self, records: list[dict[str, Any]]) -> None:
        self._path.parent.mkdir(parents=True, exist_ok=True)
        with self._path.open("w", encoding="utf-8") as fh:
            json.dump(records, fh, ensure_ascii=False, indent=2)

    def add_account(self, record: AccountRecord) -> AccountRecord:
        """Persist a new account record. Returns the saved record."""
        records = self._load()
        records.append(record.to_dict())
        self._save(records)
        return record

    def get_all_accounts(self) -> list[dict[str, Any]]:
        """Return all stored account records."""
        return self._load()

    def get_hot_accounts(self) -> list[dict[str, Any]]:
        """Return accounts with tier == 'HOT'."""
        return [r for r in self._load() if r.get("tier") == "HOT"]

    def get_accounts_by_stage(self, stage: str) -> list[dict[str, Any]]:
        """Filter accounts by pipeline stage."""
        return [r for r in self._load() if r.get("status") == stage]

    def update_status(self, account_id: str, new_status: str) -> bool:
        """Update status field for the account matching account_id. Returns True if found."""
        records = self._load()
        for record in records:
            if record.get("id") == account_id:
                record["status"] = new_status
                self._save(records)
                return True
        return False

    def export_to_markdown(self, report_path: Path | None = None) -> str:
        """Generate markdown report of all accounts. Writes to reports/crm/accounts_report.md."""
        records = self._load()
        report_dir = Path("reports/crm")
        report_dir.mkdir(parents=True, exist_ok=True)
        dest = report_path or report_dir / "accounts_report.md"

        lines = [
            "# Dealix CRM — Accounts Report",
            f"Generated: {datetime.now(UTC).isoformat()}",
            f"Total accounts: {len(records)}",
            "",
        ]
        for tier in ("HOT", "WARM", "COOL", "COLD"):
            tier_records = [r for r in records if r.get("tier") == tier]
            if not tier_records:
                continue
            lines.append(f"## {tier} ({len(tier_records)})")
            for r in tier_records:
                lines.append(
                    f"- **{r.get('company_name')}** | {r.get('sector')} | "
                    f"{r.get('city')} | Score: {r.get('score')} | "
                    f"Stage: {r.get('status')}"
                )
            lines.append("")

        content = "\n".join(lines)
        dest.write_text(content, encoding="utf-8")
        return content
