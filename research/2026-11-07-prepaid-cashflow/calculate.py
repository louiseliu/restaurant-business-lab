from decimal import Decimal
import json
old,new=Decimal('74122'),Decimal('67430')
r={'source_unit':'RMB thousand','prepaid_2024':str(old),'prepaid_2025':str(new),'prepaid_2024_wan':str(old/10),'prepaid_2025_wan':str(new/10),'decrease_wan':str((old-new)/10),'decrease_percent':str(((old-new)/old*100).quantize(Decimal('.01'))),'total_2024':'77334','total_2025':'68502','total_decrease_wan':str(Decimal(77334-68502)/10)}
assert new+1072==68502 and old+3212==77334
assert Decimal(77334)+68502-77334==68502
print(json.dumps(r,ensure_ascii=False,indent=2))
