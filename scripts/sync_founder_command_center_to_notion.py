#!/usr/bin/env python3
"""Sync the Founder Command Center into Notion (transform -> upsert).

Write-only mirror of existing Dealix generators into the founder's Notion
workspace. Composes — never duplicates — business logic:

- Offers DB     <- service_catalog.registry.list_offerings
- KPI DB        <- value_os.value_ledger.summarize (one row per value tier)
- Proof/Capital <- capital_os.capital_ledger.list_assets
- Daily Ops +   <- scripts.dealix_founder_daily_brief.build_brief
  90-Day Plan
- Action queue  <- dealix.commercial_ops.founder_full_autopilot snapshot

Hard rules mirrored from the constitution:
- Article 4: outreach rows are written `draft_only` + `Approved? = false`;
  this sync NEVER reads approval back to trigger a send (write-only).
- Article 8: KPI numbers carry their value tier; nothing is presented as
  guaranteed revenue.
- PDPL / Doctrine #6: every string is redacted by the property builders in
  `integrations/notion.py` before it is placed in a payload.
- Code-generated demo CRM / proof rows are labeled `SAMPLE / عينة`.

Usage:
    NOTION_MOCK_MODE=true python scripts/sync_founder_command_center_to_notion.py --dry-run --json
"""

from __future__ import annotations

import argparse
import asyncio
import json
import re
import sys
from datetime import UTC, datetime
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
if str(REPO_ROOT) not in sys.path:
    sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.capital_os.capital_ledger import list_assets  # noqa: E402
from auto_client_acquisition.service_catalog.registry import list_offerings  # noqa: E402
from auto_client_acquisition.value_os.value_ledger import summarize  # noqa: E402
from core.logging import get_logger  # noqa: E402
from dealix.commercial_ops.stdio_utf8 import ensure_stdout_utf8  # noqa: E402
from integrations.notion import (  # noqa: E402
    NotionClient,
    checkbox_prop,
    date_prop,
    number_prop,
    rich_text_prop,
    select_prop,
    title_prop,
)
from scripts.dealix_founder_daily_brief import build_brief  # noqa: E402

logger = get_logger(__name__)

SAMPLE_SOURCE = "SAMPLE / عينة"
OUTREACH_GOVERNANCE_STATUS = "draft_only — awaiting approval"
# Aggregate KPI summary key (no real tenant data leaves the process).
_KPI_CUSTOMER_ID = "__founder_aggregate__"


def _slug(text: str) -> str:
    """Deterministic ascii slug for external ids."""
    out = re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")
    return out or "row"


def _today() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


# ── Row builders (every value flows through redacting property builders) ──
def _offer_row(offering: Any) -> tuple[str, dict[str, Any]]:
    external_id = f"offer-{offering.id}"
    props = {
        "Name": title_prop(offering.name_en),
        "Name (AR)": rich_text_prop(offering.name_ar),
        "Price SAR": number_prop(offering.price_sar),
        "Price Unit": select_prop(offering.price_unit),
        "Journey Stage": select_prop(str(offering.customer_journey_stage)),
        "Duration Days": number_prop(offering.duration_days),
        "KPI Commitment": rich_text_prop(offering.kpi_commitment_en),
        "Source": select_prop("CATALOG / كتالوج"),
    }
    return external_id, props


def _kpi_rows(summary: dict[str, float], *, period: str) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any]]] = []
    for tier, amount in summary.items():
        external_id = f"kpi-{_slug(tier)}-{period}"
        props = {
            "Metric": title_prop(f"value_{tier}"),
            "Tier": select_prop(tier),
            "Amount SAR": number_prop(float(amount)),
            "Period": select_prop(period),
            "Is Estimate": checkbox_prop(True),
            "Source": select_prop("VALUE_LEDGER / سجل القيمة"),
        }
        rows.append((external_id, props))
    return rows


def _capital_row(asset: Any) -> tuple[str, dict[str, Any]]:
    external_id = f"cap-{asset.asset_id}"
    props = {
        "Asset": title_prop(asset.asset_type),
        "Asset Ref": rich_text_prop(asset.asset_ref or ""),
        "Owner": rich_text_prop(asset.owner or ""),
        "Reusable": checkbox_prop(bool(asset.reusable)),
        "Created": date_prop(asset.created_at or _today()),
        "Source": select_prop("CAPITAL_LEDGER / سجل رأس المال"),
    }
    return external_id, props


