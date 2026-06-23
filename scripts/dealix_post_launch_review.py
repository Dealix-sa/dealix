import datetime
import json
from pathlib import Path

metrics=json.loads(Path('data/preview/launch_week_metrics.json').read_text(encoding='utf-8'))
score=0
score += 1 if metrics.get('prospects_reviewed',0)>=50 else 0
score += 1 if metrics.get('drafts_created',0)>=10 else 0
score += 1 if metrics.get('incidents',0)==0 else 0
score += 1 if metrics.get('proof_reports_sent',0)>=0 else 0
status='CONTINUE_PREVIEW' if score>=3 else 'HOLD_AND_FIX'
print('# Post Launch Review')
print(f'Score: {score}/4')
print(f'Decision: {status}')
Path('data/preview').mkdir(exist_ok=True, parents=True)
with Path('data/preview/post_launch_reviews.jsonl').open('a',encoding='utf-8') as f:
    f.write(json.dumps({'ts':datetime.datetime.utcnow().isoformat()+'Z','score':score,'decision':status}, ensure_ascii=False)+'\n')
