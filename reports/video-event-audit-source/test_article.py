import json,hashlib,re,sys
from pathlib import Path
p=Path(__file__).parent/'video-event-audit';a=json.loads((p/'article-entry.json').read_text());s=json.loads((p/'illustrated-story.json').read_text());d=json.loads((p/'article-reviewed-data.json').read_text())
assert a['id']==s['id']=='research-2026-10-30-video-event-audit-note'
assert a['publishedAt']==a['updatedAt']=='2026-10-30T18:06:06Z'
assert '/9ba2df51078bbd601df171b7025dbbd851529f96/' in a['sourceUrl']
assert hashlib.sha256(a['body'].encode()).hexdigest()==a['originalBodySha256']
assert a['topics']==['ai','business-model']
assert len(s['diagram']['nodes'])==len(s['secondDiagram']['nodes'])==4
assert [v['title'].split('｜')[0] for v in s['diagram']['nodes']]==['案例披露','案例披露','建议','建议']
assert '不是正新已公开验证' in s['diagram']['scope']
assert '不利评价或处罚' in a['body']
assert len(d['queries'])==2 and d['buildStatus']=='complete'
for suffix,key in [('', 'diagram'),(':second','secondDiagram')]:
 q='diagram-'+a['id']+suffix;assert d['queries'][q]['rows']==s[key]['nodes'];assert d['queries'][q]['source']['metricDefinitions'][0]['componentIds']==[q]
for f in p.glob('*.json'):
 t=f.read_text();assert not re.search(r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_',t)
if len(sys.argv)>1:
 h=Path(sys.argv[1]).read_text();assert 'data-app-local-thread' not in h;assert not re.search(r'https?://(?:www\.)?chatgpt\.com/(?:g/|c/|share/)|/workspace/|/home/agent/|appgprj_|libfile_',h)
print('Passed full-body/hash/firstGit, disclosure-vs-recommendation, both query bindings and privacy checks')
