"""Illustrative table reset timing; not Haidilao or restaurant observations."""
import json
from pathlib import Path

def calculate(noticed, cleaner_available, cleaning_minutes, guest_ready):
    cleaning_start = max(noticed, cleaner_available)
    table_ready = cleaning_start + cleaning_minutes
    # The host receives ready-table information immediately; no synchronization wait.
    host_informed = table_ready
    seated = max(host_informed, guest_ready)
    return dict(noticed=noticed, cleaning_start=cleaning_start, table_ready=table_ready, host_informed=host_informed, seated=seated)

cases = [
    ('information_delay', '人员和合适顾客已可用', 0, 0),
    ('cleaner_busy', '清台人员第8分钟才能接手', 8, 0),
    ('guest_not_ready', '合适顾客第14分钟才准备好入座', 0, 14),
]
rows=[]
for key,label,staff,guest in cases:
    old=calculate(6,staff,4,guest)
    ai=calculate(1,staff,4,guest)
    rows.append(dict(id=key,label=label,cleaner_available=staff,guest_ready=guest,baseline=old,earlier_notice=ai,seating_minutes_saved=old['seated']-ai['seated']))
assert [r['seating_minutes_saved'] for r in rows] == [5,0,0]
assert rows[1]['baseline']['table_ready'] == rows[1]['earlier_notice']['table_ready'] == 12
assert rows[2]['baseline']['seated'] == rows[2]['earlier_notice']['seated'] == 14
assert all(r[variant]['host_informed'] == r[variant]['table_ready'] for r in rows for variant in ('baseline', 'earlier_notice'))
result={
 'status':'author_constructed_illustration_not_measured',
 'unit':'minutes after prior party leaves',
 'assumptions':[
  'One suitable table, one next party and one cleaner; no priority displacement or interactions with other tables.',
  'Only notice time changes: minute 6 to minute 1. Neither value is a measured AI capability.',
  'Notice means the responsible person has actionable departure information, not that a camera has just produced an output. It is not a claim of automated staff dispatch in the cited system.',
  'Cleaner availability and guest readiness are fixed exogenous times, unchanged by the earlier notice; seating escort time is ignored.',
  'Cleaning and reset take 4 minutes in every case; an illustrative input, not a target or safety standard.',
  'The host receives ready-table information immediately when the table is ready. No synchronization waiting time is modeled at this step.',
  'Restaurant permits seating as soon as the table and party are ready; service and kitchen capacity are assumed available.',
  'No extra sales, causal effects, labor savings, or ROI are calculated.'
 ],
 'formulas':{'cleaning_start':'max(noticed, cleaner_available)','table_ready':'cleaning_start + cleaning_minutes','host_informed':'table_ready (zero synchronization wait)','seated':'max(host_informed, guest_ready)'},
 'scenarios':rows
}
print(json.dumps(result,ensure_ascii=False,indent=2))
if __name__=='__main__':
    Path(__file__).with_name('scenarios.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
