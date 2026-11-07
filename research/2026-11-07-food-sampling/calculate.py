"""Recompute public award line items; no ROI or operational effect estimate."""
import json
scale_quantity, scale_unit_yuan = 5, 12000
fridge_quantity, fridge_unit_yuan = 5, 16000
result = {
    "scale_line_yuan": scale_quantity * scale_unit_yuan,
    "fridge_line_yuan": fridge_quantity * fridge_unit_yuan,
    "two_lines_total_yuan": scale_quantity * scale_unit_yuan + fridge_quantity * fridge_unit_yuan,
    "scope": "Two award line items only; not complete sampling-system cost or actual payment."
}
assert result["scale_line_yuan"] == 60000
assert result["fridge_line_yuan"] == 80000
assert result["two_lines_total_yuan"] == 140000
print(json.dumps(result, ensure_ascii=False, indent=2))
