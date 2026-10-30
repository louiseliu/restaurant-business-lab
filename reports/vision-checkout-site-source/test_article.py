import json,hashlib,re
from pathlib import Path
p=Path(__file__).parent/'vision-checkout';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-10-30-vision-checkout-note'
assert a['publishedAt']==a['updatedAt']=='2026-10-30T15:02:15Z'
assert '/98b377faa73538f6fd0168ceba7e7ec2f53faf8d/' in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']
assert a['topics']==['ai','business-model']
assert len(s['diagram']['nodes'])==2 and len(s['secondDiagram']['nodes'])==4
assert '不是已发生的客户事件' in s['diagram']['note']
assert '付款前取消' in s['secondDiagram']['nodes'][-1]['text']
assert len(s['sections'])==4 and len(d['queries'])==2 and d['buildStatus']=='complete'
h=(p/'report.html').read_text();assert 'data-app-local-thread' not in h
assert not re.search(r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)',h)
print('Original/hash/firstGit, two mechanism diagrams, payment boundary and offline metadata checks passed')
