# Environment Variables

This project currently cannot store `.env.example` through the active editing policy, so this file acts as the source of truth for required local variables.

## Required
```env
NODE_ENV=development
PORT=3000
DATABASE_URL=mysql://dealix:dealix_pass_2026@localhost:3306/dealix
DB_USER=dealix
DB_PASSWORD=dealix_pass_2026
```

## Auth / App
```env
APP_ID=
APP_SECRET=
KIMI_AUTH_URL=
KIMI_OPEN_URL=
OWNER_UNION_ID=
VITE_APP_ID=
VITE_KIMI_AUTH_URL=
```

## Safety Defaults
```env
EXTERNAL_SEND_ENABLED=false
EMAIL_SEND_ENABLED=false
WHATSAPP_SEND_ENABLED=false
WHATSAPP_ALLOW_LIVE_SEND=false
SMS_SEND_ENABLED=false
OUTBOUND_MODE=draft_only
WHATSAPP_AGENT_MODE=dry_run
```

## WhatsApp
```env
WHATSAPP_ACCESS_TOKEN=
WHATSAPP_PHONE_NUMBER_ID=
WHATSAPP_WEBHOOK_VERIFY_TOKEN=
```