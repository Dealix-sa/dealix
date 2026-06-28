#!/usr/bin/env python3
"""Generate manual LinkedIn outreach packs (copy-paste; never automated)."""
from __future__ import annotations

from _common import DATA_DIR, dump, load_json

from app.commercial import channels, reasoning
from app.commercial.lead_sourcing import load_accounts


def main() -> int:
    records = load_json(DATA_DIR / "accounts.sample.json", key="accounts")
    brain = reasoning.HeuristicBrain()
    out = []
    for a in load_accounts(records):
        if not a.linkedin_url:
            continue
        draft = brain.draft_reply({"recommended_action": "send_opener",
                                   "motion": a.recommended_motion or "sales_prospecting",
                                   "company_name": a.company_name,
                                   "pain_hypothesis": a.pain_hypothesis})
        payload = channels.prepare_linkedin(conversation_id=f"li_{a.account_id}",
                                            account_id=a.account_id,
                                            draft={"body_ar": draft["ar"], "body_en": draft["en"]},
                                            account=a)
        out.append(payload.to_dict())
    dump({"linkedin_packs": out, "count": len(out),
          "note": "manual send only — LinkedIn automation is forbidden"})
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
