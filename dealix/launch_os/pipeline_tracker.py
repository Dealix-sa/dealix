"""Sales pipeline tracker backed by a JSONL file.

Follows the JSONL-store pattern from ``value_os/value_ledger.py``:
  - env var ``DEALIX_PIPELINE_PATH`` overrides the default path
  - default path: ``var/pipeline.jsonl``
  - thread-safe file writes

Stages (in order):
    RESEARCH -> OUTREACH -> DISCOVERY -> PROPOSAL -> NEGOTIATION -> WON -> LOST

The stage list aligns with the ``sales_pipeline_item.schema.json`` enum
(simplified to 7 stages for the operational tracker; the full schema is used
for data export).
"""
from __future__ import annotations

import json
import os
import threading
import uuid
from dataclasses import asdict, dataclass, field
from datetime import UTC, datetime
from pathlib import Path
from typing import Any


class PipelineStage:
    """Stage constants for the pipeline tracker.

    Examples:
        >>> PipelineStage.RESEARCH
        'RESEARCH'
        >>> PipelineStage.WON
        'WON'
        >>> "RESEARCH" in PipelineStage.ALL
        True
    """

    RESEARCH = "RESEARCH"
    OUTREACH = "OUTREACH"
    DISCOVERY = "DISCOVERY"
    PROPOSAL = "PROPOSAL"
    NEGOTIATION = "NEGOTIATION"
    WON = "WON"
    LOST = "LOST"

    ALL: list[str] = [
        RESEARCH,
        OUTREACH,
        DISCOVERY,
        PROPOSAL,
        NEGOTIATION,
        WON,
        LOST,
    ]


_STAGE_SET: frozenset[str] = frozenset(PipelineStage.ALL)


@dataclass
class PipelineItem:
    """A single deal in the sales pipeline.

    Attributes:
        id:              UUID-based deal identifier (auto-generated).
        account_name:    Human-readable company name.
        stage:           Current pipeline stage from :class:`PipelineStage`.
        offer_id:        Canonical offer identifier.
        value_sar:       Estimated deal value in SAR (0 = unknown).
        icp_score:       ICP total score at time of entry.
        last_touch_date: ISO date of last outreach/contact.
        next_action:     Free-text description of the next step.
        owner_notes:     Internal notes (not sent to client).

    Examples:
        >>> item = PipelineItem(
        ...     id="deal_001",
        ...     account_name="Acme Motors",
        ...     stage="RESEARCH",
        ...     offer_id="REVENUE_LEAK_AUDIT",
        ...     value_sar=15000,
        ...     icp_score=72,
        ...     last_touch_date="2026-06-01",
        ...     next_action="Send initial outreach email",
        ... )
        >>> item.stage
        'RESEARCH'
        >>> item.account_name
        'Acme Motors'
    """

    id: str
    account_name: str
    stage: str
    offer_id: str = ""
    value_sar: int = 0
    icp_score: int = 0
    last_touch_date: str = ""
    next_action: str = ""
    owner_notes: str = ""

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict[str, Any]) -> PipelineItem:
        return cls(
            id=str(data.get("id", "")),
            account_name=str(data.get("account_name", "")),
            stage=str(data.get("stage", PipelineStage.RESEARCH)),
            offer_id=str(data.get("offer_id", "")),
            value_sar=int(data.get("value_sar", 0)),
            icp_score=int(data.get("icp_score", 0)),
            last_touch_date=str(data.get("last_touch_date", "")),
            next_action=str(data.get("next_action", "")),
            owner_notes=str(data.get("owner_notes", "")),
        )


def _pipeline_path() -> Path:
    raw = os.environ.get("DEALIX_PIPELINE_PATH", "var/pipeline.jsonl")
    path = Path(raw)
    if not path.is_absolute():
        path = Path(__file__).resolve().parent.parent.parent / path
    path.parent.mkdir(parents=True, exist_ok=True)
    return path


