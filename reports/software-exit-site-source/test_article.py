import json,hashlib
from pathlib import Path
p=Path(__file__).parent/'software-exit';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-10-30-software-exit-note'
assert a['publishedAt']==a['updatedAt']=='2026-10-30T06:14:48Z'
assert '/1dd3d0510b28581dc12bc6b50cf9f4ff691b2c36/' in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']
assert a['topics']==['business-model']
assert len(s['diagram']['nodes'])==len(s['secondDiagram']['nodes'])==3
assert len(s['sections'])==4 and len(d['queries'])==2
assert d['buildStatus']=='complete'
assert '正常后台' in s['secondDiagram']['note'] and '未承诺统一免费' in s['secondDiagram']['note']
assert 'data-app-local-thread' not in (p/'report.html').read_text()
print('Committed original/hash/time, classification, two qualitative diagrams, balanced boundary and offline metadata checks passed')
