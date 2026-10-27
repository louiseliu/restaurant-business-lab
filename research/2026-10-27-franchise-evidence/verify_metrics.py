"""Reproduce arithmetic only; not a model of franchisee profitability.
Sources and scopes: sources.json. Run with Python 3 standard library.
"""
import json
from pathlib import Path
from decimal import Decimal
D = Decimal
r = {
  'mixue_franchise_store_bridge': {
    'beginning_2026':59785, 'openings_h1':5455, 'closures_h1':1289,
    'calculated_ending':59785+5455-1289, 'reported_ending':63951,
    'check':59785+5455-1289==63951,
  },
  'mixue_franchise_store_yoy_growth_pct': float((D(63951)/D(52996)-1)*100),
  'mixue_h1_group_revenue_growth_pct': float((D(15215804)/D(14874809)-1)*100),
  'mixue_h1_group_profit_growth_pct': float((D(2319272)/D(2718214)-1)*100),
  'mixue_goods_and_equipment_share_of_group_revenue_pct': float((D(14264907)+D(532656))/D(15215804)*100),
  'luckin_q2_partnership_revenue_components_mn_rmb': {
    'materials':2402.2, 'delivery_services':542.1, 'profit_sharing_royalty':492.1,
    'equipment':203.4, 'franchise_other_services':28.0,
    'rounded_components_sum':float(sum(map(D,['2402.2','542.1','492.1','203.4','28.0']))),
    'reported_rounded_total':3667.8,
    'rounding_residual_mn_rmb':float(sum(map(D,['2402.2','542.1','492.1','203.4','28.0']))-D('3667.8')),
  },
  'luckin_partnership_store_yoy_growth_pct':float((D(12576)/D(9238)-1)*100),
}
assert r['mixue_franchise_store_bridge']['check']
assert abs(r['mixue_h1_group_revenue_growth_pct']-2.3)<0.05
assert abs(r['mixue_h1_group_profit_growth_pct']+14.7)<0.05
assert abs(r['luckin_q2_partnership_revenue_components_mn_rmb']['rounding_residual_mn_rmb'])<=0.1
out=Path(__file__).with_name('calculation-results.json')
out.write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(r,ensure_ascii=False,indent=2))
print('PASS: source arithmetic checks; no franchisee profit inferred.')
