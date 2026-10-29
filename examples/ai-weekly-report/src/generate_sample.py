#!/usr/bin/env python3
"""Create only synthetic day × store × channel fixtures; no input/network."""
import csv, json, hashlib
from datetime import date, timedelta
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MONEY=['gross_sales_cents','merchant_discount_cents','platform_discount_cents','customer_paid_cents','refund_cents','platform_subsidy_cents','food_cost_cents','packaging_cost_cents','platform_fee_cents','payment_fee_cents','delivery_cost_cents','advertising_cost_cents']
FIELDS=['record_id','business_date','store_id','channel','fulfilled_orders','refunded_orders']+MONEY

def generate():
    rows=[]
    for day in range(14):
        d=date(2026,10,12)+timedelta(days=day); dow=day%7; week=day//7
        for si,store in enumerate(['S01','S02']):
            for channel in ['dine_in','delivery']:
                delivery=channel=='delivery'
                base=([64,50] if not delivery else [42,35])[si]
                orders=base+[0,3,-1,4,9,20,14][dow]+(week*([14,10][si]) if delivery else week*[-2,1][si])
                ticket=([4700,4500] if not delivery else [3900,3700])[si]+[0,50,-50,0,100,150,100][dow]-(150*week if delivery else 0)
                gross=orders*ticket
                merchant=round(gross*((0.09 if week==0 else 0.17) if delivery else .04))
                platdisc=round(gross*.04) if delivery else 0
                refunds=(2 if delivery else 1)+(4 if delivery and si==1 and week==1 and dow in [4,5] else 0)
                refund=refunds*(1500 if delivery else 1200)
                net=gross-merchant-refund
                row=dict(record_id=f'SIM-{d:%Y%m%d}-{store}-{"DL" if delivery else "DI"}',business_date=d.isoformat(),store_id=store,channel=channel,fulfilled_orders=orders,refunded_orders=refunds,
                    gross_sales_cents=gross,merchant_discount_cents=merchant,platform_discount_cents=platdisc,customer_paid_cents=gross-merchant-platdisc,refund_cents=refund,platform_subsidy_cents=platdisc,
                    food_cost_cents=round(gross*(.37+week*.015 if delivery else .33)),packaging_cost_cents=orders*(180 if delivery else 20),platform_fee_cents=round(net*.08) if delivery else 0,payment_fee_cents=round(net*.006),delivery_cost_cents=orders*300 if delivery else 0,advertising_cost_cents=(6000 if week==0 else 12000) if delivery else 0)
                rows.append(row)
    # Deliberate ingestion faults: exact re-export plus cosmetic variants only.
    raw=[dict(r) for r in rows]
    raw[1]['channel']='外卖'; raw[5]['store_id']=' S01 '; raw[12]['business_date']=' 2026-10-15 '; raw[33]['record_id']=' '+raw[33]['record_id']+' '
    raw.append(dict(raw[9]))
    path=ROOT/'data/simulated_daily_raw.csv'
    with path.open('w',newline='',encoding='utf-8-sig') as f:
        w=csv.DictWriter(f,fieldnames=FIELDS);w.writeheader();w.writerows(raw)
    manifest={'classification':'synthetic_only','generation':'Deterministic formulas in src/generate_sample.py; no external or private data','period':['2026-10-12','2026-10-25'],'timezone':'Asia/Shanghai business-date convention; no event timestamps','stores':{'S01':'溪桥店（虚构）','S02':'长青店（虚构）'},'canonical_rows':56,'raw_rows':57,'injected_faults':[{'csv_line':3,'kind':'channel_alias','raw':'外卖','normalized':'delivery'},{'csv_line':7,'kind':'trim_store_id'},{'csv_line':14,'kind':'trim_business_date'},{'csv_line':35,'kind':'trim_record_id'},{'csv_line':58,'kind':'exact_duplicate','first_csv_line':11}],'sha256':hashlib.sha256(path.read_bytes()).hexdigest()}
    (ROOT/'data/generation_manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n')
    print(f'Generated {len(raw)} raw rows, 56 canonical rows; SHA256 {manifest["sha256"]}')
if __name__=='__main__':generate()
