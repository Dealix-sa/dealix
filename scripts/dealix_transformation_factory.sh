#!/usr/bin/env bash
set -Eeuo pipefail

cd "$(git rev-parse --show-toplevel)"

CLIENT="${1:-Demo Client}"
SECTOR="${2:-Clinics}"
PAIN="${3:-Leads and follow-ups are scattered across WhatsApp and management lacks daily visibility.}"
SERVICES="${4:-whatsapp_revenue_os,ai_business_command_center,brand_intelligence_os}"

python transformation_os/scripts/service_factory.py \
  --client "$CLIENT" \
  --sector "$SECTOR" \
  --pain "$PAIN" \
  --services "$SERVICES"
