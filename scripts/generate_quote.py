"""Generate a quote (price + scope + status) for an account.

Writes a Markdown artifact AND registers the quote in `business/_data/quotes.index.json`
so the deal desk and the website's `/quotes` route can read it. Demo-safe; never sent.

Usage:
    python3 scripts/generate_quote.py --account-id demo-001 --offer "Revenue OS" \
        --setup-price 18000 --monthly-price 5000
"""
from __future__ import annotations

import argparse
import datetime as dt
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from lib.quote_engine import load_quotes, save_quotes, next_id, now  # noqa: E402


REPO_ROOT = Path(__file__).resolve().parents[1]
EXPORT_DIR = REPO_ROOT / "business" / "closing" / "exports"
EXPORT_DIR.mkdir(parents=True, exist_ok=True)


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--account-id", required=True)
    parser.add_argument("--offer", required=True)
    parser.add_argument("--setup-price", type=int, required=True)
    parser.add_argument("--monthly-price", type=int, required=True)
    parser.add_argument("--scope", default="Per signed SOW.")
    parser.add_argument("--out-of-scope", default="Custom integrations beyond the SOW require a change order.")
    parser.add_argument("--valid-days", type=int, default=14)
    args = parser.parse_args()

    today = dt.date.today().isoformat()

    index = load_quotes()
    quote = {
        "id": next_id("Q", index["quotes"]),
        "accountId": args.account_id,
        "offer": args.offer,
        "setupPrice": args.setup_price,
        "monthlyPrice": args.monthly_price,
        "currency": "SAR",
        "scope": args.scope,
        "outOfScope": args.out_of_scope,
        "validUntil": (dt.date.today() + dt.timedelta(days=args.valid_days)).isoformat(),
        "createdAt": now(),
        "status": "pending_review",
        "demo": True,
    }
    index["quotes"].append(quote)
    save_quotes(index)

    body = f"""# Quote {quote['id']} — {args.offer} for {args.account_id} (DEMO)

- Setup: SAR {args.setup_price:,}
- Monthly: SAR {args.monthly_price:,}
- Generated: {today}
- Valid until: {quote['validUntil']}
- Status: {quote['status']}
- Review: required (founder)

## Scope
{args.scope}

## Out of scope
{args.out_of_scope}

## Boilerplate inclusions
- Workflow map
- Command center setup
- Top 3 automations
- Weekly proof report
- Quarterly review

## Boilerplate exclusions
- Financial / legal decision automation
- Private data scraping
- Mass cold outreach

Next step: 60-min Day 0 — Intake call.

---
*Demo draft. NOT a contract. VAT/ZATCA via customer accounting system.*
"""
    out = EXPORT_DIR / f"quote-{args.account_id}-{today}.md"
    out.write_text(body, encoding="utf-8")
    print(f"wrote {out}")
    print(f"quote-id: {quote['id']}")
    print("status: pending_review")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
