import json
from fractions import Fraction
from pathlib import Path

r = {
    "scenario_type": "作者构造，非餐厅实测；同一批60笔订单，只改变统计分母",
    "orders": 60,
    "unfiltered_entries": 120,
    "eligible_entries_after_filtering": 100,
    "old_ratio": float(Fraction(60, 120)),
    "new_ratio": float(Fraction(60, 100)),
    "percentage_point_change": float((Fraction(60, 100) - Fraction(60, 120)) * 100),
    "relative_change_percent": float((Fraction(60, 100) / Fraction(60, 120) - 1) * 100),
    "additional_orders": 0,
    "four_diners_one_order_ratio": float(Fraction(1, 4)),
    "four_diners_one_order_note": "假设四人均用餐并合付一单；1单/4人不能解释为仅一人消费",
}
assert r["old_ratio"] == 0.5 and r["new_ratio"] == 0.6
assert r["percentage_point_change"] == 10.0 and r["relative_change_percent"] == 20.0
assert r["additional_orders"] == 0 and r["four_diners_one_order_ratio"] == 0.25
Path(__file__).with_name("scenarios.json").write_text(
    json.dumps(r, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
)
print("Six scenario assertions passed.")

