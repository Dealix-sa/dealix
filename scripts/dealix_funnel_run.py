#!/usr/bin/env python3
"""Dealix Funnel Runner — chain Rung 0 to Rung 1 in one command.

Runs the Free Diagnostic, the discovery-call qualification gate, and (if
accepted) renders the Sprint proposal — in one sequenced local pass, no
server required. This is a thin orchestrator over three already-existing,
already-tested founder-facing CLIs and does not duplicate any of their
decision logic:

    scripts/dealix_diagnostic.py    -> auto_client_acquisition.diagnostic_engine.generate_diagnostic
    scripts/dealix_qualify_lead.py  -> auto_client_acquisition.sales_os.qualification.qualify
                                     -> auto_client_acquisition.sales_os.proposal_renderer.render_proposal

Each of those three tools remains fully usable on its own for a founder who
only needs one stage (e.g. running a diagnostic for a curious prospect who
hasn't had a discovery call yet). This script exists for the common case
where a founder wants to run the whole funnel for one prospect in a single
pass instead of manually copying values between three separate commands.

Pure local computation + local file I/O — NO LLM call, NO live send, NO
scraping, NO network calls. Every stage is a pure function call; nothing
is auto-sent. Every artifact is written locally and printed to stdout for
founder review.

Usage:
    python scripts/dealix_funnel_run.py \\
        --company "ACME Saudi Co." \\
        --customer-handle acme_co \\
        --sector b2b_services \\
        --region riyadh \\
        --pipeline-state "WhatsApp incoming, founder responds at night" \\
        --pain-clear --owner-present --data-available --accepts-governance \\
        --has-budget --proof-path-visible --retainer-path-visible \\
        --engagement-id eng_acme_001

Stops cleanly at whichever stage doesn't clear its own gate:
    - The Diagnostic always runs and is always written (Rung 0 is free and
      has no gate).
    - Qualification runs next. If the discovery-call flags/raw text you
      pass are all defaults (i.e. you haven't actually had a discovery
      call yet), qualification will legitimately score low or REJECT —
      that's the qualification engine doing its job, not a bug. Pass the
      real discovery-call answers you have.
    - The proposal is rendered ONLY if qualification's decision is
      "accept" or "reframe" (i.e. the qualification engine did not REJECT
      or REFER_OUT the lead, and no doctrine violation was found). If
      qualification stops the funnel, this script explains why and does
      NOT render a proposal for a lead that hasn't cleared the gate.

Founder review is required before any customer-facing send — this script
never emails, WhatsApps, or POSTs anything anywhere.
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path
from typing import Any

REPO_ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(REPO_ROOT))

from auto_client_acquisition.diagnostic_engine import (
    DiagnosticRequest,
    generate_diagnostic,
)
from auto_client_acquisition.sales_os.proposal_renderer import (
    ProposalContext,
    render_proposal,
)
from auto_client_acquisition.sales_os.qualification import Decision, qualify

# Qualification decisions that are allowed to proceed to a rendered
# proposal. REJECT and REFER_OUT explicitly stop the funnel here — this
# mirrors qualify()'s own decision tree, it does not add a new policy.
_PROCEED_TO_PROPOSAL_DECISIONS = {Decision.ACCEPT.value, Decision.REFRAME.value}


def _write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")


def main(argv: list[str] | None = None) -> int:
    p = argparse.ArgumentParser(
        description=(
            "Chain the Free Diagnostic, the qualification gate, and (if "
            "accepted) the Sprint proposal in one local pass. No external "
            "send of any kind."
        ),
    )

    # Shared prospect identity
    p.add_argument("--company", required=True, help="prospect company name")
    p.add_argument(
        "--customer-handle",
        required=True,
        help="internal customer handle/slug (used for the proposal, if rendered)",
    )
    p.add_argument("--engagement-id", required=True, help="engagement identifier")
    p.add_argument("--sector", default="b2b_services")
    p.add_argument("--region", default="ksa", help="prospect region (e.g. riyadh, jeddah, dammam, ksa)")
    p.add_argument("--city", default="Riyadh", help="city used on the proposal, if rendered")

    # Stage 1 — Diagnostic
    p.add_argument(
        "--pipeline-state",
        default="(unknown — fill in after the discovery call)",
        help="one-line description of the prospect's current pipeline state",
    )

    # Stage 2 — Qualification (discovery-call answers)
    p.add_argument("--pain-clear", action="store_true", default=False)
    p.add_argument("--owner-present", action="store_true", default=False)
    p.add_argument("--data-available", action="store_true", default=False)
    p.add_argument("--accepts-governance", action="store_true", default=False)
    p.add_argument("--has-budget", action="store_true", default=False)
    p.add_argument("--proof-path-visible", action="store_true", default=False)
    p.add_argument("--retainer-path-visible", action="store_true", default=False)
    p.add_argument(
        "--no-safe-methods",
        dest="wants_safe_methods",
        action="store_false",
        default=True,
        help="the prospect does NOT want safe/compliant methods (default: wants safe methods)",
    )
    p.add_argument(
        "--raw-request-text",
        default="",
        help="free text from the discovery call, scanned for doctrine violations (EN + AR)",
    )

    # Stage 3 — Proposal (only used if qualification allows proceeding)
    p.add_argument("--price-sar", type=int, default=499)
    p.add_argument("--delivery-days", type=int, default=7)

    p.add_argument(
        "--out-dir",
        default=None,
        help="directory to write outputs into (default: out/funnel/<engagement-id>/)",
    )
    p.add_argument(
        "--json",
        action="store_true",
        help="print a JSON envelope of all stage results instead of writing files",
    )
    args = p.parse_args(argv)

    # ---- Stage 1: Diagnostic (always runs — Rung 0 is free, no gate) ----
    diagnostic_result = generate_diagnostic(
        DiagnosticRequest(
            company=args.company,
            sector=args.sector,
            region=args.region,
            pipeline_state=args.pipeline_state,
        )
    )

    # ---- Stage 2: Qualification (the gate) ----
    qualification_result = qualify(
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

    # ---- Stage 3: Proposal (gated on qualification's own decision) ----
    proposal_markdown: str | None = None
    proposal_rendered = False
    if qualification_result.decision in _PROCEED_TO_PROPOSAL_DECISIONS:
        context = ProposalContext(
            customer_name=args.company,
            customer_handle=args.customer_handle,
            sector=args.sector,
            city=args.city,
            engagement_id=args.engagement_id,
            price_sar=args.price_sar,
            delivery_days=args.delivery_days,
        )
        proposal_markdown = render_proposal(context)
        proposal_rendered = True

    if args.json:
        payload: dict[str, Any] = {
            "engagement_id": args.engagement_id,
            "company": args.company,
            "diagnostic": {
                "recommended_bundle": diagnostic_result.recommended_bundle,
                "markdown_ar_en": diagnostic_result.markdown_ar_en,
            },
            "qualification": qualification_result.to_dict(),
            "proposal_rendered": proposal_rendered,
            "proposal_markdown": proposal_markdown,
        }
        print(json.dumps(payload, indent=2, ensure_ascii=False, default=str))
        return 0

    out_dir = Path(args.out_dir) if args.out_dir else REPO_ROOT / "out" / "funnel" / args.engagement_id
    written: list[Path] = []

    diagnostic_path = out_dir / "diagnostic.md"
    _write(diagnostic_path, diagnostic_result.markdown_ar_en)
    written.append(diagnostic_path)

    qualification_path = out_dir / "qualification.json"
    _write(
        qualification_path,
        json.dumps(qualification_result.to_dict(), indent=2, ensure_ascii=False, default=str),
    )
    written.append(qualification_path)

    if proposal_rendered and proposal_markdown is not None:
        proposal_path = out_dir / "proposal.md"
        _write(proposal_path, proposal_markdown)
        written.append(proposal_path)

    lines: list[str] = [
        f"Dealix funnel run — engagement: {args.engagement_id}",
        "",
        f"company: {args.company}",
        f"1. diagnostic: recommended_bundle={diagnostic_result.recommended_bundle}",
        f"2. qualification: decision={qualification_result.decision}, "
        f"score={qualification_result.score}, "
        f"recommended_offer={qualification_result.recommended_offer}",
    ]

    if qualification_result.doctrine_violations:
        lines.append("")
        lines.append(
            "DOCTRINE VIOLATION DETECTED — funnel stops here; do not proceed "
            "to a proposal or any further engagement."
        )
        lines.append(f"doctrine_violations: {qualification_result.doctrine_violations}")

    if proposal_rendered:
        lines.append("3. proposal: rendered (qualification allowed proceeding)")
    else:
        lines.append(
            "3. proposal: NOT rendered — qualification decision "
            f"({qualification_result.decision!r}) does not clear the gate "
            f"to proceed (only {sorted(_PROCEED_TO_PROPOSAL_DECISIONS)} proceed)."
        )

    lines.append("")
    lines.append("Files written:")
    for path in written:
        lines.append(f"  - {path}")
    lines.append("")
    lines.append(
        "Founder review required before any customer-facing send — no "
        "external message has been sent by this script."
    )

    print("\n".join(lines))
    return 0


if __name__ == "__main__":  # pragma: no cover
    sys.exit(main())
