"""Shared repository-walk scope for Dealix scanners.

Both security smoke gates (``scripts/security_smoke.py`` and
``scripts/ops/security_smoke_ci.py``) need the same answer to one question:
which files in this tree are Dealix-authored and therefore worth scanning?

They previously each answered it with their own hand-maintained set of
directory names, and both sets carried the same two defects:

  1. Virtualenvs were excluded by name (``.venv``/``venv``), so a venv under
     any other name was walked into and credential-shaped strings inside
     installed third-party packages were reported as leaked secrets.
  2. Nested paths such as ``reports/runtime`` were stored in a set matched
     against single path components, so those exclusions never fired.

The mechanism lives here so it is fixed once. The *policy* — which directory
names a given scanner excludes — stays with each caller, because the two gates
deliberately differ (only the CI gate skips ``.github``; the standalone gate
scans workflow files for hardcoded credentials).
"""

from __future__ import annotations

import os
from collections.abc import Iterable, Iterator
from pathlib import Path

# Pruned for every scanner: none of these contain Dealix-authored source, so a
# match inside them is noise rather than signal.
VENDORED_DIR_NAMES = frozenset(
    {
        "__pycache__",
        "dist-packages",
        "site-packages",
    }
)


def is_virtualenv(directory: Path) -> bool:
    """Detect a Python virtualenv by its marker file rather than by name.

    ``pyvenv.cfg`` is written by ``venv``/``virtualenv`` regardless of the
    directory name, so this catches ``.venv-audit``, ``venv312``, ``env39``
    and anything else a developer or CI job happens to create.
    """
    return (directory / "pyvenv.cfg").is_file()


def is_pruned_dir(
    directory: Path,
    rel: str,
    skip_dir_names: Iterable[str],
    skip_path_prefixes: tuple[str, ...] = (),
) -> bool:
    """Return True when ``directory`` must not be descended into.

    ``rel`` is the directory's repo-relative POSIX path, which is what makes
    nested prefixes like ``reports/runtime`` match correctly — a plain name
    lookup can never see them.
    """
    name = directory.name
    if name in VENDORED_DIR_NAMES or name in skip_dir_names:
        return True
    if name.endswith(".egg-info"):
        return True
    if skip_path_prefixes and rel.startswith(skip_path_prefixes):
        return True
    return is_virtualenv(directory)


def iter_candidate_files(
    root: Path,
    skip_dir_names: Iterable[str],
    skip_path_prefixes: tuple[str, ...] = (),
) -> Iterator[Path]:
    """Yield every file under ``root``, pruning excluded directories.

    Pruning during the walk rather than filtering afterwards means excluded
    trees are never descended, so a large ``node_modules`` or virtualenv costs
    nothing instead of being enumerated and then discarded.
    """
    skip_names = frozenset(skip_dir_names)
    for dirpath, dirnames, filenames in os.walk(root):
        current = Path(dirpath)
        rel_dir = current.relative_to(root).as_posix()
        kept: list[str] = []
        for name in sorted(dirnames):
            child_rel = name if rel_dir == "." else f"{rel_dir}/{name}"
            if not is_pruned_dir(current / name, child_rel, skip_names, skip_path_prefixes):
                kept.append(name)
        dirnames[:] = kept
        for name in sorted(filenames):
            yield current / name
