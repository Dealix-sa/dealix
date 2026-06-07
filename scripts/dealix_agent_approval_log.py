import argparse, json, uuid
from pathlib import Path
from datetime import datetime, timezone
P=Path('data/agents/approvals.jsonl'); P.parent.mkdir(parents=True, exist_ok=True)
if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--task-id', required=True); ap.add_argument('--approver', default='Sami'); ap.add_argument('--decision', choices=['approved','rejected','needs_edit'], required=True); ap.add_argument('--notes', default='')
    a=ap.parse_args(); rec={'approval_id':'approval_'+uuid.uuid4().hex[:10], 'task_id':a.task_id, 'approver':a.approver, 'decision':a.decision, 'notes':a.notes, 'timestamp':datetime.now(timezone.utc).isoformat()}
    with P.open('a',encoding='utf-8') as f: f.write(json.dumps(rec, ensure_ascii=False)+'\n')
    print('Logged approval', rec['approval_id'])
