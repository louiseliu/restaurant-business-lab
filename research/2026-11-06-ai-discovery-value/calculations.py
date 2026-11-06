"""复算公开来源的计数；不验证原始订单或复现论文数据。"""
import json
from fractions import Fraction


def calculate():
    bookings, visitors = 3, 34
    queries = 96
    repeats = {"OpenAI": 5, "Anthropic": 3, "Google": 5, "Perplexity": 10}
    percentage = float(Fraction(bookings, visitors) * 100)
    return {
        "booking_ratio": {
            "bookings": bookings,
            "visitors": visitors,
            "percentage": percentage,
            "rounded_one_decimal": round(percentage, 1),
            "limit": "服务商自报计数复算；未核订单，不识别增量或利润。",
        },
        "audit_run_count": {
            "queries": queries,
            "repetitions_per_query": repeats,
            "computed_responses": queries * sum(repeats.values()),
            "reported_responses": 2208,
            "limit": "仅校验论文设计计数，不复现审计数据或验证效果。",
        },
    }


if __name__ == "__main__":
    result = calculate()
    assert result["booking_ratio"]["rounded_one_decimal"] == 8.8
    assert result["audit_run_count"]["computed_responses"] == result["audit_run_count"]["reported_responses"]
    print(json.dumps(result, ensure_ascii=False, indent=2))
