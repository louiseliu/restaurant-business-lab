"""Synthetic rent-premium comparison, not observed restaurant data."""
import json
from decimal import Decimal
from pathlib import Path

D = Decimal
days = D('30')
rent_premium = D('6000')
scenarios = [
    ('base_incremental_demand', D('28'), D('10')),
    ('lower_contribution', D('28'), D('6')),
    ('capacity_limited', D('15'), D('10')),
]
result = {
    'data_status': 'author_constructed_synthetic_examples_only',
    'currency': 'CNY',
    'period': 'month',
    'assumptions': {
        'operating_days': int(days),
        'monthly_rent_premium': int(rent_premium),
        'baseline_contribution_per_incremental_order': 10,
        'other_cost_differences': 0,
        'limits': '差额比较，非整店利润、回本期或工具准确率；实际新增整班人力、物业、装修及资金需求需另计。'
    },
    'required_average_incremental_orders_per_day': str(rent_premium / (days * D('10'))),
    'scenarios': []
}
for name, orders, contribution in scenarios:
    gross = days * orders * contribution
    result['scenarios'].append({
        'name': name,
        'realized_incremental_orders_per_day': int(orders),
        'contribution_per_order': int(contribution),
        'monthly_incremental_contribution': int(gross),
        'net_difference_after_rent_premium': int(gross-rent_premium)
    })
assert result['required_average_incremental_orders_per_day'] == '20'
assert [x['net_difference_after_rent_premium'] for x in result['scenarios']] == [2400,-960,-1500]
out=Path(__file__).with_name('calculation-results.json')
out.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
