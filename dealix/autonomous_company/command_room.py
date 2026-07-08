"""Renders the daily Command Room: one markdown brief + one self-contained HTML
page the founder opens each morning."""

from __future__ import annotations

import html
import json
from datetime import date

from .decision_engine import DecisionResult, Recommendation
from .schemas import KPIs


def render_markdown(run_date: date, kpis: KPIs, decision: DecisionResult, learning: list[str]) -> str:
    d = run_date.isoformat()
    lines = [
        f"# Dealix Command Room — {d}",
        "",
        "> Autonomous cycle complete. Draft-only. Every send/charge below is a "
        "draft awaiting your approval. Revenue counts only on `payment_received`.",
        "",
        "## KPIs",
        f"- Recognized revenue: **{kpis.recognized_revenue_sar} SAR**",
        f"- Weighted pipeline (forecast): **{round(kpis.weighted_pipeline_sar)} SAR**",
        f"- Open pipeline: {kpis.open_pipeline_sar} SAR",
        f"- Deals: {kpis.total_deals} total · {kpis.active_deals} active · "
        f"{kpis.won_deals} won · {kpis.lost_deals} lost · {kpis.stalled_deals} stalled",
        f"- Win rate: {round(kpis.win_rate * 100)}%",
        "",
        "## Today's top actions (ranked by the engine)",
    ]
    if decision.recommendations:
        for i, r in enumerate(decision.recommendations, 1):
            flag = " ⚠️STALLED" if r.stalled else ""
            gate = " · needs approval" if r.requires_approval else ""
            lines.append(
                f"{i}. **{r.account_name}** [{r.stage}] — {r.action}{gate}{flag}  "
                f"_(score {r.score}; {r.rationale})_"
            )
    else:
        lines.append("- No active deals. Add warm leads to `data/autonomous_company/inbox.json`.")

    lines += ["", "## Approval queue (drafts — review before any send/charge)"]
    if decision.approvals:
        for r in decision.approvals:
            lines += [f"### {r.account_name} — {r.action}", "", "```", r.draft.strip() or "(no draft)", "```", ""]
    else:
        lines.append("- (nothing awaiting approval)")

    if decision.stalled:
        lines += ["", "## Stalled deals to rescue"]
        lines += [f"- {r.account_name} [{r.stage}] — {r.rationale}" for r in decision.stalled]

    lines += ["", "## What the company learned this cycle"]
    lines += [f"- {n}" for n in learning] or ["- (none)"]

    lines += [
        "",
        "## Safety",
        "- No message sent. No content published. No customer charged. No production change.",
        "- To advance a deal, record a real evidence event in "
        "`data/autonomous_company/state.json` (e.g. `payment_received`).",
    ]
    return "\n".join(lines) + "\n"


