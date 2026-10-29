#!/usr/bin/env python3
"""Independent arithmetic and fail-closed regression tests; stdlib only."""
import unittest,csv,copy,json,sqlite3
from pathlib import Path
from analyze import clean_rows,ratio,ROOT
class Checks(unittest.TestCase):
 @classmethod
 def setUpClass(cls):
  with (ROOT/'data/simulated_daily_raw.csv').open(encoding='utf-8-sig') as f:cls.raw=list(csv.DictReader(f))
  cls.cleaned,cls.actions=clean_rows(cls.raw)
 def test_shape_and_duplicate(self):
  self.assertEqual(len(self.raw),57);self.assertEqual(len(self.cleaned),56);self.assertEqual(sum(x['action']=='drop_exact_duplicate' for x in self.actions),1)
 def test_normalization_preserves_amounts(self):
  self.assertEqual(sum(x['action']=='trim_whitespace' for x in self.actions),3);self.assertEqual(sum(x['action']=='documented_alias' for x in self.actions),1)
  self.assertEqual(self.cleaned[1]['channel'],'delivery')
 def test_missing_value_rejected(self):
  r=copy.deepcopy(self.raw);r[0]['food_cost_cents']='';self.assertRaisesRegex(ValueError,'missing',clean_rows,r)
 def test_conflicting_duplicate_rejected(self):
  r=copy.deepcopy(self.raw);r[-1]['food_cost_cents']=str(int(r[-1]['food_cost_cents'])+1);self.assertRaisesRegex(ValueError,'conflicting duplicate',clean_rows,r)
 def test_missing_partition_rejected(self):
  self.assertRaisesRegex(ValueError,'incomplete partition',clean_rows,self.raw[1:])
 def test_negative_cost_rejected(self):
  r=copy.deepcopy(self.raw);r[0]['food_cost_cents']='-1';self.assertRaisesRegex(ValueError,'non-negative',clean_rows,r)
 def test_schema_change_rejected(self):
  r=copy.deepcopy(self.raw);r[0]['extra_column']='0';self.assertRaisesRegex(ValueError,'Schema',clean_rows,r)
 def test_duplicate_grain_different_id_rejected(self):
  r=copy.deepcopy(self.raw);r[-1]['record_id']='NEW-ID';self.assertRaisesRegex(ValueError,'grain',clean_rows,r)
 def test_zero_refund_count_with_amount_rejected(self):
  r=copy.deepcopy(self.raw);r[0]['refunded_orders']='0';self.assertRaisesRegex(ValueError,'mismatch',clean_rows,r)
 def test_platform_subsidy_assumption_rejected(self):
  r=copy.deepcopy(self.raw);r[1]['platform_subsidy_cents']='0';self.assertRaisesRegex(ValueError,'subsidy',clean_rows,r)
 def test_unknown_channel_rejected(self):
  r=copy.deepcopy(self.raw);r[0]['channel']='takeaway_unknown';self.assertRaisesRegex(ValueError,'unknown',clean_rows,r)
 def test_payment_bridge_rejected(self):
  r=copy.deepcopy(self.raw);r[0]['customer_paid_cents']=str(int(r[0]['customer_paid_cents'])+1);self.assertRaisesRegex(ValueError,'bridge',clean_rows,r)
 def test_refund_count_rejected(self):
  r=copy.deepcopy(self.raw);r[0]['refunded_orders']='9999';self.assertRaisesRegex(ValueError,'refund count',clean_rows,r)
 def test_zero_denominator_is_unknown(self):self.assertIsNone(ratio(0,0))
 def test_independent_sql_recompute(self):
  # Independent method: read raw strings, normalize, SELECT DISTINCT then SQL SUM.
  con=sqlite3.connect(':memory:');cols=list(self.raw[0]);con.execute('CREATE TABLE raw('+','.join(k+' TEXT' for k in cols)+')')
  con.executemany('INSERT INTO raw VALUES ('+','.join('?' for _ in cols)+')',[[r[k] for k in cols] for r in self.raw])
  norms=[("CASE TRIM(channel) WHEN '外卖' THEN 'delivery' ELSE TRIM(channel) END" if k=='channel' else 'TRIM('+k+')')+' AS '+k for k in cols]
  sql='WITH clean AS (SELECT DISTINCT '+','.join(norms)+' FROM raw) SELECT CASE WHEN business_date < \'2026-10-19\' THEN \'W1\' ELSE \'W2\' END week, COUNT(*), SUM(CAST(fulfilled_orders AS INTEGER)), SUM(CAST(gross_sales_cents AS INTEGER)-CAST(merchant_discount_cents AS INTEGER)-CAST(refund_cents AS INTEGER)), SUM(CAST(gross_sales_cents AS INTEGER)-CAST(merchant_discount_cents AS INTEGER)-CAST(refund_cents AS INTEGER)-CAST(food_cost_cents AS INTEGER)-CAST(packaging_cost_cents AS INTEGER)-CAST(platform_fee_cents AS INTEGER)-CAST(payment_fee_cents AS INTEGER)-CAST(delivery_cost_cents AS INTEGER)-CAST(advertising_cost_cents AS INTEGER)) FROM clean GROUP BY week ORDER BY week'
  found=con.execute(sql).fetchall();expected=json.loads((ROOT/'results/analysis.json').read_text())['weekly']
  self.assertEqual(found,[(x['week'],x['row_count'],x['fulfilled_orders'],x['merchant_net_revenue_cents'],x['contribution_cents']) for x in expected])
  (ROOT/'qa/independent_recompute.sql').write_text(sql+';\n')
  (ROOT/'qa/independent_recompute.json').write_text(json.dumps({'method':'SQLite SUM from independently normalized DISTINCT raw rows','columns':['week','row_count','fulfilled_orders','merchant_net_revenue_cents','contribution_cents'],'rows':found},ensure_ascii=False,indent=2)+'\n')
 def test_report_claims_against_calculation(self):
  r=json.loads((ROOT/'results/analysis.json').read_text());a,b=r['weekly'];cl=json.loads((ROOT/'docs/claims_manifest.json').read_text())
  for claim in cl:
   collection=r[claim['collection']];row=collection if isinstance(collection,dict) else next(x for x in collection if all(x[k]==v for k,v in claim['where'].items()));self.assertAlmostEqual(row[claim['metric']],claim['expected'],places=8,msg=claim['id'])
  self.assertGreater(b['merchant_net_revenue_cents'],a['merchant_net_revenue_cents']);self.assertLess(b['contribution_cents'],a['contribution_cents'])
if __name__=='__main__':unittest.main(verbosity=2)
