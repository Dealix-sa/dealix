"""Contract for the tenant-scoped-query gate.

The gate is what stops the PDPL/ZATCA/jobs defect class from returning, so
it needs its own guard: a scanner that silently stops detecting is worse
than no scanner, because it reads as a green light.
"""

from __future__ import annotations

import importlib
import subprocess
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
SCRIPT = ROOT / "scripts/ops/check_tenant_scoped_queries.py"
BASELINE = ROOT / "scripts/ops/tenant_scoped_queries_baseline.txt"

sys.path.insert(0, str(ROOT))

UNSCOPED = """
from sqlalchemy import select
from db.models import ContactRecord


async def leak(contact_id, db):
    result = await db.execute(
        select(ContactRecord).where(ContactRecord.id == contact_id)
    )
    return result.scalar_one_or_none()
"""

SCOPED = """
from sqlalchemy import select
from db.models import ContactRecord


async def safe(contact_id, tenant_id, db):
    result = await db.execute(
        select(ContactRecord).where(
            ContactRecord.id == contact_id,
            ContactRecord.tenant_id == tenant_id,
        )
    )
    return result.scalar_one_or_none()
"""

# A filtered query must not vouch for an unfiltered one beside it.
MIXED = SCOPED + UNSCOPED


def _scan(source: str, tmp_path: Path) -> list[tuple[int, str]]:
    from scripts.ops.check_tenant_scoped_queries import scan_file, tenant_owned_models

    target = tmp_path / "probe.py"
    target.write_text(source, encoding="utf-8")
    return scan_file(target, tenant_owned_models())


def test_flags_a_query_filtered_only_by_id(tmp_path):
    findings = _scan(UNSCOPED, tmp_path)
    assert [model for _line, model in findings] == ["ContactRecord"]


def test_accepts_a_query_that_also_filters_on_tenant(tmp_path):
    assert _scan(SCOPED, tmp_path) == []


def test_a_scoped_query_does_not_excuse_an_unscoped_neighbour(tmp_path):
    findings = _scan(MIXED, tmp_path)
    assert len(findings) == 1, findings


def test_reports_each_query_once(tmp_path):
    """Nested blocks must not multiply a single finding."""
    nested = """
from sqlalchemy import select
from db.models import ContactRecord


async def leak(contact_id, db):
    async with db.begin():
        try:
            result = await db.execute(
                select(ContactRecord).where(ContactRecord.id == contact_id)
            )
        except Exception:
            return None
    return result.scalar_one_or_none()
"""
    assert len(_scan(nested, tmp_path)) == 1


def test_baseline_is_absent_or_carries_real_entries():
    """The backlog is cleared, so there should be no baseline file at all.

    An empty baseline is worse than none: it reads as "a ratchet is holding
    something back" when nothing is. If entries ever return, they must be
    real and point at their tracking issue.
    """
    if not BASELINE.is_file():
        return
    text = BASELINE.read_text(encoding="utf-8")
    entries = [
        line for line in text.splitlines() if line.strip() and not line.startswith("#")
    ]
    assert entries, "delete the baseline file rather than committing it empty"
    assert "#974" in text, "the baseline must point at the tracking issue"
    for entry in entries:
        assert "::" in entry, f"malformed baseline entry: {entry!r}"


def test_a_violation_fails_when_no_baseline_holds_it(tmp_path, monkeypatch):
    """With the backlog cleared, any finding must fail the gate outright."""
    gate = importlib.import_module("scripts.ops.check_tenant_scoped_queries")

    probe = tmp_path / "probe_router.py"
    probe.write_text(UNSCOPED, encoding="utf-8")
    monkeypatch.setattr(gate, "BASELINE_PATH", tmp_path / "absent_baseline.txt")
    monkeypatch.setattr(gate, "REPO_ROOT", tmp_path)

    assert gate.main(["check", str(probe)]) == 1


