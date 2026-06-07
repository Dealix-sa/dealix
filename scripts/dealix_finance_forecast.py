import argparse
p=argparse.ArgumentParser()
p.add_argument('--pilots',type=int,default=5)
p.add_argument('--pilot-price',type=float,default=499)
p.add_argument('--retainers',type=int,default=2)
p.add_argument('--retainer-price',type=float,default=4500)
p.add_argument('--months',type=int,default=3)
a=p.parse_args()
pilot_rev=a.pilots*a.pilot_price
mrr=a.retainers*a.retainer_price
print('Dealix Finance Forecast')
print('Pilot revenue SAR:', round(pilot_rev,2))
print('MRR SAR:', round(mrr,2))
print(f'{a.months}-month revenue SAR:', round(pilot_rev + mrr*a.months,2))
if a.pilots:
 print('Pilot→Retainer conversion:', f'{a.retainers/a.pilots:.0%}')
