#!/usr/bin/env bash
set -u

cd "$(git rev-parse --show-toplevel)" || exit 1

echo "=== Dealix Intake Day ==="
date -u +"%Y-%m-%dT%H:%M:%SZ"

python company/intake/intake_engine.py

TODAY="$(date +%F)"

echo ""
echo "FILES:"
echo "company/runtime/intake/${TODAY}/CLIENT_INTAKE_TEMPLATE.csv"
echo "company/runtime/intake/${TODAY}/INTAKE_SUMMARY.md"
echo "company/intake/WHATSAPP_INTAKE_BOT_SCRIPT.md"
echo "company/presentation/DEALIX_COMPANY_PRESENTATION_AR.md"
