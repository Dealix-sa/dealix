import json
from pathlib import Path

rules=json.loads(Path('data/founder/daily_decision_rules.json').read_text(encoding='utf-8'))
tasks=json.loads(Path('data/founder/founder_tasks.json').read_text(encoding='utf-8'))
weights=rules['priority_weights']

def score(t):
    raw = sum(float(t.get(k,0)) for k in weights)
    return raw
ranked=sorted(tasks, key=score, reverse=True)[:rules.get('daily_task_limit',10)]
out=Path('out/founder'); out.mkdir(parents=True, exist_ok=True)
lines=['# Dealix Top 10 Founder Tasks','']
for i,t in enumerate(ranked,1):
    lines.append(f"{i}. **{t['title']}** — score={score(t):.1f} — source={t.get('source','manual')}")
Path('out/founder/top10_tasks.md').write_text('\n'.join(lines)+'\n', encoding='utf-8')
print('\n'.join(lines))
