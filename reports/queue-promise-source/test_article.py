import json,hashlib,re,sys
from pathlib import Path
p=Path(__file__).parent/'queue-promise';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-10-31-queue-promise-note'
assert a['publishedAt']==a['updatedAt']=='2026-10-31T16:08:16Z'
assert a['firstGit']=='10edb1edb9311446f8f524c62f1f9c35e390c1ed' and a['firstGit'] in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']=='cfa6ae5f4328964a43e9de41bdf55c487588d170b500e012f33ea053dba771be'
assert a['topics']==['ai','business-model']
assert len(s['diagram']['nodes'])==3 and len(s['secondDiagram']['nodes'])==4
assert '无真实时长比例' in s['diagram']['scope'] and '研究建议' in s['secondDiagram']['scope']
for suffix,k in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[k]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
pat=r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_'
for f in p.glob('*.json'):assert not re.search(pat,f.read_text())
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert not re.search(pat,h);assert 'data-app-local-thread' not in h
print('Passed frozen full body, firstGit/time, two non-conflated mechanism diagrams, query/source binding and privacy')
