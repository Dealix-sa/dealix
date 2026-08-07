import os
import sys

BASE_REQUIRED = [
    "APP_ENV",
    "ENVIRONMENT",
    "DATABASE_URL",
    "EXTERNAL_SEND_ENABLED",
    "OUTBOUND_MODE",
]

EMAIL_REQUIRED_WHEN_LIVE = [
    "SMTP_HOST",
    "SMTP_PORT",
    "SMTP_USERNAME",
    "SMTP_PASSWORD",
    "SMTP_FROM_EMAIL",
    "UNSUBSCRIBE_BASE_URL",
]

WHATSAPP_META_REQUIRED_WHEN_LIVE = [
    "META_WA_PHONE_NUMBER_ID",
    "META_WA_ACCESS_TOKEN",
]


def missing(keys):
    return [k for k in keys if not os.getenv(k)]


def main() -> int:
    errors = []

    for key in missing(BASE_REQUIRED):
        errors.append(f"Missing base env: {key}")

    external = os.getenv("EXTERNAL_SEND_ENABLED", "").lower() == "true"
    mode = os.getenv("OUTBOUND_MODE", "")

    if external and mode != "controlled_live":
        errors.append("When EXTERNAL_SEND_ENABLED=true, OUTBOUND_MODE must be controlled_live")

    if os.getenv("EMAIL_SEND_ENABLED", "").lower() == "true":
        for key in missing(EMAIL_REQUIRED_WHEN_LIVE):
            errors.append(f"Missing email env: {key}")

    if os.getenv("WHATSAPP_SEND_ENABLED", "").lower() == "true":
        if os.getenv("WHATSAPP_ALLOW_LIVE_SEND", "").lower() != "true":
            errors.append("WHATSAPP_ALLOW_LIVE_SEND must be true for WhatsApp live sends")
        if os.getenv("WHATSAPP_SEND_MODE") != "template_only":
            errors.append("WHATSAPP_SEND_MODE must be template_only")
        if os.getenv("WHATSAPP_REQUIRE_OPT_IN", "").lower() != "true":
            errors.append("WHATSAPP_REQUIRE_OPT_IN must be true")
        if os.getenv("WHATSAPP_PROVIDER", "meta_cloud") == "meta_cloud":
            for key in missing(WHATSAPP_META_REQUIRED_WHEN_LIVE):
                errors.append(f"Missing WhatsApp Meta env: {key}")

    if errors:
        print("CONTROLLED_LIVE_OUTBOUND_ENV_FAILED")
        for e in errors:
            print(f"- {e}")
        return 1

    print("CONTROLLED_LIVE_OUTBOUND_ENV_OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
