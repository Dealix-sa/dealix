import argparse, datetime
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
md = "# Business Case — {account}\n\n> تقدير تشغيلي وليس ضمانًا للإيراد.\n\n## الفرضيات\n- Monthly leads: {monthly_leads}\n- Average deal value: {avg:,.0f} SAR\n- Conservative uplift assumption: {uplift:.1%}\n\n## تقدير الأثر الشهري\n| السيناريو | قيمة فرص/تحسين مقدرة |\n|---|---:|\n| Conservative | {cons:,.0f} SAR |\n| Expected | {exp:,.0f} SAR |\n| Aggressive | {agg:,.0f} SAR |\n\n## توصية Dealix\nابدأ Pilot لمدة 14 يوم لإثبات التقاط الفرص، وضوح المتابعة، وجودة التقارير قبل أي توسع.\n\nCreated: {created}Z\n".format(account=args.account, monthly_leads=args.monthly_leads, avg=args.avg_deal_value, uplift=args.uplift, cons=conservative, exp=expected, agg=aggressive, created=datetime.datetime.utcnow().isoformat())
out=Path('out/business_cases'); out.mkdir(parents=True, exist_ok=True)
fn=out/(args.account.replace(' ','_')+'_business_case.md')
fn.write_text(md,encoding='utf-8')
print(f'Wrote {fn}')
