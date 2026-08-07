import argparse
import datetime
import json
from pathlib import Path

ap=argparse.ArgumentParser()
ap.add_argument('--company', required=True)
ap.add_argument('--vertical', default='training')
ap.add_argument('--employees', type=int, default=50)
ap.add_argument('--monthly_leads', type=int, default=100)
args=ap.parse_args()
score=0
if args.employees>=50: score+=25
if args.monthly_leads>=100: score+=35
if args.vertical in ['training','agencies','real_estate','clinics','professional_services']: score+=20
score+=20
plan={
 'vertical':args.vertical,'employees':args.employees,'monthly_leads':args.monthly_leads,
 'enterprise_fit_score':min(score,100),
 'stakeholders':['CEO/Founder','Sales Manager','Operations Manager','IT/Data reviewer'],
 'hypothesis':'فرص تدخل من قنوات متعددة وتضيع بسبب المتابعة غير الموحدة',
 'recommended_entry_offer':'Executive Diagnostic Workshop ثم Pilot 14 يوم',
 'next_actions':['ابن business case','جهز demo room قطاعي','اكتب رسالة لصاحب القرار','سجل interaction في CRM'],
 'created_at':datetime.datetime.utcnow().isoformat()+'Z'
}
out=Path('out/enterprise'); out.mkdir(parents=True, exist_ok=True)
fn=out/(args.company.replace(' ','_')+'_account_plan.json')
fn.write_text(json.dumps(plan,ensure_ascii=False,indent=2),encoding='utf-8')
print(f'Wrote {fn}')
