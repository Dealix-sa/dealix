#!/usr/bin/env python3
"""Verify the Marketing OS is in place."""

from __future__ import annotations

from _verify_common import Verifier


def populate(v: Verifier) -> None:
    v.check_files(
        [
            "docs/marketing/DEALIX_MARKETING_OS.md",
            "docs/marketing/CONTENT_CALENDAR_SYSTEM.md",
            "docs/marketing/FOUNDER_LED_CONTENT_SYSTEM.md",
            "docs/marketing/LANDING_PAGE_CONVERSION_SYSTEM.md",
            "docs/marketing/COPYWRITING_RULES.md",
            "docs/marketing/BRAND_VOICE_EXAMPLES.md",
            "docs/marketing/EMAIL_OUTREACH_GUIDE.md",
            "docs/marketing/LINKEDIN_OUTREACH_GUIDE.md",
            "docs/marketing/PARTNER_OUTREACH_GUIDE.md",
        ]
    )


if __name__ == "__main__":
    from _verify_common import main_for

    main_for("marketing-system", populate)
