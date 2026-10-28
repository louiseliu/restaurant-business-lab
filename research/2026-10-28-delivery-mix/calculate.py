"""Conditional delivery-cost-rate identity; inputs are rounded disclosures, not raw data."""
from decimal import Decimal, getcontext
import json
from pathlib import Path
getcontext().prec = 28
old_mix = Decimal('0.45')
new_mix = Decimal('0.54')
required_ratio = old_mix / new_mix
result = {
    'status': 'conditional_calculation_not_observed_cost_change',
    'periods': ['2025Q2', '2026Q2'],
    'source': 'https://ir.yumchina.com/news-releases/news-release-details/yum-china-reports-second-quarter-2026-results',
    'mix_definition': 'delivery accounting sales / total Company sales; not delivery order share',
    'input_precision': 'approximate published percentages; outputs must be presented as approximate',
    'old_mix': str(old_mix),
    'new_mix': str(new_mix),
    'identity': 'rider_cost/total_sales = delivery_sales_mix * rider_cost_per_delivery_order / delivery_accounting_sales_per_delivery_order',
    'required_new_to_old_cost_per_order_divided_by_delivery_ticket_ratio': str(required_ratio),
    'required_relative_reduction': str(Decimal(1) - required_ratio),
    'required_relative_reduction_percent_display': 'approximately 16.7%',
    'assumptions': [
        'All variables refer to the same restaurant scope and accounting period.',
        'Delivery sales and rider costs are consistently defined in both periods.',
        'Rider cost rate is held constant, not estimated from disclosed margins.',
        'Accounting delivery sales per order is not verified net merchant cash receipts.'
    ],
    'not_inferred': [
        'Actual rider cost reduction', 'Actual delivery contribution margin',
        'Causation from the separate 2025 management commentary',
        'Platform commission, packaging, discount, or kitchen capacity costs'
    ]
}
assert old_mix * Decimal(1) == new_mix * required_ratio
path = Path(__file__).with_name('calculation.json')
path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
