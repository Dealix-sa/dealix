#!/usr/bin/env python3
"""Generate a company-specific Dealix sales pack from public, reviewed inputs.

The script creates drafts and negotiation guidance only. It does not send
messages, call APIs, scrape websites, or contact prospects.
"""
from __future__ import annotations

import argparse
import json
from datetime import datetime, timezone
from pathlib import Path
from textwrap import dedent

ROOT = Path(__file__).resolve().parents[2]
LIBRARY_PATH = ROOT / "data" / "commercial" / "pain_signal_library.json"
OUT_DIR = ROOT / "reports" / "commercial" / "sales_packs"


def load_library() -> dict[str, dict]:
    return json.loads(LIBRARY_PATH.read_text(encoding="utf-8"))


def pick_sector(library: dict[str, dict], sector: str) -> tuple[str, dict]:
    normalized = sector.strip().lower().replace(" ", "_").replace("-", "_")
    if normalized in library:
        return normalized, library[normalized]
    return "b2b_services", library["b2b_services"]


def build_pack(company: str, sector_key: str, profile: dict, city: str, source_url: str) -> str:
    pain = profile["pain_signals"][0]
    offer = profile["best_offer"]
    questions = "\n".join(f"- {item}" for item in profile["discovery_questions"])
    objections = "\n".join(f"- **{k}:** {v}" for k, v in profile["objections"].items())
    return dedent(
        f"""
        # Dealix Sales Pack — {company}

        ## Target context

        - Company: {company}
        - Sector: {sector_key}
        - City: {city or 'not specified'}
        - Source URL: {source_url or 'manual review required'}
        - Verification status: ready_for_review
        - Owner decision required before contact: yes

        ## Pain hypothesis

        {company} may be experiencing: **{pain}**.

        This is a hypothesis, not a claim. Validate it in discovery before selling.

        ## Recommended offer

        **{offer}**

        ## First message draft

        السلام عليكم، أنا من فريق Dealix.

        نساعد شركات مثل شركتكم على تحويل المتابعة والعروض والفرص اليومية إلى نظام تشغيل واضح: من يحتاج متابعة اليوم؟ ما الفرص الساخنة؟ وما القرار التجاري الأهم؟

        بناء على طبيعة قطاعكم، قد يكون أفضل مدخل هو {offer}. نبدأ عادة بتشخيص صغير يوضح أين تضيع المتابعة أو القرار، ثم sprint قصير بمخرجات قابلة للمراجعة.

        إذا مناسب، أرسل لكم صفحة واحدة مخصصة قبل أي اجتماع.

        لإيقاف التواصل، أرسل إيقاف.

        ## Discovery questions

        {questions}

        ## Objection handling

        {objections}

        ## Negotiation guardrails

        - Start with diagnostic or 7-day sprint.
        - Do not discount without reducing scope.
        - Offer proof pack instead of guaranteed revenue.
        - Keep first scope to one pain and one channel.
        - Use founder review before sending final proposal.

        ## Next action

        Review this pack manually, then decide: send, call, personalize_more, or reject.
        """
    ).strip() + "\n"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--company", default="Sample Company")
    parser.add_argument("--sector", default="b2b_services")
    parser.add_argument("--city", default="Riyadh")
    parser.add_argument("--source-url", default="")
    args = parser.parse_args()

    library = load_library()
    sector_key, profile = pick_sector(library, args.sector)
    OUT_DIR.mkdir(parents=True, exist_ok=True)

    safe_name = "".join(ch.lower() if ch.isalnum() else "_" for ch in args.company).strip("_") or "sample_company"
    pack = build_pack(args.company, sector_key, profile, args.city, args.source_url)
    md_path = OUT_DIR / f"{safe_name}.md"
    json_path = OUT_DIR / f"{safe_name}.json"
    md_path.write_text(pack, encoding="utf-8")
    json_path.write_text(
        json.dumps(
            {
                "generated_at": datetime.now(timezone.utc).isoformat(),
                "company": args.company,
                "sector": sector_key,
                "city": args.city,
                "source_url": args.source_url,
                "recommended_offer": profile["best_offer"],
                "status": "draft_requires_owner_review",
            },
            ensure_ascii=False,
            indent=2,
        )
        + "\n",
        encoding="utf-8",
    )
    print(f"SALES_PACK_GENERATED={md_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
