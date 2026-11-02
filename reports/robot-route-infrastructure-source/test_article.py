import json,hashlib,re,sys
from pathlib import Path
p=Path(__file__).parent/'robot-route-infrastructure';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-11-02-robot-route-infrastructure-note'
assert a['publishedAt']==a['updatedAt']=='2026-11-02T06:14:57Z'
assert a['firstGit']=='6de175bcdd3afa7b3c5e4e72930369b55c305a8f' and a['firstGit'] in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']=='05deff48e778da0c4763ce98937ec7382843eb6f42e80d8a4db0ccf483f70c7d'
assert a['topics']==['business-model']
assert len(s['diagram']['nodes'])==4 and len(s['secondDiagram']['nodes'])==3
for suffix,k in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[k]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
pat=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_'
for f in p.glob('*.json'):assert not re.search(pat,f.read_text())
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert not re.search(pat,h);assert 'data-app-local-thread' not in h
print('Passed frozen full body, firstGit/time, two non-conflated mechanism diagrams, query/source binding and privacy')
