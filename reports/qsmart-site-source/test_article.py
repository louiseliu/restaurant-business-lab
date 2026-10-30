import json,hashlib
from pathlib import Path
p=Path(__file__).parent/'qsmart';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-10-30-qsmart-note'
assert a['publishedAt']==a['updatedAt']=='2026-10-30T07:29:17Z'
assert '/2d35d3947a51ebafdf8097d393ce49d6db457411/' in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']
assert a['topics']==['ai','business-model']
assert [n['title'] for n in s['diagram']['nodes']]==['发现缺员','建议替补人员','发起电话']
for term in ['拨号前','员工接受','班表写入','实际到岗','成功率','未披露不等于未实现']:assert term in s['diagram']['note']
assert len(s['sections'])==4 and len(d['queries'])==2 and d['buildStatus']=='complete'
assert 'data-app-local-thread' not in (p/'report.html').read_text()
print('Original/hash/firstGit, AI classification, disclosed endpoint, unknown boundary and offline metadata checks passed')
