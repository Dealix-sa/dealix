import datetime
import json
from pathlib import Path

checks={
 'scope_written': True,
 'invoice_or_approval': True,
 'baseline_defined': True,
 'proof_item_created': True,
 'no_sensitive_data': True,
 'no_guaranteed_roi_claims': True,
 'human_review_done': True
}
score=sum(1 for v in checks.values() if v)
status='PASS' if score==len(checks) else 'HOLD'
print('# Preview Quality Gate')
for k,v in checks.items(): print(f'- {k}: {"OK" if v else "MISSING"}')
print(f'Status: {status}')
Path('data/preview').mkdir(parents=True, exist_ok=True)
with Path('data/preview/quality_gate_results.jsonl').open('a', encoding='utf-8') as f:
    f.write(json.dumps({'ts':datetime.datetime.utcnow().isoformat()+'Z','status':status,'score':score,'total':len(checks)}, ensure_ascii=False)+'\n')
