import datetime
import json
from pathlib import Path

metrics={}
pp=Path('data/analytics/daily_metrics.jsonl')
if pp.exists():
    lines=[l for l in pp.read_text(encoding='utf-8').splitlines() if l.strip()]
    metrics['daily_metric_rows']=len(lines)
metrics['has_v5_prospects']=Path('data/prospects/v5_imported_prospects.csv').exists()
md = f"# Dealix Weekly CEO Packet\n\nDate: {datetime.date.today().isoformat()}\n\n## Executive Summary\nDealix focus remains: generate qualified demand, convert it through diagnostic/pilot, and expand into retainers.\n\n## Metrics Snapshot\n```json\n{json.dumps(metrics,ensure_ascii=False,indent=2)}\n```\n\n## CEO Decisions This Week\n1. Select one vertical to focus.\n2. Review top 20 high-fit prospects.\n3. Push 5 diagnostic conversations.\n4. Convert one proof into case study.\n5. Remove one workflow or channel that is not producing.\n\n## Risks\n- Too many verticals at once.\n- Weak follow-up discipline.\n- Technical work replacing sales activity.\n"
Path('out/ceo').mkdir(parents=True, exist_ok=True)
Path('out/ceo/weekly_ceo_packet.md').write_text(md,encoding='utf-8')
print('Wrote out/ceo/weekly_ceo_packet.md')
