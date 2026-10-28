from decimal import Decimal
import json
rows={'2025H1':(4868,1338,331,5875),'2025FY':(4868,2488,681,6675),'2026H1':(6675,800,322,7153)}
out={}
for p,(s,a,x,e) in rows.items():
 assert s+a-x==e
 # Illustrative unique-operator, no-reentry model: starters' exits range max(0,x-a) to min(x,s).
 lower=Decimal(s-min(x,s))/Decimal(s)
 upper=Decimal(s-max(0,x-a))/Decimal(s)
 out[p]={'start':s,'added':a,'exited':x,'end':e,'bridge_ok':True,'conditional_start_cohort_retention_lower':str(lower),'conditional_start_cohort_retention_upper':str(upper)}
for s,a,x,e in [(9914,1570,305,11179),(13554,1318,521,14351)]:assert s+a-x==e
# Two distinct 2026H1 allocations reproduce identical observed bridge.
s,a,x,e=rows['2026H1']
assert (s-x)+a == s+(a-x)==e
out['2026H1_counterexample']={'all_exits_are_starters':{'remaining_starters':s-x,'remaining_new':a},'all_exits_are_new':{'remaining_starters':s,'remaining_new':a-x}}
print(json.dumps(out,ensure_ascii=False,indent=2))
