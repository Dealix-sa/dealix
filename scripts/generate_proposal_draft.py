#!/usr/bin/env python3
"""Generate governed proposal drafts for proposal-ready prospects.

Writes one markdown proposal per prospect under ``data/proposals/`` and a
summary to ``reports/distribution/PROPOSAL_DRAFT_REPORT.md``. Every proposal is
a draft requiring approval — no binding commitments, no guaranteed outcomes.
"""

from __future__ import annotations

import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from auto_client_acquisition.distribution_os import (  # noqa: E402
    generate_proposals,
    load_prospects,
    render_proposal_markdown,
)
from auto_client_acquisition.distribution_os.report import render_proposal_report  # noqa: E402
from auto_client_acquisition.distribution_os.store import (  # noqa: E402
    proposals_dir,
    reports_dir,
    write_text,
)


def main() -> int:
    prospects = load_prospects()
    proposals = generate_proposals(prospects)

    pdir = proposals_dir()
    for proposal in proposals:
        write_text(pdir / f"{proposal.prospect_id}.md", render_proposal_markdown(proposal))

    report = write_text(
        reports_dir() / "PROPOSAL_DRAFT_REPORT.md", render_proposal_report(proposals)
    )
    print(f"proposal drafts: {len(proposals)}")
    print(f"wrote: {pdir.relative_to(ROOT)}/<prospect>.md")
    print(f"wrote: {report.relative_to(ROOT)}")
    print("DEALIX_PROPOSAL_DRAFTS=PASS")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
