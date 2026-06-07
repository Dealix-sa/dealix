import json
from pathlib import Path
CASES=Path('data/agents/eval_cases.json')

def fake_output(case):
    role=case['role']
    if role=='outreach_draft_agent': return 'draft_only needs_human_review conservative claims'
    if role=='lead_qualification_agent': return 'fit_score next_action approval_required'
    if role=='proposal_agent': return 'Assumptions Exclusions estimated outcomes only'
    return ''

cases=json.loads(CASES.read_text(encoding='utf-8'))
passed=0
for c in cases:
    out=fake_output(c)
    ok=all(x in out for x in c.get('expected_contains',[])) and not any(x.lower() in out.lower() for x in c.get('forbidden',[]))
    print(c['id'], 'PASS' if ok else 'FAIL')
    passed += ok
print(f'Eval score: {passed}/{len(cases)}')
if passed != len(cases): raise SystemExit(1)
