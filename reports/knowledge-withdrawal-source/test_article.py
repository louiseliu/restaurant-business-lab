import json,hashlib,re,sys
from pathlib import Path
p=Path(__file__).parent/'knowledge-withdrawal';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-10-31-knowledge-withdrawal-note'
assert a['publishedAt']==a['updatedAt']=='2026-10-31T09:01:42Z'
assert a['firstGit']=='c9978c300b1a8acb4c5b597c097e08022d9fd55f' and a['firstGit'] in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']=='7189b221fc75884d72fdfae0a45ef4c0014c1f3d5ebf2e56a99508ed491dca8b'
assert a['topics']==['ai','business-model']
assert len(s['diagram']['nodes'])==len(s['secondDiagram']['nodes'])==3
assert '假设' in s['diagram']['scope'] and '不是同一开关' in s['secondDiagram']['scope']
for suffix,k in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[k]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
pat=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_'
for f in p.glob('*.json'):assert not re.search(pat,f.read_text())
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert not re.search(pat,h);assert 'data-app-local-thread' not in h
print('Passed frozen full body, firstGit/time, two non-conflated mechanism diagrams, query/source binding and privacy')
