import argparse
from pathlib import Path

REQUIRED = ['APP_ENV','NEXT_PUBLIC_APP_URL','DATABASE_URL','AUTH_SECRET','ENCRYPTION_KEY']
SENSITIVE = ['SECRET','KEY','TOKEN','PASSWORD']

def parse_env(path):
    values = {}
    for line in Path(path).read_text(encoding='utf-8').splitlines():
        line=line.strip()
        if not line or line.startswith('#') or '=' not in line: continue
        k,v=line.split('=',1)
        values[k.strip()] = v.strip()
    return values

parser=argparse.ArgumentParser()
parser.add_argument('--env-file', default='.env.example')
args=parser.parse_args()
values=parse_env(args.env_file)
missing=[k for k in REQUIRED if k not in values]
if missing:
    print('Missing required env keys:', ', '.join(missing)); raise SystemExit(1)
weak=[]
for k,v in values.items():
    if any(s in k for s in SENSITIVE) and v and v.lower() in {'changeme','change-me','change-me-local-only','test'}:
        weak.append(k)
print('Env keys:', len(values))
if weak: print('Weak placeholder secrets allowed only in local example:', ', '.join(weak))
print('OK: env contract parsed')
