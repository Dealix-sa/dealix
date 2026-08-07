import argparse

p=argparse.ArgumentParser()
p.add_argument('--price',type=float,default=499)
p.add_argument('--hours',type=float,default=6)
p.add_argument('--hour-cost',type=float,default=75)
p.add_argument('--tools',type=float,default=0)
a=p.parse_args()
cost=a.hours*a.hour_cost+a.tools
margin=(a.price-cost)/a.price if a.price else 0
print('# Service Margin')
print(f'Revenue SAR: {a.price:.2f}')
print(f'Cost SAR: {cost:.2f}')
print(f'Margin: {margin*100:.1f}%')
print('Decision:', 'OK' if margin>=0.5 else 'Raise price / reduce scope / automate repeated work')
