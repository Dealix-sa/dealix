"""Tests for Sprint Day-3 account ranking (data_os.account_ranker)."""

from __future__ import annotations

import pytest

from auto_client_acquisition.data_os.account_ranker import (
    DEFAULT_TOP_N,
    ICPProfile,
    RankedAccount,
    rank_accounts,
)


def _row(**kwargs: object) -> dict[str, object]:
    base: dict[str, object] = {
        "company_name": "Acme",
        "sector": "fintech",
        "city": "Riyadh",
        "source": "crm_export",
    }
    base.update(kwargs)
    return base


def test_rank_returns_at_most_top_n() -> None:
    rows = [_row(company_name=f"Co{i}") for i in range(15)]
    result = rank_accounts(rows, top_n=5)
    assert len(result) == 5
    assert all(isinstance(r, RankedAccount) for r in result)


def test_rank_default_top_n_is_ten() -> None:
    rows = [_row(company_name=f"Co{i}") for i in range(25)]
    result = rank_accounts(rows)
    assert len(result) == DEFAULT_TOP_N


def test_rank_is_deterministic() -> None:
    rows = [
        _row(company_name="Beta", sector="fintech", city="Riyadh"),
        _row(company_name="Alpha", sector="fintech", city="Riyadh"),
        _row(company_name="Gamma", sector="fintech", city="Riyadh"),
    ]
    first = [a.company_name for a in rank_accounts(rows)]
    second = [a.company_name for a in rank_accounts(rows)]
    assert first == second


def test_icp_match_beats_off_icp() -> None:
    rows = [
        _row(company_name="OnICP", sector="fintech", city="Riyadh"),
        _row(company_name="OffICP", sector="agriculture", city="Tabuk"),
    ]
    icp = ICPProfile(preferred_sectors=("fintech",), preferred_cities=("riyadh",))
    result = rank_accounts(rows, icp=icp, top_n=2)
    assert result[0].company_name == "OnICP"
    assert result[0].fit > result[1].fit


def test_signal_strength_increases_with_contact_info() -> None:
    bare = _row(company_name="Bare", email="", phone="")
    rich = _row(company_name="Rich", email="ceo@rich.sa", phone="+966500000000")
    result = rank_accounts([bare, rich], top_n=2)
    rich_row = next(r for r in result if r.company_name == "Rich")
    bare_row = next(r for r in result if r.company_name == "Bare")
    assert rich_row.signal_strength > bare_row.signal_strength


def test_governance_risk_flags_missing_source() -> None:
    rows = [_row(company_name="NoSrc", source="")]
    result = rank_accounts(rows, top_n=1)
    assert result[0].governance_risk >= 60.0
    assert any("risky_or_missing_source" in r for r in result[0].reasons)


def test_governance_risk_flags_freemail() -> None:
    rows = [_row(company_name="Free", email="founder@gmail.com")]
    result = rank_accounts(rows, top_n=1)
    assert any("freemail_domain" in r for r in result[0].reasons)


def test_total_combines_signals_and_risk() -> None:
    high = _row(
        company_name="Clean",
        sector="fintech",
        city="Riyadh",
        email="ceo@clean.sa",
        phone="+966500000000",
        source="crm_export",
    )
    bad = _row(
        company_name="Risky",
        sector="agriculture",
        city="Tabuk",
        email="x@gmail.com",
        source="",
    )
    icp = ICPProfile(preferred_sectors=("fintech",), preferred_cities=("riyadh",))
    result = rank_accounts([high, bad], icp=icp, top_n=2)
    assert result[0].company_name == "Clean"
    assert result[0].total > result[1].total


def test_to_dict_is_serializable() -> None:
    rows = [_row(company_name="Acme")]
    payload = rank_accounts(rows, top_n=1)[0].to_dict()
    assert payload["company_name"] == "Acme"
    assert isinstance(payload["reasons"], list)
    assert 0.0 <= payload["total"] <= 100.0


def test_top_n_must_be_positive() -> None:
    with pytest.raises(ValueError):
        rank_accounts([_row()], top_n=0)


def test_unnamed_row_does_not_crash() -> None:
    result = rank_accounts([{"sector": "fintech", "city": "Riyadh"}], top_n=1)
    assert result[0].company_name == "(unnamed)"
    assert result[0].governance_risk >= 30.0  # missing company name flagged
