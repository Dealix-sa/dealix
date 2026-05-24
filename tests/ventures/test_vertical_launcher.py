"""Tests for `dealix.ventures.vertical_launcher.VerticalLauncher`."""

from __future__ import annotations

import pytest

from dealix.ventures.vertical_launcher import (
    VerticalCard,
    VerticalLauncher,
)


def test_seeded_launcher_contains_clinics_and_real_estate_cards() -> None:
    launcher = VerticalLauncher()
    cards = {c.vertical for c in launcher.all()}
    assert "clinics" in cards
    assert "real_estate_brokers" in cards


def test_register_custom_vertical_card() -> None:
    launcher = VerticalLauncher()
    card = VerticalCard(
        vertical="retail_chains",
        buyer="Retail multi-store operator",
        pain="Stock visibility gaps",
        offer_name="Retail Visibility Sprint",
        price_band_sar=(8000, 16000),
        delivery_window_days=21,
        success_metric="Stock visibility 95 %+ across stores",
        exit_criteria=["Stock data refuses to flow", "Store managers veto rollout"],
        sami_kill_trigger="2 stores stop reporting before day 21",
    )
    launcher.register(card)
    assert launcher.get("retail_chains").offer_name == "Retail Visibility Sprint"


def test_get_unknown_raises_key_error() -> None:
    launcher = VerticalLauncher()
    with pytest.raises(KeyError):
        launcher.get("ferrets")


def test_invalid_price_band_rejected() -> None:
    with pytest.raises(ValueError):
        VerticalCard(
            vertical="x",
            buyer="x",
            pain="x",
            offer_name="x",
            price_band_sar=(10000, 5000),  # inverted
            delivery_window_days=10,
            success_metric="x",
            exit_criteria=["x"],
            sami_kill_trigger="x",
        )