def _sample_proof_row() -> tuple[str, dict[str, Any]]:
    """A single illustrative proof row when the capital ledger is empty.

    MUST be labeled as a sample so a founder never mistakes it for a real,
    consented proof asset.
    """
    external_id = "cap-sample-proof"
    props = {
        "Asset": title_prop("Sample reusable proof asset"),
        "Asset Ref": rich_text_prop("(illustrative — replace with consented asset)"),
        "Owner": rich_text_prop(""),
        "Reusable": checkbox_prop(True),
        "Created": date_prop(_today()),
        "Source": select_prop(SAMPLE_SOURCE),
    }
    return external_id, props


def _daily_ops_rows(brief: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    date = brief.get("date") or _today()
    action = brief.get("next_founder_action") or {}
    bottleneck = brief.get("bottleneck") or {}
    rows: list[tuple[str, dict[str, Any]]] = []

    title_en = action.get("en") or "Today's single action"
    external_id = f"dailyops-{date}-{_slug(title_en)[:40]}"
    rows.append(
        (
            external_id,
            {
                "Action": title_prop(title_en),
                "Action (AR)": rich_text_prop(action.get("ar") or ""),
                "Rationale": rich_text_prop(action.get("en") or ""),
                "Severity": select_prop(str(bottleneck.get("severity") or "unknown")),
                "Date": date_prop(date),
                "Is Estimate": checkbox_prop(bool(brief.get("is_estimate", True))),
                "Source": select_prop("DAILY_BRIEF / الموجز اليومي"),
            },
        )
    )
    return rows


def _plan_rows(brief: dict[str, Any]) -> list[tuple[str, dict[str, Any]]]:
    """90-Day Plan rows derived from the brief's hard-gate posture."""
    rows: list[tuple[str, dict[str, Any]]] = []
    gates = brief.get("hard_gates") or []
    phase = "guardrails"
    for gate in gates:
        external_id = f"plan-{phase}-{_slug(str(gate))}"
        rows.append(
            (
                external_id,
                {
                    "Item": title_prop(str(gate)),
                    "Phase": select_prop(phase),
                    "State": select_prop("immutable"),
                    "Source": select_prop("HARD_GATES / الحواجز"),
                },
            )
        )
    return rows


def _action_queue_rows(queue: list[dict[str, Any]]) -> list[tuple[str, dict[str, Any]]]:
    rows: list[tuple[str, dict[str, Any]]] = []
    for item in queue:
        title_ar = str(item.get("title_ar") or "")
        priority = str(item.get("priority") or "")
        external_id = f"queue-{_slug(priority)}-{_slug(title_ar)[:40]}"
        rows.append(
            (
                external_id,
                {
                    "Task": title_prop(title_ar),
                    "Priority": select_prop(priority),
                    "Command": rich_text_prop(str(item.get("command") or "")),
                    "Kind": select_prop(str(item.get("kind") or "")),
                    "Blocking": checkbox_prop(bool(item.get("blocking"))),
                    "Source": select_prop("AUTOPILOT / الطيار"),
                },
            )
        )
    return rows


def _outreach_row(
    *, external_id: str, title: str, body: str, channel: str = "email"
) -> tuple[str, dict[str, Any]]:
    """Outreach rows are ALWAYS draft-only and unapproved (Article 4 / Doctrine #8).

    The sync is write-only: it never reads `Approved?` back to trigger a send.
    """
    props = {
        "Subject": title_prop(title),
        "Body": rich_text_prop(body),
        "Channel": select_prop(channel),
        "Governance status": select_prop(OUTREACH_GOVERNANCE_STATUS),
        "Approved?": checkbox_prop(False),
        "Source": select_prop("OUTREACH / تواصل"),
    }
    return external_id, props


# ── Orchestration ───────────────────────────────────────────────────
async def _maybe_upsert(
    client: NotionClient,
    db_id: str | None,
    external_id: str,
    properties: dict[str, Any],
    *,
    dry_run: bool,
) -> dict[str, Any]:
    """Upsert one row unless dry-run or the target DB id is unset."""
    if dry_run or db_id is None:
        logger.info(
            "notion_sync_skip",
            reason="dry_run" if dry_run else "db_id_unset",
            external_id=external_id,
        )
        return {"external_id": external_id, "skipped": True, "written": False}
    result = await client.upsert_row(db_id, external_id=external_id, properties=properties)
    return {
        "external_id": external_id,
        "skipped": False,
        "written": bool(result.success),
        "created": result.created,
        "mock": result.mock,
        "error": result.error,
    }


async def sync(*, dry_run: bool) -> dict[str, Any]:
    """Transform every source into Notion rows and (optionally) upsert them."""
    client = NotionClient()
    settings = client.settings
    results: dict[str, Any] = {
        "dry_run": dry_run,
        "mock": client.mock,
        "configured": client.configured,
        "generated_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "rows": {},
    }

    async def _section(name: str, db_id: str | None, rows: list[tuple[str, dict[str, Any]]]) -> None:
        out = []
        for external_id, props in rows:
            out.append(
                await _maybe_upsert(client, db_id, external_id, props, dry_run=dry_run)
            )
        results["rows"][name] = out

    # Offers
    await _section(
        "offers",
        settings.notion_offers_db_id,
        [_offer_row(o) for o in list_offerings()],
    )

    # KPIs (one row per value tier) — aggregate, no tenant PII.
    period = f"{_today()}-30d"
    await _section(
        "kpis",
        settings.notion_kpi_db_id,
        _kpi_rows(summarize(customer_id=_KPI_CUSTOMER_ID), period=period),
    )

    # Proof / Capital — real assets if present, else a labeled SAMPLE row.
    assets = list_assets(customer_id=None)
    proof_rows = [_capital_row(a) for a in assets] or [_sample_proof_row()]
    await _section("proof", settings.notion_proof_db_id, proof_rows)

    # Daily Ops + 90-Day Plan from the founder brief.
    brief = build_brief()
    await _section("daily_ops", settings.notion_daily_ops_db_id, _daily_ops_rows(brief))
    await _section("plan", settings.notion_plan_db_id, _plan_rows(brief))

    # Action queue from the autopilot snapshot (skip gracefully if absent).
    queue_rows: list[tuple[str, dict[str, Any]]] = []
    try:
        from dealix.commercial_ops.founder_full_autopilot import build_autopilot_snapshot

        snap = build_autopilot_snapshot()
        queue_rows = _action_queue_rows(snap.get("queue") or [])
    except Exception as exc:  # pragma: no cover - defensive: optional source
        logger.info("notion_sync_autopilot_unavailable", error=str(exc))
    await _section("action_queue", settings.notion_daily_ops_db_id, queue_rows)

    results["status"] = _verdict(results)
    return results


def _verdict(results: dict[str, Any]) -> str:
    """OK when nothing errored, PARTIAL otherwise."""
    for section in results.get("rows", {}).values():
        for row in section:
            if row.get("error"):
                return "PARTIAL"
    return "OK"


def _logs_to_stderr() -> None:
    """Route structured logs to stderr so `--json` keeps stdout machine-clean."""
    import structlog

    structlog.configure(logger_factory=structlog.PrintLoggerFactory(file=sys.stderr))


def main() -> int:
    ensure_stdout_utf8()
    _logs_to_stderr()
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument("--dry-run", action="store_true", help="Transform only; never write.")
    p.add_argument("--json", action="store_true", help="Emit the full results dict as JSON.")
    args = p.parse_args()

    results = asyncio.run(sync(dry_run=args.dry_run))

    if args.json:
        print(json.dumps(results, ensure_ascii=False, indent=2))
    else:
        print("== Founder Notion Command Center Sync ==")
        print(f"  dry_run: {results['dry_run']}  mock: {results['mock']}")
        for name, rows in results["rows"].items():
            written = sum(1 for r in rows if r.get("written"))
            skipped = sum(1 for r in rows if r.get("skipped"))
            print(f"  {name}: {len(rows)} rows ({written} written, {skipped} skipped)")

    status = results.get("status", "OK")
    print(f"FOUNDER_NOTION_SYNC={status}")
    return 0 if status == "OK" else 1


if __name__ == "__main__":
    raise SystemExit(main())
