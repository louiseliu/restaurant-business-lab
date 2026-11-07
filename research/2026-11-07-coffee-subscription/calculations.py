"""Illustrative subscription spending, not observed Pret prices or economics."""
from decimal import Decimal
import json
from pathlib import Path

D = Decimal
list_price = D('4')  # Author assumption; not a verified unified Pret price.
old_monthly = D('30')
new_monthly = D('5')
discount_fraction = D('0.5')
new_cup_payment = list_price * (1 - discount_fraction)
rows = []
for cups in (5, 12, 13, 15, 30):
    new_total = new_monthly + new_cup_payment * cups
    rows.append({'cups': cups, 'old_total_gbp': str(old_monthly),
                 'new_total_gbp': str(new_total),
                 'new_minus_old_gbp': str(new_total - old_monthly)})
crossover = (old_monthly - new_monthly) / new_cup_payment
assert crossover == D('12.5')
assert [D(x['new_total_gbp']) for x in rows] == [D('15'), D('29'), D('31'), D('35'), D('65')]
result = {
    'classification': 'author_calculated_hypothetical_scenario',
    'currency': 'GBP',
    'assumptions': {
        'hypothetical_list_price_gbp': str(list_price),
        'old_monthly_fee_gbp': str(old_monthly),
        'new_monthly_fee_gbp': str(new_monthly),
        'discount_fraction': str(discount_fraction),
        'all_cups_eligible': True,
        'same_cup_count_in_both_schemes': True,
        'scope': 'drinks_only_no_food_perks_or_tax_accounting_split',
        'warning': 'Not actual uniform Pret price, customer bill, costs, profits or causal effects.'
    },
    'continuous_spending_crossover_cups': str(crossover),
    'integer_boundary': {'12_cups_new_lower': True, '13_cups_new_higher': True},
    'rows': rows
}
target = Path(__file__).with_name('calculations.json')
target.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps(result, ensure_ascii=False, indent=2))
