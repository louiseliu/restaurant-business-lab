"""Check disclosed hiring-time arithmetic, not causal effects or return on investment."""
from decimal import Decimal, localcontext
import json
from pathlib import Path


def main():
    old_days = Decimal("12")
    new_days = Decimal("4")
    with localcontext() as context:
        context.prec = 28
        days_reduced = old_days - new_days
        reduction = days_reduced / old_days
        reduction_percent = reduction * 100
        hypothetical_days_for_75_percent = old_days * (Decimal("1") - Decimal("0.75"))
        assert days_reduced == Decimal("8")
        assert new_days / old_days == Decimal("1") / Decimal("3")
        assert hypothetical_days_for_75_percent == Decimal("3")
        assert reduction_percent.quantize(Decimal("0.1")) == Decimal("66.7")
        assert reduction_percent != Decimal("75")
        result = {
            "scope": "Arithmetic of Chipotle's disclosed average days only; no AI causation, ROI or cross-store claim.",
            "source_date": "2025-02-19",
            "old_average_days": str(old_days),
            "new_average_days": str(new_days),
            "absolute_reduction_days": str(days_reduced),
            "relative_reduction_percent": str(reduction_percent),
            "relative_reduction_percent_rounded_1dp": str(reduction_percent.quantize(Decimal("0.1"))),
            "hypothetical_days_if_75_percent_reduction_from_12": str(hypothetical_days_for_75_percent),
            "hypothetical_warning": "This is an arithmetic assertion, not an observed business outcome or an explanation of the supplier's metric.",
            "assertions_passed": 5,
        }
    destination = Path(__file__).with_name("results.json")
    destination.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(destination.name)
    print("5 arithmetic assertions passed.")


if __name__ == "__main__":
    main()
