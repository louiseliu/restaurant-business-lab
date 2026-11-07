"""Recompute five explicitly author-defined hypothetical scenarios.

No private records, actual store results, quotations, or insurance advice.
"""
import json
from decimal import Decimal
from pathlib import Path

def calculate(name, eligible_share, original_rate, months, basis):
    monthly_gross = Decimal("100000")
    new_rate = Decimal("0")
    savings = monthly_gross * Decimal(eligible_share) * (Decimal(original_rate) - new_rate) * months
    return {
        "name": name,
        "monthly_total_rmb": str(monthly_gross),
        "eligible_share": eligible_share,
        "baseline_rate": original_rate,
        "new_rate": str(new_rate),
        "effective_months": months,
        "fee_difference_rmb": str(savings.quantize(Decimal("0.01"))),
        "basis": basis,
    }

rows = [
    calculate("全部流水优惠一年", "1", "0.003", 12, "研究者假设基准情景；非实际商户数据或报价"),
    calculate("只有一半流水符合条件", "0.5", "0.003", 12, "研究者假设敏感性情景"),
    calculate("原费率已经较低", "1", "0.002", 12, "研究者假设敏感性情景"),
    calculate("优惠仅持续半年", "1", "0.003", 6, "研究者假设敏感性情景"),
    calculate("原渠道已免费", "1", "0", 12, "研究者假设敏感性情景"),
]
assert [Decimal(r["fee_difference_rmb"]) for r in rows] == [3600, 1800, 2400, 1800, 0]
out = {
    "scope": "仅计算手续费差额；未扣套餐、保险、设备、运维、迁移；不代表AI收益或净节省",
    "formula": "monthly_total_rmb * eligible_share * (baseline_rate - new_rate) * effective_months",
    "limitation": "假定单一费率、无封顶阶梯退款及其他调整；实际合同需逐项计算",
    "scenarios": rows,
}
Path(__file__).with_name("calculations.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(json.dumps(out, ensure_ascii=False, indent=2))