def render_html(run_date: date, kpis: KPIs, decision: DecisionResult) -> str:
    d = run_date.isoformat()

    def esc(s: str) -> str:
        return html.escape(s or "")

    rows = []
    for i, r in enumerate(decision.recommendations, 1):
        badge = "stalled" if r.stalled else ("approval" if r.requires_approval else "ok")
        rows.append(
            f"<tr class='{badge}'><td>{i}</td><td>{esc(r.account_name)}</td>"
            f"<td><span class='stage'>{esc(r.stage)}</span></td>"
            f"<td>{esc(r.action)}</td><td class='num'>{r.score}</td>"
            f"<td>{'⚠️' if r.stalled else ''}{'🔒' if r.requires_approval else ''}</td></tr>"
        )
    table = "\n".join(rows) or "<tr><td colspan='6'>No active deals — add warm leads to the inbox.</td></tr>"

    approvals = []
    for r in decision.approvals:
        approvals.append(
            f"<details><summary>{esc(r.account_name)} — {esc(r.action)}</summary>"
            f"<pre>{esc(r.draft.strip())}</pre></details>"
        )
    approvals_html = "\n".join(approvals) or "<p class='muted'>Nothing awaiting approval.</p>"

    kpi_cards = [
        ("Recognized revenue", f"{kpis.recognized_revenue_sar} SAR"),
        ("Forecast (weighted)", f"{round(kpis.weighted_pipeline_sar)} SAR"),
        ("Open pipeline", f"{kpis.open_pipeline_sar} SAR"),
        ("Active deals", str(kpis.active_deals)),
        ("Won", str(kpis.won_deals)),
        ("Stalled", str(kpis.stalled_deals)),
        ("Win rate", f"{round(kpis.win_rate * 100)}%"),
    ]
    cards = "\n".join(
        f"<div class='card'><div class='k'>{esc(label)}</div><div class='v'>{esc(val)}</div></div>"
        for label, val in kpi_cards
    )

    return f"""<!doctype html>
<html lang="en"><head><meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Dealix Command Room — {d}</title>
<style>
:root {{ --bg:#0b0e14; --panel:#151a23; --ink:#e6edf3; --muted:#8b98a9; --line:#232c39;
        --ok:#2ea043; --warn:#d29922; --lock:#58a6ff; }}
@media (prefers-color-scheme: light) {{
  :root {{ --bg:#f6f8fa; --panel:#fff; --ink:#1f2328; --muted:#656d76; --line:#d0d7de; }}
}}
* {{ box-sizing:border-box; }}
body {{ margin:0; background:var(--bg); color:var(--ink);
       font:15px/1.5 -apple-system,Segoe UI,Roboto,Helvetica,Arial,sans-serif; }}
.wrap {{ max-width:1000px; margin:0 auto; padding:24px 16px 64px; }}
h1 {{ font-size:22px; margin:0 0 4px; }}
.sub {{ color:var(--muted); margin:0 0 20px; }}
.grid {{ display:grid; grid-template-columns:repeat(auto-fit,minmax(140px,1fr)); gap:10px; margin-bottom:24px; }}
.card {{ background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:14px; }}
.card .k {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.04em; }}
.card .v {{ font-size:22px; font-weight:650; margin-top:6px; }}
h2 {{ font-size:16px; margin:28px 0 10px; }}
.tablewrap {{ overflow-x:auto; border:1px solid var(--line); border-radius:10px; }}
table {{ width:100%; border-collapse:collapse; min-width:640px; }}
th,td {{ text-align:left; padding:9px 12px; border-bottom:1px solid var(--line); }}
th {{ color:var(--muted); font-size:12px; text-transform:uppercase; letter-spacing:.04em; }}
td.num {{ text-align:right; font-variant-numeric:tabular-nums; }}
.stage {{ font-size:12px; padding:2px 8px; border:1px solid var(--line); border-radius:999px; }}
tr.stalled td {{ background:color-mix(in srgb, var(--warn) 10%, transparent); }}
details {{ background:var(--panel); border:1px solid var(--line); border-radius:10px; padding:10px 14px; margin:8px 0; }}
summary {{ cursor:pointer; font-weight:600; }}
pre {{ white-space:pre-wrap; background:transparent; color:var(--ink); margin:10px 0 0; }}
.muted {{ color:var(--muted); }}
.safe {{ margin-top:28px; padding:12px 14px; border:1px dashed var(--line); border-radius:10px; color:var(--muted); font-size:13px; }}
</style></head>
<body><div class="wrap">
<h1>Dealix Command Room</h1>
<p class="sub">{d} · autonomous cycle · draft-only · approval-first</p>
<div class="grid">{cards}</div>
<h2>Today's top actions</h2>
<div class="tablewrap"><table>
<thead><tr><th>#</th><th>Account</th><th>Stage</th><th>Next best action</th><th>Score</th><th></th></tr></thead>
<tbody>{table}</tbody></table></div>
<h2>Approval queue (drafts)</h2>
{approvals_html}
<div class="safe">No message was sent, nothing was published, no customer was charged, no production
change was made. Revenue is recognized only on a real <code>payment_received</code> event.</div>
</div></body></html>
"""
