from decimal import Decimal
import json
p = Decimal('200000')
u = p * Decimal('0.65')
d = p * Decimal('0.35')
assert u + d == p
print(json.dumps({'assumption':'Illustration using approximate published equipment total; not actual contract cash flow','equipment_total_rmb':str(p),'upfront_rmb':str(u),'deferred_rmb':str(d),'installment_count':24,'monthly_rmb_unrounded':str(d/24),'total_check':u+d==p},ensure_ascii=False,indent=2))
