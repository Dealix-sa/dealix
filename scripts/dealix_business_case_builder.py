import argparse
import datetime
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('--account', required=True)
ap.add_argument('--monthly_leads', type=int, required=True)
ap.add_argument('--avg_deal_value', type=float, required=True)
ap.add_argument('--uplift', type=float, default=0.05)
args=ap.parse_args()
conservative=args.monthly_leads*args.uplift*args.avg_deal_value
expected=args.monthly_leads*(args.uplift*1.5)*args.avg_deal_value
aggressive=args.monthly_leads*(args.uplift*2.2)*args.avg_deal_value
md = f"# Business Case — {args.account}\n\n> تقدير تشغيلي وليس ضمانًا للإيراد.\n\n## الفرضيات\n- Monthly leads: {args.monthly_leads}\n- Average deal value: {args.avg_deal_value:,.0f} SAR\n- Conservative uplift assumption: {args.uplift:.1%}\n\n## تقدير الأثر الشهري\n| السيناريو | قيمة فرص/تحسين مقدرة |\n|---|---:|\n| Conservative | {conservative:,.0f} SAR |\n| Expected | {expected:,.0f} SAR |\n| Aggressive | {aggressive:,.0f} SAR |\n\n## توصية Dealix\nابدأ Pilot لمدة 14 يوم لإثبات التقاط الفرص، وضوح المتابعة، وجودة التقارير قبل أي توسع.\n\nCreated: {datetime.datetime.utcnow().isoformat()}Z\n"
out=Path('out/business_cases'); out.mkdir(parents=True, exist_ok=True)
fn=out/(args.account.replace(' ','_')+'_business_case.md')
fn.write_text(md,encoding='utf-8')
print(f'Wrote {fn}')
