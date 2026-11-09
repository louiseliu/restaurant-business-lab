from decimal import Decimal as D
import json
from pathlib import Path
hourly=D('4.01'); tariff=D('1.64'); days=D('365'); monthly_rent=D('1200')
rent=monthly_rent*12
out={'type':'Conditional calculation; not measured store results','currency':'HKD','annual_rent':str(rent),'source_rounded_annual_kwh':'16656','gross_from_rounded_kwh':str(D('16656')*tariff),'two_item_difference':str(D('16656')*tariff-rent),'break_even_hours_per_day':str(rent/(hourly*tariff*days)),'scenarios':[]}
for h in ['4','6','8','11.38']:
 gross=hourly*tariff*days*D(h)
 out['scenarios'].append({'hours_per_day':h,'gross':str(gross),'gross_less_rent':str(gross-rent)})
Path(__file__).with_name('calculations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,indent=2))
