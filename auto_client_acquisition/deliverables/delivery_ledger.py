"""Append-only ledger writer for the payment->delivery audit link.

Two writers, one per ledger in ``docs/ledgers/``:

  - ``record_delivery_kickoff`` appends a dated row to ``DELIVERY_LEDGER.md``
    when a confirmed payment kicks off delivery. This is the audit link
    between a payment and its delivery.
  - ``record_proof_pack_finalized`` appends a dated row to
    ``PROOF_LEDGER.md`` when a Proof Pack deliverable is finalized.

Both are append-only and dated. They degrade gracefully — if the ledgers
directory is not writable they return False rather than raising, so the
payment state machine is never blocked by a ledger I/O failure.
"""

from __future__ import annotations

from datetime import UTC, datetime

from auto_client_acquisition.runtime_paths import resolve_ledgers_dir

_KICKOFF_HEADER = "## Delivery kickoff log (append-only)"
_PROOF_HEADER = "## Proof Pack finalized log (append-only)"


def _today() -> str:
    return datetime.now(UTC).strftime("%Y-%m-%d")


def _append_log_line(*, ledger_filename: str, header: str, line: str) -> bool:
    """Append ``line`` under a named append-only section of a ledger file.

    Returns True on success, False when the ledger is unavailable/unwritable
    (callers must not let a ledger failure block the operation).
    """
    ledger_path = resolve_ledgers_dir() / ledger_filename
    try:
        existing = ledger_path.read_text(encoding="utf-8") if ledger_path.exists() else ""
        parts: list[str] = []
        if existing and not existing.endswith("\n"):
            existing += "\n"
        if header not in existing:
            parts.append("\n" + header + "\n")
        parts.append(line + "\n")
        with open(ledger_path, "a", encoding="utf-8") as fh:
            fh.write("".join(parts))
        return True
    except OSError:
        return False


def record_delivery_kickoff(
    *,
    payment_id: str,
    delivery_kickoff_id: str,
    customer_handle: str,
    amount_sar: float | None = None,
) -> bool:
    """Record a delivery-kickoff event to ``DELIVERY_LEDGER.md`` (append-only).

    The ``delivery_kickoff_id`` is the audit link between the confirmed
    payment and the delivery work that follows it.
    """
    amount = f"{amount_sar:g} SAR" if amount_sar is not None else "—"
    line = (
        f"- {_today()} | kickoff `{delivery_kickoff_id}` | "
        f"payment `{payment_id}` | customer `{customer_handle}` | {amount}"
    )
    return _append_log_line(
        ledger_filename="DELIVERY_LEDGER.md",
        header=_KICKOFF_HEADER,
        line=line,
    )


def record_proof_pack_finalized(
    *,
    deliverable_id: str,
    customer_handle: str,
    proof_event_id: str | None = None,
    score: int | None = None,
    tier: str = "",
) -> bool:
    """Record a finalized Proof Pack to ``PROOF_LEDGER.md`` (append-only)."""
    score_str = f"{score}/100" if score is not None else "—"
    line = (
        f"- {_today()} | proof pack `{deliverable_id}` | "
        f"customer `{customer_handle}` | proof_event `{proof_event_id or '—'}` | "
        f"score {score_str} | tier {tier or '—'}"
    )
    return _append_log_line(
        ledger_filename="PROOF_LEDGER.md",
        header=_PROOF_HEADER,
        line=line,
    )


__all__ = [
    "record_delivery_kickoff",
    "record_proof_pack_finalized",
]
