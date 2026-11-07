"""Author-created RMB scenarios; not case observations or accounting advice."""
import json
from decimal import Decimal as D
from pathlib import Path

price = D('20.00')
merchant_rate = D('0.90')
discounted = price * merchant_rate
rows = []
for subsidy in (D('1.50'), D('3.00')):
    customer = discounted - subsidy
    receipts = customer + subsidy
    assert receipts == discounted
    rows.append({
        'list_price_yuan': float(price),
        'merchant_discount_yuan': float(price-discounted),
        'customer_payment_yuan': float(customer),
        'fiscal_receivable_yuan': float(subsidy),
        'total_meal_receipts_after_full_redemption_yuan': float(receipts),
    })
daily_eligible_meals = 60
per_meal_subsidy = D('1.50')
balances = [
    {'day': day, 'unredeemed_subsidy_yuan': float(day*daily_eligible_meals*per_meal_subsidy)}
    for day in (30, 60, 90)
]
assert [x['unredeemed_subsidy_yuan'] for x in balances] == [2700.0, 5400.0, 8100.0]
result = {
    'classification': 'author_hypothetical_not_observed',
    'currency': 'CNY',
    'meal_receipts': rows,
    'receivable_scenario': {
        'daily_eligible_meals': daily_eligible_meals,
        'per_meal_subsidy_yuan': float(per_meal_subsidy),
        'assumptions': [
            'Every included transaction is eligible, within once-per-day and other applicable limits.',
            'No redemption cash is received during the illustrated observation interval.',
            'No refunds, reversals, duplicate claims or eligibility adjustments.',
            '90 days is an illustrative interval, not a promised or observed payment delay.',
            'Receivable balance is not total working capital and is not an accounting recognition instruction.'
        ],
        'balances': balances
    }
}
Path(__file__).with_name('calculations.json').write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
print(json.dumps(result, ensure_ascii=False, indent=2))
