"""Regression contract for duplicate Python dependency declarations."""

from __future__ import annotations

import collections
import pathlib
import re

import tomllib

PYPROJECT = pathlib.Path(__file__).resolve().parents[1] / "pyproject.toml"
REQUIREMENT_NAME = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*")


def _canonical_requirement_name(requirement: str) -> str:
    """Return the normalized distribution name from a PEP 508 requirement string."""
    match = REQUIREMENT_NAME.match(requirement.strip())
    assert match is not None, f"Invalid dependency declaration: {requirement!r}"
    return re.sub(r"[-_.]+", "-", match.group(0)).lower()


def _duplicate_requirement_names(requirements: list[str]) -> list[str]:
    names = [_canonical_requirement_name(requirement) for requirement in requirements]
    return sorted(name for name, count in collections.Counter(names).items() if count > 1)


def test_pyproject_dependency_groups_do_not_repeat_packages() -> None:
    """Each dependency group should declare a distribution at most once."""
    with PYPROJECT.open("rb") as handle:
        project = tomllib.load(handle)["project"]

    groups = {"project.dependencies": project.get("dependencies", [])}
    groups.update(
        {
            f"project.optional-dependencies.{name}": requirements
            for name, requirements in project.get("optional-dependencies", {}).items()
        }
    )

    duplicates = {
        group: repeated
        for group, requirements in groups.items()
        if (repeated := _duplicate_requirement_names(requirements))
    }

    assert not duplicates, f"Duplicate dependency declarations found: {duplicates}"
