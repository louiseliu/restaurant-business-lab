"""Independent interval check, public MIXUE interim disclosures; no external dependencies.
Inputs transcribed from HKEX 2025 pp16/46 and 2026 pp18/60 on 2026-10-27.
Continuous-day bounds are sharp infimum/supremum when events cannot occur exactly
at period endpoints. Do not interpret network membership as actual trading days.
"""
from datetime import date
from fractions import Fraction
import json
from pathlib import Path

INPUTS = {
    2025: dict(start=46462, openings=7721, closures=1187, end=52996, goods_rmb_thousand=13843184),
    2026: dict(start=59785, openings=5455, closures=1289, end=63951, goods_rmb_thousand=14264907),
}

def bounds(s, o, c, days):
    assert min(s,o,c,days) >= 0 and s+o >= c
    return days*max(0,s-c), days*(s+o)

for y,v in INPUTS.items():
    assert v['start']+v['openings']-v['closures']==v['end']
    v['days']=(date(y,7,1)-date(y,1,1)).days
    v['store_days_min'],v['store_days_max']=bounds(v['start'],v['openings'],v['closures'],v['days'])
a,b=INPUTS[2025],INPUTS[2026]
r=Fraction(b['goods_rmb_thousand'],a['goods_rmb_thousand'])
lo=Fraction(b['store_days_min'],a['store_days_max'])
hi=Fraction(b['store_days_max'],a['store_days_min'])
# Independent construction of extremal schedules; C <= S in both observed years.
for v in INPUTS.values():
    assert v['closures']<=v['start']
    assert v['store_days_min']==(v['start']-v['closures'])*v['days']
    assert v['store_days_max']==(v['end']+v['closures'])*v['days']
# Edge cases: opened then closed, closures exceeding starting population.
assert bounds(0,10,10,181)==(0,1810)
assert bounds(5,10,10,181)==(0,2715)
assert bounds(5,0,0,181)==(905,905)
assert a['days']==b['days']==181
missing_days=Fraction(b['store_days_min'])-r*a['store_days_max']
result={
 'inputs':INPUTS,
 'goods_growth_pct':float((r-1)*100),
 'network_day_growth_lower_pct':float((lo-1)*100),
 'network_day_growth_upper_pct':float((hi-1)*100),
 'implied_intensity_ratio_lower':float(r/hi),
 'implied_intensity_ratio_upper':float(r/lo),
 'minimum_intensity_decline_pct':float((1-r/lo)*100),
 'extra_goods_revenue_needed_rmb_thousand':float(a['goods_rmb_thousand']*lo-b['goods_rmb_thousand']),
 'extra_goods_revenue_needed_as_pct_reported_2026':float((lo/r-1)*100),
 'excess_2026_network_days_vs_timing_null':float(missing_days),
 'equivalent_full_half_year_stores_to_exclude_if_zero_associated_revenue':float(missing_days/b['days']),
 'minimum_actual_operating_share_ratio_2026_over_2025_for_unchanged_per_operating_day_revenue':float(r/hi),
 'maximum_actual_operating_share_ratio_2026_over_2025_for_unchanged_per_operating_day_revenue':float(r/lo),
 'operating_share_ratio_note':'Upper bound is necessary, not sufficient alone; existence in continuous unrestricted timing/operating model requires q in [r/hi,r/lo]. For fixed actual network days q must equal r divided by the actual exposure ratio.',
 'constant_aggregate_goods_intensity_timing_only_null_feasible':bool(lo<=r<=hi),
 'caution':'Conditional accounting diagnostic, not causal or statistical rejection. Scope/product price, revenue recognition, inventory and actual trading days may vary.'
}
# Necessity versus sufficiency: test equality counterexample and too-small q.
q_upper=r/lo
assert q_upper*lo==r
q_too_small=Fraction(1,2)
assert q_too_small<q_upper and q_too_small*hi<r
for q in [r/hi,(r/hi+r/lo)/2,r/lo]:
    required_exposure=r/q
    assert lo<=required_exposure<=hi
    assert q*required_exposure==r
p=Path(__file__).with_name('bounds-check-results.json')
p.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
