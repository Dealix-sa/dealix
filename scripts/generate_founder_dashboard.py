#!/usr/bin/env python3
"""Generate founder daily dashboard (read-only report)."""

import csv
import json
from datetime import datetime
from pathlib import Path


def read_warm_intros() -> list[dict]:
    """Read warm intro targets from CSV."""
    csv_path = Path(__file__).parents[1] / "company" / "runtime" / "warm_intro_targets.csv"

    if not csv_path.exists():
        return []

    try:
        with open(csv_path, encoding='utf-8') as f:
            reader = csv.DictReader(f)
            return list(reader) if reader else []
    except (OSError, csv.Error, UnicodeDecodeError):
        return []

def calculate_metrics(targets: list[dict]) -> dict:
    """Calculate key metrics from warm intro data."""
    if not targets:
        return {
            "total_targets": 0,
            "contacted": 0,
            "diagnostics_completed": 0,
            "pilots_signed": 0,
            "conversion_rate": "—",
            "pipeline_value_sar": 0,
            "status_breakdown": {}
        }

    total = len(targets)
    contacted = sum(1 for t in targets if t.get('date_sent', '').strip())
    diagnostics = sum(1 for t in targets if t.get('outcome', '').strip() and t.get('status') in ['Completed Diagnostic', 'Pilot Signed'])
    pilots = sum(1 for t in targets if t.get('status') == 'Pilot Signed' or (t.get('outcome') and t.get('outcome').strip().lower() == 'yes'))

    status_breakdown = {}
    for t in targets:
        status = t.get('status', 'Ready')
        status_breakdown[status] = status_breakdown.get(status, 0) + 1

    conversion_rate = f"{(diagnostics / contacted * 100):.1f}%" if contacted > 0 else "—"
    pipeline_value = pilots * 499  # 499 SAR per pilot

    return {
        "total_targets": total,
        "contacted": contacted,
        "diagnostics_completed": diagnostics,
        "pilots_signed": pilots,
        "conversion_rate": conversion_rate,
        "pipeline_value_sar": pipeline_value,
        "status_breakdown": status_breakdown
    }

def generate_html_report(metrics: dict, targets: list[dict]) -> str:
    """Generate HTML founder dashboard."""
    html = f"""<!DOCTYPE html>
<html lang="ar" dir="rtl">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Dealix Founder Dashboard</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif; background: #f5f7fa; color: #1a1a1a; padding: 20px; }}
        .container {{ max-width: 1200px; margin: 0 auto; }}
        h1 {{ font-size: 2em; margin-bottom: 10px; color: #0066cc; }}
        .subtitle {{ color: #666; margin-bottom: 30px; }}
        .metrics {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 20px; margin-bottom: 40px; }}
        .metric-card {{ background: white; border-left: 4px solid #0066cc; padding: 20px; border-radius: 4px; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .metric-value {{ font-size: 2.5em; font-weight: bold; color: #0066cc; }}
        .metric-label {{ color: #666; font-size: 0.9em; margin-top: 5px; }}
        .table {{ background: white; border-collapse: collapse; width: 100%; margin-top: 30px; border-radius: 4px; overflow: hidden; box-shadow: 0 1px 3px rgba(0,0,0,0.1); }}
        .table th {{ background: #f8f9fa; padding: 12px; text-align: right; font-weight: 600; border-bottom: 1px solid #e0e0e0; }}
        .table td {{ padding: 12px; border-bottom: 1px solid #e0e0e0; }}
        .table tr:hover {{ background: #f8f9fa; }}
        .status-ready {{ color: #999; }}
        .status-sent {{ color: #ff9800; }}
        .status-completed {{ color: #4caf50; }}
        .status-signed {{ color: #0066cc; font-weight: bold; }}
        .footer {{ text-align: center; color: #999; margin-top: 40px; font-size: 0.85em; }}
        .last-updated {{ color: #999; margin-bottom: 20px; }}
    </style>
</head>
<body>
    <div class="container">
        <h1>Dealix Founder Dashboard</h1>
        <div class="last-updated">Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</div>

        <div class="metrics">
            <div class="metric-card">
                <div class="metric-value">{metrics['total_targets']}</div>
                <div class="metric-label">Total Warm Intros</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics['contacted']}</div>
                <div class="metric-label">Contacted</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics['diagnostics_completed']}</div>
                <div class="metric-label">Diagnostics Done</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics['pilots_signed']}</div>
                <div class="metric-label">Pilots Signed</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics['conversion_rate']}</div>
                <div class="metric-label">Conversion Rate</div>
            </div>
            <div class="metric-card">
                <div class="metric-value">{metrics['pipeline_value_sar']:,}</div>
                <div class="metric-label">Pipeline Value (SAR)</div>
            </div>
        </div>

        <h2>Status Breakdown</h2>
        <table class="table">
            <tr>
                <th>Status</th>
                <th>Count</th>
            </tr>
"""

    for status, count in sorted(metrics['status_breakdown'].items()):
        html += f"<tr><td>{status}</td><td>{count}</td></tr>"

    html += """
        </table>

        <h2>Warm Intro Tracking</h2>
        <table class="table">
            <tr>
                <th>#</th>
                <th>Name</th>
                <th>Company</th>
                <th>Role</th>
                <th>Sector</th>
                <th>Status</th>
                <th>Sent</th>
                <th>Outcome</th>
                <th>Next Step</th>
            </tr>
"""

    for target in targets:
        status_class = {
            'Ready': 'status-ready',
            'Sent': 'status-sent',
            'Completed Diagnostic': 'status-completed',
            'Pilot Signed': 'status-signed',
            'Declined': 'status-ready'
        }.get(target.get('status', ''), '')

        html += f"""<tr>
                <td>{target.get('id', '')}</td>
                <td>{target.get('name', '')}</td>
                <td>{target.get('company', '')}</td>
                <td>{target.get('role', '')}</td>
                <td>{target.get('sector', '')}</td>
                <td class="{status_class}">{target.get('status', '')}</td>
                <td>{target.get('date_sent', '')}</td>
                <td>{target.get('outcome', '')}</td>
                <td>{target.get('next_step', '')}</td>
            </tr>
"""

    html += """
        </table>

        <div class="footer">
            <p>Dealix Founder Dashboard — Updated daily</p>
            <p>Next Review: Day 10 (2026-06-27)</p>
        </div>
    </div>
</body>
</html>
"""

    return html

def main():
    """Generate and save founder dashboard."""
    targets = read_warm_intros()
    metrics = calculate_metrics(targets)
    html = generate_html_report(metrics, targets)

    output_path = Path(__file__).parents[1] / "company" / "runtime" / "founder_dashboard.html"
    output_path.parent.mkdir(parents=True, exist_ok=True)

    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"✅ Founder dashboard generated: {output_path}")
    print(f"Metrics: {metrics['contacted']} contacted, {metrics['diagnostics_completed']} diagnostics, {metrics['pilots_signed']} pilots signed")

    return 0

if __name__ == '__main__':
    exit(main())
