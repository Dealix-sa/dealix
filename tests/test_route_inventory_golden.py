"""The routing table may only change on purpose.

Consolidation work — collapsing duplicate implementations, retiring dead
packages, moving routers between domain aggregators — all carries the same
risk: quietly dropping a route something depends on. This test turns that
risk into a reviewable diff.

When a route change is intended:

    python3 scripts/generate_route_inventory.py

and put the added/removed list in the pull request body. A diff nobody can
explain is a regression, not a refresh.
"""

from __future__ import annotations

import pytest

from tests.support.route_inventory import (
    build_inventory,
    diff_inventories,
    load_golden,
)


@pytest.fixture(scope="module")
def current_inventory():
    from api.main import app

    return build_inventory(app)


@pytest.fixture(scope="module")
def golden_inventory():
    return load_golden()


def test_no_route_added_or_removed_without_regenerating_golden(
    current_inventory, golden_inventory
):
    added, removed = diff_inventories(golden_inventory, current_inventory)

    assert not added and not removed, (
        "The routing table changed.\n"
        f"  added ({len(added)}): {added[:20]}\n"
        f"  removed ({len(removed)}): {removed[:20]}\n"
        "If intended, run: python3 scripts/generate_route_inventory.py "
        "and list the change in the PR body."
    )


def test_shadowed_route_count_does_not_grow(current_inventory, golden_inventory):
    """FastAPI serves the first match, so a duplicate (path, method) is dead code.

    Six such pairs already exist. They are pinned rather than fixed here so
    that consolidation can only reduce the count — a new one is a new defect.
    """
    current = current_inventory["shadowed_count"]
    baseline = golden_inventory["shadowed_count"]

    assert current <= baseline, (
        f"Shadowed routes grew from {baseline} to {current}. "
        "A duplicate (path, method) registration is unreachable. "
        f"Current: {current_inventory['shadowed']}"
    )


def test_golden_matches_reported_counts(golden_inventory):
    """Guard against a hand-edited golden file."""
    routes = golden_inventory["routes"]
    assert golden_inventory["route_count"] == len(routes)
    assert golden_inventory["path_method_count"] == sum(
        len(methods) for methods in routes.values()
    )
    assert golden_inventory["shadowed_count"] == len(golden_inventory["shadowed"])
