import argparse, json, uuid
from pathlib import Path
from datetime import datetime, timezone
Q=Path('data/agents/task_queue.json')
Q.parent.mkdir(parents=True, exist_ok=True)

def load():
    if not Q.exists(): return []
    try: return json.loads(Q.read_text(encoding='utf-8') or '[]')
    except Exception: return []

def save(items): Q.write_text(json.dumps(items, ensure_ascii=False, indent=2), encoding='utf-8')

def add(role, task, priority='medium'):
    items=load()
    item={
      'id':'task_'+uuid.uuid4().hex[:10],
      'created_at':datetime.now(timezone.utc).isoformat(),
      'role':role,'priority':priority,'input':task,
      'status':'queued','output_path':None
    }
    items.append(item); save(items); print('Queued', item['id'], role)

def seed():
    add('crm_research_agent','Research شركة تدريب الرياض and list missing info','high')
    add('outreach_draft_agent','Draft first-touch WhatsApp for qualified training prospect','high')
    add('ceo_briefing_agent','Summarize today pipeline and top 3 actions','medium')

if __name__=='__main__':
    ap=argparse.ArgumentParser(); ap.add_argument('--seed', action='store_true'); ap.add_argument('--role'); ap.add_argument('--task'); ap.add_argument('--priority', default='medium')
    a=ap.parse_args()
    if a.seed: seed()
    elif a.role and a.task: add(a.role,a.task,a.priority)
    else:
        print(json.dumps(load(), ensure_ascii=False, indent=2))
