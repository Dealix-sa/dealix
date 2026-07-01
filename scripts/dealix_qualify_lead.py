#!/usr/bin/env python3
"""Dealix Lead Qualification + Proposal CLI — run the discovery-call
qualification gate and render the 499 SAR Sprint proposal from a
terminal, no server required.

Wraps the existing, already-tested decision engine and renderer
(``auto_client_acquisition.sales_os.qualification.qualify`` and
``auto_client_acquisition.sales_os.proposal_renderer.render_proposal``)
so the founder can run the qualification gate that sits BEFORE a Sprint
is even kicked off, and render the resulting proposal document, without
writing Python or hitting the FastAPI server. Pure local computation +
local file I/O — NO LLM call, NO live send, NO scraping, NO network
calls. This script only ever prints to stdout and writes a local
proposal.md file.

Usage:
    python scripts/dealix_qualify_lead.py qualify \\
        --pain-clear --owner-present --data-available --accepts-governance \\
        --has-budget --proof-path-visible --retainer-path-visible \\
        --raw-request-text "Client wants help prioritizing follow-ups" \\
        --sector b2b_services --city Riyadh

    python scripts/dealix_qualify_lead.py propose \\
        --customer-name "شركة الواحة للاستشارات" \\
        --customer-handle alwaha \\
        --sector b2b_services \\
        --city Riyadh \\
        --engagement-id eng_alwaha_001 \\
        --price-sar 499 \\
        --out-dir out/proposals/eng_alwaha_001

Qualification is a doctrine enforcement point: any doctrine violation
detected in --raw-request-text (cold WhatsApp, guaranteed-sales
language, scraping, LinkedIn automation) forces a REJECT regardless of
score, and this CLI never suppresses or softens that signal. Founder
review is still required before any customer-facing send — this script
never emails, WhatsApps, or POSTs anything anywhere.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.sales_os.proposal_renderer import (
    ProposalContext,
    render_proposal,
)
from auto_client_acquisition.sales_os.qualification import qualify

_DOCTRINE_BANNER = (
    "DOCTRINE VIOLATION DETECTED — decline this request; do not proceed "
    "to a proposal."
)


def _print_qualification_result(result, *, as_json: bool) -> None:
    if as_json:
        print(json.dumps(result.to_dict(), indent=2, ensure_ascii=False, default=str))
        return

    lines: list[str] = []

    if result.doctrine_violations:
        lines.append(_DOCTRINE_BANNER)
        lines.append("")

    lines.append(f"decision: {result.decision}")
    lines.append(f"score: {result.score}")
    lines.append(f"recommended_offer: {result.recommended_offer}")
    lines.append("")

    lines.append("reasons:")
    if result.reasons:
        for reason in result.reasons:
            lines.append(f"  - {reason}")
    else:
        lines.append("  (none)")

    if result.doctrine_violations:
        lines.append("")
        lines.append("doctrine_violations:")
        for violation in result.doctrine_violations:
            lines.append(f"  - {violation}")

    print("\n".join(lines))


def _cmd_qualify(args: argparse.Namespace) -> int:
    result = qualify(
        pain_clear=args.pain_clear,
        owner_present=args.owner_present,
        data_available=args.data_available,
        accepts_governance=args.accepts_governance,
        has_budget=args.has_budget,
        wants_safe_methods=args.wants_safe_methods,
        proof_path_visible=args.proof_path_visible,
        retainer_path_visible=args.retainer_path_visible,
        raw_request_text=args.raw_request_text,
        sector=args.sector,
        city=args.city,
    )
    _print_qualification_result(result, as_json=args.json)
    return 0


def _cmd_propose(args: argparse.Namespace) -> int:
    # Doctrine cross-check: propose() does not require a prior qualify()
    # call (a founder may already know from a live call that a lead is
    # clean), but if --raw-request-text is supplied here we still must
    # never render a proposal for a doctrine-violating request. We reuse
    # qualify() itself (rather than importing the private
    # qualification._scan_doctrine helper directly) because qualify()
    # already folds in the wants_safe_methods=False path and is the
    # single source of truth for "what counts as a doctrine violation" —
    # calling the public function keeps this CLI decoupled from
    # qualification.py's internals.
    if args.raw_request_text:
        check = qualify(raw_request_text=args.raw_request_text)
        if check.doctrine_violations:
            lines = [
                _DOCTRINE_BANNER,
                "",
                "Refusing to render a proposal for this request.",
                "",
                "doctrine_violations:",
            ]
            for violation in check.doctrine_violations:
                lines.append(f"  - {violation}")
            print("\n".join(lines))
            return 0

    context = ProposalContext(
        customer_name=args.customer_name,
        customer_handle=args.customer_handle,
        sector=args.sector,
        city=args.city,
        engagement_id=args.engagement_id,
        price_sar=args.price_sar,
        delivery_days=args.delivery_days,
    )
    markdown = render_proposal(context)

    if args.json:
        payload = {
            "engagement_id": args.engagement_id,
            "customer_handle": args.customer_handle,
            "price_sar": args.price_sar,
            "delivery_days": args.delivery_days,
            "proposal_markdown": markdown,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))
        return 0

    out_dir = Path(args.out_dir) if args.out_dir else REPO_ROOT / "out" / "proposals" / args.engagement_id
    out_dir.mkdir(parents=True, exist_ok=True)
    proposal_path = out_dir / "proposal.md"
    proposal_path.write_text(markdown, encoding="utf-8")

    lines = [
        f"Dealix proposal rendered — engagement: {args.engagement_id}",
        "",
        f"engagement_id: {args.engagement_id}",
        f"customer_handle: {args.customer_handle}",
        f"price_sar: {args.price_sar}",
        "",
        "Files written:",
        f"  - {proposal_path}",
        "",
        "Founder review required before any customer-facing send — no "
        "external message has been sent by this script.",
    ]
    print("\n".join(lines))
    return 0


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Run the Dealix discovery-call qualification gate and render "
            "the Sprint proposal locally. No external send of any kind."
        ),
    )
    sub = p.add_subparsers(dest="command", required=True)

    qualify_p = sub.add_parser(
        "qualify", help="score a discovery call and print a commercial verdict"
    )
    qualify_p.add_argument("--pain-clear", action="store_true", default=False)
    qualify_p.add_argument("--owner-present", action="store_true", default=False)
    qualify_p.add_argument("--data-available", action="store_true", default=False)
    qualify_p.add_argument("--accepts-governance", action="store_true", default=False)
    qualify_p.add_argument("--has-budget", action="store_true", default=False)
    qualify_p.add_argument("--proof-path-visible", action="store_true", default=False)
    qualify_p.add_argument("--retainer-path-visible", action="store_true", default=False)
    qualify_p.add_argument(
        "--no-safe-methods",
        dest="wants_safe_methods",
        action="store_false",
        default=True,
        help="the prospect does NOT want safe/compliant methods (default: wants safe methods)",
    )
    qualify_p.add_argument(
        "--raw-request-text",
        default="",
        help="free text from the discovery call, scanned for doctrine violations (EN + AR)",
    )
    qualify_p.add_argument("--sector", default="")
    qualify_p.add_argument("--city", default="")
    qualify_p.add_argument(
        "--json",
        action="store_true",
        help="print the full QualificationResult as JSON instead of a human-readable summary",
    )
    qualify_p.set_defaults(func=_cmd_qualify)

    propose_p = sub.add_parser(
        "propose", help="render the bilingual Sprint proposal document"
    )
    propose_p.add_argument("--customer-name", required=True, help="customer legal/display name")
    propose_p.add_argument("--customer-handle", required=True, help="internal customer handle/slug")
    propose_p.add_argument("--sector", default="b2b_services")
    propose_p.add_argument("--city", default="Riyadh")
    propose_p.add_argument("--engagement-id", required=True, help="engagement identifier")
    propose_p.add_argument("--price-sar", type=int, default=499)
    propose_p.add_argument("--delivery-days", type=int, default=7)
    propose_p.add_argument(
        "--raw-request-text",
        default="",
        help=(
            "optional free text from the discovery call; if it trips a "
            "doctrine violation, this CLI refuses to render the proposal "
            "(this text is NOT passed into ProposalContext — it is only "
            "used locally for the doctrine cross-check)"
        ),
    )
    propose_p.add_argument(
        "--out-dir",
        default=None,
        help="directory to write proposal.md into (default: out/proposals/<engagement-id>/)",
    )
    propose_p.add_argument(
        "--json",
        action="store_true",
        help="print a JSON envelope with the rendered markdown instead of writing files",
    )
    propose_p.set_defaults(func=_cmd_propose)

    args = p.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