class PipelineTracker:
    """In-memory pipeline backed by a JSONL file.

    Args:
        path: Override the storage path (useful for tests).

    Examples:
        >>> import tempfile, os
        >>> with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        ...     tmp = f.name
        >>> tracker = PipelineTracker(path=tmp)
        >>> item = tracker.add(
        ...     "Test Co",
        ...     "REVENUE_LEAK_AUDIT",
        ...     value_sar=10000,
        ...     icp_score=65,
        ...     next_action="Send intro email",
        ... )
        >>> item.stage
        'RESEARCH'
        >>> tracker.update_stage(item.id, "OUTREACH")
        >>> tracker.get(item.id).stage
        'OUTREACH'
        >>> summary = tracker.pipeline_summary()
        >>> summary["total_deals"]
        1
        >>> os.unlink(tmp)
    """

    def __init__(self, path: str | Path | None = None) -> None:
        self._path = Path(path) if path else _pipeline_path()
        self._path.parent.mkdir(parents=True, exist_ok=True)
        self._lock = threading.Lock()
        self._items: dict[str, PipelineItem] = {}
        self._load()

    def _load(self) -> None:
        if not self._path.exists():
            return
        content = self._path.read_text(encoding="utf-8").strip()
        if not content:
            return
        # Support both JSONL (line-per-item) and a single JSON array.
        if content.startswith("["):
            try:
                records = json.loads(content)
                if isinstance(records, list):
                    for data in records:
                        if isinstance(data, dict):
                            try:
                                item = PipelineItem.from_dict(data)
                                self._items[item.id] = item
                            except (KeyError, TypeError):
                                pass
                return
            except json.JSONDecodeError:
                pass
        for line in content.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                data = json.loads(line)
                item = PipelineItem.from_dict(data)
                self._items[item.id] = item
            except (json.JSONDecodeError, KeyError, TypeError):
                pass

    def _save(self) -> None:
        with self._path.open("w", encoding="utf-8") as fh:
            for item in self._items.values():
                fh.write(json.dumps(item.to_dict(), ensure_ascii=False) + "\n")

    def add(
        self,
        account_name: str,
        offer_id: str = "",
        value_sar: int = 0,
        icp_score: int = 0,
        next_action: str = "",
        owner_notes: str = "",
        stage: str = PipelineStage.RESEARCH,
    ) -> PipelineItem:
        """Add a new deal to the pipeline.

        Args:
            account_name: Company display name.
            offer_id:     Canonical offer identifier.
            value_sar:    Estimated value in SAR.
            icp_score:    ICP score from :func:`~dealix.launch_os.icp_scorer.score_account`.
            next_action:  Immediate next step.
            owner_notes:  Internal notes.
            stage:        Starting stage (default RESEARCH).

        Returns:
            The newly created :class:`PipelineItem`.

        Raises:
            ValueError: If ``stage`` is not a valid stage.

        Examples:
            >>> import tempfile, os
            >>> with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            ...     tmp = f.name
            >>> t = PipelineTracker(path=tmp)
            >>> item = t.add("Acme", "REVENUE_LEAK_AUDIT", value_sar=10000)
            >>> item.account_name
            'Acme'
            >>> item.stage
            'RESEARCH'
            >>> os.unlink(tmp)
        """
        if stage not in _STAGE_SET:
            raise ValueError(f"Invalid stage: {stage!r}. Must be one of {PipelineStage.ALL}")
        item = PipelineItem(
            id=f"deal_{uuid.uuid4().hex[:10]}",
            account_name=account_name,
            stage=stage,
            offer_id=offer_id,
            value_sar=value_sar,
            icp_score=icp_score,
            last_touch_date=datetime.now(UTC).date().isoformat(),
            next_action=next_action,
            owner_notes=owner_notes,
        )
        with self._lock:
            self._items[item.id] = item
            self._save()
        return item

    def get(self, deal_id: str) -> PipelineItem:
        """Retrieve a deal by ID.

        Raises:
            KeyError: If deal_id is not found.

        Examples:
            >>> import tempfile, os
            >>> with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            ...     tmp = f.name
            >>> t = PipelineTracker(path=tmp)
            >>> item = t.add("Test", "REVENUE_LEAK_AUDIT")
            >>> t.get(item.id).account_name
            'Test'
            >>> os.unlink(tmp)
        """
        if deal_id not in self._items:
            raise KeyError(f"Deal {deal_id!r} not found in pipeline")
        return self._items[deal_id]

    def update_stage(
        self,
        deal_id: str,
        new_stage: str,
        next_action: str = "",
        owner_notes: str = "",
    ) -> PipelineItem:
        """Move a deal to a new stage.

        Args:
            deal_id:     Existing deal identifier.
            new_stage:   Target stage from :class:`PipelineStage`.
            next_action: Updated next step (optional).
            owner_notes: Updated notes (optional).

        Returns:
            Updated :class:`PipelineItem`.

        Raises:
            KeyError:   If deal_id not found.
            ValueError: If new_stage is not valid.

        Examples:
            >>> import tempfile, os
            >>> with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            ...     tmp = f.name
            >>> t = PipelineTracker(path=tmp)
            >>> item = t.add("Acme", "REVENUE_LEAK_AUDIT")
            >>> updated = t.update_stage(item.id, "OUTREACH")
            >>> updated.stage
            'OUTREACH'
            >>> os.unlink(tmp)
        """
        if new_stage not in _STAGE_SET:
            raise ValueError(f"Invalid stage: {new_stage!r}. Must be one of {PipelineStage.ALL}")
        with self._lock:
            if deal_id not in self._items:
                raise KeyError(f"Deal {deal_id!r} not found in pipeline")
            item = self._items[deal_id]
            self._items[deal_id] = PipelineItem(
                id=item.id,
                account_name=item.account_name,
                stage=new_stage,
                offer_id=item.offer_id,
                value_sar=item.value_sar,
                icp_score=item.icp_score,
                last_touch_date=datetime.now(UTC).date().isoformat(),
                next_action=next_action or item.next_action,
                owner_notes=owner_notes or item.owner_notes,
            )
            self._save()
        return self._items[deal_id]

    def list_all(self) -> list[PipelineItem]:
        """Return all pipeline items sorted by icp_score descending.

        Examples:
            >>> import tempfile, os
            >>> with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            ...     tmp = f.name
            >>> t = PipelineTracker(path=tmp)
            >>> t.list_all()
            []
            >>> os.unlink(tmp)
        """
        return sorted(self._items.values(), key=lambda i: i.icp_score, reverse=True)

    def list_by_stage(self, stage: str) -> list[PipelineItem]:
        """Return all items in a specific stage.

        Examples:
            >>> import tempfile, os
            >>> with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            ...     tmp = f.name
            >>> t = PipelineTracker(path=tmp)
            >>> _ = t.add("A", "REVENUE_LEAK_AUDIT", stage=PipelineStage.RESEARCH)
            >>> len(t.list_by_stage(PipelineStage.RESEARCH))
            1
            >>> os.unlink(tmp)
        """
        return [i for i in self._items.values() if i.stage == stage]

    def pipeline_summary(self) -> dict[str, Any]:
        """Return counts and ARR by stage.

        Returns:
            Dict with keys ``total_deals``, ``total_arr_sar``,
            ``by_stage`` (dict of stage -> count) and
            ``arr_by_stage`` (dict of stage -> sum_sar).

        Examples:
            >>> import tempfile, os
            >>> with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
            ...     tmp = f.name
            >>> t = PipelineTracker(path=tmp)
            >>> summary = t.pipeline_summary()
            >>> summary["total_deals"]
            0
            >>> summary["total_arr_sar"]
            0
            >>> isinstance(summary["by_stage"], dict)
            True
            >>> os.unlink(tmp)
        """
        by_stage: dict[str, int] = {s: 0 for s in PipelineStage.ALL}
        arr_by_stage: dict[str, int] = {s: 0 for s in PipelineStage.ALL}
        total_arr = 0

        for item in self._items.values():
            stage = item.stage if item.stage in by_stage else PipelineStage.RESEARCH
            by_stage[stage] += 1
            arr_by_stage[stage] += item.value_sar
            total_arr += item.value_sar

        return {
            "total_deals": len(self._items),
            "total_arr_sar": total_arr,
            "by_stage": by_stage,
            "arr_by_stage": arr_by_stage,
        }


if __name__ == "__main__":
    import doctest
    results = doctest.testmod(verbose=False)
    print(f"Pipeline tracker doctests: {results.attempted} run, {results.failed} failed")

    import tempfile
    with tempfile.NamedTemporaryFile(suffix=".jsonl", delete=False) as f:
        tmp = f.name

    tracker = PipelineTracker(path=tmp)
    i1 = tracker.add("Acme Motors", "REVENUE_LEAK_AUDIT", value_sar=15000, icp_score=82)
    i2 = tracker.add("Global Realty", "SALES_COMMAND_CENTER", value_sar=25000, icp_score=70)
    tracker.update_stage(i1.id, "OUTREACH")
    summary = tracker.pipeline_summary()
    print(f"Pipeline: {summary['total_deals']} deals, {summary['total_arr_sar']:,} SAR pipeline")
    print(f"By stage: {summary['by_stage']}")
    os.unlink(tmp)
