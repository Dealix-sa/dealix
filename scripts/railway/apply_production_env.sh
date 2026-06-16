#!/usr/bin/env bash
# Apply Dealix controlled-live-outbound production variables to Railway.
# Run after: railway login && railway link

set -Eeuo pipefail

SERVICE="${1:-dealix}"

echo "Applying production env to Railway service: $SERVICE"

railway variables --service "$SERVICE" --set "APP_ENV=production"
railway variables --service "$SERVICE" --set "ENVIRONMENT=production"
railway variables --service "$SERVICE" --set "APP_URL=https://api.dealix.me"
railway variables --service "$SERVICE" --set "BASE_URL=https://api.dealix.me"
railway variables --service "$SERVICE" --set "DEALIX_API_BASE=https://api.dealix.me"
railway variables --service "$SERVICE" --set "CORS_ORIGINS=https://dealix.me,https://www.dealix.me,https://api.dealix.me"

# Reference variable — must be set via Railway dashboard reference, not CLI literal
# railway variables --service "$SERVICE" --set "DATABASE_URL=\${{Postgres.DATABASE_URL}}"

echo "⚠️  Set DATABASE_URL as a Reference Variable in the Railway dashboard:"
echo "   Service Variables → DATABASE_URL → Add Reference → Postgres.DATABASE_URL"

railway variables --service "$SERVICE" --set "COMMAND_ROOM_ENABLED=true"
railway variables --service "$SERVICE" --set "CEO_DAILY_REPORT_ENABLED=true"
railway variables --service "$SERVICE" --set "REPLY_CLASSIFICATION_ENABLED=true"
railway variables --service "$SERVICE" --set "OUTREACH_TIMEZONE=Asia/Riyadh"

railway variables --service "$SERVICE" --set "EXTERNAL_SEND_ENABLED=true"
railway variables --service "$SERVICE" --set "OUTBOUND_MODE=controlled_live"
railway variables --service "$SERVICE" --set "OUTBOUND_REQUIRE_APPROVAL=true"
railway variables --service "$SERVICE" --set "OUTBOUND_REQUIRE_VERIFIED_TARGET=true"
railway variables --service "$SERVICE" --set "OUTBOUND_REQUIRE_SOURCE_URL=true"
railway variables --service "$SERVICE" --set "OUTBOUND_REQUIRE_OPT_OUT=true"
railway variables --service "$SERVICE" --set "OUTBOUND_BLOCK_FAKE_CLAIMS=true"
railway variables --service "$SERVICE" --set "OUTBOUND_BLOCK_GUARANTEED_ROI=true"

railway variables --service "$SERVICE" --set "EMAIL_SEND_ENABLED=true"
railway variables --service "$SERVICE" --set "EMAIL_SEND_MODE=live"
railway variables --service "$SERVICE" --set "EMAIL_PROVIDER=smtp"
railway variables --service "$SERVICE" --set "EMAIL_DAILY_LIMIT=25"
railway variables --service "$SERVICE" --set "EMAIL_BATCH_LIMIT=10"
railway variables --service "$SERVICE" --set "EMAIL_MIN_SECONDS_BETWEEN_SENDS=90"
railway variables --service "$SERVICE" --set "EMAIL_REQUIRE_UNSUBSCRIBE=true"
railway variables --service "$SERVICE" --set "EMAIL_TRACK_REPLIES=true"

railway variables --service "$SERVICE" --set "WHATSAPP_SEND_ENABLED=true"
railway variables --service "$SERVICE" --set "WHATSAPP_ALLOW_LIVE_SEND=true"
railway variables --service "$SERVICE" --set "WHATSAPP_PROVIDER=meta_cloud"
railway variables --service "$SERVICE" --set "WHATSAPP_SEND_MODE=template_only"
railway variables --service "$SERVICE" --set "WHATSAPP_DAILY_LIMIT=10"
railway variables --service "$SERVICE" --set "WHATSAPP_BATCH_LIMIT=5"
railway variables --service "$SERVICE" --set "WHATSAPP_MIN_SECONDS_BETWEEN_SENDS=120"
railway variables --service "$SERVICE" --set "WHATSAPP_REQUIRE_OPT_IN=true"
railway variables --service "$SERVICE" --set "WHATSAPP_REQUIRE_APPROVED_TEMPLATE=true"
railway variables --service "$SERVICE" --set "WHATSAPP_STOP_KEYWORDS=STOP,UNSUBSCRIBE,إيقاف,الغاء,إلغاء"

echo "✅ Base production variables applied."
echo "🔑 Now set secrets via Railway dashboard or CLI:"
echo "   APP_SECRET_KEY, JWT_SECRET_KEY, API_KEYS, ADMIN_API_KEYS, DEALIX_ADMIN_API_KEY"
echo "   SMTP_HOST, SMTP_USER, SMTP_PASSWORD, META_PHONE_NUMBER_ID, META_WA_ACCESS_TOKEN"