@pytest.mark.timeout(180)
def test_gate_passes_on_the_current_tree():
    """The committed baseline must match reality, or the gate is noise."""
    result = subprocess.run(
        [sys.executable, str(SCRIPT)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )
    assert result.returncode == 0, result.stdout + result.stderr
    assert "TENANT_SCOPED_QUERY_GATE=PASS" in result.stdout


def test_matrix_runs_the_gate_as_required():
    script = (ROOT / "scripts/ops/run_full_repo_test_matrix.sh").read_text(
        encoding="utf-8"
    )
    assert 'run_step "tenant-scoped-queries" required' in script


# ── A file the scanner cannot read has not been checked ───────────────────


def test_unparseable_file_raises_instead_of_being_skipped(tmp_path):
    """Silently skipping a file turns PASS into a claim about unread code.

    Four files under ``dealix/`` carried a UTF-8 BOM. Under plain ``utf-8``
    the BOM decodes to U+FEFF, ``ast.parse`` rejects it on line 1, and the
    scanner printed a warning and returned no findings — so the gate reported
    PASS over files it had never actually read.
    """
    from scripts.ops.check_tenant_scoped_queries import (
        UnparseableSource,
        scan_file,
        tenant_owned_models,
    )

    target = tmp_path / "broken.py"
    target.write_text("def (:\n", encoding="utf-8")

    with pytest.raises(UnparseableSource):
        scan_file(target, tenant_owned_models())


def test_byte_order_mark_does_not_hide_a_violation(tmp_path):
    """The exact shape that was being skipped: a BOM in front of real code."""
    from scripts.ops.check_tenant_scoped_queries import scan_file, tenant_owned_models

    target = tmp_path / "bom.py"
    target.write_bytes(b"\xef\xbb\xbf" + UNSCOPED.encode("utf-8"))

    findings = scan_file(target, tenant_owned_models())

    assert findings, "a BOM in front of the file hid an unscoped query"


def test_gate_fails_on_an_unparseable_file(tmp_path, monkeypatch):
    """End to end: an unreadable file must be a red gate, not a stderr note."""
    broken = tmp_path / "broken.py"
    broken.write_text("def (:\n", encoding="utf-8")

    proc = subprocess.run(
        [sys.executable, str(SCRIPT), str(broken)],
        capture_output=True,
        text=True,
        cwd=ROOT,
    )

    assert proc.returncode == 1, proc.stdout + proc.stderr
    assert "unparseable=1" in proc.stdout
    assert "TENANT_SCOPED_QUERY_GATE=FAIL" in proc.stdout


def test_no_tracked_python_file_carries_a_byte_order_mark():
    """Keeps the four stripped files from quietly coming back.

    A BOM also breaks other AST-based tooling, so this is worth holding
    repo-wide rather than only over the gate's own scan scope.
    """
    tracked = subprocess.run(
        ["git", "ls-files", "*.py"],
        capture_output=True,
        text=True,
        cwd=ROOT,
        check=True,
    ).stdout.split()

    with_bom = [
        name
        for name in tracked
        if (ROOT / name).exists() and (ROOT / name).read_bytes().startswith(b"\xef\xbb\xbf")
    ]

    assert not with_bom, f"UTF-8 BOM would hide these from AST tooling: {with_bom}"


# ── Scan scope ────────────────────────────────────────────────────────────


def test_scope_reaches_past_the_http_surface():
    """A request id does not stop being caller-controlled off the HTTP path.

    The gate began at ``api/routers`` alone. Widening it is what surfaced the
    cross-tenant write in ``core/memory/embedding_service.py``, which is
    reached through a background-job payload rather than a URL.
    """
    from scripts.ops.check_tenant_scoped_queries import DEFAULT_PATHS

    for required in ("api", "core", "dealix"):
        assert required in DEFAULT_PATHS, (
            f"{required!r} dropped from the scan scope — whole subsystems "
            f"would stop being checked without the gate ever going red"
        )


# ── session.get(Model, id) — the shape the rule above cannot see ───────────

UNGUARDED_GET = """
from db.models import ContactRecord


async def leak(contact_id, session):
    return await session.get(ContactRecord, contact_id)
"""

GUARDED_GET = """
from db.models import ContactRecord


async def safe(contact_id, tenant_id, session):
    contact = await session.get(ContactRecord, contact_id)
    if contact is None or contact.tenant_id != tenant_id:
        return None
    return contact
"""


def test_flags_an_unguarded_session_get(tmp_path):
    """`session.get(Model, id)` fetches by id with none of the select syntax.

    No `select()`, no `.where()` — so the original rule was blind to it, and
    20 call sites across the repo were never checked. It cannot carry a
    tenant predicate, so the check has to follow the call.
    """
    assert _scan(UNGUARDED_GET, tmp_path), "session.get by id was not flagged"


def test_accepts_a_session_get_followed_by_an_ownership_check(tmp_path):
    """The correct shape, as api/routers/billing.py:pay_invoice uses it."""
    assert not _scan(GUARDED_GET, tmp_path)


def test_session_get_on_an_untenanted_model_is_ignored(tmp_path):
    """The rule must stay narrow — a model with no tenant_id has no boundary."""
    source = """
from db.models import AccountRecord


async def fine(account_id, session):
    return await session.get(AccountRecord, account_id)
"""
    assert not _scan(source, tmp_path)
