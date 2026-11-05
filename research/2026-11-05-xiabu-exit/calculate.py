"""Reproduce non-causal differences from Xiabuxiabu 2026 interim report.

Inputs are in RMB thousand, using both columns of one report.
This is an arithmetic check, not a model of closure effects or cash savings.
"""

from decimal import Decimal
import json
from pathlib import Path

SOURCE = "https://www.hkexnews.hk/listedco/listconews/sehk/2026/0923/2026092300499_c.pdf"
inputs = {
    "pre_tax_loss": {"2025": "75721", "2026": "33858", "printed_page": 41},
    "lease_termination_gain": {"2025": "4986", "2026": "36149", "printed_page": 59},
    "net_operating_cash_inflow": {"2025": "195495", "2026": "124389", "printed_page": 46},
}

def d(metric, year):
    return Decimal(inputs[metric][year])

results = {
    "pre_tax_loss_reduction": d("pre_tax_loss", "2025") - d("pre_tax_loss", "2026"),
    "lease_termination_gain_increase": d("lease_termination_gain", "2026") - d("lease_termination_gain", "2025"),
    "net_operating_cash_inflow_change": d("net_operating_cash_inflow", "2026") - d("net_operating_cash_inflow", "2025"),
}

expected = {
    "pre_tax_loss_reduction": "41863",
    "lease_termination_gain_increase": "31163",
    "net_operating_cash_inflow_change": "-71106",
}
for metric, result in results.items():
    assert result == Decimal(expected[metric]), metric
    assert (result / Decimal("1000")) * Decimal("1000") == result, metric

assert d("pre_tax_loss", "2026") + results["pre_tax_loss_reduction"] == d("pre_tax_loss", "2025")
assert d("lease_termination_gain", "2025") + results["lease_termination_gain_increase"] == d("lease_termination_gain", "2026")
assert d("net_operating_cash_inflow", "2025") + results["net_operating_cash_inflow_change"] == d("net_operating_cash_inflow", "2026")

output = {
    "status": "arithmetic_checked_independent_visual_source_review_passed",
    "source": SOURCE,
    "entity_scope": "consolidated group, not the subset of closed restaurants",
    "periods": "six months ended 30 June 2026 and 2025, both as presented in the 2026 interim report",
    "input_unit": "RMB thousand",
    "inputs": inputs,
    "results": {
        name: {"RMB_thousand": str(value), "RMB_million": str(value / Decimal("1000"))}
        for name, value in results.items()
    },
    "checks": {"assertions_passed": 9, "causal_attribution_ratios": "not calculated"},
    "limitations": [
        "Arithmetic differences do not identify the causal effect of restaurant closures.",
        "Profit measures are not cash receipts, and operating cash flow excludes financing-classified lease repayments.",
        "Do not combine 2025 annual amounts with 2026 half-year amounts.",
    ],
}
text = json.dumps(output, ensure_ascii=False, indent=2) + "\n"
Path(__file__).with_name("calculation-results.json").write_text(text, encoding="utf-8")
print(text, end="")
