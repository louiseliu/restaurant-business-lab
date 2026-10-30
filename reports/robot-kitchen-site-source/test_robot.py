import json,hashlib
from pathlib import Path
p=Path(__file__).parent/'robot-kitchen';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-10-30-robot-kitchen-note'
assert a['publishedAt']==a['updatedAt']=='2026-10-30T05:06:54Z'
assert '/6becd8035a336f37598f918a0089893dacd66337/' in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']
assert a['topics']==['business-model']
assert len(s['diagram']['nodes'])==3 and len(s['secondDiagram']['nodes'])==4
assert len(s['sections'])==4 and len(d['queries'])==2
assert d['buildStatus']=='complete'
assert '25%' not in json.dumps(s,ensure_ascii=False),'Do not move menu percentage into visual or narrative repetition'
assert 'data-app-local-thread' not in (p/'report.html').read_text()
print('Committed original/hash/time, business-model-only classification, two qualitative diagrams and offline metadata checks passed')
