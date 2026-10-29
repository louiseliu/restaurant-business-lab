#!/usr/bin/env python3
"""Copy reviewed outputs into app snapshot; no model calls, no network."""
import json,csv
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
def write():
 r=json.loads((ROOT/'results/analysis.json').read_text());q=json.loads((ROOT/'results/quality_report.json').read_text())
 with (ROOT/'results/cleaned_daily.csv').open(encoding='utf-8-sig') as f:raw=list(csv.DictReader(f))
 for row in raw:
  for k,v in list(row.items()):
   if k.endswith('_cents') or k in ['fulfilled_orders','refunded_orders','raw_csv_line']:row[k]=int(v)
 def readable(rows):
  for row in rows:
   for k,v in list(row.items()):
    if k.endswith('_cents'):row[k.replace('_cents','_yuan')]=v/100
   if 'channel' in row:row['channel_label']={'delivery':'外卖','dine_in':'堂食'}[row['channel']]
   if 'business_date' in row:row['day_label']=row['business_date'][5:]
   if 'store_id' in row:row['store_label']={'S01':'溪桥店（虚构）','S02':'长青店（虚构）'}[row['store_id']]
   if 'week' in row:row['week_label']={'W1':'前周 10/12–18','W2':'本周 10/19–25'}[row['week']]
  return rows
 definitions=[{'label':'商家净收入（元）','definition':'同一履约订单群：标价 − 商家优惠 − 客户退款；平台优惠由等额补贴补足，不重复加减。含税经营金额，非银行到账或会计收入。','formula':'(gross_sales_cents - merchant_discount_cents - refund_cents) / 100'},{'label':'所列成本后贡献（元）','definition':'商家净收入减食材、包装、平台服务费、支付费、商家配送和广告；未扣人工、租金、税费、折旧等，非净利润。','formula':'(merchant_net_revenue_cents - food_cost_cents - packaging_cost_cents - platform_fee_cents - payment_fee_cents - delivery_cost_cents - advertising_cost_cents) / 100'},{'label':'履约订单','definition':'同日期门店渠道已履约订单，包含部分退款订单；不含未履约取消；退款按原履约日归属。'}]
 queries={}
 for id,rows in [('weekly',r['weekly']),('channel_weekly',r['channel_weekly']),('store_weekly',r['store_weekly']),('store_channel_weekly',r['store_channel_weekly']),('daily',r['daily']),('raw_daily',raw),('channel_bridge',r['channel_delta_bridge'])]:
  queries[id]={'rows':readable(rows),'source':{'label':'完全模拟：两店 × 14日 × 堂食/外卖','files':['data/simulated_daily_raw.csv','src/analyze.py','results/analysis.json'],'filters':['2026-10-12 至 2026-10-25；W1/W2均完整7日','只含S01/S02两家虚构门店，已履约订单群'],'metricDefinitions':definitions,'caveats':['不是门店实测；没有测得省时/准确率提升','原记录粒度为日×店×渠道，不是逐笔订单；费用非完整成本','前后周变化是描述性，不能认定活动或AI因果效果'],'evidenceFlow':[{'title':'模拟输入','detail':'src/generate_sample.py 以固定公式生成57行原始CSV；数据SHA256 '+r['dataset_sha256']},{'title':'实际执行','detail':'python src/analyze.py；清理3处空白、映射1处别名、删1条完全重复；56行保留原CSV行号。78项金额/汇总检查通过。'},{'title':'独立回查','detail':'python src/test_analysis.py；独立SQLite从原CSV SELECT DISTINCT并重算周合计，另有缺值/冲突/缺分区等故障测试。'},{'title':'AI编制边界','detail':'当前AI助手读结果起草；没有调用外部模型API。脚本只作确定性计算，不能证明AI省时或准确率提升。'}]},'methods':[{'language':'python','code':'python src/generate_sample.py\npython src/analyze.py\npython src/test_analysis.py'}]}
 snapshot={'surface':'report','title':'经营数据 → AI 周报｜离线实战样板','generatedAt':'2026-10-29T03:12:25Z','status':'synthetic','buildStatus':'creating','filters':[],'report':{'asOf':'2026-10-28'},'exportPreferences':{'selected':None,'destinations':[]},'queries':queries,'samplePackage':{'analysis':r,'quality':q,'narrative':(ROOT/'docs/weekly_report.md').read_text(),'dictionary':(ROOT/'docs/data_dictionary.md').read_text(),'prompts':(ROOT/'docs/prompts.md').read_text(),'checklist':(ROOT/'docs/review_checklist.md').read_text()}}
 dest=ROOT/'reviewed-snapshot.json'
 # Preserve stable app identity when regenerating an existing snapshot.
 app=ROOT/'app/src/data.json'
 if app.exists():
  old=json.loads(app.read_text());snapshot['id']=old['id'];snapshot['buildStatus']='updating'
 dest.write_text(json.dumps(snapshot,ensure_ascii=False,indent=2)+'\n')
 if app.exists():app.write_text(dest.read_text())
 print('Prepared reviewed snapshot from actual calculation outputs')
if __name__=='__main__':write()
