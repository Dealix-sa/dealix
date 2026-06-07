import json
from pathlib import Path
clients=[{'client':'Pilot Client','usage':70,'outcome':60,'relationship':75,'risk':25}]
out=[]
for c in clients:
    health=round((c['usage']+c['outcome']+c['relationship']+(100-c['risk']))/4)
    c['health_score']=health
    c['status']='green' if health>=75 else 'yellow' if health>=55 else 'red'
    out.append(c)
Path('out/customer_success').mkdir(parents=True, exist_ok=True)
Path('out/customer_success/health_scores.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8')
print('Customer Success Health')
for c in out: print(f"{c['client']}: {c['health_score']} ({c['status']})")
