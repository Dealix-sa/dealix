"""Contract for the tenant-scoped-query gate.

The gate is what stops the PDPL/ZATCA/jobs defect class from returning, so
it needs its own guard: a scanner that silently stops detecting is worse
than no scanner, because it reads as a green light.
"""

from __future__ import annotations

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


def test_baseline_exists_and_is_documented():
    assert BASELINE.is_file(), "the ratchet needs its baseline committed"
    text = BASELINE.read_text(encoding="utf-8")
    assert "#974" in text, "the baseline must point at the tracking issue"
    entries = [
        line for line in text.splitlines() if line.strip() and not line.startswith("#")
    ]
    assert entries, "an empty baseline should be deleted, not committed"
    for entry in entries:
        assert "::" in entry, f"malformed baseline entry: {entry!r}"


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
