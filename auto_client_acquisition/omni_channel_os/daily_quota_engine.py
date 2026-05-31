"""Daily Quota Engine — runs the daily 300+ company batch."""
from __future__ import annotations

import json
import logging
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

from auto_client_acquisition.omni_channel_os.schemas import Company, DailyQuota, FounderReviewItem

log = logging.getLogger(__name__)
_NO_AUTO_SEND = True

_DEFAULT_OUTPUT_DIR = Path("data/omni_channel_output")
_DEFAULT_QUEUE_FILE = Path("data/founder_review_queue_daily.jsonl")


class DailyQuotaEngine:
    """Runs the daily omni-channel batch. Loads companies, processes, saves output."""

    _NO_AUTO_SEND = True
    DEFAULT_DAILY_TARGET = 300

    def __init__(self) -> None:
        from auto_client_acquisition.omni_channel_os.orchestrator import OmniChannelOrchestrator

        self._orchestrator = OmniChannelOrchestrator()

    def run(
        self,
        companies: list[Company] | None = None,
        input_file: str | None = None,
        date: str | None = None,
    ) -> dict[str, Any]:
        """Run the daily quota. Returns a summary dict."""
        if date is None:
            date = datetime.now(UTC).strftime("%Y-%m-%d")

        if companies is None and input_file:
            companies = self._load_companies_from_file(input_file)
        if not companies:
            log.warning("daily_quota_engine.no_companies date=%s", date)
            return {
                "status": "no_companies",
                "date": date,
                "total_companies": 0,
                "total_assets": 0,
                "errors": [],
            }

        log.info(
            "daily_quota_engine.run_start date=%s company_count=%d",
            date,
            len(companies),
        )

        result = self._orchestrator.run_batch(companies, date=date)

        output_path = self._save_output(result, date)
        queue_path = self._save_founder_queue(result.founder_queue, date)

        summary: dict[str, Any] = {
            "status": "ok",
            "date": date,
            "total_companies": result.total_companies,
            "total_assets": result.total_assets,
            "founder_queue_size": len(result.founder_queue),
            "auto_queued_count": len(result.auto_queued),
            "errors": result.errors,
            "output_path": output_path,
            "queue_path": queue_path,
        }
        if result.quota:
            summary["quota"] = {
                "email_drafts_done": result.quota.email_drafts_done,
                "linkedin_drafts_done": result.quota.linkedin_drafts_done,
                "website_form_drafts_done": result.quota.website_form_drafts_done,
                "whatsapp_drafts_done": result.quota.whatsapp_drafts_done,
                "call_scripts_done": result.quota.call_scripts_done,
                "total_assets_done": result.quota.total_assets_done,
                "completion_pct": result.quota.completion_pct,
            }
        if result.report:
            from auto_client_acquisition.omni_channel_os.channel_report import ChannelReporter

            summary["report"] = ChannelReporter().format_as_dict(result.report)

        log.info(
            "daily_quota_engine.run_done date=%s companies=%d assets=%d errors=%d",
            date,
            result.total_companies,
            result.total_assets,
            len(result.errors),
        )
        return summary

    def _load_companies_from_file(self, path: str) -> list[Company]:
        """Load companies from a JSON or JSONL file."""
        file_path = Path(path)
        if not file_path.exists():
            log.warning("daily_quota_engine.input_file_missing path=%s", path)
            return []
        try:
            text = file_path.read_text(encoding="utf-8")
            if file_path.suffix == ".jsonl":
                return [
                    Company.model_validate_json(line)
                    for line in text.splitlines()
                    if line.strip()
                ]
            raw = json.loads(text)
            if isinstance(raw, list):
                return [Company.model_validate(c) for c in raw]
            return []
        except Exception as exc:
            log.warning("daily_quota_engine.load_failed path=%s error=%s", path, exc)
            return []

    def _save_output(self, result: Any, date: str) -> str:
        """Save pipeline result to JSON file. Returns the output path."""
        output_dir = _DEFAULT_OUTPUT_DIR
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            output_file = output_dir / f"batch_{date}.json"
            payload: dict[str, Any] = {
                "date": date,
                "total_companies": result.total_companies,
                "total_assets": result.total_assets,
                "errors": result.errors,
                "auto_queued_count": len(result.auto_queued),
                "founder_queue_count": len(result.founder_queue),
            }
            output_file.write_text(
                json.dumps(payload, ensure_ascii=False, indent=2),
                encoding="utf-8",
            )
            return str(output_file)
        except Exception as exc:
            log.warning("daily_quota_engine.save_output_failed date=%s error=%s", date, exc)
            return ""

    def _save_founder_queue(self, items: list[FounderReviewItem], date: str) -> str:
        """Save founder queue items to a JSONL file. Returns the path."""
        output_dir = _DEFAULT_OUTPUT_DIR
        try:
            output_dir.mkdir(parents=True, exist_ok=True)
            queue_file = output_dir / f"founder_queue_{date}.jsonl"
            with queue_file.open("w", encoding="utf-8") as fh:
                for item in items:
                    fh.write(item.model_dump_json() + "\n")
            return str(queue_file)
        except Exception as exc:
            log.warning(
                "daily_quota_engine.save_queue_failed date=%s error=%s", date, exc
            )
            return ""

    def get_today_summary(self) -> dict[str, Any]:
        """Load today's output file and return its summary."""
        today = datetime.now(UTC).strftime("%Y-%m-%d")
        output_file = _DEFAULT_OUTPUT_DIR / f"batch_{today}.json"
        if not output_file.exists():
            return {"status": "not_found", "date": today}
        try:
            return json.loads(output_file.read_text(encoding="utf-8"))
        except Exception as exc:
            return {"status": "read_error", "date": today, "error": str(exc)}

    def get_founder_actions(self, limit: int = 100) -> list[FounderReviewItem]:
        """Load today's top founder actions sorted by quality score."""
        today = datetime.now(UTC).strftime("%Y-%m-%d")
        queue_file = _DEFAULT_OUTPUT_DIR / f"founder_queue_{today}.jsonl"
        if not queue_file.exists():
            return []
        items: list[FounderReviewItem] = []
        try:
            for line in queue_file.read_text(encoding="utf-8").splitlines():
                line = line.strip()
                if line:
                    try:
                        items.append(FounderReviewItem.model_validate_json(line))
                    except Exception:
                        pass
        except Exception as exc:
            log.warning("daily_quota_engine.load_queue_failed error=%s", exc)
            return []
        items.sort(key=lambda x: x.quality_score, reverse=True)
        return items[:limit]


__all__ = ["DailyQuotaEngine"]
