"""Public repo must not contain private-ops top-level directories or marker files."""
from __future__ import annotations

from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent

# Directories whose mere existence at the public-repo root is a leak.
PRIVATE_TOP_LEVEL = {
    "founder", "pipeline", "weekly_reviews", "prompts",
    "people", "legal", "partners", "learning", "finance",
}
# `clients/` is allowed at the root if and only if it contains *only*
# templates and scaffolding (entries beginning with "_" or being a README).
PRIVATE_FILE_MARKERS = {
    "approval_log.csv", "suppression_list.csv", "claim_approval_log.csv",
    "export_log.csv", "mrr_tracker.csv", "cash_collected.csv",
}


def test_no_private_top_level_dirs():
    offenders = [name for name in PRIVATE_TOP_LEVEL if (REPO / name).exists()]
    assert not offenders, f"Private top-level dirs present in public repo: {offenders}"


def test_clients_dir_holds_only_templates():
    clients = REPO / "clients"
    if not clients.exists():
        return
    real_client_dirs = [
        p.name for p in clients.iterdir()
        if p.is_dir() and not p.name.startswith("_") and p.name.upper() != "README"
    ]
    assert not real_client_dirs, (
        f"clients/ should only hold templates/scaffolding in the public repo, "
        f"found: {real_client_dirs}"
    )


def test_no_private_marker_files():
    found: list[str] = []
    for p in REPO.rglob("*"):
        if not p.is_file():
            continue
        if ".git" in p.parts or "__pycache__" in p.parts:
            continue
        if p.name in PRIVATE_FILE_MARKERS:
            found.append(str(p.relative_to(REPO)))
    assert not found, f"Private marker files found in public repo: {found}"
