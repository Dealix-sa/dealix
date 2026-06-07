import argparse
from pathlib import Path
packs={
 'training':'industries/TRAINING_VERTICAL_PACK_AR.md','agencies':'industries/AGENCIES_VERTICAL_PACK_AR.md',
 'real_estate':'industries/REAL_ESTATE_VERTICAL_PACK_AR.md','clinics':'industries/CLINICS_VERTICAL_PACK_AR.md',
 'professional_services':'industries/PROFESSIONAL_SERVICES_VERTICAL_PACK_AR.md'}
p=argparse.ArgumentParser(); p.add_argument('--vertical',required=True,choices=packs.keys()); a=p.parse_args()
path=Path(packs[a.vertical])
print(path.read_text(encoding='utf-8') if path.exists() else 'Pack missing')
