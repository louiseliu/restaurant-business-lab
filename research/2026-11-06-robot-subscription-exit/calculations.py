#!/usr/bin/env python3
"""复算供应商历史月价的12个月尺度，不构造租期或合同总价。"""
import json
from pathlib import Path

monthly_cny = [2000, 4000]
months_assumed = 12
result = {
    "source": "https://www.acewill.cn/news-detail/298.html",
    "source_published": "2025-05-28",
    "currency": "CNY",
    "monthly_price_stated": monthly_cny,
    "comparison_months_assumed_by_researcher": months_assumed,
    "payments_over_assumed_period": [price * months_assumed for price in monthly_cny],
    "formula": "monthly_price_stated * comparison_months_assumed_by_researcher",
    "exclusions": "未知附加费用、税费、押金、调料、安装/改造、退出、资金时间价值及收益；不是完整合同或全流程成本。",
    "boundary": "12个月不是公开租期，历史月价不是当前正式报价；不用于与其他品牌设备价直接比较。"
}
assert result["payments_over_assumed_period"] == [24000, 48000]
out = Path(__file__).with_name("calculation-results.json")
out.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
print(json.dumps(result, ensure_ascii=False))
