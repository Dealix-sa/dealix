"""Tests for the Dealix Sales Strategist Agent."""

import json
import pytest
from unittest.mock import AsyncMock, MagicMock

from agents.sales_agent.sales_strategist import SalesStrategistAgent
from intelligence import SaudiCompanyProfile


@pytest.mark.asyncio
async def test_sales_strategist_returns_strategy():
    agent = SalesStrategistAgent()

    fake_response = MagicMock()
    fake_response.content = json.dumps({
        "fit_summary": "Strong fit for Dealix Revenue OS",
        "pitch_angles": [
            "Reduce lead research time by 80%",
            "Get Saudi-qualified prospects weekly",
            "Close pilots with evidence packs",
        ],
        "outreach_channel": "email",
        "objections_handling": {
            "budget": "Pilot starts at SAR 2,500 with measurable ROI",
        },
        "recommended_next_step": "Send diagnostic offer email",
        "confidence": 0.85,
    })

    agent.router = AsyncMock()
    agent.router.run = AsyncMock(return_value=fake_response)

    prospect = SaudiCompanyProfile(
        company_name="Najm Tech",
        sector="software",
        city="Riyadh",
        employees_estimate=45,
        website="https://najmtech.sa",
    )

    strategy = await agent.run(prospect)

    assert strategy.prospect_name == "Najm Tech"
    assert strategy.icp_score > 0
    assert len(strategy.pitch_angles) == 3
    assert strategy.outreach_channel == "email"
    assert "budget" in strategy.objections_handling
    assert strategy.confidence == 0.85


@pytest.mark.asyncio
async def test_sales_strategist_raises_on_bad_json():
    agent = SalesStrategistAgent()

    fake_response = MagicMock()
    fake_response.content = "not json"

    agent.router = AsyncMock()
    agent.router.run = AsyncMock(return_value=fake_response)

    prospect = SaudiCompanyProfile(
        company_name="Bad Data Co",
        sector="retail",
        city="Jeddah",
    )

    with pytest.raises(Exception):
        await agent.run(prospect)
