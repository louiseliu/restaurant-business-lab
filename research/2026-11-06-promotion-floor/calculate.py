"""作者假设情景；无门店数据，无平台阈值估计。"""
from decimal import Decimal as D
import json
from pathlib import Path

scenarios = [
    {"id": "idle_positive", "settlement_net": "12.00", "remaining_variable_cost": "8.00", "displaced_order_contribution": "0.00", "expected_order_contribution": "4.00", "expected_relative_contribution": "4.00"},
    {"id": "cost_drift", "settlement_net": "12.00", "remaining_variable_cost": "13.00", "displaced_order_contribution": "0.00", "expected_order_contribution": "-1.00", "expected_relative_contribution": "-1.00"},
    {"id": "one_for_one_peak_displacement", "settlement_net": "12.00", "remaining_variable_cost": "8.00", "displaced_order_contribution": "5.00", "expected_order_contribution": "4.00", "expected_relative_contribution": "-1.00"},
]
results = []
for s in scenarios:
    contribution = D(s["settlement_net"]) - D(s["remaining_variable_cost"])
    relative = contribution - D(s["displaced_order_contribution"])
    assert contribution == D(s["expected_order_contribution"])
    assert relative == D(s["expected_relative_contribution"])
    results.append({"id": s["id"], "settlementNetCNY": s["settlement_net"], "notYetDeductedVariableCostCNY": s["remaining_variable_cost"], "displacedContributionCNY": s["displaced_order_contribution"], "orderContributionCNY": str(contribution), "relativeContributionCNY": str(relative)})
# Prevent double subtraction of a fee already included in settlement.
gross_before_fee, already_deducted_fee, other_cost = D("14"), D("2"), D("8")
assert gross_before_fee - already_deducted_fee - other_cost == D("12") - other_cost == D("4")
# A positive order contribution does not establish total shop profit.
assert D("4") * D("100") - D("500") == D("-100")
out = {"kind": "author_assumed_scenarios_not_measured_results", "currency": "CNY", "checksPassed": 8, "formula": "orderContribution = settlementNet - notYetDeductedVariableCost; relativeContribution = orderContribution - displacedContribution", "limitations": ["No platform alert threshold is assumed or estimated.", "Displacement scenario assumes exactly one otherwise-completed alternative order is lost; not an empirical substitution rate.", "No campaign causal effect, total shop net profit, or ROI is estimated.", "Final settlement and costs must use one consistent tax, refund, fee and observation scope."], "scenarios": results}
Path(__file__).with_name("calculation-results.json").write_text(json.dumps(out, ensure_ascii=False, indent=2) + "\n")
print(json.dumps({"checksPassed": 8, "scenarios": len(results)}, ensure_ascii=False))
