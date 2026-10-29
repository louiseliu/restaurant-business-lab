#!/usr/bin/env python3
"""Strict local data quality, integer-cent arithmetic and auditable aggregation."""
import csv,json,hashlib,argparse
from collections import defaultdict
from datetime import date,timedelta
from pathlib import Path
from generate_sample import FIELDS,MONEY
ROOT=Path(__file__).resolve().parents[1]
SUM_FIELDS=['fulfilled_orders','refunded_orders']+MONEY+['merchant_net_revenue_cents','specified_costs_cents','contribution_cents']
COSTS=['food_cost_cents','packaging_cost_cents','platform_fee_cents','payment_fee_cents','delivery_cost_cents','advertising_cost_cents']
START=date(2026,10,12);END=date(2026,10,25)

def clean_rows(raw):
    cleaned=[]; actions=[];seen={}; business_keys={}
    for line,r0 in enumerate(raw,2):
        if set(r0)!=set(FIELDS):raise ValueError('Schema differs from dictionary')
        r=dict(r0)
        for k,v in r.items():
            if v is None or not str(v).strip():raise ValueError(f'line {line}: missing {k}; never impute zero')
            if v!=v.strip():actions.append({'csv_line':line,'record_id':r['record_id'].strip(),'action':'trim_whitespace','field':k,'before':v,'after':v.strip()})
            r[k]=v.strip()
        if r['channel']=='外卖':
            actions.append({'csv_line':line,'record_id':r['record_id'],'action':'documented_alias','field':'channel','before':'外卖','after':'delivery'});r['channel']='delivery'
        for k in ['fulfilled_orders','refunded_orders']+MONEY:
            if not r[k].isdigit():raise ValueError(f'line {line}: non-negative integer required for {k}')
            r[k]=int(r[k])
        if r['store_id'] not in ['S01','S02'] or r['channel'] not in ['dine_in','delivery']:raise ValueError('unknown store/channel')
        d=date.fromisoformat(r['business_date'])
        if not START<=d<=END:raise ValueError('date outside declared 14-day closed window')
        ident=r['record_id'];bk=(r['business_date'],r['store_id'],r['channel'])
        if ident in seen:
            if {k:seen[ident][k] for k in FIELDS}!=r:raise ValueError(f'conflicting duplicate id: {ident}')
            actions.append({'csv_line':line,'record_id':ident,'action':'drop_exact_duplicate','kept_csv_line':seen[ident]['raw_csv_line']});continue
        if bk in business_keys:raise ValueError(f'conflicting day/store/channel grain: {bk}')
        if not 0<=r['refunded_orders']<=r['fulfilled_orders']:raise ValueError('refund count > fulfilled count')
        if r['fulfilled_orders']==0 and any(r[k] for k in MONEY if k!='advertising_cost_cents'):raise ValueError('zero orders with transaction amounts')
        if (r['refunded_orders']==0)!=(r['refund_cents']==0):raise ValueError('refund count/amount mismatch')
        if r['gross_sales_cents']-r['merchant_discount_cents']-r['platform_discount_cents']!=r['customer_paid_cents']:raise ValueError('customer payment bridge failed')
        if r['platform_subsidy_cents']!=r['platform_discount_cents']:raise ValueError('sample assumes subsidy equals platform discount; clawback unsupported')
        if r['refund_cents']>r['customer_paid_cents']:raise ValueError('refund exceeds customer paid')
        if r['channel']=='dine_in' and any(r[k] for k in ['platform_discount_cents','platform_subsidy_cents','platform_fee_cents','delivery_cost_cents']):raise ValueError('dine-in has unsupported platform/delivery amount')
        r['raw_csv_line']=line;r['week']='W1' if d<date(2026,10,19) else 'W2'
        r['merchant_net_revenue_cents']=r['customer_paid_cents']-r['refund_cents']+r['platform_subsidy_cents']
        if r['merchant_net_revenue_cents']!=r['gross_sales_cents']-r['merchant_discount_cents']-r['refund_cents']:raise ValueError('merchant revenue bridge failed')
        r['specified_costs_cents']=sum(r[k] for k in COSTS)
        r['contribution_cents']=r['merchant_net_revenue_cents']-r['specified_costs_cents']
        seen[ident]=r;business_keys[bk]=ident;cleaned.append(r)
    expected={( (START+timedelta(days=d)).isoformat(),s,c) for d in range(14) for s in ['S01','S02'] for c in ['dine_in','delivery']}
    if set(business_keys)!=expected:raise ValueError(f'incomplete partition coverage: missing={sorted(expected-set(business_keys))}')
    return cleaned,actions

