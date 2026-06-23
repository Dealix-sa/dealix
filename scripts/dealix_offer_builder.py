#!/usr/bin/env python3
import argparse
from datetime import date
from pathlib import Path

TEMPLATES = {
 'diagnostic': 'templates/offers/diagnostic_offer_ar.md',
 'pilot': 'templates/offers/pilot_offer_ar.md',
 'executive': 'templates/offers/executive_os_offer_ar.md',
 'custom': 'templates/offers/custom_ai_offer_ar.md',
 'enterprise': 'templates/offers/enterprise_offer_ar.md',
}

ap=argparse.ArgumentParser()
ap.add_argument('--company', required=True)
ap.add_argument('--package', choices=TEMPLATES.keys(), required=True)
ap.add_argument('--sector', default='')
ap.add_argument('--pain', required=True)
args=ap.parse_args()

t=Path(TEMPLATES[args.package]).read_text(encoding='utf-8')
out=t.replace('{{company}}', args.company).replace('{{sector}}', args.sector).replace('{{pain}}', args.pain).replace('{{date}}', str(date.today()))
outdir=Path('out/offers'); outdir.mkdir(parents=True, exist_ok=True)
file=outdir / f"{args.company.replace(' ','_')}_{args.package}_offer.md"
file.write_text(out, encoding='utf-8')
print(f'Wrote {file}')
