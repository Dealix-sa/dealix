"""Channel Report — generates daily omni-channel performance reports."""
from __future__ import annotations

import logging
from datetime import UTC, datetime
from typing import Any

from auto_client_acquisition.omni_channel_os.schemas import ChannelReport, DailyQuota

log = logging.getLogger(__name__)
_NO_AUTO_SEND = True


class ChannelReporter:
    """Generates daily omni-channel performance summaries."""

    _NO_AUTO_SEND = True

    def generate(self, result: Any, quota: DailyQuota) -> ChannelReport:
        """Generate a ChannelReport from a PipelineResult and DailyQuota."""
        by_channel: dict[str, int] = {}
        by_sector: dict[str, int] = {}
        by_country: dict[str, int] = {}

        for item in getattr(result, "founder_queue", []):
            ch = getattr(item, "best_channel", None)
            if ch:
                ch_val = ch.value if hasattr(ch, "value") else str(ch)
                by_channel[ch_val] = by_channel.get(ch_val, 0) + 1
            sec = getattr(item, "sector", None)
            if sec:
                by_sector[sec] = by_sector.get(sec, 0) + 1
            country = getattr(item, "country", None)
            if country:
                by_country[country] = by_country.get(country, 0) + 1

        for asset in getattr(result, "auto_queued", []):
            ch = getattr(asset, "channel", None)
            if ch:
                ch_val = ch.value if hasattr(ch, "value") else str(ch)
                by_channel[ch_val] = by_channel.get(ch_val, 0) + 1
            country = getattr(asset, "country", None)
            if country:
                by_country[country] = by_country.get(country, 0) + 1

        founder_queue_size = len(getattr(result, "founder_queue", []))
        auto_sent_count = len(getattr(result, "auto_queued", []))
        pending_approval_count = founder_queue_size

        top_actions: list[str] = []
        for item in getattr(result, "founder_queue", [])[:5]:
            top_actions.append(
                f"{getattr(item, 'company', '')} — "
                f"{getattr(item, 'best_channel', '').value if hasattr(getattr(item, 'best_channel', ''), 'value') else ''} "
                f"[{getattr(item, 'offer_name', '')}]"
            )

        return ChannelReport(
            date=quota.date,
            total_companies=getattr(result, "total_companies", 0),
            total_assets=getattr(result, "total_assets", 0),
            by_channel=by_channel,
            by_sector=by_sector,
            by_country=by_country,
            founder_queue_size=founder_queue_size,
            auto_sent_count=auto_sent_count,
            pending_approval_count=pending_approval_count,
            top_actions=top_actions,
        )

    def format_for_display(self, report: ChannelReport) -> str:
        """Format report as human-readable bilingual text."""
        lines = [
            f"=== Daily Omni-Channel Report / تقرير القناة اليومي ===",
            f"Date / التاريخ: {report.date}",
            f"Companies processed / الشركات: {report.total_companies}",
            f"Assets generated / الأصول: {report.total_assets}",
            f"Founder queue / قائمة المراجعة: {report.founder_queue_size}",
            f"Auto-queued / تلقائي: {report.auto_sent_count}",
            f"Pending approval / بانتظار الموافقة: {report.pending_approval_count}",
        ]
        if report.by_channel:
            lines.append("By channel / بالقناة:")
            for ch, count in sorted(report.by_channel.items(), key=lambda x: -x[1]):
                lines.append(f"  {ch}: {count}")
        if report.by_sector:
            lines.append("By sector / بالقطاع:")
            for sec, count in sorted(report.by_sector.items(), key=lambda x: -x[1]):
                lines.append(f"  {sec}: {count}")
        if report.top_actions:
            lines.append("Top actions / أبرز الإجراءات:")
            for action in report.top_actions:
                lines.append(f"  - {action}")
        return "\n".join(lines)

    def format_as_dict(self, report: ChannelReport) -> dict[str, Any]:
        """Format report as a JSON-serialisable dict."""
        return report.model_dump()

    def compare_to_previous(
        self,
        current: ChannelReport,
        previous: ChannelReport,
    ) -> dict[str, Any]:
        """Compare current vs previous day report — return deltas."""
        def _delta(a: int, b: int) -> str:
            diff = a - b
            return f"+{diff}" if diff >= 0 else str(diff)

        return {
            "date_current": current.date,
            "date_previous": previous.date,
            "companies_delta": _delta(current.total_companies, previous.total_companies),
            "assets_delta": _delta(current.total_assets, previous.total_assets),
            "founder_queue_delta": _delta(
                current.founder_queue_size, previous.founder_queue_size
            ),
            "auto_sent_delta": _delta(current.auto_sent_count, previous.auto_sent_count),
        }


__all__ = ["ChannelReporter"]