def ratio(n,d):return None if d==0 else n/d

def aggregate(rows,keys):
    groups=defaultdict(list)
    for row in rows:groups[tuple(row[k] for k in keys)].append(row)
    result=[]
    for key,rs in sorted(groups.items()):
        d=dict(zip(keys,key));d.update({k:sum(r[k] for r in rs) for k in SUM_FIELDS})
        d.update(row_count=len(rs),source_record_ids=[r['record_id'] for r in rs],raw_csv_lines=[r['raw_csv_line'] for r in rs],net_per_order_yuan=ratio(d['merchant_net_revenue_cents'],100*d['fulfilled_orders']),contribution_per_order_yuan=ratio(d['contribution_cents'],100*d['fulfilled_orders']),contribution_rate=ratio(d['contribution_cents'],d['merchant_net_revenue_cents']),refund_order_rate=ratio(d['refunded_orders'],d['fulfilled_orders']),merchant_discount_rate=ratio(d['merchant_discount_cents'],d['gross_sales_cents']))
        result.append(d)
    return result

def writecsv(path,rows):
    if not rows:return
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=rows[0].keys());w.writeheader();w.writerows(rows)

def run(input_path=None,out=None):
    inp=Path(input_path) if input_path else ROOT/'data/simulated_daily_raw.csv';out=Path(out) if out else ROOT/'results';out.mkdir(parents=True,exist_ok=True)
    with inp.open(encoding='utf-8-sig',newline='') as f:raw=list(csv.DictReader(f))
    rows,actions=clean_rows(raw)
    weekly=aggregate(rows,['week']);channel=aggregate(rows,['week','channel']);store=aggregate(rows,['week','store_id']);sc=aggregate(rows,['week','store_id','channel']);daily=aggregate(rows,['business_date'])
    a,b=weekly;comparisons=[]
    for key in ['fulfilled_orders','merchant_net_revenue_cents','contribution_cents','net_per_order_yuan','contribution_per_order_yuan','refund_order_rate','contribution_rate']:
        comparisons.append({'metric':key,'W1':a[key],'W2':b[key],'absolute_change':b[key]-a[key],'relative_change':ratio(b[key]-a[key],a[key]),'rate_change_pp':(b[key]-a[key])*100 if key.endswith('_rate') else None})
    checks=[]
    def check(name,ok,detail):
        checks.append({'check':name,'passed':bool(ok),'detail':detail})
        if not ok:raise AssertionError(name)
    check('partition_coverage',len(rows)==56,'2 stores × 14 complete business days × 2 channels; 28 rows per week')
    check('unique_grain',len({(r['business_date'],r['store_id'],r['channel']) for r in rows})==56,'Exactly one accepted row per day/store/channel')
    check('normalized_raw_row_accounting',len(raw)==len(rows)+sum(x['action']=='drop_exact_duplicate' for x in actions),'57 raw = 56 accepted + 1 exact duplicate; no silently discarded business rows')
    for w in weekly:
        for key in SUM_FIELDS:
            check('channel_to_total_'+w['week']+'_'+key,sum(r[key] for r in channel if r['week']==w['week'])==w[key],'Mutually exclusive channels reconcile')
            check('store_to_total_'+w['week']+'_'+key,sum(r[key] for r in store if r['week']==w['week'])==w[key],'Mutually exclusive stores reconcile')
        check('payment_bridge_'+w['week'],w['gross_sales_cents']-w['merchant_discount_cents']-w['platform_discount_cents']==w['customer_paid_cents'],'gross − merchant discount − platform discount = customer paid before refund')
        check('net_revenue_bridge_'+w['week'],w['customer_paid_cents']-w['refund_cents']+w['platform_subsidy_cents']==w['merchant_net_revenue_cents'],'customer paid − customer refund + settled platform subsidy = merchant net revenue')
        check('contribution_bridge_'+w['week'],w['merchant_net_revenue_cents']-sum(w[k] for k in COSTS)==w['contribution_cents'],'net revenue − six specified costs; excludes fixed labor/rent/tax etc.')
    contributions=[]
    for c in ['dine_in','delivery']:
        x=next(r for r in channel if r['week']=='W1' and r['channel']==c);y=next(r for r in channel if r['week']=='W2' and r['channel']==c)
        contributions.append({'channel':c,'revenue_delta_cents':y['merchant_net_revenue_cents']-x['merchant_net_revenue_cents'],'contribution_delta_cents':y['contribution_cents']-x['contribution_cents'],'orders_delta':y['fulfilled_orders']-x['fulfilled_orders'],'W1_contribution_per_order_yuan':x['contribution_per_order_yuan'],'W2_contribution_per_order_yuan':y['contribution_per_order_yuan']})
    check('channel_delta_bridge',sum(x['contribution_delta_cents'] for x in contributions)==b['contribution_cents']-a['contribution_cents'],'Arithmetic contribution, not causal attribution')
    # Transparent adverse sensitivity: additional hypothetical food cost, not forecast.
    cost_bridge=[{'component':'merchant_net_revenue_cents','W1_cents':a['merchant_net_revenue_cents'],'W2_cents':b['merchant_net_revenue_cents'],'contribution_effect_cents':b['merchant_net_revenue_cents']-a['merchant_net_revenue_cents']}] + [{'component':k,'W1_cents':a[k],'W2_cents':b[k],'contribution_effect_cents':-(b[k]-a[k])} for k in COSTS]
    # Reconciliation already covered by aggregate contribution bridge; retain exact components.
    assert sum(x['contribution_effect_cents'] for x in cost_bridge)==b['contribution_cents']-a['contribution_cents']
    scenario={'classification':'hypothetical sensitivity, not observed','extra_food_cost_rate_of_W2_gross':.01,'extra_food_cost_cents':round(b['gross_sales_cents']*.01),'W2_contribution_after_extra_cost_cents':b['contribution_cents']-round(b['gross_sales_cents']*.01)}
    result={'classification':'模拟数据；本包AI辅助编制并经计算回查，非门店实测；没有测得省时/准确率提升','dataset_sha256':hashlib.sha256(inp.read_bytes()).hexdigest(),'periods':{'W1':'2026-10-12—2026-10-18','W2':'2026-10-19—2026-10-25'},'weekly':weekly,'channel_weekly':channel,'store_weekly':store,'store_channel_weekly':sc,'daily':daily,'comparisons':comparisons,'channel_delta_bridge':contributions,'sensitivity':scenario,'cost_delta_bridge':cost_bridge}
    qa={'raw_rows':len(raw),'accepted_rows':len(rows),'actions':actions,'checks':checks,'checks_passed':sum(c['passed'] for c in checks),'critical_failures':0,'limitations':['Synthetic arithmetic validation, not real-store reconciliation','No order-level IDs: drilldown ends at raw day/store/channel aggregate','No invoice or platform statement supplied','No saved labor-time or AI accuracy evaluation; no external model API call']}
    for file,data in [('analysis.json',result),('quality_report.json',qa)]: (out/file).write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')
    writecsv(out/'cleaned_daily.csv',rows)
    for name,data in [('weekly_summary',weekly),('channel_weekly',channel),('store_weekly',store),('store_channel_weekly',sc),('daily_summary',daily),('metric_comparisons',comparisons)]:writecsv(out/(name+'.csv'),data)
    print(json.dumps({'raw_rows':len(raw),'accepted_rows':len(rows),'passed_checks':len(checks),'weekly':[{'week':w['week'],'orders':w['fulfilled_orders'],'merchant_net_yuan':w['merchant_net_revenue_cents']/100,'contribution_yuan':w['contribution_cents']/100} for w in weekly]},ensure_ascii=False,indent=2))
    return result,qa
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--input');p.add_argument('--out');args=p.parse_args();run(args.input,args.out)
