"""V11 — central runtime path resolver.

Modules that read repo-shipped files (``docs/registry/*.yaml``,
``docs/SEO_AUDIT_REPORT.json``, etc.) must work in three deploy modes:

1. **Local checkout** — ``Path(__file__).parents[N] / "docs" / ...``
2. **Docker image** — ``docs/`` is shipped at the image root after the
   ``.dockerignore`` patch; the same relative path resolves
3. **Override** — operator sets ``DEALIX_REGISTRY_DIR`` to point at a
   bundled artifact dir (used by smoke tests + emergency rollback)

When the registry dir is missing, callers should report **degraded**
status with a 200 response — never 5xx. This module gives them a clean
detection primitive (``resolve_registry_dir`` + ``registry_dir_exists``)
so the failure surface is explicit.
"""
from __future__ import annotations

import os
from pathlib import Path

# 3 levels up from this file: auto_client_acquisition/runtime_paths.py
# → auto_client_acquisition → repo root.
_REPO_ROOT = Path(__file__).resolve().parent.parent


def resolve_repo_root() -> Path:
    """The repository root (or the equivalent at runtime)."""
    return _REPO_ROOT


def resolve_registry_dir() -> Path:
    """Return the canonical ``docs/registry`` path.

    Resolution order:
      1. ``DEALIX_REGISTRY_DIR`` env override (absolute path)
      2. Repo-relative ``docs/registry`` (development + Docker image)

    The returned path may NOT exist — callers should check
    ``.exists()`` and degrade gracefully.
    """
    override = os.getenv("DEALIX_REGISTRY_DIR")
    if override:
        return Path(override)
    return _REPO_ROOT / "docs" / "registry"


def registry_dir_exists() -> bool:
    return resolve_registry_dir().exists()


def resolve_seo_audit_report() -> Path:
    """Path to ``docs/SEO_AUDIT_REPORT.json``."""
    return _REPO_ROOT / "docs" / "SEO_AUDIT_REPORT.json"


def resolve_proof_events_dir() -> Path:
    """Path to ``docs/proof-events/`` — created on demand by ledger writers."""
    return _REPO_ROOT / "docs" / "proof-events"


def resolve_phase_e_dir() -> Path:
    """Path to ``docs/phase-e/`` — V11 customer execution kit."""
    return _REPO_ROOT / "docs" / "phase-e"


def resolve_ledgers_dir() -> Path:
    """Path to ``docs/ledgers/`` — the append-only audit ledgers.

    Resolution order:
      1. ``DEALIX_LEDGERS_DIR`` env override (absolute path — use when
         ``docs/`` is read-only in the deploy image)
      2. Repo-relative ``docs/ledgers``.

    Callers must degrade gracefully if the directory is not writable.
    """
    override = os.getenv("DEALIX_LEDGERS_DIR")
    if override:
        return Path(override)
    return _REPO_ROOT / "docs" / "ledgers"


def resolve_proposals_dir() -> Path:
    """Path where generated proposal artifacts (HTML) are written.

    Resolution order:
      1. ``DEALIX_PROPOSALS_DIR`` env override (absolute, writable path —
         use this when ``docs/`` is read-only in the deploy image)
      2. Repo-relative ``docs/proposals`` — created on demand.

    Callers must ``mkdir(parents=True, exist_ok=True)`` and degrade
    gracefully if the directory is not writable.
    """
    override = os.getenv("DEALIX_PROPOSALS_DIR")
    if override:
        return Path(override)
    return _REPO_ROOT / "docs" / "proposals"


def resolve_deliverables_dir() -> Path:
    """Path where rendered rung 0-1 deliverable artifacts (HTML) are written.

    Resolution order:
      1. ``DEALIX_DELIVERABLES_DIR`` env override (absolute, writable path —
         use when ``docs/`` is read-only in the deploy image)
      2. Repo-relative ``docs/deliverables`` — created on demand.

    Callers must ``mkdir(parents=True, exist_ok=True)`` and degrade
    gracefully if the directory is not writable.
    """
    override = os.getenv("DEALIX_DELIVERABLES_DIR")
    if override:
        return Path(override)
    return _REPO_ROOT / "docs" / "deliverables"


__all__ = [
    "registry_dir_exists",
    "resolve_deliverables_dir",
    "resolve_ledgers_dir",
    "resolve_phase_e_dir",
    "resolve_proof_events_dir",
    "resolve_proposals_dir",
    "resolve_registry_dir",
    "resolve_repo_root",
    "resolve_seo_audit_report",
]
