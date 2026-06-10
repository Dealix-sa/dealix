#!/usr/bin/env python3
import argparse, json, re
from pathlib import Path
from datetime import date
ap=argparse.ArgumentParser()
ap.add_argument('--client-label', required=True)
ap.add_argument('--sector', required=True)
ap.add_argument('--problem', required=True)
ap.add_argument('--intervention', required=True)
ap.add_argument('--result', required=True)
args=ap.parse_args()
slug=re.sub(r'[^a-zA-Z0-9]+','-',args.client_label).strip('-').lower()
md=f"""# دراسة حالة: {args.client_label}\n\nالتاريخ: {date.today()}\n\n## القطاع\n{args.sector}\n\n## المشكلة\n{args.problem}\n\n## تدخل Dealix\n{args.intervention}\n\n## النتيجة\n{args.result}\n\n## الدليل المطلوب\n- لقطة قبل/بعد\n- تقرير أسبوعي\n- شهادة عميل عند الإمكان\n"""
out=Path('docs/case-studies/generated'); out.mkdir(parents=True, exist_ok=True)
(out/f'{slug}.md').write_text(md, encoding='utf-8')
print(out/f'{slug}.md')
