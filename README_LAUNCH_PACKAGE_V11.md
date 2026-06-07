# Dealix Launch Package V11 — Live Customer Onboarding & First Revenue Sprint

V11 converts the production-ready Dealix stack into a 30-day first-revenue operating sprint.

## Core loop
Lead → Discovery → Pilot Room → Invoice Tracker → Delivery Milestones → Acceptance → Proof Report → Retainer Conversion

## Run checks
```bash
python scripts/dealix_v11_readiness_check.py
python scripts/dealix_first_revenue_sprint.py
python scripts/dealix_revenue_dashboard.py
python scripts/dealix_client_room_builder.py --client "شركة تدريب الرياض" --package pilot
python scripts/dealix_invoice_tracker.py --client "شركة تدريب الرياض" --amount 499 --status sent
python scripts/dealix_pilot_acceptance_tracker.py --client "شركة تدريب الرياض" --milestone "CRM workflow map" --status accepted
python scripts/dealix_weekly_proof_report.py --client "شركة تدريب الرياض"
```
