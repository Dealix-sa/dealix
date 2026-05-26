#!/usr/bin/env python3
"""Verification script for the Dealix-Hermes Integration.
Runs in-process HTTP smoke tests against the registered endpoints and Pydantic validation.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
from pathlib import Path

# Setup REPO path for import resolving
_REPO = Path(__file__).resolve().parents[1]
if str(_REPO) not in sys.path:
    sys.path.insert(0, str(_REPO))

import httpx

# Configure mock API keys and SQLite in-memory database to prevent PG connection hangs
os.environ["APP_ENV"] = "test"
os.environ["DATABASE_URL"] = "sqlite+aiosqlite:///:memory:"
os.environ["API_KEYS"] = "test-client-key"
os.environ["ADMIN_API_KEYS"] = "test-admin-key"

from api.main import create_app  # noqa: E402

async def run_tests() -> int:
    try:
        sys.stdout.reconfigure(encoding="utf-8")
    except (AttributeError, OSError):
        pass

    print("Initializing Dealix app in-process...")
    app = create_app()
    transport = httpx.ASGITransport(app=app)
    
    # Establish test headers matching APIKeyMiddleware expectations
    headers = {
        "X-API-Key": "test-client-key",
        "X-Admin-API-Key": "test-admin-key",
        "Content-Type": "application/json"
    }

    failed = 0

    async with httpx.AsyncClient(transport=transport, base_url="http://test", headers=headers) as client:
        # Test 1: Sovereign Command snapshot (GET)
        print("\n--- Test 1: Sovereign Command Snapshot ---")
        r = await client.get("/api/v1/hermes-integration/command")
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("Response:", json.dumps(r.json(), indent=2, ensure_ascii=False))
        else:
            failed += 1
            print(f"FAILED: {r.text}", file=sys.stderr)

        # Test 2: Signal Intake (POST)
        print("\n--- Test 2: Signal Intake ---")
        signal_data = {
            "source": "SPL Address API Validation",
            "payload": {
                "address_registered": True,
                "city": "Riyadh",
                "zip_code": "11564",
                "district": "Al-Malaz"
            }
        }
        r = await client.post("/api/v1/hermes-integration/signals", json=signal_data)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("Response:", json.dumps(r.json(), indent=2, ensure_ascii=False))
        else:
            failed += 1
            print(f"FAILED: {r.text}", file=sys.stderr)

        # Test 3: Strategic Opportunity Scoring (POST)
        print("\n--- Test 3: Opportunity Scoring ---")
        opportunity_data = {
            "title": "Hermes Europe-to-GCC Cross-Border Flow",
            "sector": "Luxury Goods",
            "buyer_persona": "High-net-worth Saudi retail merchants",
            "estimated_revenue": 125000.00,
            "speed_to_cash": 8.5,
            "repeatability": 9.0,
            "data_moat": 7.5,
            "partner_leverage": 8.0,
            "risk_factor": 2.5
        }
        r = await client.post("/api/v1/hermes-integration/opportunities/score", json=opportunity_data)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("Response:", json.dumps(r.json(), indent=2, ensure_ascii=False))
        else:
            failed += 1
            print(f"FAILED: {r.text}", file=sys.stderr)

        # Test 4: Agent Execution Gated Approval (POST)
        print("\n--- Test 4: Gated Action Approval ---")
        approval_data = {
            "agent_id": "00000000-0000-0000-0000-000000000001",
            "action_type": "Execute Customs Cargo Booking",
            "evidence_payload": {
                "customs_duty_estimated_sar": 4350.00,
                "declarations_passed": True
            },
            "approved_by": "Sami"
        }
        r = await client.post("/api/v1/hermes-integration/executions/approve", json=approval_data)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("Response:", json.dumps(r.json(), indent=2, ensure_ascii=False))
        else:
            failed += 1
            print(f"FAILED: {r.text}", file=sys.stderr)

        # Test 5: Shipment & National Address Verification (POST)
        print("\n--- Test 5: Shipment Verification ---")
        shipment_data = {
            "tracking_number": "HRM9876543210SA",
            "client_name": "Sami bin Khalid",
            "delivery_address": "8234 King Fahd Branch Rd, Al-Olaya, Riyadh 12211, Saudi Arabia",
            "cargo_value": 45000.00,
            "is_luxury": True
        }
        r = await client.post("/api/v1/hermes-integration/shipments/verify", json=shipment_data)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("Response:", json.dumps(r.json(), indent=2, ensure_ascii=False))
        else:
            failed += 1
            print(f"FAILED: {r.text}", file=sys.stderr)

        # Test 6: Personal Deal Logger (POST)
        print("\n--- Test 6: Sami Personal Deal Logger ---")
        deal_data = {
            "opportunity_id": "11111111-1111-1111-1111-111111111111",
            "deal_type": "Revenue Share",
            "target_value": 250000.00,
            "my_share_percentage": 15.00,
            "expected_cash_date": "2026-08-01",
            "walkaway_conditions": "Revenue share falls below 10% or logistics delays exceed 4 days."
        }
        r = await client.post("/api/v1/hermes-integration/deals", json=deal_data)
        print(f"Status: {r.status_code}")
        if r.status_code == 200:
            print("Response:", json.dumps(r.json(), indent=2, ensure_ascii=False))
        else:
            failed += 1
            print(f"FAILED: {r.text}", file=sys.stderr)

    if failed:
        print(f"\nVerification FAILED with {failed} errors.", file=sys.stderr)
        return 1

    print("\nDealix-Hermes integration verification completed successfully. (SMOKE_OK)")
    return 0

if __name__ == "__main__":
    raise SystemExit(asyncio.run(run_tests()))
