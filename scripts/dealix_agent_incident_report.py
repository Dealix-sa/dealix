import argparse, json, uuid
from pathlib import Path
from datetime import datetime, timezone
P=Path('data/agents/agent_incidents.jsonl'); P.parent.mkdir(parents=True, exist_ok=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--severity', choices=['low','medium','high'], required=True); ap.add_argument('--summary', required=True); ap.add_argument('--owner', default='founder')
    a=ap.parse_args(); rec={'incident_id':'agent_inc_'+uuid.uuid4().hex[:10], 'severity':a.severity, 'summary':a.summary, 'owner':a.owner, 'created_at':datetime.now(timezone.utc).isoformat(), 'status':'open'}
    with P.open('a',encoding='utf-8') as f: f.write(json.dumps(rec, ensure_ascii=False)+'\n')
    print('Logged incident', rec['incident_id'])
