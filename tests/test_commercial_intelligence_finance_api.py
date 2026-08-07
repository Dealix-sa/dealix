from decimal import Decimal
from types import SimpleNamespace

import pytest
from fastapi import HTTPException
from pydantic import ValidationError

from api.routers import commercial_intelligence as router_module
from api.routers.commercial_intelligence import FinanceCaseBody, PriceApprovalBody
from db.models import AuditLogRecord
from db.models_commercial_intelligence import (
    CommercialFinanceCaseRecord,
    CommercialOpportunityRecord,
)
from dealix.commercial_finance import REQUIRED_ECONOMIC_SOURCE_KEYS, CommercialFinanceInputs


def _source_refs() -> dict[str, str]:
    return {key: f"evidence://finance/{key}" for key in REQUIRED_ECONOMIC_SOURCE_KEYS}


def _body() -> FinanceCaseBody:
    return FinanceCaseBody(
        offer_class="productized",
        list_price_sar=Decimal("10000"),
        proposed_price_sar=Decimal("9000"),
        delivery_cost_sar=Decimal("3000"),
        acquisition_cost_sar=Decimal("500"),
        upfront_cash_exposure_sar=Decimal("500"),
        payment_terms_days=30,
        capacity_required_pct=Decimal("10"),
        source_refs=_source_refs(),
    )


def _opportunity() -> SimpleNamespace:
    return SimpleNamespace(
        id="opp_1",
        tenant_id="tenant-a",
        status="active",
        offer_id="revenue_proof_sprint",
    )


class _Session:
    def __init__(self, *, finance_case: object | None = None) -> None:
        self.opportunity = _opportunity()
        self.finance_case = finance_case
        self.added: list[object] = []
        self.commits = 0
        self.rollbacks = 0

    async def __aenter__(self) -> "_Session":
        return self

    async def __aexit__(self, *_: object) -> None:
        return None

    async def get(self, model: type[object], record_id: str) -> object | None:
        if model is CommercialOpportunityRecord and record_id == "opp_1":
            return self.opportunity
        if model is CommercialFinanceCaseRecord and record_id == "fin_draft":
            return self.finance_case
        return None

    def add(self, record: object) -> None:
        self.added.append(record)

    async def commit(self) -> None:
        self.commits += 1

    async def rollback(self) -> None:
        self.rollbacks += 1


@pytest.mark.asyncio
async def test_create_finance_case_is_append_only_draft_and_audited(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _Session()
    monkeypatch.setattr(router_module, "async_session_factory", lambda: lambda: session)

    result = await router_module.create_finance_case(
        "opp_1",
        _body(),
        current_user={"id": "user-sales", "tenant_id": "tenant-a"},
    )

    finance_records = [item for item in session.added if isinstance(item, CommercialFinanceCaseRecord)]
    audits = [item for item in session.added if isinstance(item, AuditLogRecord)]
    assert len(finance_records) == 1
    assert len(audits) == 1
    assert finance_records[0].pricing_status == "draft"
    assert finance_records[0].approval_required is True
    assert finance_records[0].external_action_allowed is False
    assert result["finance_case"]["decision"] == "pursue"
    assert result["finance_case"]["price_approved"] is False
    assert result["external_side_effect"] is False
    assert session.commits == 1


def test_finance_body_cannot_self_assert_founder_approval() -> None:
    with pytest.raises(ValidationError):
        FinanceCaseBody.model_validate(
            {
                **_body().model_dump(),
                "pricing_status": "founder_approved",
            }
        )


def _draft_case(*, corrupt: bool = False) -> SimpleNamespace:
    body = _body()
    inputs = CommercialFinanceInputs(
        opportunity_id="opp_1",
        offer_id="revenue_proof_sprint",
        offer_class=body.offer_class,
        list_price_sar=body.list_price_sar,
        proposed_price_sar=body.proposed_price_sar,
        delivery_cost_sar=body.delivery_cost_sar,
        acquisition_cost_sar=body.acquisition_cost_sar,
        upfront_cash_exposure_sar=body.upfront_cash_exposure_sar,
        payment_terms_days=body.payment_terms_days,
        capacity_required_pct=body.capacity_required_pct,
        source_refs=body.source_refs,
    ).to_dict()
    if corrupt:
        inputs.pop("delivery_cost_sar")
    return SimpleNamespace(
        id="fin_draft",
        tenant_id="tenant-a",
        opportunity_id="opp_1",
        parent_case_id=None,
        offer_id="revenue_proof_sprint",
        pricing_status="draft",
        proposed_price_sar=Decimal("9000.00"),
        inputs_json=inputs,
    )


@pytest.mark.asyncio
async def test_price_approval_creates_immutable_child_and_audit(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _Session(finance_case=_draft_case())
    monkeypatch.setattr(router_module, "async_session_factory", lambda: lambda: session)

    result = await router_module.approve_finance_case_price(
        "opp_1",
        "fin_draft",
        PriceApprovalBody(
            confirmed_proposed_price_sar=Decimal("9000"),
            approval_ref="founder-decision-2026-07-17-001",
        ),
        current_user={"id": "founder-user", "tenant_id": "tenant-a"},
    )

    children = [item for item in session.added if isinstance(item, CommercialFinanceCaseRecord)]
    audits = [item for item in session.added if isinstance(item, AuditLogRecord)]
    assert len(children) == 1
    assert len(audits) == 1
    assert children[0].parent_case_id == "fin_draft"
    assert children[0].pricing_status == "founder_approved"
    assert children[0].approved_by_user_id == "founder-user"
    assert children[0].external_action_allowed is False
    assert result["finance_case"]["price_approved"] is True
    assert result["finance_case"]["decision"] == "pursue"


@pytest.mark.asyncio
async def test_price_approval_requires_exact_confirmed_price(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _Session(finance_case=_draft_case())
    monkeypatch.setattr(router_module, "async_session_factory", lambda: lambda: session)

    with pytest.raises(HTTPException) as error:
        await router_module.approve_finance_case_price(
            "opp_1",
            "fin_draft",
            PriceApprovalBody(
                confirmed_proposed_price_sar=Decimal("8999"),
                approval_ref="founder-decision-mismatch",
            ),
            current_user={"id": "founder-user", "tenant_id": "tenant-a"},
        )

    assert error.value.status_code == 409
    assert error.value.detail == "confirmed_price_does_not_match_finance_case"
    assert not session.added


@pytest.mark.asyncio
async def test_corrupt_historical_finance_input_fails_closed(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _Session(finance_case=_draft_case(corrupt=True))
    monkeypatch.setattr(router_module, "async_session_factory", lambda: lambda: session)

    with pytest.raises(HTTPException) as error:
        await router_module.approve_finance_case_price(
            "opp_1",
            "fin_draft",
            PriceApprovalBody(
                confirmed_proposed_price_sar=Decimal("9000"),
                approval_ref="founder-decision-corrupt",
            ),
            current_user={"id": "founder-user", "tenant_id": "tenant-a"},
        )

    assert error.value.status_code == 409
    assert error.value.detail == "finance_case_inputs_corrupt"
    assert not session.added


@pytest.mark.asyncio
async def test_finance_case_is_tenant_scoped(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    session = _Session()
    monkeypatch.setattr(router_module, "async_session_factory", lambda: lambda: session)

    with pytest.raises(HTTPException) as error:
        await router_module.create_finance_case(
            "opp_1",
            _body(),
            current_user={"id": "user-sales", "tenant_id": "tenant-b"},
        )

    assert error.value.status_code == 404
    assert not session.added
