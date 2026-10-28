#!/usr/bin/env python3
"""Reproduce the FY2019 UK reported like-for-like definition gap; not a causal estimate."""
from decimal import Decimal
import json

source = "https://investors.dominos.co.uk/system/files/press/prelims-results-2019.pdf"
excluding_splits = Decimal("3.7")  # Source p.1: percentage growth, not a fraction.
including_splits = Decimal("1.9")  # Source p.1: percentage growth, not a fraction.
gap_pp = excluding_splits - including_splits
assert gap_pp == Decimal("1.8")
assert gap_pp * Decimal("100") == Decimal("180")
result = {
    "entity": "Domino's Pizza Group plc",
    "market": "UK",
    "fiscal_period": "52 weeks ended 2019-12-29",
    "source_published": "2020-03-05",
    "source_url": source,
    "source_pages": {"growth_rates": 1, "definitions_footnotes_2_and_7": 2},
    "inputs_are_reported_rounded_percentages": True,
    "excluding_splits_growth_percent": str(excluding_splits),
    "including_splits_growth_percent": str(including_splits),
    "formula": "3.7 - 1.9",
    "definition_gap_percentage_points": str(gap_pp),
    "interpretation": "Difference between reported growth rates with different sample exclusions.",
    "not_identified": [
        "Causal effect of store splitting",
        "Growth of the excluded donor-store cohort",
        "Amount of transferred or lost sales",
        "Franchisee profit or return on investment",
    ],
    "cross_period_limit": "No projection of this FY2019 UK gap to FY2025 UK & Ireland.",
}
print(json.dumps(result, ensure_ascii=False, indent=2))
