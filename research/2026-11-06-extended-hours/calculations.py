"""Illustrative assumptions only; no real shop observations. Python standard library."""
import json
from pathlib import Path
base=dict(new_slot_orders=30, contribution_per_order=18, displaced_orders=4, old_contribution_per_order=18, extra_staff=210, utilities=45, waste=30, equipment_reserve=15, owner_hours=3, owner_hour_value=50)
def calc(name, **changes):
 d=base|changes
 cash=d['new_slot_orders']*d['contribution_per_order']-d['displaced_orders']*d['old_contribution_per_order']-d['extra_staff']-d['utilities']-d['waste']
 sustainable=cash-d['equipment_reserve']-d['owner_hours']*d['owner_hour_value']
 threshold=(d['displaced_orders']*d['old_contribution_per_order']+d['extra_staff']+d['utilities']+d['waste']+d['equipment_reserve']+d['owner_hours']*d['owner_hour_value'])/d['contribution_per_order']
 return dict(scenario=name,assumptions=d,cash_increment=cash,after_equipment_reserve=cash-d['equipment_reserve'],economic_surplus=sustainable,break_even_orders=threshold)
rows=[calc('owner_covers'),calc('paid_handoff',extra_staff=330,owner_hours=.5),calc('handoff_service_loss',extra_staff=330,owner_hours=.5,new_slot_orders=26),calc('strong_slot_handoff',extra_staff=330,owner_hours=.5,new_slot_orders=36)]
out={'scope':'One added operating slot; all amounts CNY. Hypothetical, pre-income-tax, steady operation excluding one-off launch outlays. Equipment reserve is not current cash expense.','results':rows}
Path(__file__).with_name('calculations.json').write_text(json.dumps(out,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(out,ensure_ascii=False,indent=2))
