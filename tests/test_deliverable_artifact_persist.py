"""save_rendered_artifact — persist a rendered deliverable to disk.

When a rung 0-1 deliverable is rendered, the HTML must be written to a
real file and the record's artifact_uri set, so the `delivered`
transition references an actual artifact. I/O failure degrades to None.
"""

from __future__ import annotations

import pytest

from auto_client_acquisition.deliverables import (
    render_deliverable_html,
    save_rendered_artifact,
)
from auto_client_acquisition.deliverables.store import (
    create_deliverable,
    get_deliverable,
    reset_for_test,
)


@pytest.fixture(autouse=True)
def _isolate_deliverables_dir(tmp_path, monkeypatch):
    monkeypatch.setenv("DEALIX_DELIVERABLES_DIR", str(tmp_path / "deliverables"))
    reset_for_test()
    yield
    reset_for_test()


def _make_diagnostic():
    return create_deliverable(
        session_id="sess_1",
        customer_handle="Slot-A",
        type="diagnostic_report",
        title_ar="تشخيص",
        title_en="Diagnostic",
        persist=False,
    )


def test_save_writes_file_and_sets_artifact_uri(tmp_path):
    rec = _make_diagnostic()
    html = render_deliverable_html(
        deliverable_type=rec.type, content={"context": "x"}, customer_handle="Slot-A"
    )
    uri = save_rendered_artifact(rec, html)

    assert uri is not None
    assert uri.endswith(".html")
    from pathlib import Path

    assert Path(uri).is_file()
    assert Path(uri).read_text(encoding="utf-8") == html
    # The record now references the real file.
    assert rec.artifact_uri == uri
    assert get_deliverable(rec.deliverable_id).artifact_uri == uri


def test_save_filename_is_path_safe():
    rec = _make_diagnostic()
    uri = save_rendered_artifact(rec, "<html></html>")
    assert uri is not None
    # deliverable_id is hex-suffixed; the type prefixes the filename.
    assert "diagnostic_report_" in uri


def test_save_degrades_gracefully_on_io_failure(monkeypatch):
    rec = _make_diagnostic()

    def _boom(*_a, **_k):
        raise OSError("disk full")

    monkeypatch.setattr("pathlib.Path.write_text", _boom)
    uri = save_rendered_artifact(rec, "<html></html>")
    assert uri is None  # never raises — rendering still succeeds
